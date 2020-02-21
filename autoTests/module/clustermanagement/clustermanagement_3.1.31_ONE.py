#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.31.py - test case 3.1.31 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-16 17:34:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.31 AP根据硬件类型,IP地址和ap database选择Profile功能测试及优先级测试
# 测试目的:测试AP根据硬件类型,IP地址和ap database选择Profile功能及优先级功能是否正常
# 测试环境:同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.31'

avoiderror(testname)
printTimer(testname,'Start','Test AP select profile and priority through hardware type,IP Address and ap database')

################################################################################
#Step 1
#
#操作
#在AC1和AC2下删除ap database下绑定的profile,删除profile 1和profile 2下绑定的硬件类型,即硬件类型为any
#把AP1的管理vlan vlan70加入到AC1的vlan list中
#
#预期
#show wi ap status在AC1上可以检测到AP1和AP2被AC1成功管理
#AP1_MAC的“Status”为“Managed Success”,“Profile”为“1”
#AP2_MAC的“Status”为“Managed Success”,“Profile”为“1”
################################################################################

printStep(testname,'Step 1',
          'Set hwtype as any',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'no profile')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap2mac)
SetCmd(switch1,'no profile')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 1')
SetCmd(switch1,'no hwtype')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 2')
SetCmd(switch1,'no hwtype')

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery vlan-list',Vlan70)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(20)
EnterEnableMode(switch1)
#check1
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'1','Managed','Success'),
				          (ap2mac,'1','Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
#在AC1创建profile 3和profile 4,硬件类型绑定AP1和AP2对应的硬件类型:AP1_HWTYPE和AP2_HWTYPE
#
#预期
#show wi ap status在AC1上可以检测到AP1和AP2被AC1成功管理
#AP1_MAC的“Status”为“Managed Success”,“Profile”为“3”
#AP2_MAC的“Status”为“Managed Success”,“Profile”为“4”
################################################################################

printStep(testname,'Step 2',
          'Creat two profile and bind AP1 and AP2 hwtype',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 3')
SetCmd(switch1,'hwtype',hwtype1)
SetCmd(switch1,'exit')
SetCmd(switch1,'ap profile 4')
SetCmd(switch1,'hwtype',hwtype2)

EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(20)
EnterEnableMode(switch1)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'3','Managed','Success'),
				          (ap2mac,'4','Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
#对AP1、AC1和S3进行配置
#
#预期
#show wi ap status在AC1上可以检测到AP1和AP2被AC1成功管理
#AP1_MAC的“Status”为“Managed Success”,“Profile”为“5”
#AP2_MAC的“Status”为“Managed Success”,“Profile”为“6”
################################################################################

printStep(testname,'Step 3',
          'Creat two profile and config AP select profile according to IP',
		  'Check the result')		  

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery vlan-list',Vlan90)

EnterWirelessMode(switch1)	
SetCmd(switch1,'ap profile 5')
EnterWirelessMode(switch1)	
SetCmd(switch1,'ap profile 6')

EnterConfigMode(switch1)
SetCmd(switch1,'vlan',Vlan90)
EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan90)
SetCmd(switch1,'ip address',If_vlan90_s1_ipv4)

EnterConfigMode(switch1)
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'switchport mode trunk')
SetCmd(switch1,'switchport trunk allowed vlan',Vlan70+';'+Vlan80+';'+Vlan90)

EnterConfigMode(switch3)
SetCmd(switch3,'interface vlan',Vlan70)
SetCmd(switch3,'ip address',If_vlan70_s3_ipv4)

EnterConfigMode(switch3)
SetCmd(switch3,'vlan',Vlan90)
EnterConfigMode(switch3)
SetCmd(switch3,'interface vlan',Vlan90)
SetCmd(switch3,'ip address',If_vlan90_s3_ipv4)
	
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p4)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan90)
SetCmd(switch3,'switchport trunk allowed vlan',Vlan80)

EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p1)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk allowed vlan',Vlan70+';'+Vlan80+';'+Vlan90)

EnterConfigMode(switch3)
SetCmd(switch3,'ip dhcp pool AP1')
SetCmd(switch3,'network-address',Dhcp_ap_pool_ipv4)
SetCmd(switch3,'default-router',If_vlan70_s3_ipv4_s)

EnterConfigMode(switch3)
SetCmd(switch3,'ip dhcp pool AP2')
SetCmd(switch3,'network-address',Dhcp_ap_pool_ipv4_vlan90)
SetCmd(switch3,'default-router',If_vlan90_s3_ipv4_s)

