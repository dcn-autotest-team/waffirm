#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.17.py - test case 3.1.17 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-4 10:46:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.17 AC间三层自动发现
# 测试目的：测试AC间三层自动发现功能是否正常
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.17'

avoiderror(testname)
printTimer(testname,'Start','Test three layer automatic discovery between AC')

################################################################################
#Step 1
#
#操作
#关闭AC1二层发现功能
#关闭AC2二层和三层发现功能
#把AC2的IP地址加入到AC1的三层发现ip list中
#
#预期
#AC1上show wireless discovery ip-list看到ip list发现列表“IP Address”中有“IF_VLAN70_S2_IPV4_s
################################################################################

printStep(testname,'Step 1',
          'Close the vlan list discovery',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery method l2-multicast')
SetCmd(switch1,'discovery ip-list',If_vlan70_s2_ipv4_s)

EnterWirelessMode(switch2)
SetCmd(switch2,'no discovery method ip-poll')
SetCmd(switch2,'no discovery method l2-multicast')
	
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless discovery ip-list')
#check
res1 = CheckLine(data1,If_vlan70_s2_ipv4_s,IC=True)
	
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
#在AC1上查看peer AC
#
#预期
#等待30s后，在AC1上show wireless peer-switch显示有:
#“IP Address”为“IF_VLAN70_S2_IPV4”,“Disc. Reason”显示为“IP Poll”
################################################################################

printStep(testname,'Step 2',
          'Check peer switch status on AC1 1',
          'Check the result')

# operate
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
#修改vlan70的接口IP为IF_VLAN70_S1_BACKIPV4,使IF_VLAN70_S1_BACKIPV4>IF_VLAN70_S2_IPV4
#
#预期
#在AC1上show wireless peer-switch显示有“IP Address”为“IF_VLAN70_S2_IPV4”的,Reason”显示为“IP Poll”
################################################################################

printStep(testname,'Step 3',
          'Change AC1 ip index greater then AC2 ip index',
		  'Check the result')		  

# operate	
EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan70)
SetCmd(switch1,'ip address',If_vlan70_s1_backipv4)

EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip',If_vlan70_s1_backipv4_s)
	
IdleAfter(20)
#check
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
				   check=[(If_vlan70_s2_ipv4_s,'IP Poll')],
				   retry=30,interval=5,waitflag=False,IC=True)
						
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
#在AC2上把s2p1口down掉
#
#预期
#在AC1上show wireless peer-switch显示“No peer wireless switch exists”
################################################################################

printStep(testname,'Step 4',
          'Shutdown the interface on AC2',
          'Check the result')

# operate		  
EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'shutdown')

IdleAfter(20)
#check
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
				   check=[('No peer wireless switch exists')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 5',
          'Recover initial config')

# operate		  
#恢复AC1的配置
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery method l2-multicast')
SetCmd(switch1,'no discovery ip-list')
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

#恢复AC2的配置
EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'no shutdown')

EnterWirelessMode(switch2)
SetCmd(switch2,'discovery method ip-poll')
SetCmd(switch2,'discovery method l2-multicast')

#AC1上配置Vlan和静态IP	
EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan70)
SetCmd(switch1,'ip address',If_vlan70_s1_ipv4)

EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip',If_vlan70_s1_ipv4_s)
	
#end
printTimer(testname, 'End')