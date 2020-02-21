#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_6.2.2.py - test case 6.2.2 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
# 
# Date 2012-12-7 14:37:33
#
# Features:
# 6.2.2 AP设置特定IP集中转发测试(三层转发)
# 测试目的：测试客户端三层数据通过IPv4集中式隧道能够被正常转发
# 测试环境：同测试拓扑
# 测试描述：测试客户端三层数据通过IPv4集中式隧道能够被正常转发。测试中覆盖IPv4数据和IPv6数据
#
#*******************************************************************************
# Change log:
#     -
#*******************************************************************************

#Package

#Global Definition
staticIpv6_sta1 = '2001:91::100'
staticIpv6_sta2 = '2001:92::200'

#三层隧道转发 ipv6路由配置
CMD_Add_ipv6_route_test1_to_test2_sta1 = 'route -A inet6 add '+ staticIpv6_sta2 + '/64 gw '+ If_vlan4091_s1_ipv6 +' dev '+ Netcard_sta1
CMD_Add_ipv6_route_test2_to_test1_sta2 = 'route -A inet6 add '+ staticIpv6_sta1 + '/64 gw '+ If_vlan4092_s1_ipv6 +' dev '+ Netcard_sta2
CMD_Del_ipv6_route_test1_to_test2_sta1 = 'route -A inet6 del '+ staticIpv6_sta2 + '/64 gw '+ If_vlan4091_s1_ipv6 +' dev '+ Netcard_sta1
CMD_Del_ipv6_route_test2_to_test1_sta2 = 'route -A inet6 del '+ staticIpv6_sta1 + '/64 gw '+ If_vlan4092_s1_ipv6 +' dev '+ Netcard_sta2

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 6.2.2'
avoiderror(testname)
printTimer(testname,'Start','test L3 tunnel switch in central switch mode')

################################################################################
#Step 1 step2
#操作
#在AC1配置network1的SSID为test1，关联vlan4091，配置下发到AP1，
#配置network2的SSID为test2，关联vlan4092，配置下发到AP2
#在AC1上面将vlan4091和vlan4092加入到l2-tunnel vlan-list中
#
#(以上均包含在初始配置之中)
#
#
#预期
#通过show wireless l2-tunnel vlan-list可以看到vlan4091和vlan4092
################################################################################
printStep(testname,'Step 1,Step 2',
          'Show wireless l2tunnel vlan-list',
          'Check if contain vlan 4091,4092')

res1=1
#operate

#配置AP1
SetCmd(ap1,'set management vlan-id',Vlan20)
SetCmd(ap1,'set untagged-vlan vlan-id',Vlan20)
SetCmd(ap1,'set management static-ip 172.16.20.38')
SetCmd(ap1,'set management static-mask 255.255.254.0')
SetCmd(ap1,'set static-ip-route gateway 172.16.20.2')
SetCmd(ap1,'set management dhcp-status down')

#配置AP2
SetCmd(ap2,'set management vlan-id',Vlan30)
SetCmd(ap2,'set untagged-vlan vlan-id',Vlan30)
SetCmd(ap2,'set management static-ip 172.16.30.38')
SetCmd(ap2,'set management static-mask 255.255.254.0')
SetCmd(ap2,'set static-ip-route gateway 172.16.30.2')
SetCmd(ap2,'set management dhcp-status down')

#配置AC1
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list 172.16.20.38')
SetCmd(switch1,'discovery ip-list 172.16.30.38')
SetCmd(switch1,'network 1024')
SetCmd(switch1,'ssid 1024')
EnterApProMode(switch1,'1')
SetCmd(switch1,'management vlan',Vlan20)
SetCmd(switch1,'ethernet native-vlan 20')
EnterApProMode(switch1,'2')
SetCmd(switch1,'management vlan',Vlan30)
SetCmd(switch1,'ethernet native-vlan 30')

#配置L3
EnterInterfaceMode(switch3,'vlan '+Vlan20)
SetCmd(switch3,'no ip address')
SetCmd(switch3,'ip address 172.16.20.2 255.255.254.0')

EnterInterfaceMode(switch3,'vlan '+Vlan30)
SetCmd(switch3,'no ip address')
SetCmd(switch3,'ip address 172.16.30.2 255.255.254.0')

EnterConfigMode(switch3)
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan 20')
EnterInterfaceMode(switch3,s3p4)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan 30')
IdleAfter(30)

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless l2tunnel vlan-list')


#check
res1 = CheckLineList(data1,[(Vlan4091),(Vlan4092)],IC=True)

#result
printCheckStep(testname, 'Step 1 Step 2',res1)

################################################################################
#Step 3
#操作
#将STA1,STA2 分别关联到AP1的网络test1，AP2的 test2
#
#预期
#关联成功
#客户端STA1能够获取192.168.91.X网段的IP地址，STA2能够获取192.168.92.X网段的IP地址。
################################################################################

printStep(testname,'Step 3',
          'STA1 connect to test1, get 192.168.91.x ip via dhcp',
          'STA2 connect to test1, get 192.168.92.x ip via dhcp')

sta1_ipv4 = ''
sta2_ipv4 = ''

res1=res2=res3=res4=1

#operate
#STA1,STA2关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,bssid=ap2mac_type1_network2)


#获取STA1,STA2的地址
sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
res3 = sta1_ipresult['res']

sta2_ipresult = GetStaIp(sta2,checkippool=Dhcp_pool2)
sta2_ipv4 = sta2_ipresult['ip']
res4 = sta2_ipresult['res']
  
