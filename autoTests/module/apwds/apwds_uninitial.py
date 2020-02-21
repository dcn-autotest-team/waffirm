#-*- coding: UTF-8 -*-#
#*******************************************************************************
# waffirm_uninitial.py
#
# Author:  (jinpfb)
#
# Version 1.0.0
#
# Copyright (c) 2004-2008 Digital China Networks Co. Ltd
#
# Features: 恢复设置
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

printUninitialTimer('TestCase Uninitial','Start')

avoiderror('TestCase Uninitial')

# SetCmd(ap1,'ifconfig ath0 down')
# SetCmd(ap1,'ifconfig ath1 down')
# SetCmd(ap1,'ifconfig ath16 down')

# SetCmd(ap2,'ifconfig ath0 down')
# SetCmd(ap2,'ifconfig ath1 down')
# SetCmd(ap2,'ifconfig ath16 down')
SetCmd(ap1,'set managed-ap mode down')
SetCmd(ap2,'set managed-ap mode down')

#-----------------------  S1 uninitial ------------------

#wireless mode
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery ip-list')
SetCmd(switch1,'no discovery ipv6-list')
SetCmd(switch1,'no discovery vlan-list')
SetCmd(switch1,'no ap database',ap1mac)
SetCmd(switch1,'no ap database',ap2mac)
SetCmd(switch1,'no','static-ip')
SetCmd(switch1,'no','static-ipv6')
SetCmd(switch1,'no','l2tunnel vlan-list')
SetCmd(switch1,'no ap profile','2')
SetCmd(switch1,'discovery vlan-list 1')
SetCmd(switch1,'channel enhance enable')
SetCmd(switch1,'no client roam-timeout')
#network mode
ClearNetworkConfig(switch1,'1')

#profile mode
ClearProfileConfig(switch1,'1')

# wireless
EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter('5')
SetCmd(switch1,'enable')

#vlan
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan',Vlan10)
SetCmd(switch1,'no interface loopback 1')
SetCmd(switch1,'no','vlan',Vlan10)
SetCmd(switch1,'no','vlan',Vlan4091)
SetCmd(switch1,'no','vlan',Vlan4092)
SetCmd(switch1,'no','router rip')
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral == True:
    #DHCP
    EnterConfigMode(switch1)
    SetCmd(switch1,'no service dhcp')
    SetCmd(switch1,'no ip dhcp pool pool4091')
    SetCmd(switch1,'no ip dhcp pool pool4092')
    SetCmd(switch1,'no ip dhcp pool pool4093')
    SetCmd(switch1,'no ip dhcp excluded-address ' + If_vlan4091_s1_ipv4)
    SetCmd(switch1,'no ip dhcp excluded-address ' + If_vlan4092_s1_ipv4)
    SetCmd(switch1,'no ip dhcp excluded-address ' + If_vlan4093_s1_ipv4)
    SetCmd(switch1,'no ip dhcp excluded-address ' + If_vlan4091_s2_ipv4)
    SetCmd(switch1,'no ip dhcp excluded-address ' + If_vlan4092_s2_ipv4)
    SetCmd(switch1,'no ip dhcp excluded-address ' + If_vlan4093_s2_ipv4)
    # vlan
    SetCmd(switch1,'no interface vlan',Vlan4091)
    SetCmd(switch1,'no interface vlan',Vlan4092)
    SetCmd(switch1,'no interface vlan',Vlan4093)
    SetCmd(switch1,'no','vlan',Vlan4091)
    SetCmd(switch1,'no','vlan',Vlan4092)
    SetCmd(switch1,'no','vlan',Vlan4093)

#------------------------  S3 uninitial ----------------------
#vlan
EnterConfigMode(switch3)
SetCmd(switch3,'no interface vlan',Vlan10)
SetCmd(switch3,'no interface vlan',Vlan20)
SetCmd(switch3,'no','vlan',Vlan10)
SetCmd(switch3,'no','vlan',Vlan20)
# s3p4
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p4)
SetCmd(switch3,'no shutdown')
#router ospf
EnterConfigMode(switch3)
SetCmd(switch3,'no','router rip')
EnterEnableMode(switch3)
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral == True:
    pass
else:
    #DHCP
    EnterConfigMode(switch3)
    SetCmd(switch3,'no service dhcp')
    SetCmd(switch3,'no ip dhcp conflict ping-detection enable ')
    SetCmd(switch3,'no ip dhcp pool vlan20')
    SetCmd(switch3,'no ip dhcp pool vlan4091')
    SetCmd(switch3,'no ip dhcp pool vlan4092')
    SetCmd(switch3,'no ip dhcp excluded-address ' + If_vlan4091_s3_ipv4)
    SetCmd(switch3,'no ip dhcp excluded-address ' + If_vlan4092_s3_ipv4)
    SetCmd(switch3,'no ip dhcp excluded-address ' + If_vlan20_s3_ipv4)
    # vlan
    SetCmd(switch3,'no interface vlan',Vlan4091)
    SetCmd(switch3,'no interface vlan',Vlan4092)
    SetCmd(switch3,'no','vlan',Vlan4091)
    SetCmd(switch3,'no','vlan',Vlan4092)
    #Interface
    EnterConfigMode(switch3)
    SetCmd(switch3,'interface',s3p3)
    SetCmd(switch3,'no switchport mode')
    SetCmd(switch3,'interface',s3p4)
    SetCmd(switch3,'no switchport mode')

#--------------  AP1  uninitial ------------------
# SetCmd(ap1,'\n')
# SetCmd(ap1,CMD_Set_management_staticip)
# #SetCmd(ap1,'set management static-ipv6','::')
# SetCmd(ap1,'set management static-ipv6')
# SetCmd(ap1,'set static-ip-route gateway')
# #SetCmd(ap1,'set static-ipv6-route gateway','::')
# SetCmd(ap1,'set static-ipv6-route gateway')
# SetCmd(ap1,'save-running')


#--------------  AP2  uninitial ------------------
# SetCmd(ap2,'\n')
# SetCmd(ap2,CMD_Set_management_staticip)
# #SetCmd(ap2,'set management static-ipv6','::')
# SetCmd(ap2,'set management static-ipv6')
# SetCmd(ap2,'set static-ip-route gateway')
# #SetCmd(ap2,'set static-ipv6-route gateway','::')
# SetCmd(ap2,'set static-ipv6-route gateway')
# SetCmd(ap2,'save-running')

#---------------  PC1 -----------------------------
#清除PC1默认网关配置
SetCmd(pc1,'route del -net default gw',If_vlan192_s3_ipv4)


######################## 保存各交换机配置 #####################

EnterEnableMode(switch1)
data = SetCmd(switch1,'write',timeout=1)
if 0==CheckLine(data,'Y/N'):
   SetCmd(switch1,'y',timeout=3)
SetCmd(switch1,'y',timeout=3)

EnterEnableMode(switch2)
data = SetCmd(switch2,'write',timeout=1)
if 0==CheckLine(data,'Y/N'):
   SetCmd(switch2,'y',timeout=3)
SetCmd(switch2,'y',timeout=3)
   
EnterEnableMode(switch3)
data = SetCmd(switch3,'write',timeout=1)
if 0==CheckLine(data,'Y/N'):
   SetCmd(switch3,'y',timeout=3)
SetCmd(switch3,'y',timeout=3)

SetCmd(ap1,'set managed-ap mode up')
SetCmd(ap2,'set managed-ap mode up')
SetCmd(switch1,'show run')
SetCmd(switch3,'show run')
printUninitialTimer('TestCase Uninitial','End')

