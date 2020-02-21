# -*- coding: UTF-8 -*-#
#
# *******************************************************************************
# waffirm_5.8.py - test case 5.8 of waffirm
#
# Author:  qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 5.8 AC通过静态IPv6地址发现AC
# 测试目的：测试AP能否通过静态配置的AC的IPv6无线地址注册上线。
# 测试环境：同测试拓扑
# 测试描述：在AP上面配置静态的AC的IPv6无线地址自动发现AC并注册上线。
#
# *******************************************************************************
# Change log:
#     - zhangjxp 2017.11.10 RDM50304 修改step2
# *******************************************************************************

# Package
# Global Definition

# Source files

# Procedure Definition

# Functional Code

testname = 'TestCase 5.8'
avoiderror(testname)
printTimer(testname, 'Start', 'Test manage ap via static ipv6 address')

################################################################################
# Step 1
# 操作
# AC1上面将interface loopback1的ipv4地址删除。
# Interface loopback1
# No ip address
# Exit
# AC1上面关闭所有的自动发现功能。
# AC1配置：
# Wireless
# No discovery method
# Show wireless能够看到无线地址变更为2001:20::1。使用show wireless discovery可以看到二层和三层自动发现功能均已经关闭。
# DCWS-6028(config-wireless)#sho wireless discovery
# IP Polling Mode................................ Disable
# L2 Multicast Discovery Mode.................... Disable
################################################################################
printStep(testname, 'Step 1',
          'set managed-ap managed-type 1 on ap1')
# operate
EnterConfigMode(switch3)
SetCmd(switch3, 'ipv6 route ' + StaticIpv6_ac1 + '/128 ' + If_vlan40_s1_ipv6)
EnterConfigMode(switch1)
SetCmd(switch1, 'ipv6 route 2001:20::/64 ' + If_vlan40_s3_ipv6)

EnterInterfaceMode(switch1, 'loopback1')
SetCmd(switch1, 'no ip address')

EnterWirelessMode(switch1)
SetCmd(switch1, 'no discovery method')

data1 = SetCmd(switch1, 'show wireless discovery')
res1 = CheckLine(data1, 'IP Polling Mode', 'Disable')
res2 = CheckLine(data1, 'L2 Multicast Discovery Mode', 'Disable')

# result
printCheckStep(testname, 'Step 1', res1, res2)

################################################################################
# Step 2
# 在AP1上面配置静态的AC的IPv6无线地址2001:20::1。
# set managed-ap switch-ipv6-address-1 2001:20::1
# 在AP1上面get managed-ap可以看到配置的静态IPv6无线地址。
################################################################################

printStep(testname, 'Step 2',
          'Config switch-ipv6-address1')

SetCmd(ap1, 'set managed-ap switch-ipv6-address-1', StaticIpv6_ac1)
SetCmd(ap1, 'save-running')
data1 = SetCmd(ap1, 'get managed-ap', timeout=10)
res1 = CheckLine(data1, 'switch-ipv6-address-1\s+' + StaticIpv6_ac1)
# RebootAp(AP=ap1)
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap1, ap1mac, switch1)
IdleAfter(10)
# result
printCheckStep(testname, 'Step 2', res1)

################################################################################
# Step 3
# 操作
# 等待AP1自动发现AC1并注册上线。
# 预期
# AP1上线后，在AC1上面查看AP1的状态：
# Show wireless ap <ap1-mac> status可以看到AP的发现方式为switch ip configured。
################################################################################

printStep(testname, 'Step 3',
          'Check show wi ap status')

# 检查Ap1是否被AC管理成功
CheckSutCmd(switch1, 'show wireless ap status', check=[(ap1mac, Ap1_ipv6, '1', 'Managed', 'Success')], retry=20,
            interval=5, IC=True)
data1 = SetCmd(switch1, 'show wireless ap', ap1mac, 'status')

res1 = CheckLine(data1, 'Discovery Reason', 'Switch IP Configured')

printCheckStep(testname, 'Step 3', res1)

################################################################################
# Step 4
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 4',
          'Recover initial config for switches.')

# operate
EnterConfigMode(switch3)
SetCmd(switch3, 'no ipv6 route ', StaticIpv6_ac1 + '/128 ' + If_vlan40_s1_ipv6)
EnterConfigMode(switch1)
SetCmd(switch1, 'no ipv6 route 2001:20::/64 ' + If_vlan40_s3_ipv6)

EnterInterfaceMode(switch1, 'loopback1')
SetCmd(switch1, 'ip address ' + StaticIpv4_ac1 + ' 255.255.255.255')

EnterWirelessMode(switch1)
SetCmd(switch1, 'discovery method')

SetCmd(ap1, 'set managed-ap switch-ipv6-address-1 ::')
SetCmd(ap1, 'save-running')
RebootAp(AP=ap1)
# end
printTimer(testname, 'End')
