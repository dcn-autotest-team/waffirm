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
#     - 2017.2.27 lupingc RDM46364 获取ap1 dhcp option60版本号
#     - 2017.6.1 lupingc ac1配置登录用户名和密码
#     - 2017.10.27 zhangjxp RDM50238
#     - 2017.11.10 zhangjxp RDM50321
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
#*******************************************************************************
import os
import time
import re
import wx


def reloadallsut(**kargs):
    '''
    功能:使用多线程重启所有设备
    参数：AP或SWITCH类型的设备，参数格式：AP=[ap1,ap2],SWITCH=[switch1,switch2,switch3]
    返回：None
    举例：reloadallsut(AP=[ap1,ap2],SWITCH=[switch1,switch2,switch3]) 
    备注：此函数基本只在初始化过程中使用，其他用例中用到的概率极少
    '''
    threadslist = []
    for type in list(kargs.keys()):
        if type=='AP':
            for ap in kargs[type]:
                Apcmdtype = Ap1cmdtype if ap == 'ap1' else Ap2cmdtype
                t = CallThread(RebootAp,'AP',150,0,'admin','admin',True,AP=ap,apcmdtype=Apcmdtype)
                threadslist.append(t)
        if type=='SWITCH':
            for switch in kargs[type]:
                t = CallThread(ReloadMultiSwitch,[switch])
                threadslist.append(t)
    for t in threadslist:
        t.start()
    for t in threadslist:
        t.join()

#记录日志
printInitialTimer('TestCase Initial', 'Start')

#各设备恢复出厂设置
if set_default == 1:#this defined in topo file
    print('setting default')
    SetDefault(switch1)
    SetDefault(switch2)
    SetDefault(switch3)
    Receiver(switch1,'write',timeout=1)
    Receiver(switch2,'write',timeout=1)
    Receiver(switch3,'write',timeout=1)
    IdleAfter(1)
    Receiver(switch1,'y',timeout=2)
    Receiver(switch2,'y',timeout=2)
    Receiver(switch3,'y',timeout=2)
    #使用多线程对各设备同时进行重启操作
    reloadallsut(AP=[ap1, ap2], SWITCH=[switch1, switch2, switch3])

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
EnterEnableMode(switch1)
SetCmd(switch1, 'show version')
printRes('Check the software version of s2...')
EnterEnableMode(switch2)
SetCmd(switch2, 'show version')

SetCmd(pc1,'cd /root')
SetCmd(pc1,'service dhcpd stop')
SetCmd(sta1,'cd /root')
SetCmd(sta1,'service dhcpd stop')
SetCmd(sta2,'cd /root')
SetCmd(sta2,'service dhcpd stop')

print('initialing ')
avoiderror('Initialial')
#交换机初始配置
#---------------------------  初始化AC1  ---------------------------------------
# 查看AC1默认的wireless protocol
EnterEnableMode(switch1)
data = SetCmd(switch1, 'show wireless')
if CheckLine(data,'Wireless Management Protocol','TCP',IC=True) == 0:
    default_wireless_protocol = 'tcp'
    non_default_wireless_protocol = 'tls'
else:
    default_wireless_protocol = 'tls'
    non_default_wireless_protocol = 'tcp'
EnterConfigMode(switch1)
SetCmd(switch1,'vlan',Vlan1)
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport access vlan',Vlan1)
EnterInterfaceMode(switch1,'vlan '+Vlan1)
IdleAfter(Vlan_Idle_time)
SetCmd(switch1,'no ip address')
SetCmd(switch1,'ip address',StaticIpv4_ac1,'255.255.255.0')

#配置wireless视图下的参数
EnterWirelessMode(switch1)
SetCmd(switch1,'enable')
SetCmd(switch1,'no auto-ip-assign')
SetCmd(switch1,'static-ip',StaticIpv4_ac1)
SetCmd(switch1,'no discovery method l2-multicast')
SetCmd(switch1,'keep-alive-interval 10000')
SetCmd(switch1,'keep-alive-max-count 3')
SetCmd(switch1,'country-code cn')
SetCmd(switch1,'channel enhance disable')

