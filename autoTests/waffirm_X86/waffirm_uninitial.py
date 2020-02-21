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

SetCmd(ap1,'')
SetCmd(ap1,'')
SetCmd(ap1,'')
SetCmd(ap1,'admin')
SetCmd(ap1,'admin')
SetCmd(ap1,'admin')
SetCmd(ap1,'admin')
SetCmd(ap1,'ifconfig ath0 down')
SetCmd(ap1,'ifconfig ath1 down')
SetCmd(ap1,'ifconfig ath16 down')

SetCmd(ap2,'')
SetCmd(ap2,'')
SetCmd(ap2,'')
SetCmd(ap2,'admin')
SetCmd(ap2,'admin')
SetCmd(ap2,'admin')
SetCmd(ap2,'admin')
SetCmd(ap2,'ifconfig ath0 down')
SetCmd(ap2,'ifconfig ath1 down')
SetCmd(ap2,'ifconfig ath16 down')
##SetCmd(ap1,CMD_Set_management_staticip)

#-----------------------  S1 uninitial ------------------

#wireless mode
##EnterWirelessMode(switch1)
##SetCmd(switch1,'no discovery ip-list')
##SetCmd(switch1,'no discovery ipv6-list')
##SetCmd(switch1,'no discovery vlan-list')
##SetCmd(switch1,'no ap database',ap1mac)
##SetCmd(switch1,'no ap database',ap2mac)
##
##EnterWirelessMode(switch2)
##SetCmd(switch2,'no ap database',ap1mac)
##SetCmd(switch2,'no ap database',ap2mac)
##
##RebootAp(AP=ap1)
##RebootAp(AP=ap2)
##SetCmd(switch1,'no ap profile','2')   
##SetCmd(switch1,'no','static-ip')
##SetCmd(switch1,'no','static-ipv6')
##SetCmd(switch1,'no','l2tunnel vlan-list add')
###network mode
##EnterNetworkMode(switch1,'1')
##data = SetCmd(switch1,'clear',timeout=3)
##if 0 == CheckLine(data,'Y/N'):
##    SetCmd(switch1,'y',timeout=3)
##SetCmd(switch1,'y',timeout=3)
##
##EnterNetworkMode(switch1,'2')
##data = SetCmd(switch1,'clear',timeout=3)
##if 0 == CheckLine(data,'Y/N'):
##    SetCmd(switch1,'y',timeout=3)
##SetCmd(switch1,'y',timeout=3)
###profile mode
##EnterApProMode(switch1,'1')
##data = SetCmd(switch1,'clear',timeout=3)
##if 0 == CheckLine(data,'Y/N'):
##    SetCmd(switch1,'y',timeout=3)
##SetCmd(switch1,'y',timeout=3)
##
###DHCP
##EnterConfigMode(switch1)
##SetCmd(switch1,'no service dhcp')
##SetCmd(switch1,'no ip dhcp pool pool4091')
##SetCmd(switch1,'no ip dhcp pool pool4092')
##SetCmd(switch1,'no ip dhcp pool pool4093')
###vlan
##SetCmd(switch1,'no interface vlan',Vlan40)
##SetCmd(switch1,'no interface vlan',Vlan4091)
##SetCmd(switch1,'no interface vlan',Vlan4092)
##SetCmd(switch1,'no interface vlan',Vlan4093)
##SetCmd(switch1,'no interface loopback 1')
##SetCmd(switch1,'no','vlan',Vlan40)
##SetCmd(switch1,'no','vlan',Vlan4091)
##SetCmd(switch1,'no','vlan',Vlan4092)
##SetCmd(switch1,'no','vlan',Vlan4093)
##SetCmd(switch1,'no','router ospf')
##
##
###------------------------  S2 uninitial -----------------------
##
###wireless mode
##EnterWirelessMode(switch2)
##SetCmd(switch2,'no ap profile','2') 
##SetCmd(switch2,'no discovery ip-list')
##SetCmd(switch2,'no discovery ipv6-list')
##SetCmd(switch2,'no discovery vlan-list')  
##SetCmd(switch2,'no','static-ip')
##SetCmd(switch2,'no','static-ipv6')
##SetCmd(switch2,'no','l2tunnel vlan-list add')
###network mode
##EnterNetworkMode(switch2,'1')
##data = SetCmd(switch2,'clear',timeout=3)
##if 0==CheckLine(data,'Y/N'):
##    SetCmd(switch2,'y',timeout=3)
##SetCmd(switch2,'y',timeout=3)
##
##EnterNetworkMode(switch2,'2')
##data = SetCmd(switch2,'clear',timeout=3)
##if 0==CheckLine(data,'Y/N'):
##    SetCmd(switch2,'y',timeout=3)
##SetCmd(switch2,'y',timeout=3)
###profile mode
##EnterApProMode(switch2,'1')
##data = SetCmd(switch2,'clear',timeout=3)
##if 0==CheckLine(data,'Y/N'):
##    SetCmd(switch2,'y',timeout=3)
##SetCmd(switch2,'y',timeout=3)
##
###DHCP
##EnterConfigMode(switch2)
##SetCmd(switch2,'no service dhcp')
##SetCmd(switch2,'no ip dhcp pool pool4091')
##SetCmd(switch2,'no ip dhcp pool pool4092')
##SetCmd(switch2,'no ip dhcp pool pool4093')
###vlan
##SetCmd(switch2,'no interface vlan',Vlan30)
##SetCmd(switch2,'no interface vlan',Vlan4091)
##SetCmd(switch2,'no interface vlan',Vlan4092)
##SetCmd(switch2,'no interface vlan',Vlan4093)
##SetCmd(switch2,'no interface loopback 1')
##SetCmd(switch2,'no','vlan',Vlan30)
##SetCmd(switch2,'no','vlan',Vlan4091)
##SetCmd(switch2,'no','vlan',Vlan4092)
##SetCmd(switch2,'no','vlan',Vlan4093)
##SetCmd(switch2,'no','router ospf')
##
##
###------------------------  S3 uninitial ----------------------
###vlan
##EnterConfigMode(switch3)
##SetCmd(switch3,'no interface vlan',Vlan20)
##SetCmd(switch3,'no interface vlan',Vlan30)
##SetCmd(switch3,'no interface vlan',Vlan40)
##SetCmd(switch3,'no interface vlan',Vlan192)
##SetCmd(switch3,'no','vlan',Vlan20)
##SetCmd(switch3,'no','vlan',Vlan30)
##SetCmd(switch3,'no','vlan',Vlan40)
##SetCmd(switch3,'no','vlan',Vlan192)
###router ospf
##SetCmd(switch3,'no','router ospf')
##EnterEnableMode(switch3)
##
##
###--------------  AP1  uninitial ------------------
##SetCmd(ap1,'\n')
##SetCmd(ap1,CMD_Set_management_staticip)
###SetCmd(ap1,'set management static-ipv6','::')
##SetCmd(ap1,'set management static-ipv6')
##SetCmd(ap1,'set static-ip-route gateway')
###SetCmd(ap1,'set static-ipv6-route gateway','::')
##SetCmd(ap1,'set static-ipv6-route gateway')
##SetCmd(ap1,'save-running')
##
##
###--------------  AP2  uninitial ------------------
##SetCmd(ap2,'\n')
##SetCmd(ap2,CMD_Set_management_staticip)
###SetCmd(ap2,'set management static-ipv6','::')
##SetCmd(ap2,'set management static-ipv6')
##SetCmd(ap2,'set static-ip-route gateway')
###SetCmd(ap2,'set static-ipv6-route gateway','::')
##SetCmd(ap2,'set static-ipv6-route gateway')
##SetCmd(ap2,'save-running')
##
###---------------  PC1 -----------------------------
###清除PC1默认网关配置
##SetCmd(pc1,'route del -net default gw',If_vlan192_s3_ipv4)
##
##
########################## 保存各交换机配置 #####################

##data = SetCmd(switch1,'write',timeout=1)
##if 0==CheckLine(data,'Y/N'):
##    SetCmd(switch1,'y',timeout=3)
##SetCmd(switch1,'y',timeout=3)
##
##EnterEnableMode(switch2)
##data = SetCmd(switch2,'write',timeout=1)
##if 0==CheckLine(data,'Y/N'):
##    SetCmd(switch2,'y',timeout=3)
##SetCmd(switch2,'y',timeout=3)
##    
##EnterEnableMode(switch3)
##data = SetCmd(switch3,'write',timeout=1)
##if 0==CheckLine(data,'Y/N'):
##    SetCmd(switch3,'y',timeout=3)
##SetCmd(switch3,'y',timeout=3)

printUninitialTimer('TestCase Uninitial','End')
