#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.5.4.py - test case 4.5.4 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 4.5.4	Client QoS基本功能测试3（MAC ACL）
# 测试目的：测试AP上面能够通过配置MAC ACL对客户的上/下行流量进行控制。
# 测试环境：同测试拓扑
# 测试描述：在AP的vap上绑定mac acl，可以根据mac信息控制流量的转发，绑定acl可以分为
#           up方向和down方向，分别对通过ap的上行流量和下行流量进行控制
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package

#Global Definition
staticIp_sta1 = If_vlan4091_s2_ipv4
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.5.4'
printTimer(testname,'Start','test mac-acl, the basic function of client qos.')

################################################################################
#Step 1
#操作
#UWS上面配置MAC MAC-ACL：
##Access-list 1100 deny host-source-mac <STA1-MAC> any-destination-mac
##Access-list 1100 permit any-source-mac any-destination-mac
##Access-list 1101 deny hostany-source-mac <PC1-MAC> host-destination-mac <STA1-MAC>
##Access-list 1101 permit any-source-mac any-destination-mac
##开启无线全局以及network1的Client Qos功能。
##将ACL 1100绑定到network 1上行方向，ACL 1101绑定到network 1的下行方向并把配置下发到AP1。
##Wireless
##Ap client-qos
##Network 1
##Client-qos enable
##client-qos access-control up mac 1100
##client-qos access-control down mac 1101
##exit
##exit
##exit
##wireless ap profile apply 1
#
#预期
#配置成功。
################################################################################
printStep(testname,'Step 1',\
          'set ip acl 100 deny icmp source 192.168.91.0 0.0.0.255 host-destination 25.1.1.1192.168.10.2,',\
          'access-list 100 permit any-source any-destination,',\
          'access-list 101 deny icmp host-source 192.168.10.2 destination 192.168.91.0 0.0.0.255,',\
          'access-list 101 permit any-source any-destination,',\
          'config success.')

res1=res2=res3=res4=1
#operate

#无线全局开启 qos
EnterWirelessMode(switch1)
SetCmd(switch1,'ap client-qos')

#配置MAC ACL 
EnterConfigMode(switch1)
SetCmd(switch1,'access-list 1100 deny host-source-mac',sta1mac,'any-destination-mac')
SetCmd(switch1,'access-list 1100 permit any-source-mac any-destination-mac')
SetCmd(switch1,'access-list 1101 deny any-source-mac host-destination-mac',sta1mac)
SetCmd(switch1,'access-list 1101 permit any-source-mac any-destination-mac')

EnterNetworkMode(switch1,'1')
SetCmd(switch1,'client-qos enable')
SetCmd(switch1,'client-qos access-control up mac 1100')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')

# IdleAfter(Ac_ap_syn_time) 

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show access-lists')
data2 = SetCmd(switch1,'show wireless')
data3 = SetCmd(switch1,'show wireless network','1')

#check
res1 = CheckLineInOrder(data1,['access-list 1100',\
                               'deny host-source-mac\s*'+sta1mac+'\s*any-destination-mac', \
                               'permit any-source-mac any-destination-mac'],IC=True)
res2 = CheckLineInOrder(data1,['access-list 1101',\
                               'deny any-source-mac host-destination-mac\s*'+sta1mac, \
                               'permit any-source-mac any-destination-mac'],IC=True)

res3 = CheckLine(data2,'AP Client QoS Mode','Enable',IC=True)

res4 = CheckLineList(data3,[('Client QoS Mode','Enable'), \
                            ('Client QoS Access Control Up','MAC - 1100')],IC=True)
# res5 = CheckLine(data3,'Client QoS Access Control Down','MAC - 1101')

#result
printCheckStep(testname, 'Step 1',res1,res2,res3,res4)

################################################################################
#Step 2
#操作
#STA1关联到网络test1
#
#预期
#STA1关联成功，获取手动配置 192.168.91.x网段的地址。
################################################################################
printStep(testname,'Step 2',\
          'STA1 connect to network 1,',\
          'Config static ip "192.168.91.x" for STA1')

res1=res2=1 
         
#operate

#!!!!!!!!!!!!此处已将 STA1的mac地址deny ,因此STA1无法通过DHCP 获取地址，需要静态配置

#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)

#手动配置STA1地址
SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask 255.255.255.0')

#获取已配置地址
data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)

#check
if None != SearchResult1: 
    if SearchResult1.group(1).strip() == staticIp_sta1:
        printRes('STA1 ip address: ' + staticIp_sta1)
        res2 = 0  
else:
    res2 = 1
    printRes('Failed: Config static ip for STA1 failed') 

#result
printCheckStep(testname, 'Step 2',res1,res2)

################################################################################
#Step 3
#操作
#在STA1上面ping PC1。
#
#预期
#不能ping通。PC1不能收到STA1的ping包。
################################################################################

printStep(testname,'Step 3',\
          'STA1 ping pc1,',\
          'ping failed.')

res1 = 0
#operate

# STA1 ping PC1
SetCmd(sta1,'route add -net default gw',If_vlan4091_s1_ipv4)
res1 = CheckPing(sta1,pc1_ipv4,mode='linux')

#check
res1 = 0 if 0 != res1 else 1

#result
printCheckStep(testname, 'Step 3',res1)
################################################################################
#Step 4
#操作
#在ac1的network1下取消上行方向的mac acl绑定，并下发配置。
#等待sta1关联test1后，在STA1上面ping PC1
#
#预期
#可以ping通，PC1能收到STA1的ping包
################################################################################
printStep(testname,'Step 4',\
          'Delete MAC ACL configuration on network1 up stream,', \
          'pc1 ping STA1 succeed.')

res1=res2=1
#operate

