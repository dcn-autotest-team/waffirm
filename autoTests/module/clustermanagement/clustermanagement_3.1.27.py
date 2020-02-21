#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.27.py - test case 3.1.27 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-16 13:31:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.27 Radio,VAP信息和通过认证的client信息的收集和处理
# 测试目的：测试Radio,VAP信息和通过认证的client信息的收集和处理功能是否正常
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.27'

avoiderror(testname)
printTimer(testname,'Start','Test collection and disposal of Radio,VAP and client information')

################################################################################
#Step 1
#
#操作
#把AP1的管理vlan vlan70加入到AC1的vlan list中
#
#预期
#show wi ap status在AC1上可以检测到AP1被AC1成功管理
#AP1_MAC的“Status”为“Managed”,“Configuration Status”为“Success”
################################################################################

printStep(testname,'Step 1',
          'Add management vlan to discovery vlan list on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch2)
SetCmd(switch2,'no discovery vlan-list 1')

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery vlan-list',Vlan70)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

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
#在AC1上show wireless peer-switch显示有“IP Address”为“IF_VLAN70_S2_IPV4”
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
				   check=[(If_vlan70_s2_ipv4_s)],
				   retry=30,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
#在AC1上开启消息传输debug开关
#在AC2上配置集群优先级2 
#
#预期
#AC2上show wireless显示”Cluster Controller”为”Yes”
#在AC1上可以看到AC1发送”Cluster-Radio-VAP-Status”打印给新的Cluster Controller AC2
################################################################################

printStep(testname,'Step 3',
          'Set cluster-priority value as 2 on AC2',
		  'Check the result')		  

# operate
EnterEnableMode(switch1)
StartDebug(switch1)
SetCmd(switch1,'debug wireless cluster packet all')	

EnterWirelessMode(switch2)
SetCmd(switch2,'cluster-priority 2')	  
		  
IdleAfter(180)
data1 = StopDebug(switch1)

#check1
res1 = CheckLine(data1,'Cluster-Radio-VAP-Status',IC=True)

#check2	
res2 = CheckSutCmd(switch2,'show wireless',
				   check=[('Cluster Controller','Yes')],
				   retry=5,interval=5,waitflag=False,IC=True)	   
#result
printCheckStep(testname, 'Step 3', res1, res2)

################################################################################
#Step 4
#
#操作
#在AC1上把AP1的channel设置成3信道
#
#预期
#在AC1上可以看到AC1发送” Cluster-Radio-VAP-Status”打印给Cluster Controller AC2
################################################################################

printStep(testname,'Step 4',
          'Check Cluster-Radio-VAP-Status on AC1',
          'Check the result')

# operate
EnterEnableMode(switch1)
StartDebug(switch1)
SetCmd(switch1,'wireless ap channel set',ap1mac,'radio 1 3')

IdleAfter(180)
data1 = StopDebug(switch1)
#check
res1 = CheckLine(data1,'Cluster-Radio-VAP-Status',IC=True)
			   
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#在AC1上把AP1的认证方式改为mac认证
#
#预期
#当AP1通过认证后在AC1上可以看到AC1发送”Cluster-Radio-VAP-Status”打印给Cluster Controller AC2
################################################################################

printStep(testname,'Step 5',
          'Change ap authentication mac',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap authentication mac')
SetCmd(switch1,'no enable')
SetCmd(switch1,'enable')		  
		
EnterEnableMode(switch1)		
StartDebug(switch1)
SetCmd(switch1,'debug wireless cluster packet all')		  
		  
IdleAfter(180)
data1 = StopDebug(switch1)
#check
res1 = CheckLine(data1,'Cluster-Radio-VAP-Status',IC=True)
	
#result
printCheckStep(testname,'Step 5', res1)

################################################################################
#Step 6
#
#操作
#在S3上配置vlan,vlan70和vlan80接口IP，并配置STA地址池
#
#预期
#在AC1上显示MAC Address为STA1_MAC
#在AC2上显示MAC Address为STA1_MAC
################################################################################

printStep(testname,'Step 6',
          'Config sta1 connect ap1',
          'Check the result')

# operate
EnterConfigMode(switch3)
SetCmd(switch3,'interface vlan',Vlan70)
SetCmd(switch3,'ip address',If_vlan70_s3_ipv4)
EnterConfigMode(switch3)
SetCmd(switch3,'interface vlan',Vlan80)
SetCmd(switch3,'ip address',If_vlan80_s3_ipv4)

EnterConfigMode(switch3)
SetCmd(switch3,'ip dhcp pool STA')
SetCmd(switch3,'network-address',Dhcp_sta_pool_ipv4)
SetCmd(switch3,'default-router',If_vlan80_s3_ipv4_s)

EnterConfigMode(switch3)
SetCmd(switch3,'no service dhcp')
SetCmd(switch3,'service dhcp')

WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='open')

#check1
res1 = CheckSutCmd(switch1,'show wireless client summary',
				   check=[(sta1mac)],
				   retry=30,interval=5,waitflag=False,IC=True)	
				   
#check2
res2 = CheckSutCmd(switch2,'show wireless client summary',
				   check=[(sta1mac)],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 6', res1, res2)

################################################################################
#Step 7
#
#操作
#在AC2上配置集群优先级1
#
#预期
#当有新的controllerAC1被选出来后,AC2会删除sta1的相信息
#在AC2上用show wireless client summary查看sta1相关信息显示为“No clients associated to Aps”
################################################################################

printStep(testname,'Step 7',
          'Set cluster-priority value as 1 on AC2',
          'Check the result')	  

# operate
EnterWirelessMode(switch2)
SetCmd(switch2,'cluster-priority 1')		  
		  
IdleAfter(20)		  
#check1
res1 = CheckSutCmd(switch2,'show wireless client summary',
				   check=[('No clients associated to Aps')],
				   retry=30,interval=5,waitflag=False,IC=True)	
	
#result
printCheckStep(testname,'Step 7', res1)

################################################################################
#Step 8
#
#操作
#在AC2上配置集群优先级为2
#
#预期
#在AC2上显示MAC Address为STA1_MAC
################################################################################

printStep(testname,'Step 8',
          'Set cluster-priority value as 2 on AC2',
          'Check the result')

# operate
EnterEnableMode(switch1)
SetCmd(switch1,'debug wireless cluster packet all')

EnterWirelessMode(switch2)
SetCmd(switch2,'cluster-priority 2')

IdleAfter(20)
EnterEnableMode(switch2)
#check
res1 = CheckSutCmd(switch2,'show wireless client summary',
				   check=[(sta1mac)],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 8', res1)

################################################################################
#Step 9
#
#操作
#把AC2上s2p1接口down掉
#
#预期
#AC2会删除sta1的相信息
#在AC2上用show wireless client summary查看sta1相关信息显示为“No clients associated to Aps”
################################################################################

printStep(testname,'Step 9',
          'Shutdown interface s2p1 on AC2',
          'Check the result')

# operate
EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'shutdown')

EnterEnableMode(switch2)	
IdleAfter(20)	
#check
res1 = CheckSutCmd(switch2,'show wireless client summary',
				   check=[('No clients associated to Aps')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 9', res1)

################################################################################
#Step 10
#
#操作
#把AC2上s2p1接口up
#
#预期
#在AC2上显示MAC Address为STA1_MAC
################################################################################

printStep(testname,'Step 10',
          'No shutdown interface s2p1 on AC2',
          'Check the result') 

# operate
EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'no shutdown')
		  
IdleAfter(20)
EnterEnableMode(switch2)
#check
res1 = CheckSutCmd(switch2,'show wireless client summary',
				   check=[(sta1mac)],
				   retry=30,interval=5,waitflag=False,IC=True)		

#result
printCheckStep(testname,'Step 10', res1)

################################################################################
#Step 11
#
#操作
#Sta1从AP1上断开，在AC1上查看sta1相关信息
#
#预期
#在AC1上显示No clients associated to Aps
#在AC2上查看sta1相关信息显示No clients associated to Aps
################################################################################

printStep(testname,'Step 11',
          'Config sta1 disconnect ap1',
          'Check the result')

# operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

EnterEnableMode(switch1)
IdleAfter(20)
#check1
res1 = CheckSutCmd(switch1,'show wireless client summary',
				   check=[('No clients associated to Aps')],
				   retry=30,interval=5,waitflag=False,IC=True)	
				   
EnterEnableMode(switch2)
#check2
res2 = CheckSutCmd(switch2,'show wireless client summary',
				   check=[('No clients associated to Aps')],
				   retry=30,interval=5,waitflag=False,IC=True)	
			   
#result
printCheckStep(testname,'Step 11', res1, res2)

################################################################################
#Step 12
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 12',
          'Recover initial config')

# operate		  
#恢复AC1的配置
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list',Vlan70)
SetCmd(switch1,'no discovery ip-list',If_vlan70_s2_ipv4_s)
SetCmd(switch1,'ap authentication none')
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

EnterEnableMode(switch1)
SetCmd(switch1,'no debug wireless cluster packet all')

#恢复AC2的配置
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery vlan-list 1')
SetCmd(switch2,'no cluster-priority')

EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'no shutdown')

#end
printTimer(testname, 'End')