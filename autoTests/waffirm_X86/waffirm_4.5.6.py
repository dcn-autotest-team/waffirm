#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.5.6.py - test case 4.5.6 of waffirm_new
#
# Author:  (wangyinb,jinpfb)
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Date: 2013-1-22 15:52:39
#
# Features:
# 4.5.6	Client QoS基本功能测试5（Policy）
# 测试目的：测试AP上面能够通过配置Policy对客户的上/下行流量进行控制。
# 测试环境：同测试拓扑
# 测试描述：测试AP上面能够通过配置Policy对客户的上/下行流量进行控制。
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package

s1vlanmac = GetVlanMac(switch1) 
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.5.6'
printTimer(testname,'Start','test policy, the basic function of client qos.')

################################################################################
#Step 1
#操作
# 在AC1配置network1的SSID为test1，关联vlan4092。配置下发到AP1。
# AC1配置：
# Wireless
# Network 1
# Ssid test1
# Vlan 4092
# End
# Wireless ap profile apply 1
#
#预期
#配置下发成功
################################################################################
printStep(testname,'Step 1',\
          'Set network 1 ssid test1 and vlan 4092',\
          'Apply configuration to AP1')

res1=res2=1
#operate

EnterNetworkMode(switch1,'1')
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan '+Vlan4092)

# WirelessApProfileApply(switch1,'1')
    
# IdleAfter(Ac_ap_syn_time)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
data1 = SetCmd(switch1,'show wireless network','1')

#check
res1 = CheckLine(data1,'Default VLAN',Vlan4092,IC=True)
res2 = CheckLine(data1,'SSID',Network_name1,IC=True)

#result
printCheckStep(testname, 'Step 1',res1,res2)

################################################################################
#Step 2
#操作
#开启network1的Client Qos功能。配置QoS规则：
##Access-list 1 permit source 192.168.1.0 0.0.0.255
##Class c
##Match access-group 1
##Policy p
##Class c
##Policy 1000 64
#将policy p绑定到network 1的up方向并下发到AP1上面。
#
#预期
#配置下发成功。
################################################################################

printStep(testname,'Step 2',\
          'set access-list 1 permit source 192.168.92.0 0.0.0.255,',\
          'add class c and match access-group 1,',\
          'add policy p bind class c and set policy 500 64,',\
          'bing policy p to network 1 up direction.')
          
res1=res2=res3=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'access-list 1 permit ' + Dhcp_pool2+ '0 0.0.0.255')
SetCmd(switch1,'class c')
SetCmd(switch1,'match access-group 1')
EnterConfigMode(switch1)
SetCmd(switch1,'policy-map p')
SetCmd(switch1,'class c')
SetCmd(switch1,'policy 2000 64')

#无线全局开启 qos
EnterWirelessMode(switch1)
SetCmd(switch1,'ap client-qos')
#开启network 1 qos
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'client-qos enable')
#将policy p绑定到network 1的up方向并下发到AP1上面
SetCmd(switch1,'client-qos diffserv-policy up p')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')
    
# IdleAfter(Ac_ap_syn_time)
    
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show access-lists')
data2 = SetCmd(switch1,'show policy-map')
data3 = SetCmd(switch1,'show wireless network','1')

#check

res1 = CheckLineInOrder(data1,['access-list 1',\
                               'permit ' + Dhcp_pool2 + '0 0.0.0.255'],IC=True)

res2 = CheckLine(data2,'Policy Map p',IC=True)
res3 = CheckLineList(data3,[('Client QoS Mode','Enable'), \
                            ('Client QoS Diffserv Policy Up','p')],IC=True)

#result
printCheckStep(testname, 'Step 2',res1,res2,res3)

################################################################################
#Step 3
#操作
#STA1和STA2关联到网络test1。
#
#预期
#STA1和STA2关联成功，获取192.168.92.X网段的IP地址。
################################################################################
printStep(testname,'Step 3',\
          'STA1 and STA2 connect to network 1,',\
          'STA1 and STA2 dhcp and get 192.168.92.X ip address.')

res1=res2=res3=res4=1
#operate
sta1_ipv4 = ''
sta2_ipv4 = ''

