#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.23.py - test case 3.1.23 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-10 13:21:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.23 AP Provisioning表的添加,更新和删除
# 测试目的：测试AP Provisioning表的添加,更新和删除是否正确
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.23'

avoiderror(testname)
printTimer(testname,'Start','Test insert,update and delete of AP Provisioning table')

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

IdleAfter(30)
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
	
IdleAfter(20)
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

#check
res1 = CheckSutCmd(switch1,'show wireless',
                   check=[('Cluster Controller','Yes')],
                   retry=6,interval=5,waitflag=False,IC=True)
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
#在AC1上查看AP provisioning表
#
#预期
#在AC1上可以看到MAC Address显示为AP1_MAC和AP2_MAC,Primary&Backup Switch IP显示为”-----“
################################################################################

printStep(testname,'Step 4',
          'Check AP provisioning table on AC1',
          'Check the result')

#check
res1 = CheckSutCmd(switch1,'show wireless ap provisioning status',
                   check=[(ap1mac,'-----'),(ap2mac,'-----')],
                   retry=6,interval=5,waitflag=False,IC=True)			   
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#在AC2上查看AP provisioning表
#
#预期
#在AC2上显示”This command is valid only on the Cluster Controller”
################################################################################

printStep(testname,'Step 5',
          'Check AP provisioning table on AC2 1',
          'Check the result')

#check
res1 = CheckSutCmd(switch2,'show wireless ap provisioning status',
                   check=[('This command is valid only on the Cluster Controller')],
                   retry=1,waitflag=False,IC=True)	
#result
printCheckStep(testname,'Step 5', res1)

################################################################################
#Step 6
#
#操作
#在AC1的vlan-list发现列表中删除AP1和AP2的管理vlan vlan70
#在AC1上为AP1进行部署
#
#预期
#在AC1上通过show wireless ap provisioning status可以看到:
#MAC Address为AP1_MAC的Primary&Backup Switch IP显示为IF_VLAN70_S1_IPV4
################################################################################

printStep(testname,'Step 6',
          'Config primary and backup switch ip on AP1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list',Vlan70)	

EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap provision',ap1mac,'switch primary',If_vlan70_s1_ipv4_s)	
SetCmd(switch1,'wireless ap provision',ap1mac,'switch backup',If_vlan70_s2_ipv4_s)	  
SetCmd(switch1,'wireless ap provision start')
	   
IdleAfter(10)		  
data1 = SetCmd(switch1,'show wireless ap provisioning status')
#check
res1 = CheckLine(data1,ap1mac,If_vlan70_s1_ipv4_s,'Success',IC=True)

#result
printCheckStep(testname,'Step 6', res1)

################################################################################
#Step 7
#
#操作
#在S3上把接AP1的端口s3p3down掉
#
#预期
#在AC1上用show wireless ap provisioning status不能看到MAC Address显示为AP1_MAC的表项
################################################################################

printStep(testname,'Step 7',
          'Shutdown the interface on S3',
          'Check the result')

# operate
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'shutdown')		  
		  
IdleAfter(20)
#check	
res1 = CheckSutCmdWithNoExpect(switch1,'show wireless ap provisioning status',
                               check=[(ap1mac)],retry=30,interval=5,waitflag=False,IC=True)	
				   
#result
printCheckStep(testname,'Step 7', res2)

################################################################################
#Step 8
#
#操作
#在S3上把接AP1的端口s3p3up起来
#重启AP1
#
#预期
#AP1能成功被AC1管理,show wi ap status在AC1上能检测MAC Address为AP1_MAC的表项
#在AC1上用show wireless ap provisioning status能看到MAC Address显示为AP1_MAC的表项
################################################################################

printStep(testname,'Step 8',
          'No shutdown the interface on S3',
          'Check the result')

# operate
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'no shutdown')

#重启AP1
RebootAp(AP=ap1,connectTime=1)

IdleAfter(20)
#check1
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#check2
res2 = CheckSutCmd(switch1,'show wireless ap provisioning status',
				   check=[(ap1mac)],retry=30,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname,'Step 8', res1, res2)

################################################################################
#Step 9
#
#操作
#在AC2上把s2p1接口down掉
#在AC1上修改ap的认证方式为mac认证，删除AP1的ap database数据库
#在AC1上重启无线功能
#
#预期
#在AC1上sho wireless ap failure status可以检测到 MAC Address为AP1_MAC的表项
#在AC1上用show wireless ap provisioning status能看到MAC Address显示为AP1_MAC的表项
################################################################################

printStep(testname,'Step 9',
          'Change ap authentication mac after delete AP1 mac',
          'Check the result')

# operate
EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'shutdown')

EnterWirelessMode(switch1)
SetCmd(switch1,'no ap database',ap1mac)
SetCmd(switch1,'ap authentication mac')
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(20)
#check1
res1 = CheckSutCmd(switch1,'show wireless ap failure status',
				   check=[(ap1mac)],retry=30,interval=5,waitflag=False,IC=True)	

