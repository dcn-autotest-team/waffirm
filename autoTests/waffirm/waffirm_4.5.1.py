#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.5.1.py - test case 4.5.1 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 4.5.1	WMM QoS基本功能测试
# 测试目的：WMM QoS基本功能测试
# 测试环境：同测试拓扑
# 测试描述：wmm的基本功能是能够正确的执行80211的wmm qos字段和802.3的vlan tag 中cos字段之间的转换。
#
#*******************************************************************************
# Change log:
#     - add by lupingc 2017.6.2
#*******************************************************************************

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.5.1'
import re
avoiderror(testname)
printTimer(testname,'Start','the basic function of wmm qos.')

################################################################################
#Step 1
#操作
#在ac1配置network1的SSID为test1，关联vlan4091，采用本地转发
#
#预期
#配置成功。
################################################################################
printStep(testname,'Step 1',
          'set network 1 ssid test1 and vlan 4091,',
          'config success.')
          
res1=res2=1
#operate
EnterWirelessMode(switch1)
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan '+Vlan4091)

data1 = SetCmd(switch1,'show wireless network','1')

#check
res1 = CheckLine(data1,'Default VLAN',Vlan4091,IC=True)
res2 = CheckLine(data1,'SSID',Network_name1,IC=True)

#result
printCheckStep(testname, 'Step 1',res1,res2)


################################################################################
#Step 2
#操作
#STA1连接网络test1，

#预期
# 能够成功关联并获取192.168.11.1X网段的地址
################################################################################
printStep(testname,'Step 3',
          'STA1 connect to network 1,',
          'connect successed.')

res1=res2=1
sta1_ipv4 = ''

#operate
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower) 

#获取STA1的地址
data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
if None != SearchResult1:
    sta1_ipv4 = SearchResult1.group(1)
    if None != re.search(Dhcp_pool1,sta1_ipv4):
        printRes('STA1 ip address: ' + sta1_ipv4)
        res2 = 0
    else:
        res2 = 1
        printRes('get address success but not match ip of vlan 4091')
else:
    res2 = 1
    sta1_ipv4 = '7.7.7.7'
    printRes('Failed: Get ipv4 address of STA1 failed')

res3 = CheckPing(pc1,sta1_ipv4,mode='linux')

#result
printCheckStep(testname, 'Step 2',res1,res2,res3)

################################################################################
#Step 3
#操作
#在s3连接pc的端口s3p5上配置mls qos cos 5，
#通过pc1 ping sta1，pc和 sta1属于同vlan

#
#预期
#在sta1上通过空口抓包，检查下行ICMP REQ报文的wmm qos字段值为5。
################################################################################
printStep(testname,'Step 3',
          's3p5 config mls qos cos 5',
          'pc1 ping sta1,',
          'Check config success.')
          
res1=1
#operate
 
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p5)
SetCmd(switch3,'mls qos cos 5')
SetCmd(pc1,'nohup ping '+sta1_ipv4+' -i 0.2 &')  
data = SetCmd(sta1,'tcpdump -i mon0 icmp -c 1',promoteTimeout=60)
match = re.search('.*?'+sta1_ipv4+'.*?ICMP echo request.*?1 packets captured',data,re.S)
if match !=None:
	res1 = 0
	SetCmd(pc1,'pkill ping')   
	
#result
printCheckStep(testname, 'Step 3',res1)


################################################################################
#Step 4
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 4',
          'Recover initial config for switches.')

#operate


##解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p5)
SetCmd(switch3,'no mls qos cos')

#end
printTimer(testname, 'End')