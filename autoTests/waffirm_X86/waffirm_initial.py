#-*- coding: UTF-8 -*-#
#*******************************************************************************
# waffirm_initial.py
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2008 Digital China Networks Co. Ltd
#
# Features: 初始设置
# 2012-12-4 10:01:57
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************
import os
import time
import re
import wx

#记录日志
printInitialTimer('TestCase Initial','Start')

SetTerminalLength(switch1)
SetWatchdogDisable(switch1)
SetExecTimeout(switch1)
SetTerminalLength(switch2)
SetWatchdogDisable(switch2)
SetExecTimeout(switch2)
SetTerminalLength(switch3)
SetWatchdogDisable(switch3)
SetExecTimeout(switch3)

printRes('Check the software version of s1...')
ShowVersion(switch1)

SetCmd(pc1,'cd /root')
SetCmd(pc1,'service dhcpd stop')
SetCmd(sta1,'cd /root')
SetCmd(sta1,'service dhcpd stop')
SetCmd(sta2,'cd /root')
SetCmd(sta2,'service dhcpd stop')

#交换机初始配置
#---------------------------  初始化AC1  ---------------------------------------
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan 1')
SetCmd(switch1,'radius-server key 0 test')
SetCmd(switch1,'radius-server authentication host ' + Radius_server)
SetCmd(switch1,'radius-server accounting host ' + Radius_server)
SetCmd(switch1,'aaa-accounting enable')
SetCmd(switch1,'aaa enable')
SetCmd(switch1,'radius nas-ipv4 ' + StaticIpv4_ac1)
SetCmd(switch1,'radius source-ipv4 ' + StaticIpv4_ac1)
SetCmd(switch1,'aaa group server radius wlan')
SetCmd(switch1,'server ' + Radius_server)

SetCmd(switch1,'vlan',Vlan40 + ';' + Vlan4091 + '-' + Vlan4093)
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport access vlan',Vlan40)
EnterInterfaceMode(switch1,'vlan '+Vlan40)
IdleAfter(Vlan_Idle_time)
SetCmd(switch1,'ip address',If_vlan40_s1_ipv4,'255.255.255.0')
SetCmd(switch1,'ipv6 address',If_vlan40_s1_ipv6+'/64')
EnterInterfaceMode(switch1,'vlan '+Vlan4091)
IdleAfter(Vlan_Idle_time)
SetCmd(switch1,'ip address',If_vlan4091_s1_ipv4,'255.255.255.0')
SetCmd(switch1,'ipv6 address',If_vlan4091_s1_ipv6+'/64')
EnterInterfaceMode(switch1,'vlan '+Vlan4092)
IdleAfter(Vlan_Idle_time)
SetCmd(switch1,'ip address',If_vlan4092_s1_ipv4,'255.255.255.0')
SetCmd(switch1,'ipv6 address',If_vlan4092_s1_ipv6+'/64')
EnterInterfaceMode(switch1,'vlan '+Vlan4093)
IdleAfter(Vlan_Idle_time)
SetCmd(switch1,'ip address',If_vlan4093_s1_ipv4,'255.255.255.0')
SetCmd(switch1,'ipv6 address',If_vlan4093_s1_ipv6+'/64')
EnterInterfaceMode(switch1,'loopback 1')
SetCmd(switch1,'ip address',StaticIpv4_ac1,'255.255.255.255')
SetCmd(switch1,'ipv6 address',StaticIpv6_ac1+'/128')

