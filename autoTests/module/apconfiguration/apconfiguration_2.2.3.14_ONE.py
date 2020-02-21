#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.3.14_ONE.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features: 
# 2.2.3.14	Controller分组独立升级状态测试(合并用例2.2.3.14，2.2.3.15，2.2.3.16)
# 测试目的： 
# 2.2.3.14 分组手动独立升级AP image：Controller上可以wireless ap download start 触发手动独立升级所有ap，
# 第一组ap先下载Image，show wireless ap download显示前x个ap状态处于Code Transfer In Progress，
# 其它等待ap状态处于Requested（使用wireless ap download group-size x配置每组同时下载Image的 AP数目小于目前管理AP数）
# 2.2.3.15 分组手动独立升级AP image：Controller上可以wireless ap download start 触发手动独立升级所有ap，
# 下载完Image的ap状态处于Waiting For APs To Dow，正在下载的ap状态处于Code Transfer In Progress，
# 其它等待ap状态处于Requested
# 2.2.3.16 分组手动独立升级AP image：Controller上可以wireless ap download start 触发手动独立升级所有ap，
# ap全部下载完Image后状态都为NVRAM Update In Progress，ap全部重启后被AC管理，image版本已经更新成功。
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.4.2
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'apconfiguration_2.2.3.14-16'
avoiderror(testname)
printTimer(testname,'Start','controller set ap download group-size x',
           'only x aps are downloading image at the same time',
           'ap that is downloading image is in Code Transfer In Progress status',
           'ap that does not start downloading image is in Requested status',
           'ap that have finished downloading image is in Waiting For APs To Dow status',
           'aps change to NVRAM Update In Progress status after all aps finish downloading image')
###############################################################################
#Step 1
#操作
# 在AC1上配置discovery ip-list StaticIpv4_ac2
# 在AP2上配置管理AC的地址为AC2的IP
# set managed-ap switch-address-1 ac2_ip
# 重启AP2
# 预期
# AC1和AC2建立集群关系
# AP2被AC2成功管理
################################################################################
printStep(testname,'Step 1',
          'config discovery ip-list StaticIpv4_ac2 on ac1',
          'ap2 set managed-ap switch-address-1 ac2_ip',
          'reboot ap2',
          'ac1 and ac2 are in a cluster',
          'ac2 manages ap2 successfully')
res1=res2=1
#operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'cluster-priority 10')
SetCmd(switch1, 'discovery ip-list',StaticIpv4_ac2)

# AP2上配置管理AC的地址为AC2的IP
ApSetcmd(ap2,Ap2cmdtype,'set_switch_address',StaticIpv4_ac2,addressnum='1')
ApSetcmd(ap2,Ap2cmdtype,'saverunning')
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap2, ap2mac, switch1, Ap2cmdtype)
IdleAfter(30)

# 检查AC1和AC2建立集群关系
res1=CheckSutCmd(switch1,'show wireless peer-switch', 
                 check=[(StaticIpv4_ac2)],
                 retry=20,interval=5,waitflag=False,IC=True)
# 检查AP2是否被AC2管理
res2=CheckSutCmd(switch2,'show wireless ap status', 
                 check=[(ap2mac,'Managed','Success')],
                 retry=20,interval=10,waitflag=False,IC=True)
#result
printCheckStep(testname, 'Step 1',res1,res2)
###############################################################################
#Step 2
#操作
# 在AC1上为AP1_image_type指定image文件为ap1_standby_build，
# 在AC1上为AP2_image_type指定image文件为ap2_standby_build，
# AC1设置每组同时下载image的AP数目为1
# wireless ap download group-size 1
# AC1上升级所有管理AP
# 预期
# 同一时刻只能有1个AP进行image下载，
# 正在下载的AP处于Code Transfer In Progress状态，
# 未开始下载的AP处于Requested状态，
# 已经完成下载的AP处于Waiting For APs To Dow状态，必须等待所有AP都完成下载后才能开始升级
# 所有AP都完成下载后，AP进入NVRAM Update In Progress状态
# AP1,Ap2升级成功
################################################################################
printStep(testname,'Step 2',
          'controller config wireless ap download group-size 1',
          'controller upgrade all aps',
          'only one ap download image at the same time',
          'ap that is downloading image is in Code Transfer In Progress status',
          'ap that does not start downloading image is in Requested status',
          'ap that have finished downloading image is in Waiting For APs To Dow status',
          'ap change to NVRAM Update In Progress status after all aps finish downloading image',
          'ap1 and ap2 upgrade successfully')
