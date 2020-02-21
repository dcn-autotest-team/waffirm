#-*- coding: UTF-8 -*-#
#*******************************************************************************
# waffirm_vars.py - variables defination for waffirm test script
#
# Author:  ()
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
import re

Vlan10 = '10'
Vlan20 = '20'
Vlan30 = '30'
Vlan40 = '40'
Vlan192 = '192'
Vlan4091 = '4091'
Vlan4092 = '4092'
Vlan4093 = '4093'

pc1_ipv4 = '192.168.10.'+EnvNo+'2'
Radius_server = '192.168.10.101'
Radius_server_windows = '192.168.10.104'
BW_server = '192.168.10.102'

Netcard_sta1 = 'wls224'
Netcard_sta2 = 'wls224'
Netcard_pc = 'wls224'

Dhcp_pool1 = '192.168.'+EnvNo+'1.'
Dhcp_pool2 = '192.168.'+EnvNo+'2.'
Dhcp_pool3 = '192.168.'+EnvNo+'3.'

If_vlan20_s1_ipv4 = '20.1.1.1'
If_vlan20_s1_ipv6 = '2001:20::1'
If_vlan40_s1_ipv4 = '40.1.1.1'
If_vlan40_s1_ipv6 = '2001:40::1'

If_vlan4091_s1_ipv4 = Dhcp_pool1 + '1'
If_vlan4092_s1_ipv4 = Dhcp_pool2 + '1'
If_vlan4093_s1_ipv4 = Dhcp_pool3 + '1'
If_vlan4091_s2_ipv4 = Dhcp_pool1 + '100'
If_vlan4092_s2_ipv4 = Dhcp_pool2 + '100'
If_vlan4093_s2_ipv4 = Dhcp_pool3 + '100'

If_vlan4091_s1_ipv6 = '2001:91::1'
If_vlan4092_s1_ipv6 = '2001:92::1'
If_vlan4093_s1_ipv6 = '2001:93::1'
If_vlan4091_s2_ipv6 = '2001:91::2'
If_vlan4092_s2_ipv6 = '2001:92::2'
If_vlan4093_s2_ipv6 = '2001:93::2'

If_vlan30_s2_ipv4 = '30.1.1.2'
If_vlan30_s2_ipv6 = '2001:30::2'

If_vlan20_s3_ipv4 = '20.1.1.2'
If_vlan20_s3_ipv6 = '2001:20::2'
If_vlan30_s3_ipv4 = '30.1.1.1'
If_vlan30_s3_ipv6 = '2001:30::1'
If_vlan40_s3_ipv4 = '40.1.1.2'
If_vlan40_s3_ipv6 = '2001:40::2'
If_vlan192_s3_ipv4 = '192.168.10.'+EnvNo+'1'
If_vlan1_s3_ipv4 = '100.1.1.254'

Ap1_ipv4 = '20.1.1.3'
Ap1_ipv6 = '2001:20::3'
Ap2_ipv4 = '30.1.1.3'
Ap2_ipv6 = '2001:30::3'

StaticIpv4_ac1 = '1.1.1.'+EnvNo+'1'
StaticIpv6_ac1 = '2001::1'
StaticIpv4_ac2 = '1.1.2.'+EnvNo+'1'
StaticIpv6_ac2 = '2003::1'

Var_Staticip1 = '10.1.1.2'

ap1backupip = '20.1.1.'+EnvNo+'1'
ap2backupip = '20.1.1.'+EnvNo+'2'
updatel3ip = '100.1.1.23'+EnvNo
if 'bj' in Network_name1:
    updateserver = '100.1.1.1'
elif 'wh' in Network_name1:
    updateserver = '100.1.1.2'
else:
    pass

apsimstartmac = '00-03-0f-50-10-10'
apsimtempip = '20.1.1.72'
maxapcount = 100

web_ip = 'http://1.1.1.1'
Dot1x_identity = 'aaa'
Dot1x_password = '111'
Dot1x_identity_with_idletimeout = 'aaa'
Dot1x_password_with_idletimeout = '111'
Dot1x_identity_no_idletimeout = 'bbb'
Dot1x_password_no_idletimeout = '111'

portal_username = 'aaa'
portal_password = '111'
Pc1_telnet_name = 'root'
Pc1_telnet_password = '123456'
Ap_login_name = 'admin'
Ap_login_password = 'admin'
Ssh_login_name = 'admin'
Ssh_login_password = 'admin'
Network_wpa_password  = 'abcd1234'

Netcard_ipaddress_check = Dhcp_pool1
Netcard_ipaddress_check2 = Dhcp_pool2

multicast_srcip = Radius_server
Report_rate = '10'

Ap_connect_after_reboot = 60
Vlan_Idle_time = 3
Ap_manage_timeout = 120
Ac_ap_syn_time = 60
Wait_rf_scan_time = 15
Ap_reboot_time = 100
Pc_client_login_wait_time = 8
Rate_stable_wait_time = 30
Signal_scan_diff_time = 10
Signal_scan_times = 15
Apply_profile_wait_time = 80
                        