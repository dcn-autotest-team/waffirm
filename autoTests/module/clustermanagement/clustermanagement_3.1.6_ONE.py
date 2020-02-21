#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.6.py - test case 3.1.6 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2017-12-28 10:10:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.6 AP Failure表维护
# 测试目的：测试AP Failure表的维护是否正确 
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.6'

avoiderror(testname)
printTimer(testname,'Start','Test maintenance of AP failure table')

################################################################################
#Step 1
#
#操作
# 在AC1的vlan-list发现列表中加入AP1和AP2的管理vlan vlan70
#
#预期
# AP1和AP2能成功被AC1管理
# 在AC1上show wireless ap status可以看到：
# MAC Address显示为AP1_MAC和AP2_MAC
# Status显示为Managed,Configuration Status显示为Success
################################################################################

printStep(testname,'Step 1',
          'Add discovery vlan list on AC1',
          'Check the result')

# operate		  
EnterEnableMode(switch1)
SetCmd(switch1,'clear wireless ap failure list',timeout=3)
IdleAfter(1)
SetCmd(switch1,'y',timeout=3)

EnterEnableMode(switch2)
SetCmd(switch2,'clear wireless ap failure list',timeout=3)
SetCmd(switch2,'y',timeout=3)

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery vlan-list',Vlan70)

