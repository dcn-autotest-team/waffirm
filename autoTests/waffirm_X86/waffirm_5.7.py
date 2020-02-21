#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_5.7.py - test case 5.7 of waffirm
#
# Author:  qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 5.7 AP通过静态IPv4地址发现AC
# 测试目的：测试AP通过配置AC地址发现AC 
# 测试环境：同测试拓扑
# 测试描述：AP1上配置AC1的地址后，AP主动发现AC。AC1的无线地址：1.1.1.1
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 5.7'
printTimer(testname,'Start','Test manage ap via static ip')

################################################################################
#Step 1
#操作
#AC1上关闭主动发现
#S1(config-wireless)#no discovery method
#AC1上show wireless discovery看到“IP Polling Mode”显示“Disable”，
#“L2 Multicast Discovery Mode”显示“Disable”
################################################################################
printStep(testname,'Step 1',\
          'set managed-ap managed-type 1 on ap1')
#operate

EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery method')

data1 = SetCmd(switch1,'show wireless discovery')
res1 = CheckLine(data1,'IP Polling Mode','Disable')
#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#AP1上配置上AC1的无线地址
#后重起AP1
#WLAN-AP# set managed-ap switch-address-1 1.1.1.1
#WLAN-AP# save-running 
#WLAN-AP# reboot

################################################################################

printStep(testname,'Step 2',\
          'Remove configuration of auto discovery on ac1')

SetCmd(ap1,'set managed-ap switch-address-1',StaticIpv4_ac1)
SetCmd(ap1,'save-running')
data1 = SetCmd(ap1,'get managed-ap')
res1 = CheckLine(data1,'switch-address-1\s+' + StaticIpv4_ac1)
RebootAp(AP=ap1)

#result
printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#AC1上查看AP1的状态
#S1#show wi ap statu
#预期
#AC1上show wi ap status显示AP的“Status”为“Managed”，“Configuration Status”为“Success”
################################################################################

printStep(testname,'Step 3',\
          'Check show wi ap status')
res1 = 1
IdleAfter(20)
for i in range(20):
	data1 = SetCmd(switch1,'show wireless ap status')
	res1 = CheckLine(data1,ap1mac,'Managed Success',IC=True)
	if res1 == 0:
		break
	IdleAfter(5)	
# if res1 != 0:
    # IdleAfter(20)
    # data1 = SetCmd(switch1,'show wireless ap status')
    # res1 = CheckLine(data1,ap1mac,'Managed Success',IC=True)
# if res1 != 0:
    # IdleAfter(20)
    # data1 = SetCmd(switch1,'show wireless ap status')
    # res1 = CheckLine(data1,ap1mac,'Managed Success',IC=True)
# if res1 != 0:
    # IdleAfter(20)
    # data1 = SetCmd(switch1,'show wireless ap status')
    # res1 = CheckLine(data1,ap1mac,'Managed Success',IC=True)
# if res1 != 0:
    # IdleAfter(20)
    # data1 = SetCmd(switch1,'show wireless ap status')
    # res1 = CheckLine(data1,ap1mac,'Managed Success',IC=True)
printCheckStep(testname, 'Step 3',res1)

################################################################################
#Step 4
#操作
#AC1上用命令show wireless ap AP1mac status查看Discovery Reason
#预期
#AC1上用命令show wireless ap AP1mac status显示“Discovery Reason”为“Switch IP Configured”
################################################################################

printStep(testname,'Step 4',\
          'Check show wi ap status')

data1 = SetCmd(switch1,'show wireless ap',ap1mac,'status')

res1 = CheckLine(data1,'Discovery Reason','Switch IP Configured')

printCheckStep(testname, 'Step 4',res1)

################################################################################
#Step 5
#操作
#AP1上删除AC1的无线地址
#WLAN-AP# set managed-ap switch-address-1 
#WLAN-AP# save-running 
#预期
#AP1上WLAN-AP# get managed-ap switch-address-1查看显示为空
################################################################################

printStep(testname,'Step 5',\
          'Remove switch-address-1 config of ap1')

SetCmd(ap1,'set managed-ap switch-address-1')
SetCmd(ap1,'save-running')
data1 = SetCmd(ap1,'get managed-ap')

res1 = CheckLine(data1,'switch-address-1')
res2 = CheckLine(data1,'switch-address-1\s+40\.1\.1\.1')

printCheckStep(testname, 'Step 5',res1,not res2)

################################################################################
#Step 6
#操作
#重起AP1
#WLAN-AP# reboot
#预期
#重起后AP1无法被AC1管理
################################################################################

printStep(testname,'Step 6',\
          'Reboot ap1 and ap1 cannot managed by ac1')

RebootAp(AP=ap1)
data1 = SetCmd(switch1,'show wireless ap status')
res1 = CheckLine(data1,ap1mac,'Failed  Not Config')

printCheckStep(testname, 'Step 6',res1)

################################################################################
#Step 7
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 7',\
          'Recover initial config for switches.')

#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery method')
IdleAfter(Apply_profile_wait_time)
#end
EnterEnableMode(switch1)
SetCmd(switch1,'show wireless peer-switch')
EnterWirelessMode(switch1)
SetCmd(switch1,'peer-group 2')
SetCmd(switch1,'peer-group 1')
printTimer(testname, 'End')