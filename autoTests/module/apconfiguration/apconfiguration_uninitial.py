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

SetCmd(ap1,'set managed-ap mode down')
SetCmd(ap2,'set managed-ap mode down')

#-----------------------  S1 uninitial ------------------

#wireless mode
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery ip-list')
SetCmd(switch1,'no ap database',ap1mac)
SetCmd(switch1,'no ap database',ap2mac)
SetCmd(switch1,'no','static-ip')
SetCmd(switch1,'no ap profile','2')
SetCmd(switch1,'discovery method l2-multicast')
SetCmd(switch1,'discovery vlan-list 1')
   
#network mode
ClearNetworkConfig(switch1,'1')

#profile mode
ClearProfileConfig(switch1,'1')

# wireless
EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter('5')
SetCmd(switch1,'enable')

# interface
EnterConfigMode(switch1)
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'no switchport mode')
#vlan
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan',Vlan1)
SetCmd(switch1,'no','vlan',Vlan1)
SetCmd(switch1,'no','router rip')
# # 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
# if testcentral:
    # #DHCP
    # EnterConfigMode(switch1)
    # SetCmd(switch1,'no service dhcp')
    # SetCmd(switch1,'no ip dhcp pool pool4091')
    # SetCmd(switch1,'no ip dhcp pool pool4092')
    # SetCmd(switch1,'no ip dhcp pool pool4093')
    # SetCmd(switch1,'no ip dhcp excluded-address ' + If_vlan4091_s1_ipv4)
    # SetCmd(switch1,'no ip dhcp excluded-address ' + If_vlan4092_s1_ipv4)
    # SetCmd(switch1,'no ip dhcp excluded-address ' + If_vlan4093_s1_ipv4)
    # SetCmd(switch1,'no ip dhcp excluded-address ' + If_vlan4091_s2_ipv4)
    # SetCmd(switch1,'no ip dhcp excluded-address ' + If_vlan4092_s2_ipv4)
    # SetCmd(switch1,'no ip dhcp excluded-address ' + If_vlan4093_s2_ipv4)
    # # vlan
    # SetCmd(switch1,'no interface vlan',Vlan4091)
    # SetCmd(switch1,'no interface vlan',Vlan4092)
    # SetCmd(switch1,'no interface vlan',Vlan4093)
    # SetCmd(switch1,'no','vlan',Vlan4091)
    # SetCmd(switch1,'no','vlan',Vlan4092)
    # SetCmd(switch1,'no','vlan',Vlan4093)

#------------------------  S2 uninitial -----------------------

#wireless mode
EnterWirelessMode(switch2)
SetCmd(switch2,'no discovery ip-list')
SetCmd(switch2,'no ap database',ap1mac)
SetCmd(switch2,'no ap database',ap2mac)
SetCmd(switch2,'no','static-ip')
SetCmd(switch2,'no ap profile','2')
SetCmd(switch2,'discovery method l2-multicast')
SetCmd(switch2,'discovery vlan-list 1')
#network mode
ClearNetworkConfig(switch2,'1')

#profile mode
ClearProfileConfig(switch2,'1')

# wireless
EnterWirelessMode(switch2)
SetCmd(switch2,'no enable')
IdleAfter('5')
SetCmd(switch2,'enable')

# interface
EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'no switchport mode')
#vlan
EnterConfigMode(switch2)
SetCmd(switch2,'no interface vlan',Vlan1)
SetCmd(switch2,'no','vlan',Vlan1)
SetCmd(switch2,'no','router rip')

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

SetCmd(ap1,'set managed-ap mode up')
SetCmd(ap2,'set managed-ap mode up')

printUninitialTimer('TestCase Uninitial','End')
