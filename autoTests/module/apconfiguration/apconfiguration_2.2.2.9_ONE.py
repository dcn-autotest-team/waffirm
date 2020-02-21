#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.2.9_ONE.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features: 
# 2.2.2.9	手动独立升级下载过程中可取消(合并用例2.2.2.9和2.2.2.10)
# 测试目的： 
# 2.2.2.9 管理AC上可以wireless ap download start 触发手动独立升级所有ap，ap正在下载image，
#         show wireless ap download显示ap状态为Code Transfer In Progress，
#         可以使用wireless ap download abort命令终止AP Image更新进程。
#         show wireless ap download显示Download Status为Aborted。
# 2.2.2.10 （接上）show wireless ap download显示Download Status为Aborted的时候，
#         管理AC上可以wireless ap download start 重新触发手动独立升级所有ap，
#         ap重启后被AC管理，image版本已经更新成功。
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.3.29
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'apconfiguration_2.2.2.9'
avoiderror(testname)
printTimer(testname,'Start','ac can abort ap upgrade before ap finishing download image file')

###############################################################################
#Step 1
#操作
# 在AC1上为AP1_image_type指定image文件为ap1_standby_build，
# 在AC1上为AP2_image_type指定image文件为ap2_standby_build，
# AC1上升级所有管理AP
# 在AP下载image文件过程中，AC上终止升级
# wireless ap download abort
# 预期
# AP1和AP2的升级被终止
################################################################################
printStep(testname,'Step 2',
          'config ap1_image_type upgrade to ap1_standby_build',
          'config ap2_image_type upgrade to ap2_standby_build',
          'upgrade all aps',
          'abort ap download when ap is downloading image file',
          'upgrade should be aborted')
res1=res2=1
#operate
# 查看AP1和AP2当前的版本号
ap1_version = Get_ap_version(ap1, Ap1cmdtype)
ap2_version = Get_ap_version(ap2, Ap2cmdtype)

# 在AC1上为AP1和AP2指定image文件
# (脚本中先配置AP2再配置AP1，目的是如果AP2和AP1的image type相同时，AP2的配置会被AP1覆盖）
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap2_image_type, ap2_ftpupgrade_standby_path)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, ap1_ftpupgrade_standby_path)

# 升级所有管理AP
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap download start')
# 终止AP升级
SetCmd(ap1,'\n',promotePatten='ETA', promoteTimeout=10)
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap download abort')

# AP1和AP2的升级被终止
res1 = CheckSutCmd(switch1, 'show wireless ap download',
                   check=[('Download Status', 'Aborted'),(ap1mac, 'Aborted'),(ap2mac, 'Aborted')],
                   retry=5, interval=5, waitflag=False,IC=True)    

# 检查AC1是否管理AP1和AP2
res2=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                 retry=20,interval=5,waitflag=False,IC=True)
# 检查AP1和AP2版本号
res3 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_version)
res4 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_version)
#result
printCheckStep(testname, 'Step 1',res1,res2,res3,res4)
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
SetCmd(switch1, 'no wireless ap download image-type',ap1_image_type)
SetCmd(switch1, 'no wireless ap download image-type',ap2_image_type)
#end
printTimer(testname, 'End')