#开启DHCP
EnterConfigMode(switch1)
SetCmd(switch1,'service dhcp')
SetCmd(switch1,'ip dhcp excluded-address ' + If_vlan4091_s1_ipv4)
SetCmd(switch1,'ip dhcp excluded-address ' + If_vlan4092_s1_ipv4)
SetCmd(switch1,'ip dhcp excluded-address ' + If_vlan4093_s1_ipv4)
SetCmd(switch1,'ip dhcp excluded-address ' + If_vlan4091_s2_ipv4)
SetCmd(switch1,'ip dhcp excluded-address ' + If_vlan4092_s2_ipv4)
SetCmd(switch1,'ip dhcp excluded-address ' + If_vlan4093_s2_ipv4)
SetCmd(switch1,'ip dhcp pool pool4091')
SetCmd(switch1,'network-address ' + Dhcp_pool1 + '0 255.255.255.0')
SetCmd(switch1,'default-router ' + If_vlan4091_s1_ipv4)
SetCmd(switch1,'exit')
SetCmd(switch1,'ip dhcp pool pool4092')
SetCmd(switch1,'network-address ' + Dhcp_pool2 + '0 255.255.255.0')
SetCmd(switch1,'default-router ' + If_vlan4092_s1_ipv4)
SetCmd(switch1,'exit')
SetCmd(switch1,'ip dhcp pool pool4093')
SetCmd(switch1,'network-address ' + Dhcp_pool3 + '0 255.255.255.0')
SetCmd(switch1,'default-router ' + If_vlan4093_s1_ipv4)
SetCmd(switch1,'exit')

#配置wireless视图下的参数
EnterWirelessMode(switch1)
SetCmd(switch1,'enable')
SetCmd(switch1,'keep-alive-interval 10000')
SetCmd(switch1,'keep-alive-max-count 3')
# SetCmd(switch1,'country-code cn')
SetCmd(switch1,'static-ip',StaticIpv4_ac1)
# SetCmd(switch1,'static-ipv6',StaticIpv6_ac1)
EnterWirelessMode(switch1)
SetCmd(switch1,'no auto-ip-assign')

#配置Network1
EnterNetworkMode(switch1,1)
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan ' + Vlan4091)
#配置Network2
EnterNetworkMode(switch1,2)
SetCmd(switch1,'ssid ' + Network_name2)
SetCmd(switch1,'vlan '+ Vlan4092)

#配置Ap-profile1
EnterApProMode(switch1,1)
SetCmd(switch1,'hwtype',hwtype1)
SetCmd(switch1,'radio 1')
# SetCmd(switch1,'rf-scan other-channels interval 5')
# SetCmd(switch1,'rf-scan duration 50')
# SetCmd(switch1,'vap 1')
# SetCmd(switch1,'enable')
# SetCmd(switch1,'exit')
SetCmd(switch1,'exit')
SetCmd(switch1,'radio 2')
SetCmd(switch1,'mode ac')
# SetCmd(switch1,'vap 1')
# SetCmd(switch1,'enable')
# SetCmd(switch1,'exit')
SetCmd(switch1,'exit')
SetCmd(switch1,'exit')

#配置Ap-profile2
EnterApProMode(switch1,2)
SetCmd(switch1,'hwtype',hwtype2)
SetCmd(switch1,'radio 1')
SetCmd(switch1,'vap 1')
SetCmd(switch1,'enable')
SetCmd(switch1,'exit')
SetCmd(switch1,'exit')
SetCmd(switch1,'radio 2')
SetCmd(switch1,'mode ac')
# SetCmd(switch1,'vap 1')
# SetCmd(switch1,'enable')
SetCmd(switch1,'end')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'profile 1')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap2mac)
SetCmd(switch1,'profile 2')
#配置Discovery ip-list
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list',1)
SetCmd(switch1,'discovery ip-list',Ap1_ipv4)                      
# SetCmd(switch1,'discovery ipv6-list',Ap1_ipv6)
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',Ap2_ipv4)
# SetCmd(switch1,'discovery ipv6-list',Ap2_ipv6)
EnterWirelessMode(switch1)
SetCmd(switch1,'l2tunnel vlan-list add',Vlan4091 + '-' + Vlan4093)
EnterConfigMode(switch1)
SetCmd(switch1,'router ospf')
SetCmd(switch1,'network 0.0.0.0/0 area 0')
SetCmd(switch1,'redistribute connected')
EnterEnableMode(switch1)

