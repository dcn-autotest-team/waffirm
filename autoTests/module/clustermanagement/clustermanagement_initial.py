#-*- coding: UTF-8 -*-#
#*******************************************************************************
# initial.py
#
# Author:  humj
#
# Version 1.0.0
#
# Copyright (c) 2004-2008 Digital China Networks Co. Ltd
#
# Features: 初始设置
#
#*******************************************************************************
# Change log:
#     - 2017.12.14 created by humj
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
printInitialTimer('TestCase Initial','Start')

#各设备恢复出厂设置
if set_default == 1:#this defined in topo file
    print('setting default')

    if EnvNo == '4':#云AC环境S1-2恢复出厂设置
        SetDefault(switch3)
        EnterEnableMode(switch3)
        Receiver(switch3,'write',timeout=1)
        IdleAfter(1)
        Receiver(switch3,'y',timeout=3)
        ReloadMultiSwitch([switch3])
        ac1 = 'ac1'
        ac2 = 'ac2'
        CreateNewConn('Telnet',ac1,switch1_host,None,'run')
        CreateNewConn('Telnet',ac2,switch2_host,None,'run')
        Receiver(ac1,'\n\n')
        Receiver(ac2,'\n\n')
        TelnetLogin('ac1',Pc1_telnet_name,Pc1_telnet_password)
        TelnetLogin('ac2',Pc1_telnet_name,Pc1_telnet_password)

        SetCmd(ac1,'pkill -9 dcn_console')
        SetCmd(ac1,'pkill -9 monitor.sh')
        SetCmd(ac1,'pkill -9 nos.img')
        SetCmd(ac1,'rm /home/dscc/startup.cfg')

        SetCmd(ac2,'pkill -9 dcn_console')
        SetCmd(ac2,'pkill -9 monitor.sh')
        SetCmd(ac2,'pkill -9 nos.img')
        SetCmd(ac2,'rm /home/dscc/startup.cfg')

        Receiver(switch1,'\n\n')
        SetCmd(switch1,'cd /home/dscc',timeout=5)
        SetCmd(switch1,'./start.sh nos.img',promoteStop=30)
        SetCmd(switch1,'./dcn_console',timeout=10)
        Receiver(switch1,'\n\n')

        SetCmd(switch2,'cd /home/dscc',timeout=5)
        SetCmd(switch2,'./start.sh nos.img',promoteStop=30)
        SetCmd(switch2,'./dcn_console',timeout=10)
        Receiver(switch2,'\n\n')
        #AP1-2恢复出厂设置
        FactoryResetMultiAp([ap1,ap2])
        Receiver(switch1,'\n\n\n',timeout=1)
        Receiver(switch2,'\n\n\n',timeout=1)
        Receiver(switch3,'\n\n\n',timeout=1)
        EnterEnableMode(switch1)
        EnterEnableMode(switch2)
        EnterEnableMode(switch3)
        Receiver(switch1,'terminal length 0')
        Receiver(switch2,'terminal length 0')
        Receiver(switch3,'terminal length 0')
        #登录AP1,AP2 
        ApLogin(ap1)
        ApLogin(ap2)
    else:
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
        reloadallsut(AP=[ap1,ap2],SWITCH=[switch1,switch2,switch3]) 

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
printRes('Check the software version of s2...')
ShowVersion(switch2)

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
EnterConfigMode(switch1)
SetCmd(switch1,'watchdog disable')
SetCmd(switch1,'exec-timeout 0')
SetCmd(switch1,'no interface vlan 1')
SetCmd(switch1,'vlan',Vlan70)
SetCmd(switch1,'vlan',Vlan80)

EnterConfigMode(switch1)
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'switchport mode trunk')
SetCmd(switch1,'switchport trunk allowed vlan',Vlan70+';'+Vlan80)
SetCmd(switch1,'exit')

EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan70)
SetCmd(switch1,'ip address',If_vlan70_s1_ipv4)
SetCmd(switch1,'ipv6 address',If_vlan70_s1_ipv6)
IdleAfter(3)

EnterConfigMode(switch1)
SetCmd(switch1,'interface vlan',Vlan80)
SetCmd(switch1,'ip address',If_vlan80_s1_ipv4)
SetCmd(switch1,'ipv6 address',If_vlan80_s1_ipv6)
IdleAfter(3)

EnterConfigMode(switch1)
SetCmd(switch1,'interface loopback 100')
SetCmd(switch1,'ip address',StaticIpv4_ac1,'255.255.255.255')
IdleAfter(3)

EnterConfigMode(switch1)
SetCmd(switch1,'router rip')
SetCmd(switch1,'network 0.0.0.0/0')

#配置wireless视图下的参数
EnterWirelessMode(switch1)
SetCmd(switch1,'enable')
SetCmd(switch1,'ap authentication none')
SetCmd(switch1,'no auto-ip-assign')
SetCmd(switch1,'static-ip',If_vlan70_s1_ipv4_s)
SetCmd(switch1,'static-ipv6',If_vlan70_s1_ipv6_s)

