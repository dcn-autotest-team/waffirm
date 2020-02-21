#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.12.py - test case 3.1.12 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-2 13:50:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.12 AP通过静态配置主动发现AC
# 测试目的：测试AP能通过静态配置主动发现AC
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.12'

avoiderror(testname)
printTimer(testname,'Start','Test AP active discovery AC through static config')

################################################################################
#Step 1
#
#操作
# 在AP1上配置4个AC的IP地址
#预期
# 配置成功，在AP1上通过get managed-ap查看：
# switch-address-1为1.1.1.1; switch-address-2为2.2.2.2
# switch-address-3为3.3.3.3; switch-address-4为4.4.4.4
################################################################################

printStep(testname,'Step 1',
          'Config four managed-ap switch-address on AP1',
          'Check the result')

# operate
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address','1.1.1.1',addressnum='1')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address','2.2.2.2',addressnum='2')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address','3.3.3.3',addressnum='3')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address','4.4.4.4',addressnum='4')
	
#check
res1 = Check_ap_static_switchip(ap1,Ap1cmdtype,['1.1.1.1','2.2.2.2','3.3.3.3','4.4.4.4'],['1','2','3','4'])
	
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
# 在AP1上配置4个AC的IP地址对应的域名
#
#预期
#配置成功，在AP1上通过get managed-ap查看：
#switch-address-1为test11; switch-address-2为test21
#switch-address-3为test31; switch-address-4为test41
################################################################################

printStep(testname,'Step 2',
          'Config four domain of AC on AP1',
          'Check the result')

# operate
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address','test11',addressnum='1')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address','test21',addressnum='2')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address','test31',addressnum='3')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address','test41',addressnum='4')

#check
res1 = Check_ap_static_switchip(ap1,Ap1cmdtype,['test11','test21','test31','test41'],['1','2','3','4'])
	
#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
# 在AP1上配置2个AC的IP地址，2个AC的IP地址对应的域名
#
#预期
# 配置成功，在AP1上通过get managed-ap查看：
#switch-address-1为IF_VLAN70_S1_IPV4; switch-address-2为test2
#switch-address-3为IF_VLAN70_S2_IPV4; switch-address-4为test4
#show wi ap status在AC1上可以检测到AP1被AC1成功管理,AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 3',
          'Config managed-ap switch-address with AC1 and AC2 ip',
		  'Check the result')		  

# operate
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address',If_vlan70_s1_ipv4_s,addressnum='1')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address','test2',addressnum='2')	
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address',If_vlan70_s2_ipv4_s,addressnum='3')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address','test4',addressnum='4')		
ApSetcmd(ap1,Ap1cmdtype,'saverunning')
RebootAp(AP=ap1,connectTime=1)

#check1
res1 = Check_ap_static_switchip(ap1,Ap1cmdtype,[If_vlan70_s1_ipv4_s,'test2',
                                If_vlan70_s2_ipv4_s,'test4'],['1','2','3','4'])

IdleAfter(20)
#check2
res2 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
						
#result
printCheckStep(testname, 'Step 3', res1, res2)

################################################################################
#Step 4
#
#操作
# 把AC2的IPv4地址加入到AC1的ip-list中
#
#预期
# 在AC1上show wireless peer-switch显示有“IP Address”为“IF_VLAN70_S2_IPV4”的条目
################################################################################

printStep(testname,'Step 4',
          'Add AC2 ip address to discovery ip list',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',If_vlan70_s2_ipv4_s)
IdleAfter(30)

#check1
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
				   check=[(If_vlan70_s2_ipv4_s)],
				   retry=30,interval=5,waitflag=False,IC=True)
#check2
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[ap1mac,'Managed','Success'],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname,'Step 4', res1, res2)

################################################################################
#Step 5
#
#操作
#在AC1和AC2 的profile 1中配置DNS 
#
#预期
#show wi ap status在AC2上可以检测到AP1被AC2成功管理,AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 5',
          'Config DNS on profile 1 of AC1 and AC2',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 1')
SetCmd(switch1,'dns-server primary',dns_server_ip)
		 
