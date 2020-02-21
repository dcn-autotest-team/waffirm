#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.13.py - test case 4.13 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Date: 2013-09-23 10:41:12
#
# Copyright (c) 2004-2013 Digital China Networks Co. Ltd
#
# Features:
# 4.13	抢占模式1+1备份功能测试（pantw）
# 测试目的：测试无线控制器1+1热备份的基本功能。
# 测试环境：同测试拓扑
# 测试描述：AC1与AC2构成备份组。当AC1出现故障，AC2可以代替AC1管理AP。
#         当AP1故障恢复后能够重新管理AP，而AC2恢复为备份设备。要求AC
#         之间发生切换时，数据基本上没有丢失
#
#*******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
#     - zhangjxp 2017.11.10 RDM50304 修改step2
#     - zhangjxp 2017.12.13 修改step8，RDM50597
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.13'
avoiderror(testname)
printTimer(testname,'Start','1+1 backup，preempt mode')

################################################################################
#Step 1
#操作
# 1+1初始环境配置，AC1和L3和AC2都是trunk相连，sta的网关在L3上，dhcp配置在L3上：
# s1上配置：
# con
# vlan 4081
# interface vlan 4081
# ip address 192.168.81.1 255.255.255.0
# interface s1p1
# switchport mode trunk 
# exit
# wireless 
# l2tunnel vlan-list add 4081
# network 1
# vlan 4081
#
# s2上配置：
# con
# vlan 4081
# interface vlan 4081
# ip address 192.168.81.100 255.255.255.0
# interface s2p1
# switchport mode trunk 
# exit
# wireless 
# l2tunnel vlan-list add 4081
# network 1
# vlan 4081
#
# s3上配置：
# con
# vlan 4081
# interface vlan 4081
# ip address 192.168.81.254 255.255.255.0
# interface s3p2
# switchport mode trunk 
# interface s3p1
# switchport mode trunk 
# exit
# service dhcp
# ip dhcp excluded-address 192.168.81.1
# ip dhcp excluded-address 192.168.81.100
# ip dhcp excluded-address 192.168.81.254
# ip dhcp pool vlan4081
#  network-address 192.168.81.0 255.255.255.0
#  default-router 192.168.81.254
#
#预期
#配置成功
################################################################################
printStep(testname,'Step 1',
          'set s1p1,s3p1,s3p2 and s2p1 as trunk port,',
          'set gateway of sta1 on L3, and set dhcp server on L3,',
          'config success.')

#operate
#配置s1
EnterConfigMode(switch1)
SetCmd(switch1,'vlan 4081')
EnterInterfaceMode(switch1,'vlan 4081')
IdleAfter(Vlan_Idle_time)
SetCmd(switch1,'ip address 192.168.81.1 255.255.255.0')
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport mode trunk')
EnterNetworkMode(switch1,1)
SetCmd(switch1,'vlan 4081')
EnterConfigMode(switch1)
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    EnterWirelessMode(switch1)
    SetCmd(switch1,'l2tunnel vlan-list add 4081')
#配置s2
EnterConfigMode(switch2)
SetCmd(switch2,'vlan 4081')
EnterInterfaceMode(switch2,'vlan 4081')
IdleAfter(Vlan_Idle_time)
SetCmd(switch2,'ip address 192.168.81.100 255.255.255.0')
EnterInterfaceMode(switch2,s2p1)
SetCmd(switch2,'switchport mode trunk')
EnterNetworkMode(switch2,1)
SetCmd(switch2,'vlan 4081')
EnterConfigMode(switch2)
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    EnterWirelessMode(switch2)
    SetCmd(switch2,'l2tunnel vlan-list add 4081')
    EnterConfigMode(switch3)
    SetCmd(switch3,'service dhcp')
#配置s3
EnterConfigMode(switch3)
# SetCmd(switch3,'service dhcp')
SetCmd(switch3,'vlan 4081')
EnterInterfaceMode(switch3,'vlan 4081')
IdleAfter(Vlan_Idle_time)
SetCmd(switch3,'ip address 192.168.81.254 255.255.255.0')
EnterInterfaceMode(switch3,s3p2)
SetCmd(switch3,'switchport mode trunk')
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport mode trunk')
EnterConfigMode(switch3)
SetCmd(switch3,'ip dhcp excluded-address 192.168.81.1')
SetCmd(switch3,'ip dhcp excluded-address 192.168.81.100')
SetCmd(switch3,'ip dhcp excluded-address 192.168.81.254')
SetCmd(switch3,'ip dhcp pool vlan4081')
SetCmd(switch3,'network-address 192.168.81.0 255.255.255.0')
SetCmd(switch3,'default-router 192.168.81.254')
EnterConfigMode(switch3)

