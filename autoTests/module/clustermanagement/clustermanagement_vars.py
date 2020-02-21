#-*- coding: UTF-8 -*-#
#*******************************************************************************
# clustermanagement__vars.py - variables defination for clustermanagement_ test script
#
# Author:  humj
#
# Version 1.0.0
#
# Copyright (c) 2004-2008 Digital China Networks Co. Ltd
#
# Features: 存放变量信息
#
# 2012-12-4 10:23:59
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

Netcard_sta1 = 'wls224'
Netcard_sta2 = 'wls224'
Netcard_pc = 'wls224'

Vlan8 = '8'
Vlan9 = '9'
Vlan10 = '10'
Vlan70 = '70'
Vlan80 = '81'
Vlan90 = '90'
Vlan192 = '192'

If_vlan8_ipv4 = '3.3.3.3 255.255.255.0'
If_vlan8_ipv4_s = '3.3.3.3'
If_vlan8_ipv6 = '2001:50::1/64'
If_vlan8_ipv6_s = '2001:50::1'

If_vlan9_ipv4 = '2.2.2.2 255.255.255.0'
If_vlan9_ipv4_s = '2.2.2.2'
If_vlan9_ipv6 = '2001:40::1/64'
If_vlan9_ipv6_s = '2001:40::1'

If_vlan10_ipv4 = '1.1.1.1 255.255.255.0'
If_vlan10_ipv4_s = '1.1.1.1'
If_vlan10_ipv6 = '2001:30::1/64'
If_vlan10_ipv6_s = '2001:30::1'

If_loopback1_ipv4 = '4.4.4.4 255.255.255.255'
If_loopback1_ipv4_s = '4.4.4.4'
If_loopback1_ipv6 = '2001:60::1/128'
If_loopback1_ipv6_s = '2001:60::1'

If_loopback2_ipv4 = '5.5.5.5 255.255.255.255'
If_loopback2_ipv4_s = '5.5.5.5'
If_loopback2_ipv6 = '2001:70::1/128'
If_loopback2_ipv6_s = '2001:70::1'

If_loopback3_ipv4 = '6.6.6.6 255.255.255.255'
If_loopback3_ipv4_s = '6.6.6.6'
If_loopback3_ipv6 = '2001:80::1/128'
If_loopback3_ipv6_s = '2001:80::1'

If_vlan70_s1_ipv4 = '70.1.'+EnvNo+'1.100 255.255.255.0'
If_vlan70_s1_ipv6 = '2001:'+EnvNo+'1::100/64'
If_vlan70_s1_backipv4 = '70.1.'+EnvNo+'1.102 255.255.255.0'
If_vlan70_s1_backipv6 = '2001:'+EnvNo+'1::102/64'
If_vlan70_s1_ipv4_s = '70.1.'+EnvNo+'1.100'
If_vlan70_s1_ipv6_s = '2001:'+EnvNo+'1::100'
If_vlan70_s1_backipv4_s = '70.1.'+EnvNo+'1.102'
If_vlan70_s1_backipv6_s = '2001:'+EnvNo+'1::102'

If_vlan70_s2_ipv4 = '70.1.'+EnvNo+'1.101 255.255.255.0'
If_vlan70_s2_ipv6 = '2001:'+EnvNo+'1::101/64'
If_vlan70_s2_ipv4_s = '70.1.'+EnvNo+'1.101'
If_vlan70_s2_ipv6_s = '2001:'+EnvNo+'1::101'

If_vlan70_s3_ipv4 = '70.1.'+EnvNo+'1.1 255.255.255.0'
If_vlan70_s3_ipv6 = '2001:'+EnvNo+'1::1/64'
If_vlan70_s3_ipv4_s = '70.1.'+EnvNo+'1.1'
If_vlan70_s3_ipv6_s = '2001:'+EnvNo+'1::1'

If_vlan80_s1_ipv4 = '80.1.'+EnvNo+'1.100 255.255.255.0'
If_vlan80_s1_ipv6 = '2001:41::100/64'

If_vlan80_s2_ipv4 = '80.1.'+EnvNo+'1.101 255.255.255.0'
If_vlan80_s2_ipv6 = '2001:41::101/64'

If_vlan80_s3_ipv4 = '80.1.'+EnvNo+'1.1 255.255.255.0'
If_vlan80_s3_ipv6 = '2001:41::1/64'
If_vlan80_s3_ipv4_s = '80.1.'+EnvNo+'1.1'
If_vlan80_s3_ipv6_s = '2001:'+EnvNo+'1::1'

If_vlan90_s1_ipv4 = '90.1.'+EnvNo+'1.100 255.255.255.0'
If_vlan90_s3_ipv4 = '90.1.'+EnvNo+'1.1 255.255.255.0'
If_vlan90_s3_ipv4_s = '90.1.'+EnvNo+'1.1'

If_vlan192_s3_ipv4 = '192.168.10.'+EnvNo+'1'

StaticIpv4_ac1 = '1.1.1.'+EnvNo+'1'

Ap1_ipv4 = '70.1.'+EnvNo+'1.2'
Ap1_ipv6 = '2001:'+EnvNo+'1::2'
Ap2_ipv4 = '70.1.'+EnvNo+'1.3'
Ap2_ipv6 = '2001:'+EnvNo+'1::3'

NetWork_name1 = 'affirm_autobj_'+EnvNo+'1'
NetWork_name2 = 'affirm_autobj_'+EnvNo+'2'

Dhcp_ap_pool_ipv4 = '70.1.'+EnvNo+'1.0 '+'255.255.255.0'
Dhcp_ap_pool_ipv4_1 = '70.1.'+EnvNo+'1.'
ap_address_vlan70 = '70.1.'+EnvNo+'1.2 70.1.'+EnvNo+'1.99'
Dhcp_ap_pool_ipv6 = '2001:'+EnvNo+'1::10 64'
Dhcp_sta_pool_ipv4 = '80.1.'+EnvNo+'1.0 255.255.255.0'
Dhcp_sta_pool_ipv6 = '2001:41::2 64'
Dhcp_ap_pool_ipv4_vlan90 = '90.1.'+EnvNo+'1.0 255.255.255.0'
ap_address_vlan90 = '90.1.'+EnvNo+'1.2 90.1.'+EnvNo+'1.99'

dns_server_ip = '192.168.10.104'
ac1_domain = 'ac'+EnvNo+'1.test.com'
ac2_domain = 'ac'+EnvNo+'2.test.com'
radius_server_name = 'dcn'
radius_server_ipv4 = '192.168.10.104'
radius_password = '123456'
                        
