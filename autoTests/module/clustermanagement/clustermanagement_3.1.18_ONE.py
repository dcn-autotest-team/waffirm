#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.18.py - test case 3.1.18 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-4 11:06:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.18 自动选举controller功能测试
# 测试目的：测试自动选举controller功能测试是否正常
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.18'

avoiderror(testname)
printTimer(testname,'Start','Test AC automatic elect controller')

################################################################################
#Step 1
#
#操作
#把AP1的管理vlan vlan70加入到AC1的vlan list中
#
#预期
#AP1被AC1成功管理,AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 1',
          'Add management vlan to discovery vlan list on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery vlan-list',Vlan70)
	
IdleAfter(20)
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
#把AP1的管理vlan vlan70加入到AC2的vlan list中
#
#预期
#AC1上show wireless peer-switch显示有:
#“IP Address”为“IF_VLAN70_S2_IPV4”的,“Disc. Reason”显示为“L2 Poll”
################################################################################

printStep(testname,'Step 2',
          'Add management vlan to discovery vlan list on AC2',
          'Check the result')

# operate
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery vlan-list',Vlan70)
		  
IdleAfter(20)
#check
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
				   check=[(If_vlan70_s2_ipv4_s,'L2 Poll')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
#在AC1上查看AC1的自动选举相关信息
#
#预期
#在AC1上用show wireless显示有:
#Cluster Priority为1,Cluster Controller为Yes,Peer Group ID为1
################################################################################

printStep(testname,'Step 3',
          'Check the cluster controller on AC1 1',
		  'Check the result')		  

# operate	
IdleAfter(20)
data1 = SetCmd(switch1,'show wireless')
#check
res1 = CheckLineList(data1,[('Peer Group ID','1'),('Cluster Priority','1'),
                     ('Cluster Controller','Yes')],IC=True)
						
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
#在AC1上修改AC1的优先级为2
#
#预期
#在AC1上用show wireless显示Cluster Priority为2
################################################################################

printStep(testname,'Step 4',
          'Change the cluster priority on AC1',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'cluster-priority 2')

IdleAfter(20)
data1 = SetCmd(switch1,'show wireless')
#check
res1 = CheckLine(data1,'Cluster Priority','2',IC=True)
	
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#在AC2上修改AC2的优先级为3
#
#预期
#AC2被选举为Cluster Controller,在AC1上用show wireless显示Cluster Controller为No
################################################################################

printStep(testname,'Step 5',
          'Change the cluster priority on AC2',
          'Check the result')

# operate		  
EnterWirelessMode(switch2)
SetCmd(switch2,'cluster-priority 3')

IdleAfter(20)
data1 = SetCmd(switch1,'show wireless')
#check
res1 = CheckLine(data1,'Cluster Controller','No',IC=True)
	
#result
printCheckStep(testname,'Step 5', res1)

################################################################################
#Step 6
#
#操作
#在AC1和AC2上恢复优先级为默认值
#
#预期
#在AC2上用show wireless显示Cluster Priority为1
#AC1被选举为Cluster Controller,用show wireless显示 Cluster Controller为Yes
################################################################################

printStep(testname,'Step 6',
          'Change the cluster priority with default value on AC1 and AC2',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'no cluster-priority')

EnterWirelessMode(switch2)
SetCmd(switch2,'no cluster-priority')

IdleAfter(20)
data1 = SetCmd(switch2,'show wireless')
#check1
res1 = CheckLine(data1,'Cluster Priority','1',IC=True)

data2 = SetCmd(switch1,'show wireless')
#check2
res2 = CheckLine(data2,'Cluster Controller','Yes',IC=True)

#result
printCheckStep(testname,'Step 6', res1, res2)

################################################################################
#Step 7
#
#操作
#修改vlan70的接口IP为IF_VLAN70_S1_BACKIPV4,使IF_VLAN70_S1_BACKIPV4>IF_VLAN70_S2_IPV4
#
#预期
#等待60s,AC2被选举为Cluster Controller,在AC2上用show wireless显示 Cluster Controller为Yes
################################################################################

printStep(testname,'Step 7',
          'Change AC1 ip index greater than AC2 ip index',
          'Check the result')

# operate		  
EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan70)
SetCmd(switch1,'ip address',If_vlan70_s1_backipv4)

EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip',If_vlan70_s1_backipv4_s)

IdleAfter(30)
#check
res1 = CheckSutCmd(switch2,'show wireless',
				   check=[('Cluster Controller','Yes')],
				   retry=30,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname,'Step 7', res1)

################################################################################
#Step 8
#
#操作
#在AC2上修改AC2的优先级为0
#
#预期
#AC2将不参加选举,在AC1上用show wireless显示 Cluster Controller为Yes
################################################################################

