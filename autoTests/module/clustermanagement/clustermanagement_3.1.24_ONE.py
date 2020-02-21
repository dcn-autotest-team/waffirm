#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.24.py - test case 3.1.24 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-10 15:21:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.24 AP自动部署功能
# 测试目的：测试AP自动部署功能是否正确
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.24'

avoiderror(testname)
printTimer(testname,'Start','Test automatic deployment of AP')

################################################################################
#Step 1
#
#操作
#在AC1的vlan-list发现列表中加入AP1和AP2的管理vlan vlan70
#
#预期
#AP1能成功被AC管理,show wi ap status在AC1上可以检测到AP1和AP2被AC1成功管理
#AP1_MAC的“Status”为“Managed Success”,AP2_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 1',
          'Add management vlan to discovery vlan list on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch2)
SetCmd(switch2,'no discovery vlan-list 1')

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery vlan-list',Vlan70)
SetCmd(switch1,'no wireless ap anti-flood')
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(20)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success'),
				   (ap2mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
#在AC1的ip-list发现列表中加入AC的ip
#
#预期
#AC1上show wireless peer-switch显示有:
#“IP Address”为“IF_VLAN70_S2_IPV4”,“Disc. Reason”显示为“IP Poll”
################################################################################

printStep(testname,'Step 2',
          'Add AC2 ip to discovery ip list on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',If_vlan70_s2_ipv4_s)
	
IdleAfter(30)	
#check
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
				   check=[(If_vlan70_s2_ipv4_s,'IP Poll')],
				   retry=30,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
#在AC1上查看集群信息
#
#预期
#show wireless显示”Cluster Controller”为”Yes”
################################################################################

printStep(testname,'Step 3',
          'Check the cluster controller on AC1',
		  'Check the result')		  

# operate
IdleAfter(20)
data1 = SetCmd(switch1,'show wireless')
#check
res1 = CheckLine(data1,'Cluster Controller','Yes',IC=True)
				   
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
#在AC1上为AP1进行部署
#
#预期
#在AC1上通过show wireless ap provisioning status可以看到:
#MAC Address为AP1_MAC的Primary&Backup Switch IP显示为IF_VLAN70_S1_IPV4,Provisioning Status显示为“Success”
################################################################################

printStep(testname,'Step 4',
          'Config primary switch ip on AP1',
          'Check the result')

# operate
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap provision',ap1mac,'switch primary',If_vlan70_s1_ipv4_s)
SetCmd(switch1,'wireless ap provision start')	
	
IdleAfter(10)
data1 = SetCmd(switch1,'show wireless ap provisioning status')
#check
res1 = CheckLine(data1,ap1mac,If_vlan70_s1_ipv4_s,'Success',IC=True)
				   
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#在AC2从valid ap表中删除MAC地址为AP1_MAC的表项
#
#预期
#在AC2上用sho wireless ap database不能找到MAC地址为AP1_MAC的表项
################################################################################

printStep(testname,'Step 5',
          'Delete AP1 MAC from ap database on AC2',
          'Check the result')

# operate
EnterWirelessMode(switch2)
SetCmd(switch2,'no ap database',ap1mac)
  
IdleAfter(5)
data1 = SetCmd(switch2,'show wireless ap database')
#check
res1 = CheckLine(data1,ap1mac,IC=True)
res1 = 0 if res1 != 0 else 1
	
#result
printCheckStep(testname,'Step 5', res1)

################################################################################
#Step 6
#
#操作
#在AC1上为AP1进行部署
#
#预期
#在AC1上通过show wireless ap provisioning status可以看到:
#MAC Address为AP1_MAC的Primary&Backup Switch IP显示为IF_VLAN70_S2_IPV4,Provisioning Status显示为“Success”
#在AP1上通过get map-ap-provisioning可以检测到:primary-switch-ip-address为IF_VLAN70_S2_IPV4
################################################################################

printStep(testname,'Step 6',
          'Config primary switch ip on AP1',
          'Check the result')

# operate
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap provision',ap1mac,'switch primary',If_vlan70_s2_ipv4_s)	  
SetCmd(switch1,'wireless ap provision start')
	   
IdleAfter(10)		  
data1 = SetCmd(switch1,'show wireless ap provisioning status')
#check1
res1 = CheckLine(data1,ap1mac,If_vlan70_s2_ipv4_s,'Success',IC=True)

IdleAfter(10)		  
#check2
res2 = Check_ap_provision_switchip(ap1,Ap1cmdtype,If_vlan70_s2_ipv4_s,mode='primary',ipversion='ipv4')

#result
printCheckStep(testname,'Step 6', res1, res2)

################################################################################
#Step 7
#
#操作
#在AC2上查看ap valid database
#
#预期
#在AC2上用sho wireless ap database 显示“MAC Address”为“AP1_MAC"
################################################################################

printStep(testname,'Step 7',
          'Check ap database on AC2',
          'Check the result')	  

# operate		  
data1 = SetCmd(switch2,'show wireless ap database')
#check
res1 = CheckLine(data1,ap1mac,IC=True)
				   
#result
printCheckStep(testname,'Step 7', res1)

################################################################################
#Step 8
#
#操作
#在AC1的vlan-list发现列表中删除AP1和AP2的管理vlan vlan70
#在AC1上重启无线功能
#
#预期
#AP1能成功被AC2管理,show wi ap status在AC2上可以检测到AP1被AC2成功管理
#AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 8',
          'Delete management vlan from discovery vlan list on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list',Vlan70)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(20)