#交换机初始配置
#---------------------------  初始化AC2  ---------------------------------------
EnterConfigMode(switch2)
SetCmd(switch2,'no interface vlan 1')
SetCmd(switch2,'vlan',Vlan30 + ';' + Vlan4091 + '-' + Vlan4093)
EnterInterfaceMode(switch2,s2p1)
SetCmd(switch2,'switchport access vlan',Vlan30)
EnterInterfaceMode(switch2,'vlan '+Vlan30)
IdleAfter(Vlan_Idle_time)
SetCmd(switch2,'ip address',If_vlan30_s2_ipv4,'255.255.255.0')
SetCmd(switch2,'ipv6 address',If_vlan30_s2_ipv6+'/64')
EnterInterfaceMode(switch2,'vlan '+Vlan4091)
IdleAfter(Vlan_Idle_time)
SetCmd(switch2,'ip address',If_vlan4091_s2_ipv4,'255.255.255.0')
SetCmd(switch2,'ipv6 address',If_vlan4091_s2_ipv6+'/64')
EnterInterfaceMode(switch2,'vlan '+Vlan4092)
IdleAfter(Vlan_Idle_time)
SetCmd(switch2,'ip address',If_vlan4092_s2_ipv4,'255.255.255.0')
SetCmd(switch2,'ipv6 address',If_vlan4092_s2_ipv6+'/64')
EnterInterfaceMode(switch2,'vlan '+Vlan4093)
IdleAfter(Vlan_Idle_time)
SetCmd(switch2,'ip address',If_vlan4093_s2_ipv4,'255.255.255.0')
SetCmd(switch2,'ipv6 address',If_vlan4093_s2_ipv6+'/64')
EnterInterfaceMode(switch2,'loopback 1')
SetCmd(switch2,'ip address',StaticIpv4_ac2,'255.255.255.255')
SetCmd(switch2,'ipv6 address',StaticIpv6_ac2+'/128')

#配置wireless视图下的参数
EnterWirelessMode(switch2)
SetCmd(switch2,'enable')
# SetCmd(switch2,'country-code cn')
SetCmd(switch2,'keep-alive-interval 10000')
SetCmd(switch2,'keep-alive-max-count 3')
SetCmd(switch2,'no discovery vlan-list',1)
SetCmd(switch2,'static-ip',StaticIpv4_ac2)
# SetCmd(switch2,'static-ipv6',StaticIpv6_ac2)
EnterWirelessMode(switch2)
SetCmd(switch2,'no auto-ip-assign')

#配置Network1
EnterNetworkMode(switch2,1)
SetCmd(switch2,'ssid',Network_name1)
SetCmd(switch2,'vlan',Vlan4091)
#配置Network2
EnterNetworkMode(switch2,2)
SetCmd(switch2,'ssid',Network_name2)
SetCmd(switch2,'vlan',Vlan4092)

#配置Ap-profile1
EnterApProMode(switch2,1)
SetCmd(switch2,'hwtype',hwtype1)
SetCmd(switch2,'radio 1')
# SetCmd(switch2,'rf-scan other-channels interval 5')
# SetCmd(switch2,'rf-scan duration 50')
# SetCmd(switch2,'vap 1')
# SetCmd(switch2,'enable')
# SetCmd(switch2,'exit')
SetCmd(switch2,'exit')
SetCmd(switch2,'radio 2')
SetCmd(switch2,'mode ac')
# SetCmd(switch2,'vap 1')
# SetCmd(switch2,'enable')
# SetCmd(switch2,'exit')
SetCmd(switch2,'exit')
SetCmd(switch2,'exit')

#配置Ap-profile2
EnterApProMode(switch2,2)
SetCmd(switch2,'hwtype',hwtype2)
SetCmd(switch2,'radio 1')
SetCmd(switch2,'vap 1')
SetCmd(switch2,'enable')
SetCmd(switch2,'exit')
SetCmd(switch2,'exit')
SetCmd(switch2,'radio 2')
SetCmd(switch2,'mode ac')
# SetCmd(switch2,'vap 1')
# SetCmd(switch2,'enable')
SetCmd(switch2,'end')

