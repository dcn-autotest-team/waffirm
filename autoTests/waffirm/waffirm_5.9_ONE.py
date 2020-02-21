#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_5.9.py - test case 5.9 of waffirm
#
# Author:  qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 5.9 DHCPv6 Option52
# 测试目的：测试AP能否通过DHCPv6 Option52来获取AC的IPv6地址并进行自动发现。
# 测试环境：同测试拓扑
# 测试描述：AP能够通过DHCPv6报文中的Option52选项来获取AC的IPv6无线管理地址，并根据这些地址自动发现AC。
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 5.9'
avoiderror(testname)
printTimer(testname,'Start','Test manage ap via DHCPv6 Option 52')

################################################################################
#Step 1
#操作
#在AC1上面使能DHCPv6 Server功能并在vlan20的接口上面绑定相应的DHCPv6地址池。地址池中配置Option52相关选项的内容。
#AC1配置：
#Service dhcpv6
#service dhcpv6
#ipv6 dhcp pool ap
#network-address 2001:20::1 64
#excluded-address 2001:20::1
#excluded-address 2001:20::2
#option 52 ipv6 2001:20::1
#exit
#interface Vlan20
#no ipv6 nd suppress-ra
#ipv6 dhcp server ap
#exit
#AC1上面将interface loopback1的ipv4地址删除。
#Interface loopback1
#No ip address
#Exit
#AC1上面关闭所有的自动发现功能。
#AC1配置：
#Wireless
#No discovery method
#Show run查看ipv6地址池配置正确，能够看到Option52的相关配置。
#Show wireless能够看到无线地址变更为2001:20::1。使用show wireless discovery可以看到二层和三层自动发现功能均已经关闭。
#DCWS-6028(config-wireless)#sho wireless discovery 
#IP Polling Mode................................ Disable
#L2 Multicast Discovery Mode.................... Disable
################################################################################
printStep(testname,'Step 1',
          'Config dhcpv6 server on ac1 and disable auto discovery')
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'service dhcpv6')
SetCmd(switch1,'ipv6 dhcp pool ap')
SetCmd(switch1,'network-address 2001:20::1 64')
SetCmd(switch1,'excluded-address ' + If_vlan20_s1_ipv6)
SetCmd(switch1,'excluded-address ' + If_vlan20_s3_ipv6)
SetCmd(switch1,'option 52 ipv6 2001::1')

#switch1 拓扑配置
EnterConfigMode(switch1)
SetCmd(switch1,'vlan',Vlan20)
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport access vlan',Vlan20)
EnterInterfaceMode(switch1,'vlan ' + Vlan20)
SetCmd(switch1,'no','ipv6 nd suppress-ra')
SetCmd(switch1,'ipv6 dhcp server ap')
SetCmd(switch1,'ipv6 nd min-ra-interval 3')
SetCmd(switch1,'ipv6 nd max-ra-interval 4')
SetCmd(switch1,'ipv6 address',If_vlan20_s1_ipv6 + '/64')

#switch3 拓扑配置
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport access vlan',Vlan20)

EnterInterfaceMode(switch1,'loopback1')
SetCmd(switch1,'no ip address')
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery method')

EnterConfigMode(switch3)
SetCmd(switch3,'no service dhcp')
SetCmd(ap1,'set management static-ipv6')

IdleAfter('5')

data1 = SetCmd(switch1,'show wireless discovery')
res1 = CheckLine(data1,'IP Polling Mode','Disable')
res2 = CheckLine(data1,'L2 Multicast Discovery Mode','Disable')

#result
printCheckStep(testname, 'Step 1',res1,res2)

################################################################################
#Step 2
#开启AP1的DHCPv6 Client功能。
#在AP1上面配置：
#Set management dhcpv6-status up
#在AP上面使用get management查看AP能够获取到IPv6地址2001:20::XX。
#通过get managed-ap查看：
#dhcpv6-switch-ipv6-address-1为2001:20::1。
################################################################################
printStep(testname,'Step 2',
          'Config dhcpv6-status up on ap1')
