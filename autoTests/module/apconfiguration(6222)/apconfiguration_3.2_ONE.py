#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_3.2_ONE.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features: 
# 3.2	无线使用tcp/tls协议可以进行自动集成升级
# 测试目的：   wireless protocol使用tcp：可以集成升级的方式自动升级ap版本
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.4.2
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'apconfiguration_3.2'
avoiderror(testname)
printTimer(testname,'Start','single ap integrated upgrade under tcp/tls protocol')
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
# 在AC1上指定AP1的集成升级版本为ap1_standby_build，并配置ap auto-upgrade
# 重启AP1
# 预期
# AP1重启后，自动升级到ap1_standby_build版本
################################################################################
printStep(testname,'Step 2',
          'ac1 config ap1_image_type integrated upgrade version to ap1_standby_build',
          'config ap auto-upgrade',
          'reboot ap1',
          'ap1 upgrade to ap1_standby_build after reboot')
res1=res2=1
#operate
# 查看AP2当前的版本号
ap2_version = Get_ap_version(ap2, Ap2cmdtype)

# 在AC1上为AP1指定image文件,并配置ap auto-upgrade
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap integrated image-type', ap1_image_type, ap1_ftpupgrade_standby_path_6222)
SetCmd(switch1,'ap auto-upgrade')

# 重启AP,等待升级
RebootAp(AP=ap1)
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)

# check
# 检查AP1是否被AC1重新管理
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,Ap1_ipv4,'1','Managed','Success')],
                 retry=20,interval=10,waitflag=False,IC=True)

# 检查AP1版本
ApLogin(ap1)
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_standby_buildnum)
# 检查AP2版本
if ap1_image_type == ap2_image_type:
    res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap1_standby_buildnum)
else:
    res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_version)
#result
printCheckStep(testname, 'Step 2',res1,res2,res3)
###############################################################################
#Step 3
#操作
# 在AC1上指定AP1的集成升级版本为ap1_current_build，并配置ap auto-upgrade
# 重启AP1
# 预期
# AP1重启后，自动升级到ap1_current_buildnum版本
################################################################################
printStep(testname,'Step 3',
          'ac1 config ap1_image_type integrated upgrade version to ap1_current_build',
          'reboot ap1',
          'ap1 upgrade to ap1_current_buildnum after reboot')
res1=res2=1
#operate
# 在AC1上为AP1指定image文件，
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap integrated image-type', ap1_image_type, ap1_ftpupgrade_current_path_6222)

# 重启AP,并等待AP升级
RebootAp(AP=ap1)
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)

# 检查AP1是否被AC1重新管理
res1=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,Ap1_ipv4,'1','Managed','Success')],
                 retry=20,interval=10,waitflag=False,IC=True)
# 检查AP版本
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
SetCmd(switch1, 'no wireless ap integrated image-type', ap1_image_type)      
SetCmd(switch1, 'no ap auto-upgrade')  
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