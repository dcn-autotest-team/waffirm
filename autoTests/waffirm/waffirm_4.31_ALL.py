#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.31.py - test case 4.31 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
# 
# Date 2017-5-16 14:37:33
#
# Features:
# 4.31	PROXY-ARP功能测试
# 测试目的：测试proxy-arp功能
# 测试环境：同测试拓扑
# 测试描述：测试开启proxy-arp后，指向目的终端STA2的arp request报文会由ap代替该目的终端回arp response报文给请求终端STA1
#
#*******************************************************************************
# Change log:
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
#*******************************************************************************

#Package

#Global Definition
 
#Source files

#Procedure Definition 

#Functional Code

# testname = 'waffirm_4.31'
testname = 'TestCase 4.31'
avoiderror(testname)
printTimer(testname,'Start','test PROXY-ARP function')
# 2.4G、5G差异化配置,test24gflag为True代表执行2.4G脚本，False代表执行5G脚本
if test24gflag:
    wlan='wlan0'
else:
    wlan='wlan1'
################################################################################
#Step 1
#操作
# 开启AC1的network1下proxy-arp功能：
# 将proxy-arp功能相关参数下发到profile 1。
#预期
#在AC1上面show wireless network 1可以看到相关的配置
# 在AP上执行get bss wlan0bssvap0  proxy-arp，可以看到proxy-arp 开关为on
################################################################################
printStep(testname,'Step 1',
          'Config proxy-arp in network 1 on AC1',
          'apply ap profile 1')
res1=res2=1
#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'proxy-arp')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#check
data=SetCmd(switch1,'show wireless network 1')
res1 = CheckLineList(data,[('Wireless Proxy ARP','Enable')],IC=True)
# Ap上查看proxy-arp仅作参考
SetCmd(ap1,'\n')
data1=SetCmd(ap1,'get bss '+wlan+'bssvap0  proxy-arp')
# res2=CheckLine(data1,'on',IC=True)
#result
printCheckStep(testname, 'Step 1',res1)
################################################################################
#Step 2
#操作
# 设置STA1、STA2通过dhcp关联网络test1。
#
#预期
#成功关联，并获取192.168.91.X网段的IP地址。Show wireless client summery可以
# 看到STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确, 
# STA2（“MAC Address”显示“STA2MAC”），IP地址的网段正确。
################################################################################
printStep(testname,'Step 2',
          'STA1 connect to test1 sucessfully',
          'STA2 connect to test1 sucessfully')
res1=res2=res3=res4=1
#operate&check
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
res3 = CheckWirelessClientOnline(switch1,sta1mac,'online')
res4 = CheckWirelessClientOnline(switch1,sta2mac,'online')
#result
printCheckStep(testname, 'Step 2',res1,res2,res3,res4)
################################################################################
#Step 3
#操作
#在STA1上面ping STA2
#
#预期
#能够ping通。
################################################################################
printStep(testname,'Step 3',
          'STA1 ping STA2 sucessfully')
res1=res2=1
# check
#获取STA2的地址
sta2_ipresult = GetStaIp(sta2)
sta2_ipv4 = sta2_ipresult['ip']

# STA1和STA2是否能互通
res1 = CheckPing(sta1,sta2_ipv4,mode='linux')  
#result
printCheckStep(testname, 'Step 3',res1)

################################################################################
#Step 4
#操作
#STA1持续向STA2发起arp requet请求。（linux下面使用arping命令来达到发送arp报文）
#预期
#在STA1抓包可以获取到以STA2MAC为源MAC，源IP为STA2IP，目的IP为STA1的arp response报文；
# 在STA2抓包无法获取到以STA1MAC为源MAC，源IP为STA1IP，目的IP为STA2的arp request报文。
################################################################################
printStep(testname,'Step 4',
          'STA1 arping STA2',
          'STA1 can capture packets that source mac is sta2mac,source ip is sta2ip,destination ip is sta1ip',
          'STA2 can not capture packets that source mac is sta1mac,source ip is sta1ip,destination ip is sta2ip')
res1=res2=1
#operate
ConnectDsendWireless(testerip_sta1)
StartDsendCaptureWireless(Port=testerp1_sta1)
DisconnectDsendWireless()
ConnectDsendWireless(testerip_sta2)
StartDsendCaptureWireless(Port=testerp1_sta2)
DisconnectDsendWireless()
SetCmd(sta1,'\n')
SetCmd(sta1,'arping -I ',Netcard_sta1,sta2_ipv4,' -c 10')
# check
# sta1抓包
ConnectDsendWireless(testerip_sta1)
StopDsendCaptureWireless(testerp1_sta1) 
res1=CheckDsendCaptureStreamWireless(testerp1_sta1,SrcMac=sta2mac,DstMac=sta1mac,Arp='1',ArpType='reply')
DisconnectDsendWireless()
# sta2抓包
ConnectDsendWireless(testerip_sta2)
StopDsendCaptureWireless(testerp1_sta2) 
res2=CheckDsendCaptureStreamWireless(testerp1_sta2,Arp='1',SrcMac=sta1mac,ArpType='request')
DisconnectDsendWireless()
res1=0 if res1 > 0 else -1
#result
printCheckStep(testname, 'Step 4',res1,res2)
################################################################################
#Step 5
#操作
#关闭AC1的network1下proxy-arp功能
#将proxy-arp功能相关参数下发到profile 1
#预期
#配置成功。在AC1上面show wireless network 1无proxy-arp配置
# 在AP上执行get bss wlan0bssvap0  proxy-arp，可以看到proxy-arp 开关为off
################################################################################
printStep(testname,'Step 5',
          'Clear proxy-arp configuration in network 1 on AC1',
          'apply ap profile 1')
