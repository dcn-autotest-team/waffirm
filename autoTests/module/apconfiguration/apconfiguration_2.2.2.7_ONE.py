#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.2.7_ONE.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features: 
# 2.2.2.7-8	管理Ac上可以同时升级全部Ap(合并用例2.2.2.7和2.2.2.8)
# 测试目的： 2.2.2.7 管理AC上可以wireless ap download start 触发手动独立升级所有ap，ap重启后被AC管理，image版本已经更新成功。
#   2.2.2.8 管理AC上可以wireless ap download start 触发手动独立升级所有ap，ap已经下载完image，无法使用wireless ap download abort命令终止AP Image更新进程。
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.3.29
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'apconfiguration_2.2.2.7'
avoiderror(testname)
printTimer(testname,'Start','ac upgrade all aps, and can not abort ap upgrade after ap finishes downloading image file ')

###############################################################################
#Step 1
#操作
# 在AC1上为AP1_image_type指定image文件为ap1_standby_build，
# 在AC1上为AP2_image_type指定image文件为ap2_standby_build，
# AC1上升级所有管理AP
# 等待AP下载image file完成后终止Ap升级
# wireless ap download abort
# 预期
# abort命令不生效
# AP1,Ap2升级成功
################################################################################
printStep(testname,'Step 1',
          'config ap1_image_type upgrade to ap1_standby_build',
          'config ap2_image_type upgrade to ap2_standby_build',
          'upgrade all aps',
          'abort ap download after ap finishes downloading',
          'ap1 and ap2 upgrade successfully',)
res1=res2=1
#operate
# 在AC1上为AP1和AP2指定image文件
# (脚本中先配置AP2再配置AP1，目的是如果AP2和AP1的image type相同时，AP2的配置会被AP1覆盖）
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap2_image_type, ap2_ftpupgrade_standby_path)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, ap1_ftpupgrade_standby_path)

# 升级所有管理AP,并等待AP下载完成image文件
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap download start')
CheckSutCmd(switch1,'show wireless ap download', 
            check=[(ap1mac,'NVRAM Update In Progress'),(ap2mac,'NVRAM Update In Progress')],
            retry=20,interval=3,waitflag=False,IC=True)
# 终止AP升级
IdleAfter(10)
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap download abort')
# 等待升级完成
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)

# check
# 检查AC1是否重新管理AP1和AP2
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                 retry=20,interval=5,waitflag=False,IC=True)
# 检查AP1和Ap2升级成功
ApLogin(ap1)
ApLogin(ap2) 
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_standby_buildnum)
if ap1_image_type != ap2_image_type:
    res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_standby_buildnum)
else:
    res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap1_standby_buildnum)
#result
printCheckStep(testname, 'Step 1',res1,res2,res3)
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
SetCmd(switch1, 'no wireless ap download image-type',ap1_image_type)
SetCmd(switch1, 'no wireless ap download image-type',ap2_image_type)
#end
printTimer(testname, 'End')