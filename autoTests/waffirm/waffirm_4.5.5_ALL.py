#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.5.5.py - test case 4.5.5 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 4.5.5	Client QoS基本功能测试4（IPv6 ACL）
# 测试目的：测试AP上面能够通过配置IPv6 ACL对客户的上/下行流量进行控制。
# 测试环境：同测试拓扑
# 测试描述：在AP的vap上绑定IPv6 acl，可以控制特定的IPv6流量的转发，绑定acl可以分
#           为up方向和down方向，分别对通过ap的上行流量和下行的IPv6流量进行控制
#
#*******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
#*******************************************************************************

#Package

#Global Definition
staticIpv6_sta1 = '2001:91::100'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.5.5'
avoiderror(testname)
printTimer(testname,'Start','test ipv6-acl, the basic function of client qos.')

suggestionList = []

################################################################################
#Step 1
#操作
# 在AC1配置network1的SSID为test1，关联vlan4091。配置下发到AP1。
# AC1配置：
# Wireless
# Network 1
# Ssid test1
# Vlan 4091
# End
# Wireless ap profile apply 1
#
#预期
#配置下发成功
################################################################################
printStep(testname,'Step 1',
          'Set network 1 ssid test1 and vlan 4091',
          'Apply configuration to AP1')

res1=res2=1
#operate

EnterNetworkMode(switch1,'1')
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan '+Vlan4091)

WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless network','1')

#check
res1 = CheckLine(data1,'Default VLAN',Vlan4091,IC=True)
res2 = CheckLine(data1,'SSID',Network_name1,IC=True)

#result
printCheckStep(testname, 'Step 1',res1,res2)

################################################################################
#Step 2
#操作
#Sta1启用ipv6，无线网卡的ipv6地址为 2001:91::100/64,
#关联到test1,Sta1 ping 2001:91::1
#
#预期
#Sta1关联成功，sta1可以ping通2001:91::1(s3 的int vlan 4091的ipv6地址)
################################################################################
printStep(testname,'Step 2',
          'STA1 connect to network 1,',
          'Config static ipv6 2001:91::100/64 for STA1',
          'STA1 ping interface vlan of vlan4091 on S1')

res1=res2=-1 
         
#operate

#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)

#手动配置STA1 ipv6 地址
SetCmd(sta1,'ifconfig '+ Netcard_sta1 + ' inet6 add',staticIpv6_sta1 + '/64')
SetCmd(sta1,'ping6',If_vlan4091_s1_ipv6,promotePatten = 'PING',promoteTimeout=10)
IdleAfter(10)
data1 = SetCmd(sta1,'\x03',timeout = 2)

#check
res2 = int(str(GetValueBetweenTwoValuesInData(data1,'transmitted,','received')).strip()) 
res2 = 0 if res2 > 0 else 1

#result
printCheckStep(testname, 'Step 2',res1,res2)

################################################################################
#Step 3
#操作
#开启network1的Client Qos功能。配置IPv6 ACL：
##Access-list 500 deny host-source 2001::1
##Access-list 500 permit any-source
##Access-list 501 deny host-source 2001::2
##Access-list 501 permit any-source
##将ACL 500绑定到network 1上行方向并把配置下发到AP1。
#
##Sta1关联到test1后，ping 2001:91::1
#
#预期
#配置下发成功,Sta1不能ping通2001:91::1。
################################################################################
printStep(testname,'Step 3',
          'access-list 500 deny host-source 2001:91::100,',
          'access-list 500 permit any-source,',
          'access-list 501 deny host-source 2001:91::1,',
          'access-list 501 permit any-source,',
          'bind 500 to network client-qos up direction,',
          'STA1 connect to test1 again and ping 2001:91::1 failed.')
          
res1=res2=res3=res4=res5=res6=1          
#operate

# STA1 解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

#配置IPV6 ACL规则
EnterConfigMode(switch1)
SetCmd(switch1,'ipv6 access-list 500 deny host-source',staticIpv6_sta1)
SetCmd(switch1,'ipv6 access-list 500 permit any-source')
SetCmd(switch1,'ipv6 access-list 501 deny host-source',If_vlan4091_s1_ipv6)
SetCmd(switch1,'ipv6 access-list 501 permit any-source')

