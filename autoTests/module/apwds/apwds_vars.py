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

if test24gflag ==  True:
    wds0num = 'wds0'
    wds1num = 'wds1'
    wds2num = 'wds2'
else:
    wds0num = 'wds16'
    wds1num = 'wds17'
    wds2num = 'wds18'
wds_ssid = 'module_apwds'+EnvName+'_'+EnvNo+'1'
ap1_wds_network = 2
wds_psk_key = '12345678'

Vlan10 = '10'
Vlan20 = '20'
Vlan4091 = '4091'
Vlan4092 = '4092'

pc1_ipv4 = '192.168.10.'+EnvNo+'2'

Netcard_sta1 = 'wls224'
Netcard_sta2 = 'wls224'
Netcard_pc = 'wls224'

Dhcp_pool1 = '192.168.'+EnvNo+'1.'
Dhcp_pool2 = '192.168.'+EnvNo+'2.'

If_vlan10_s1_ipv4 = '10.1.1.1'
If_vlan20_s1_ipv4 = '20.1.1.1'

If_vlan4091_s3_ipv4 = Dhcp_pool1 + '1'
If_vlan4092_s3_ipv4 = Dhcp_pool2 + '1'

If_vlan10_s3_ipv4 = '10.1.1.2'
If_vlan20_s3_ipv4 = '20.1.1.1'

If_vlan192_s3_ipv4 = '192.168.10.'+EnvNo+'1'

Ap1_ipv4 = '20.1.1.2'
Ap2_ipv4 = '20.1.1.3'
ap1mac_type1_network3 =incrmac(ap1mac_type1,2).lower()
ap2mac_type1_network3 =incrmac(ap2mac_type1,2).lower()
ap1vapmac_network2 = incrmac(ap1vapmac,1).lower()
ap1vapmac_network3 = incrmac(ap1vapmac,2).lower()
ap2vapmac_network2 = incrmac(ap2vapmac,1).lower()
ap2vapmac_network3 = incrmac(ap2vapmac,2).lower()

StaticIpv4_ac1 = '1.1.1.'+EnvNo+'1'
StaticIpv6_ac1 = '2001::1'
StaticIpv4_ac2 = '1.1.2.'+EnvNo+'1'
StaticIpv6_ac2 = '2003::1'

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
            
##################################################################################
## Ap_openwds_config(ap,cmdtype,wdsnum,remotemac,apmode)
## 
## function:
##     在AP上进行open模式的wds配置(此函数主要是为了兼容后期可能会出现其他命令格式的AP)
## args: 
##     ap: 需要下发命令的AP设备
##     cmdtype:AP支持的命令形式，目前有两类，一类是'set'形式的，大部分AP支持
##          另一类是'uci'形式的，I3R2支持
##     wdsnum:wds序号
##     remotemac:需要建立wds连接的远端AP的mac,以':'作为连接符
##     apmode:ap的模式，satelliteap或者rootap
## examples:
##     Ap_openwds_config(ap1,'set','wds1','00:03:0F:46:CF:20')
###################################################################################    
def Ap_openwds_config(ap,cmdtype,wdsnum,ssid,remotemac,apmode='satelliteap'):
    SetCmd(ap,'\n')
    SetCmd(ap,'set wds',wdsnum,'wds-mode',apmode,promotePatten='#',promoteTimeout=20)
    SetCmd(ap,'set wds',wdsnum,'wds-ssid',ssid,promotePatten='#',promoteTimeout=20)
    SetCmd(ap,'set wds',wdsnum,'remote-mac',remotemac,promotePatten='#',promoteTimeout=20)
    SetCmd(ap,'set wds',wdsnum,'wds-security-policy plain-text',promotePatten='#',promoteTimeout=20)
    SetCmd(ap,'set wds',wdsnum,'wds-status up',promotePatten='#',promoteTimeout=20)
    
##################################################################################
## Ap_pskwds_config(ap,cmdtype,wdsnum,remotemac,psk_key,apmode)
## 
## function:
##     在AP上进行open模式的wds配置(此函数主要是为了兼容后期可能会出现其他命令格式的AP)
## args: 
##     ap: 需要下发命令的AP设备
##     cmdtype:AP支持的命令形式，目前有两类，一类是'set'形式的，大部分AP支持
##          另一类是'uci'形式的，I3R2支持
##     wdsnum:wds序号
##     remotemac:需要建立wds连接的远端AP的mac,以':'作为连接符
##     apmode:ap的模式，satelliteap或者rootap
##     psk_key:密码
## examples:
##     Ap_openwds_config(ap1,'set','wds1','00:03:0F:46:CF:20','12345678')
###################################################################################    
def Ap_pskwds_config(ap,cmdtype,wdsnum,ssid,remotemac,psk_key,apmode='satelliteap'):
    SetCmd(ap,'\n')
    SetCmd(ap,'set wds',wdsnum,'wds-mode',apmode,promotePatten='#',promoteTimeout=20)
    SetCmd(ap,'set wds',wdsnum,'wds-ssid',ssid,promotePatten='#',promoteTimeout=20)
    SetCmd(ap,'set wds',wdsnum,'remote-mac',remotemac,promotePatten='#',promoteTimeout=20)
    SetCmd(ap,'set wds',wdsnum,'wds-security-policy wpa-personal',promotePatten='#',promoteTimeout=20)
    SetCmd(ap,'set wds',wdsnum,'wds-wpa-personal-key',psk_key,promotePatten='#',promoteTimeout=20)
    SetCmd(ap,'set wds',wdsnum,'wds-status up',promotePatten='#',promoteTimeout=20)