#check
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 8', res1)

################################################################################
#Step 9
#
#操作
#在AC1上为AP1进行部署
#
#预期
#AC1上show wireless peer-switch显示有“IP Address”为“IF_VLAN70_S2_IPV4",“Disc. Reason”显示为“IP Poll”
#在AC1上通过show wireless ap provisioning status可以看到:
#MAC Address为AP1_MAC的Primary&Backup Switch IP显示为IF_VLAN70_S1_IPV4,Provisioning Status显示为“Success”
#在AP1上通过get map-ap-provisioning可以检测到:primary-switch-ip-address为IF_VLAN70_S1_IPV4
################################################################################

printStep(testname,'Step 9',
          'Config primary switch ip on AP1',
          'Check the result')

# operate
IdleAfter(20)
EnterEnableMode(switch1)
#check
res = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)	
				   
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap provision',ap1mac,'switch primary',If_vlan70_s1_ipv4_s)	  
SetCmd(switch1,'wireless ap provision start')		  
		  
IdleAfter(20)
#check1
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
				   check=[(If_vlan70_s2_ipv4_s,'IP Poll')],
				   retry=30,interval=5,waitflag=False,IC=True)	
				   
IdleAfter(10)
data1 = SetCmd(switch1,'show wireless ap provisioning status')
#check2
res2 = CheckLine(data1,ap1mac,If_vlan70_s1_ipv4_s,'Success',IC=True)

IdleAfter(10)
#check3
res3 = Check_ap_provision_switchip(ap1,Ap1cmdtype,If_vlan70_s1_ipv4_s,mode='primary',ipversion='ipv4')

#result
printCheckStep(testname,'Step 9', res, res1, res2, res3)

################################################################################
#Step 10
#
#操作
#在AC2上删除AP1的valid database
#在AC1上为AP1进行部署
#
#预期
#在AC1上通过show wireless ap provisioning status可以看到:
#MAC Address为AP1_MAC的Primary&Backup Switch IP显示为IF_VLAN70_S2_IPV4,Provisioning Status显示为“Success”
#在AP1上通过get map-ap-provisioning可以检测到:primary-switch-ip-address为IF_VLAN70_S2_IPV4
################################################################################

printStep(testname,'Step 10',
          'Config primary switch ip on AP1',
          'Check the result') 

# operate
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap provision',ap1mac,'switch primary',If_vlan70_s2_ipv4_s)
SetCmd(switch1,'wireless ap provision start')

EnterWirelessMode(switch1)
SetCmd(switch1,'no ap database',ap1mac)

IdleAfter(10)
data1 = SetCmd(switch1,'show wireless ap provisioning status')
#check1
res1 = CheckLine(data1,ap1mac,If_vlan70_s2_ipv4_s,'Success',IC=True)
IdleAfter(10)
#check2
res2 = Check_ap_provision_switchip(ap1,Ap1cmdtype,If_vlan70_s2_ipv4_s,mode='primary',ipversion='ipv4')
				   