#check
data1 = ShowRun(switch1)
data2 = ShowRun(switch2)
res1 = CheckLineList(data1,[('interface Vlan4081'),
                            ('ip address 192.168.81.1 255.255.255.0')],
                     IC=True)
res3 = CheckLineList(data2,[('interface Vlan4081'),
                            ('ip address 192.168.81.100 255.255.255.0')],
                     IC=True)
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    res2 = CheckLine(data1,'l2tunnel vlan-list add','4081',IC=True)
    res4 = CheckLine(data2,'l2tunnel vlan-list add','4081',IC=True)
else:
    res2 = 0
    res4 = 0
    
data3 = ShowRun(switch3)
res5 = CheckLineList(data3,[('interface Vlan4081'),
                            ('ip address 192.168.81.254 255.255.255.0'),
                            ('ip dhcp pool vlan4081'),
                            ('network-address 192.168.81.0 255.255.255.0'),
                            ('default-router 192.168.81.254'),
                            ('ip dhcp excluded-address 192.168.81.1'),
                            ('ip dhcp excluded-address 192.168.81.100'),
                            ('ip dhcp excluded-address 192.168.81.254')],IC=True)
             
#result
printCheckStep(testname,'Step 1',res1,res2,res3,res4,res5)

################################################################################
#Step 2
#操作
#分别在AC1和AC2配置冗备功能。AC1为master，AC2为backup(缺省即为抢占模式)：
#switch-redundancy master 1.1.1.1 backup 2.2.2.2
#在AC1上单独配置发现列表发现AC2，建立集群：
#discovery ip-list 2.2.2.2
#AC1上面重起ap：
#wireless ap reset
#预期
#Ap重起后被ac1管理上（需要判断）：
#Ac1上show wireless l2tunnel tunnel-list显示其隧道状态为“Active”（为了兼容四期，只作show不作判断）
#Ac2上show wireless l2tunnel tunnel-list显示其隧道状态为”Standby” （为了兼容四期，只作show不作判断）
################################################################################
printStep(testname,'Step 2',
          'switch-redundancy master 1.1.1.1 backup 1.1.1.2,',
          'show wireless l2tunnel tunnel-list')
          
res1=1
#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'switch-redundancy master ' + StaticIpv4_ac1 + ' backup ' + StaticIpv4_ac2)
SetCmd(switch1,'discovery ip-list ' + StaticIpv4_ac2)
EnterWirelessMode(switch2)
SetCmd(switch2,'switch-redundancy master ' + StaticIpv4_ac1 + ' backup ' + StaticIpv4_ac2)
EnterEnableMode(switch1)
# RebootMulitAp('AC',AC=switch1,MAC=[ap1mac,ap2mac],AP=[ap1,ap2])
# SetCmd(ap1,'set managed-ap mode down')
# SetCmd(ap2,'set managed-ap mode down')
# IdleAfter(8)
# SetCmd(ap1,'set managed-ap mode up')
# SetCmd(ap2,'set managed-ap mode up')
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap1,ap1mac,switch1)
ChangeAPMode(ap2,ap2mac,switch1)
IdleAfter(20)
#check
i_times = 0
while i_times < 20: 
    data1 = SetCmd(switch1,'show wireless ap status')
    if 0 ==  CheckLine(data1,ap1mac,'Managed','Success',IC=True) and 0 ==  CheckLine(data1,ap2mac,'Managed','Success',IC=True):
        res1 = 0
        break
    i_times += 1
    IdleAfter(5)
    
SetCmd(switch1,'show wireless l2tunnel tunnel-list')
SetCmd(switch2,'show wireless l2tunnel tunnel-list')
#result
printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#sta1关联到网络test1 ，ping s3(不同于sta1网段的IP)
#
#预期
#Sta1获取ip,可以ping通s3(不同于sta1网段的IP)

################################################################################
printStep(testname,'Step 3',
          'STA1 connect to network 1',
          'STA1 ping pc1',
          'STA1 dhcp and get ip address,'
          'sta1 ping pc1 success')

res1=res2=res3=1
#operate
sta1_ipv4 = ''

#STA1关联 network 1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
IdleAfter(10)

