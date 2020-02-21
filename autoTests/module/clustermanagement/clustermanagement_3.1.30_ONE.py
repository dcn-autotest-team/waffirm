#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.30.py - test case 3.1.30 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-16 16:50:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.30 AP Troubleshooting功能测试
# 测试目的：测试AP Troubleshooting功能是否正常
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.30'

avoiderror(testname)
printTimer(testname,'Start','Test AC Troubleshooting function')

################################################################################
#Step 1
#
#操作
#把AP1的管理vlan vlan70加入到AC1的vlan list中
#
#预期
#show wi ap status在AC1上可以检测到AP1和AP2被AC1成功管理
#AP1_MAC的“Status”为“Managed Success”
#AP2_MAC的“Status”为“Managed Success”
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
				   check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
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

IdleAfter(20)
EnterEnableMode(switch1)
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
#在AC1上关闭AP1的Troubleshooting功能
#
#预期
#在AC1上检测提示“telnet: Unable to connect to remote host, err -111”
################################################################################

printStep(testname,'Step 3',
          'Close AP1 troubleshooting on AC1',
		  'Check the result')		  

# operate
EnterEnableMode(switch1)
SetCmd(switch1,'no wireless ap debug',ap1mac)	  
		  
IdleAfter(5)
data1 = SetCmd(switch1,'telnet',Ap1_ipv4)
#check
res1 = CheckLine(data1,'telnet: Unable to connect to remote host, err -111',IC=True)
		   
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
#在AC1上telnet到AP2
#
#预期
#在AC1上检测提示“login:”
################################################################################

printStep(testname,'Step 4',
          'Check troubleshooting on AP2',
          'Check the result')	  

# operate
IdleAfter(5)
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'telnet',Ap2_ipv4)
#check
res1 = CheckLine(data1,'login:',IC=True)
			   
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#在AC1上开启AP1的Troubleshooting功能
#在AC1上telnet到AP1
#
#预期
#在AC1上检测提示“login:”
################################################################################

printStep(testname,'Step 5',
          'Open AP1 troubleshooting on AC1',
          'Check the result')

# operate
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap debug',ap1mac,'admin')  
	
IdleAfter(5)
data1 = SetCmd(switch1,'telnet',Ap1_ipv4)
#check
res1 = CheckLine(data1,'login:',IC=True)
				   
#result
printCheckStep(testname,'Step 5', res1)

################################################################################
#Step 6
#
#操作
#在AC2修改AC2优先级为2
#
#预期
#AC2选举为Cluster Controller,在AC2用show wireless显示 Cluster Controller为Yes
################################################################################

printStep(testname,'Step 6',
          'Set cluster-priority value as 2 on AC2',
          'Check the result')

# operate
EnterWirelessMode(switch2)
SetCmd(switch2,'cluster-priority 2')
IdleAfter(20)

#check
res1 = CheckSutCmd(switch2,'show wireless',
				   check=[('Cluster Controller','Yes')],
				   retry=6,interval=5,waitflag=False,IC=True)
#result
printCheckStep(testname,'Step 6', res1)

################################################################################
#Step 7
#
#操作
#在AC2关闭AP1的Troubleshooting功能
#
#预期
#在AC2上检测提示“telnet: Unable to connect to remote host, err -111”
################################################################################

printStep(testname,'Step 7',
          'Close AP1 troubleshooting on AC2',
          'Check the result')

# operate		  
IdleAfter(30)
EnterEnableMode(switch2)
SetCmd(switch2,'no wireless ap debug',ap1mac)

IdleAfter(5)
data1 = SetCmd(switch2,'telnet',Ap1_ipv4)
#check
res1 = CheckLine(data1,'telnet: Unable to connect to remote host, err -111',IC=True)
	
#result
printCheckStep(testname,'Step 7', res1)

################################################################################
#Step 8
#
#操作
#在AC1上telnet到AP
#
#预期
#在AC1上检测提示“telnet: Unable to connect to remote host, err -111”
################################################################################

printStep(testname,'Step 8',
          'Check troubleshooting on AP1',
          'Check the result')

# operate
IdleAfter(5)
data1 = SetCmd(switch1,'telnet',Ap1_ipv4)
#check
res1 = CheckLine(data1,'telnet: Unable to connect to remote host, err -111',IC=True)	
	
#result
printCheckStep(testname,'Step 8', res1)

################################################################################
#Step 9
#
#操作
#在AC2上开启AP1的Troubleshooting功能
#在AC2上telnet到AP1
#
#预期
#在AC2上检测提示“login:”
################################################################################

printStep(testname,'Step 9',
          'Open AP1 troubleshooting on AC2',
          'Check the result')

# operate
EnterEnableMode(switch2)
SetCmd(switch2,'wireless ap debug',ap1mac,'admin')

IdleAfter(5)
EnterEnableMode(switch2)
data1 = SetCmd(switch2,'telnet',Ap1_ipv4)
#check
res1 = CheckLine(data1,'login:',IC=True)	

#result
printCheckStep(testname,'Step 9', res1)

################################################################################
#Step 10
#
#操作
#在AC1上telnet到AP1
#
#预期
#在AC1上检测提示“login:”
################################################################################

printStep(testname,'Step 10',
          'Check troubleshooting on AP1',
          'Check the result')

# operate
IdleAfter(5)
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'telnet',Ap1_ipv4)
#check
res1 = CheckLine(data1,'login:',IC=True)	

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
#配置AC2的vlan list
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery vlan-list 1')
SetCmd(switch2,'no cluster-priority')
SetCmd(switch2,'no enable')
IdleAfter(1)
SetCmd(switch2,'enable')
		  
#恢复AC1的配置
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list',Vlan70)
SetCmd(switch1,'no discovery ip-list',If_vlan70_s2_ipv4_s)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap debug',ap1mac,'admin')

#AC2操作
EnterEnableMode(switch2)
SetCmd(switch2,'wireless ap debug',ap1mac,'admin')

#end
printTimer(testname, 'End')