#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_3.1_ONE.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features: 
# 3.1	无线使用tcp/tls协议可以进行手动独立升级Ap
# 测试目的：   wireless protocol使用tcp：可以手动独立升级的方式升级ap版本
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.4.2
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'apconfiguration_3.1'
avoiderror(testname)
printTimer(testname,'Start','ac upgrade all aps with ap1_image_type under tcp/tls protocol')
###############################################################################
#Step 1
#操作
# 查看AC1当前的协议，
# 如果当前协议为tcp，则修改为tls;
# 如果当前协议为tls，则修改为tcp;
# 预期
# 协议修改成功
################################################################################
printStep(testname,'Step 1',
          'change ac wireless protocol')
# operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless protocol', non_default_wireless_protocol, promotePatten='Y/N', promoteTimeout=10)
SetCmd(switch1, 'y')
IdleAfter(120)
# check
# 检查AP被重新管理
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'), (ap2mac,'Managed','Success')],
                 retry=20,interval=5,waitflag=False,IC=True)
#result
printCheckStep(testname, 'Step 1',res1)                 
###############################################################################
#Step 2
#操作
# 在AC1上为AP1_image_type指定image文件为ap1_standby_build，
# AC1上为AP1_image_type的所有AP升级
# 预期
# AP1升级成功
################################################################################
printStep(testname,'Step 2',
          'config ap1_image_type upgrade to ap1_standby_build',
          'upgrade ap1_image_type',
          'ap1 upgrade successfully')
res1=res2=1
#operate
# 在AC1上为AP1指定image文件
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, ap1_ftpupgrade_standby_path)

# 升级AP1_image_type
EnterEnableMode(switch1)
SetCmd(switch1,' wireless ap download start imagetype',ap1_image_type)

# 等待升级完成
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)

# check
# 检查AC1是否重新管理AP1
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success')],
                 retry=20,interval=5,waitflag=False,IC=True)
# 检查AP1版本是否与预期一致 
ApLogin(ap1)
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_standby_buildnum)

#result
printCheckStep(testname, 'Step 2',res1,res2)
###############################################################################
#Step 3
#操作
# 在AC1上为AP1_image_type指定image文件为ap1_current_build，并升级AP1
# 预期
# 等待AP1升级成功，检查AP1升级后的版本和预期是否一致
################################################################################
printStep(testname,'Step 3',
          'config ap1_image_type upgrade to ap1_current_build',
          'upgrade ap1_image_type',
          'ap1 upgrade successfully')

#operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, ap1_ftpupgrade_current_path)
EnterEnableMode(switch1)
SetCmd(switch1,' wireless ap download start imagetype',ap1_image_type)
# 等待升级完成
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)
# check
res1 = CheckSutCmd(switch1,'show wireless ap status', 
                   check=[(ap1mac,'Managed','Success')],
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
SetCmd(switch1, 'wireless protocol', default_wireless_protocol, promotePatten='Y/N', promoteTimeout=10)
SetCmd(switch1, 'y')
IdleAfter(120)
# check
# 检查AP被重新管理
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'), (ap2mac,'Managed','Success')],
                 retry=20,interval=5,waitflag=False,IC=True)
#end
printTimer(testname, 'End')