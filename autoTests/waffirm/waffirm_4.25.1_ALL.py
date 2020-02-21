# -*- coding: UTF-8 -*-#
#
# *******************************************************************************
# waffirm_4.25.1.py - test case 4.25.1 of waffirm
#
# Author:  fuzf@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.25.1 文件捕获模式的空口抓包
# 测试目的：文件捕获模式下的空口抓包功能。
# 测试环境：同测试拓扑
# 测试描述：开启文件捕获模式，配置相关参数，AC1可以正确下发命令，控制AP1捕获radio1 radio2的报文，并能够实现对mac地址的过滤。
#           同时可以停止AP抓包，并将捕获的报文上传到AC1
#          （STA1的MAC地址：STA1MAC）
#
# *******************************************************************************
# Change log:
#     - 
# *******************************************************************************

# Package

# Global Definition

# Source files

# Procedure Definition

# Functional Code

testname = 'TestCase 4.25.1'
avoiderror(testname)
printTimer(testname, 'Start', "wireless capture")

################################################################################
# Step 1
# 操作
# AC1配置抓包模式为file，packet-num为5000
#
# 预期
# 配置成功
################################################################################
printStep(testname, 'Step 1',
          'Set wireless capture mode file success')

res1 = res2 = 1
# operate
# 检查AC1 flash中是否存在file_capture.pcap文件，如果存在，删除
EnterEnableMode(switch1)
data = SetCmd(switch1, 'dir')
SearchResult1 = re.search('(file_capture.pcap)', data)
if None != SearchResult1:
    SetCmd(switch1, 'delete file_capture.pcap', timeout=1)
    SetCmd(switch1, 'y', timeout=1)

EnterEnableMode(switch1)
SetCmd(switch1, 'wireless capture mode file')
SetCmd(switch1, 'wireless capture packet-num 5000')

# check
data = SetCmd(switch1, 'show wireless capture status')
res1 = CheckLine(data, 'wireless capture mode', 'file', IC=True)
res2 = CheckLine(data, 'wireless capture packet number', '5000', IC=True)

if 0 != res1:
    printRes('Failed:config mode file failed！')
if 0 != res2:
    printRes('Failed:config packet-num failed!')

# result
printCheckStep(testname, 'Step 1', res1, res2)

################################################################################
# Step 2
# 操作
# 将AP1 AP2的radio 1调整到相同的信道，然后配置AP1在radio 1抓包
#
# 预期
# 信道调整成功
################################################################################
printStep(testname, 'Step 2',
          'Set both radio of AP1 and AP2 with the same channel',
          'Start wireless capture on radio 1 of AP1')

res1 = res2 = res3 = res4 = 1
# operate
# 配置AP1 AP2的信道为6
EnterEnableMode(switch1)
SetCmd(switch1, 'wireless ap channel set', ap1mac, 'radio 1 6')

EnterEnableMode(switch1)
SetCmd(switch1, 'wireless ap channel set', ap2mac, 'radio 1 6')

# 检查AP1 AP2的信道配置情况
for i in range(24):
    data1 = SetCmd(switch1, 'show wireless ap', ap1mac, 'radio 1 channel status')
    data2 = SetCmd(switch1, 'show wireless ap', ap2mac, 'radio 1 channel status')
    res1 = CheckLine(data1, 'channel', '6', IC=True)
    res2 = CheckLine(data2, 'channel', '6', IC=True)
    if res1 == 0 and res2 == 0:
        break
    IdleAfter(5)

# 开始抓包
EnterEnableMode(switch1)
SetCmd(switch1, 'wireless capture start ap', ap1mac, 'interface radio 1')
data3 = SetCmd(switch1, 'show wireless capture status | include wireless capture running status')
res3 = CheckLine(data3, 'wireless capture in progress', IC=True)

if 0 != res3:
    printRes("Failed:not start wireless capture!")
# result
printCheckStep(testname, 'Step 2', res1, res2, res3)

################################################################################
# Step 3
# 操作
# STA1关联AP2的test2，并ping网关
#
# 预期
# STA1关联成功，可以ping通pc1_ipv4
################################################################################
printStep(testname, 'Step 3',
          'STA1 connect AP2 test2',
          'STA1 ping gateway success')

res1 = res2 = 1
# operate
res1 = WpaConnectWirelessNetwork(sta1, Netcard_sta1, Network_name2, checkDhcpAddress=Netcard_ipaddress_check2,
                                 bssid=ap2mac_type1_network2)
res2 = CheckPing(sta1, pc1_ipv4, time=30, pingPara='-c 100 -i 0.2 -s 1500', mode='linux')
# check
if 0 != res1:
    printRes('Failed:STA1 not connected AP2 network2')
if 0 != res2:
    printRes('Failed:STA1 can not ping through gateway')

# result
printCheckStep(testname, 'Step 3', res1, res2)

################################################################################
# Step 4
# 操作
# 手动停止抓包，然后检查AC1 flash中的文件
#
# 预期
# 执行成功,在AC1 flash中有file_capture.pcap文件，并且大小不为0
################################################################################

printStep(testname, 'Step 4',
          'wireless capture stop',
          'AC1 dir could see file file_capture.pcap and size not zero')

res1 = res2 = 1

# operate
EnterEnableMode(switch1)
for i in range(5):
    data = SetCmd(switch1, 'wireless capture stop')
    if CheckLine(data, 'Error') != 0:
        break
    IdleAfter(2)