#STA1获取地址
sta1_ipresult = GetStaIp(sta1,checkippool='192.168.81.')
sta1_ipv4 = sta1_ipresult['ip']
res2 = sta1_ipresult['res']

#STA11 ping pc1
if res2 == 0:
    #res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res3 = CheckPing(sta1,If_vlan192_s3_ipv4,mode='linux')
             
#result
printCheckStep(testname,'Step 3',res1,res2,res3)

################################################################################
#Step 4
#操作
#断开AC1和S3的网络连接，
#
#预期
#AC1和AC2之间发生主备切换。AC2成为master。通过show wireless switch redundancy status查看冗备状态正确。
#STA 1 ping s3(不同于sta1网段的IP),可以ping通
################################################################################
printStep(testname,'Step 4',
          'Disconnect connection between ac1 and s3')
res1=res2=1          
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'shutdown')
#check
IdleAfter(30)
for i in range(14):
	data1 = SetCmd(switch2,'show wireless switch redundancy status',timeout=3)
	res2 = CheckLineList(data1,[(StaticIpv4_ac2 + '\(Active\)')],IC=True)
	if res2 == 0:
		break
	else:
		IdleAfter(5)

for i in range(14):		
	res1 = CheckPing(sta1,If_vlan192_s3_ipv4,mode='linux')
	if res1 == 0:
		break
	else:
		IdleAfter(5)
#result
printCheckStep(testname, 'Step 4',res1,res2)
################################################################################
#Step 5
#操作
#在S2上面查看AP和Client相关的信息。
#
#预期
#AP1和AP2关联在AC2。STA1和STA2不会掉线，仍然与原来的AP关联。
#Ac2上show wireless l2tunnel tunnel-list显示其隧道状态为“Active” （为了兼容四期，只作show不作判断）
################################################################################
printStep(testname,'Step 5',
          'Check ap and client info on s2')
          

#check
SetCmd(switch1,'show wireless l2tunnel tunnel-list')
SetCmd(switch2,'show wireless l2tunnel tunnel-list')
IdleAfter(2)
data1 = SetCmd(switch2,'show wireless ap status',timeout=5)
res1 = CheckLineList(data1,[(re.sub(':','-',ap1mac),'Success')],IC=True)
res3 = CheckLineList(data1,[(re.sub(':','-',ap2mac),'Success')],IC=True)

data1 = SetCmd(switch2,'show wireless client status',timeout=5)
res2 = CheckLineList(data1,[(re.sub(':','-',sta1mac))],IC=True)

#result
printCheckStep(testname, 'Step 5',res1,res2,res3)
################################################################################
#Step 6
#操作
#AC1恢复和S3的网络连接，等待5分钟。
#
#预期
#AC1和AC2重新发生主备切换。AC1仍然为master。通过show wireless switch redundancy status查看冗备配置正确。
#sta1 ping ac1上网关通
################################################################################
printStep(testname,'Step 6',
          'Reconnect ac1 and s3')
res1=res2=1         
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'no shutdown',promotePatten='administratively',promoteTimeout=380)
IdleAfter(30)
for i in range(14):
	data1 = SetCmd(switch1,'show wireless switch redundancy status',timeout=3)
	res2 = CheckLineList(data1,[(StaticIpv4_ac1 + '\(Active\)')],IC=True)
	if res2 == 0:
		break
	else:
		IdleAfter(5)

for i in range(14):		
	res1 = CheckPing(sta1,'192.168.81.1',mode='linux')
	if res1 == 0:
		break
	else:
		IdleAfter(5)
#check

#result
printCheckStep(testname, 'Step 6',res1,res2)
################################################################################
#Step 7
#操作
#在AC1上面查看AP和Client相关的信息。
#
#预期
#AP1和AP2关联在AC1。STA1和STA2不会掉线，仍然与原来的AP关联。
################################################################################
printStep(testname,'Step 7',
          'Check client info on ac1')
          
data1 = SetCmd(switch1,'show wireless ap status')
res1 = CheckLineList(data1,[(re.sub(':','-',ap1mac),'Success')],IC=True)
data1 = SetCmd(switch1,'show wireless ap status')
res3 = CheckLineList(data1,[(re.sub(':','-',ap2mac),'Success')],IC=True)

data1 = SetCmd(switch1,'show wireless client status')
res2 = CheckLineList(data1,[(re.sub(':','-',sta1mac))],IC=True)

