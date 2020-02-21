#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.26.py - test case 3.1.26 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-16 10:42:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.26 AP信息和AP认证失败信息的收集和处理
# 测试目的：测试AP信息和AP认证失败信息的收集和处理功能是否正常
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.26'

avoiderror(testname)
printTimer(testname,'Start','Test collection and disposal of AP authentic information')

################################################################################
#Step 1
#
#操作
#把AP1的ip list中添加AC1的发现IP列表中
#
#预期
#show wi ap status在AC1上可以检测到AP1被AC1成功管理
################################################################################

printStep(testname,'Step 1',
          'Add AP1 ip to discovery ip list on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',Ap1_ipv4)

IdleAfter(20)
EnterEnableMode(switch1)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
#把AC2的IP地址加入到AC1的三层发现ip list中
#
#预期
#在AC1上show wireless peer-switch显示有“IP Address”为“IF_VLAN70_S2_IPV4”的
################################################################################

printStep(testname,'Step 2',
          'Add AC2 ip to discovery ip list on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',If_vlan70_s2_ipv4_s)

IdleAfter(30)
EnterEnableMode(switch1)
#check
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
				   check=[(If_vlan70_s2_ipv4_s)],
				   retry=30,interval=5,waitflag=False,IC=True)
				   
#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
#在AC2上查看AP的状态
#
#预期
#在AC2上检查显示：No managed APs discovered
################################################################################

printStep(testname,'Step 3',
          'Check AP1 status on AC2',
		  'Check the result')		  

# operate
IdleAfter(20)
EnterEnableMode(switch1)
#check
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[('No managed APs discovered')],
				   retry=30,interval=5,waitflag=False,IC=True)			   
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
#在AC2上配置集群优先级2
#
#预期
#show wireless显示”Cluster Controller”为”Yes”
################################################################################

printStep(testname,'Step 4',
          'Set cluster-priority value as 2 on AC2',
          'Check the result')

# operate
EnterWirelessMode(switch2)
SetCmd(switch2,'cluster-priority 2')	
	
IdleAfter(30)
data1 = SetCmd(switch2,'show wireless')
#check
res1 = CheckLine(data1,'Cluster Controller','Yes',IC=True)
				   
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#在AC2上查看AP的状态
#
#预期
#非Controller AC1会把AP的信息发送给新的Controller AC2
#在AC2上show wireless ap status显示:AP1的mac地址“AP1_MAC”的“Status”为“Managed”
#AP1的mac地址“AP1_MAC”的“Status”为“Managed,“Configuration Status”为“Success”
################################################################################

printStep(testname,'Step 5',
          'Check AP1 status on AC2',
          'Check the result')

# operate
IdleAfter(20)
EnterEnableMode(switch2)
#check
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)	
	
#result
printCheckStep(testname,'Step 5', res1)

################################################################################
#Step 6
#
#操作
#在S3上把接AP1的端口s3p3down掉
#
#预期
#AP1_MAC的“Status”为“Failed”,“Configuration Status”为“Not Config”
################################################################################

printStep(testname,'Step 6',
          'Shutdown interface s3p3 on S3',
          'Check the result')

# operate
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'shutdown')

IdleAfter(20)
EnterEnableMode(switch1)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Failed','Not Config')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 6', res1)

################################################################################
#Step 7
#
#操作
#在AC2上查看AP1的状态
#
#预期
#非Controller AC1会把AP的新的信息发送给Controller AC2
#在AC2上show wireless ap status显示AP1的mac地址“AP1_MAC”的“Status”为“Failed”
#“AP1_MAC”的“Configuration Status”为“Not Config”
################################################################################

printStep(testname,'Step 7',
          'Check AP1 status on AC2',
          'Check the result')	  

# operate
IdleAfter(20)	
EnterEnableMode(switch1)	  
data1 = SetCmd(switch1,'show wireless ap status')
#check1
res1 = CheckLine(data1,ap1mac,'Failed','Not Config',IC=True)		
	
#result
printCheckStep(testname,'Step 7', res1)

################################################################################
#Step 8
#
#操作
#在AC1上把failed AP AP1从managed AP database里清除
#
#预期
#非Controller AC1会把AP的新的信息发送给Controller AC2,在AC2上显示：No managed APs discovered
################################################################################

printStep(testname,'Step 8',
          'Clear failed ap on AC1',
          'Check the result')

# operate
EnterEnableMode(switch1)
SetCmd(switch1,'clear wireless ap failed',timeout=3)
SetCmd(switch1,'y',timeout=3)

IdleAfter(20)
EnterEnableMode(switch2)
#check
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[('No managed APs discovered')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 8', res1)

################################################################################
#Step 9
#
#操作
#在S3上把接AP1的端口s3p3up起来
#
#预期
#show wi ap status在AC1上可以检测到AP1被AC1成功管理
#AP1_MAC的“Status”为“Managed”,“Configuration Status”为“Success”
################################################################################

printStep(testname,'Step 9',
          'No shutdown interface s3p3 on S3',
          'Check the result')

# operate
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'no shutdown')
	
