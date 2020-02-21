#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.3.py - test case 3.1.3 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2017-12-26 10:20:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.3 AP获取IP地址
# 测试目的：测试AP可以通过DHCP和静态指定两种方式获取IP地址
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.3'

avoiderror(testname)
printTimer(testname,'Start','Test AP acquire IP Address')

################################################################################
#Step 1
#
#操作
# AP恢复出厂后，在AP上查看AP dhcp的状态
#
#预期
# dhcp-status状态显示为up
################################################################################

printStep(testname,'Step 1',
          'Check AP1 dhcp status after AP1 factory reset',
          'Check the result')

# operate		  
RebootAp(setdefaut=True, AP=ap1)
IdleAfter(5)

#check
res1 = Check_ap_dhcpstatus(ap1,Ap1cmdtype,type='up')

#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
# 在AP上把AP dhcp状态down掉，查看AP的IP地址
#
#预期
# 查看AP的IP地址显示为默认出厂IP:192.168.1.10
################################################################################

printStep(testname,'Step 2',
          'Check AP1 ip address after config AP1 dhcp status down',
          'Check the result')

# operate
ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_down')
IdleAfter(10)
	
#check
res1 = Check_ap_ip(ap1,Ap1cmdtype,'192.168.1.10',mode='ip',ipversion='ipv4')	

#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
#在AP上配置静态IP地址
#
#预期
#查看AP static-ip地址显示为:1.1.1.1
################################################################################

printStep(testname,'Step 3',
          'Check AP1 ip address after config a static ip address on AP1',
		  'Check the result')		  

# operate	
ApSetcmd(ap1,Ap1cmdtype,'set_static_ip','1.1.1.1')	
IdleAfter(10)

#check
res1 = Check_ap_ip(ap1,Ap1cmdtype,'1.1.1.1',mode='staticip',ipversion='ipv4')	

#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
# 在S3上配置vlan70的接口IP,并配置AP的地址池
#
#预期
#查看AP IP地址显示为从dhcp server服务器获取的IP
################################################################################

printStep(testname,'Step 4',
          'Config AP dhcp pool on S3',
          'Check the result')

# operate		  
EnterConfigMode(switch3)
SetCmd(switch3,'interface vlan',Vlan70)
SetCmd(switch3,'ip address',If_vlan70_s3_ipv4)

EnterConfigMode(switch3)
SetCmd(switch3,'ip dhcp pool AP')
SetCmd(switch3,'network-address',Dhcp_ap_pool_ipv4)
SetCmd(switch3,'default-router',If_vlan70_s3_ipv4_s)

EnterConfigMode(switch3)
SetCmd(switch3,'no service dhcp')
SetCmd(switch3,'service dhcp')
IdleAfter(5)

ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_up')
IdleAfter(60)

#check
res1 = Check_ap_ip(ap1,Ap1cmdtype,Dhcp_ap_pool_ipv4_1,mode='dhcp',ipversion='ipv4')

#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 5',
          'Recover initial config')

# operate		  
#恢复AP的配置
ApSetcmd(ap1,Ap1cmdtype,'set_static_ip',Ap1_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6',Ap1_ipv6)
ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_down')
ApSetcmd(ap1,Ap1cmdtype,'set_dhcpv6_down')
ApSetcmd(ap1,Ap1cmdtype,'set_ip_route',If_vlan70_s3_ipv4_s)
ApSetcmd(ap1,Ap1cmdtype,'set_ipv6_route',If_vlan70_s3_ipv6_s)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6_prefix_len','64')
ApSetcmd(ap1,Ap1cmdtype,'saverunning')

#恢复s3的配置
EnterConfigMode(switch3)
SetCmd(switch3,'no ip dhcp pool AP')
SetCmd(switch3,'no interface vlan',Vlan70)
		  
#end
printTimer(testname, 'End')