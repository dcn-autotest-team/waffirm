# -*- coding: UTF-8 -*-#
#
# *******************************************************************************
# waffirm_4.1.2.py - test case 4.1.2 of waffirm_new
#
# Author:  (jinpfb)
#
# Version 1.0.0
#
# Date:  2012-12-7 13:47:23
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 4.1.2  AC通过三层方式自动发现AP
# 测试目的：测试AC通过配置ip发现列表发现AP
# 测试环境：同测试拓扑
# 测试描述：AC1通过配置ip发现列表发现AP1
# （AP1的MAC地址：AP1MAC ；AP1的ip地址是20.1.1.3）
#
# *******************************************************************************
# Change log:
#     - zhangjxp 2017.11.10 RDM50304 修改step2、5
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
# *******************************************************************************

###########???????此脚本需要在初始配置中关掉AP1的ipv6的三层发现，否则即使no掉20.1.1.3，还是会通过ipv6发现

# Package
# Global Definition

# Source files

# Procedure Definition

# Functional Code

testname = 'TestCase 4.1.2'
avoiderror(testname)
printTimer(testname, 'Start', 'test AC discovery AP automatically via L3')

################################################################################
# Step 1
#
# 操作
# 把AP1的ip地址加入发现列表
# AC1(config-wireless)#no discovery vlan-list 20
# AC1(config-wireless)#discovery ip-list 20.1.1.3
#
# 预期
# AC1上show wireless discovery ip-list看到ip发现列表“IP Address”中有“20.1.1.3”
#
################################################################################
printStep(testname, 'Step 1',
          'Config AC1 and S3 to enable discover AP1 automatically',
          'Check the result')

res1 = 1
# operate

EnterEnableMode(switch1)
data1 = SetCmd(switch1, 'show wireless discovery ip-list', timeout=5)

# check
res1 = CheckLine(data1, Ap1_ipv4)

# result
printCheckStep(testname, 'Step 1', res1)

################################################################################
# Step 2
# 操作
# 重起AP1
# WLAN-AP# reboot
#
# 预期
# 重起后AP1被AC1管理。AC1上show wi ap status显示AP的“Status”为“Managed”，
# “Configuration Status”为“Success”
################################################################################
printStep(testname, 'Step 2',
          'Reboot AP1',
          'Check if AC1 managed AP1')

res1 = 1
# operate
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
# ChangeAPMode(ap1, ap1mac, switch1, Ap1cmdtype)
RebootAp(AP=ap1, Type='AP')
IdleAfter(20)
EnterEnableMode(switch1)
res1 = CheckSutCmd(switch1, 'show wireless ap status',
                   check=[(ap1mac, Ap1_ipv4, 'Managed', 'Success')],
                   waittime=5, retry=20, interval=5, IC=True)

# result
printCheckStep(testname, 'Step 2', res1)

################################################################################
# Step 3
#
# 操作
# AC1上用命令show wireless ap < AP1MAC > status查看Discovery Reason
#
# 预期
# AC1上显示 “Discovery Reason”为“IP Poll Received”
################################################################################
printStep(testname, 'Step 3',
          'AC1 show wireless ap <AP1MAC> status',
          'Check the result')

res1 = 1
# operate
EnterEnableMode(switch1)
res1 = CheckSutCmd(switch1, 'show wireless ap ' + ap1mac + ' status',
                   check=[('Discovery Reason', 'IP Poll Received')],
                   waittime=8, retry=10, interval=5, IC=True)
# result
printCheckStep(testname, 'Step 3', res1)

################################################################################
# Step 4
# 操作
# AC1上把20.1.1.3从ip发现列表删除
# AC1(config-wireless)# no discovery ip-list 20.1.1.3
#
# 预期
# AC1上show wireless discovery ip-list看到ip发现列表“IP Address”中没有“20.1.1.3”
################################################################################
printStep(testname, 'Step 4',
          'Delete discovery ip-list 20.1.1.3 AC1',
          'Check the result')

res1 = 1
# operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'no discovery ip-list', Ap1_ipv4)
data1 = SetCmd(switch1, 'show wireless discovery ip-list', timeout=5)

# check
res1 = CheckLine(data1, Ap1_ipv4, IC=True)
res1 = 1 if 0 == res1 else 0

# result
printCheckStep(testname, 'Step 4', res1)

################################################################################
# Step 5
# 操作
# 重起AP1
# WLAN-AP# reboot
#
# 预期
# 重起后AP1不能被AC1管理。AC1上show wi ap status显示AP的“Status”为“Failed”，
################################################################################
printStep(testname, 'Step 5',
          'Reboot AP1',
          'Check if AC1 managed AP1')

res1 = 1

# operate
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap1, ap1mac, switch1, Ap1cmdtype)
IdleAfter(30)
EnterEnableMode(switch1)
data1 = SetCmd(switch1, 'show wireless ap status', timeout=5)

# check
res1 = CheckLine(data1, ap1mac, 'Failed', IC=True)

# result
printCheckStep(testname, 'Step 5', res1)

################################################################################
# Step 6
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 6',
          'Recover initial config')

# AC1恢复
EnterWirelessMode(switch1)
SetCmd(switch1, 'discovery ip-list', Ap1_ipv4)
# IdleAfter(Ap_connect_after_reboot)
CheckSutCmd(switch1, 'show wireless ap status',
            check=[(ap1mac, 'Managed', 'Success'), (ap2mac, 'Managed', 'Success')],
            waittime=5, retry=20, interval=5, IC=True)
# end
printTimer(testname, 'End')
