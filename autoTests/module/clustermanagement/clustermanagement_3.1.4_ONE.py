#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.4.py - test case 3.1.4 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2017-12-26 11:28:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.4	AC无线特性的开启和关闭
# 测试目的：测试AC无线特性的开启和关闭功能是否正常。
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.4'

avoiderror(testname)
printTimer(testname,'Start','Test AC open and shutdown wireless')

################################################################################
#Step 1
#
#操作
# 在AC1上删除vlan 70和vlan 80的接口
# 另外配置一个三层接口,把这个三层接口的状态down掉,启动AC无线特性
#
#预期
# show wireless看到'Operational Status'项显示为'Disabled'
################################################################################

printStep(testname,'Step 1',
          'Delete all the interface on AC1 and config a other three interface',
          'Check the result')

# operate		  
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan',Vlan70)
SetCmd(switch1,'no interface vlan',Vlan80)
SetCmd(switch1,'no interface loopback 100')

EnterConfigMode(switch1)
SetCmd(switch1,'vlan',Vlan10)
EnterConfigMode(switch1)
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'switchport trunk allowed vlan',Vlan70+';'+Vlan80+';'+Vlan10)
EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan10)
SetCmd(switch1,'ip address',If_vlan10_ipv4)
SetCmd(switch1,'shutdown')

EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
IdleAfter(5)

#check
res1 = CheckSutCmd(switch1,'show wireless',
                   check=[('Operational Status','Disabled')],
                   retry=5,waitflag=False,IC=True)
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
# 把AC1上配置的三层接口状态up起来
# 在AC1上关闭自动获取无线IP地址功能并且不指定AC静态无线IP
#
#预期
# show wireless看到'Operational Status'项显示为'Disabled'
#
################################################################################

printStep(testname,'Step 2',
          'No shutdown the three layer interface',
          'Check the result')

# operate		  
EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan10)
SetCmd(switch1,'no shutdown')
IdleAfter(5)

#check
res1 = CheckSutCmd(switch1,'show wireless',
                   check=[('Operational Status','Disabled')],
                   retry=5,waitflag=False,IC=True)
#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
# 把AC1上配置的三层接口状态down掉,静态指定无线IP地址为三层接口地址
#
#预期
#show wireless看到'Operational Status'项显示为'Disabled'
################################################################################

printStep(testname,'Step 3',
          'Shutdown the three layer interface and assign as it a static ip',
		  'Check the result')		  

# operate		  
EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan10)
SetCmd(switch1,'shutdown')

EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip',If_vlan10_ipv4_s)
IdleAfter(5)

#check
res1 = CheckSutCmd(switch1,'show wireless',
                   check=[('Operational Status','Disabled')],
                   retry=5,waitflag=False,IC=True)
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
# 把AC1上配置的三层接口状态up起来，静态指定无线IP地址为三层接口地址
#
#预期
# show wireless看到'Operational Status'项显示为'Enabled','WS IP Address'项显示为'If_vlan10_ipv4_s'
################################################################################

printStep(testname,'Step 4',
          'No shutdown the three layer interface',
          'Check the result')

# operate
EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan10)
SetCmd(switch1,'no shutdown')
IdleAfter(10)

#check
res1 = CheckSutCmd(switch1,'show wireless',
                   check=[('WS IP Address',If_vlan10_ipv4_s),
                          ('Operational Status','Enabled')],
                   retry=10,waitflag=False,IC=True)
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#在AC1上更改静态指定无线IP地址
#
#预期
#等待3s，show wireless看到'Operational Status'项显示为'Enabled','WS IP Address'项显示为'If_vlan10_ipv4_s'
#再等待30s，show wireless看到'Operational Status'项显示为'Enabled','WS IP Address'项显示为'If_vlan10_ipv4_s'
################################################################################

