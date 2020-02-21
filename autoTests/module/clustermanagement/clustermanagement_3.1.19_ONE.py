#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.19.py - test case 3.1.19 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-9 15:35:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.19 Valid ap 表维护测试
# 测试目的：测试AP MAC认证功能是否正确
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.19'

avoiderror(testname)
printTimer(testname,'Start','Test maintenance of Valid AP table')

################################################################################
#Step 1
#
#操作
#在AC1上向valid ap表中添加一个表项
#
#预期
#在AC1上show wireless ap database可以检测到MAC Address 为00-03-0f-00-00-01的条目
################################################################################

printStep(testname,'Step 1',
          'Add a AP to valid ap table on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database 00-03-0f-00-00-01')
	
data1 = SetCmd(switch1,'show wireless ap database')
#check
res1 = CheckLine(data1,'00-03-0f-00-00-01',IC=True)
	
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
#在AC1上向valid ap表中再添加一个表项
#
#预期
#在AC1上show wireless ap database可以看到:
#MAC Address为00-03-0f-00-00-01和00-03-0f-00-00-02的条目
################################################################################

printStep(testname,'Step 2',
          'Add another AP to valid ap table on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database 00-03-0f-00-00-02')
		  
data1 = SetCmd(switch1,'show wireless ap database')
#check
res1 = CheckLineList(data1,[('00-03-0f-00-00-01'),('00-03-0f-00-00-02')],IC=True)
	
#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
#在AC1上向valid ap表中添加一个已存在的表项
#
#预期
#可以添加成功,在AC1上show wireless ap database可以看到:
#MAC Address为00-03-0f-00-00-01和00-03-0f-00-00-02的条目
################################################################################

printStep(testname,'Step 3',
          'Add a exist AP to valid ap table on AC1',
		  'Check the result')		  

# operate	
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database 00-03-0f-00-00-01')
		  
data1 = SetCmd(switch1,'show wireless ap database')
#check
res1 = CheckLineList(data1,[('00-03-0f-00-00-01'),('00-03-0f-00-00-02')],IC=True)
						
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
#为MAC为00-03-0f-00-00-01的AP配置位置信息
#
#预期
#在AC1上show wireless ap database可以检测到:
#MAC Address为”00-03-0f-00-00-01”,Location为”1234Z5-a_89”的条目
################################################################################