#无线全局开启 qos
EnterWirelessMode(switch1)
SetCmd(switch1,'ap client-qos')
#开启network 1 qos
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'client-qos enable')

#将ACL 500绑定到network 1上行方向并把配置下发到AP1
SetCmd(switch1,'client-qos access-control up ipv6 500')

#配置下发
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show ipv6 access-lists')
data2 = SetCmd(switch1,'show wireless')
data3 = SetCmd(switch1,'show wireless network','1')

#STA1关联 network1
res5 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)
#STA1 ping 2001:92::1
SetCmd(sta1,'ifconfig '+ Netcard_sta1 + ' inet6 add',staticIpv6_sta1 + '/64')
SetCmd(sta1,'ping6',If_vlan4091_s1_ipv6,promotePatten = 'PING',promoteTimeout=10)
IdleAfter(10)
data0 = SetCmd(sta1,'\x03',timeout = 2)
res6 = int(str(GetValueBetweenTwoValuesInData(data0,'transmitted,','received')).strip()) 

#check
res1 = CheckLineInOrder(data1,['ipv6 access-list 500',
                               'deny host-source '+ staticIpv6_sta1,
                               'permit any-source'],IC=True)
res2 = CheckLineInOrder(data1,['ipv6 access-list 501',
                               'deny host-source '+ If_vlan4091_s1_ipv6,
                               'permit any-source'],IC=True)

res3 = CheckLine(data2,'AP Client QoS Mode','Enable',IC=True)
res4 = CheckLineList(data3,[('Client QoS Mode','Enable'),
                            ('Client QoS Access Control Up','IPV6 - 500')],IC=True)
if res5 == 3:
    suggestionList.append('Suggestions: Step 3 failed reason MAYBE RDM17192')

#result
printCheckStep(testname, 'Step 3',res1,res2,res3,res4,res5,res6)

################################################################################
#Step 4
#操作
#在ACL 500的network1下取消上行方向的ACL 绑定，并下发配置。
#等待sta1关联test1后，ping 2001:91::1
#
#预期
#可以ping通
################################################################################
printStep(testname,'Step 4',
          'Delete ACL 500 configuration on network1 up stream,',
          'STA1 ping 2001:91::1 succeed.')

res1=res2=-1
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
#STA1 ping 2001:92::1
SetCmd(sta1,'ifconfig '+ Netcard_sta1 + ' inet6 add',staticIpv6_sta1 + '/64')
SetCmd(sta1,'ping6',If_vlan4091_s1_ipv6,promotePatten = 'PING',promoteTimeout=10)
IdleAfter(10)
data0 = SetCmd(sta1,'\x03',timeout = 2)
res2 = int(str(GetValueBetweenTwoValuesInData(data0,'transmitted,','received')).strip()) 
res2 = 0 if res2 > 0 else 1 

#check

#result
printCheckStep(testname, 'Step 4',res1,res2)

################################################################################
#Step 5
#操作
#从S1 ping sta1（2001:91::100）（下行流量）
#
#预期
#可以ping通sta1
################################################################################
printStep(testname,'Step 5',
          'S1 ping STA1 succeed')

res1=-1
#operate

#S1 ping STA1 (2001:91::100)
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    StartDebug(switch1)
    SetCmd(switch1,'ping6',staticIpv6_sta1,promotePatten = 'Send',promoteTimeout=10)
    IdleAfter(10)
    SetCmd(switch1,'\x03',timeout=1)
    data0 = StopDebug(switch1)
    res1 = int(str(GetValueBetweenTwoValuesInData(data0,'rate is','percent')).strip()) 
else:
    StartDebug(switch3)
    EnterEnableMode(switch3)
    SetCmd(switch3,'ping6',staticIpv6_sta1,promotePatten = 'Send',promoteTimeout=10)
    IdleAfter(10)
    SetCmd(switch3,'\x03',timeout=1)
    data0 = StopDebug(switch3)
    res1 = int(str(GetValueBetweenTwoValuesInData(data0,'rate is','percent')).strip())
    
res1 = 0 if res1 > 0 else 1 

#check

#result
printCheckStep(testname, 'Step 5',res1)

