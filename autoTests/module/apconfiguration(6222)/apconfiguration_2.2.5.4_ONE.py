#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.5.4_ONE.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features:
# 2.2.5.4	Ac上Image版本与Ap一致时不会进行升级
# 测试目的： 开启自动集成升级AP image，ap版本已经和ac上的image文件版本一致，ap上线不会再升级
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

testname = 'apconfiguration_2.2.5.4'
avoiderror(testname)
printTimer(testname,'Start','ac would not start integrated upgrade when ap version is the same with ac configuration')

###############################################################################
#Step 1
#操作
# 在AC1上指定AP1的集成升级版本为AP当前的版本，并配置ap auto-upgrade
# 重启AP1
# 预期
# AP1重启后不会自动升级
################################################################################
printStep(testname,'Step 1',
          'ac1 config ap1_image_type integrated upgrade version to ap now version',
          'config ap auto-upgrade',
          'reboot ap1',
          'ap1 would not upgrade')
res1=res2=1
#operate
# 查看AP当前的版本号
ap1_version = Get_ap_version(ap1, Ap1cmdtype)
ap2_version = Get_ap_version(ap2, Ap2cmdtype)
ap1_ftpupgrade_path = ap1_ftpupgrade_current_path_6222 if ap1_version  == ap1_current_buildnum else ap1_ftpupgrade_standby_path_6222

# 在AC1上为AP1_image_type指定升级文件为当前AP的版本文件,并配置ap auto-upgrade
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap integrated image-type', ap1_image_type, ap1_ftpupgrade_path)
SetCmd(switch1,'ap auto-upgrade')

# 重启AP
RebootAp(AP=ap1)

# check
# 检查没有AP处于升级状态
res1 = CheckSutCmd(switch1,'show wireless ap download ', 
                 check=[('Total Count','0')],
                 retry=1,interval=1,waitflag=False,IC=True)
# check
# 检查AP是否被AC1重新管理
res2=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                 retry=20,interval=10,waitflag=False,IC=True)

# 检查AP没有升级
res3 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_version)
res4 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_version)
#result
printCheckStep(testname, 'Step 1',res1,res2,res3,res4)
###############################################################################
#Step 2
#恢复初始配置
################################################################################
printStep(testname,'Step 2',
          'Recover initial config for switches.')
# operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'no wireless ap integrated image-type', ap1_image_type)        
SetCmd(switch1, 'no ap auto-upgrade')  
#end
printTimer(testname, 'End')