#AP1恢复出厂设置,清除自动部署配置
# data0 = SetCmd(ap1,'factory-reset',timeout=2)
# SetCmd(ap1,'y',timeout=1)
# IdleAfter(Ap_reboot_time)
FactoryResetMultiAp([ap1])
i_times = 0
while i_times < 10:
    data0 = SetCmd(ap1,'\n\n',promoteStop=False,timeout=1)
    if 0 == CheckLine(data0,'login',IC=True):
        SetCmd(ap1,Ap_login_name,promotePatten='Password',promoteTimeout=5)
        SetCmd(ap1,Ap_login_password,timeout=1)  
        break  
    IdleAfter(2)
    i_times += 1

SetCmd(ap1,'set management dhcpv6-status up')
SetCmd(ap1,'save-running')
IdleAfter(60)
data1 = SetCmd(ap1,'get managed-ap')
res1 = CheckLine(data1,'switch-ipv6-address-1\s+'+StaticIpv6_ac1)
if res1 != 0:
    IdleAfter(15)
    data1 = SetCmd(ap1,'get managed-ap')
    res1 = CheckLine(data1,'switch-ipv6-address-1\s+'+StaticIpv6_ac1)
#result
printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#等待AP1自动发现AC1并注册上线。
#预期
#AP1上线后，在AC1上面查看AP1的状态：
#Show wireless ap <ap1-mac> status可以看到AP的发现方式为switch ip configured。
################################################################################
printStep(testname,'Step 3',
          'Check show wi ap status')

IdleAfter(10)
data1 = SetCmd(switch1,'show wireless ap',ap1mac,'status')
res1 = CheckLine(data1,'Discovery Reason','Switch IP DHCP',IC=True)

printCheckStep(testname, 'Step 3',res1)

################################################################################
#Step 4
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 4',
          'Recover initial config for switches.')

#operate  

#switch3 拓扑还原
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport access vlan',Vlan40)

EnterConfigMode(switch3)
SetCmd(switch3,'service dhcp')
EnterConfigMode(switch1)
SetCmd(switch1,'no service dhcpv6')

SetCmd(switch1,'no interface vlan',Vlan20)
SetCmd(switch1,'no','vlan',Vlan20)
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport access vlan',Vlan40)

EnterInterfaceMode(switch1,'loopback1')
SetCmd(switch1,'ip address ' + StaticIpv4_ac1 + ' 255.255.255.255')

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery method')
SetCmd(switch1,'discovery ip-list',Ap1_ipv4)
SetCmd(switch1,'discovery ipv6-list',Ap1_ipv6)

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',Ap2_ipv4)
SetCmd(switch1,'discovery ipv6-list',Ap2_ipv6)
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    EnterWirelessMode(switch1)
    SetCmd(switch1,'l2tunnel vlan-list add',Vlan4091 + '-' + Vlan4093)

SetCmd(ap1,'set management dhcp-status down')
SetCmd(ap1,'set management dhcpv6-status down')
SetCmd(ap1,'set management static-ip',Ap1_ipv4)
SetCmd(ap1,'set management static-ipv6',Ap1_ipv6)
SetCmd(ap1,'set static-ip-route gateway',If_vlan20_s3_ipv4)

SetCmd(ap1,'set managed-ap switch-ipv6-address-1')
SetCmd(ap1,'save-running')

SetCmd(ap1,'\n')
SetCmd(ap1,'set management dhcp-status down')
SetCmd(ap1,'set management dhcpv6-status down')
SetCmd(ap1,'set management static-ip',Ap1_ipv4)
SetCmd(ap1,'set management static-ipv6',Ap1_ipv6)
SetCmd(ap1,'set static-ip-route gateway',If_vlan20_s3_ipv4)
SetCmd(ap1,'set static-ipv6-route gateway',If_vlan20_s3_ipv6)
SetCmd(ap1,'set management static-ipv6-prefix-length','64')
SetCmd(ap1,'save-running')
RebootAp(AP=ap1)

#end
printTimer(testname, 'End')