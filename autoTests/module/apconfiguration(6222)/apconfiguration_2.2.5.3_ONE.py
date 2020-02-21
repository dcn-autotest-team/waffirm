#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.5.3_ONE.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features:
# 2.2.5.3	Ac上没有保存指定Image文件不会升级
# 测试目的： 开启自动集成升级AP image，配置指定image文件，ac上没有保存此tar文件，ap上线不会自动升级
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

testname = 'apconfiguration_2.2.5.3'
avoiderror(testname)
printTimer(testname,'Start','ac would not start integrated upgrade when there is no correct image file')

###############################################################################
#Step 1
#操作
# 在AC1上指定AP1的集成升级版本为错误的文件名，并配置ap auto-upgrade
# 重启AP1
# 预期
# AP1重启后不会自动升级
################################################################################
printStep(testname,'Step 1',
          'ac1 config ap1_image_type integrated upgrade version to wrong image name',
          'config ap auto-upgrade',
          'reboot ap1',
          'ap1 would not upgrade')
res1=res2=1
#operate
# 查看AP当前的版本号
ap1_version = Get_ap_version(ap1, Ap1cmdtype)
ap2_version = Get_ap_version(ap2, Ap2cmdtype)

# 在AC1上为AP1指定错误的image文件,并配置ap auto-upgrade
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap integrated image-type', ap1_image_type, 'flash:/wrong_image_name.tar')
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

# 检查AP版本
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
SetCmd(switch1, 'no wireless ap integrated image-type', ap2_image_type)       
SetCmd(switch1, 'no ap auto-upgrade')  
#end
printTimer(testname, 'End')