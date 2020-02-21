#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.1.5.py - test case 4.1.5 of waffirm_new
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
# 4.1.5	AC间三层发现（IPv6）
# 测试目的：测试AC可以通过三层发现建立集群
# 测试环境：同测试拓扑
# 测试描述：在AC2通过配置ipv6发现列表发现AC1。
#（AC1的wireless地址是2001::1；AP1的MAC地址：AP1MAC；AC2的wireless地址是2003::1）
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

testname = 'TestCase 4.1.5'
avoiderror(testname)
printTimer(testname,'Start','test automatic discovery between AC1 and AC2 via ipv6')

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

#由于之前可能存在v4的发现,虽然已经no掉v4的discovery ip-list,但发现状态不会消失，
#因此先no掉AC之间的v4 ip 连接,避免v4对v6的影响
EnterInterfaceMode(switch2,'vlan 30')
SetCmd(switch2,'no ip address',If_vlan30_s2_ipv4,'255.255.255.0')
EnterWirelessMode(switch2)
SetCmd(switch2,'no static-ip')
IdleAfter(60)
#check
EnterEnableMode(switch1)
res1=CheckSutCmd(switch1,'show wireless peer-switch',
                 check=[('No peer wireless switch exist')],
                 waittime=5,retry=10,interval=3,IC=True)

#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
# 操作
# 在AC2上配置集群优先级2，把AC1的无线地址加入ip发现列表
# AC2(config-wireless)#cluster-priority 2
# AC2(config-wireless)#discovery ip-list 2001::1
#
#预期
#AC2上show wireless discovery ip-list看到ip发现列表“IP Address”中有2001::1”
################################################################################
printStep(testname,'Step 2',
          'Config AC2 cluster priority to 2',
          'Add AC1\'s static-ipv6 to discovery ipv6-list')

res1=1
#operate
EnterWirelessMode(switch2)
SetCmd(switch2,'cluster-priority','2')

#添加v6路由
#AC1
EnterConfigMode(switch1)
SetCmd(switch1,'ipv6 route',StaticIpv6_ac2 + '/128',If_vlan40_s3_ipv6)
SetCmd(switch1,'ipv6 route',If_vlan30_s2_ipv6 + '/64',If_vlan40_s3_ipv6)
#AC2
EnterConfigMode(switch2)
SetCmd(switch2,'ipv6 route',StaticIpv6_ac1 + '/128',If_vlan30_s3_ipv6)
SetCmd(switch2,'ipv6 route',If_vlan40_s1_ipv6 + '/64',If_vlan30_s3_ipv6)
#S3
EnterConfigMode(switch3)
SetCmd(switch3,'ipv6 route',StaticIpv6_ac2 + '/128',If_vlan30_s2_ipv6)
SetCmd(switch3,'ipv6 route',StaticIpv6_ac1 + '/128',If_vlan40_s1_ipv6)

#把AC1的无线地址加入ip发现列表
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery ipv6-list',StaticIpv6_ac1)
EnterEnableMode(switch2)
data1 = SetCmd(switch2,'show wireless discovery ip-list',timeout=5)

#check
res1 = CheckLine(data1,StaticIpv6_ac1)

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
# AC2上show wireless peer-switch显示有'IP Address'为'2001::1'的peer-switch，
# show wireless ap status显示的关联AP的mac地址'AP1MAC'前有'*'标记
################################################################################
printStep(testname,'Step 3',
          'Wait 1 minute',
          'Show wireless peer-switch and ap status on AC2')

res1=res2=1

#operate
IdleAfter(60)
#check
EnterEnableMode(switch2)
res1=CheckSutCmd(switch2,'show wireless peer-switch',
                 check=[(StaticIpv6_ac1)],
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
#AC1上show wireless peer-switch显示有'IP Address'为'2003::1'的peer-switch。
################################################################################
printStep(testname,'Step 4',
          'Show peer-switch on AC1')

res1=1
#operate
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless peer-switch',timeout=5)

#check
res1 = CheckLine(data1,StaticIpv6_ac2,IC=True)

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
IdleAfter(5)
SetCmd(switch2,'no discovery ipv6-list',StaticIpv6_ac1)
#恢复v4三层接口
EnterInterfaceMode(switch2,'vlan 30')
SetCmd(switch2,'ip address',If_vlan30_s2_ipv4,'255.255.255.0')
EnterWirelessMode(switch2)
SetCmd(switch2,'static-ip',StaticIpv4_ac2)

#删除v6路由
#AC1
EnterConfigMode(switch1)
SetCmd(switch1,'no','ipv6 route',StaticIpv6_ac2 + '/128',If_vlan40_s3_ipv6)
SetCmd(switch1,'no','ipv6 route',If_vlan30_s2_ipv6 + '/64',If_vlan40_s3_ipv6)
#AC2
EnterConfigMode(switch2)
SetCmd(switch2,'no','ipv6 route',StaticIpv6_ac1 + '/128',If_vlan30_s3_ipv6)
SetCmd(switch2,'no','ipv6 route',If_vlan40_s1_ipv6 + '/64',If_vlan30_s3_ipv6)
#S3
EnterConfigMode(switch3)
SetCmd(switch3,'no','ipv6 route',StaticIpv6_ac2 + '/128',If_vlan30_s2_ipv6)
SetCmd(switch3,'no','ipv6 route',StaticIpv6_ac1 + '/128',If_vlan40_s1_ipv6)

#RDM37511
EnterWirelessMode(switch2)
SetCmd(switch2,'peer-group 2')
IdleAfter(5)
SetCmd(switch2,'peer-group 1')

IdleAfter(60)
#end
printTimer(testname, 'End')