EnterConfigMode(switch2)
EnterWirelessMode(switch2)
SetCmd(switch2,'ap database',ap1mac)
SetCmd(switch2,'profile 1')
EnterWirelessMode(switch2)
SetCmd(switch2,'ap database',ap2mac)
SetCmd(switch2,'profile 2')

EnterWirelessMode(switch2)
SetCmd(switch2,'l2tunnel vlan-list add',Vlan4091 + '-' + Vlan4093)
    
EnterConfigMode(switch2)
SetCmd(switch2,'router ospf')
SetCmd(switch2,'network 0.0.0.0/0 area 0')
SetCmd(switch2,'redistribute connected')
EnterEnableMode(switch2)
  
#---------------------------  初始化AP1  ---------------------------------------
SetCmd(ap1,'\n')
SetCmd(ap1,'set management static-ip',Ap1_ipv4)
# SetCmd(ap1,'set management static-ipv6',Ap1_ipv6)
SetCmd(ap1,'set management dhcp-status down')
SetCmd(ap1,'set management dhcpv6-status down')
SetCmd(ap1,'set static-ip-route gateway',If_vlan20_s3_ipv4)
# SetCmd(ap1,'set static-ipv6-route gateway',If_vlan20_s3_ipv6)
# SetCmd(ap1,'set management static-ipv6-prefix-length 64')
SetCmd(ap1,'save-running')

#---------------------------  初始化AP2  ---------------------------------------
SetCmd(ap2,'\n')
SetCmd(ap2,'set management static-ip',Ap2_ipv4)
# SetCmd(ap2,'set management static-ipv6',Ap2_ipv6)
SetCmd(ap2,'set management dhcp-status down')
SetCmd(ap2,'set management dhcpv6-status down')
SetCmd(ap2,'set static-ip-route gateway',If_vlan30_s3_ipv4)
# SetCmd(ap2,'set static-ipv6-route gateway',If_vlan30_s3_ipv6)
# SetCmd(ap2,'set management static-ipv6-prefix-length 64')
SetCmd(ap2,'save-running')

#---------------------------  初始化 S3  ---------------------------------------
#vlan20
EnterConfigMode(switch3)
SetCmd(switch3,'no interface vlan 1')
SetCmd(switch3,'vlan',Vlan20 + ';' + Vlan4091 + '-' + Vlan4093)
SetCmd(switch3,'Interface vlan 4091')
SetCmd(switch3,'Ip address ' + If_vlan4091_s1_ipv4 + ' 255.255.255.0')
SetCmd(switch3,'Exit')
SetCmd(switch3,'Interface vlan 4092')
SetCmd(switch3,'Ip address ' + If_vlan4092_s1_ipv4 + ' 255.255.255.0')
SetCmd(switch3,'ipv6 address 2001:92::1/64')
SetCmd(switch3,'Exit')
SetCmd(switch3,'Interface vlan 4093')
SetCmd(switch3,'Ip address ' + If_vlan4093_s1_ipv4 + ' 255.255.255.0')
SetCmd(switch3,'Exit')
SetCmd(switch3,'service dhcp')
SetCmd(switch3,'ip dhcp pool vlan4091')
SetCmd(switch3,'network ' + Dhcp_pool1 + '2 24')
SetCmd(switch3,'default-router ' + If_vlan4091_s1_ipv4)
SetCmd(switch3,'exit')
SetCmd(switch3,'ip dhcp pool vlan4092')
SetCmd(switch3,'network ' + Dhcp_pool2 + '2 24')
SetCmd(switch3,'default-router ' + If_vlan4092_s1_ipv4)
SetCmd(switch3,'exit')
SetCmd(switch3,'ip dhcp pool vlan4093')
SetCmd(switch3,'network ' + Dhcp_pool3 + '2 24')
SetCmd(switch3,'default-router ' + If_vlan4093_s1_ipv4)
SetCmd(switch3,'exit')