res1=res2=1
#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'no proxy-arp')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#check
data=SetCmd(switch1,'show wireless network 1')
res1 = CheckLineList(data,[('Wireless Proxy ARP','Disable')],IC=True)
# Ap上查看proxy-arp仅作参考
SetCmd(ap1,'\n')
data1=SetCmd(ap1,'get bss '+wlan+'bssvap0  proxy-arp')
# res2=CheckLine(data1,'off',IC=True)
#result
printCheckStep(testname, 'Step 5',res1)
################################################################################
#Step 6
#操作
#设置STA1、STA2通过dhcp关联网络test1
#
#预期
#成功关联，并获取192.168.91.X网段的IP地址。Show wireless client summery可以看到STA1
# （“MAC Address”显示“STA1MAC”），IP地址的网段正确, STA2（“MAC Address”显示“STA2MAC”），
# IP地址的网段正确
################################################################################
printStep(testname,'Step 6',
          'STA1 connect to test1 sucessfully',
          'STA2 connect to test1 sucessfully')
res1=res2=res3=res4=1
#operate&check
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
res3 = CheckWirelessClientOnline(switch1,sta1mac,'online')
res4 = CheckWirelessClientOnline(switch1,sta2mac,'online')
#result
printCheckStep(testname, 'Step 6',res1,res2,res3,res4)
################################################################################
#Step 7
#操作
#在STA1上面ping STA2
#
#预期
#能够ping通。
################################################################################
printStep(testname,'Step 7',
          'STA1 ping STA2 sucessfully')
res1=res2=1
sta1_ipv4='1.1.1.1'
sta2_ipv4='2.2.2.2'
# check
#获取STA2的地址
data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
data2 = SetCmd(sta2,'ifconfig -v',Netcard_sta2)
SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
SearchResult2 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data2,re.I)
if None != SearchResult1:
	sta1_ipv4 = SearchResult1.group(1)
	if None != re.search(Dhcp_pool1,sta1_ipv4):
		printRes('STA1 ip address: ' + sta1_ipv4)
if None != SearchResult2:
	sta2_ipv4 = SearchResult2.group(1)
	if None != re.search(Dhcp_pool1,sta2_ipv4):
		printRes('STA1 ip address: ' + sta2_ipv4)
		res1 = 0  
		# STA1和STA2是否能互通
		res2 = CheckPing(sta1,sta2_ipv4,mode='linux')  
else:
	res1 = 1
	printRes('Failed: Get ipv4 address of STA1 failed') 
#result
printCheckStep(testname, 'Step 7',res1,res2)

################################################################################
#Step 8
#操作
#STA1持续向STA2发起arp requet请求。（linux下面使用arping命令来达到发送arp报文）
#预期
#在STA1抓包可以获取到以STA2MAC为源MAC，源IP为STA2IP，目的IP为STA1的arp response报文；
# 在STA2抓包无法获取到以STA1MAC为源MAC，源IP为STA1IP，目的IP为STA2的arp request报文。
################################################################################
printStep(testname,'Step 8',
          'STA1 arping STA2',
          'STA1 can capture packets that source mac is sta2mac,source ip is sta2ip,destination ip is sta1ip',
          'STA2 can not capture packets that source mac is sta1mac,source ip is sta1ip,destination ip is sta2ip')
res1=res2=1
#operate
ConnectDsendWireless(testerip_sta1)
StartDsendCaptureWireless(Port=testerp1_sta1)
DisconnectDsendWireless()
ConnectDsendWireless(testerip_sta2)
StartDsendCaptureWireless(Port=testerp1_sta2)
DisconnectDsendWireless()
SetCmd(sta1,'\n')
SetCmd(sta1,'arping -I ',Netcard_sta1,sta2_ipv4,' -c 10')
# check
# sta1抓包
ConnectDsendWireless(testerip_sta1)
StopDsendCaptureWireless(testerp1_sta1) 
res1=CheckDsendCaptureStreamWireless(testerp1_sta1,SrcMac=sta2mac,DstMac=sta1mac,Arp='1',ArpType='reply')
DisconnectDsendWireless()
# sta2抓包
ConnectDsendWireless(testerip_sta2)
StopDsendCaptureWireless(testerp1_sta2) 
res2=CheckDsendCaptureStreamWireless(testerp1_sta2,Arp='1',SrcMac=sta1mac,ArpType='request')
DisconnectDsendWireless()
res1=0 if res1 > 0 else -1
res2=0 if res2 > 0 else -1
#result
printCheckStep(testname, 'Step 8',res1,res2)
################################################################################
#Step 9
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 9',
          'Recover initial config for switches.')
##解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta1)
#end
printTimer(testname, 'End')