EnterWirelessMode(switch2)
SetCmd(switch2,'ap profile 1')
SetCmd(switch2,'dns-server primary',dns_server_ip)
		 
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap profile apply 1',promotePatten='Y/N',promoteTimeout=5)
SetCmd(switch1,'y')

IdleAfter(20)
EnterEnableMode(switch1)
#check1
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)

ApSetcmd(ap1,Ap1cmdtype,'set_switch_address',If_vlan70_s2_ipv4_s,addressnum='1')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address',If_vlan70_s1_ipv4_s,addressnum='3')
ApSetcmd(ap1,Ap1cmdtype,'saverunning')

EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

RebootAp(AP=ap1)

#check2
res2 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname,'Step 5', res1, res2)

################################################################################
#Step 6
#
#操作
#在S3上配置用户vlan80和管理VLAN 70对应的IP地址
#在AP1上配置switch-address-2为AC1对应的域名,switch-address-4为AC2对应的域名,
#switch-address-1和switch-address-3为不可达IP,保存配置
#在AC2上重启无线功能
#
#预期
#show wi ap status在AC1上可以检测到AP1被AC1成功管理,AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 6',
          'Config the domain of AC1 on AP1',
          'Check the result')

# operate		  
EnterConfigMode(switch3)
SetCmd(switch3,'interface vlan',Vlan80)
SetCmd(switch3,'ip address',If_vlan80_s3_ipv4)
EnterConfigMode(switch3)
SetCmd(switch3,'interface vlan',Vlan70)
SetCmd(switch3,'ip address',If_vlan70_s3_ipv4)

ApSetcmd(ap1,Ap1cmdtype,'set_switch_address','1.1.1.1',addressnum='1')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address',ac1_domain,addressnum='2')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address','3.3.3.3',addressnum='3')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address',ac2_domain,addressnum='4')
ApSetcmd(ap1,Ap1cmdtype,'saverunning')

EnterWirelessMode(switch2)
SetCmd(switch2,'no enable')
IdleAfter(1)
SetCmd(switch2,'enable')
IdleAfter(20)

#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname, 'Step 6', res1)

################################################################################
#Step 7
#
#操作
#在AC1上把s1p1接口down掉
#
#预期
#等待60s,show wi ap status在AC2上可以检测到AP1被AC2成功管理,AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 7',
          'Shutdown the interface on AC1',
          'Check the result')

# operate		  
EnterConfigMode(switch1)
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'shutdown')	
IdleAfter(20)

#check
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname, 'Step 7', res1)

################################################################################
#Step 8
#
#操作
#在AC1上把s1p1接口up
#在AC2上重启无线功能
#
#预期
#show wi ap status在AC1上可以检测到AP1被AC1成功管理。AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 8',
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
printCheckStep(testname, 'Step 8', res1)

################################################################################
#Step 9
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 9',
          'Recover initial config')

# operate		  
#恢复AC1的配置
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 1')
SetCmd(switch1,'no dns-server primary')
EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
SetCmd(switch1,'no discovery ip-list')
EnterConfigMode(switch1)
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'no shutdown')

#恢复AC2的配置
EnterWirelessMode(switch2)
SetCmd(switch2,'ap profile 1')
SetCmd(switch2,'no dns-server primary')
EnterWirelessMode(switch2)
SetCmd(switch2,'no enable')
IdleAfter(1)
SetCmd(switch2,'enable')

#恢复S3的配置
EnterConfigMode(switch3)
SetCmd(switch3,'no interface vlan',Vlan80)
SetCmd(switch3,'no interface vlan',Vlan70)

#恢复AP1的配置
RebootAp(setdefaut=True, AP=ap1,connectTime=1)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ip',Ap1_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6',Ap1_ipv6)
ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_down')
ApSetcmd(ap1,Ap1cmdtype,'set_dhcpv6_down')
ApSetcmd(ap1,Ap1cmdtype,'set_ip_route',If_vlan70_s3_ipv4_s)
ApSetcmd(ap1,Ap1cmdtype,'set_ipv6_route',If_vlan70_s3_ipv6_s)
ApSetcmd(ap1,Ap1cmdtype,'saverunning')
		  
#end
printTimer(testname, 'End')