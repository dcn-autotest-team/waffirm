# -*- coding: UTF-8 -*-#
# *******************************************************************************
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
# *******************************************************************************
# Change log:
#     - modified by zhangjxp 新增升级脚本5.3，添加参数If_vlan1_s3_ipv4，修改参数updateserver
#     - modified by yanwh 增加from waffirm_config_topu import *
#     - modified by yanwh 增加库函数导入，支持后面的函数运行
# *******************************************************************************
import re

from dcntestlibrary.dcnlibrary.lib_all import SetCmd, GetValueBetweenTwoValuesInData, \
    EnterEnableMode, CheckLine, IdleAfter
from dutils.dcnprint import printResInfo
from dcntestlibrary.dcnlibrary.dreceiver import StartDebug, StopDebug
from waffirm_config_topu import *

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
Network_wpa_password = 'abcd1234'

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

# 确定AP版本号
current_buildnum = ''
standby_buildnum = ''
if vars().has_key('current_build') and vars().has_key('standby_build'):
    temp1 = re.search('(\d+\.){3}\d+\.tar|(\d+_){3}\d+\.tar',current_build)
    temp2 = re.search('(\d+\.){3}\d+\.tar|(\d+_){3}\d+\.tar',standby_build)
    if temp1 and temp2:
        current_buildnum = temp1.group(0)[:-4].replace('_','.')
        standby_buildnum = temp2.group(0)[:-4].replace('_','.')

##################################################################################
# 检查linux pc机ping ip地址是否成功
# args: 
#     switch:要ping的linuxpc机的switch号
#     ipadd:需要ping的目的ip地址
#     time:ping操作的时间
# return: 
#       1 :失败
#       0 :ping成功
# addition:
# examples:
#     CheckPingLinux(switch5,'172.16.1.2')
#     CheckPingLinux(switch5,'172.16.1.2',10)
###################################################################################
def CheckPingLinux(switch,ipadd,time=20):
    SetCmd(switch,'ping ',ipadd,promoteStop=False,timeout=time)
    data = SetCmd(switch,'\x03',promoteStop=False,timeout = 1)
    res1 = int(str(GetValueBetweenTwoValuesInData(data,'transmitted, ',' received')).lstrip().rstrip())
    res1 = 0 if res1 > 0 else 1
    if 0==res1:
        printResInfo('Ping '+ipadd+' success!')
    else:
        printResInfo('!Ping '+ipadd+' failed!')
    return res1

##################################################################################
# 下发配置wireless ap profile apply profile_num
#	
#
# args: 
#     switch:要下发配置的switch号
#     profile:profile号
#     waittime:如果第一次下发不成功，第二次下发的默认等待时间
# return: 
#
# addition:
#
# examples:
#     WirelessApProfileApply(switch1,'1',10)
#     WirelessApProfileApply(switch1,'1')
#
###################################################################################
def WirelessApProfileApply(switch,profile,waittime=15):
    EnterEnableMode(switch)
    data0 = SetCmd(switch,'wireless ap profile apply',profile,timeout=1)
    if CheckLine(data0,'Y/N') == 0:
        datatmp = SetCmd(switch,'y',timeout=3)
        if 'could not be applied to the associated' in datatmp:
            for tmpCounter in xrange(0,3):
                StartDebug(switch)
                IdleAfter(waittime)
                SetCmd(switch,'y',timeout=3)                
                datatmp = StopDebug(switch)        
                if 'AP Profile apply is in progress' in datatmp:
                    break
                elif 'Y/N' in datatmp:
                    IdleAfter(waittime)
                    datatmp1 = SetCmd(switch,'y',timeout=3)
                    if 'AP Profile apply is in progress' in datatmp1:
                        break
                        
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