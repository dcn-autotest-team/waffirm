#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_6.2.1.py - test case 6.2.1 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2016 Digital China Networks Co. Ltd
# 
# Date 2016-04-21 14:37:33
#
# Features:
# 6.2.1	AP设置特定IP集中转发测试(二层转发)
# 测试目的：测试客户端二层数据通过IPv4集中式隧道能够被正常转发
# 测试环境：同测试拓扑
# 测试描述：测试客户端二层数据通过IPv4集中式隧道能够被正常转发。测试中覆盖IPv4数据和IPv6数据转发
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package

#Global Definition
staticIpv6_sta1 = '2001:91::100'
staticIpv6_sta2 = '2001:91::200'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 6.2.1'
avoiderror(testname)
printTimer(testname,'Start','test L2 tunnel switch in central switch mode')

suggestionList = []

################################################################################
#Step 1
#操作
# 修改AP1的管理vlan为vlan20。
# 设置AP1的静态ip为172.16.20.38/22，默认网关为172.16.20.1，关闭ap dhcp功能
# ac1上发现ap1
# discovery ip-list 172.16.20.38
# 同时需要在profile下配置管理vlan和un tag vlan为20
# 修改三层交换机连接AP1的端口为trunk口
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

#配置AP1
SetCmd(ap1,'set management vlan-id',Vlan20)
SetCmd(ap1,'set untagged-vlan vlan-id',Vlan20)
SetCmd(ap1,'set management static-ip 172.16.20.38')
SetCmd(ap1,'set management static-mask 255.255.254.0')
SetCmd(ap1,'set static-ip-route gateway 172.16.20.2')
SetCmd(ap1,'set management dhcp-status down')

#配置s3p3为Trunk 口,native vlan
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan20)
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan40)

EnterInterfaceMode(switch3,'vlan '+Vlan20)
SetCmd(switch3,'no ip address')
SetCmd(switch3,'ip address 172.16.20.2 255.255.254.0')

#配置s1p1为Trunk 口,native vlan为40
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport mode trunk')
SetCmd(switch1,'switchport trunk native vlan',Vlan40)

#配置AC1
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list 172.16.20.38')
EnterApProMode(switch1,'1')
SetCmd(switch1,'management vlan',Vlan20)
SetCmd(switch1,'ethernet native-vlan 20')

EnterNetworkMode(switch1,'1')
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan '+Vlan4091)

# WirelessApProfileApply(switch1,'1')
    
# IdleAfter(Ac_ap_syn_time)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

data1 = SetCmd(switch1,'show wireless network','1')

#check
res1 = CheckLine(data1,'Default VLAN',Vlan4091,IC=True)
res2 = CheckLine(data1,'SSID',Network_name1,IC=True)

#result
printCheckStep(testname, 'Step 1',res1,res2)

################################################################################
#Step 2
#操作
#在AC1上面将vlan4091加入到l2-tunnel vlan-list中。
#AC1配置：
#Wireless
#L2tunnel vlan-list 4091
#
#预期
#AC1上面通过show wireless l2tunnel vlan-list可以看到vlan4091。
################################################################################

printStep(testname,'Step 2',
          'add vlan4091 to l2-tunnel vlan-list,',
          'config success')
EnterWirelessMode(switch1)
SetCmd(switch1,'l2tunnel vlan-list 4091')
data = SetCmd(switch1,'show wireless l2tunnel vlan-list')
res = CheckLine(data,Vlan4091,'VLAN4091',IC=True)
printCheckStep(testname,'Step 2',res)

################################################################################
#Step 3
#操作
#将STA1和STA2均关联到AP1的网络test1 (vlan 4091 本身已经在 l2tunnel list之中)
#
#预期
#成功关联并获取192.168.91.X网段的IP地址。
################################################################################

printStep(testname,'Step 3',
          'STA1 and STA2 connect to network 1,',
          'STA1 and STA2 dhcp and get 192.168.91.x ip')

sta1_ipv4 = ''
sta2_ipv4 = ''

res1=res2=res3=res4=1

#operate
#STA1,STA2关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap1mac_lower)
if (res1 == 3) or (res2 == 3):
    suggestionList.append('Suggestions: Step 2,3 failed reason MAYBE RDM17192')
#获取STA1,STA2的地址
data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
data2 = SetCmd(sta2,'ifconfig -v',Netcard_sta2)
SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
SearchResult2 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data2,re.I)

#check
if None != SearchResult1:
    sta1_ipv4 = SearchResult1.group(1)
    if None != re.search(Dhcp_pool1,sta1_ipv4):
        printRes('STA1 ip address: ' + sta1_ipv4)
        res3 = 0  
else:
    res3 = 1
    printRes('Failed: Get ipv4 address of STA1 failed') 
    