IdleAfter(20)	
EnterEnableMode(switch1)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 9', res1)

################################################################################
#Step 10
#
#操作
#在AC2上查看AP1的状态
#
#预期
#非Controller AC1会把AP的更新的信息发送给Controller AC2
#在AC2上show wireless ap status显示AP1的mac地址“AP1_MAC”的“Status”为“Managed”
#“AP1_MAC”的“Configuration Status”为“Success”
################################################################################

printStep(testname,'Step 10',
          'Check AP1 status on AC2',
          'Check the result') 

#check
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)		

#result
printCheckStep(testname,'Step 10', res1)

################################################################################
#Step 11
#
#操作
#把AC2上s2p1接口down掉
#
#预期
#集群管理的AP从managed AP database里去除
#在AC2上show wireless ap status 显示为No managed APs discovered
################################################################################

printStep(testname,'Step 11',
          'Shutdown interface s2p1 on AC2',
          'Check the result')

# operate
EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'shutdown')

IdleAfter(20)
EnterEnableMode(switch2)
#check
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[('No managed APs discovered')],
				   retry=30,interval=5,waitflag=False,IC=True)	
			   
#result
printCheckStep(testname,'Step 11', res1)

################################################################################
#Step 12
#
#操作
#把AC2上s2p1接口up
#
#预期
#在AC2上show wireless ap status显示AP1的mac地址“AP1_MAC”的“Status”为“Managed”
#“AP1_MAC”的“Configuration Status”为“Success”
################################################################################

printStep(testname,'Step 12',
          'No shutdown interface s2p1 on AC2',
          'Check the result')

# operate
EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'no shutdown')

IdleAfter(20)
EnterEnableMode(switch2)
#check
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 12', res1)

################################################################################
#Step 13
#
#操作
#在AC1上配置集群优先级3
#
#预期
#AC2上show wireless显示”Cluster Controller”为”No”
#集群管理的AP从managed AP database里去除
#在AC2上show wireless ap status 显示为No managed APs discovered
################################################################################

printStep(testname,'Step 13',
          'Set cluster-priority value as 3 on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'cluster-priority 3')

IdleAfter(30)
EnterEnableMode(switch2)
data1 = SetCmd(switch2,'show wireless')
#check1
res1 = CheckLine(data1,'Cluster Controller','No',IC=True) 

IdleAfter(20)
EnterEnableMode(switch2)
#check2
res2 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[('No managed APs discovered')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 13', res1, res2)

################################################################################
#Step 14
#
#操作
#在AC1上配置集群优先级1 
#
#预期
#在AC2上show wireless ap status显示AP1的mac地址“AP1_MAC”的“Status”为“Managed”,“Configuration Status”为“Success”
################################################################################

printStep(testname,'Step 14',
          'Set cluster-priority value as 1 on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'cluster-priority 1')

IdleAfter(20)
EnterEnableMode(switch2)
#check
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 14', res1)

################################################################################
#Step 15
#
#操作
#在AC1上把AP的认证方式修改为MAC认证,把AP1从ap database数据库中删除
#
#预期
#在AC1上用show wireless ap failure status查看认证失败AP信息，MAC Address中显示有AP1_MAC
################################################################################

printStep(testname,'Step 15',
          'Change ap authentication mac and delete the ap datebase on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no ap database',ap1mac)
SetCmd(switch1,'ap authentication mac')
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

EnterEnableMode(switch1)
#check
res1 = CheckSutCmd(switch1,'show wireless ap failure status',
				   check=[(ap1mac,'No Database Entry')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 15', res1)

################################################################################
#Step 16
#
#操作
#在AC2上show wireless ap failure status查看认证失败AP信息
#
#预期
#非Controller AC1会把AP的更新的信息发送给Controller AC2
#在AC2上用show wireless ap failure status查看认证失败AP信息,MAC Address中显示有AP1_MAC
################################################################################

printStep(testname,'Step 16',
          'Check failure ap table on AC2',
          'Check the result')

# operate
EnterEnableMode(switch1)
#check
res1 = CheckSutCmd(switch1,'show wireless ap failure status',
				   check=[(ap1mac,'No Database Entry')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 16', res1)

################################################################################
#Step 17
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 17',
          'Recover initial config')

# operate		  
#恢复AC1的配置
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery ip-list',Ap1_ipv4)
SetCmd(switch1,'no discovery ip-list',If_vlan70_s2_ipv4_s)
SetCmd(switch1,'no cluster-priority')
SetCmd(switch1,'ap authentication none')
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
SetCmd(switch1,'ap database',ap1mac)

#恢复AC2的配置
EnterWirelessMode(switch2)
SetCmd(switch2,'no cluster-priority')

EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'no shutdown')

#恢复S3的配置
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'no shutdown')

#end
printTimer(testname, 'End')