#result
printCheckStep(testname,'Step 10', res1, res2)

################################################################################
#Step 11
#
#操作
#在AC2上查看ap valid database
#
#预期
#在AC2上用show wireless ap database 显示“MAC Address”为“AP1_MAC"
################################################################################

printStep(testname,'Step 11',
          'Check ap database on AC2',
          'Check the result')

# operate
data1 = SetCmd(switch2,'show wireless ap database')
#check
res1 = CheckLine(data1,ap1mac,IC=True)
				   
#result
printCheckStep(testname,'Step 11', res1)

################################################################################
#Step 12
#
#操作
#在AC2上删除AP1的valid database
#在AC1上为AP1进行部署
#
#预期
#在AC1上通过show wireless ap provisioning status可以看到:
#MAC Address为AP1_MAC的Primary&Backup Switch IP显示为IF_VLAN70_S2_IPV4,Provisioning Status显示为“Success”
#在AP1上通过get map-ap-provisioning可以检测到:backup-switch-ip-address显示为IF_VLAN70_S2_IPV4
################################################################################

printStep(testname,'Step 12',
          'Config primary switch ip on AP1',
          'Check the result')

# operate
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap provision',ap1mac,'switch backup',If_vlan70_s2_ipv4_s)
SetCmd(switch1,'wireless ap provision start')		  

EnterWirelessMode(switch1)
SetCmd(switch1,'no ap database',ap1mac)

IdleAfter(10)
data1 = SetCmd(switch1,'show wireless ap provisioning status')
#check1
res1 = CheckLine(data1,ap1mac,If_vlan70_s2_ipv4_s,'Success',IC=True)

IdleAfter(10)
#check2
res2 = Check_ap_provision_switchip(ap1,Ap1cmdtype,If_vlan70_s2_ipv4_s,mode='primary',ipversion='ipv4')

#result
printCheckStep(testname,'Step 12', res1, res2)

################################################################################
#Step 13
#
#操作
#在AC2上查看ap valid database 
#
#预期
#在AC2上用sho wireless ap database 显示“MAC Address”为“AP1_MAC"
################################################################################

printStep(testname,'Step 13',
          'Check ap database on AC2',
          'Check the result')

# operate
IdleAfter(10)
data1 = SetCmd(switch2,'show wireless ap database')

#check
res1 = CheckLine(data1,ap1mac,IC=True)

#result
printCheckStep(testname,'Step 13', res1)

################################################################################
#Step 14
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 14',
          'Recover initial config')

# operate		  
#配置AC1的database
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'profile 1')

#配置AC2的database
EnterWirelessMode(switch2)
SetCmd(switch2,'ap database',ap1mac)
SetCmd(switch2,'profile 1')

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

#恢复AP2的配置
RebootAp(setdefaut=True, AP=ap2,connectTime=1)
ApSetcmd(ap2,Ap2cmdtype,'set_static_ip',Ap2_ipv4) 
ApSetcmd(ap2,Ap2cmdtype,'set_static_ipv6',Ap2_ipv6) 
ApSetcmd(ap2,Ap2cmdtype,'set_dhcp_down') 
ApSetcmd(ap2,Ap2cmdtype,'set_dhcpv6_down') 
ApSetcmd(ap2,Ap2cmdtype,'set_ip_route',If_vlan70_s3_ipv4_s) 
ApSetcmd(ap2,Ap2cmdtype,'set_ipv6_route',If_vlan70_s3_ipv6_s) 
ApSetcmd(ap2,Ap2cmdtype,'set_static_ipv6_prefix_len','64') 
ApSetcmd(ap2,Ap2cmdtype,'saverunning') 

#配置AC2的vlan list
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery vlan-list 1')
SetCmd(switch2,'no enable')
IdleAfter(1)
SetCmd(switch2,'enable')

#配置AC1的vlan list
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list',Vlan70)
SetCmd(switch1,'wireless ap anti-flood')
SetCmd(switch1,'no discovery ip-list',If_vlan70_s2_ipv4_s)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

#end
printTimer(testname, 'End')