#result
printCheckStep(testname, 'Step 7',res1,res2,res3)
################################################################################
#Step 8
#操作
#1、在2个ap上执行factory-reset
#2、恢复初始配置。
################################################################################
printStep(testname,'Step 8',
          'Recover initial config for switches.')

#operate
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    EnterWirelessMode(switch1)
    SetCmd(switch1,'l2tunnel vlan-list remove 4081')
    EnterWirelessMode(switch2)
    SetCmd(switch2,'l2tunnel vlan-list remove 4081')
    EnterConfigMode(switch3)
    SetCmd(switch3,'no service dhcp')
#恢复配置s1
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan 4081')
SetCmd(switch1,'no vlan 4081')
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport mode access')
SetCmd(switch1,'switchport access vlan 40')
EnterNetworkMode(switch1,1)
SetCmd(switch1,'vlan '+Vlan4091)
EnterConfigMode(switch1)

#恢复配置s2
EnterConfigMode(switch2)
SetCmd(switch2,'no interface vlan 4081')
SetCmd(switch2,'no vlan 4081')
EnterInterfaceMode(switch2,s2p1)
SetCmd(switch2,'switchport mode access')
SetCmd(switch2,'switchport access vlan 30')
EnterNetworkMode(switch2,1)
SetCmd(switch2,'vlan '+Vlan4091)
#RDM37511
EnterWirelessMode(switch2)
SetCmd(switch2,'peer-group 2')
IdleAfter(5)
SetCmd(switch2,'peer-group 1')
EnterConfigMode(switch2)

#恢复配置s3
EnterConfigMode(switch3)
SetCmd(switch3,'no interface vlan 4081')
SetCmd(switch3,'no vlan 4081')
EnterInterfaceMode(switch3,s3p2)
SetCmd(switch3,'switchport mode access')
SetCmd(switch3,'switchport access vlan 30')
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport mode access')
SetCmd(switch3,'switchport access vlan 40')
EnterConfigMode(switch3)
SetCmd(switch3,'no ip dhcp excluded-address 192.168.81.1')
SetCmd(switch3,'no ip dhcp excluded-address 192.168.81.100')
SetCmd(switch3,'no ip dhcp excluded-address 192.168.81.254')
SetCmd(switch3,'no ip dhcp pool vlan4081')
EnterConfigMode(switch3)

##解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)


EnterWirelessMode(switch1)
SetCmd(switch1,'no switch-redundancy ')
EnterWirelessMode(switch2)
SetCmd(switch2,'no switch-redundancy ')

SetCmd(switch1,'no discovery ip-list ' + StaticIpv4_ac2)
#SetCmd(switch2,'no discovery ip-list ' + StaticIpv4_ac1)

#在2个ap上执行factory-reset

FactoryResetMultiAp([ap1,ap2])
ApLogin(ap1,retry=10)
ApLogin(ap2,retry=10)

#---------------------------  初始化AP1  ---------------------------------------
SetCmd(ap1,'\n')
SetCmd(ap1,'set management static-ip',Ap1_ipv4)
SetCmd(ap1,'set management static-ipv6',Ap1_ipv6)
SetCmd(ap1,'set management dhcp-status down')
SetCmd(ap1,'set management dhcpv6-status down')
SetCmd(ap1,'set static-ip-route gateway',If_vlan20_s3_ipv4)
SetCmd(ap1,'set static-ipv6-route gateway',If_vlan20_s3_ipv6)
SetCmd(ap1,'set management static-ipv6-prefix-length','64')
SetCmd(ap1,'save-running')

#---------------------------  初始化AP2  ---------------------------------------
SetCmd(ap2,'\n')
SetCmd(ap2,'set management static-ip',Ap2_ipv4)
SetCmd(ap2,'set management static-ipv6',Ap2_ipv6)
SetCmd(ap2,'set management dhcp-status down')
SetCmd(ap2,'set management dhcpv6-status down')
SetCmd(ap2,'set static-ip-route gateway',If_vlan30_s3_ipv4)
SetCmd(ap2,'set static-ipv6-route gateway',If_vlan30_s3_ipv6)
SetCmd(ap2,'set management static-ipv6-prefix-length','64')
SetCmd(ap2,'save-running')
EnterWirelessMode(switch2)
SetCmd(switch2,'peer-group 2')
IdleAfter(3)
SetCmd(switch2,'peer-group 1')
#下发配置
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
 
#end
printTimer(testname, 'End')
