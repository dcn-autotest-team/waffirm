#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.2.15_ONE.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features: 
# 2.2.2.15	分组独立升级Abort测试1
# 测试目的： 
# 分组手动独立升级AP image的时候，ap处于Waiting For APs To Dow和Code Transfer In Progress，
# 管理AC上可以使用wireless ap download abort命令终止AP Image更新进程，
# 之后管理AC上可以wireless ap download start 重新触发手动独立升级所有ap，
# ap重启后被AC管理，image版本已经更新成功。
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.3.30
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'apconfiguration_2.2.2.15'
avoiderror(testname)
printTimer(testname,'Start','set ap download group-size 1,\n \
           abort ap download when ap1 is in Waiting For APs To Dow status and ap2 is in Code Transfer In Progress status,\n \
           ap upgrading is aborted')

###############################################################################
#Step 1
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
printStep(testname,'Step 1',
          'wireless ap download group-size 1',
          'upgrade all aps',
          'abort ap download when ap1 is in Waiting For APs To Dow status and ap2 is in Code Transfer In Progress status',
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
ApLogin(ap1) 
ApLogin(ap2) 
res4 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_version)
res5 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_version)

#result
printCheckStep(testname, 'Step 1',res1,res2,res3,res4,res5)
###############################################################################
#Step 2
#操作
# AC1上升级所有管理AP
# 预期
# AP1,AP2升级成功
################################################################################
printStep(testname,'Step 2',
          'upgrade all aps',
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
printCheckStep(testname, 'Step 2',res1,res2,res3)
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
printCheckStep(testname, 'Step 3',res1,res2,res3)
################################################################################
# Step 4
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 4',
          'Recover initial config')
          
# operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download group-size 10')
SetCmd(switch1, 'no wireless ap download image-type',ap1_image_type)
SetCmd(switch1, 'no wireless ap download image-type',ap2_image_type)
#end
printTimer(testname, 'End')