printStep(testname,'Step 5',
          'Assign a same static ip on AC1',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip')
SetCmd(switch1,'static-ip',If_vlan10_ipv4_s)

IdleAfter(4)
data1 = SetCmd(switch1,'show wireless')
#check1
res1 = CheckLineList(data1,[('WS IP Address',If_vlan10_ipv4_s),
                     ('Operational Status','Enabled')],IC=True)
                     
IdleAfter(15)
data2 = SetCmd(switch1,'show wireless')
#check2
res2 = CheckLineList(data2,[('WS IP Address',If_vlan10_ipv4_s),
                     ('Operational Status','Enabled')],IC=True)

#result
printCheckStep(testname, 'Step 5', res1, res2)

################################################################################
#Step 6
#
#操作
#在AC1上另外再配置一个三层接口,更改静态指定无线IP地址
#
#预期
#show wireless看到'Operational Status'项显示为'Disabled'
#等待40s，show wireless看到'Operational Status'项显示为'Enabled','WS IP Address'项显示为'If_vlan9_ipv4_s'
################################################################################

printStep(testname,'Step 6',
          'Config a three layer interface and assign it as a static ip',
          'Check the result')

# operate		  
EnterConfigMode(switch1)
SetCmd(switch1,'vlan',Vlan9)
EnterConfigMode(switch1)
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'switchport trunk allowed vlan',Vlan70+';'+Vlan80+';'+Vlan10+';'+Vlan9)
EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan9)
SetCmd(switch1,'ip address',If_vlan9_ipv4)

EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip',If_vlan9_ipv4_s)

#check1
res1 = CheckSutCmd(switch1,'show wireless',check=[('Operational Status','Disable')],
			       retry=10,interval=1,waitflag=False,IC=True)
#check2	
IdleAfter(10)	
res2 = CheckSutCmd(switch1,'show wireless',
                   check=[('WS IP Address',If_vlan9_ipv4_s),('Operational Status','Enabled')],
			       retry=6,interval=5,waitflag=False,IC=True)			
#result
printCheckStep(testname, 'Step 6', res1, res2)

################################################################################
#Step 7
#
#操作
#在AC1上更改静态指定无线IP地址为If_vlan10_ipv4
#
#预期
#show wireless看到'Operational Status'项显示为'Disabled'
#等待40s，show wireless看到'Operational Status'项显示为'Enabled','WS IP Address'项显示为'If_vlan10_ipv4_s'
################################################################################

printStep(testname,'Step 7',
          'Assign a different static ip on AC1',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip',If_vlan10_ipv4_s)

#check1
res1 = CheckSutCmd(switch1,'show wireless',
                   check=[('Operational Status','Disable')],
			       retry=10,interval=1,waitflag=False,IC=True)
#check2
IdleAfter(10)
res2 = CheckSutCmd(switch1,'show wireless',
                   check=[('WS IP Address',If_vlan10_ipv4_s),('Operational Status','Enabled')],
			       retry=6,interval=5,waitflag=False,IC=True)	
#result
printCheckStep(testname, 'Step 7', res1, res2)

################################################################################
#Step 8
#
#操作
#在AC1上另外再配置一个三层接口
#
#预期
#在静态配置和自动选择都配置的情况下,会优先采用自动分配的地址，
#how wireless看到'Operational Status'项显示为'Enabled','WS IP Address'项显示为'If_vlan8_ipv4_s'
################################################################################

printStep(testname,'Step 8',
          'Config a other three layer interface and open the auto ip assign',
          'Check the result')

# operate
EnterConfigMode(switch1)
SetCmd(switch1,'vlan',Vlan8)
EnterConfigMode(switch1)
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'switchport trunk allowed vlan',Vlan70+';'+Vlan80+';'+Vlan10+';'+Vlan9+';'+Vlan8)

EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan8)
SetCmd(switch1,'ip address',If_vlan8_ipv4)
		  
EnterWirelessMode(switch1)
SetCmd(switch1,'auto-ip-assign')
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
#check
IdleAfter(10)
res2 = CheckSutCmd(switch1,'show wireless',
                   check=[('WS IP Address',If_vlan8_ipv4_s),('Operational Status','Enabled')],
			       retry=6,interval=5,waitflag=False,IC=True)
#result
printCheckStep(testname, 'Step 8', res1)

################################################################################
#Step 9
#
#操作
#在AC1上down掉无线IP对应的接口
#
#预期
#show wireless看到'Operational Status'项显示为'Disabled'
#等待40s，show wireless看到'Operational Status'项显示为'Enabled','WS IP Address'项显示为'If_vlan9_ipv4_s'
################################################################################

printStep(testname,'Step 9',
          'Shutdown the interface which assign as a static ip',
          'Check the result')