#配置Network1
EnterNetworkMode(switch1,1)
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan ' + Vlan1)

#配置Ap-profile1
EnterApProMode(switch1,1)
SetCmd(switch1,'hwtype',hwtype1)

#配置Ap-profile2
EnterApProMode(switch1,2)
SetCmd(switch1,'hwtype',hwtype2)

EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap2mac)

EnterConfigMode(switch1)
SetCmd(switch1,'router rip')
SetCmd(switch1,'network 0.0.0.0/0')

    
#交换机初始配置
#---------------------------  初始化AC2  ---------------------------------------
EnterConfigMode(switch2)
SetCmd(switch2,'vlan',Vlan1)
EnterInterfaceMode(switch2,s2p1)
SetCmd(switch2,'switchport access vlan',Vlan1)
EnterInterfaceMode(switch2,'vlan '+Vlan1)
IdleAfter(Vlan_Idle_time)
SetCmd(switch2,'no ip address')
SetCmd(switch2,'ip address',StaticIpv4_ac2,'255.255.255.0')

#配置wireless视图下的参数
EnterWirelessMode(switch2)
SetCmd(switch2,'enable')
SetCmd(switch2,'no auto-ip-assign')
SetCmd(switch2,'static-ip',StaticIpv4_ac2)
SetCmd(switch2,'no discovery method l2-multicast')
SetCmd(switch2,'country-code cn')
SetCmd(switch2,'keep-alive-interval 10000')
SetCmd(switch2,'keep-alive-max-count 3')
SetCmd(switch2,'channel enhance disable')
# SetCmd(switch2,'discovery ip-list',StaticIpv4_ac1)
#配置Network1
EnterNetworkMode(switch2,1)
SetCmd(switch2,'ssid',Network_name1)
SetCmd(switch2,'vlan',Vlan1)

#配置Ap-profile1
EnterApProMode(switch2,1)
SetCmd(switch2,'hwtype',hwtype1)

#配置Ap-profile2
EnterApProMode(switch2,2)
SetCmd(switch2,'hwtype',hwtype2)

EnterWirelessMode(switch2)
SetCmd(switch2,'ap database',ap1mac)
EnterWirelessMode(switch2)
SetCmd(switch2,'ap database',ap2mac)

EnterConfigMode(switch2)
SetCmd(switch2,'router rip')
SetCmd(switch2,'network 0.0.0.0/0')
EnterEnableMode(switch2)

#---------------------------  初始化AP1  ---------------------------------------
SetCmd(ap1,'\n')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address',StaticIpv4_ac1,addressnum='1')
ApSetcmd(ap1,Ap1cmdtype,'set_static_ip',Ap1_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'set_ip_route',StaticIpv4_ac1)
ApSetcmd(ap1,Ap1cmdtype,'saverunning')

#---------------------------  初始化AP2  ---------------------------------------
SetCmd(ap2,'\n')
ApSetcmd(ap2,Ap2cmdtype,'set_switch_address',StaticIpv4_ac1,addressnum='1')
ApSetcmd(ap2,Ap2cmdtype,'set_static_ip',Ap2_ipv4)
ApSetcmd(ap2,Ap2cmdtype,'set_ip_route',StaticIpv4_ac1)
ApSetcmd(ap2,Ap2cmdtype,'saverunning')

######################## 保存各交换机配置 ###################
EnterEnableMode(switch1)
SetCmd(switch1,'clock set 09:00:00 2012.12.21')
IdleAfter('1')
data = SetCmd(switch1,'write',timeout=1)
SetCmd(switch1,'y',timeout=2)

EnterEnableMode(switch2)
SetCmd(switch2,'clock set 09:00:00 2012.12.21')
IdleAfter('1')
EnterEnableMode(switch2)
data = SetCmd(switch2,'write',timeout=1)
SetCmd(switch2,'y',timeout=2)

#检测AC1是否成功管理AP1和AP2
EnterEnableMode(switch1)
CheckSutCmd(switch1,'show wireless ap status',
            check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
            waittime=5,retry=20,interval=5,IC=True)
            
printInitialTimer('TestCase Initial','End')