printStep(testname,'Step 4',
          'Config location on AP',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database 00-03-0f-00-00-01')
SetCmd(switch1,'location 1234Z5-a_89')

data1 = SetCmd(switch1,'show wireless ap database')
#check
res1 = CheckLine(data1,'00-03-0f-00-00-01','1234Z5-a_89',IC=True)
	
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#在AC1上修改MAC地址为00-03-0f-00-00-01的AP的位置信息
#
#预期
#在AC1上show wireless ap database可以检测到:
#MAC Address为”00-03-0f-00-00-01”,Location为”12345”的条目
################################################################################

printStep(testname,'Step 5',
          'Change location on AP',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database 00-03-0f-00-00-01')
SetCmd(switch1,'location 12345')

data1 = SetCmd(switch1,'show wireless ap database')
#check
res1 = CheckLine(data1,'00-03-0f-00-00-01','12345',IC=True)
	
#result
printCheckStep(testname,'Step 5', res1)

################################################################################
#Step 6
#
#操作
#在AC1上删除MAC地址为00-03-0f-00-00-01的AP的位置信息
#
#预期
#在AC1上show wireless ap database可以检测到:
#MAC Address为”00-03-0f-00-00-01”,Location为空的条目
################################################################################

printStep(testname,'Step 6',
          'Delet location on AP',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database 00-03-0f-00-00-01')
SetCmd(switch1,'no location')

data1 = SetCmd(switch1,'show wireless ap database')
#check1
res1 = CheckLine(data1,'00-03-0f-00-00-01',IC=True)
data2 = SetCmd(switch1,'show wireless ap database')
#check2
res2 = CheckLine(data2,'00-03-0f-00-00-01','12345',IC=True)
res2 = 0 if res2 != 0 else 1

#result
printCheckStep(testname,'Step 6', res1, res2)

################################################################################
#Step 7
#
#操作
#在AC1上查看MAC地址为00-03-0f-00-00-01的AP的工作模式
#
#预期
#在AC1上可以检测到MAC Address为”00-03-0f-00-00-01”,AP Mode为”ws-managed”的条目
################################################################################

printStep(testname,'Step 7',
          'Check ap work mode',
          'Check the result')

# operate		  
data1 = SetCmd(switch1,'show wireless ap database')
#check
res1 = CheckLine(data1,'00-03-0f-00-00-01','ws-managed',IC=True)
	
#result
printCheckStep(testname,'Step 7', res1)

################################################################################
#Step 8
#
#操作
#在AC1上修改MAC地址为00-03-0f-00-00-01的AP的工作模式
#
#预期
#修改成功,在AC1上show wireless ap database可以检测到:
#MAC Address为”00-03-0f-00-00-01”,AP Mode为”standalone”的条目
################################################################################

printStep(testname,'Step 8',
          'Change AP work mode',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database 00-03-0f-00-00-01')
SetCmd(switch1,'mode standalone')

data1 = SetCmd(switch1,'show wireless ap database')
#check
res1 = CheckLine(data1,'00-03-0f-00-00-01','standalone',IC=True)
	
#result
printCheckStep(testname,'Step 8', res1)

################################################################################
#Step 9
#
#操作
#在AC1上为MAC地址为00-03-0f-00-00-01的AP的指定一个profile id，查看当前配置
#
#预期
#在ap database模式下用show running-config current-mode可以检测到“profile 1”
################################################################################

printStep(testname,'Step 9',
          'Config profile id on AP',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database 00-03-0f-00-00-01')
SetCmd(switch1,'profile 1')

data1 = SetCmd(switch1,'show running-config current-mode')
#check
res1 = CheckLine(data1,'profile 1',IC=True)
	
#result
printCheckStep(testname,'Step 9', res1)

################################################################################
#Step 10
#
#操作
#在AC1上删除MAC地址为00-03-0f-00-00-01的AP指定的profile id，查看当前配置
#
#预期
#删除成功,在ap database模式下用show running-config current-mode不能检测到“profile 1”
################################################################################

printStep(testname,'Step 10',
          'Delete profile id on AP',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database 00-03-0f-00-00-01')
SetCmd(switch1,'no profile')

data1 = SetCmd(switch1,'show running-config current-mode')
#check
res1 = CheckLine(data1,'profile 1',IC=True)
res1 = 0 if res1 != 0 else 1
	
#result
printCheckStep(testname,'Step 10', res1)

################################################################################
#Step 11
#
#操作
#在AC1上删除valid ap表中一个表项
#
#预期
#删除成功,在AC1上show wireless ap database不能检测到MAC Address 为”00-03-0f-00-00-01”的条目
################################################################################

printStep(testname,'Step 11',
          'Delete AP from valid ap table',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'no ap database 00-03-0f-00-00-01')

data1 = SetCmd(switch1,'show wireless ap database')
#check
res1 = CheckLine(data1,'00-03-0f-00-00-01',IC=True)
res1 = 0 if res1 != 0 else 1
	
#result
printCheckStep(testname,'Step 11', res1)

################################################################################
#Step 12
#
#操作
#在AC1上删除valid ap表中不存在的表项
#
#预期
#在AC1上可以检测到提示“An AP with the entered MAC address does not exist”
################################################################################

printStep(testname,'Step 12',
          'Check valid ap table on AC1 after'
          'Delete a none exist AP from valid ap table',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
data1 = SetCmd(switch1,'no ap database 00-03-0f-00-00-03')
#check
res1 = CheckLine(data1,'An AP with the entered MAC address does not exist',IC=True)
	
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
SetCmd(switch1,'no ap database 00-03-0f-00-00-01')
SetCmd(switch1,'no ap database 00-03-0f-00-00-02')
SetCmd(switch1,'no ap database 00-03-0f-00-00-03')

#end
printTimer(testname, 'End')