#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.22.py - test case 3.1.22 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-10 10:26:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.22 AP Flood反制功能测试
# 测试目的：测试AP Flood反制功能是否正确
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.22'

avoiderror(testname)
printTimer(testname,'Start','Test anti-flood function of AP')

################################################################################
#Step 1
#
#操作
#在AC1缺省情况下，查看AP Flood功能状态
#
#预期
#在缺省情况下,AP Flood的功能是默认开启的
#在AC1上可以检测到:
#Operational Status显示为Enable，Detected Interval显示为5
#Allowed Max Connect Count显示为4，Age Time显示为30
################################################################################

printStep(testname,'Step 1',
          'Check ap flood with default config',
          'Check the result')

# operate
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless ap anti-flood')
#check
res1 = CheckLineList(data1,[('Operational Status','Enable'),
					 ('Detected Interval','5'),('Allowed Max Connect Count','4'),
					 ('Age Time','30')],IC=True)
	
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
#在AC1的vlan-list发现列表中加入AP1和AP2的管理vlan vlan70
#
#预期
#AP1和AP2能成功被AC1管理,show wi ap status在AC1上可以检测到:
#AP1_MAC的“Status”为“Managed Success”,AP2_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 2',
          'Add management vlan to discovery vlan list on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery vlan-list',Vlan70)
	
IdleAfter(20)	
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success'),
				   (ap2mac,'Managed','Success')],
				   waittime=5,retry=15,interval=5,IC=True)

#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
#在AC1上把AP Flood允许最大连接次数改为1,修改认证方式为MAC,本地认证
#从valid ap表中删除MAC地址为AP1_MAC的表项
#在AC1上重启无线功能
#
#预期
#在AC1上用show wireless ap anti-flood检测到：
#Allowed Max Connect Count显示为1,Total Flood Aps显示为1
#在AC1上用show wireless ap anti-flood status检测MAC Address显示为AP1_MAC
################################################################################

printStep(testname,'Step 3',
          'Set ap anti-flood max-conn-count 1 on AC1',
		  'Check the result')		  

# operate	
EnterWirelessMode(switch1)
SetCmd(switch1,'wireless ap anti-flood max-conn-count 1')
SetCmd(switch1,'ap authentication mac')
SetCmd(switch1,'no ap database',ap1mac)

EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(20)
#check1
res1 = CheckSutCmd(switch1,'show wireless ap anti-flood status',check=[(ap1mac)],
				   retry=30,interval=5,waitflag=False,IC=True)

#check2
res2 = CheckSutCmd(switch1,'show wireless ap anti-flood',
				   check=[('Total Flood Aps','1'),
				   ('Allowed Max Connect Count','1')],
				   retry=30,interval=5,waitflag=False,IC=True)
				   
#result
printCheckStep(testname, 'Step 3', res1, res2)

################################################################################
#Step 4
#
#操作
#在AC1的valid ap表中加入MAC地址为AP1_MAC的表项
#
#预期
#由于AP1被加入到ap anti-flood表中，AP1无法被AC1管理
#show wi ap status不能检测到MAC地址为AP1_MAC的表项
################################################################################

printStep(testname,'Step 4',
          'Add AP1 mac to ap database on AC1',
          'Check the result')

# operate  
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'profile 1')
	
IdleAfter(60)
#check
res1 = CheckSutCmdWithNoExpect(switch1,'show wireless ap status',
                               check=[(ap1mac,'Managed','Success')],
                               retry=1,interval=5,waitflag=False,IC=True)	
				   
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#在AC1上把AP Flood的agetime改为3
#
#预期
#在AC1上用show wireless ap anti-flood查看Age Time显示为3
################################################################################

printStep(testname,'Step 5',
          'Set ap flood agetime as 3',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'wireless ap anti-flood agetime 3')

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless ap anti-flood')
#check
res1 = CheckLine(data1,'Age Time','3',IC=True)
	
#result
printCheckStep(testname,'Step 5', res1)

################################################################################
#Step 6
#
#操作
#等待3分钟，在AC1上查看AP Flood反制表中所有的记录
#
#预期
#老化时间到3分钟后,AP1从反制表中删除
#在AC1上用show wireless ap anti-flood status显示为No ap flood entries discovered
################################################################################

printStep(testname,'Step 6',
          'Check ap anti-flood status',
          'Check the result')

# operate
IdleAfter(180)		  
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless ap anti-flood status')
#check
res1 = CheckLine(data1,'No ap flood entries discovered',IC=True)

#result
printCheckStep(testname,'Step 6', res1)

################################################################################
#Step 7
#
#操作
#在AC1上查看AP1的状态
#
#预期
#AP1能成功被AC1管理,show wi ap status在AC1上可以检测到AP1被AC1成功管理
#AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 7',
          'Check AP1 on AC1',
          'Check the result')