#check1
IdleAfter(20)
res1 = CheckSutCmd(switch1,'show wireless ap status',
                   check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
# 在AC1上修改ap的认证方式为mac认证,删除AP1和AP2的ap database
#
#预期
# 在AC1上show wireless ap failure status可以检测到 MAC Address为AP1_MAC和AP2_MAC的表项
################################################################################

printStep(testname,'Step 2',
          'Change ap authentication mac and delete the ap datebase on AC1',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'ap authentication mac')
SetCmd(switch1,'no ap database',ap1mac)
SetCmd(switch1,'no ap database',ap2mac)

EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

#check1
IdleAfter(10)
res1 = CheckSutCmd(switch1,'show wireless ap failure status',
                   check=[(ap1mac,'No Database Entry'),(ap2mac,'No Database Entry')],
                   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
# 在AC1上增加AP1的ap database数据库
#
#预期
#在AC1上show wireless ap failure status不能检测到MAC Address为AP1_MAC的表项
#在AC1上show wireless ap status能检测到MAC Address为AP1_MAC,Configuration Status显示为Success
################################################################################

printStep(testname,'Step 3',
          'Add AP1 datebase on AC1',
		  'Check the result')		  

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'profile 1')

EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
IdleAfter(20)

#check1
res1 = CheckSutCmd(switch1,'show wireless ap status',
                   check=[(ap1mac,'Managed','Success')],
                   retry=30,interval=5,waitflag=False,IC=True)

#check2
res2 = CheckSutCmdWithNoExpect(switch1,'show wireless ap failure status',
                               check=[(ap1mac,'No Database Entry')],
                               retry=30,interval=5,waitflag=False,IC=True)
					
#result
printCheckStep(testname, 'Step 3', res1, res2)

################################################################################
#Step 4
#
#操作
# 在AC1上删除AP管理vlan
# 在AC1删除所有AP Failure表
#
#预期
# show wireless ap failure status显示为No failed APs exist
################################################################################

printStep(testname,'Step 4',
          'Clear failure ap table',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list')

EnterEnableMode(switch1)
SetCmd(switch1,'clear wireless ap failure list',timeout=3)
SetCmd(switch1,'y',timeout=3)

#check
res1 = CheckSutCmd(switch1,'show wireless ap failure status',
                   check=[('No failed APs exist')],
                   retry=30,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#把AP1的管理vlan vlan70加入到AC1和AC2的vlan list中
#
#预期
#AC1上show wireless peer-switch可以看到IP Address显示为If_vlan70_s2_ipv4_s
#AC2上show wireless ap status检测到AP2的AP2_MAC的Status显示为Managed,“Configuration Status”为“Success”
#AC2上show wireless ap failure status显示为No failed APs exist
################################################################################

printStep(testname,'Step 5',
          'Add discovery vlan list on AC1 and AC2',
          'Check the result')

# operate		
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery vlan-list',Vlan70)

EnterWirelessMode(switch2)
SetCmd(switch2,'discovery vlan-list',Vlan70)

IdleAfter(20)
#check1
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
                   check=[(If_vlan70_s2_ipv4_s)],
                   retry=30,interval=5,waitflag=False,IC=True)

#check1
res2 = CheckSutCmdWithNoExpect(switch1,'show wireless ap failure status',
                               check=[(ap2mac,'No Database Entry')],
                               retry=30,interval=5,waitflag=False,IC=True)		
#check3
res3 = CheckSutCmd(switch2,'show wireless ap status',
                   check=[(ap2mac,'Managed','Success')],
                   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 5', res1, res2, res3)

################################################################################
#Step 6
#
#操作
#在AC1上关闭二层和三层发现功能
#在AC2上修改ap的认证方式为mac认证,删除AP2的ap database数据库
#
#预期
#AC1上show wireless ap failure status可以检测到MAC Address为AP2_MAC的表项
#AC2上show wireless ap failure status可以检测到MAC Address为AP2_MAC的表项
################################################################################

printStep(testname,'Step 6',
          'Change ap authentication mac and delete the ap1 datebase on AC2',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery method ip-poll')
SetCmd(switch1,'no discovery method l2-multicast')

EnterWirelessMode(switch2)
SetCmd(switch2,'ap authentication mac')
SetCmd(switch2,'no ap database',ap2mac)

EnterWirelessMode(switch2)
SetCmd(switch2,'no enable')
IdleAfter(1)
SetCmd(switch2,'enable')
IdleAfter(60)

#check1
res1 = CheckSutCmd(switch2,'show wireless ap failure status',
                   check=[(ap2mac,'No Database Entry')],
                   retry=30,interval=5,waitflag=False,IC=True)	
					
#check2
res2 = CheckSutCmd(switch1,'show wireless ap failure status',
                   check=[(ap2mac,'No Database Entry')],
                   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname, 'Step 6', res1, res2)

################################################################################
#Step 7
#
#操作
#在AC1上删除AP管理vlan,在AC1删除所有AP Failure表
#
#预期
#AC1上show wireless ap failure status显示No failed APs exist
################################################################################

printStep(testname,'Step 7',
          'Clear failure AP on AC1',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list')

EnterWirelessMode(switch1)
SetCmd(switch1,'no ap database',ap1mac)
SetCmd(switch1,'no ap database',ap2mac)

EnterEnableMode(switch1)
SetCmd(switch1,'clear wireless ap failure list',timeout=3)
SetCmd(switch1,'y',timeout=3)

#check
res1 = CheckSutCmd(switch1,'show wireless ap failure status',
                   check=[('No failed APs exist')],
                   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname, 'Step 7', res1)

################################################################################
#Step 8
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 8',
          'Recover initial config')

# operate		  
#恢复AC1配置
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list',Vlan70)
SetCmd(switch1,'discovery method ip-poll')
SetCmd(switch1,'discovery method l2-multicast')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap authentication none')
SetCmd(switch1,'ap database',ap2mac)
SetCmd(switch1,'profile 2')
SetCmd(switch1,'exit')
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'profile 1')

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery vlan-list 1')
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

#恢复AC2配置
EnterWirelessMode(switch2)
SetCmd(switch2,'no discovery vlan-list',Vlan70)
SetCmd(switch2,'no enable')
IdleAfter(1)
SetCmd(switch2,'enable')

EnterWirelessMode(switch2)
SetCmd(switch2,'ap authentication none')
SetCmd(switch2,'ap database',ap1mac)
SetCmd(switch2,'profile 1')
SetCmd(switch2,'exit')
SetCmd(switch2,'ap database',ap2mac)
SetCmd(switch2,'profile 2')

EnterWirelessMode(switch2)
SetCmd(switch2,'no enable')
IdleAfter(1)
SetCmd(switch2,'enable')

#end
printTimer(testname, 'End')