##################################################################################
## Ac_wds_config(ac,networknum,remotemac,apmode='rootap',securitymode='none',**kargs)
## 
## function:
##     在AC上进行open模式的wds配置
## args: 
##     ac: 需要下发命令的AP设备
##     network:需要配置的network
##     remotemac:需要建立wds连接的远端AP的mac,以':'作为连接符
##     apmode:ap的模式，satelliteap或者rootap
##     securitymode:安全模式
## examples:
##     Ac_wds_config(switch1,'2','00:03:0F:46:CF:20','rootap','none')
###################################################################################  
def Ac_wds_config(ac,networknum,ssid,remotemac,apmode='rootap',securitymode='none',**kargs):
    if 'psk_key' in kargs:
        wpa_key = kargs['psk_key']
    EnterWirelessMode(ac)
    SetCmd(ac,'network',str(networknum))
    SetCmd(ac,'wds-mode',apmode)
    SetCmd(ac,'wds-remote-vap',remotemac)
    SetCmd(ac,'ssid',ssid)
    if securitymode == 'none':
        SetCmd(ac,'security mode',securitymode)
    else:
        SetCmd(ac,'security mode',securitymode)
        SetCmd(ac,'wpa key',wpa_key)
##################################################################################
## Initial_ap2()
## 
## function:
##     对AP2进行初始化配置
################################################################################### 
def Initial_ap2():
    SetCmd(ap2,'\n')
    ApSetcmd(ap2,Ap2cmdtype,'set_dhcp_down')
    ApSetcmd(ap2,Ap2cmdtype,'set_ip_route',If_vlan20_s3_ipv4)
    ApSetcmd(ap2,Ap2cmdtype,'set_static_ip',Ap2_ipv4)
    ApSetcmd(ap2,Ap2cmdtype,'saverunning')
##################################################################################
## Initial_ap1()
## 
## function:
##     对AP1进行初始化配置
################################################################################### 
def Initial_ap1():
    SetCmd(ap1,'\n')
    ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_down')
    ApSetcmd(ap1,Ap1cmdtype,'set_ip_route',If_vlan20_s3_ipv4)
    ApSetcmd(ap1,Ap1cmdtype,'set_static_ip',Ap1_ipv4)
    ApSetcmd(ap1,Ap1cmdtype,'saverunning')
##################################################################################
## Ap_set_wds(ap,cmdtype,wdsnum,option,*args)
## 
## function:
##     在AP上进行wds配置，此函数不同于Ap_openwds_config和Ap_pskwds_config，一次只能配置一个命令
##    (此函数主要是为了兼容后期可能会出现其他命令格式的AP)
## args: 
##     ap: 需要下发命令的AP设备
##     cmdtype:AP支持的命令形式，目前有两类，一类是'set'形式的，大部分AP支持
##          另一类是'uci'形式的，I3R2支持
##     wdsnum:wds序号
##     option:需要配置wds的哪一项参数
##     args:配置参数的具体值
## examples:
##     Ap_set_wds(ap1,'set','wds1','wds-mode','rootap')
###################################################################################    
def Ap_set_wds(ap,cmdtype,wdsnum,option,*args):
    SetCmd(ap,'\n')
    _data = SetCmd(ap,'set wds',wdsnum,option,*args)
    return _data

##################################################################################
## Check_ap_wdsconfig(ap,cmdtype,wdsnum,check,**kargs)
## 
## function:
##     在AP上检查wds配置是否符合预期
##    (此函数主要是为了兼容后期可能会出现其他命令格式的AP)
## args: 
##     ap: 需要下发命令的AP设备
##     cmdtype:AP支持的命令形式，目前有两类，一类是'set'形式的，大部分AP支持
##          另一类是'uci'形式的，I3R2支持
##     wdsnum:wds序号
##     check:需要检查的参数
## examples:
##     Check_ap_wdsconfig(ap1,'set','wds1',check=[('radio',wlan),('wds-status','up')],IC=True)
###################################################################################     
def Check_ap_wdsconfig(ap,cmdtype,wdsnum,check,**kargs):
    _res = 1
    SetCmd(ap,'\n')
    data = SetCmd(ap,'get wds',wdsnum)
    _res1 = CheckLineList(data,check,**kargs)
    return _res1
    
##################################################################################
## Set_apmode(ap,cmdtype,mode)
## 
## function:
##     配置AP模式为胖AP或瘦AP
## args: 
##     ap: 需要下发命令的AP设备
##     cmdtype:AP支持的命令形式，目前有两类，一类是'set'形式的，大部分AP支持
##          另一类是'uci'形式的，I3R2支持
##     mode:fat或者fit
## examples:
##     Set_apmode(ap1,'set','fat')
###################################################################################  
def Set_apmode(ap,cmdtype,mode):
    SetCmd(ap,'switch-apmode',mode,timeout=1)
    SetCmd(ap,'y',timeout=1)