EnterConfigMode(switch3)
SetCmd(switch3,'no service dhcp')
SetCmd(switch3,'service dhcp')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap address',ap_address_vlan70,'profile 5')
SetCmd(switch1,'ap address',ap_address_vlan90,'profile 6')

EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_up')
ApSetcmd(ap2,Ap2cmdtype,'set_dhcp_up')

IdleAfter(30)
EnterEnableMode(switch1)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'5','Managed','Success'),
				          (ap2mac,'6','Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
		   
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
#在AC1的AP1 database下绑定profile 1,AP2 database下绑定profile2
#
#预期
#show wi ap status在AC1上可以检测到AP1和AP2被AC1成功管理
#AP1_MAC的“Status”为“Managed Success”,“Profile”为“1”
#AP2_MAC的“Status”为“Managed Success”,“Profile”为“2”
################################################################################

printStep(testname,'Step 4',
          'Bind profile to ap database',
          'Check the result')	  

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'profile 1')	
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap2mac)
SetCmd(switch1,'profile 2')	 

EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable') 
		  
IdleAfter(20)
EnterEnableMode(switch1)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'1','Managed','Success'),
				          (ap2mac,'2','Managed','Success')],
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
#恢复AP1的配置
ApSetcmd(ap1,Ap1cmdtype,'set_static_ip',Ap1_ipv4) 
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6',Ap1_ipv6) 
ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_down') 
ApSetcmd(ap1,Ap1cmdtype,'set_dhcpv6_down') 
ApSetcmd(ap1,Ap1cmdtype,'set_ip_route',If_vlan70_s3_ipv4_s) 
ApSetcmd(ap1,Ap1cmdtype,'set_ipv6_route',If_vlan70_s3_ipv6_s) 
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6_prefix_len','64') 
ApSetcmd(ap1,Ap1cmdtype,'saverunning') 

#恢复AP2的配置
ApSetcmd(ap2,Ap2cmdtype,'set_static_ip',Ap2_ipv4) 
ApSetcmd(ap2,Ap2cmdtype,'set_static_ipv6',Ap2_ipv6) 
ApSetcmd(ap2,Ap2cmdtype,'set_dhcp_down') 
ApSetcmd(ap2,Ap2cmdtype,'set_dhcpv6_down') 
ApSetcmd(ap2,Ap2cmdtype,'set_ip_route',If_vlan70_s3_ipv4_s) 
ApSetcmd(ap2,Ap2cmdtype,'set_ipv6_route',If_vlan70_s3_ipv6_s) 
ApSetcmd(ap2,Ap2cmdtype,'set_static_ipv6_prefix_len','64') 
ApSetcmd(ap2,Ap2cmdtype,'saverunning') 

#恢复AC1的配置
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'profile 1')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap2mac)
SetCmd(switch1,'profile 2')

EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list',Vlan70)
SetCmd(switch1,'no discovery vlan-list',Vlan90)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 1')
SetCmd(switch1,'hwtype',hwtype1)
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 2')
SetCmd(switch1,'hwtype',hwtype2)

EnterWirelessMode(switch1)
SetCmd(switch1,'no ap address',ap_address_vlan70,'profile 5')
SetCmd(switch1,'no ap address',ap_address_vlan90,'profile 6')

EnterWirelessMode(switch1)
SetCmd(switch1,'no ap profile 3')
SetCmd(switch1,'no ap profile 4')
SetCmd(switch1,'no ap profile 5')
SetCmd(switch1,'no ap profile 6')

EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan',Vlan90)
SetCmd(switch1,'no vlan',Vlan90)

EnterConfigMode(switch1)
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'switchport mode trunk')
SetCmd(switch1,'switchport trunk allowed vlan',Vlan70+';'+Vlan80)

#恢复S3的配置
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p4)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan70)
SetCmd(switch3,'switchport trunk allowed vlan',Vlan80)

EnterConfigMode(switch3)
SetCmd(switch3,'no interface vlan',Vlan70)
SetCmd(switch3,'no interface vlan',Vlan90)
SetCmd(switch3,'no vlan',Vlan90)
SetCmd(switch3,'no ip dhcp pool AP1')
SetCmd(switch3,'no ip dhcp pool AP2')

EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p1)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk allowed vlan',Vlan70+';'+Vlan80)
	  
#end
printTimer(testname, 'End')