#result
printCheckStep(testname, 'Step 3',res1,res2,res3,res4)

################################################################################
#Step 4
#操作
#用STA1的ipv4地址ping STA2的ipv4地址，
#用STA1的ipv6地址ping STA2的ipv6地址（ipv6地址手动配置为与ac网段的地址）。
#
#预期
#能够ping通，在AC1使用命令show arp可看到STA1和STA2的mac对应的port为
#capwaptnl隧道类型，使用show mac-address-table命令看到STA1和STA2的Ports类型为
#capwaptnl隧道类型，ipv6流量使用show ipv6 neighbors查看；
################################################################################

printStep(testname,'Step 4',
          'STA1 ping STA2 in both ipv4 and ipv6',
          'Check if succeed')

res1=res2=res3=res4=res5=-1

#operate

#手动配置STA1，STA2 ipv6 地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'ifconfig '+ Netcard_sta1 + ' inet6 add',staticIpv6_sta1 + '/64')
SetCmd(sta2,'\x03')
SetCmd(sta2,'ifconfig '+ Netcard_sta2 + ' inet6 add',staticIpv6_sta2 + '/64')
IdleAfter(30)
#配置test1 至 test2 ipv6 路由
SetCmd(sta1,CMD_Add_ipv6_route_test1_to_test2_sta1)
#配置test2 至 test1 ipv6 路由
SetCmd(sta2,CMD_Add_ipv6_route_test2_to_test1_sta2)

#ping,ping6
res1 = CheckPing(sta1,sta2_ipv4,mode='linux')
SetCmd(sta1,'ping6',staticIpv6_sta2,promotePatten = 'PING',promoteTimeout = 10)
IdleAfter(10)
data0 = SetCmd(sta1,'\x03',timeout = 1)

#查看表项
IdleAfter(10)
EnterEnableMode(switch1)
data3 = SetCmd(switch1,'show mac-address-table')
data4 = SetCmd(switch1,'show ipv6 neighbors')
data5 = SetCmd(switch1,'show arp')
SetCmd(sta1,'arp -a')
SetCmd(sta2,'arp -a')
#check

res2 = int(str(GetValueBetweenTwoValuesInData(data0,'transmitted,','received')).strip()) 
res2 = 0 if res2 > 0 else 1
res3 = CheckLineList(data3,[(sta1mac,'capwaptnl'),(sta2mac,'capwaptnl')],IC=True)  
res4 = CheckLineList(data4,[(staticIpv6_sta1,sta1mac,'capwaptnl'),
                            (staticIpv6_sta2,sta2mac,'capwaptnl')],IC=True)               
res5 = CheckLineList(data5,[(sta1_ipv4,sta1mac,'capwaptnl'),(sta2_ipv4,sta2mac,'capwaptnl')],IC=True)

#result
printCheckStep(testname,'Step 4',res1,res2,res3,res4,res5)


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

#删除手工配置
SetCmd(ap1,'set management static-ip 20.1.1.3')
SetCmd(ap1,'set management static-mask 255.255.255.0')
SetCmd(ap1,'set static-ip-route gateway 20.1.1.2')

SetCmd(ap2,'set management static-ip 30.1.1.3')
SetCmd(ap2,'set management static-mask 255.255.255.0')
SetCmd(ap2,'set static-ip-route gateway 30.1.1.1')

EnterInterfaceMode(switch3,'vlan '+Vlan20)
SetCmd(switch3,'no ip address')
SetCmd(switch3,'ip address 20.1.1.2 255.255.255.0')

EnterInterfaceMode(switch3,'vlan '+Vlan30)
SetCmd(switch3,'no ip address')
SetCmd(switch3,'ip address 30.1.1.1 255.255.255.0')

EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'switchport mode access ')
SetCmd(switch3,'switchport access vlan ',Vlan20)

EnterInterfaceMode(switch3,s3p4)
SetCmd(switch3,'switchport mode access ')
SetCmd(switch3,'switchport access vlan ',Vlan30)

EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery ip-list 172.16.20.38')
SetCmd(switch1,'no discovery ip-list 172.16.30.38')
SetCmd(switch1,'no network 1024')
EnterApProMode(switch1,'1')
SetCmd(switch1,'no management vlan')
SetCmd(switch1,'no ethernet native-vlan')

EnterApProMode(switch1,'2')
SetCmd(switch1,'no management vlan')
SetCmd(switch1,'no ethernet native-vlan')

# EnterEnableMode(switch1)
# SetCmd(switch1,'wireless ap eth-parameter apply profile 1',timeout=1)
# SetCmd(switch1,'y',timeout=1)
# SetCmd(switch1,'wireless ap eth-parameter apply profile 2',timeout=1)
# SetCmd(switch1,'y',timeout=1)
WirelessApplyProfileWithCheck(switch1,['1','2'],[ap1mac,ap2mac],eth_parameter=True)

#删除手工配置ipv6 地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'ifconfig '+ Netcard_sta1 + ' inet6 del',staticIpv6_sta1 + '/64')
SetCmd(sta2,'\x03')
SetCmd(sta2,'ifconfig '+ Netcard_sta2 + ' inet6 del',staticIpv6_sta2 + '/64')

#删除test1 至 test2 ipv6 路由
SetCmd(sta1,CMD_Del_ipv6_route_test1_to_test2_sta1)
#删除test2 至 test1 ipv6 路由
SetCmd(sta2,CMD_Del_ipv6_route_test2_to_test1_sta2)


#end
printTimer(testname, 'End')