# operate
EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan8)
SetCmd(switch1,'shutdown')

#check1
res1 = CheckSutCmd(switch1,'show wireless',check=[('Operational Status','Disable')],
			       retry=10,interval=1,waitflag=False,IC=True)

#check2
IdleAfter(10)
res2 = CheckSutCmd(switch1,'show wireless',
                   check=[('WS IP Address',If_vlan9_ipv4_s),('Operational Status','Enabled')],
			       retry=6,interval=5,waitflag=False,IC=True)
#result
printCheckStep(testname, 'Step 9', res1, res2)

################################################################################
#Step 10
#
#操作
#在AC1上删除目前无线IP地址对应的接口
#
#预期
#show wireless看到'Operational Status'项显示为'Disabled'
#等待40s，show wireless看到'Operational Status'项显示为'Enabled','WS IP Address'项显示为'If_vlan10_ipv4_s'
################################################################################

printStep(testname,'Step 10',
          'Delete the three layer interface which assign as a static ip',
          'Check the result')

# operate
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan',Vlan9)

#check1
res1 = CheckSutCmd(switch1,'show wireless',check=[('Operational Status','Disable')],
			       retry=10,interval=1,waitflag=False,IC=True)
                   
#check2
IdleAfter(10)
res2 = CheckSutCmd(switch1,'show wireless',
                   check=[('WS IP Address',If_vlan10_ipv4_s),('Operational Status','Enabled')],
			       retry=6,interval=5,waitflag=False,IC=True)
#result
printCheckStep(testname, 'Step 10', res1, res2)

################################################################################
#Step 11
#
#操作
#在AC1上改变目前无线IP地址对应的接口IP
#
#预期
#show wireless看到'Operational Status'项显示为'Disabled'
#等待40s，show wireless看到'Operational Status'项显示为'Enabled','WS IP Address'项显示为'11.11.11.11'
################################################################################

printStep(testname,'Step 11',
          'Change the three layer interface ip which assign as a static ip',
          'Check the result')

# operate
EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan10)
SetCmd(switch1,'ip address 11.11.11.11 255.255.255.0')

#check1
res1 = CheckSutCmd(switch1,'show wireless',check=[('Operational Status','Disable')],
			       retry=10,interval=1,waitflag=False,IC=True)

#check2
IdleAfter(10)
res2 = CheckSutCmd(switch1,'show wireless',
                   check=[('WS IP Address','11.11.11.11'),('Operational Status','Enabled')],
			       retry=6,interval=5,waitflag=False,IC=True)
#result
printCheckStep(testname, 'Step 11', res1, res2)

################################################################################
#Step 12
#
#操作
#在AC1上down掉无线IP地址对应的接口
#
#预期
#show wireless看到'Operational Status'项显示为'Disabled'
################################################################################

printStep(testname,'Step 12',
          'Shutdown the three layer interface which change the ip address',
          'Check the result')

# operate
EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan10)
SetCmd(switch1,'shutdown')

#check
IdleAfter(10)
res1 = CheckSutCmd(switch1,'show wireless',
                   check=[('Operational Status','Disabled')],
			       retry=6,interval=5,waitflag=False,IC=True)
#result
printCheckStep(testname, 'Step 12', res1)

################################################################################
#Step 13
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 13',
          'Recover initial config')

# operate		  
#删除三层接口和vlan
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan',Vlan10)
SetCmd(switch1,'no interface vlan',Vlan8)
SetCmd(switch1,'no vlan',Vlan10)
SetCmd(switch1,'no vlan',Vlan9)
SetCmd(switch1,'no vlan',Vlan8)

#添加vlan
EnterConfigMode(switch1)
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'switchport trunk allowed vlan',Vlan70+';'+Vlan80)

#配置IP
EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan70)
SetCmd(switch1,'ip address',If_vlan70_s1_ipv4)
EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan80)
SetCmd(switch1,'ip address',If_vlan80_s1_ipv4)
EnterConfigMode(switch1)
SetCmd(switch1,'interface loopback 100')
SetCmd(switch1,'ip address',StaticIpv4_ac1,'255.255.255.255')

#配置静态IP
EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip',If_vlan70_s1_ipv4_s)
SetCmd(switch1,'no auto-ip-assign')

#end
printTimer(testname, 'End')