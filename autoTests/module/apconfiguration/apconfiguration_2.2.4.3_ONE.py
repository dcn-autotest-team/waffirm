#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.4.3_ONE.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features:
# 2.2.4.3	版本一致不会自动升级
# 测试目的：开启自动独立升级AP image功能，ap版本已经和ac上配置的image文件版本一致，ap上线不会再升级
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

testname = 'apconfiguration_2.2.4.3'
avoiderror(testname)
printTimer(testname,'Start','ap would not upgrade when ap version is the same with ac configuration')

###############################################################################
#Step 1
#操作
# 在AC1上配置ap independent auto-upgrade，
# 为AP1_image_type指定version和image为 ap1_current_build
# 为AP2_image_type指定version和image为 ap2_current_build
# 预期
# AP1和AP2不会升级
################################################################################
printStep(testname,'Step 1',
          'AC1 config ap independent auto-upgrade',
          'config ap1_image_type upgrade to ap1_current_build(same with ap1 now version)',
          'config ap2_image_type upgrade to ap2_current_build(same with ap2 now version)',
          'ap1 and ap2 should not upgrade')
res1=res2=1
#operate
# 查看AP当前的版本号
ap1_version = Get_ap_version(ap1, Ap1cmdtype)
ap2_version = Get_ap_version(ap2, Ap2cmdtype)
ap1_ftpupgrade_path = ap1_ftpupgrade_current_path if ap1_version  == ap1_current_buildnum else ap1_ftpupgrade_standby_path
ap2_ftpupgrade_path = ap2_ftpupgrade_current_path if ap2_version  == ap2_current_buildnum else ap2_ftpupgrade_standby_path

# 在AC1上配置ap independent auto-upgrade，并为AP1_image_type和AP2_image_type指定与当前版本相同的version和image
EnterWirelessMode(switch1)
SetCmd(switch1, 'ap independent auto-upgrade')
SetCmd(switch1, 'wireless ap download image-type',ap2_image_type, 'version', ap2_version, ap2_ftpupgrade_path)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, 'version', ap1_version, ap1_ftpupgrade_path)
IdleAfter(10)
# check
# 检查AP版本没有变化 
res1 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_version)
res2 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_version)

#result
printCheckStep(testname, 'Step 1',res1,res2)
################################################################################
# Step 2
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 2',
          'Recover initial config')
# operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'no ap independent auto-upgrade')
SetCmd(switch1, 'no wireless ap download image-type',ap1_image_type)
SetCmd(switch1, 'no wireless ap download image-type',ap2_image_type)
# 检查AC1是否管理AP
CheckSutCmd(switch1,'show wireless ap status', 
            check=[(ap1mac,'Managed','Success'), (ap2mac,'Managed','Success')],
            retry=50,interval=10,waitflag=False,IC=True)
#end
printTimer(testname, 'End')