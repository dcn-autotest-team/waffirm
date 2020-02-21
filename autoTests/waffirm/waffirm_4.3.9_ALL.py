# -*- coding: UTF-8 -*-#
#
# *******************************************************************************
# waffirm_4.3.9.py - test case 4.3.9 of waffirm
#
# Author:  qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.3.9 客户端接入的MAC认证测试
# 测试目的：AP能够根据认证client的MAC来判断是否允许接入。
# 测试环境：同测试拓扑
# 测试描述：AP能够根据认证client的MAC来判断是否允许接入。
#          （STA1的MAC地址：STA1MAC；STA2的MAC地址：STA2MAC）
#
# *******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
# *******************************************************************************
# Package

# Global Definition

# Source files

# Procedure Definition

# Functional Code

testname = 'TestCase 4.3.9'
avoiderror(testname)
printTimer(testname, 'Start', 'Test client access wireless network by mac authenticate')

################################################################################
# Step 1
# 操作
# AC1上设置client的MAC认证方式为本地方式，将STA1的MAC加入kown client表，设置为global-action；
# STA2不在kown client中；全局动作设置为白名单：
# AC1#config
# AC1(config)#wireless
# AC1(config-wireless)#network 1
# AC1(config-network)#mac authentication local
# AC1(config-network)#exit
# AC1(config-wireless)#known-client < STA1MAC > action global-action
# AC1(config-wireless)#mac-authentication-mode white-list
# 将配置下发到AP1。
# wireless ap profile apply 1
# 配置成功。
################################################################################
printStep(testname, 'Step 1',
          'set security mode mac authentication and create white list')
# operate
EnterNetworkMode(switch1, '1')

SetCmd(switch1, 'mac authentication local')
EnterWirelessMode(switch1)
SetCmd(switch1, 'known-client', sta1mac, 'action global-action')
SetCmd(switch1, 'mac-authentication-mode white-list')
WirelessApplyProfileWithCheck(switch1, ['1'], [ap1mac])

# check
data1 = SetCmd(switch1, 'show wireless network 1', timeout=5)
res1 = CheckLine(data1, 'MAC Authentication', 'Local')
data2 = SetCmd(switch1, 'show wireless known-client', timeout=5)
res3 = CheckLine(data2, sta1mac, 'global-action')
data3 = SetCmd(switch1, 'show wireless mac-authentication-mode', timeout=5)
res4 = CheckLine(data3, 'mac-authentication-mode', 'white-list')

# result
printCheckStep(testname, 'Step 1', res1, res3, res4)

################################################################################
# Step 2
# 使用STA1关联网络test1。
# 成功关联并获取192.168.91.X网段的IP地址。在AC1上面show wireless client summary可以看到STA1。
################################################################################

printStep(testname, 'Step 2',
          'STA1 connect to wireless network,',
          'should be successfully')

res3 = WpaConnectWirelessNetwork(sta1, Netcard_sta1, Network_name1, connectType='open',
                                 checkDhcpAddress=Netcard_ipaddress_check, bssid=ap1mac_lower)

res4 = CheckWirelessClientOnline(switch1, sta1mac, 'online')

# result
printCheckStep(testname, 'Step 2', res3, res4)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res3
if GetWhetherkeepon(keeponflag):
    ################################################################################
    # Step 3
    # 操作
    # 在STA1上ping PC1
    #
    # 预期
    # 能够ping通。
    ################################################################################
    printStep(testname, 'Step 3',
              'STA1 ping pc1',
              'ping success.')

    res1 = CheckPing(sta1, pc1_ipv4, mode='linux')

    printCheckStep(testname, 'Step 3', res1)

################################################################################
# Step 4
# 操作
# 使用STA2关联网络test1。
#
# 预期
# 关联失败。在AC1上面show wireless client summary不能看到STA2。
################################################################################
printStep(testname, 'Step 4',
          'STA2 cannot connect with network1,',
          'show wireless client summary and no STA2 client online.')

# sta连接无线时会出现状态偶然变为completed，但实际上并未连接上无线，遇到此情况则再检查一次sta的状态，若仍为completed则fail
res3 = WpaConnectWirelessNetwork(sta2, Netcard_sta2, Network_name1, connectType='open', reconnectflag=0,
                                 bssid=ap1mac_lower)
res3 = 0 if res3 != 0 else 1
res4 = CheckWirelessClientOnline(switch1, sta2mac, 'online', retry=6)
res4 = 0 if res4 != 0 else 1
printCheckStep(testname, 'Step 4', res3, res4)

################################################################################
# Step 5
# 修改STA1的动作为deny，全局为黑名单：
# AC1(config-wireless)#known-client < STA1MAC >  action deny
# AC1(config-wireless)#mac-authentication-mode black-list
# 设置成功。
################################################################################
printStep(testname, 'Step 5',
          'Change sta1 action deny,',
          'and set mac-authentication-mode black-list')

EnterWirelessMode(switch1)
SetCmd(switch1, 'known-client', sta1mac, 'action deny')
SetCmd(switch1, 'mac-authentication-mode black-list')
WirelessApplyProfileWithCheck(switch1, ['1'], [ap1mac])

data2 = SetCmd(switch1, 'show wireless known-client')
res4 = CheckLine(data2, sta1mac, 'deny')
data3 = SetCmd(switch1, 'show wireless mac-authentication-mode')
res5 = CheckLine(data3, 'mac-authentication-mode', 'black-list')

# result
printCheckStep(testname, 'Step 5', res4, res5)

################################################################################
# Step 6
# 操作
# 使用STA1关联网络test1。
#
# 预期
# 关联失败。在AC1上面show wireless client summary不能看到STA1。
################################################################################
printStep(testname, 'Step 6',
          'STA1 can not associate with wireless network ')

res1 = WpaConnectWirelessNetwork(sta1, Netcard_sta1, Network_name1, connectType='open', reconnectflag=0,
                                 bssid=ap1mac_lower)
res1 = 0 if res1 != 0 else 1
res2 = CheckWirelessClientOnline(switch1, sta1mac, 'online', retry=6)
res2 = 0 if res2 != 0 else 1
printCheckStep(testname, 'Step 6', res1, res2)

################################################################################
# Step 7
# 操作
# 使用STA2关联网络test1。
#
# 预期
# 关联成功并获取192.168.91.X网段的IP地址。在AC1上面show wireless client summary可以看到STA2。
################################################################################

printStep(testname, 'Step 7',
          'STA1 disconnect with network1,',
          'show wireless client summary and no STA1 client online.')

res3 = WpaConnectWirelessNetwork(sta2, Netcard_sta2, Network_name1, connectType='open',
                                 checkDhcpAddress=Netcard_ipaddress_check, bssid=ap1mac_lower)

res4 = CheckWirelessClientOnline(switch1, sta2mac, 'online')

printCheckStep(testname, 'Step 7', res3, res4)

################################################################################
# Step 8
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 8',
          'Recover initial config for switches.')

# operate
WpaDisconnectWirelessNetwork(sta1, Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2, Netcard_sta2)
EnterNetworkMode(switch1, 1)
SetCmd(switch1, 'no mac authentication')
EnterWirelessMode(switch1)
SetCmd(switch1, 'no', 'known-client', sta1mac)
SetCmd(switch1, 'no mac-authentication-mode')
WirelessApplyProfileWithCheck(switch1, ['1'], [ap1mac])

# end
printTimer(testname, 'End')
