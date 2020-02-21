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
SetCmd(switch1,'no ap database',ap1mac)
SetCmd(switch1,'no ap database',ap2mac)
SetCmd(switch1,'no','static-ip')
SetCmd(switch1,'no','static-ipv6')
SetCmd(switch1,'no','l2tunnel vlan-list')
SetCmd(switch1,'no ap profile','2')
SetCmd(switch1,'discovery vlan-list 1')
   
#network mode
ClearNetworkConfig(switch1,'1')
ClearNetworkConfig(switch1,'2')

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
SetCmd(switch1,'no interface vlan',Vlan70)
SetCmd(switch1,'no interface vlan',Vlan80)
SetCmd(switch1,'no interface loopback 100')
SetCmd(switch1,'no','vlan',Vlan70)
SetCmd(switch1,'no','vlan',Vlan80)
SetCmd(switch1,'no','router rip')

#------------------------  S2 uninitial -----------------------
#wireless mode
EnterWirelessMode(switch2)
SetCmd(switch2,'no ap database',ap1mac)
SetCmd(switch2,'no ap database',ap2mac)
SetCmd(switch2,'no','static-ip')
SetCmd(switch2,'no','static-ipv6')
SetCmd(switch2,'no','l2tunnel vlan-list')
SetCmd(switch2,'no ap profile','2')
SetCmd(switch2,'discovery vlan-list 1')
#network mode
ClearNetworkConfig(switch2,'1')
ClearNetworkConfig(switch2,'2')

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
SetCmd(switch2,'no interface vlan',Vlan70)
SetCmd(switch2,'no interface vlan',Vlan80)
SetCmd(switch2,'no','vlan',Vlan70)
SetCmd(switch2,'no','vlan',Vlan80)
SetCmd(switch2,'no','router rip')


#------------------------  S3 uninitial ----------------------
#vlan
EnterConfigMode(switch3)
SetCmd(switch3,'no interface vlan',Vlan70)
SetCmd(switch3,'no interface vlan',Vlan80)
SetCmd(switch3,'no interface vlan',Vlan192)
SetCmd(switch3,'no','vlan',Vlan70)
SetCmd(switch3,'no','vlan',Vlan80)
SetCmd(switch3,'no','vlan',Vlan192)
# interface
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s2p1)
SetCmd(switch3,'no switchport mode')
SetCmd(switch3,'interface',s2p2)
SetCmd(switch3,'no switchport mode')
SetCmd(switch3,'interface',s2p3)
SetCmd(switch3,'no switchport mode')
SetCmd(switch3,'interface',s2p4)
SetCmd(switch3,'no switchport mode')
SetCmd(switch3,'interface',s2p5)
SetCmd(switch3,'no switchport mode')
#router ospf
SetCmd(switch3,'no','router rip')
EnterEnableMode(switch3)

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
printUninitialTimer('TestCase Uninitial','End')
