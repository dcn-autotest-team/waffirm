#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.28.py - test case 3.1.28 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-16 15:06:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.28 AC对AC Controllor与AP之间消息的中继
# 测试目的：测试AC对AC Controllor与AP之间消息的中继功能是否正常
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.28'

avoiderror(testname)
printTimer(testname,'Start','Test AC relay message between AC Controllor and AP')

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

IdleAfter(20)
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
#在AC1上开启消息传输debug开关
#在AC2上配置集群优先级2 
#
#预期
#AC2上show wireless显示”Cluster Controller”为”Yes”
################################################################################

printStep(testname,'Step 3',
          'Set cluster-priority value as 2 on AC2',
		  'Check the result')		  

# operate
EnterEnableMode(switch1)
SetCmd(switch1,'debug wireless cluster packet all')	

EnterWirelessMode(switch2)
SetCmd(switch2,'cluster-priority 2')	  
		  
IdleAfter(20)
data1 =SetCmd(switch2,'show wireless')
#check1
res1 = CheckLine(data1,'Cluster Controller','Yes',IC=True)
		   
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
#在AC2上查看AP的状态
#
#预期
#在AC2上show wireless ap status显示AP1的mac地址“AP1_MAC”的“Status”为“Managed”,“Configuration Status”为“Success”
################################################################################

printStep(testname,'Step 4',
          'Check AP status on AC2',
          'Check the result')	  

# operate		  
IdleAfter(20)

#check
res1 = CheckSutCmd(switch2,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
			   
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#在AC2上重启AP1
#
#预期
#在AC1上能检测到”Rxd WS_AP_RESET_MSG Message from cluster controller IF_VLAN70_S2_IPV4 for forwarding” 
#在AC2上show wireless ap status显示AP1的mac地址“AP1_MAC”的“Status”为“Managed”,“Configuration Status”为“Success”
################################################################################

printStep(testname,'Step 5',
          'Reboot AP1 on AC2',
          'Check the result')

# operate
StartDebug(switch1)

EnterEnableMode(switch2)
RebootAp(Type='AC',connectTime=1,AP=ap1,AC=switch2,MAC=ap1mac) 

IdleAfter(180)
data1 = StopDebug(switch1)	
#check
res1 = CheckLine(data1,'Rxd WS_AP_RESET_MSG Message from cluster controller '+If_vlan70_s2_ipv4_s+' for forwarding',IC=True)
	
IdleAfter(20)
EnterEnableMode(switch2)
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
#把AP1的管理vlan vlan70从AC1的vlan list中删除
#在AC2上配置AP1的自动部署信息,primary地址设置为IF_VLAN70_S2_IPV4
#
#预期
#在AC1上能检测到”send ap discover ack msg to peer switch: IF_VLAN70_S2_IPV4”
################################################################################

printStep(testname,'Step 6',
          'Config ap provision on AP1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list',Vlan70)
StartDebug(switch1)

EnterEnableMode(switch2)
SetCmd(switch2,'wireless ap provision',ap1mac,'switch primary',If_vlan70_s2_ipv4_s)
SetCmd(switch2,'wireless ap provision start')

IdleAfter(20)
RebootAp(Type='AC',connectTime=1,AP=ap1,AC=switch2,MAC=ap1mac)

IdleAfter(180)
data1 = StopDebug(switch1)
#check	
res1 = CheckLine(data1,'send ap discover ack msg to peer switch: '+If_vlan70_s2_ipv4_s,IC=True)
		
#result
printCheckStep(testname,'Step 6', res1)

################################################################################
#Step 7
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 7',
          'Recover initial config')

# operate
#恢复AC2的配置
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery vlan-list 1')
SetCmd(switch2,'no cluster-priority')
		  
#恢复AC1的配置
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list',Vlan70)
SetCmd(switch1,'no discovery ip-list',If_vlan70_s2_ipv4_s)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

EnterEnableMode(switch1)
SetCmd(switch1,'no debug wireless cluster packet all')

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

#end
printTimer(testname, 'End')