################################################################################
#Step 6
#操作
#将ACL 501绑定到network 1下行方向并把配置下发到AP1
#Sta1关联到test1后，从s1 ping sta1（2001:91::100）
#
#预期
#Show wireless network 1 能看到：
# Client QoS Mode............Enable                          
# Client QoS Access Control Down...................IPv6 - 501
# 不能ping通sta1
################################################################################
printStep(testname,'Step 6',
          'Bind ACL 501 to network1 down stream,',
          'STA1 connect to test1 again',
          'S1 ping STA1 failed')

res1=res2=res3=-1
#operate

# STA1 解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

#将ACL 501绑定到network 1下行方向
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'client-qos access-control down ipv6 501')

#配置下发
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless network','1')

#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)
SetCmd(sta1,'ifconfig '+ Netcard_sta1 + ' inet6 add',staticIpv6_sta1 + '/64')
res2 = CheckLineList(data1,[('Client QoS Mode','Enable'),
                            ('Client QoS Access Control Down','IPV6 - 501')],IC=True)

#S1 ping STA1 (2001:92::100)
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    StartDebug(switch1)
    SetCmd(switch1,'ping6',staticIpv6_sta1,promotePatten = 'Send',promoteTimeout=10)
    IdleAfter(10)
    SetCmd(switch1,'\x03',timeout=1)
    data0 = StopDebug(switch1)
    res3 = int(str(GetValueBetweenTwoValuesInData(data0,'rate is','percent')).strip())                          
else:
    StartDebug(switch3)
    SetCmd(switch3,'ping6',staticIpv6_sta1,promotePatten = 'Send',promoteTimeout=10)
    IdleAfter(10)
    SetCmd(switch3,'\x03',timeout=1)
    data0 = StopDebug(switch3)
    res3 = int(str(GetValueBetweenTwoValuesInData(data0,'rate is','percent')).strip())   
#check
   
#result
printCheckStep(testname, 'Step 6',res1,res2,res3)

################################################################################
#Step 7
#操作
#取消ACL 501到network 1下行方向绑定，并把配置下发到AP1
#Sta1关联到test1后，从s3 ping sta1（2001:91::100
#
#预期
#能ping通sta1
################################################################################
printStep(testname,'Step 7',
          'Delete ACL 501 configuration on network1 down stream,',
          'S1 ping STA1 succeed.')

res1=res2=-1
#operate

# STA1 解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

#取消ACL 501到network 1下行方向绑定
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no client-qos access-control down')

#配置下发
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless network','1')

#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)
SetCmd(sta1,'ifconfig '+ Netcard_sta1 + ' inet6 add',staticIpv6_sta1 + '/64')
#S1 ping STA1 (2001:92::100)
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    StartDebug(switch1)
    SetCmd(switch1,'ping6',staticIpv6_sta1,promotePatten = 'Send',promoteTimeout=10)
    IdleAfter(10)
    SetCmd(switch1,'\x03',timeout=1)
    data0 = StopDebug(switch1)
    res2 = int(str(GetValueBetweenTwoValuesInData(data0,'rate is','percent')).strip()) 
else:
    StartDebug(switch3)
    SetCmd(switch3,'ping6',staticIpv6_sta1,promotePatten = 'Send',promoteTimeout=10)
    IdleAfter(10)
    SetCmd(switch3,'\x03',timeout=1)
    data0 = StopDebug(switch3)
    res2 = int(str(GetValueBetweenTwoValuesInData(data0,'rate is','percent')).strip()) 

res2 = 0 if res2 > 0 else 1                             

#check
                            
#result
printCheckStep(testname, 'Step 7',res1,res2)

################################################################################
#Step 8
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 8',
          'Recover initial config for switches.')

#operate

#解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
#删除手工配置ipv6 地址
SetCmd(sta1,'ifconfig '+ Netcard_sta1 + ' inet6 del',staticIpv6_sta1 + '/64')

##删除qos配置
EnterWirelessMode(switch1)
SetCmd(switch1,'no ap client-qos')
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no','client-qos enable')
SetCmd(switch1,'vlan ' + Vlan4091)
                                         
#清除 acl 500,501                                          
EnterConfigMode(switch1)
SetCmd(switch1,'no ipv6 access-list 500')
SetCmd(switch1,'no ipv6 access-list 501')

#配置下发
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#end
printTimer(testname, 'End',suggestion = suggestionList)