#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.5.py - test case 3.1.5 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2017-12-26 17:16:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.5 Managed AP表的维护
# 测试目的：测试Managed AP表的维护是否正确
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.5'

avoiderror(testname)
printTimer(testname,'Start','Test maintenance of managed AP table')

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
# IP Address显示为AP1_IPV4和AP2_IPV4,Profile显示为1和2
# Status显示为Managed,Configuration Status显示为Success
################################################################################

printStep(testname,'Step 1',
          'Add discovery vlan list on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery vlan-list',Vlan70)

#check1
IdleAfter(10)
res1 = CheckSutCmd(switch1,'show wireless ap status',
                   check=[(ap1mac,Ap1_ipv4,'1','Managed','Success'),(ap2mac,Ap2_ipv4,'2','Managed','Success')],
                   retry=30,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
# 把AP1的管理vlan加入到AC2的vlan list中
#
#预期
#AC1上show wireless peer-switch显示有“IP Address”为“IF_VLAN70_S2_IPV4_s
#AC2上show wi ap status可以检测到Managed AP表为空,显示为No managed Aps discovered
################################################################################

printStep(testname,'Step 2',
          'Add discovery vlan list on AC2',
          'Check the result')

# operate		  
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery vlan-list',Vlan70)
SetCmd(switch2,'no enable')
IdleAfter(1)
SetCmd(switch2,'enable')

IdleAfter(20)
#check1
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
                   check=[(If_vlan70_s2_ipv4_s)],
                   retry=30,interval=5,waitflag=False,IC=True)

#check2
data1 = SetCmd(switch2,'show wireless ap status')
res2 = CheckLine(data1,'No managed APs discovered',IC=True)	
	
#result
printCheckStep(testname, 'Step 2', res1, res2)

################################################################################
#Step 3
#
#操作
# 在S3上把接AP1的接口s3p3down掉
#
#预期
# show wireless ap status可以看到MAC Address显示为AP1_MAC,Status显示为Failed
################################################################################

printStep(testname,'Step 3',
          'Shutdown interface which is connected AP1 on S3',
		  'Check the result')		  

# operate		  
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'shutdown')

IdleAfter(30)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
                   check=[(ap1mac,'Failed')],
                   retry=5,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
# 在AC1上关闭二层和三层发现功能
# 在S3上把接AP1的接口s3p3 up起来
# 
#预期
#AP1会在AC2上上线,AC1上可以检测到:AP1的mac地址“AP1_MAC”的Status显示为Managed
#AC2上可以检测到:AP1的AP1_MAC的Status显示为Managed
################################################################################

printStep(testname,'Step 4',
          'Close L2 and L3 discovery method on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery method ip-poll')
SetCmd(switch1,'no discovery method l2-multicast')

EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'no shutdown')

IdleAfter(20)
#check1
res1 = CheckSutCmd(switch1,'show wireless ap status',
                   check=[(ap1mac,'Managed')],
                   retry=30,interval=5,waitflag=False,IC=True)
	
#check2
res2 = CheckSutCmd(switch2,'show wireless ap status',
                   check=[(ap1mac,'Managed')],
                   retry=5,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname,'Step 4', res1, res2)

################################################################################
#Step 5
#
#操作
#在S3上把接AP1的接口s3p3和接AP2的接口s3p4均down掉
#
#预期
#AC1上show wireless ap status可以看到：
#AP1的mac地址AP1_MAC的Status显示为Failed
#MAC Address为AP2_MAC的Status显示为Failed
################################################################################

printStep(testname,'Step 5',
          'Shutdown interface which is connected AP1 and AP2 on S3',
          'Check the result')

# operate		
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'shutdown')

EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p4)
SetCmd(switch3,'shutdown')

IdleAfter(30)
#check1
res1 = CheckSutCmd(switch1,'show wireless ap status',
                   check=[(ap1mac,'Failed'),(ap2mac,'Failed')],
                   retry=5,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname,'Step 5', res1)

################################################################################
#Step 6
#
#操作
#在AC1上删除Managed AP表中所有failed AP
#
# 预期
# 在AC1上查看Managed AP表,MAC Address为AP1_MAC和AP2_MAC的表项被删除
##############################################################################

printStep(testname,'Step 6',
          'Clear failed AP on AC1',
          'Check the result')

# operate		  
EnterEnableMode(switch1)
SetCmd(switch1,'clear wireless ap failed',timeout=3)
IdleAfter(1)
SetCmd(switch1,'y',timeout=3)

#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
                   check=[('No managed APs discovered')],
                   retry=5,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname, 'Step 6', res1)

################################################################################
#Step 7
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 7',
          'Recover initial config')

# operate		  
#恢复AC1配置
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list',Vlan70)
SetCmd(switch1,'discovery method ip-poll')
SetCmd(switch1,'discovery method l2-multicast')
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

#恢复AC2配置
EnterWirelessMode(switch2)
SetCmd(switch2,'no discovery vlan-list',Vlan70)
SetCmd(switch2,'no enable')
IdleAfter(1)
SetCmd(switch2,'enable')

#恢复S3配置
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'no shutdown')
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p4)
SetCmd(switch3,'no shutdown')

#end
printTimer(testname, 'End')