#配置Network1
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'ssid',Network_name1)
SetCmd(switch1,'vlan',Vlan80)

#配置Network2
EnterNetworkMode(switch1,'2')
SetCmd(switch1,'ssid',Network_name2)
SetCmd(switch1,'vlan',Vlan80)

#配置Ap-profile1
EnterApProMode(switch1,'1')
SetCmd(switch1,'hwtype',hwtype1)
SetCmd(switch1,'radio 1')
SetCmd(switch1,'vap 1')
SetCmd(switch1,'no enable')
SetCmd(switch1,'enable')
SetCmd(switch1,'exit')
SetCmd(switch1,'exit')
SetCmd(switch1,'radio 2')
SetCmd(switch1,'vap 1')
SetCmd(switch1,'no enable')
SetCmd(switch1,'enable')

#配置Ap-profile2
EnterApProMode(switch1,'2')
SetCmd(switch1,'hwtype',hwtype2)
SetCmd(switch1,'radio 1')
SetCmd(switch1,'vap 1')
SetCmd(switch1,'enable')
SetCmd(switch1,'exit')
SetCmd(switch1,'exit')
SetCmd(switch1,'radio 2')
SetCmd(switch1,'vap 1')
SetCmd(switch1,'enable')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'profile 1')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap2mac)
SetCmd(switch1,'profile 2')

#---------------------------  初始化AC2  ---------------------------------------
EnterConfigMode(switch2)
SetCmd(switch2,'watchdog disable')
SetCmd(switch2,'exec-timeout 0')
SetCmd(switch2,'no interface vlan 1')
SetCmd(switch2,'vlan',Vlan70)
SetCmd(switch2,'vlan',Vlan80)

SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'switchport mode trunk')
SetCmd(switch2,'switchport trunk allowed vlan',Vlan70+';'+Vlan80)

SetCmd(switch2,'interface vlan',Vlan70)
SetCmd(switch2,'ip address',If_vlan70_s2_ipv4)
SetCmd(switch2,'ipv6 address',If_vlan70_s2_ipv6)

SetCmd(switch2,'interface vlan',Vlan80)
SetCmd(switch2,'ip address',If_vlan80_s2_ipv4)
SetCmd(switch2,'ipv6 address',If_vlan80_s2_ipv6)

EnterConfigMode(switch2)
SetCmd(switch2,'router rip')
SetCmd(switch2,'network 0.0.0.0/0')

#配置wireless视图下的参数
EnterWirelessMode(switch2)
SetCmd(switch2,'enable')
SetCmd(switch2,'ap authentication none')
SetCmd(switch2,'no auto-ip-assign')
SetCmd(switch2,'static-ip',If_vlan70_s2_ipv4_s)
SetCmd(switch2,'static-ipv6',If_vlan70_s2_ipv6_s)

#配置Network1
EnterNetworkMode(switch2,1)
SetCmd(switch2,'ssid',Network_name1)
SetCmd(switch2,'vlan',Vlan80)

#配置Network2
EnterNetworkMode(switch2,2)
SetCmd(switch2,'ssid',Network_name2)
SetCmd(switch2,'vlan',Vlan80)

#配置Ap-profile1
EnterApProMode(switch2,1)
SetCmd(switch2,'hwtype',hwtype1)
SetCmd(switch2,'radio 1')
SetCmd(switch2,'vap 1')
SetCmd(switch2,'enable')
SetCmd(switch2,'exit')
SetCmd(switch2,'exit')
SetCmd(switch2,'radio 2')
SetCmd(switch2,'vap 1')
SetCmd(switch2,'enable')

#配置Ap-profile2
EnterApProMode(switch2,2)
SetCmd(switch2,'hwtype',hwtype2)
SetCmd(switch2,'radio 1')
SetCmd(switch2,'vap 1')
SetCmd(switch2,'enable')
SetCmd(switch2,'exit')
SetCmd(switch2,'exit')
SetCmd(switch2,'radio 2')
SetCmd(switch2,'vap 1')
SetCmd(switch2,'enable')

EnterWirelessMode(switch2)
SetCmd(switch2,'ap database',ap1mac)
SetCmd(switch2,'profile 1')
EnterWirelessMode(switch2)
SetCmd(switch2,'ap database',ap2mac)
SetCmd(switch2,'profile 2')