# operate
for i in range(20):
    data = SetCmd(switch1, 'dir')
    res1 = CheckLine(data, 'file_capture.pcap', IC=True)
    res2 = CheckLine(data, '-rwx\s+0\s+file_capture\.pcap')
    if res1 == 0 and res2 != 0:
        res2 = 0
        break
    IdleAfter(2)
# check
if res1 != 0:
    printRes('Failed:AC1 dir could not see file file_capture.pcap!')
if res2 != 0:
    printRes('Failed:file_capture.pcap size is 0!')

# result
printCheckStep(testname, 'Step 4', res1, res2)

################################################################################
# Step 5
# 操作
# AC1配置开启抓包混杂模式，抓包时长为60s，过滤STA1MAC地址，清除抓包个数配置
#
# 预期
# show wireless capture status查看配置成功
################################################################################
printStep(testname, 'Step 5',
          'wireless capture promiscuous-mode',
          'wireless capture duration 60',
          'wireless capture filter-mac sta1mac',
          'no wireless capture packet-num')

res1 = res2 = res3 = res4 = 1

# operate
EnterEnableMode(switch1)
SetCmd(switch1, 'wireless capture promiscuous-mode')
SetCmd(switch1, 'wireless capture duration 60')
SetCmd(switch1, 'wireless capture filter-mac', sta1mac)
SetCmd(switch1, 'no wireless capture packet-num')

data = SetCmd(switch1, 'show wireless capture status', timeout=8)

res1 = CheckLine(data, 'wireless capture promiscuous mode', 'Enable', IC=True)
res2 = CheckLine(data, 'wireless capture duration', '60', IC=True)
res3 = CheckLine(data, 'wireless capture filter mac', sta1mac, IC=True)
res4 = CheckLine(data, 'wireless capture packet number', '5000', IC=True)
res4 = 0 if 0 != res4 else 1

# check
if res1 | res2 | res3 | res4 != 0:
    printRes('Failed:config failed!')

# result
printCheckStep(testname, 'Step 5', res1, res2, res3, res4)

################################################################################
# Step 6
# 操作
# 配置AP1在radio 1抓包
#
# 预期
# 开始抓包成功
################################################################################
printStep(testname, 'Step 6',
          'Start wireless capture on AP1 radio 1')

res1 = 1

# operate
# 检查AC1 flash中是否存在file_capture.pcap文件，如果存在，删除
EnterEnableMode(switch1)
data = SetCmd(switch1, 'dir')
SearchResult1 = re.search('(file_capture.pcap)', data)
if None != SearchResult1:
    SetCmd(switch1, 'delete file_capture.pcap', timeout=1)
    SetCmd(switch1, 'y', timeout=1)
EnterEnableMode(switch1)
for i in range(5):
    SetCmd(switch1, 'wireless capture start ap', ap1mac, 'interface radio 1')
    if CheckLine(data, 'Error') != 0:
        break
    IdleAfter(2)
IdleAfter(2)
data1 = SetCmd(switch1, 'show wireless capture status | include wireless capture running status')
print data1
# check
res1 = CheckLine(data1, 'wireless capture in progress', IC=True)
if res1 != 0:
    printRes('Failed:start wireless capture failed!')

# result
printCheckStep(testname, 'Step 6', res1)

################################################################################
# Step 7
# 操作
# 持续ping网关
#
# 预期
# 能够ping通pc1_ipv4
################################################################################
printStep(testname, 'Step 7',
          'Sta1 connect AP2 radio1 test2',
          'sta1 ping gateway succeed')

res1 = 1

# operate
res1 = CheckPing(sta1, pc1_ipv4, time=60, pingPara='-c 50 -s 1500', mode='linux')
# check
if 0 != res1:
    printRes('Failed:STA1 can not ping through gateway')

# result
printCheckStep(testname, 'Step 7', res1)

################################################################################
# Step 8
# 操作
#
# 预期
# AC1 dir查看有文件file_capture.pcap，并且文件大小不为0
################################################################################
printStep(testname, 'Step 8',
          'wait 200s',
          'AC1 dir can see file file_capture.pcap and file size not 0')

res1 = 1
res2 = 0
# operate
IdleAfter(10)
EnterEnableMode(switch1)
for i in xrange(10):
    data = SetCmd(switch1, 'dir')
    res1 = CheckLine(data, 'file_capture.pcap', IC=True)
    res2 = CheckLine(data, '-rwx\s+0\s+file_capture\.pcap')
    if res1 == 0 and res2 != 0:
        res2 = 0
        break
    IdleAfter(2)

# check
if res1 != 0:
    printRes('Failed:AC1 dir could not see file file_capture.pcap!')
    if res2 != 0:
        printRes('Failed:file_capture.pcap size is 0!')

# result
printCheckStep(testname, 'Step 8', res1, res2)

################################################################################
# Step 9
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 9',
          'Recover initial config')

# operate
EnterEnableMode(switch1)
SetCmd(switch1, 'wireless capture stop')
data = SetCmd(switch1, 'dir')
SearchResult1 = re.search('(file_capture.pcap)', data)
if None != SearchResult1:
    SetCmd(switch1, 'delete file_capture.pcap', timeout=1)
    SetCmd(switch1, 'y', timeout=1)
# end
WpaDisconnectWirelessNetwork(sta1, Netcard_sta1)
printTimer(testname, 'End')
