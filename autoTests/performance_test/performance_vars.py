#-*- coding: UTF-8 -*-#
#*******************************************************************************
# waffirm_vars.py - variables defination for performance test script
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2017 Digital China Networks Co. Ltd
#
# Features: 存放变量信息
#
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.11.29
#*******************************************************************************
import re
import random
from performance_topu import *
        
Vlan1 = '2'
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
    updateserver = '100.1.1.3'

apsimstartmac = '00-03-0f-50-10-10'
apsimtempip = '20.1.1.72'
maxapcount = 100

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

if vars().has_key('aplist'):
    pass
else:
    aplist = []

# 根据环境编号配置AP的IP,S3 Vlan1接口IP，S1 Vlan1接口IP
#根据环境编号配置网段（子网掩码为255.255.255.192，将100.1.1.0分为4个子网)
if EnvNo == '1':
    maskprefix = '00'
elif EnvNo == '2':
    maskprefix = '01'
elif EnvNo == '3':
    maskprefix = '10'
else:
    pass
# 根据网段配置Ap1_ipv4、If_vlan1_s3_ipv4、If_vlan1_s1_ipv4
# Ap1_ipv4为网段内第7个IP，If_vlan1_s3_ipv4为网段内倒数第二个IP，If_vlan1_s1_ipv4为网段内倒数第三个IP
# 举例：环境编号为1，子网网络号为100.1.1.0，Ap1_ipv4为100.1.1.7，If_vlan1_s3_ipv4为100.1.1.62，If_vlan1_s1_ipv4为100.1.1.61
Ap1_ipv4_tail_binary = maskprefix+'000111'
If_vlan1_s3_ipv4_tail_binary = maskprefix+'111110'
If_vlan1_s1_ipv4_tail_binary = maskprefix+'111101'
Ap1_ipv4_tail_dec = int(Ap1_ipv4_tail_binary,2)
If_vlan1_s3_ipv4_tail_dec = int(If_vlan1_s3_ipv4_tail_binary,2)
If_vlan1_s1_ipv4_tail_dec = int(If_vlan1_s1_ipv4_tail_binary,2)

Ap1_ipv4 = '100.1.1.'+ str(Ap1_ipv4_tail_dec)
If_vlan1_s3_ipv4 = '100.1.1.'+str(If_vlan1_s3_ipv4_tail_dec)
If_vlan1_s1_ipv4 = '100.1.1.'+str(If_vlan1_s1_ipv4_tail_dec)

ap_ipv4_tail_dec = Ap1_ipv4_tail_dec + 1 
for ap in aplist:
    ap['ipv4'] = '100.1.1.'+ str(ap_ipv4_tail_dec)
    ap_ipv4_tail_dec += 1
        
# 确定AP版本号
ap1_now_versionnum = ''
ap1_old_versionnum = ''
if vars().has_key('ap1_now_versionfile') and vars().has_key('ap1_old_versionfile'):
    temp1 = re.search('(\d+\.){3}\d+\.tar|(\d+_){3}\d+\.tar',ap1_now_versionfile)
    temp2 = re.search('(\d+\.){3}\d+\.tar|(\d+_){3}\d+\.tar',ap1_old_versionfile)
    if temp1 and temp2:
        ap1_now_versionnum = temp1.group(0)[:-4].replace('_','.')
        ap1_old_versionnum = temp2.group(0)[:-4].replace('_','.')
        
for ap in aplist:
    temp1 = re.search('(\d+\.){3}\d+\.tar|(\d+_){3}\d+\.tar',ap['now_versionfile'])
    temp2 = re.search('(\d+\.){3}\d+\.tar|(\d+_){3}\d+\.tar',ap['old_versionfile'])
    if temp1 and temp2:
        ap['now_versionnum'] = temp1.group(0)[:-4].replace('_','.')
        ap['old_versionnum'] = temp2.group(0)[:-4].replace('_','.')
##################################################################################
## GetWhetherkeepon
## 
## function:
##     结合topo文件中的mainkeeponflag参数和脚本执行情况判断继续执行后续步骤
## args: 
##     keeponflag: 脚本上一步存在sta无法关联无线或无法获取IP地址的标志
##   
## examples:
##     GetWhetherkeepon（keeponflag）
################################################################################### 
def GetWhetherkeepon(flag):
    global mainkeeponflag
    if mainkeeponflag == True:
        return True
    else:
        if flag == 0:
            return True
        else:
            return False