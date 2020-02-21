#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.2.7.py - test case 3.2.7 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-18 15:17:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.2.7 AP通过静态配置主动发现AC(IPV6)
# 测试目的：测试AP能通过静态配置主动发现AC(IPV6)
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.2.7'

avoiderror(testname)
printTimer(testname,'Start','Test AP active discovery AC through static config')

################################################################################
#Step 1
#
#操作
# 在AP1上配置4个AC的IP地址
#预期
# 配置成功，在AP1上通过get managed-ap查看：
#switch-ipv6-address-1为2001:1::100;switch-ipv6-address-2为2001:2::100
#switch-ipv6-address-3为2001:3::100;switch-ipv6-address-4为2001:4::100
################################################################################
printStep(testname,'Step 1',
          'Config four managed-ap switch-address on AP1',
          'Check the result')

# operate# operate
exec(compile(open('clustermanagement\\clustermanagement_initial(ipv6).py', "rb").read(), 'clustermanagement\\clustermanagement_initial(ipv6).py', 'exec'))

ApSetcmd(ap1,Ap1cmdtype,'set_switch_address_ipv6','2001:1::100',addressnum='1')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address_ipv6','2001:2::100',addressnum='2')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address_ipv6','2001:3::100',addressnum='3')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address_ipv6','2001:4::100',addressnum='4')	
	
#check
res1 = Check_ap_static_switchip(ap1,Ap1cmdtype,
                                ['2001:1::100','2001:2::100','2001:3::100','2001:4::100'],
                                ['1','2','3','4'],ipversion='ipv6')
	
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
# 在AP1上配置2个AC的IP地址，2个不可达的IP地址
#
#预期
# 配置成功，在AP1上通过get managed-ap查看：
#switch-ipv6-address-1为If_vlan70_S1_ipv6;switch-ipv6-address-2为2001:2::100
#switch-ipv6-address-3为If_vlan70_S2_ipv6;switch-ipv6-address-4为2001:4::100
################################################################################
printStep(testname,'Step 2',
          'Config managed-ap switch-address with AC1 and AC2 ip',
		  'Check the result')		  

# operate
# operate
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address_ipv6',If_vlan70_s1_ipv6_s,addressnum='1')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address_ipv6','2001:2::100',addressnum='2')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address_ipv6',If_vlan70_s2_ipv6_s,addressnum='3')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address_ipv6','2001:4::100',addressnum='4')
ApSetcmd(ap1,Ap1cmdtype,'saverunning')

#check
res1 = Check_ap_static_switchip(ap1,Ap1cmdtype,
                                [If_vlan70_s1_ipv6_s,'2001:2::100',If_vlan70_s2_ipv6_s,'2001:4::100'],
                                ['1','2','3','4'],ipversion='ipv6')
						
#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
# 把AC2的IPv6地址加入到AC1的ip-list中
#
#预期
#在AC1上show wi ap status可以检测到AP1被AC1成功管理
#AP1_MAC的“Status”为“Managed Success”
#在AC1上show wireless peer-switch显示有“IP Address”为“If_vlan70_S2_ipv6（”的条目
################################################################################

printStep(testname,'Step 3',
          'Add AC2 ip address to discovery ip list',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ipv6-list',If_vlan70_s2_ipv6_s)
IdleAfter(20)

#check
EnterEnableMode(switch1)
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
				   check=[(If_vlan70_s2_ipv6_s)],
				   retry=30,interval=5,waitflag=False,IC=True)
res2 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname,'Step 3', res1, res2)

###############################################################################
#Step 4
#
#操作
#在AP1上配置switch-ipv6-address-1为IF_VLAN70_S2_IPV4,switch-ipv6-address-3为IF_VLAN70_S1_IPV4
#
#预期
#show wi ap status在AC2上可以检测到AP1被AC2成功管理
#AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 4',
          'Config managed-ap switch-address 1 with AC2 ip on AP1',
          'Check the result')

# operate# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list')
SetCmd(switch1,'no discovery method l2-multicast')

EnterWirelessMode(switch2)
SetCmd(switch2,'no discovery vlan-list')
SetCmd(switch2,'no discovery method l2-multicast')

ApSetcmd(ap1,Ap1cmdtype,'set_switch_address_ipv6',If_vlan70_s2_ipv6_s,addressnum='1')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address_ipv6',If_vlan70_s1_ipv6_s,addressnum='3')
ApSetcmd(ap1,Ap1cmdtype,'saverunning')

EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

RebootAp(AP=ap1,connectTime=1)

IdleAfter(20)
# check
EnterEnableMode(switch2)
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#在AC2上把s2p1接口down掉
#
#预期
#show wi ap status在AC1上可以检测到AP1被AC1成功管理
#AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 5',
          'Shutdown the interface on AC2',
          'Check the result')

# operate		  
EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'shutdown')

IdleAfter(20)
#check
EnterEnableMode(switch1)
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname, 'Step 5', res1)

################################################################################
#Step 6
#
#操作
#在AC2上把s2p1接口up
#在AC1上重启无线功能
#
#预期
#show wi ap status在AC2上可以检测到AP1被AC2成功管理
#AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 6',
          'Shutdown the interface on AC1',
          'Check the result')

# operate		  
EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'no shutdown')
		
EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')		
	
RebootAp(AP=ap1,connectTime=1)
	
IdleAfter(20)
#check
EnterEnableMode(switch2)
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname, 'Step 6', res1)

################################################################################
#Step 7
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 7',
          'Recover initial config')

# operate
#恢复AP1的配置
RebootAp(setdefaut=True, AP=ap1,connectTime=1)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ip',Ap1_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6',Ap1_ipv6)
ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_down')
ApSetcmd(ap1,Ap1cmdtype,'set_dhcpv6_down')
ApSetcmd(ap1,Ap1cmdtype,'set_ip_route',If_vlan70_s3_ipv4_s)
ApSetcmd(ap1,Ap1cmdtype,'set_ipv6_route',If_vlan70_s3_ipv6_s)
ApSetcmd(ap1,Ap1cmdtype,'saverunning')

#重启AC1无线
EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
SetCmd(switch1,'enable')

#重启AC2无线
EnterWirelessMode(switch2)
SetCmd(switch2,'no enable')
IdleAfter(1)
SetCmd(switch2,'enable')

#配置AC1的vlan list
SetCmd(switch1,'no discovery ipv6-list')
SetCmd(switch1,'discovery vlan-list 1')
SetCmd(switch1,'discovery method l2-multicast')

#配置AC2的vlan list
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery vlan-list 1')
SetCmd(switch2,'discovery method l2-multicast')

exec(compile(open('clustermanagement\\clustermanagement_unitial(ipv6).py', "rb").read(), 'clustermanagement\\clustermanagement_unitial(ipv6).py', 'exec'))	  
#end
printTimer(testname, 'End')