#STA1,STA2关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap1mac_lower)
IdleAfter(10)

#获取STA1,STA2的地址
data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
data2 = SetCmd(sta2,'ifconfig -v',Netcard_sta2)
SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
SearchResult2 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data2,re.I)

#check
if None != SearchResult1:
    sta1_ipv4 = SearchResult1.group(1)
    if None != re.search(Dhcp_pool2,sta1_ipv4):
        printRes('STA1 ip address: ' + sta1_ipv4)
        res3 = 0
else:
    res3 = 1
    printRes('Failed: Get ipv4 address of STA1 failed') 
    
if None != SearchResult2:
    sta2_ipv4 = SearchResult2.group(1)
    if None != re.search(Dhcp_pool2,sta2_ipv4):
        printRes('STA2 ip address: ' + sta2_ipv4)
        res4 = 0
else:
    res4 = 1
    printRes('Failed: Get ipv4 address of STA2 failed')          
#result
printCheckStep(testname,'Step 3',res1,res2,res3,res4)

################################################################################
#Step 4
#操作
#在STA1上通过CommView发送报文，STA1->STA2，发送速率1Mbps，持续发送
#
#预期
#STA2只能收到500kbps的流量。
################################################################################
printStep(testname,'Step 4',\
          'STA1 start stream to STA2 with 1Mbps,',\
          'STA2 receive packets with 500kbps.')

res1=1

data3 = SetCmd(pc1,'downloadtest -u http://' + sta1_ipv4 + '/upgrade.tar')
re3 = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s',data3)
if re3 is not None:
    speed = re3.group(1)
else:
    speed = 0
if (float(speed) > float(0.1)) and (float(speed) < float(0.20)):
    data3 = SetCmd(pc1,'downloadtest -u http://' + sta1_ipv4 + '/upgrade.tar')
    re3 = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s',data3)
    if re3 is not None:
        speed = re3.group(1)
    else:
        speed = 0

if (float(speed) > float(0.22)) and (float(speed) < float(0.26)):
    res3 = 0
else:
    res3 = 1
#result
printCheckStep(testname, 'Step 4',res3)

################################################################################
#Step 5
#操作
#删除绑定在network 1上面的policy p
##下发配置后 用PC1 pingSTA1,如果能ping通，PC1直接下载STA1的文件，
#如果不能Ping通，STA1在关联网络test1后，PC1再下载STA1的文件
#预期
#STA2可以收到1Mbps的流量。
################################################################################
printStep(testname,'Step 5',\
          'unbind policy p to network 1,',\
          'STA2 can receive 1Mbps.')

res1=1
#operate
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no client-qos diffserv-policy up')

WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
EnterConfigMode(switch1)
SetCmd(switch1,'no policy-map p')
SetCmd(switch1,'no class-map c')

res = CheckPing(pc1,sta1_ipv4,mode='linux',srcip=pc1_ipv4)
if res != 0:
    sta1_ipv4 = ''
    #STA1关联 network1
    res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
    IdleAfter(10)
    #获取STA1的地址
    data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
    SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
    #check
    if None != SearchResult1:
        sta1_ipv4 = SearchResult1.group(1)
        if None != re.search(Dhcp_pool2,sta1_ipv4):
            printRes('STA1 ip address: ' + sta1_ipv4)
    else:
        printRes('Failed: Get ipv4 address of STA1 failed') 

data3 = SetCmd(pc1,'downloadtest -u http://' + sta1_ipv4 + '/upgrade.tar')
re3 = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s',data3)
if re3 is not None:
    speed = re3.group(1)
else:
    speed = 0
if (float(speed) > float(1)):
    res3 = 0
else:
    res3 = 1
  
#result
printCheckStep(testname, 'Step 5',res3)

################################################################################
#Step 6
#操作
#将policy p绑定在network 1的down方向并将配置下发至AP1,。
#
#预期
#配置下发成功。
################################################################################
printStep(testname,'Step 6',\
          'bing policy p to network 1 down direction.,',\
          '.check config success.')

