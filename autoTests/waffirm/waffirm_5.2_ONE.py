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
#     - 2017.2.27 lupingc RDM46364 修改step1
#     - 2017.3.14 lupingc RDM48869 修改step1
#     - 2017.8.23 zhangjxp RDM49910、49725修改step3
#     - 2017.10.27 zhangjxp RDM50249 修改step3,先检测AP上是否通过DHCP成功获取了AC的IP，
#                           再检测AC是否成功管理了AP
#     - 2017.11.10 zhangjxp RDM50304 修改step3
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 5.2'
avoiderror(testname)
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
printStep(testname,'Step 1',
          'set managed-ap managed-type 1 on ap1')
#operate
if EnvNo == '1':
	option43 = '01040101010B'
if EnvNo == '2':
	option43 = '010401010115'
if EnvNo == '3':
	option43 = '01040101011F'
if EnvNo == '4':
	option43 = '010401010129'	

EnterConfigMode(switch1)
SetCmd(switch1,'service dhcp')
SetCmd(switch1,'ip dhcp server option60 check enable')
SetCmd(switch1,'ip dhcp pool a')
SetCmd(switch1,'network-address ' + '.'.join(If_vlan20_s1_ipv4.split('.')[:-1]) + '.0 255.255.255.0')
SetCmd(switch1,'default-router ' + If_vlan20_s1_ipv4)
SetCmd(switch1,'option 43 hex '+option43)
SetCmd(switch1,'option 60 ascii udhcp ' +dhcp_option60_version)

#AC1上创建vlan20 及三层接口,s1p1划入vlan 20
EnterConfigMode(switch1)
SetCmd(switch1,'vlan',Vlan20)
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport access vlan',Vlan20)
EnterInterfaceMode(switch1,'vlan '+Vlan20)
IdleAfter(Vlan_Idle_time)
SetIpAddress(switch1,If_vlan20_s1_ipv4,'255.255.255.0')

#s3p1划入 vlan20
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport access vlan',Vlan20)

data1 = ShowRun(switch1)
res1 = CheckLineList(data1,['ip dhcp server option60 check enable','ip dhcp pool a','option 43 hex '+option43,'option 60 ascii udhcp '+dhcp_option60_version])

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

printStep(testname,'Step 2',
          'Remove configuration of auto discovery on ac1')

EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery ip-list')
SetCmd(switch1,'no discovery ipv6-list')
SetCmd(switch1,'no discovery vlan-list')
data1 = ShowRun(switch1)
res1 = CheckLineList(data1,['discovery ipv6-list','discovery ip-list'])
res2 = CheckLine(data1,'no discovery vlan-list')

#result
printCheckStep(testname, 'Step 2',not res1,res2)

################################################################################
#Step 3
#操作
#配置AP通过dhcp获取地址
#WLAN-AP# set management dhcp-status up
#AP1主动发现AC，并与AC关联
#预期
#AP1成功获取地址，get managed-ap能看到dhcp-switch-address-1为1.1.1.1
#AC1上用命令show wireless ap < AP1MAC > status显示“Discovery Reason”为“Switch IP DHCP”
################################################################################
printStep(testname,'Step 3',
          'Config ap set management dhcp-status up')

SetCmd(ap1,'set management static-ip 192.168.1.10')
SetCmd(ap1,'set management dhcp-status up')
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap1,ap1mac,switch1)
IdleAfter(20)
res1=CheckSutCmd(ap1,'get managed-ap',
                 check=[('dhcp-switch-address-1\s+'+StaticIpv4_ac1)],
                 waittime=10,retry=10,interval=5,IC=True)
i = 1
while i<10:
	EnterEnableMode(switch1)
	data1 = SetCmd(switch1,'show wireless ap status')
	res = CheckLine(data1,ap1mac,Ap1_ipv4,'1','Managed','Success',IC=True)
	if res == 0:
		break
	IdleAfter('5')
	i = i + 1

data1 = SetCmd(switch1,'show wireless ap',ap1mac,'status')

res2 = CheckLine(data1,'Discovery Reason','Switch IP DHCP',IC=True)

printCheckStep(testname, 'Step 3',res1,res2)

################################################################################
#Step 4
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 4',
          'Recover initial config for switches.')

EnterConfigMode(switch1)
SetCmd(switch1,'no','ip dhcp server option60 check enable')
SetCmd(switch1,'no ip dhcp pool a')

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',Ap1_ipv4)
SetCmd(switch1,'discovery ipv6-list',Ap1_ipv6)

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',Ap2_ipv4)
SetCmd(switch1,'discovery ipv6-list',Ap2_ipv6)
# EnterWirelessMode(switch1)
# SetCmd(switch1,'l2tunnel vlan-list add',Vlan4091 + '-' + Vlan4093)

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