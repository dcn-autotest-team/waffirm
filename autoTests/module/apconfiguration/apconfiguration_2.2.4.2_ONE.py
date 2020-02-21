#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.4.2_ONE.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features:
# 2.2.4.2	多Ap上线自动升级
# 测试目的：多ap场景：多个不同image-type 的ap（需要都配置指定image文件），ap上线自动升级，ap重启后被AC管理，image版本已经更新成功。
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

testname = 'apconfiguration_2.2.4.2'
avoiderror(testname)
printTimer(testname,'Start','multi ap independent auto-upgrade ')

###############################################################################
#Step 1
#操作
# 在AC1上配置ap independent auto-upgrade，
# 为AP1_image_type指定version和image为 ap1_standby_build
# 为AP2_image_type指定version和image为 ap2_standby_build
# 预期
# AP1和AP2自动升级，检查升级后的版本和预期是否一致
################################################################################
printStep(testname,'Step 1',
          'AC1 config ap independent auto-upgrade',
          'config ap1_image_type upgrade to ap1_standby_build',
          'config ap2_image_type upgrade to ap2_standby_build',
          'ap1 and ap2 upgrade automatically')
res1=res2=1
#operate
# 在AC1上上配置ap independent auto-upgrade，并为AP1_image_type和AP2_image_type指定version和image
EnterWirelessMode(switch1)
SetCmd(switch1, 'ap independent auto-upgrade')
SetCmd(switch1, 'wireless ap download image-type',ap2_image_type, 'version', ap2_standby_buildnum, ap2_ftpupgrade_standby_path)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, 'version', ap1_standby_buildnum, ap1_ftpupgrade_standby_path)

# 等待升级完成
IdleAfter(ftp_ap_upgrade_time*2)
ac_wait_download_finish(switch1)

# check
# 检查AC1是否重新管理AP
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'), (ap2mac,'Managed','Success')],
                 retry=20,interval=5,waitflag=False,IC=True)

# 检查AP版本是否与预期一致  
ApLogin(ap1)  
ApLogin(ap2) 
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_standby_buildnum)
# 检查AP1版本是否与预期一致 
if ap1_image_type == ap2_image_type:
    res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap1_standby_buildnum)
else:
    res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_standby_buildnum)
#result
printCheckStep(testname, 'Step 1',res1,res2,res3)
###############################################################################
#Step 2
#操作
# 在AC1上为AP1_image_type指定version和image为 ap1_current_build
# 在AC1上为AP2_image_type指定version和image为 ap2_current_build
# 预期
# AP1和AP2自动升级，检查升级后的版本和预期是否一致
################################################################################
printStep(testname,'Step 2',
          'config ap1_image_type upgrade to ap1_current_build',
          'config ap2_image_type upgrade to ap2_standby_build',
          'ap1 and ap2 upgrade automatically')
res1=res2=1
#operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap2_image_type, 'version', ap2_current_buildnum, ap2_ftpupgrade_current_path)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, 'version', ap1_current_buildnum, ap1_ftpupgrade_current_path)

# 等待升级完成
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)

# check
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'), (ap2mac,'Managed','Success')],
                 retry=20,interval=5,waitflag=False,IC=True)    
# 检查AP版本是否与预期一致  
ApLogin(ap1)  
ApLogin(ap2) 
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_current_buildnum)
# 检查AP1版本是否与预期一致 
if ap1_image_type == ap2_image_type:
    res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap1_current_buildnum)
else:
    res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_current_buildnum)
#result
printCheckStep(testname, 'Step 2',res1,res2)
################################################################################
# Step 3
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 3',
          'Recover initial config')
# operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'no ap independent auto-upgrade')
SetCmd(switch1, 'no wireless ap download image-type',ap1_image_type)
SetCmd(switch1, 'no wireless ap download image-type',ap2_image_type)
#end
printTimer(testname, 'End')