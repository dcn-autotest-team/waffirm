#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.15.py - test case 3.1.15 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-2 17:10:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.15 AP主动发现AC方式优先级测试
# 测试目的：测试AP主动发现AC方式优先级
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.15'

avoiderror(testname)
printTimer(testname,'Start','Test AP active discovery AC priority')

################################################################################
#Step 1
#
#操作
#把AC2的IPv4地址加入到AC1的ip-list中
#在S3上配置vlan70的接口IP，在S3上AP dhcp server中配置option 43选项
#重启dhcp 服务
#
#预期
#在AC1上show wireless peer-switch显示有“IP Address”为“IF_VLAN70_S2_IPV4”的条目
#dhcp状态重启成功,在AP1上用get managed-ap检验,可以看到AP1能通过option43获取了两个交换机地址,如下：
#dhcp-switch-address-1为IF_VLAN70_S1_IPV4; dhcp-switch-address-2为IF_VLAN70_S2_IPV4
################################################################################

printStep(testname,'Step 1',
          'Config dhcp server on S3',
          'Check the result')

# operate
EnterConfigMode(switch3)
SetCmd(switch3,'interface vlan',Vlan70)
SetCmd(switch3,'ip address',If_vlan70_s3_ipv4)
EnterConfigMode(switch3)
SetCmd(switch3,'ip dhcp pool AP')
SetCmd(switch3,'network-address',Dhcp_ap_pool_ipv4)
SetCmd(switch3,'default-router',If_vlan70_s3_ipv4_s)
if EnvNo == '1':
	SetCmd(switch3,'option 43 hex 010446010B64010446010B65010401010101010402020202')
elif EnvNo == '2':
	SetCmd(switch3,'option 43 hex 010446011564010446011565010401010101010402020202')
elif EnvNo == '3':
	SetCmd(switch3,'option 43 hex 010446011f64010446011f65010401010101010402020202')

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
	Check_ap_automatic_switchip(ap1,Ap1cmdtype,'dhcp',[If_vlan70_s1_ipv4_s,If_vlan70_s2_ipv4_s],['1','2'])
	if res2 == 0:
		break
	IdleAfter(30)
	
#result
printCheckStep(testname, 'Step 1', res1, res2)

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
# 在AP1上配置1个AC2的静态发现IP地址,保存配置
# 在AC1上重启无线功能
#
#预期
# AP静态配置优先级高于DHCP发现,show wi ap status在AC2上可以检测到AP1被AC2成功管理
# AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 3',
          'Config AC2 ip as switch-address-1 ip on AP1',
		  'Check the result')		  

# operate		  
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address1',If_vlan70_s2_ipv4_s)
ApSetcmd(ap1,Ap1cmdtype,'saverunning')

EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(20)
EnterEnableMode(switch2)
#check
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
						
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
# 在AC2上把s2p1接口down掉
#
#预期
# show wi ap status在AC1上可以检测到AP1被AC1成功管理,AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 4',
          'shutdown the interface on AC2',
          'Check the result')

# operate		  
EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'shutdown')

IdleAfter(20)
EnterEnableMode(switch1)
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
# 在AP1上把switch-address-1地址改为一个不可达的地址,保存配置
# 在AC2上把s2p1接口up
# 在AC1上配置部署AP1的主交换机地址为AC2的无线IP地址
#
#预期
#AC1上show wireless ap provisioning status显示“AP1_MAC”的“Provisioning Status”为“Success”
#在AP1上用get map-ap-provisioning查看：primary-switch-ip-address显示为IF_VLAN70_S2_IPV4
################################################################################

printStep(testname,'Step 5',
          'Config primary switch ip with AC2 ip on AP1',
          'Check the result')

# operate
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address1','1.1.1.1')	
ApSetcmd(ap1,Ap1cmdtype,'saverunning')
	  
EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'no shutdown')

EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap provision',ap1mac,'switch primary',If_vlan70_s2_ipv4_s)
SetCmd(switch1,'wireless ap provision start')

IdleAfter(10)
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless ap provisioning status')
#check1
res1 = CheckLine(data1,ap1mac,If_vlan70_s2_ipv4_s,'Success',IC=True)

IdleAfter(10)
#check2
res2 = Check_ap_provision_switchip(ap1,Ap1cmdtype,If_vlan70_s2_ipv4_s,mode='primary',ipversion='ipv4')
	
#result
printCheckStep(testname,'Step 5', res1, res2)

################################################################################
#Step 6
#
#操作
# 在AC1上重启无线功能
#
#预期
#AP自动部署发现的优先级高于DHCP发现,show wi ap status在AC2上可以检测到AP1被AC2成功管理
#AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 6',
          'Reboot wireless on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(20)
EnterEnableMode(switch2)
#check
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname,'Step 6', res1)

################################################################################
#Step 7
#
#操作
# 在AC2上把s2p1接口down掉
#
#预期
#show wi ap status在AC1上可以检测到AP1被AC1成功管理,AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 7',
          'Shutdown the interface on AC2',
          'Check the result')

# operate
EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'shutdown')

IdleAfter(20)
EnterEnableMode(switch1)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname,'Step 7', res1)

################################################################################
#Step 8
#
#操作
# 在S3关闭 dhcp 服务
# 在AP1上重启dhcp状态,并把switch-address-1地址改为AC1的IP地址,保存配置
#
#预期
#在AP1上通过get managed-ap查看：switch-address-1为IF_VLAN70_S1_IPV4
################################################################################

printStep(testname,'Step 8',
          'Config AC1 ip as switch-address-1 ip on AP1',
          'Check the result')

# operate
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address1',If_vlan70_s1_ipv4_s)
ApSetcmd(ap1,Ap1cmdtype,'saverunning')
ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_down')
ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_up')

EnterConfigMode(switch3)
SetCmd(switch3,'no service dhcp')

EnterConfigMode(switch2)
SetCmd(switch3,'interface',s2p1)
SetCmd(switch3,'no shutdown')

for i in range(5):
	#check
	res1 = Check_ap_automatic_switchip(ap1,Ap1cmdtype,'dhcp',[If_vlan70_s1_ipv4_s],['1'])
	if res1 == 0:
		break
	IdleAfter(30)
	
#result
printCheckStep(testname,'Step 8', res1)

################################################################################
#Step 9
#
#操作
# 在AC1上重启无线功能
#
#预期
#AP自动部署发现的优先级高于静态发现，show wi ap status在AC2上可以检测到AP1被AC2成功管理
#AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 9',
          'Reboot wireless on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(20)
EnterEnableMode(switch2)
#check
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname,'Step 9', res1)

################################################################################
#Step 10
#
#操作
# 在AC2上把s2p1接口down掉
#
#预期
#show wi ap status在AC1上可以检测到AP1被AC1成功管理,AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 10',
          'Shutdown the interface on AC2',
          'Check the result')

# operate
EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'shutdown')

IdleAfter(20)
EnterEnableMode(switch1)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname,'Step 10', res1)

################################################################################
#Step 11
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 11',
          'Recover initial config')

# operate		  
#恢复AC1的配置
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery ip-list')
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
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
	  
#end
printTimer(testname, 'End')