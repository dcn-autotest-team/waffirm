#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.11.py - test case 3.1.11 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-2 10:52:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.11 AP通过自动部署主动发现AC
# 测试目的：测试AP能通过自动部署主动发现AC
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.11'

avoiderror(testname)
printTimer(testname,'Start','Test AP active discovery AC through automatic deployment')

################################################################################
#Step 1
#
#操作
# 在AC1的ip-list发现列表中加入AP1的IP
#预期
# AP1能成功被AC管理,show wireless ap status在AC1上可以检测到AP1被AC1成功管理
################################################################################

printStep(testname,'Step 1',
          'Add AP1 ip address to discovery ip list',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',Ap1_ipv4)		  
IdleAfter(20)

# check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
# 在AC1上配置部署AP1的主交换机地址为AC1的无线IP地址
#
#预期
# AC1上show wireless ap provisioning status显示“AP1_MAC”的“Provisioning Status”为“Success”
# 在AP1上用get map-ap-provisioning查看:primary-switch-ip-address显示为If_vlan70_S1_ipv4
################################################################################

printStep(testname,'Step 2',
          'Config primary switch ip on AP1',
          'Check the result')

# operate
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap provision',ap1mac,'switch primary',If_vlan70_s1_ipv4_s)
SetCmd(switch1,'wireless ap provision start')
IdleAfter(10)
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless ap provisioning status')

#check1
res1 = CheckLine(data1,ap1mac,If_vlan70_s1_ipv4_s,'Success',IC=True)
IdleAfter(10)
#check2
res2 = Check_ap_provision_switchip(ap1,Ap1cmdtype,If_vlan70_s1_ipv4_s,mode='primary',ipversion='ipv4')
	
#result
printCheckStep(testname, 'Step 2', res1, res2)

################################################################################
#Step 3
#
#操作
# 在AC1上把AP1的IP从ip-list发现列表中删除
#
#预期
# show wi ap status在AC1上可以检测到AP1被AC1成功管理,AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 3',
          'Delete AP1 ip address from discovery ip list',
		  'Check the result')		  

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery ip-list',Ap1_ipv4)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
EnterEnableMode(switch1)
IdleAfter(20)

#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
# 在AC1的ip-list发现列表中加入AC2的IP
#
#预期
# 在AC1上用show wireless peer-switch可以检测到有"IP Address"为"IF_VLAN70_S2_IPV4"
################################################################################

printStep(testname,'Step 4',
          'Add AC2 ip address to discovery ip list',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',If_vlan70_s2_ipv4_s)
EnterEnableMode(switch1)
IdleAfter(20)

#check
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
				   check=[(If_vlan70_s2_ipv4_s)],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#在AC1上配置部署AP1的备交换机地址为AC2的无线IP地址
#
#预期
#配置成功,AC1上show wireless ap provisioning status显示"AP1_MAC"的"Backup"为"IF_VLAN70_S2_IPV4"
#在AP1上用get map-ap-provisioning查看:backup-switch-ip-address显示为IF_VLAN70_S2_IPV4
################################################################################

printStep(testname,'Step 5',
          'Config backup switch ip on AP1',
          'Check the result')

# operate
EnterEnableMode(switch1)
SetCmd(switch1,'show wireless ap status')
SetCmd(switch1,'wireless ap provision',ap1mac,'switch backup',If_vlan70_s2_ipv4_s)
SetCmd(switch1,'wireless ap provision start')
EnterEnableMode(switch1)
IdleAfter(10)
data1 = SetCmd(switch1,'show wireless ap provisioning status')

#check1
res1 = CheckLine(data1,If_vlan70_s2_ipv4_s,IC=True)
#check2
res2 = Check_ap_provision_switchip(ap1,Ap1cmdtype,If_vlan70_s2_ipv4_s,mode='backup',ipversion='ipv4')
	
#result
printCheckStep(testname,'Step 5', res1, res2)

################################################################################
#Step 6
#
#操作
#在AC1上把s1p1接口down掉
#
#预期
#等待60s,show wi ap status在AC2上可以检测到AP1被AC2成功管理,AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 6',
          'Shutdown the interface on AC1',
          'Check the result')

# operate		  
EnterConfigMode(switch1)
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'shutdown')
EnterEnableMode(switch2)
IdleAfter(60)

# check
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname, 'Step 6', res1)

################################################################################
#Step 7
#
#操作
#在AC1上把s1p1接口up
#在AC2上重启无线功能
#
#预期
#show wireless ap status在AC1上可以检测到AP1被AC1成功管理
#AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 7',
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
	
RebootAp(AP=ap1,connectTime=1)
IdleAfter(20)

#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname, 'Step 7', res1)

################################################################################
#Step 8
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 8',
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
		  
#end
printTimer(testname, 'End')