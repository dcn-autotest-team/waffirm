#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.8.py - test case 3.1.8 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2017-12-28 15:34:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.8 自动发现功能AC上discovery vlan list列表测试
# 测试目的：测试AC上discovery vlan list列表
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.8'

avoiderror(testname)
printTimer(testname,'Start','Test discovery vlan list on AC')

################################################################################
#Step 1
#
#操作
# 在没有任何配置情况下查看vlan list列表
#
#预期
# 查看成功,缺省vlan list中只包括vlan1,检查：VLAN显示为1
################################################################################

printStep(testname,'Step 1',
          'Check vlan list with default config on AC1',
          'Check the result')

# operate		  
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless discovery vlan-list')

#check
res1 = CheckLine(data1,'1',IC=True)
	
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
# 在AC1上创建一个vlan后,在vlan list列表中添加这个vlan
#
#预期
# 添加成功,用show wireless discovery vlan-list查看检查:2这个VLAN在列表中
################################################################################

printStep(testname,'Step 2',
          ' Add a vlan in discovery vlan list',
          'Check the result')

# operate	
EnterConfigMode(switch1)
SetCmd(switch1,'vlan 2')
	
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery vlan-list 2')

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless discovery vlan-list')

#check
res1 = CheckLine(data1,'2','VLAN0002',IC=True)

#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
# 在AC1上创建一个已经在vlan list列表中存在的vlan
#
#预期
# 在AC1上会出现提示信息：VLAN ID 2 already exists in the polling list.
################################################################################

printStep(testname,'Step 3',
          'Add a exist ip into discovery ip list',
		  'Check the result')		  

# operate		  
EnterWirelessMode(switch1)
data1 = SetCmd(switch1,'discovery vlan-list 2')

#check
res1 = CheckLine(data1,'VLAN ID 2 already exists in the polling list',IC=True)

#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
# 在AC1的vlan list上添加一个AC1上不存在的vlan
#
#预期
# 添加成功,用show wireless discovery vlan-list查看检查:3这个VLAN在列表中
################################################################################

printStep(testname,'Step 4',
          'Add a vlan which is not exist on AC1 into discovery vlan list',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery vlan-list 3')

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless discovery vlan-list')

#check
res1 = CheckLine(data1,'3',IC=True)

#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#在AC1上删除一个vlan列表中不存在的vlan
#
#预期
#在AC1上会出现提示信息：Failed to delete VLAN ID from the polling list
################################################################################

printStep(testname,'Step 5',
          'Delete a vlan which is not exist on AC1 from discovery vlan list',
          'Check the result')

# operate		
EnterWirelessMode(switch1)
data1 = SetCmd(switch1,'no discovery vlan-list 4')

#check
res1 = CheckLine(data1,'Failed to delete VLAN ID from the polling list',IC=True)

#result
printCheckStep(testname,'Step 5', res1)

################################################################################
#Step 6
#
#操作
#在AC1上删除一个vlan列表中已经存在的vlan
#
#预期
#删除成功,用show wireless discovery vlan-list查看检查：3这个VLAN不在列表中
################################################################################

printStep(testname,'Step 6',
          'Delete a exist vlan from discovery vlan list',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list 3')

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless discovery vlan-list')

#check
res1 = CheckLine(data1,'3','VLAN0003',IC=True)
res1 = 0 if res1 != 0 else 1
	
#result
printCheckStep(testname, 'Step 6', res1)

################################################################################
#Step 7
#
#操作
#在AC1上删除所有vlan list中的vlan
#
#预期
#删除成功,用show wireless discovery vlan-list查看检查提示：
#L2 Multicast discovery list is empty
################################################################################

printStep(testname,'Step 7',
          'Delete all the vlan from discovery vlan list',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list')

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless discovery vlan-list')

#check
res1 = CheckLine(data1,'L2 Multicast discovery list is empty',IC=True)

#result
printCheckStep(testname, 'Step 7', res1)

################################################################################
#Step 8
#
#操作
#AC1的vlan-list列表删空后,添加一个vlan到vlan list中
#
#预期
#添加成功，用show wireless discovery vlan-list查看检查:2这个VLAN在列表中
################################################################################

printStep(testname,'Step 8',
          'Add a vlan in discovery vlan list',
          'Check the result')

# operate		
EnterConfigMode(switch1)
SetCmd(switch1,'vlan 2')
		
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery vlan-list 2')

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless discovery vlan-list')

#check
res1 = CheckLine(data1,'2','VLAN0002',IC=True)

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
EnterConfigMode(switch1)
SetCmd(switch1,'no vlan 2')

EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list')
SetCmd(switch1,'discovery vlan-list 1')
		  
#end
printTimer(testname, 'End')