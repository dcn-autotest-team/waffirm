#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.1.3.py - test case 4.1.3 of waffirm_new
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
# 4.1.3	AC间二层自动发现
# 测试目的：测试AC可以通过二层发现建立集群
# 测试环境：同测试拓扑
# 测试描述：在AC2通过配置vlan发现列表发现peer AC（AP1的MAC地址：AP1MAC）
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

testname = 'TestCase 4.1.3'
avoiderror(testname)
printTimer(testname,'Start','test automatic discovery between AC1 and AC2 via L2')

################################################################################
#Step 1
#
#操作
# S3上把s3p2、s3p1加入vlan 20
# S3(config-if-ethernet s3p2)# switchport access vlan 20
# AC2上，配置vlan20，把S2p1加入vlan 20
# AC1上面创建vlan20，将端口s1p1划入vlan20
#
#预期
#配置成功
#
################################################################################
printStep(testname,'Step 1',
          'Switchport s3p2 and s3p1 access to vlan 20 ',
          'Switchport s2p1 access to vlan 20',
          'Switchport s1p1 access to vlan 20')

res1=res2=res3=1
#operate

#S3
EnterConfigMode(switch3)
SetCmd(switch3,'vlan',Vlan20)
SetCmd(switch3,'switchport interface',s3p2)
SetCmd(switch3,'switchport interface',s3p1)

#AC1
EnterConfigMode(switch1)
SetCmd(switch1,'vlan',Vlan20)
SetCmd(switch1,'switchport interface',s1p1)
EnterInterfaceMode(switch1,'vlan '+Vlan20)
IdleAfter(3)
SetCmd(switch1,'ip address 20.1.1.100 255.255.255.0')

#AC2
EnterConfigMode(switch2)
SetCmd(switch2,'vlan',Vlan20)
SetCmd(switch2,'switchport interface',s2p1)
EnterInterfaceMode(switch2,'vlan '+Vlan20)
IdleAfter(3)
SetCmd(switch2,'ip address 20.1.1.200 255.255.255.0')

EnterEnableMode(switch1)
EnterEnableMode(switch2)
EnterEnableMode(switch3)
data1 = SetCmd(switch1,'show vlan id',Vlan20,timeout=3)
data2 = SetCmd(switch2,'show vlan id',Vlan20,timeout=3)
data3 = SetCmd(switch3,'show vlan id',Vlan20,timeout=3)

#check
res1 = CheckLine(data1,s1p1)
res2 = CheckLine(data2,s2p1)
res3 = CheckLineList(data3,[(s3p2),(s3p1)])
#result
printCheckStep(testname, 'Step 1', res1,res2,res3)

################################################################################
#Step 2
#操作
# AC2上固定无线地址为20.1.1.200
# AC2(config-wireless)#no auto-ip-assign 
# AC2(config-wireless)#static-ip 20.1.1.200
#
#预期
#AC2上show wireless看到'WS IP Address' 更新为 '20.1.1.200'
################################################################################
printStep(testname,'Step 2',
          'Config AC2 static wireless ip 20.1.1.200',
          'Check if AC1 managed AP1')

res1=1
#operate
EnterWirelessMode(switch2)
SetCmd(switch2,'no auto-ip-assign')
SetCmd(switch2,'static-ip 20.1.1.200')

IdleAfter(10)
data1 = SetCmd(switch2,'show wireless',timeout=5)

#check
res1 = CheckLine(data1,'WS IP Address','20.1.1.200',IC=True)

#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
# 在AC1上查看peer AC
# S1#show wireless peer-switch
#
#预期
#AC1上show wireless peer-switch显示“No peer wireless switch exists”
################################################################################
printStep(testname,'Step 3',
          'Show peer-switch on AC1')

res1=1
#operate
IdleAfter(60)
#check
EnterEnableMode(switch1)
res1=CheckSutCmd(switch1,'show wireless peer-switch',
                 check=[('No peer wireless switch exists')],
                 waittime=5,retry=10,interval=5,IC=True)
                
CheckSutCmd(switch1,'show wireless ap status',
            check=[(ap1mac,'Managed','Success')],
            waittime=5,retry=20,interval=5,IC=True)

