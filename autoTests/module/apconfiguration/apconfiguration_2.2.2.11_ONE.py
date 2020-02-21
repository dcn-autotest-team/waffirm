#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.2.11_ONE.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features: 
# 2.2.2.11	分组独立升级状态测试1/2/3(合并用例2.2.2.11，2.2.2.12，2.2.2.13)
# 测试目的： 
# 2.2.2.11  分组手动独立升级AP image：管理AC上可以wireless ap download start 触发手动独立升级所有ap，
# 第一组ap先下载Image，show wireless ap download显示前x个ap状态处于Code Transfer In Progress，
# 其它等待ap状态处于Requested（使用wireless ap download group-size x配置每组同时下载Image的 AP数目小于目前管理AP数）
# 2.2.2.12  分组手动独立升级AP image：管理AC上可以wireless ap download start 触发手动独立升级所有ap，
# 下载完Image的ap状态处于Waiting For APs To Dow，正在下载的ap状态处于Code Transfer In Progress，
# 其它等待ap状态处于Requested
# 2.2.2.13  分组手动独立升级AP image：管理AC上可以wireless ap download start 触发手动独立升级所有ap，
# ap全部下载完Image后状态都为NVRAM Update In Progress，ap全部重启后被AC管理，image版本已经更新成功。
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.3.30
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'apconfiguration_2.2.2.11-13'
avoiderror(testname)
printTimer(testname,'Start','set ap download group-size x,\n \
           only x aps are downloading image at the same time,\n \
           ap that is downloading image is in Code Transfer In Progress status,\n \
           ap that does not start downloading image is in Requested status,\n \
           ap that have finished downloading image is in Waiting For APs To Dow status,\n \
           aps change to NVRAM Update In Progress status after all aps finish downloading image')

###############################################################################
#Step 1
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
printStep(testname,'Step 1',
          'wireless ap download group-size 1',
          'upgrade all aps',
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
printCheckStep(testname, 'Step 1',res1,res2,res3,res4,res5,res6)
###############################################################################
#Step 2
#操作
# 在AC1上为AP1_image_type指定image文件为ap1_current_build，
# 在AC1上为AP2_image_type指定image文件为ap2_current_build，
# AC1上升级所有管理AP
# 预期
# AP1,AP2升级成功
################################################################################
printStep(testname,'Step 2',
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
printCheckStep(testname, 'Step 2',res1,res2,res3)
################################################################################
# Step 3
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 3',
          'Recover initial config')
          
# operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download group-size 10')
SetCmd(switch1, 'no wireless ap download image-type',ap1_image_type)
SetCmd(switch1, 'no wireless ap download image-type',ap2_image_type)
#end
printTimer(testname, 'End')