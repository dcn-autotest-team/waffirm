#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.5.2_ONE.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features:
# 2.2.5.2	多Type的Ap自动集成升级
# 测试目的：  多ap场景：多个不同image-type 的ap（需要都配置指定image文件），ap上线自动升级，ap重启后被AC管理，image版本已经更新成功。
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.4.2
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'apconfiguration_2.2.5.2'
avoiderror(testname)
printTimer(testname,'Start','multi ap integrated upgrade')

###############################################################################
#Step 1
#操作
# 在AC1配置ap auto-upgrade
# 指定AP1的集成升级版本为ap1_standby_build，AP2的集成升级版本为ap2_standby_build，
# 重启AP1
# 预期
# AP1和AP2重启后，会自动升级
################################################################################
printStep(testname,'Step 1',
          'ac1 config ap1_image_type integrated upgrade version to ap1_standby_build',
          'ac1 config ap2_image_type integrated upgrade version to ap2_standby_build',
          'config ap auto-upgrade',
          'reboot ap1 and ap2',
          'ap1 upgrade to ap1_standby_build after reboot',
          'ap2 upgrade to ap2_standby_build after reboot')
res1=res2=1
#operate
# 在AC1上为AP指定image文件，并配置ap auto-upgrade
EnterWirelessMode(switch1)
SetCmd(switch1,'ap auto-upgrade')
SetCmd(switch1, 'wireless ap integrated image-type', ap2_image_type, ap2_ftpupgrade_standby_path_6222)
SetCmd(switch1, 'wireless ap integrated image-type', ap1_image_type, ap1_ftpupgrade_standby_path_6222)

# 重启AP,等待升级
RebootAp(AP=ap1)
# RebootAp(AP=ap2)
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)

# check
# 检查AP是否被AC1重新管理
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'), (ap2mac,'Managed','Success')],
                 retry=20,interval=10,waitflag=False,IC=True)

# 检查AP版本
ApLogin(ap1)
ApLogin(ap2)
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_standby_buildnum)
res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap1_standby_buildnum)
#result
printCheckStep(testname, 'Step 1',res1,res2,res3)
###############################################################################
#Step 2
#操作
# 指定AP1的集成升级版本为ap1_current_build，AP2的集成升级版本为ap2_current_build，
# 重启AP1
# 预期
# AP1和AP2重启后，会自动升级
################################################################################
printStep(testname,'Step 2',
          'ac1 config ap1_image_type integrated upgrade version to ap1_current_build',
          'ac1 config ap2_image_type integrated upgrade version to ap2_current_build',
          'reboot ap1 and ap2',
          'ap1 upgrade to ap1_current_build after reboot',
          'ap2 upgrade to ap2_current_build after reboot')
res1=res2=1
#operate
# 在AC1上为AP1指定image文件
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap integrated image-type', ap1_image_type, ap1_ftpupgrade_current_path_6222)
SetCmd(switch1, 'wireless ap integrated image-type', ap2_image_type, ap2_ftpupgrade_current_path_6222)

# 重启AP
RebootAp(AP=ap1)
RebootAp(AP=ap2)
# 等待AP升级
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)

# 检查AP是否被AC1重新管理
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'), (ap2mac,'Managed','Success')],
                 retry=20,interval=10,waitflag=False,IC=True)
# 检查AP版本
ApLogin(ap1)
ApLogin(ap2)
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_current_buildnum)
res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap1_current_buildnum)
#result
printCheckStep(testname, 'Step 2',res1,res2,res3)
###############################################################################
#Step 3
#恢复初始配置
################################################################################
printStep(testname,'Step 3',
          'Recover initial config for switches.')
# operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'no wireless ap integrated image-type', ap1_image_type)     
SetCmd(switch1, 'no wireless ap integrated image-type', ap2_image_type) 
SetCmd(switch1, 'no ap auto-upgrade')  
#end
printTimer(testname, 'End')