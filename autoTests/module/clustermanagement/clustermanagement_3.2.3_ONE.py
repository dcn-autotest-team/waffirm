#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.2.3.py - test case 3.2.3 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-01-18 11:08:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.2.3 AP获取IP地址(IPV6)
# 测试目的：测试AP可以通过DHCP和静态指定两种方式获取IPv6地址
# 测试描述：AP支持静态IPv6地址的配置,AP支持动态获取IPv6地址
# 测试环境：同测试拓扑

#Package

#Global Definition
ap_ipv6addr_frompool = '2001:'+EnvNo+'1::'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.2.3'

avoiderror(testname)
printTimer(testname,'Start','Test AP acquire IPv6 Address')

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
exec(compile(open('clustermanagement\\clustermanagement_initial(ipv6).py', "rb").read(), 'clustermanagement\\clustermanagement_initial(ipv6).py', 'exec'))
		  
EnterEnableMode(ap1)
RebootAp(setdefaut=True, AP=ap1,connectTime=10)

#check
res1 = Check_ap_dhcpstatus(ap1,Ap1cmdtype,'down',version='ipv6')

#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
# 在AP上把AP dhcp状态down掉，查看AP dhcp的状态
#
#预期
# dhcpv6-status状态显示为down
################################################################################

printStep(testname,'Step 2',
          'Check AP1 ipv6 address after config AP1 dhcp status down',
          'Check the result')

# operate
ApSetcmd(ap1,Ap1cmdtype,'set_dhcpv6_down')
IdleAfter(10)
	
#check
res1 = Check_ap_dhcpstatus(ap1,Ap1cmdtype,'down',version='ipv6')

#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
#在AP上配置静态IPv6地址
#
#预期
#查看AP static-ipv6地址显示为:2001:20::8
################################################################################

printStep(testname,'Step 3',
          'Check AP1 ipv6 address after config a static ipv6 address on AP1',
		  'Check the result')

# operate	  
# 在AP上配置静态IPv6地址	
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6','2001:20::8')	
IdleAfter(10)

# check
res1 = Check_ap_ip(ap1,Ap1cmdtype,'2001:20::8',mode='staticip',ipversion='ipv6')

# result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
#在S3上配置AP的IPv6地址池,配置vlan70的接口IPv6
#在AP上把AP dhcpv6状态up,让AP从dhcpv6 server中获取地址,查看AP的IPv6地址
#
#预期
#查看AP IP地址显示为从dhcpv6 server获取的IP：Dhcp_ap_pool_ipv6 
#
################################################################################

printStep(testname,'Step 4',
          'Config AP dhcp pool on S3',
          'Check the result')

# operate		  
EnterConfigMode(switch3)
SetCmd(switch3,'interface vlan',Vlan70)
SetCmd(switch3,'ipv6 address',If_vlan70_s3_ipv6)

EnterConfigMode(switch3)
SetCmd(switch3,'service dhcpv6')
SetCmd(switch3,'ipv6 dhcp pool APv6')
SetCmd(switch3,'network-address',Dhcp_ap_pool_ipv6)

EnterConfigMode(switch3)
SetCmd(switch3,'no service dhcpv6')
SetCmd(switch3,'service dhcpv6')

EnterConfigMode(switch3)
SetCmd(switch3,'interface vlan',Vlan70)
SetCmd(switch3,'no ipv6 nd suppress-ra')
SetCmd(switch3,'ipv6 nd managed-config-flag')
SetCmd(switch3,'ipv6 nd other-config-flag')
SetCmd(switch3,'ipv6 dhcp server APv6')
IdleAfter(5)

ApSetcmd(ap1,Ap1cmdtype,'set_dhcpv6_up')

#check
for i in range(10):
    IdleAfter(5)
    res1 =  Check_ap_ip(ap1,Ap1cmdtype,ap_ipv6addr_frompool,mode='ip',ipversion='ipv6')
    if res1 == 0:
        break

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
SetCmd(switch3,'no ipv6 dhcp pool APv6')
SetCmd(switch3,'no interface vlan',Vlan70)
SetCmd(switch3,'no service dhcpv6')
	
exec(compile(open('clustermanagement\\clustermanagement_unitial(ipv6).py', "rb").read(), 'clustermanagement\\clustermanagement_unitial(ipv6).py', 'exec'))   
#end
printTimer(testname, 'End')