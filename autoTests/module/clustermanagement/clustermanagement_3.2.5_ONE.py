#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.2.5.py - test case 3.2.5 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-01-18 13:45:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.2.5 AC通过ip list列表进行主动发现AP(IPV6)
# 测试目的：测试AC通过ipv6 list列表进行主动发现功能是否正常
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.2.5'

avoiderror(testname)
printTimer(testname,'Start','Test AC active discovery AP through ip list')

################################################################################
#Step 1
#
#操作
# AC1的ip list发现功能默认为开启状态,不添加ip地址到ip list列表中,开启debug wireless discovery packet
#
#预期
# 当ip list列表为空时,开始ip list发现功能,不会有ip discovery发出来
# 等待60s,在AC1上不能检测到如下提示报文：udp discovery msg sent to peer
################################################################################

printStep(testname,'Step 1',
          'Check the wireless discovery packet with default config',
          'Check the result')

# operate	
exec(compile(open('clustermanagement\\clustermanagement_initial(ipv6).py', "rb").read(), 'clustermanagement\\clustermanagement_initial(ipv6).py', 'exec'))
	  
EnterEnableMode(switch1)
StartDebug(switch1)
SetCmd(switch1,'debug wireless discovery packet all')

IdleAfter(60)
data1 = StopDebug(switch1)

#check
res1 = CheckLine(data1,'udp discovery msg sent to peer',IC=True)
res1 = 0 if res1 != 0 else 1
	
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
# 关闭vlan list二层主动发现功能,在ip list中添加一个未建立tls连接的ip 地址
#
#预期
# 等待60s，在AC1上可以检测到如下提示报文：Error udp send to peer:2002:10::1.
################################################################################

printStep(testname,'Step 2',
          'Add an ip address that does not establish a TLS connection in ip list',
          'Check the result')

# operate	
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery method l2-multicast')
SetCmd(switch1,'discovery ipv6-list 2002:10::1')

EnterEnableMode(switch1)
StartDebug(switch1)
SetCmd(switch1,'debug wireless discovery packet all')
IdleAfter(60)
data1 = StopDebug(switch1)

#check
res1 = CheckLine(data1,'Error udp send to peer:2002:10::1.',IC=True)
	
#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
# 在ip list中添加一个未建立连接的AP1的IP地址
#
#预期
# 在AC1上可以检测到如下提示报文:udp discovery msg sent to peer: AP1_IPV6
################################################################################

printStep(testname,'Step 3',
          'Check the message on AC1 after add an AP1 ip into the discovery ip list',
		  'Check the result')		  

# operate
EnterEnableMode(switch1)
StartDebug(switch1)
SetCmd(switch1,'debug wireless discovery packet all')

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ipv6-list',Ap1_ipv6)
IdleAfter(60)
data1 = StopDebug(switch1)

#check
res1 = CheckLine(data1,'udp discovery msg sent to peer:'+Ap1_ipv6,IC=True)
	
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#在AC1上查看AP1的状态
#
#预期
# 等待60s,show wireless ap status在AC1上可以检测到AP1被AC1成功管理
# AP1_MAC的“Status”为“Managed Success”
# 等待60s，在AC1上不能检测到如下提示报文：
# udp discovery msg sent to peer: AP1_IPV6
################################################################################

printStep(testname,'Step 4',
          'Check the AP1 status on AC1 1 and the message on AC1',
          'Check the result')

#check1
res1 = CheckSutCmd(switch1,'show wireless ap status',
		check=[(ap1mac,'Managed','Success')],
		retry=30,interval=5,waitflag=False,IC=True)

EnterEnableMode(switch1)
StartDebug(switch1)
SetCmd(switch1,'debug wireless discovery packet all')

IdleAfter(60)
data1 = StopDebug(switch1)

#check2
res2 = CheckLine(data1,'udp discovery msg sent to peer:'+Ap1_ipv6,IC=True)
res2 = 0 if res2 != 0 else 1
	
#result
printCheckStep(testname,'Step 4', res1, res2)

################################################################################
#Step 5
#
#操作
#在AC1上关闭ip list主动发现功能
#
#预期
#等待30s,在AC1上不能检测到如下提示报文：
#udp discovery msg sent to peer:1.1.1.1;Error udp send to peer:2002:10::1
################################################################################

printStep(testname,'Step 5',
          'Close the discovery ip list method',
          'Check the result')

# operate		
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery method ip-poll')
IdleAfter(5)
EnterEnableMode(switch1)
StartDebug(switch1)
SetCmd(switch1,'debug wireless discovery packet all')

IdleAfter(60)
data1 = StopDebug(switch1)

#check
res1 = CheckLine(data1,'Error udp send to peer:2002:10::1',IC=True)
res1 = 0 if res1 != 0 else 1
	
#result
printCheckStep(testname,'Step 5', res1)

################################################################################
#Step 6
#
#操作
#在AC1上重启无线功能
#
#预期
#重启后AP1无法被AC1管理。show wireless ap status显示No managed APs discovered
################################################################################

printStep(testname,'Step 6',
          'Reboot the wireless',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
IdleAfter(30)

#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[('No managed APs discovered')],
				   retry=30,interval=5,waitflag=False,IC=True)	
#result
printCheckStep(testname, 'Step 6', res1)

################################################################################
#Step 7
#
#操作
#在AC1上开启ip list主动发现功能
#
#预期
#等待60s，在AC1上可以检测到如下提示报文：udp discovery msg sent to peer: AP1_IPV6
#等待60s，show wireless ap status在AC1上可以检测到AP1被AC1成功管理
#AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 7',
          'Check the AP1 status on AC1 after Open the discovery ip list method',
          'Check the result')

# operate
EnterEnableMode(switch1)
StartDebug(switch1)
SetCmd(switch1,'debug wireless discovery packet all')
		  
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery method ip-poll')
IdleAfter(60)
data1 = StopDebug(switch1)

#check1
res1 = CheckLine(data1,'udp discovery msg sent to peer:'+Ap1_ipv6,IC=True)
#check2
res2 = CheckSutCmd(switch1,'show wireless ap status',
					check=[(ap1mac,'Managed','Success')],
					retry=30,interval=5,waitflag=False,IC=True)
		
#result
printCheckStep(testname, 'Step 7', res1, res2)

################################################################################
#Step 8
#
#操作
#在AC1上删除ip list中AP1的IPv6
#
#预期
#重启后AP1无法被AC1管理
#show wireless ap status显示No managed APs discovered
################################################################################

printStep(testname,'Step 8',
          'Delete AP1 ip form discovery ip list and reboot the wireless',
          'Check the result')

# operate		
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery ipv6-list',Ap1_ipv6)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
IdleAfter(40)

#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[('No managed APs discovered')],
				   retry=5,interval=5,waitflag=False,IC=True)	
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
SetCmd(switch1,'no discovery ipv6-list 2002:10::1')
SetCmd(switch1,'no discovery ipv6-list',Ap1_ipv6)

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery method l2-multicast')
SetCmd(switch1,'discovery method ip-poll')

EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
	
EnterEnableMode(switch1)
SetCmd(switch1,'no debug wireless discovery packet all')

exec(compile(open('clustermanagement\\clustermanagement_unitial(ipv6).py', "rb").read(), 'clustermanagement\\clustermanagement_unitial(ipv6).py', 'exec'))
#end
printTimer(testname, 'End')