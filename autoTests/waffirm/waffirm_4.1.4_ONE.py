#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.1.4.py - test case 4.1.4 of waffirm_new
#
# Author:  (jinpfb)
#
# Version 1.0.0
#
# Date:  2012-12-7 13:47:23
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 4.1.4	AC间三层发现
# 测试目的：测试AC可以通过三层发现建立集群
# 测试环境：同测试拓扑
# 测试描述：在AC2通过配置ip发现列表发现AC1。
#（AC1的wireless地址是1.1.1.1；AP1的MAC地址：AP1MAC；AC2的wireless地址是2.2.2.2）
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package

#Global Definition
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.1.4'
avoiderror(testname)
printTimer(testname,'Start','test automatic discovery between AC1 and AC2 via L3')

################################################################################
#Step 1
#
#操作
# 在AC1上查看peer AC
# S1#show wireless peer-switch
#
#预期
#AC1上show wireless peer-switch显示“No peer wireless switch exists”
################################################################################
printStep(testname,'Step 1',
          'Show peer-switch on AC1')

res1=1
#operate
EnterEnableMode(switch1)
res1=CheckSutCmd(switch1,'show wireless peer-switch',
                 check=[('No peer wireless switch exists')],
                 waittime=5,retry=20,interval=5,IC=True)

#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
# 操作
# 在AC2上配置集群优先级2，把AC1的无线地址加入ip发现列表
# AC2(config-wireless)#cluster-priority 2
# AC2(config-wireless)#discovery ip-list 1.1.1.1
#
#预期
#AC2上show wireless discovery ip-list看到ip发现列表“IP Address”中有1.1.1.1”
################################################################################
printStep(testname,'Step 2',
          'Config AC2 cluster priority to 2',
          'Add AC1\'s static-ip to discovery ip-list')

res1=1
#operate
EnterWirelessMode(switch2)
SetCmd(switch2,'cluster-priority 2')

#把AC1的无线地址加入ip发现列表
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery ip-list',StaticIpv4_ac1)
EnterEnableMode(switch2)
data1 = SetCmd(switch2,'show wireless discovery ip-list',timeout=5)

#check
res1 = CheckLine(data1,StaticIpv4_ac1)

#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#操作
# 等待1分钟后，在AC2上查看peer AC
# AC2#show wireless peer-switch。
# 在AC2上查看AP状态
# AC2#show wireless ap status
#
#预期
# AC2上show wireless peer-switch显示有'IP Address'为'1.1.1.1'的peer-switch，
#'Discovery Reason”显示为 'IP Poll'。
# show wireless ap status显示的关联AP的mac地址'AP1MAC'前有'*'标记
#如果show表项为空，则等待30秒后再次show wireless ap status后作出判断。
################################################################################
printStep(testname,'Step 3',
          'Wait 1 minute',
          'Show wireless peer-switch and ap status on AC2')

res1=res2=1

#operate
IdleAfter(60)
EnterEnableMode(switch2)
res1=CheckSutCmd(switch2,'show wireless peer-switch',
                 check=[(StaticIpv4_ac1,'IP Poll')],
                 waittime=5,retry=16,interval=5,IC=True)
res2=CheckSutCmd(switch2,'show wireless ap status',
                 check=[('\*' + ap1mac,'Managed','Success')],
                 waittime=5,retry=10,interval=5,IC=True)

#result
printCheckStep(testname, 'Step 3', res1,res2)

################################################################################
#Step 4
#
#操作
# 在AC1上查看peer AC
# S1#show wireless peer-switch
#
#预期
#AC1上show wireless peer-switch显示有'IP Address'为'2.2.2.2'的peer-switch。
################################################################################
printStep(testname,'Step 4',
          'Show peer-switch on AC1')

res1=1
#operate
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless peer-switch',timeout=5)

#check
res1 = CheckLine(data1,StaticIpv4_ac2,IC=True)

#result
printCheckStep(testname, 'Step 4',res1)

################################################################################
#Step 5
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 5',
          'Recover initial config')

#operate

#AC2恢复
EnterWirelessMode(switch2)
#恢复cluster priority值为1，此后 controller 会切换为AC1
SetCmd(switch2,'no cluster-priority')

SetCmd(switch2,'no discovery ip-list',StaticIpv4_ac1)

#RDM36880
SetCmd(switch2,'peer-group 2')
IdleAfter(20)
SetCmd(switch2,'peer-group 1')

IdleAfter(60)
#end
printTimer(testname, 'End')