if None != SearchResult2:
    sta2_ipv4 = SearchResult2.group(1)
    if None != re.search(Dhcp_pool1,sta2_ipv4):
        printRes('STA2 ip address: ' + sta2_ipv4)
        res4 = 0  
else:
    res4 = 1
    printRes('Failed: Get ipv4 address of STA2 failed')
             

#result
printCheckStep(testname, 'Step 3',res1,res2,res3,res4)

################################################################################
#Step 4
#操作
#用STA1的ipv4地址ping STA2的ipv4地址，用STA1的ipv6地址ping STA2的ipv6地址
#（ipv6地址手动配置为与ac网段的地址）
#
#预期
#能够ping通，在AC1使用命令show arp可看到STA1和STA2的mac对应的port为capwaptnl
#隧道类型，使用show mac-address-table命令看到STA1和STA2的Ports类型为capwaptnl
#隧道类型，ipv6流量使用show ipv6 neighbors查看(不必检查show ipv6 neighbors，RDM33582)
################################################################################

printStep(testname,'Step 4',
          'STA1 ping STA2 in both ipv4 and ipv6',
          'Check if succeed')

res1=res2=res3=res4=-1

#operate

#手动配置STA1，STA2 ipv6 地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'ifconfig '+ Netcard_sta1 + ' inet6 add',staticIpv6_sta1 + '/64')
SetCmd(sta2,'\x03')
SetCmd(sta2,'ifconfig '+ Netcard_sta2 + ' inet6 add',staticIpv6_sta2 + '/64')

#ping,ping6
res1 = CheckPing(sta1,sta2_ipv4,mode='linux')
SetCmd(sta1,'ping6',staticIpv6_sta2,promotePatten = 'PING',promoteTimeout=10)
IdleAfter(10)
data0 = SetCmd(sta1,'\x03',timeout = 1)

#查看表项
IdleAfter(10)
EnterEnableMode(switch1)
data3 = SetCmd(switch1,'show mac-address-table')
data4 = SetCmd(switch1,'show arp')
#data5 = SetCmd(switch1,'show ipv6 neighbors')

#check
res2 = int(str(GetValueBetweenTwoValuesInData(data0,'transmitted,','received')).strip()) 
res2 = 0 if res2 > 0 else 1
res3 = CheckLineList(data3,[(sta1mac,'capwaptnl'),(sta2mac,'capwaptnl')],IC=True)  
# 产品缺陷RDM48795，show arp看不到sta表项
# res4 = CheckLineList(data4,[(sta1_ipv4,sta1mac,'capwaptnl'),(sta2_ipv4,sta2mac,'capwaptnl')],IC=True)
#res5 = CheckLineList(data5,[(staticIpv6_sta1,sta1mac,'capwaptnl'),\
#                            (staticIpv6_sta2,sta2mac,'capwaptnl')],IC=True)

#result
printCheckStep(testname,'Step 4',res1,res2,res3)


################################################################################
#Step 5
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 5',
          'Recover initial config')

#operate

#解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

#删除dhcp binding,arp,mac-address-table,ipv6 neighbors信息
EnterEnableMode(switch1)
SetCmd(switch1,'clear ip dhcp binding all')
SetCmd(switch1,'clear arp traffic')
SetCmd(switch1,'clear mac-address-table dynamic')
SetCmd(switch1,'clear ipv6 neighbors')
# 恢复s1p1配置
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'no switchport mode')
SetCmd(switch1,'switchport access vlan',Vlan40)
#删除手工配置ipv6 地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'ifconfig '+ Netcard_sta1 + ' inet6 del',staticIpv6_sta1 + '/64')
SetCmd(sta2,'\x03')
SetCmd(sta2,'ifconfig '+ Netcard_sta2 + ' inet6 del',staticIpv6_sta2 + '/64')

EnterNetworkMode(switch1,'1')
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan ' + Vlan4091)

#删除手工配置
SetCmd(ap1,'set management static-ip 20.1.1.3')
SetCmd(ap1,'set management static-mask 255.255.255.0')
SetCmd(ap1,'set static-ip-route gateway 20.1.1.2')

EnterInterfaceMode(switch3,'vlan '+Vlan20)
SetCmd(switch3,'no ip address')
SetCmd(switch3,'ip address 20.1.1.2 255.255.255.0')
# 恢复s3p1、s3p3配置
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'no switchport mode')
SetCmd(switch3,'switchport access vlan',Vlan20)
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'no switchport mode')
SetCmd(switch3,'switchport access vlan',Vlan40)

EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery ip-list 172.16.20.38')
SetCmd(switch1,'ap profile 1')
SetCmd(switch1,'no management vlan')
SetCmd(switch1,'no ethernet native-vlan')
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap eth-parameter apply profile 1',timeout=1)
SetCmd(switch1,'y',timeout=1)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

#end
printTimer(testname, 'End',suggestion = suggestionList)