# operate
IdleAfter(20)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 7', res1)

################################################################################
#Step 8
#
#操作
#在AC1上把AP Flood的agetime改为默认值
#
#预期
#在AC1上用show wireless ap anti-flood可以检测到Age Time显示为30
################################################################################

printStep(testname,'Step 8',
          'Change agetime with default value',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no wireless ap anti-flood agetime')

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless ap anti-flood')
#check
res1 = CheckLine(data1,'Age Time','30')

#result
printCheckStep(testname,'Step 8', res1)

################################################################################
#Step 9
#
#操作
#在AC1中从valid ap表中删除MAC地址为AP2_MAC的表项
#在AC1上重启无线功能
#
#预期
#等待3分钟,在AC1上用show wireless ap anti-flood status检测MAC Address显示为AP2_MAC
################################################################################

printStep(testname,'Step 9',
          'Delete AP2 mac from ap database',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no ap database',ap2mac)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(20)
#check
res1 = CheckSutCmd(switch1,'show wireless ap anti-flood status',
				   check=[(ap2mac)],retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 9', res1)

################################################################################
#Step 10
#
#操作
#在AC1的valid ap表中加入MAC地址为AP2_MAC的表项
#
#预期
#由于AP2被加入到ap anti-flood表中,AP2无法被AC1管理
#show wi ap status不能检测到MAC地址为AP2_MAC的表项
################################################################################

printStep(testname,'Step 10',
          'Add AP2 mac to ap database on AC1',
          'Check the result') 

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap2mac)
SetCmd(switch1,'profile 2')

IdleAfter(60)
#check
res1 = CheckSutCmdWithNoExpect(switch1,'show wireless ap status',
                               check=[(ap2mac,'Managed','Success')],
                               retry=1,interval=5,waitflag=False,IC=True)
				   
#result
printCheckStep(testname,'Step 10', res1)

################################################################################
#Step 11
#
#操作
#在AC1上用clear wireless ap anti-flood清空AP flood表
#
#预期
#由于AP2从 ap anti-flood表中被删除，AP2能成功被AC1管理
#show wi ap status能检测到MAC地址为AP2_MAC的表项
################################################################################

printStep(testname,'Step 11',
          'Clear ap anti-flood table',
          'Check the result')

# operate
EnterEnableMode(switch1)
SetCmd(switch1,'clear wireless ap anti-flood',timeout=3)
SetCmd(switch1,'y',timeout=3)

IdleAfter(20)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap2mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 11', res1)

################################################################################
#Step 12
#
#操作
#在AC1上关闭AP Flood功能
#
#预期
#在AC1上sho wireless ap anti-flood检查显示AP anti-flood is not enabl
################################################################################

printStep(testname,'Step 12',
          'Shutdown ap anti-flood on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no wireless ap anti-flood')

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless ap anti-flood')
#check
res1 = CheckLine(data1,'AP anti-flood is not enable',IC=True)

#result
printCheckStep(testname,'Step 12', res1)

################################################################################
#Step 13
#
#操作
#在AC1上从valid ap表中删除MAC地址为AP2_MAC的表项
#在AC1上重启无线功能
#
#预期
#等待3分钟,在AC1上用show wireless ap anti-flood status不能检测到MAC Address显示为AP2_MAC
################################################################################

printStep(testname,'Step 13',
          'Delete AP2 mac from ap database',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no ap database',ap2mac)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(180)
#check
res1 = CheckSutCmd(switch1,'show wireless ap anti-flood status',
				   check=[(ap2mac)],waittime=5,retry=1,interval=5,IC=True)
res1 = 0 if res1 != 0 else 1

#result
printCheckStep(testname,'Step 13', res1)

################################################################################
#Step 14
#
#操作
#在AC1的valid ap表中加入MAC地址为AP2_MAC的表项
#
#预期
#等待3分钟,AP1能成功被AC1管理,show wi ap status在AC1上可以检测到AP2被AC1成功管理
#AP2_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 14',
          'Add AP2 mac to ap database on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap2mac)
SetCmd(switch1,'profile 2')

IdleAfter(20)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap2mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 14', res1)

################################################################################
#Step 15
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 15',
          'Recover initial config')

# operate		  
#恢复AC1的配置
EnterWirelessMode(switch1)
SetCmd(switch1,'wireless ap anti-flood')
SetCmd(switch1,'no discovery vlan-list',Vlan70)
SetCmd(switch1,'ap authentication none')
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
SetCmd(switch1,'no wireless ap anti-flood max-conn-count')
SetCmd(switch1,'no wireless ap anti-flood agetime')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'profile 1')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap2mac)
SetCmd(switch1,'profile 2')

#end
printTimer(testname, 'End')