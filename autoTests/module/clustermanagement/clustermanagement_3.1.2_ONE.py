#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.2.py - test case 3.1.2 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2017-12-21 17:00:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.2 AC由管理员静态指定无线IP地址功能
# 测试目的：测试AC开启静态指定无线IP地址功能，是否能为AC指定固定的IP地址提供无线服务。
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.2'

avoiderror(testname)
printTimer(testname,'Start','Test static designated wireless IP Address on AC')

################################################################################
#Step 1
#
#操作
# 在AC1上删除已配置的三层接口,开启静态指定无线IP地址功能
# 指定一个AC1上不存在的IP地址
# 用show wireless查看结果
#
#预期
# show wireless看到'WLAN Switch Disable Reason'项已经显示为'IP address not configured'
#
################################################################################

printStep(testname,'Step 1',
          'Delete all the interface and assign a none-exist static ip',
          'Check the result')

# operate		  
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan',Vlan70)
SetCmd(switch1,'no interface vlan',Vlan80)
SetCmd(switch1,'no interface loopback 100')

EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip 1.1.1.1')
IdleAfter(5)

#check
res1=CheckSutCmd(switch1,'show wireless',
                 check=[('WLAN Switch Disable Reason','IP address not configured')],
                 retry=5,interval=5,waitflag=False,IC=True)
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
# 在AC1上配置一个三层接口地址,并静态指定这个三层接口地址为AC的无线IP地址
#
#预期
#AC1上show wireless看到'WS IP Address'项已经显示为'If_vlan10_ipv4_s'
#
################################################################################

printStep(testname,'Step 2',
          'Config a three layer interface and assign it as a static ip',
          'Check the result')

# operate		  
EnterConfigMode(switch1)
SetCmd(switch1,'vlan',Vlan10)
EnterConfigMode(switch1)
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'switchport trunk allowed vlan',Vlan70+';'+Vlan80+';'+Vlan10)

EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan10)
SetCmd(switch1,'ip address',If_vlan10_ipv4)

EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip',If_vlan10_ipv4_s)
IdleAfter(5)

#check
res1 = CheckSutCmd(switch1,'show wireless',
                   check=[('WS IP Address',If_vlan10_ipv4_s)],
                   retry=5,waitflag=False,IC=True)
#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
#删除静态指定的IP地址
#
#预期
#AC1上show wireless看到'WLAN Switch Disable Reason'项已经显示为'IP address not configured'
#
################################################################################

printStep(testname,'Step 3',
          'Delete the static ip',
		  'Check the result')		  

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'no static-ip')
IdleAfter(5)

#check
res1 = CheckSutCmd(switch1,'show wireless',
                   check=[('WLAN Switch Disable Reason','IP address not configured')],
                   retry=5,waitflag=False,IC=True)
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
# AC1上静态指定IP地址为If_vlan10_ipv4,另外再配置一个三层接口地址
# 开启无线IP自动选择功能,重启AC无线功能
#
#预期
#在静态配置和自动选择都配置的情况下,会优先采用自动分配的地址
#AC1上show wireless看到'WS IP Address'项已经显示为'If_vlan9_ipv4_s'
################################################################################

printStep(testname,'Step 4',
          'Assign a static ip and open auto ip assign',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip',If_vlan10_ipv4_s)
SetCmd(switch1,'auto-ip-assign')

EnterConfigMode(switch1)
SetCmd(switch1,'vlan',Vlan9)
EnterConfigMode(switch1)
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'switchport trunk allowed vlan',Vlan70+';'+Vlan80+';'+Vlan10+';'+Vlan9)

EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan9)
SetCmd(switch1,'ip address',If_vlan9_ipv4)

IdleAfter(30)
EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

# IdleAfter(30)
# EnterWirelessMode(switch1)
# SetCmd(switch1,'no enable')
IdleAfter(1)
# SetCmd(switch1,'enable')
IdleAfter(30)

#check
res1 = CheckSutCmd(switch1,'show wireless',
                   check=[('WS IP Address',If_vlan9_ipv4_s)],
                   retry=5,waitflag=False,IC=True)
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#关闭无线IP自动选择功能
#在AC上配置一个环回接口地址,并静态指定这个环回接口地址为AC的无线IP地址
#
#预期
#AC1上show wireless看到'WS IP Address'项已经显示为'If_loopback2_ipv4_s'
################################################################################

printStep(testname,'Step 5',
          'Config a loopback interface and assign it as a static ip',
          'Check the result')

# operate		  
EnterConfigMode(switch1)
SetCmd(switch1,'interface loopback 2')
SetCmd(switch1,'ip address',If_loopback2_ipv4)

EnterWirelessMode(switch1)
SetCmd(switch1,'no auto-ip-assign')
SetCmd(switch1,'static-ip',If_loopback2_ipv4_s)
IdleAfter(20)

#check
res1 = CheckSutCmd(switch1,'show wireless',
                   check=[('WS IP Address',If_loopback2_ipv4_s)],
                   retry=5,waitflag=False,IC=True)
#result
printCheckStep(testname, 'Step 5', res1)

################################################################################
#Step 6
#
#操作
#在AC上另外再配置一个环回接口地址,并更改静态指定的IP地址为这个环回接口的地址
#
#预期
#AC1上show wireless看到'WS IP Address'项已经显示为'If_loopback1_ipv4_s'
################################################################################

printStep(testname,'Step 6',
          'Config a other loopback interface and assign it as a static ip',
          'Check the result')

# operate		  
EnterConfigMode(switch1)
SetCmd(switch1,'interface loopback 1')
SetCmd(switch1,'ip address',If_loopback1_ipv4)

EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip',If_loopback1_ipv4_s)
IdleAfter(5)

#check
res1 = CheckSutCmd(switch1,'show wireless',
                   check=[('WS IP Address',If_loopback1_ipv4_s)],
                   retry=5,waitflag=False,IC=True)
#result
printCheckStep(testname, 'Step 6', res1)

################################################################################
#Step 7
#
#操作
#在AC上把静态指定的环回接口的状态down掉
#
#预期
#AC1上show wireless看到'WLAN Switch Disable Reason'项显示为'IP address not configured'
################################################################################

printStep(testname,'Step 7',
          'Shutdown the interface which assign as a static ip',
          'Check the result')

# operate		  
EnterConfigMode(switch1)
SetCmd(switch1,'interface loopback 1')
SetCmd(switch1,'shutdown')
IdleAfter(5)

#check
res1 = CheckSutCmd(switch1,'show wireless',
                   check=[('WLAN Switch Disable Reason','IP address not configured')],
                   retry=5,waitflag=False,IC=True)
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
#删除以上三层接口、环回接口和vlan
EnterConfigMode(switch1)
SetCmd(switch1,'no interface loopback 1')
SetCmd(switch1,'no interface loopback 2')
SetCmd(switch1,'no interface vlan',Vlan10)
SetCmd(switch1,'no interface vlan',Vlan9)
SetCmd(switch1,'no vlan',Vlan10)
SetCmd(switch1,'no vlan',Vlan9)

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

#配置静态IP
EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip',If_vlan70_s1_ipv4_s)

#end
printTimer(testname, 'End')