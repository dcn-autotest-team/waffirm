#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.3.18_ONE.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features: 
# 2.2.3.18	Controller分组独立升级Abort测试2
# 测试目的： 
# 分组手动独立升级AP image的时候，ap处于Waiting For APs To Dow和Code Transfer In Progress，
# Controller上可以使用wireless ap download abort命令终止AP Image更新进程，
# 之后Controller上可以wireless ap download start 重新触发手动独立升级所有ap，
# ap重启后被AC管理，image版本已经更新成功。
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.4.2
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'apconfiguration_2.2.3.18'
avoiderror(testname)
printTimer(testname,'Start','Controller set ap download group-size 1',
           'abort ap download when ap1 is in Waiting For APs To Dow status and ap2 is in Code Transfer In Progress status',
           'ap upgrading is aborted')
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
# 当一个AP处于Waiting For APs To Dow状态，另一个AP处于Code Transfer In Progress状态时，
# AC终止AP升级
# 预期
# AP1,Ap2升级失败
################################################################################
printStep(testname,'Step 2',
          'controller set wireless ap download group-size 1',
          'controller upgrade all aps',
          'controller abort ap download when ap1 is in Waiting For APs To Dow status and ap2 is in Code Transfer In Progress status',
          'ap1 and ap2 upgrading is aborted')
res1=res2=1
#operate
# 查看AP1和AP2当前的版本号
ap1_version = Get_ap_version(ap1, Ap1cmdtype)
ap2_version = Get_ap_version(ap2, Ap2cmdtype)

# 为防止AP下载image速率过快，捕捉不到预期的状态，对S3端口进行限速，限制AP下载速率
EnterInterfaceMode(switch3, s3p6)
SetCmd(switch3, 'bandwidth control 5056')

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

# 检查一个AP处于Waiting For APs To Dow状态，另一个AP处于Code Transfer In Progress状态
res1 = CheckSutCmd(switch1,'show wireless ap download', 
                   check=[('Waiting For APs To Dow'), ('Code Transfer In Progress')],
                   retry=40,interval=3,waitflag=False,IC=True)
                   
# 终止AP升级
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap download abort')

# 检查AP升级处于Aborted状态
res2 = CheckSutCmd(switch1,'show wireless ap download', 
                   check=[('Download Status','Aborted'),(ap1mac, 'Aborted'),(ap2mac, 'Aborted')],
                   retry=5,interval=5,waitflag=False,IC=True)

# 取消S3端口限速
EnterInterfaceMode(switch3, s3p6)
SetCmd(switch3, 'no bandwidth control')
                   
# 检查AC1仍然管理AP1和AP2
res3=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                 retry=20,interval=5,waitflag=False,IC=True)    
                 
# 检查AP1和Ap2版本没有变化
res4 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_version)
res5 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_version)

#result
printCheckStep(testname, 'Step 2',res1,res2,res3,res4,res5)
###############################################################################
#Step 3
#操作
# AC1上重新升级所有管理AP
# 预期
# AP1,AP2升级成功
################################################################################
printStep(testname,'Step 3',
          'controller upgrade all aps again',
          'ap1 and ap2 upgrade successfully',)
res1=res2=1
#operate
# 升级所有管理AP
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap download start')

# 等待升级完成
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)

# check
# 检查AC1是否重新管理AP1和AP2
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                 retry=20,interval=5,waitflag=False,IC=True)
# 检查AP1和AP2升级成功
ApLogin(ap1)
ApLogin(ap2)
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_standby_buildnum)
if ap1_image_type != ap2_image_type:
    res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_standby_buildnum)
else:
    res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap1_standby_buildnum)
#result
printCheckStep(testname, 'Step 3',res1,res2,res3)
###############################################################################
#Step 4
#操作
# 在AC1上为AP1_image_type指定image文件为ap1_current_build，
# 在AC1上为AP2_image_type指定image文件为ap2_current_build，
# AC1上升级所有管理AP
# 预期
# AP1,AP2升级成功
################################################################################
printStep(testname,'Step 4',
          'config ap1_image_type upgrade to ap1_standby_build',
          'config ap2_image_type upgrade to ap2_standby_build',
          'upgrade all aps',
          'ap1 and ap2 upgrade successfully',)

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
printCheckStep(testname, 'Step 4',res1,res2,res3)
################################################################################
# Step 5
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 5',
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