res1=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'no access-list 1')
SetCmd(switch1,'access-list 1 permit ' + re.sub('\d+$','',pc1_ipv4) + '0 0.0.0.255')
SetCmd(switch1,'class c')
SetCmd(switch1,'match access-group 1')
EnterConfigMode(switch1)
SetCmd(switch1,'policy-map p')
SetCmd(switch1,'class c')
SetCmd(switch1,'policy 2000 64')

EnterNetworkMode(switch1,'1')
SetCmd(switch1,'client-qos diffserv-policy down p')

WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless network','1')

#check
res1 = CheckLine(data1,'Client QoS Diffserv Policy Down','p')

#result
printCheckStep(testname, 'Step 6',res1)

################################################################################
#Step 7
#操作
#在STA1上ping PC1,如果能ping通，就在STA1上通过HTTP下载PC1的文件
#如果不能Ping通，STA1关联到网络test1后，在STA1上通过HTTP下载PC1的文件
#
#预期
#STA2只能收到500kbps的流量。
################################################################################
printStep(testname,'Step 7',\
           'STA1 send stream to STA2 with 1Mbps,',\
          'STA2 receive 500kbps.')
          
res1=1
res = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
if res != 0:
    sta1_ipv4 = ''
    #STA1关联 network1
    res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
    IdleAfter(10)
    #获取STA1的地址
    data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
    SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
    #check
    if None != SearchResult1:
        sta1_ipv4 = SearchResult1.group(1)
        if None != re.search(Dhcp_pool2,sta1_ipv4):
            printRes('STA1 ip address: ' + sta1_ipv4)
    else:
        printRes('Failed: Get ipv4 address of STA1 failed') 

data3 = SetCmd(sta1,'downloadtest -u http://' + pc1_ipv4 + ':90/upgrade.tar')
re3 = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s',data3)
if re3 is not None:
    speed = re3.group(1)
else:
    speed = 0

if (float(speed) > float(0.1)) and (float(speed) < float(0.22)):
    data3 = SetCmd(sta1,'downloadtest -u http://' + pc1_ipv4 + ':90/upgrade.tar')
    re3 = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s',data3)
    if re3 is not None:
        speed = re3.group(1)
    else:
        speed = 0

if (float(speed) > float(0.22)) and (float(speed) < float(0.27)):
    res3 = 0
else:
    res3 = 1
printCheckStep(testname, 'Step 7',res3)

################################################################################
#Step 8
#操作
#删除绑定在network 1上面的policy p
#下发配置后 在STA1上PingPC1,如果能ping通，就在STA1上通过HTTP下载PC1的文件，
#如果不能Ping通，STA1关联到网络test1后，在STA1上通过HTTP下载PC1的文件
#预期
#STA2可以收到1Mbps的流量
################################################################################
printStep(testname,'Step 8',\
          'unbind policy p to network 1,',\
          'STA2 can receive 1Mbps')

res1=1
#operate
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no client-qos diffserv-policy down')

WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

res = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
if res != 0:
    #operate
    sta1_ipv4 = ''
    #STA1关联 network1
    res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
    IdleAfter(10)
    #获取STA1的地址
    data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
    SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
    #check
    if None != SearchResult1:
        sta1_ipv4 = SearchResult1.group(1)
        if None != re.search(Dhcp_pool2,sta1_ipv4):
            printRes('STA1 ip address: ' + sta1_ipv4)
    else:
        printRes('Failed: Get ipv4 address of STA1 failed') 

data3 = SetCmd(sta1,'downloadtest -u http://' + pc1_ipv4 + ':90/upgrade.tar')
re3 = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s',data3)
if re3 is not None:
    speed = re3.group(1)
else:
    speed = 0
if (float(speed) > float(1)):
    res3 = 0
else:
    res3 = 1
#result
printCheckStep(testname, 'Step 8',res3)

################################################################################
#Step 9
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 9',\
          'Recover initial config for switches.')

#operate

#解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

#删除qos配置
EnterWirelessMode(switch1)
SetCmd(switch1,'no ap client-qos')
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no','client-qos enable')
SetCmd(switch1,'vlan ' + Vlan4091)

WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

#删除policy 配置
EnterConfigMode(switch1)
SetCmd(switch1,'no policy-map p')
SetCmd(switch1,'no class-map c')
SetCmd(switch1,'no access-list 1')

#end
printTimer(testname, 'End')