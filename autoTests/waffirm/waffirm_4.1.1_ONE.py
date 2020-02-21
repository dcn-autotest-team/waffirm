# -*- coding: UTF-8 -*-#
#
# *******************************************************************************
# waffirm_4.1.1.py - test case 4.1.1 of waffirm_new
#
# Author:  (jinpfb)
#
# Version 1.0.0
#
# Date:  2012-12-7 9:54:28
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 4.1.1  AC通过二层方式自动发现AP
# 测试目的：测试AC通过配置二层vlan发现列表发现AP
# 测试环境：同测试拓扑
# 测试描述：AC1通过配置vlan发现列表发现AP1(AP1的MAC地址：AP1MAC)
#
# *******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
#     - zhangjxp 2017.11.10 RDM50304 修改step2、5
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
# *******************************************************************************
# Package

# Global Definition
# Source files

# Procedure Definition

# Functional Code

testname = 'TestCase 4.1.1'
avoiderror(testname)
printTimer(testname, 'Start', '测试AC通过配置二层vlan发现列表发现AP')

################################################################################
# Step 1
#
# 操作
# AC1上面创建vlan20，将端口s1p1划入vlan20。
# AC1上面将vlan20加入到自动发现的vlan列表。
# AC1(config-wireless)#discovery vlan-list 20
# S3上面将s3p1划入vlan20
#
# 预期
# AC1上show wireless discovery vlan-list看到'VLAN'项已经显示有'0'
#
################################################################################
printStep(testname, 'Step 1',
          'Config AC1 and S3 to enable discover AP1 automatically',
          'Check the result')

res1 = 1
# operate

# AC1 配置
EnterConfigMode(switch1)
SetCmd(switch1, 'vlan', Vlan20)
SetCmd(switch1, 'switchport interface', s1p1)
EnterInterfaceMode(switch1, 'vlan ' + Vlan20)
IdleAfter(3)
SetIpAddress(switch1, If_vlan20_s1_ipv4, '255.255.255.0')

# 关闭初始配置中AP1三层发现
EnterWirelessMode(switch1)
SetCmd(switch1, 'no discovery ip-list', Ap1_ipv4)
SetCmd(switch1, 'no discovery ipv6-list', Ap1_ipv6)

# 打开二层发现
EnterWirelessMode(switch1)
SetCmd(switch1, 'discovery vlan-list', Vlan20)

# S3配置
EnterConfigMode(switch3)
SetCmd(switch3, 'vlan', Vlan20)
SetCmd(switch3, 'switchport interface', s3p1)

EnterEnableMode(switch1)
data1 = SetCmd(switch1, 'show wireless discovery vlan-list', timeout=5)

# check
res1 = CheckLine(data1, Vlan20, 'vlan', IC=True)

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
ChangeAPMode(ap1, ap1mac, switch1, Ap1cmdtype)
IdleAfter(20)
EnterEnableMode(switch1)
res1 = CheckSutCmd(switch1, 'show wireless ap status',
                   check=[(ap1mac, 'Managed', 'Success')],
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
# AC1上显示 “Discovery Reason”为“L2 Poll Received”
################################################################################

printStep(testname, 'Step 3',
          'AC1 show wireless ap <AP1MAC> status',
          'Check the result')

res1 = 1
# operate&check
EnterEnableMode(switch1)
res1 = CheckSutCmd(switch1, 'show wireless ap ' + ap1mac + ' status',
                   check=[('Discovery Reason', 'L2 Poll Received')],
                   waittime=8, retry=10, interval=5, IC=True)

# result
printCheckStep(testname, 'Step 3', res1)

################################################################################
# Step 4
# 操作
# AC1上把vlan 20从vlan发现列表删除
# no discovery vlan-list 20
#
# 预期
# AC1上show wireless discovery vlan-list看到“VLAN”项已经没有“20”
################################################################################

printStep(testname, 'Step 4',
          'Delete discovery vlan-list 20 on AC1',
          'Check the result')

res1 = 1
# operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'no discovery vlan-list', Vlan20)
data1 = SetCmd(switch1, 'show wireless discovery vlan-list')

# check
res1 = CheckLine(data1, Vlan20, 'vlan', IC=True)
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

# operate

# S3恢复
EnterConfigMode(switch3)
SetCmd(switch3, 'vlan', Vlan40, timeout=1)
SetCmd(switch3, 'switchport interface', s3p1, timeout=3)

# AC1恢复
EnterConfigMode(switch1)
SetCmd(switch1, 'no interface vlan', Vlan20, timeout=5)
SetCmd(switch1, 'no vlan', Vlan20, timeout=3)
SetCmd(switch1, 'vlan', Vlan40, timeout=3)
SetCmd(switch1, 'switchport interface', s1p1, timeout=3)

# 开启对AP1的三层发现
EnterWirelessMode(switch1)
SetCmd(switch1, 'discovery ip-list', Ap1_ipv4)
SetCmd(switch1, 'discovery ipv6-list', Ap1_ipv6)
# IdleAfter(Ap_connect_after_reboot)
CheckSutCmd(switch1, 'show wireless ap status',
            check=[(ap1mac, 'Managed', 'Success'), (ap2mac, 'Managed', 'Success')],
            waittime=5, retry=20, interval=5, IC=True)
# end
printTimer(testname, 'End')
