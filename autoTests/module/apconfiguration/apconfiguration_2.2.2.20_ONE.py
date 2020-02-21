#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.2.20_ONE.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features: 
# 2.2.2.20	手动升级配置错误文件不能正常升级(合并用例2.2.2.20和2.2.2.21)
# 测试目的： 2.2.2.20 手动独立升级，配置的ap image文件错误（其它image-type的文件），ap从服务器下载完image后不重启，
#                     ac上show wireless ap download显示Download Status为Failure
#            2.2.2.21 （接上）重新配置正确的ap image文件，可以重新触发手动独立升级，ap版本升级成功
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.3.29
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'apconfiguration_2.2.2.20'
avoiderror(testname)
printTimer(testname,'Start','Ac config wrong image file for ap. Ap can download image, but can not upgrade')

###############################################################################
#Step 1
#操作
# 在AC1上为AP1_image_type指定错误的image文件,(其他image_type的文件)
# 在AC1上为AP2_image_type指定错误的image文件,(其他image_type的文件)
# AC1上为AP1升级
# 预期
# AP1和AP2不会升级
################################################################################
printStep(testname,'Step 1',
          'config ap1_image_type upgrade to wrong image_type file',
          'config ap2_image_type upgrade to wrong image_type file',
          'upgrade ap1',
          'ap1 and ap2 should not upgrade')
res1=res2=1
#operate
# 查看AP1和AP2当前的版本号
ap1_version = Get_ap_version(ap1, Ap1cmdtype)
ap2_version = Get_ap_version(ap2, Ap2cmdtype)

# 在AC1上为AP1和AP2指定image文件
# (脚本中先配置AP2再配置AP1，目的是如果AP2和AP1的image type相同时，AP2的配置会被AP1覆盖）
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap2_image_type, wrong_imagetype_ftpupgrade_path)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, wrong_imagetype_ftpupgrade_path)

# 升级AP1
EnterEnableMode(switch1)
SetCmd(switch1,'  wireless ap download start',ap1mac)
IdleAfter(60)

# AP1升级失败
res1 = CheckSutCmd(switch1, 'show wireless ap download',
                   check=[(ap1mac, 'Failure')],
                   retry=20, interval=5, waitflag=False,IC=True)
# AP2不会出现在升级列表中
res2 = CheckSutCmdWithNoExpect(switch1, 'show wireless ap download',
                               check=[(ap2mac)],
                               retry=1, waitflag=False,IC=True)    

# 检查AC1仍然管理AP1和AP2
res3=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                 retry=20,interval=5,waitflag=False,IC=True)
# 检查AP1和AP2没有升级
ApLogin(ap1)
res4 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_version)
res5 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_version)
#result
printCheckStep(testname, 'Step 1',res1,res2,res3,res4,res5)
###############################################################################
#Step 2
#操作
# 在AC1上为AP1_image_type指定image文件为ap1_standby_build，
# 在AC1上为AP2_image_type指定image文件为ap2_standby_build，
# AC1上为AP1升级
# 预期
# AP1升级成功
# AP2不会升级
################################################################################
printStep(testname,'Step 2',
          'config ap1_image_type upgrade to ap1_standby_build',
          'config ap2_image_type upgrade to ap2_standby_build',
          'upgrade ap1',
          'ap1 upgrade successfully',
          'ap2 should not upgrade')
res1=res2=1
#operate
# 在AC1上为AP1和AP2指定image文件
# (脚本中先配置AP2再配置AP1，目的是如果AP2和AP1的image type相同时，AP2的配置会被AP1覆盖）
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap2_image_type, ap2_ftpupgrade_standby_path)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, ap1_ftpupgrade_standby_path)
# 升级AP1
EnterEnableMode(switch1)
SetCmd(switch1,'  wireless ap download start',ap1mac)

# 等待升级完成
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)

# check
# 检查AC1是否重新管理AP1和AP2
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                 retry=20,interval=5,waitflag=False,IC=True)
# 检查AP1升级成功
ApLogin(ap1)
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_standby_buildnum)
# 检查AP2没有升级 
res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_version)
#result
printCheckStep(testname, 'Step 2',res1,res2,res3)
###############################################################################
#Step 3
#操作
# 在AC1上为AP1_image_type指定image文件为ap1_current_build，并升级AP1
# 预期
# 等待AP1升级成功，检查AP1升级后的版本和预期是否一致
################################################################################
printStep(testname,'Step 3',
          'config ap1 upgrade image to ap1_current_build',
          'upgrade ap1',
          'ap1 upgrade successfully')

#operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, ap1_ftpupgrade_current_path)
EnterEnableMode(switch1)
SetCmd(switch1,'  wireless ap download start',ap1mac)
# 等待升级完成
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)
# check
res1 = CheckSutCmd(switch1,'show wireless ap status', 
                   check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                   retry=20,interval=5,waitflag=False,IC=True)
ApLogin(ap1)
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_current_buildnum)
#result
printCheckStep(testname, 'Step 3',res1,res2)
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