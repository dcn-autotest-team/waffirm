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

#交换机清除初始配置(ipv6)
#---------------------------  清除初始化配置AC1(ipv6)  ---------------------------------------
# 删除IPV6地址，配置IPV4地址
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan',Vlan70)
SetCmd(switch1,'no interface vlan',Vlan80)

SetCmd(switch1,'interface vlan',Vlan70)
SetCmd(switch1,'ip address',If_vlan70_s1_ipv4)
IdleAfter(3)

SetCmd(switch1,'interface vlan',Vlan80)
SetCmd(switch1,'ip address',If_vlan80_s1_ipv4)
IdleAfter(3)

SetCmd(switch1,'interface loopback 100')
SetCmd(switch1,'ip address',StaticIpv4_ac1,'255.255.255.255')
IdleAfter(3)

EnterWirelessMode(switch1)
SetCmd(switch1,'no static-ipv6')
SetCmd(switch1,'static-ip',If_vlan70_s1_ipv4_s)

EnterEnableMode(switch1)
data = SetCmd(switch1,'write',timeout=1)
SetCmd(switch1,'y',timeout=1)

#---------------------------  清除初始化配置AC2(ipv6)  ---------------------------------------
# 删除IPV6地址，配置IPV4地址
EnterConfigMode(switch2)
SetCmd(switch2,'no interface vlan',Vlan70)
SetCmd(switch2,'no interface vlan',Vlan80)

SetCmd(switch2,'interface vlan',Vlan70)
SetCmd(switch2,'ip address',If_vlan70_s2_ipv4)
IdleAfter(3)

SetCmd(switch2,'interface vlan',Vlan80)
SetCmd(switch2,'ip address',If_vlan80_s2_ipv4)
IdleAfter(3)

EnterWirelessMode(switch2)
SetCmd(switch2,'no static-ipv6')
SetCmd(switch2,'static-ip',If_vlan70_s2_ipv4_s)

EnterEnableMode(switch2)
data = SetCmd(switch2,'write',timeout=1)
SetCmd(switch2,'y',timeout=1)
