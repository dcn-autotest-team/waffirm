#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_5.2.py - test case 5.2 of waffirm
#
# Author:  qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 5.2 DHCP Option60/43
# 测试目的：测试AP通过dhcp option60/43发现并关联AC。
# 测试环境：同测试拓扑
# 测试描述：测试AP1通过dhcp option60/43发现并关联AC1。（AP1的MAC地址：AP1MAC）
#
#*******************************************************************************
# Change log:
#
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 5.2'
printTimer(testname,'Start','Test manage ap via dhcp option 60 43')

################################################################################
#Step 1
#操作
#配置AC1的dhcp相关配置
#service dhcp
#ip dhcp server option60 check enable
#ip dhcp pool a
#network-address 20.1.1.0 255.255.255.0
#default-router 20.1.1.2
#option 43 hex 010401010101
#option 60 ascii udhcp 1.18.2
#配置成功。在AC上面show running-config可以看到相关的配置。
################################################################################
printStep(testname,'Step 1',\
          'set managed-ap managed-type 1 on ap1')
#operate
EnterConfigMode(switch3)
SetCmd(switch3,'ip dhcp pool a')
SetCmd(switch3,'network-address ' + '.'.join(If_vlan20_s1_ipv4.split('.')[:-1]) + '.0 255.255.255.0')
SetCmd(switch3,'default-router ' + If_vlan20_s3_ipv4)
CMD_Option43Hex = CMD_Option43Hex = 'option 43 hex 01040101010'
CMD_Option43Hex = CMD_Option43Hex + StaticIpv4_ac1[-1]
SetCmd(switch3,'option 43 hex 010428010101')
data1 = ShowRun(switch3)
res1 = CheckLineList(data1,["ip dhcp pool a","option 43 hex 01042801010" + StaticIpv4_ac1[-1],])

#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#清空AC上的自动发现ip和vlan的配置
#no discovery ip-list
#no discovery ipv6-list
#no discovery vlan-list
#配置成功。在AC上面Show running-config可以看到相关的配置。
################################################################################

printStep(testname,'Step 2',\
          'Remove configuration of auto discovery on ac1')

EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery ip-list')
SetCmd(switch1,'no discovery ipv6-list')
SetCmd(switch1,'no discovery vlan-list')
data1 = ShowRun(switch1)
res1 = CheckLineList(data1,['discovery ipv6-list','discovery ip-list'])
res2 = CheckLine(data1,'no discovery vlan-list')

#result
printCheckStep(testname, 'Step 2',not res1)

################################################################################
#Step 3 Step 4
#操作
#配置AP通过dhcp获取地址
#WLAN-AP# set management dhcp-status up
#AP1主动发现AC，并与AC关联
#预期
#AP1成功获取地址，get managed-ap能看到dhcp-switch-address-1为1.1.1.1
#AC1上用命令show wireless ap < AP1MAC > status显示“Discovery Reason”为“Switch IP DHCP”
################################################################################
printStep(testname,'Step 3,Step 4',\
          'Config ap set management dhcp-status up')

SetCmd(ap1,'set management static-ip 192.168.1.10')
IdleAfter('5')
SetCmd(ap1,'set management dhcp-status up')
EnterConfigMode(switch3)
SetCmd(switch3,'interface ' + s3p3)
SetCmd(switch3,'shutdown')
IdleAfter('120')
SetCmd(switch3,'no shutdown')
IdleAfter(Apply_profile_wait_time)
IdleAfter('60')
data1 = SetCmd(ap1,'get managed-ap')
res1 = CheckLine(data1,'dhcp-switch-address-1\s+'+StaticIpv4_ac1)
SetCmd(switch1,'show wi ap st')
data1 = SetCmd(switch1,'show wireless ap',ap1mac,'status')

res2 = CheckLine(data1,'Discovery Reason','Switch IP DHCP',IC=True)

printCheckStep(testname, 'Step 3 Step 4',res1,res2)

################################################################################
#Step 5
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 5',\
          'Recover initial config for switches.')

EnterConfigMode(switch1)
SetCmd(switch3,'no','ip dhcp server option60 check enable')
SetCmd(switch3,'no ip dhcp pool a')

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',Ap1_ipv4)
SetCmd(switch1,'discovery ipv6-list',Ap1_ipv6)

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',Ap2_ipv4)
SetCmd(switch1,'discovery ipv6-list',Ap2_ipv6)
EnterWirelessMode(switch1)
SetCmd(switch1,'l2tunnel vlan-list add',Vlan4091 + '-' + Vlan4093)

#s3p1 划入vlan40
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport access vlan',Vlan40)
#AC1恢复
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan',Vlan20)
SetCmd(switch1,'no vlan',Vlan20)
SetCmd(switch1,'vlan',Vlan40)
SetCmd(switch1,'switchport interface',s1p1)

SetCmd(ap1,'set management static-ip',Ap1_ipv4)
SetCmd(ap1,'set management dhcp-status down')
SetCmd(ap1,'set static-ip-route gateway',If_vlan20_s3_ipv4)
SetCmd(ap1,'save-running')

IdleAfter(Apply_profile_wait_time)

printTimer(testname, 'End')