res1=res2=1
#operate
# 在AC1上为AP1和AP2指定image文件,设置ap download group-size
# (脚本中先配置AP2再配置AP1，目的是如果AP2和AP1的image type相同时，AP2的配置会被AP1覆盖）
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap2_image_type, ap2_ftpupgrade_standby_path)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, ap1_ftpupgrade_standby_path)
SetCmd(switch1, 'wireless ap download group-size 1')

# 升级所有管理AP
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap download start')
IdleAfter(5)
# 检查只有一个AP在下载image文件，另一个AP处于Requested状态
res1 = CheckSutCmd(switch1,'show wireless ap download', 
                   check=[('Code Transfer In Progress'),('Requested')],
                   retry=20,interval=1,waitflag=False,IC=True)
# 检查已完成下载的AP处于Waiting For APs To Dow状态，另一个AP处于下载状态
res2 = CheckSutCmd(switch1,'show wireless ap download', 
                   check=[('Waiting For APs To Dow'),('Code Transfer In Progress')],
                   retry=30,interval=1,waitflag=False,IC=True)
# 检查所有AP都完成下载后，AP进入NVRAM Update In Progress状态
res3 = CheckSutCmd(switch1,'show wireless ap download', 
                   check=[(ap1mac, 'NVRAM Update In Progress'),(ap2mac, 'NVRAM Update In Progress')],
                   retry=20,interval=5,waitflag=False,IC=True)                   

# 等待升级完成
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)

# check
# 检查AC1是否重新管理AP1和AP2
res4=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                 retry=20,interval=5,waitflag=False,IC=True)
# 检查AP1和Ap2升级成功
ApLogin(ap1)
ApLogin(ap2) 
res5 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_standby_buildnum)
if ap1_image_type != ap2_image_type:
    res6 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_standby_buildnum)
else:
    res6 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap1_standby_buildnum)
    
#result
printCheckStep(testname, 'Step 2',res1,res2,res3,res4,res5,res6)
###############################################################################
#Step 3
#操作
# 在AC1上为AP1_image_type指定image文件为ap1_current_build，
# 在AC1上为AP2_image_type指定image文件为ap2_current_build，
# AC1上升级所有管理AP
# 预期
# AP1,AP2升级成功
################################################################################
printStep(testname,'Step 3',
          'config ap1_image_type upgrade to ap1_standby_build',
          'config ap2_image_type upgrade to ap2_standby_build',
          'upgrade all aps',
          'ap1 and ap2 upgrade successfully')

#operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap2_image_type, ap2_ftpupgrade_current_path)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, ap1_ftpupgrade_current_path)
# 升级所有管理AP
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap download start')
# 等待升级完成
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)
# check
res1 = CheckSutCmd(switch1,'show wireless ap status', 
                   check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                   retry=20,interval=5,waitflag=False,IC=True)
ApLogin(ap1)
ApLogin(ap2)
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_current_buildnum)
if ap1_image_type != ap2_image_type:
    res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_current_buildnum)
else:
    res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap1_current_buildnum)
    
#result
printCheckStep(testname, 'Step 3',res1,res2,res3)
################################################################################
# Step 4
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 4',
          'Recover initial config')
          
# operate
# 恢复AP2配置
ApSetcmd(ap2,Ap2cmdtype,'set_switch_address',StaticIpv4_ac1,addressnum='1')
ApSetcmd(ap2,Ap2cmdtype,'saverunning')
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap2, ap2mac, switch2, Ap2cmdtype)

# 恢复AC1配置
EnterWirelessMode(switch1)
SetCmd(switch1, 'no wireless ap download image-type',ap1_image_type)
SetCmd(switch1, 'no wireless ap download image-type',ap2_image_type)
SetCmd(switch1, 'wireless ap download group-size 10')
SetCmd(switch1, 'no cluster-priority')
SetCmd(switch1, 'no discovery ip-list',StaticIpv4_ac2)
SetCmd(switch1, 'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
IdleAfter(30)
CheckSutCmd(switch1,'show wireless peer-switch', 
            check=[('No peer wireless switch exists')],
            retry=10,interval=5,waitflag=False,IC=True)

CheckSutCmd(switch2,'show wireless ap status', 
            check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
            retry=20,interval=10,waitflag=False,IC=True)
#end
printTimer(testname, 'End')