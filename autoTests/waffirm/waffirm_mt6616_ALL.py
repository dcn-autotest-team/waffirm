#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_mt6616.py
#
# Author:  (zhangjxp)
#
# Version 1.0.0
#
# Date:  2017-7-27 9:54:28
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# [MT6616]终端无法接入无线网络
# 测试目的：测试终端是否能正常接入网络
# 测试环境：同测试拓扑
# 测试描述：测试多个终端反复上下线后，关联终端表与实际是否相符。
#
#*******************************************************************************
# Change log:
#     - creadte by zhangjxp 2017.7.27
#     - modified by zhangjxp RDM50346 2017.11.9
#     - modified by zhangjxp 修改step2-9,对客户端绝对数量的检测变为相对数量的检测
#*******************************************************************************
#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code
def get_stanum_from_wireless(switch):
    _num = -1
    EnterEnableMode(switch)
    _data = SetCmd(switch,'show wireless status')
    temp = re.search('Total Clients.*?(\d+)\s',_data,re.I)
    if temp:
        _num = int(temp.group(1))
    else:
        print _data
    return _num
    
def get_stanum_from_buffer(switch):
    _num = -1
    EnterEnableMode(switch)
    _data = SetCmd(switch,'show buffer wireless',promotePatten='Total Connections is')
    temp = re.search('wdmOprData->assocClientTree\s+0x[0-9a-z0-9]*\s+\d+\s+(\d+)\s+',_data,re.I)
    if temp:
        _num = int(temp.group(1))
    else:
        print _data
    return _num
    
testname = 'TestCase mt6616'
avoiderror(testname)
printTimer(testname,'Start')

################################################################################
#Step 1
#
#操作
# AC1的network1采用默认的安全接入方式none，即open方式。
#
#预期
# AC1上network 1下配置只有“ssid test1”，以下命令确认：
# AC1(config-wireless)#network 1
# AC1(config-network)#show running-config current-mode
################################################################################
printStep(testname,'Step 1','check the configuration of network 1',
          'there should be only ssid and vlan configuration')
res1=1
#operate
EnterNetworkMode(switch1,1)
data=SetCmd(switch1,'show run c',timeout=5)
# 实际ACnetwork1配置下有ssid和vlan两项配置
res1=CheckLine(data, 'ssid\s+'+Network_name1, 'vlan\s+'+Vlan4091,ML=True)
#result
printCheckStep(testname, 'Step 1', res1)
################################################################################
#Step 2
#操作
# 在AC上查看终端表：
# show wireless status
# show bufferwireless
#
#预期
# show wireless status中Total Clients显示为0,show buffer wireless中
# wdmOprData->assocClientTree的Current Entries显示为0
################################################################################
printStep(testname,'Step 2',
          'AC1:show wireless status',
          'AC1:show bufferwireless',
          'Check Total Clients:0,'
          'Check wdmOprData->assocClientTree:0')
res1=res2=1
#operate
# 因为自动化环境中经常有不明身份的终端自动连接AP，导致step2客户端数量不为0，
# 所以脚本中不再检测客户端的绝对数量，改为检测客户端对于step2的相对数量,
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)
EnterEnableMode(switch1)
SetCmd(switch1,'wireless client  disassociate',timeout=1)
SetCmd(switch1,'y')
CheckSutCmd(switch1,'show wireless client summary',
            check=[('No clients associated to APs')],
            waittime=5,retry=3,interval=1,IC=True)
stanum1_from_wireless = get_stanum_from_wireless(switch1)
stanum1_from_buffer = get_stanum_from_buffer(switch1)
print 'stanum1_from_wireless=',str(stanum1_from_wireless)
print 'stanum1_from_buffer=',str(stanum1_from_buffer)
#result
printCheckStep(testname, 'Step 2', 0)

################################################################################
#Step 3
#操作
# STA1关联test1,在STA1上ping PC1
#
#预期
#成功关联，并获取192.168.91.X网段的IP地址。
# Show wireless client summery可以看到STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
# sta1能够ping通pc1
################################################################################
printStep(testname,'Step 3',
          'STA1 connect to network 1',
          'STA1 ping pc1',
          'STA1 dhcp and get ip address,'
          'sta1 ping pc1 success')

res1=res2=res3=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower,checkDhcpAddress=Dhcp_pool1)
res2 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
EnterEnableMode(switch1)
data=SetCmd(switch1,'show wireless client summary')
res3=CheckLine(data,sta1mac)
#result
printCheckStep(testname, 'Step 3',res1,res2,res3)

################################################################################
#Step 4
#操作
#在AC上查看终端表：
# show wireless status
# show buffer wireless
#
#预期
#Total Clients显示为1，show buffer wireless中wdmOprData->assocClientTree的Current Entries显示为1
################################################################################
printStep(testname,'Step 4',
          'AC1:show wireless status',
          'AC1:show bufferwireless',
          'Check Total Clients:1,'
          'Check wdmOprData->assocClientTree:1')

res1=res2=1
#operate
# 检测客户端数量相对于step2中是否加1
stanum2_from_wireless = get_stanum_from_wireless(switch1)
stanum2_from_buffer = get_stanum_from_buffer(switch1)
print 'stanum2_from_wireless=',str(stanum2_from_wireless)
print 'stanum2_from_buffer=',str(stanum2_from_buffer)
if stanum2_from_wireless - stanum1_from_wireless == 1:
    res1 = 0
