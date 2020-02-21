#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_3.3_ONE.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features: 
# 3.3	Tftp进行独立手动升级
# 测试目的：  采用tftp服务器：为AP指定image文件后，通过手动更新的方式能够为AP更新image，更新完成后AP重启，并重新认证关联。
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.4.2
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'apconfiguration_3.3'
avoiderror(testname)
printTimer(testname,'Start','ac upgrade aps by tftp server')

###############################################################################
#Step 1
#操作
# 在AC1上使用tftp方式为AP1升级
# 为AP1_image_type指定image文件为ap1_standby_build，
# AC1上为AP1_image_type的所有AP升级
# 预期
# AP1升级成功
################################################################################
printStep(testname,'Step 1',
          'config ap1_image_type upgrade to ap1_standby_build by tftp path',
          'upgrade ap1_image_type',
          'ap1 upgrade successfully')
res1=res2=1
#operate
# 在AC1上为AP1指定image文件,使用tftp方式升级
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, ap1_tftpupgrade_standby_path)

# 升级AP1_image_type
EnterEnableMode(switch1)
SetCmd(switch1,' wireless ap download start imagetype',ap1_image_type)

# 等待升级完成
IdleAfter(tftp_ap_upgrade_time)
ac_wait_download_finish(switch1)

# check
# 检查AC1是否重新管理AP1和AP2
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                 retry=20,interval=5,waitflag=False,IC=True)
# 检查AP1版本是否与预期一致 
ApLogin(ap1)
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_standby_buildnum)
# 检查AP2版本是否与预期一致 
if ap1_image_type == ap2_image_type:
    ApLogin(ap2)
    res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap1_standby_buildnum)
else:
    res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_version)
#result
printCheckStep(testname, 'Step 1',res1,res2,res3)
###############################################################################
#Step 2
#操作
# 在AC1上为AP1_image_type指定image文件为ap1_current_build，并升级AP1
# 预期
# 等待AP1升级成功，检查AP1升级后的版本和预期是否一致
################################################################################
printStep(testname,'Step 2',
          'config ap1_image_type upgrade to ap1_current_build',
          'upgrade ap1_image_type',
          'ap1 upgrade successfully')

#operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, ap1_tftpupgrade_current_path)
EnterEnableMode(switch1)
SetCmd(switch1,' wireless ap download start imagetype',ap1_image_type)
# 等待升级完成
IdleAfter(tftp_ap_upgrade_time)
ac_wait_download_finish(switch1)
# check
res1 = CheckSutCmd(switch1,'show wireless ap status', 
                   check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                   retry=20,interval=5,waitflag=False,IC=True)
ApLogin(ap1)
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_current_buildnum)
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
SetCmd(switch1, 'no wireless ap download image-type',ap1_image_type)
#end
printTimer(testname, 'End')