#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.1.1.2.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features:
# 2.1.1.2	为AP指定Image并手动更新
# 测试目的：为AP指定image文件后，通过手动更新的方式能够为AP更新image，更新完成后AP重启，并重新认证关联。
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

testname = 'apconfiguration_2.1.1.2'
avoiderror(testname)
printTimer(testname,'Start','ac upgrade ap image')

###############################################################################
#Step 1
#操作
# 在AC1上为AP1指定image文件为ap1_standby_build，并升级AP1
# 预期
# 等待AP1升级成功，检查AP1升级后的版本和预期是否一致
################################################################################
printStep(testname,'Step 1',
          'config ap1 upgrade image to ap1_standby_build',
          'upgrade ap1 from ac1',
          'ap1 upgrade successfully')
res1=res2=1
#operate
# 在AC1上为AP1指定image文件，并升级AP1
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, ap1_ftpupgrade_standby_path)
EnterEnableMode(switch1)
SetCmd(switch1,' wireless ap download start imagetype',ap1_image_type)
# 等待升级完成
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)

# check
# 检查AC1是否重新管理AP1
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,Ap1_ipv4,'1','Managed','Success')],
                 retry=20,interval=5,waitflag=False,IC=True)

# 检查AP1版本是否与预期一致  
ApLogin(ap1)   
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_standby_buildnum)
#result
printCheckStep(testname, 'Step 1',res1,res2)
###############################################################################
#Step 2
#操作
# 在AC1上为AP1指定image文件为ap1_current_build，并升级AP1
# 预期
# 等待AP1升级成功，检查AP1升级后的版本和预期是否一致
################################################################################
printStep(testname,'Step 2',
          'config ap1 upgrade image to ap1_current_build',
          'upgrade ap1 from ac1',
          'ap1 upgrade successfully')
res1=res2=1
#operate
# 在AC1上为AP1指定image文件，并升级AP1
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, ap1_ftpupgrade_current_path)
EnterEnableMode(switch1)
SetCmd(switch1,' wireless ap download start imagetype',ap1_image_type)
# 等待升级完成
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)

# check
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,Ap1_ipv4,'1','Managed','Success')],
                 retry=20,interval=5,waitflag=False,IC=True)     
# 检查AP1版本是否与预期一致  
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