SetCmd(switch3,'switchport interface',s3p3)
EnterInterfaceMode(switch3,'vlan '+Vlan20)
IdleAfter(Vlan_Idle_time)
SetIpAddress(switch3,If_vlan20_s3_ipv4,'255.255.255.0')
SetCmd(switch3,'ipv6 address',If_vlan20_s3_ipv6 + '/64')

#vlan30
EnterConfigMode(switch3)
SetCmd(switch3,'vlan',Vlan30)
SetCmd(switch3,'switchport interface',s3p2)
SetCmd(switch3,'switchport interface',s3p4)
EnterInterfaceMode(switch3,'vlan '+Vlan30)
IdleAfter(Vlan_Idle_time)
SetIpAddress(switch3,If_vlan30_s3_ipv4,'255.255.255.0')
SetCmd(switch3,'ipv6 address',If_vlan30_s3_ipv6+'/64')

#vlan40
EnterConfigMode(switch3)
SetCmd(switch3,'vlan',Vlan40)
SetCmd(switch3,'switchport interface',s3p1)
EnterInterfaceMode(switch3,'vlan '+Vlan40)
IdleAfter(Vlan_Idle_time)
SetIpAddress(switch3,If_vlan40_s3_ipv4,'255.255.255.0')
SetCmd(switch3,'ipv6 address',If_vlan40_s3_ipv6+'/64')

#vlan192
EnterConfigMode(switch3)
SetCmd(switch3,'vlan',Vlan192)
SetCmd(switch3,'switchport interface',s3p5)
EnterInterfaceMode(switch3,'vlan '+Vlan192)
IdleAfter(Vlan_Idle_time)
SetIpAddress(switch3,If_vlan192_s3_ipv4,'255.255.255.0')

EnterConfigMode(switch3)
SetCmd(switch3,'service dhcp')

SetCmd(switch3,'Interface ',s3p3)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan20)
SetCmd(switch3,'Interface ',s3p4)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan30)

#router ospf
EnterConfigMode(switch3)
SetCmd(switch3,'router ospf')
SetCmd(switch3,'network 0.0.0.0/0 area 0')
SetCmd(switch3,'redistribute connected')
EnterEnableMode(switch3)

#----------------------- PC1，STA1，STA2 配置实验网路由,保持控制连接-------------------------------
# 配置PC1默认网关
SetCmd(pc1,'route add -net default gw',If_vlan192_s3_ipv4)

######################## 保存各交换机配置 ###################
EnterEnableMode(switch1)
SetCmd(switch1,'clock set 09:00:00 2012.12.21')
IdleAfter('1')
data = SetCmd(switch1,'write',timeout=1)
if 0==CheckLine(data,'Y/N'):
    SetCmd(switch1,'y',timeout=3)
SetCmd(switch1,'y',timeout=3)

SetCmd(switch2,'clock set 09:00:00 2012.12.21')
IdleAfter('1')
EnterEnableMode(switch2)
data = SetCmd(switch2,'write',timeout=1)
if 0==CheckLine(data,'Y/N'):
    SetCmd(switch2,'y',timeout=3)
SetCmd(switch2,'y',timeout=3)

SetCmd(switch3,'clock set 09:00:00 2012.12.21')
IdleAfter('1')   
EnterEnableMode(switch3)
data = SetCmd(switch3,'write',timeout=1)
if 0==CheckLine(data,'Y/N'):
    SetCmd(switch3,'y',timeout=3)
SetCmd(switch3,'y',timeout=3)
EnterEnableMode(switch1)

# WirelessApProfileApply(switch1,'1')
# IdleAfter(Apply_profile_wait_time)

# WirelessApProfileApply(switch1,'2')
WirelessApplyProfileWithCheck(switch1,['1','2'],[ap1mac,ap2mac])
data6 = SetCmd(switch1,'show wireless')


#######################################################################################
#如果数据vlan和管理vlan在同一vlan的话，需要在ap上配置set management vlan-id 10
#######################################################################################

time.sleep(60)
printInitialTimer('TestCase Initial','End')