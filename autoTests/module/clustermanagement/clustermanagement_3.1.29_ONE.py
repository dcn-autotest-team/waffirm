#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.29.py - test case 3.1.29 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-16 15:59:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.29 系统控制功能
# 测试目的：测试AC的系统控制功能是否正确
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.29'

avoiderror(testname)
printTimer(testname,'Start','Test system control function of AC')

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

EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p4)
SetCmd(switch3,'shutdown')

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
#在S3把接AP1的接口s3p3down掉
#
#预期
#在AC1上可以检测到AP1不能被AC1成功管理
#AP1_MAC的“Status”为“Failed”,“Configuration Status”为“Not Config”
################################################################################

printStep(testname,'Step 2',
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
printCheckStep(testname, 'Step 2', res1)
				   
################################################################################
#Step 3
#
#操作
#把AC2的IP地址加入到AC1的三层发现ip list中
#
#预期
#在AC1上show wireless peer-switch显示有“IP Address”为“IF_VLAN70_S2_IPV4”的
################################################################################

printStep(testname,'Step 3',
          'Add AC2 ip to discovery ip list on AC1',
		  'Check the result')		  

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',If_vlan70_s2_ipv4_s)	  
		  
IdleAfter(20)
EnterEnableMode(switch1)
#check
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
				   check=[(If_vlan70_s2_ipv4_s)],
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
#在AC2上show wireless显示”Cluster Controller”为”Yes”
#在AC2上可以检测到AP1的mac地址“AP1_MAC”的“Status”为“Failed”,“Configuration Status”为“Not Config”
################################################################################

printStep(testname,'Step 4',
          'Set cluster-priority value as 2 on AC2',
          'Check the result')	  

# operate
EnterWirelessMode(switch2)
SetCmd(switch2,'no enable')
IdleAfter(1)
SetCmd(switch2,'enable')
SetCmd(switch2,'cluster-priority 2')
		  
IdleAfter(20)
EnterEnableMode(switch2)
#check
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[(ap1mac,'Failed','Not Config')],
				   retry=30,interval=5,waitflag=False,IC=True)
			   
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#在AC1上开启集群debug
#在AC2上删除状态为failed的AP1
#
#预期
#在AC1上不能查看到MAC地址为“AP1_MAC”的AP
################################################################################

printStep(testname,'Step 5',
          'Delete the failed AP on AC2',
          'Check the result')

# operate
EnterEnableMode(switch1)
SetCmd(switch1,'debug wireless cluster packet all')  

EnterEnableMode(switch2)
SetCmd(switch2,'clear wireless ap failed',ap1mac,timeout=3)
SetCmd(switch2,'y',timeout=3)
	
#check
res1 = CheckSutCmdWithNoExpect(switch1,'show wireless ap status',
                               check=[(ap1mac)],
                               retry=30,interval=5,waitflag=False,IC=True)
				   
#result
printCheckStep(testname,'Step 5', res1)

################################################################################
#Step 6
#
#操作
#在S3把接AC2的接口s3p2 down掉
#在S3把接AP1的接口s3p3 up起来
#
#预期
#在AC1上show wi ap status可以检测到AP1被AC1成功管理
#AP1_MAC的“Status”为“Managed”,“Configuration Status”为“Success”
################################################################################

printStep(testname,'Step 6',
          'No shutdown interface s3p3 and shutdown interface s3p2 on S3',
          'Check the result')

# operate
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p2)
SetCmd(switch3,'shutdown')

EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'no shutdown')
	
IdleAfter(30)
EnterEnableMode(switch1)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname,'Step 6', res1)

################################################################################
#Step 7
#
#操作
#在S3把接AC2的接口s3p2 up起来
#
#预期
#在AC1上show wireless peer-switch显示有“IP Address”为“IF_VLAN70_S2_IPV4”的
################################################################################

printStep(testname,'Step 7',
          'No shutdown interface s3p2 on S3',
          'Check the result')

# operate
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p2)
SetCmd(switch3,'no shutdown')
	
IdleAfter(30)
EnterEnableMode(switch1)
#check
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
				   check=[(If_vlan70_s2_ipv4_s)],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname,'Step 7', res1)

################################################################################
#Step 8
#
#操作
#在S3把接AP1的接口s3p3 down掉
#
#预期
#在AC1上可以检测到在AC1发向集群交换机的“Peer AP remove notification sent to peer switch”报文
################################################################################

printStep(testname,'Step 8',
          'Check the AP remove notification on AC1',
          'Check the result')

# operate
StartDebug(switch1)

EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'shutdown')

IdleAfter(120)
data1 = StopDebug(switch1)
#check
res1 = CheckLine(data1,'Peer AP remove notification sent to peer switch',IC=True)
	
#result
printCheckStep(testname,'Step 8', res1)

################################################################################
#Step 9
#
#操作
#在S3把接AP1的接口s3p3 up起来
#
#预期
#在AC1上可以检测到在AC1发向集群交换机的“Peer AP discover notification sent to peer switch”报文
################################################################################

printStep(testname,'Step 9',
          'Check the AP discover notification on AC1',
          'Check the result')

# operate
StartDebug(switch1)

EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'no shutdown')

IdleAfter(120)
data1 = StopDebug(switch1)
#check
res1 = CheckLine(data1,'Peer AP discover notification sent to peer switch',IC=True)
	
#result
printCheckStep(testname,'Step 9', res1)

################################################################################
#Step 10
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 10',
          'Recover initial config')

# operate	
#恢复AC2的配置
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery vlan-list 1')
SetCmd(switch2,'no cluster-priority')
	
#配置AC1的vlan list
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list',Vlan70)
SetCmd(switch1,'no discovery ip-list',If_vlan70_s2_ipv4_s)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

#恢复S3的配置
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p4)
SetCmd(switch3,'no shutdown')
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'no shutdown')
SetCmd(switch3,'interface',s3p2)
SetCmd(switch3,'no shutdown')

#关闭AC1调试
EnterEnableMode(switch1)
SetCmd(switch1,'no debug wireless cluster packet all')

#end
printTimer(testname, 'End')