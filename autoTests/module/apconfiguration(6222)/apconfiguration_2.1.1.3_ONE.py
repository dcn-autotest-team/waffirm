#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.1.1.3.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features:
# 2.1.1.3	Ap与Ac存储版本不一致时会触发Ap自动更新
# 测试目的： 当AP的image版本与AC存储的不一致时，会触发AP image的自动更新，更新后AP应自动重启并重新认证关联。
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.3.28
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'apconfiguration_2.1.1.3'
avoiderror(testname)
printTimer(testname,'Start',' ap auto-upgrade when ap version differ from ac preset version')

###############################################################################
#Step 1
#操作
# 在AC1上指定AP1的版本为ap1_standby_build，并配置ap auto-upgrade
# 重启AP1
# 预期
# AP1重启后，自动升级到ap1_standby_build版本
################################################################################
printStep(testname,'Step 1',
          'config ap1 preset version to ap1_standby_build on ac1',
          'config ap auto-upgrade on ac1',
          'reboot ap1',
          'ap1 upgrade to ap1_standby_build after reboot')
res1=res2=1
#operate
# 在AC1上为AP1指定image文件，
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap integrated image-type', ap1_image_type, ap1_ftpupgrade_standby_path_6222)
SetCmd(switch1,'ap auto-upgrade')
# 重启AP
RebootAp(AP=ap1)
# 等待AP升级
IdleAfter(ftp_ap_upgrade_time)
# 检查AP1是否被AC1重新管理
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,Ap1_ipv4,'1','Managed','Success')],
                 retry=20,interval=10,waitflag=False,IC=True)

# 检查AP版本
ApLogin(ap1)
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_standby_buildnum)
#result
printCheckStep(testname, 'Step 1',res1,res2)
###############################################################################
#Step 2
#操作
# 在AC1上指定AP1的版本为ap1_current_buildnum，并配置ap auto-upgrade
# 重启AP1
# 预期
# AP1重启后，自动升级到ap1_current_buildnum版本
################################################################################
printStep(testname,'Step 2',
          'config ap1 preset version to ap1_current_buildnum on ac1',
          'config ap auto-upgrade on ac1',
          'reboot ap1',
          'ap1 upgrade to ap1_current_buildnum after reboot')
res1=res2=1
#operate
# 在AC1上为AP1指定image文件，
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap integrated image-type', ap1_image_type, ap1_ftpupgrade_current_path_6222)
SetCmd(switch1,'ap auto-upgrade')
# 重启AP
RebootAp(AP=ap1)
# 等待AP升级
IdleAfter(ftp_ap_upgrade_time)
# 检查AP1是否被AC1重新管理
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,Ap1_ipv4,'1','Managed','Success')],
                 retry=20,interval=10,waitflag=False,IC=True)
# 检查AP版本
ApLogin(ap1)
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_current_buildnum)
#result
printCheckStep(testname, 'Step 2',res1,res2)
###############################################################################
#Step 3
#恢复初始配置
################################################################################
printStep(testname,'Step 3',
          'Recover initial config for switches.')
# operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'no wireless ap integrated image-type', ap1_image_type)   
SetCmd(switch1, 'no ap auto-upgrade')        
#end
printTimer(testname, 'End')