# STA1 解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

#network1下取消上行方向的acl绑定
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no client-qos access-control up')

#配置下发
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
 
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)

#手动配置STA1地址
SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask 255.255.255.0')

#获取已配置地址
data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)

#check
if None != SearchResult1: 
    if SearchResult1.group(1).strip() == staticIp_sta1:
        printRes('STA1 ip address: ' + staticIp_sta1)
        res2 = 0  
else:
    res2 = 1
    printRes('Failed: Config static ip for STA1 failed') 

#check
SetCmd(sta1,'route add -net default gw',If_vlan4091_s1_ipv4)
res2 = CheckPing(sta1,pc1_ipv4,mode='linux')

#result
printCheckStep(testname, 'Step 4',res1,res2)

################################################################################
#Step 5
#操作
#在AC1上将MAC ACL 1101绑定到network 1的下行方向
#STA1关联到网络test1
#
#预期
# Show wireless network 1 能看到：
# Client QoS Mode............Enable
# Client QoS Access Control Down................... IP - 101
# STA1关联成功，手动配置192.168.91.X网段的IP地址
################################################################################
printStep(testname,'Step 5',\
          'Bind MAC ACL 1101 to network 1 down stream,', \
          'STA1 connect to test1')

res1=res2=1
#operate

# STA1 解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

#将ACL 101绑定到network 1下行方向
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'client-qos access-control down mac 1101')

#配置下发
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)

#手动配置STA1地址
SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask 255.255.255.0')

#获取已配置地址
data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)

#check
if None != SearchResult1: 
    if SearchResult1.group(1).strip() == staticIp_sta1:
        printRes('STA1 ip address: ' + staticIp_sta1)
        res2 = 0  
else:
    res2 = 1
    printRes('Failed: Config static ip for STA1 failed') 

#result
printCheckStep(testname, 'Step 5',res1,res2)

################################################################################
#Step 6
#操作
#在PC1上ping STA1
#
#预期
#不能ping通,STA1不能收到PC1的ping包
################################################################################
printStep(testname,'Step 6',\
          'PC1 ping STA1 failed')

res1 = 0
#operate

# STA1 ping PC1
SetCmd(sta1,'route add -net default gw',If_vlan4091_s1_ipv4)
res1 = CheckPing(pc1,staticIp_sta1,mode='linux',srcip=pc1_ipv4)

#check
res1 = 0 if 0 != res1 else 1

#result
printCheckStep(testname, 'Step 6',res1)

################################################################################
#Step 7
#操作
#在ac1的network1下取消下行方向的MAC ACL绑定，并下发配置。
#等待sta1关联test1后，在pc1上面ping STA1
#
#预期
#可以ping通，STA1能收到PC1的ping包
################################################################################
printStep(testname,'Step 7',\
          'Delete MAC ACL configuration on network1 down stream,', \
          'pc1 ping STA1 succeed.')

res1=res2=res3=1
#operate

# STA1 解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

#network1下取消下行方向的acl绑定
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no client-qos access-control down')

#配置下发
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)

#手动配置STA1地址
SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask 255.255.255.0')

#获取已配置地址
data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)

#check
if None != SearchResult1: 
    if SearchResult1.group(1).strip() == staticIp_sta1:
        printRes('STA1 ip address: ' + staticIp_sta1)
        res2 = 0  
else:
    res2 = 1
    printRes('Failed: Config static ip for STA1 failed') 
        
#check
SetCmd(sta1,'route add -net default gw',If_vlan4091_s1_ipv4)
res3 = CheckPing(pc1,staticIp_sta1,mode='linux',srcip=pc1_ipv4)

#result
printCheckStep(testname, 'Step 7',res1,res2,res3)

################################################################################
#Step 8
#操作
#关闭network 1的Client QoS。配置下发到AP1。
##Wireless
##Network 1
##No client-qos enable
##Exit
##Exit
##Exit
##Wireless ap profile apply 1
#
#预期
#配置下发成功
################################################################################
printStep(testname,'Step 8',\
          'close client-qos of network 1',\
          'apply ap profile 1 to ap',\
          'Check config success.')

res1=1
#operate
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no','client-qos enable')

#配置下发
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

data1 = SetCmd(switch1,'show wireless network','1')

#check
res1 = CheckLine(data1,'Client QoS Mode','Disable',IC=True)

#result
printCheckStep(testname, 'Step 8',res1)

################################################################################
#Step 9
#操作
#在STA1上面ping PC1。
#
#预期
#可以ping通
################################################################################
printStep(testname,'Step 9',\
          'STA1 ping pc1,',\
          'ping success.')

res1=1
#operate
res1 = CheckPing(sta1,pc1_ipv4,mode='linux')

#result
printCheckStep(testname, 'Step 9',res1)

################################################################################
#Step 10
#操作
#在PC1上面ping STA1。
#
#预期
#可以ping通。
################################################################################
printStep(testname,'Step 10',\
           'pc ping STA1,',\
          'ping success.')

res1=1
#operate

#check
res1 = CheckPing(pc1,staticIp_sta1,mode='linux',srcip=pc1_ipv4)

#result

printCheckStep(testname,'Step 10',res1)

################################################################################
#Step 11
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 11',\
          'Recover initial config for switches.')

#operate

#解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

##删除qos配置
EnterWirelessMode(switch1)
SetCmd(switch1,'no ap client-qos')
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no client-qos access-control up')
SetCmd(switch1,'no client-qos access-control down')
                                         
#清除 acl 1100,1101                                          
EnterConfigMode(switch1)
SetCmd(switch1,'no access-list 1100')
SetCmd(switch1,'no access-list 1101')

#配置下发
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

#end
printTimer(testname, 'End')