#check2
res2 = CheckSutCmd(switch1,'show wireless ap provisioning status',
				   check=[(ap1mac)],retry=30,interval=5,waitflag=False,IC=True)	
				   
#result
printCheckStep(testname,'Step 9', res1, res2)

################################################################################
#Step 10
#
#操作
#在AC2上把s2p1接口up起来
#在AC1上为AP2进行部署,重启无线功能
#
#预期
#在AC2上可以检测到AP2被AC2成功管理,AP2_MAC的“Status”为“Managed Success”
#在AC1上用show wireless ap provisioning status能看到MAC Address显示为AP2_MAC的表项
################################################################################

printStep(testname,'Step 10',
          'Config primary switch ip on AP2',
          'Check the result') 

# operate
EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'no shutdown')

IdleAfter(60)
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap provision',ap2mac,'switch primary',If_vlan70_s2_ipv4_s)
SetCmd(switch1,'wireless ap provision start')

IdleAfter(10)
EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(20)
#check1
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[(ap2mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)	
#check2
res2 = CheckSutCmd(switch1,'show wireless ap provisioning status',
				   check=[(ap2mac)],retry=30,interval=5,waitflag=False,IC=True)	
				   
#result
printCheckStep(testname,'Step 10', res1, res2)

################################################################################
#Step 11
#
#操作
#在S3上把接AP2的端口s3p4down掉
#
#预期
#在AC1上不能看到MAC Address显示为AP2_MAC的表项
################################################################################

printStep(testname,'Step 11',
          'Shutdown the interface on S3',
          'Check the result')

# operate
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p4)
SetCmd(switch3,'shutdown')

IdleAfter(20)
#check
res1 = CheckSutCmdWithNoExpect(switch1,'show wireless ap provisioning status',
                               check=[(ap2mac)],retry=30,interval=5,waitflag=False,IC=True)	
				   
#result
printCheckStep(testname,'Step 11', res2)

################################################################################
#Step 12
#
#操作
#在S3上把接AP2的端口s3p4up起来
#
#预期
#在AC2上可以检测到AP2被AC2成功管理,AP2_MAC的“Status”为“Managed Success”
#在AC1上用show wireless ap provisioning status能看到MAC Address显示为AP2_MAC的表项
################################################################################

printStep(testname,'Step 12',
          'No shutdown the interface on S3',
          'Check the result')

# operate
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p4)
SetCmd(switch3,'no shutdown')

IdleAfter(20)
#check1
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[(ap2mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)	
#check2
res2 = CheckSutCmd(switch1,'show wireless ap provisioning status',
				   check=[(ap2mac)],retry=30,interval=5,waitflag=False,IC=True)
#result
printCheckStep(testname,'Step 12', res1, res2)

################################################################################
#Step 13
#
#操作
#在AC2上配置集群优先级2 
#
#预期
#在AC1上用show wireless ap provisioning status显示:”This command is valid only on the Cluster Controller”
################################################################################

printStep(testname,'Step 13',
          'Set cluster priority as 2 on AC2',
          'Check the result')

# operate
EnterWirelessMode(switch2)
SetCmd(switch2,'cluster-priority 2')

IdleAfter(30)
#check
res1 = CheckSutCmd(switch1,'show wireless ap provisioning status',
				   check=[('This command is valid only on the Cluster Controller')],
				   retry=30,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname,'Step 13', res1)

################################################################################
#Step 14
#
#操作
#在AC2上查看AP provisioning表
#
#预期
#在AC2上用show wireless ap provisioning status能看到MAC Address显示为AP2_MAC的表项
################################################################################

printStep(testname,'Step 14',
          'Check AP provisioning table on AC2',
          'Check the result')

# operate
IdleAfter(30)
#check
res1 = CheckSutCmd(switch2,'show wireless ap provisioning status',
				   check=[(ap2mac)],retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 14', res1)

################################################################################
#Step 15
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 15',
          'Recover initial config')

# operate		  
#恢复AC1的配置
EnterWirelessMode(switch1)
SetCmd(switch1,'ap authentication none')
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'profile 1')

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

#配置AC1的IP列表
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery ip-list',If_vlan70_s2_ipv4_s)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
SetCmd(switch1,'wireless ap anti-flood')
SetCmd(switch1,'no discovery vlan-list',Vlan70)

#恢复AC2的配置
EnterWirelessMode(switch2)
SetCmd(switch2,'no enable')
IdleAfter(1)
SetCmd(switch2,'enable')
SetCmd(switch2,'no cluster-priority')

EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'no shutdown')

#恢复S3的配置
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'no shutdown')
SetCmd(switch3,'interface',s3p4)
SetCmd(switch3,'no shutdown')

#end
printTimer(testname, 'End')