#---------------------------  初始化 S3  ---------------------------------------
EnterConfigMode(switch3)
SetCmd(switch3,'vlan',Vlan70+';'+Vlan80+';'+Vlan192)
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p1)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk allowed vlan',Vlan70+';'+Vlan80)
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p2)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk allowed vlan',Vlan70+';'+Vlan80)
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan70)
SetCmd(switch3,'switchport trunk allowed vlan',Vlan80)
SetCmd(switch3,'exit')
SetCmd(switch3,'interface',s3p4)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan70)
SetCmd(switch3,'switchport trunk allowed vlan',Vlan80)
SetCmd(switch3,'exit')
SetCmd(switch3,'interface',s3p5)
SetCmd(switch3,'switchport mode access')
SetCmd(switch3,'switchport access vlan',Vlan192)
SetCmd(switch3,'interface vlan',Vlan192)
SetCmd(switch3,'ip address',If_vlan192_s3_ipv4,'255.255.255.0')
SetCmd(switch3,'exit')
SetCmd(switch3,'router rip')
SetCmd(switch3,'network 0.0.0.0/0')


#---------------------------  初始化AP1  ---------------------------------------
SetCmd(ap1,'\n')
ApSetcmd(ap1,Ap1cmdtype,'set_static_ip',Ap1_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6',Ap1_ipv6)
ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_down')
ApSetcmd(ap1,Ap1cmdtype,'set_dhcpv6_down')
ApSetcmd(ap1,Ap1cmdtype,'set_ip_route',If_vlan70_s3_ipv4_s)
ApSetcmd(ap1,Ap1cmdtype,'set_ipv6_route',If_vlan70_s3_ipv6_s)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6_prefix_len','64')
ApSetcmd(ap1,Ap1cmdtype,'saverunning')


#---------------------------  初始化AP2  ---------------------------------------
SetCmd(ap2,'\n')
ApSetcmd(ap2,Ap2cmdtype,'set_static_ip',Ap2_ipv4)
ApSetcmd(ap2,Ap2cmdtype,'set_static_ipv6',Ap2_ipv6)
ApSetcmd(ap2,Ap2cmdtype,'set_dhcp_down')
ApSetcmd(ap2,Ap2cmdtype,'set_dhcpv6_down')
ApSetcmd(ap2,Ap2cmdtype,'set_ip_route',If_vlan70_s3_ipv4_s)
ApSetcmd(ap2,Ap2cmdtype,'set_ipv6_route',If_vlan70_s3_ipv6_s)
ApSetcmd(ap2,Ap2cmdtype,'set_static_ipv6_prefix_len','64')
ApSetcmd(ap2,Ap2cmdtype,'saverunning')


#----------------------- PC1，STA1，STA2 配置实验网路由,保持控制连接-------------------------------
# 配置PC1默认网关
SetCmd(pc1,'route add -net default gw',If_vlan192_s3_ipv4)
#----------------------- 初始化STA1，STA2，开启wpa_supplicant-------------------------------
#开启sta1，sta2的wpa_supplicant
SetCmd(sta1,'ifconfig %s up' % Netcard_sta1)
IdleAfter(2)
data = SetCmd(sta1,'iwconfig')
if CheckLine(data,'%s' % Netcard_sta1)!=0:
    SetCmd(sta1,'rmmod iwldvm')
    SetCmd(sta1,'rmmod iwlwifi')
    IdleAfter(5)
    SetCmd(sta1,'modprobe iwlwifi')
#data = SetCmd(sta1,'ifconfig mon0')
if CheckLine(data,'mon0')!=0:
    SetCmd(sta1,'airmon-ng start ' + Netcard_sta1)
IdleAfter(2)	
SetCmd(sta1,'pkill -9 wpa_supplicant')
IdleAfter(3)
SetCmd(sta1,'wpa_supplicant -B -i '+ Netcard_sta1 +' -c /etc/wpa_supplicant/wpa_supplicant.conf -f /tmp/wpa_log/%s.log' % Netcard_sta1)

SetCmd(sta2,'ifconfig %s up' % Netcard_sta2)
IdleAfter(2)
data = SetCmd(sta2,'iwconfig')
if CheckLine(data,'%s' % Netcard_sta2)!=0:
    SetCmd(sta2,'rmmod iwldvm')
    SetCmd(sta2,'rmmod iwlwifi')
    IdleAfter(5)
    SetCmd(sta2,'modprobe iwlwifi')
#data = SetCmd(sta2,'ifconfig mon0')
if CheckLine(data,'mon0')!=0:
    SetCmd(sta2,'airmon-ng start ' + Netcard_sta2)
IdleAfter(2)
SetCmd(sta2,'pkill -9 wpa_supplicant')
IdleAfter(3)
SetCmd(sta2,'wpa_supplicant -B -i '+ Netcard_sta2 +' -c /etc/wpa_supplicant/wpa_supplicant.conf -f /tmp/wpa_log/%s.log' % Netcard_sta2)

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

EnterEnableMode(switch3)
SetCmd(switch3,'clock set 09:00:00 2012.12.21')
IdleAfter('1')   
EnterEnableMode(switch3)
data = SetCmd(switch3,'write',timeout=1)
SetCmd(switch3,'y',timeout=2)
# end
printInitialTimer('TestCase Initial','End')