#result
printCheckStep(testname, 'Step 3',res1)

################################################################################
#Step 4
#操作
# 在AC2上配置集群优先级2，把vlan 20加入vlan发现列表
# AC2(config-wireless)#cluster-priority 2
# AC2(config-wireless)#discovery vlan-list 20
#
#预期
#AC2上show wireless discovery vlan-list看到vlan发现列表“VLAN”中有“20”
################################################################################
printStep(testname,'Step 4',
          'Config AC2 cluster priority to 2,'
          'Add vlan 20 to L2 discovery list,')
          
res1=1
#operate
EnterWirelessMode(switch2)
SetCmd(switch2,'cluster-priority 2')

#把vlan 20加入vlan发现列表
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery vlan-list',Vlan20)
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery vlan-list',Vlan20)

data1 = SetCmd(switch2,'show wireless discovery vlan-list',timeout=5)

#check
res1 = CheckLine(data1,Vlan20,'vlan',IC=True)

#result
printCheckStep(testname, 'Step 4',res1)

################################################################################
#Step 5
#操作
# 等待1分钟后，在AC2上查看peer AC
# AC2#show wireless peer-switch。
# 在AC2上查看AP状态
# AC2#show wireless ap status
#
#预期
# AC2上show wireless peer-switch显示有'IP Address'为'1.1.1.1'的peer-switch，
#'Discovery Reason”显示为 'L2 Poll'。
# show wireless ap status显示的关联AP的mac地址'AP1MAC'前有'*'标记
################################################################################
printStep(testname,'Step 5',
          'Wait 1 minute',
          'Show wireless peer-switch and ap status on AC2')

res1=res2=1

#operate
IdleAfter(60)
# check
EnterEnableMode(switch2)
res1=CheckSutCmd(switch2,'show wireless peer-switch',
                 check=[(StaticIpv4_ac1,'L2 Poll')],
                 waittime=10,retry=10,interval=5,IC=True)
res2=CheckSutCmd(switch2,'show wireless ap status',
                 check=[('\*' + ap1mac,'Managed','Success')],
                 waittime=5,retry=10,interval=5,IC=True)
#result
printCheckStep(testname, 'Step 5', res1,res2)

################################################################################
#Step 6
#
#操作
# 在AC1上查看peer AC
# S1#show wireless peer-switch
#
#预期
#AC1上show wireless peer-switch显示有“IP Address”为“20.1.1.200”的peer-switch。
################################################################################
printStep(testname,'Step 6',
          'Show peer-switch on AC1')

res1=1
#operate
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless peer-switch')

#check
res1 = CheckLine(data1,'20.1.1.200','L2 Poll',IC=True)

#result
printCheckStep(testname, 'Step 6',res1)

################################################################################
#Step 7
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 7',
          'Recover initial config')

#operate

#AC2恢复
EnterWirelessMode(switch2)

#恢复cluster priority值为1，此后 controller 会切换为AC1
SetCmd(switch2,'no cluster-priority')
SetCmd(switch2,'static-ip',StaticIpv4_ac2)
SetCmd(switch2,'no discovery vlan-list',Vlan20)

EnterConfigMode(switch2)
SetCmd(switch2,'vlan',Vlan30)
SetCmd(switch2,'switchport interface',s2p1)
EnterConfigMode(switch2)
SetCmd(switch2,'no interface vlan',Vlan20)
SetCmd(switch2,'no vlan',Vlan20)
EnterConfigMode(switch2)

#S3
EnterInterfaceMode(switch3,s3p2)
SetCmd(switch3,'switchport access vlan',Vlan30)
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport access vlan',Vlan40)
EnterEnableMode(switch3)

#AC1
#删除discovery vlan-list 20的配置
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list',Vlan20)

EnterConfigMode(switch1)
SetCmd(switch1,'vlan',Vlan40)
SetCmd(switch1,'switchport interface',s1p1)
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan',Vlan20)
SetCmd(switch1,'no vlan',Vlan20)
#RDM37511
EnterWirelessMode(switch2)
SetCmd(switch2,'peer-group 2')
IdleAfter(5)
SetCmd(switch2,'peer-group 1')
IdleAfter(60)

#end
printTimer(testname, 'End')