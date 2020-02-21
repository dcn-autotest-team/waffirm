#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_6.1.1.py - test case 6.1.1 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2016 Digital China Networks Co. Ltd
# 
# Date 2016-04-21 14:37:33
#
# Features:
# 6.1.1	lan port vlan功能测试（二层转发）
# 测试目的：测试lan port vlan功能
# 测试环境：同测试拓扑
# 测试描述：测试pc连接lan口后二层数据能够被正常转发
#
#*******************************************************************************
# Change log:
#     - modified by zhangjxp 2017.11.13 RDM50358 修改step2
#*******************************************************************************

#Package

#Global Definition
#Source files
#Procedure Definition 

#Functional Code

if hwtype1 == '33':  
	testname = 'TestCase 6.1.1'
	avoiderror(testname)
	printTimer(testname,'Start','test L2 switch in lan port mode')

	suggestionList = []

	################################################################################
	#Step 1
	#操作
	# 修改AP1的管理vlan为vlan20，untagged-vlan为vlan 20。
	# 修改三层交换机连接AP1的端口为trunk口，native vlan为vlan 20。
	# 在AC1 ap profile 1 中配置lan port 1 vlan 4092
	# 配置下发到AP1
	#预期
	#AP1能够被AC1管理，配置下发成功
	# ################################################################################
	printStep(testname,'Step 1',
              'Set AP1 management vlan-id to vlan 20,and untagged',
              'Set ap profile 1 lan port 1 vlan 4092')
	res1=1
	#operate
	EnterWirelessMode(switch1)
	EnterApProMode(switch1,'1')
	SetCmd(switch1,'management vlan',Vlan20)
	SetCmd(switch1,'ethernet native-vlan 20')
	SetCmd(switch1,'lan port 1 vlan 4092')
	SetCmd(switch1,'lan port 2 vlan 4092')
	SetCmd(ap1,'set management vlan-id',Vlan20)
	SetCmd(ap1,'set untagged-vlan vlan-id',Vlan20)
	EnterConfigMode(switch1)
	SetCmd(switch1,'ip dhcp pool pool4091')
	SetCmd(switch1,'no default-router')
	#配置s3p3为Trunk 口,native vlan
	EnterInterfaceMode(switch3,s3p3)
	SetCmd(switch3,'switchport mode trunk')
	SetCmd(switch3,'switchport trunk native vlan',Vlan20)
	SetCmd(switch3,'switchport trunk allowed vlan 20,4092')
	EnterInterfaceMode(switch3,s3p1)
	SetCmd(switch3,'switchport mode trunk')
	SetCmd(switch3,'switchport trunk native vlan',Vlan40)
	SetCmd(switch3,'switchport trunk allowed vlan 40,4092')
	#S3 上配置 vlan 4092
	EnterConfigMode(switch3)
	SetCmd(switch3,'vlan 4092')
	#配置s1p1为Trunk 口,native vlan为40
	EnterInterfaceMode(switch1,s1p1)
	SetCmd(switch1,'switchport mode trunk')
	SetCmd(switch1,'switchport trunk native vlan',Vlan40)
	SetCmd(switch1,'switchport trunk allowed vlan 40,4092')
	#配置下发到AP1
	WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
	EnterEnableMode(switch1)
	data1 = SetCmd(switch1,'show wireless ap status')
	# EnterInterfaceMode(switch1,'vlan '+Vlan4092)
	# SetCmd(switch1,'shut')
	# IdleAfter(5)
	# SetCmd(switch1,'no shut')
	# IdleAfter(15)
	#check
	res1 = CheckLine(data1,ap1mac,Ap1_ipv4,'Managed','Success',IC=True)
	#result
	printCheckStep(testname, 'Step 1',res1)

	################################################################################
	#Step 2
	#操作
	#pc2、pc3获取地址
	#
	#预期
	#关联成功。客户端能够获取192.168.92.X网段的IP地址
	################################################################################

	printStep(testname,'Step 2',
              'pc2 and pc3 connect to Lan',
              'Check if AP3 can obtain 192.168.92.x address via dhcp')
	res1 = res2 = 1
	pc2_ipv4='2.2.2.2'
	pc3_ipv4='3.3.3.3'
	SetCmd(pc1,'\n')
	SetCmd(pc1,'dhclient eth2 -r') 
	SetCmd(pc1,'ifconfig eth2 up')
	SetCmd(pc1,'dhclient eth2')
	data1 = SetCmd(pc1,'ifconfig eth2',timeout=5)  
	pc2_ipv4result = re.search('inet addr:(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
	if pc2_ipv4result:
		pc2_ipv4 = pc2_ipv4result.group(1)
	SetCmd(pc1,'dhclient eth3 -r') 
	SetCmd(pc1,'ifconfig eth3 up')
	SetCmd(pc1,'dhclient eth3')
	data2 = SetCmd(pc1,'ifconfig eth3',timeout=5)  
	pc3_ipv4result = re.search('inet addr:(\d+\.\d+\.\d+\.\d+)\s+',data2,re.I)
	if pc3_ipv4result:
		pc3_ipv4 = pc3_ipv4result.group(1)	
	if pc2_ipv4.find(Dhcp_pool2) != -1:
		res1 = 0
		print 'pc2 ipv4 address is :'+pc2_ipv4
	if pc3_ipv4.find(Dhcp_pool2) != -1:
		res2 = 0
		print 'pc3 ipv4 address is :'+pc3_ipv4	
	#result
	printCheckStep(testname, 'Step 2',res1,res2)

	################################################################################
	#Step 3
	#操作
	# AC1 ping pc2和pc3
	#
	#预期
	#能够 ping 通
	################################################################################
	printStep(testname,'Step 3',
              'pc2 and pc3 ping AC1')

	res1=1
	res2=1
	#check
	res1 = CheckPing(switch1,pc2_ipv4,srcip=If_vlan4092_s1_ipv4)
	res2 = CheckPing(switch1,pc3_ipv4,srcip=If_vlan4092_s1_ipv4)
	#result
	printCheckStep(testname,'Step 3',res1,res2)

	################################################################################
	#Step 4
	#操作
	#恢复默认配置
	################################################################################
	printStep(testname,'Step 4',
              'Recover initial config')
	#operate

	#清除management vlan 配置
	EnterWirelessMode(switch1)
	EnterApProMode(switch1,'1')
	SetCmd(switch1,'no','management vlan')
	SetCmd(switch1,'ethernet native-vlan 1')
	SetCmd(switch1,'no lan port 1 vlan')
	SetCmd(switch1,'no lan port 2 vlan')
	SetCmd(ap1,'set management vlan-id',1)
	SetCmd(ap1,'set untagged-vlan vlan-id',1)

	#恢复拓扑配置
	#AC1
	EnterNetworkMode(switch1,'1')
	SetCmd(switch1,'ssid ' + Network_name1)
	SetCmd(switch1,'vlan ' + Vlan4091)
	EnterInterfaceMode(switch1,s1p1)
	SetCmd(switch1,'no switchport mode')
	SetCmd(switch1,'switchport access vlan',Vlan40)
	EnterWirelessMode(switch1)
	SetCmd(switch1,'l2tunnel vlan-list add 4091-4094')
	EnterApProMode(switch1,'1')
	SetCmd(switch1,'no lan port vlan')
	EnterConfigMode(switch1)
	SetCmd(switch1,'ip dhcp pool pool4091')
	SetCmd(switch1,'default-router ' + If_vlan4091_s1_ipv4)
	#S3
	EnterInterfaceMode(switch3,s3p1)
	SetCmd(switch3,'no switchport mode')
	SetCmd(switch3,'switchport access vlan',Vlan40)
	EnterInterfaceMode(switch3,s3p3)
	SetCmd(switch3,'no switchport mode')
	SetCmd(switch3,'switchport access vlan',Vlan20)
	EnterInterfaceMode(switch3,'vlan '+Vlan20)

	#S3 上删除 vlan 4092
	EnterConfigMode(switch3)
	SetCmd(switch3,'no vlan 4092')
	#配置下发到AP1
	i=0
	while i<10:
		data = SetCmd(switch1,'show wireless ap status')
		res1 = CheckLine(data,ap1mac,Ap1_ipv4,'1','Managed','Success',IC=True)
		if res1 == 0:
			break
		IdleAfter(15)
		i=i+1
	WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])    
	printTimer(testname, 'End')
