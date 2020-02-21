#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.14.py - test case 3.1.14 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-2 16:48:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.14 AP通过DNS主动发现AC
# 测试目的：测试AP能通过DNS主动发现AC
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.14'

avoiderror(testname)
printTimer(testname,'Start','Test AP active discovery AC through DNS')

################################################################################
#Step 1
#
#操作
#把AC2的IPv4地址加入到AC1的ip-list中
#在S3上配置vlan70的接口IP，在S3上AP dhcp server中配置dns-server地址和option 43选项
#选项内容包括AC1的域名:ac1_domain,AC2的域名:ac2_domain。
#重启dhcp服务
#
#预期
#在AC1上show wireless peer-switch显示有“IP Address”为“IF_VLAN70_S2_IPV4”的条目
#dhcp状态重启成功,在AP1上用get managed-ap检验,可以看到AP1能通过option43获取了两个交换机域名,如下：
#dhcp-switch-address-1为ac1_domain; dhcp-switch-address-2为ac2_domain
#在AP1上get host检验：dns-1为dns_server_ip
################################################################################

printStep(testname,'Step 1',
          'Config dhcp server on S3',
          'Check the result')

# operate
EnterConfigMode(switch3)
SetCmd(switch3,'interface vlan',Vlan70)
SetCmd(switch3,'ip address',If_vlan70_s3_ipv4)

EnterConfigMode(switch3)
SetCmd(switch3,'interface vlan',Vlan80)
SetCmd(switch3,'ip address',If_vlan80_s3_ipv4)

EnterConfigMode(switch3)
SetCmd(switch3,'ip dhcp pool AP')
SetCmd(switch3,'dns-server',dns_server_ip)
SetCmd(switch3,'network-address',Dhcp_ap_pool_ipv4)
SetCmd(switch3,'default-router',If_vlan70_s3_ipv4_s)
SetCmd(switch3,'option 43 hex 020D61633'+EnvNo+'312E746573742E636F6D020D61633'+EnvNo+'322E746573742E636F6D')

EnterConfigMode(switch3)
SetCmd(switch3,'no service dhcp')	
SetCmd(switch3,'service dhcp')

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',If_vlan70_s2_ipv4_s)

ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_down')
ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_up')
ApSetcmd(ap1,Ap1cmdtype,'saverunning')
	
IdleAfter(30)
EnterEnableMode(switch1)
#check1
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
				   check=[(If_vlan70_s2_ipv4_s)],
				   retry=30,interval=5,waitflag=False,IC=True)

for i in range(5):
	#check2
	res2 = Check_ap_automatic_switchip(ap1,Ap1cmdtype,'dhcp',[ac1_domain,ac2_domain],['1','2'])
	if res2 == 0:
		break
	IdleAfter(30)

#check3
res3 = Check_ap_dnsserver_ip(ap1,Ap1cmdtype,dns_server_ip)
	
#result
printCheckStep(testname, 'Step 1', res1, res2, res3)

################################################################################
#Step 2
#
#操作
# 在AC1上查看AP1的状态
#
#预期
#show wi ap status在AC1上可以检测到AP1被AC1成功管理,AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 2',
          'Check AP1 status on AC1',
          'Check the result')

# operate
IdleAfter(20)
EnterEnableMode(switch1)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
# 在AC1上把s1p1接口down掉
#
#预期
# show wi ap status在AC2上可以检测到AP1被AC2成功管理,AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 3',
          'Shutdown the interface on AC1',
		  'Check the result')		  

# operate		  
EnterConfigMode(switch1)
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'shutdown')

IdleAfter(20)
EnterEnableMode(switch2)
#check
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=40,interval=5,waitflag=False,IC=True)
						
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
# 在AC1上把s1p1接口up
# 在AC2上重启无线功能
#
#预期
# show wi ap status在AC1上可以检测到AP1被AC1成功管理,AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 4',
          'No shutdown the interface on AC1',
          'Check the result')

# operate		  
EnterConfigMode(switch1)
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'no shutdown')

EnterWirelessMode(switch2)
SetCmd(switch2,'no enable')
IdleAfter(1)
SetCmd(switch2,'enable')

RebootAp(AP=ap1,connectTime=30)

#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 5',
          'Recover initial config')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery ip-list')

EnterConfigMode(switch1)
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'no shutdown')

#恢复AP1的配置
RebootAp(setdefaut=True, AP=ap1,connectTime=1)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ip',Ap1_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6',Ap1_ipv6)
ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_down')
ApSetcmd(ap1,Ap1cmdtype,'set_dhcpv6_down')
ApSetcmd(ap1,Ap1cmdtype,'set_ip_route',If_vlan70_s3_ipv4_s)
ApSetcmd(ap1,Ap1cmdtype,'set_ipv6_route',If_vlan70_s3_ipv6_s)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6_prefix_len','64')
ApSetcmd(ap1,Ap1cmdtype,'saverunning')

#恢复S3的配置
EnterConfigMode(switch3)
SetCmd(switch3,'no ip dhcp pool AP')
SetCmd(switch3,'no interface vlan',Vlan70)
SetCmd(switch3,'no interface vlan',Vlan80)

#AC1重启无线
EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

#AC2重启无线
EnterWirelessMode(switch2)
SetCmd(switch2,'no enable')
IdleAfter(1)
SetCmd(switch2,'enable')

#end
printTimer(testname, 'End')