if stanum2_from_buffer - stanum1_from_buffer == 1:
    res2 = 0
#result
printCheckStep(testname, 'Step 4', res1,res2)
################################################################################
#Step 5
#操作
# STA2关联test1,在STA2上ping PC1
#
#预期
#成功关联，并获取192.168.91.X网段的IP地址。
# Show wireless client summery可以看到STA2（“MAC Address”显示“STA2MAC”），IP地址的网段正确。
# sta2能够ping通pc1。
################################################################################
printStep(testname,'Step 5',
          'sta2 connect to network 1',
          'sta2 ping pc1',
          'sta2 dhcp and get ip address,'
          'sta2 ping pc1 success')

res1=res2=res3=1
#operate
#sta2关联 network1
res1 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap1mac_lower,checkDhcpAddress=Dhcp_pool1)
res2 = CheckPing(sta2,pc1_ipv4,mode='linux',pingPara=' -c 10')
EnterEnableMode(switch1)
data=SetCmd(switch1,'show wireless client summary')
res3=CheckLine(data,sta2mac)
#result
printCheckStep(testname, 'Step 5',res1,res2,res3)
################################################################################
#Step 6
#操作
#在AC上查看终端表：
# show wireless status
# show buffer wireless
#
#预期
#Total Clients显示为2，show buffer wireless中wdmOprData->assocClientTree的Current Entries显示为2
################################################################################
printStep(testname,'Step 6',
          'AC1:show wireless status',
          'AC1:show bufferwireless',
          'Check Total Clients:2,'
          'Check wdmOprData->assocClientTree:2')

res1=res2=1
#operate
# 检测客户端数量相对于step2中是否加2
stanum3_from_wireless = get_stanum_from_wireless(switch1)
stanum3_from_buffer = get_stanum_from_buffer(switch1)
print 'stanum3_from_wireless=',str(stanum3_from_wireless)
print 'stanum3_from_buffer=',str(stanum3_from_buffer)
if stanum3_from_wireless - stanum1_from_wireless == 2:
    res1 = 0
if stanum3_from_buffer - stanum1_from_buffer == 2:
    res2 = 0
#result
printCheckStep(testname, 'Step 6', res1,res2)
################################################################################
#Step 7
#操作
# 客户端STA1，STA2断开与test1的连接
#
#预期
#客户端下线成功。等待1分钟查看show wireless status中Total Clients显示为0，
# show buffer wireless中wdmOprData->assocClientTree的Current Entries显示为0。
################################################################################
printStep(testname,'Step 7',
          'sta1 and sta2 disconnect to network 0',
          'Check Total Clients:1,'
          'Check wdmOprData->assocClientTree:0')

res1=res2=1
#operate
#sta2关联 network1
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)
# 检测客户端数量是否等于step2中的数量
for i in range(10):
    IdleAfter(10)
    stanum4_from_wireless = get_stanum_from_wireless(switch1)
    stanum4_from_buffer = get_stanum_from_buffer(switch1)
    if stanum4_from_wireless == stanum1_from_wireless:
        res1 = 0
    if stanum4_from_buffer == stanum1_from_buffer:
        res2 = 0
    if res1==0 and res2==0:
        break
print 'stanum4_from_wireless=',str(stanum4_from_wireless)
print 'stanum4_from_buffer=',str(stanum4_from_buffer)
#result
printCheckStep(testname, 'Step 7',res1,res2)
################################################################################
#Step 8
#操作
# sta1接入AP1的network1
#
#预期
#client接入成功，获取了192.168.x.x的地址,sta1 ping PC1，可以ping通
################################################################################
printStep(testname,'Step 8',
          'STA1 connect to network 1',
          'STA1 ping pc1',
          'STA1 dhcp and get ip address,'
          'sta1 ping pc1 success')
res1=res2=res3=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower,checkDhcpAddress=Dhcp_pool1)
res2 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
EnterEnableMode(switch1)
data=SetCmd(switch1,'show wireless client summary')
res3=CheckLine(data,sta1mac)
#result
printCheckStep(testname, 'Step 8', res1,res2,res3)
################################################################################
#Step 9
#操作
#在AC上查看终端表：
# show wireless status
# show buffer wireless
#
#预期
#Total Clients显示为1，show buffer wireless中wdmOprData->assocClientTree的Current Entries显示为1
################################################################################
printStep(testname,'Step 9',
          'AC1:show wireless status',
          'AC1:show bufferwireless',
          'Check Total Clients:1,'
          'Check wdmOprData->assocClientTree:1')

res1=res2=1
#operate
# 检测客户端数量相对于step2中是否加1
stanum5_from_wireless = get_stanum_from_wireless(switch1)
stanum5_from_buffer = get_stanum_from_buffer(switch1)
print 'stanum5_from_wireless=',str(stanum5_from_wireless)
print 'stanum5_from_buffer=',str(stanum5_from_buffer)
if stanum5_from_wireless - stanum1_from_wireless == 1:
    res1 = 0
if stanum5_from_buffer - stanum1_from_buffer == 1:
    res2 = 0

#result
printCheckStep(testname, 'Step 9', res1,res2)
################################################################################
#Step 10
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 10',
          'Recover initial config')

#operate
# sta1下线
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
#end
printTimer(testname, 'End')
