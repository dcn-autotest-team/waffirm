#-*- coding: UTF-8 -*-#
#*******************************************************************************
# initial(ipv6).py
#
# Author:  zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2008 Digital China Networks Co. Ltd
#
# Features: 初始设置
#
#*******************************************************************************
# Change log:
#     - 2017.12.14 created by zhangjxp
#*******************************************************************************

#交换机初始配置(ipv6)
#---------------------------  初始化AC1(ipv6)  ---------------------------------------
# 删除IPV4地址，配置IPV6地址
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan',Vlan70)
SetCmd(switch1,'no interface vlan',Vlan80)
SetCmd(switch1,'no interface loopback 100')

SetCmd(switch1,'interface vlan',Vlan70)
SetCmd(switch1,'ipv6 address',If_vlan70_s1_ipv6)
IdleAfter(3)

EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan80)
SetCmd(switch1,'ipv6 address',If_vlan80_s1_ipv6)
IdleAfter(3)

EnterWirelessMode(switch1)
SetCmd(switch1,'no static-ip')
SetCmd(switch1,'static-ipv6',If_vlan70_s1_ipv6_s)

EnterEnableMode(switch1)
data = SetCmd(switch1,'write',timeout=1)
SetCmd(switch1,'y',timeout=1)

#---------------------------  初始化AC2(ipv6)  ---------------------------------------
# 删除IPV4地址，配置IPV6地址
EnterConfigMode(switch2)
SetCmd(switch2,'no interface vlan',Vlan70)
SetCmd(switch2,'no interface vlan',Vlan80)

SetCmd(switch2,'interface vlan',Vlan70)
SetCmd(switch2,'ipv6 address',If_vlan70_s2_ipv6)
IdleAfter(3)

SetCmd(switch2,'interface vlan',Vlan80)
SetCmd(switch2,'ipv6 address',If_vlan80_s2_ipv6)
IdleAfter(3)

EnterWirelessMode(switch2)
SetCmd(switch2,'no static-ip')
SetCmd(switch2,'static-ipv6',If_vlan70_s2_ipv6_s)

EnterEnableMode(switch2)
data = SetCmd(switch2,'write',timeout=1)
SetCmd(switch2,'y',timeout=1)