printStep(testname,'Step 8',
          'Change the cluster priority with 0 on AC2',
          'Check the result')

# operate		  
EnterWirelessMode(switch2)
SetCmd(switch2,'cluster-priority 0')

IdleAfter(20)
data1 = SetCmd(switch1,'show wireless')
#check
res1 = CheckLine(data1,'Cluster Controller','Yes',IC=True)
	
#result
printCheckStep(testname,'Step 8', res1)

################################################################################
#Step 9
#
#操作
#在AC2上修改AC2的优先级为3
#
#预期
#AC2被选举为Cluster Controller,在AC2上用show wireless显示Cluster Controller为Yes
################################################################################

printStep(testname,'Step 9',
          'Change the cluster priority with 3 on AC2',
          'Check the result')

# operate		  
EnterWirelessMode(switch2)
SetCmd(switch2,'cluster-priority 3')

IdleAfter(20)
data1 = SetCmd(switch2,'show wireless')
#check
res1 = CheckLine(data1,'Cluster Controller','Yes',IC=True)
	
#result
printCheckStep(testname,'Step 9', res1)

################################################################################
#Step 10
#
#操作
#在AC2上修改AC2加入组2
#
#预期
#在AC1上用show wireless显示 Cluster Controller为Yes,Peer Group ID显示为1
#在AC2上用show wireless显示 Cluster Controller为Yes,Peer Group ID显示为2
################################################################################

printStep(testname,'Step 10',
          'Change peer group value on AC2',
          'Check the result')

# operate		  
EnterWirelessMode(switch2)
SetCmd(switch2,'peer-group 2')

IdleAfter(60)
data1 = SetCmd(switch1,'show wireless')
#check1
res1 = CheckLineList(data1,[('Peer Group ID','1'),
                     ('Cluster Controller','Yes')],IC=True)
					 
data2 = SetCmd(switch2,'show wireless')
#check2
res2 = CheckLineList(data2,[('Peer Group ID','2'),
                     ('Cluster Controller','Yes')],IC=True)
	
#result
printCheckStep(testname,'Step 10', res1, res2)

################################################################################
#Step 11
#
#操作
#在AC2上恢复AC2为默认组
#
#预期
#在AC1上用show wireless显示 Cluster Controller为No,Peer Group ID显示为1
#在AC2上用show wireless显示 Cluster Controller为Yes,Peer Group ID显示为1
################################################################################

printStep(testname,'Step 11',
          'Change peer group with default value on AC2',
          'Check the result')

# operate		  
EnterWirelessMode(switch2)
SetCmd(switch2,'no peer-group')

IdleAfter(60)
data1 = SetCmd(switch1,'show wireless')
#check1
res1 = CheckLineList(data1,[('Peer Group ID','1'),('Cluster Controller','No')],IC=True)
					 
data2 = SetCmd(switch2,'show wireless')
#check2
res2 = CheckLineList(data2,[('Peer Group ID','1'),('Cluster Controller','Yes')],IC=True)
	
#result
printCheckStep(testname,'Step 11', res1, res2)

################################################################################
#Step 12
#
#操作
#在AC2上关闭无线特性
#
#预期
#在AC1上用show wireless显示Cluster Controller为Yes,Peer Group ID显示为1
################################################################################

printStep(testname,'Step 12',
          'Close the wireless on AC2',
          'Check the result')

# operate		  
EnterWirelessMode(switch2)
SetCmd(switch2,'no enable')

IdleAfter(60)
data1 = SetCmd(switch1,'show wireless')
#check1
res1 = CheckLineList(data1,[('Peer Group ID','1'),('Cluster Controller','Yes')],IC=True)
	
#result
printCheckStep(testname,'Step 12', res1)

################################################################################
#Step 13
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 13',
          'Recover initial config')

# operate		  
#恢复AC1的配置
EnterWirelessMode(switch1)
SetCmd(switch1,'no peer-group')
SetCmd(switch1,'no cluster-priority')
SetCmd(switch1,'no discovery vlan-list',Vlan70)

#恢复AC2的配置
EnterWirelessMode(switch2)
SetCmd(switch2,'no peer-group')
SetCmd(switch2,'no cluster-priority')
SetCmd(switch2,'no discovery vlan-list',Vlan70)
SetCmd(switch2,'no enable')
IdleAfter(1)
SetCmd(switch2,'enable')

#AC1上配置Vlan和静态IP	
EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan70)
SetCmd(switch1,'ip address',If_vlan70_s1_ipv4)

EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip',If_vlan70_s1_ipv4_s)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
	
#end
printTimer(testname, 'End')