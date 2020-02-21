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
                # Apcmdtype = Ap1cmdtype if ap == 'ap1' else Ap2cmdtype
                Apcmdtype = Ap1cmdtype
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
    SetDefault(switch1)
    SetDefault(switch3)
    Receiver(switch1,'write',timeout=1)
    Receiver(switch3,'write',timeout=1)
    IdleAfter(1)
    Receiver(switch1,'y',timeout=2)
    Receiver(switch3,'y',timeout=2)
    #使用多线程对各设备同时进行重启操作
    reloadallsut(AP=ap_name_list,SWITCH=[switch1,switch3])

SetTerminalLength(switch1)
SetWatchdogDisable(switch1)
SetExecTimeout(switch1)
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

print('initialing ')
#交换机初始配置
#---------------------------  初始化AC1  ---------------------------------------
EnterInterfaceMode(switch1,'loopback 1')
SetCmd(switch1,'ip address',StaticIpv4_ac1,'255.255.255.255')
SetCmd(switch1,'ipv6 address',StaticIpv6_ac1+'/128')
EnterConfigMode(switch1)
SetCmd(switch1,'vlan '+Vlan1)
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport access vlan '+Vlan1)
EnterInterfaceMode(switch1,'vlan '+Vlan1)
IdleAfter(Vlan_Idle_time)
SetCmd(switch1,'no ip address')
SetCmd(switch1,'ip address',If_vlan1_s1_ipv4,'255.255.255.192')
#配置wireless视图下的参数
EnterWirelessMode(switch1)
SetCmd(switch1,'keep-alive-interval 10000')
SetCmd(switch1,'keep-alive-max-count 3')
SetCmd(switch1,'country-code cn')
SetCmd(switch1,'channel enhance disable')
SetCmd(switch1,'enable')
SetCmd(switch1,'static-ip',StaticIpv4_ac1)
SetCmd(switch1,'static-ipv6',StaticIpv6_ac1)
EnterWirelessMode(switch1)
SetCmd(switch1,'no auto-ip-assign')
SetCmd(switch1,'no discovery vlan-list',1)
SetCmd(switch1,'discovery vlan-list',Vlan1)
#配置Network1
EnterNetworkMode(switch1,1)
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan ' + Vlan4091)                  

for i in range(total_apnum):
    #配置Ap-profile1
    EnterApProMode(switch1,i+1)
    SetCmd(switch1,'hwtype',ap_hwtype_list[i])
    SetCmd(switch1,'radio '+radio1num)
    SetCmd(switch1,'rf-scan other-channels interval 5')
    SetCmd(switch1,'rf-scan duration 50')
    SetCmd(switch1,'vap 1')
    SetCmd(switch1,'enable')
    SetCmd(switch1,'exit')
    SetCmd(switch1,'exit')
    SetCmd(switch1,'radio '+radio2num)
    SetCmd(switch1,'mode ac')
    SetCmd(switch1,'vap 1')
    SetCmd(switch1,'enable')
    EnterWirelessMode(switch1)
    SetCmd(switch1,'ap database',ap_mac_list[i])
    SetCmd(switch1,'profile',i+1)
    #配置Discovery ip-list
    # EnterWirelessMode(switch1)
    # SetCmd(switch1,'discovery ip-list',ap_ipv4_list[i])  

EnterConfigMode(switch1)
SetCmd(switch1,'username '+Ssh_login_name+' privilege 15 password 0 '+Ssh_login_password)
SetCmd(switch1,'router rip')
SetCmd(switch1,'network 0.0.0.0/0')

# 集中转发、本地转发差异化配置，如测试集中转发，AC1需进行如下配置
if testcentral == True:
    print('s1 initial centralizedforwarding')
    EnterConfigMode(switch1)
    # SetCmd(switch1,'no interface vlan 1')
    SetCmd(switch1,'vlan',Vlan4091 + '-' + Vlan4093)
    EnterInterfaceMode(switch1,'vlan '+Vlan4091)
    IdleAfter(Vlan_Idle_time)
    SetCmd(switch1,'ip address',If_vlan4091_s1_ipv4,'255.255.255.0')
    SetCmd(switch1,'ipv6 address',If_vlan4091_s1_ipv6+'/64')
    EnterInterfaceMode(switch1,'vlan '+Vlan4092)
    IdleAfter(Vlan_Idle_time)
    SetCmd(switch1,'ip address',If_vlan4092_s1_ipv4,'255.255.255.0')
    #开启DHCP
    EnterConfigMode(switch1)
    SetCmd(switch1,'service dhcp')
    SetCmd(switch1,'ip dhcp excluded-address ' + If_vlan4091_s1_ipv4)
    SetCmd(switch1,'ip dhcp excluded-address ' + If_vlan4091_s2_ipv4)
    SetCmd(switch1,'ip dhcp excluded-address ' + If_vlan4092_s1_ipv4)
    SetCmd(switch1,'ip dhcp excluded-address ' + If_vlan4092_s2_ipv4)
    SetCmd(switch1,'ip dhcp pool pool4091')
    SetCmd(switch1,'network-address ' + Dhcp_pool1 + '0 255.255.255.0')
    SetCmd(switch1,'default-router ' + If_vlan4091_s1_ipv4)
    SetCmd(switch1,'exit')
    SetCmd(switch1,'ip dhcp pool pool4092')
    SetCmd(switch1,'network-address ' + Dhcp_pool2 + '0 255.255.255.0')
    SetCmd(switch1,'default-router ' + If_vlan4092_s1_ipv4)
    SetCmd(switch1,'exit')
    # 配置wireless模式，开启集中转发
    EnterWirelessMode(switch1)
    SetCmd(switch1,'l2tunnel vlan-list add',Vlan4091 + '-' + Vlan4093)
    


# # #---------------------------  初始化AP  ---------------------------------------
# for i in range(total_apnum):
    # SetCmd(ap_name_list[i],'\n')
    # ApSetcmd(ap_name_list[i],ap_cmdtype_list[i],'set_static_ip',ap_ipv4_list[i])
    # ApSetcmd(ap_name_list[i],ap_cmdtype_list[i],'set_dhcp_down')
    # ApSetcmd(ap_name_list[i],ap_cmdtype_list[i],'set_dhcpv6_down')
    # ApSetcmd(ap_name_list[i],ap_cmdtype_list[i],'set_ip_route',If_vlan1_s3_ipv4)
    # ApSetcmd(ap_name_list[i],ap_cmdtype_list[i],'saverunning') 
#---------------------------  初始化 S3  ---------------------------------------

#vlan1
EnterConfigMode(switch3)
SetCmd(switch3,'vlan '+Vlan1)
SetCmd(switch3,'switchport interface',s3p1)
# SetCmd(switch3,'switchport interface',s3p3)
SetCmd(switch3,'switchport interface',s3p6)
EnterInterfaceMode(switch3,'vlan '+Vlan1)
IdleAfter(Vlan_Idle_time)
SetIpAddress(switch3,If_vlan1_s3_ipv4,'255.255.255.192')

#vlan192
EnterConfigMode(switch3)
SetCmd(switch3,'vlan',Vlan192)
SetCmd(switch3,'switchport interface',s3p5)
EnterInterfaceMode(switch3,'vlan '+Vlan192)
IdleAfter(Vlan_Idle_time)
SetIpAddress(switch3,If_vlan192_s3_ipv4,'255.255.255.0')

#router rip
EnterConfigMode(switch3)
SetCmd(switch3,'router rip')
SetCmd(switch3,'network 0.0.0.0/0')
EnterEnableMode(switch3)

EnterConfigMode(switch3)
SetCmd(switch3,'vlan '+Vlan1)
for i in range(total_apnum):
    SetCmd(switch3,'switchport interface',ap_s3port_list[i])
# 集中转发、本地转发差异化配置,如测试本地转发，S3需进行如下配置
if testcentral == False:
    print('s3 initial localforwarding')
    EnterConfigMode(switch3)
    # SetCmd(switch3,'no interface vlan 1')
    SetCmd(switch3,'vlan',Vlan4091 + '-' + Vlan4093)
    EnterInterfaceMode(switch3,'vlan '+Vlan4091)
    IdleAfter(Vlan_Idle_time)
    SetCmd(switch3,'ip address',If_vlan4091_s1_ipv4,'255.255.255.0')
    SetCmd(switch3,'ipv6 address',If_vlan4091_s1_ipv6+'/64')
    EnterInterfaceMode(switch3,'vlan '+Vlan4092)
    IdleAfter(Vlan_Idle_time)
    SetCmd(switch3,'ip address',If_vlan4092_s1_ipv4,'255.255.255.0')
    
    #开启DHCP
    EnterConfigMode(switch3)
    SetCmd(switch3,'service dhcp')
    SetCmd(switch3,'ip dhcp excluded-address',If_vlan4091_s1_ipv4)
    SetCmd(switch3,'ip dhcp excluded-address',If_vlan4092_s1_ipv4)
    SetCmd(switch3,'ip dhcp excluded-address',updateserver)
    SetCmd(switch3,'ip dhcp excluded-address',If_vlan1_s3_ipv4)
    SetCmd(switch3,'ip dhcp excluded-address',If_vlan1_s1_ipv4)
    SetCmd(switch3,'ip dhcp pool vlan4091')
    SetCmd(switch3,'network',Dhcp_pool1 + '2 24')
    SetCmd(switch3,'default-router',If_vlan4091_s1_ipv4)
    SetCmd(switch3,'exit')
    SetCmd(switch3,'ip dhcp pool vlan4092')
    SetCmd(switch3,'network',Dhcp_pool2 + '2 24')
    SetCmd(switch3,'default-router',If_vlan4092_s1_ipv4)
    SetCmd(switch3,'exit')
    SetCmd(switch3,'ip dhcp pool vlan'+Vlan1)
    SetCmd(switch3,'network',If_vlan1_s3_ipv4,'26')
    SetCmd(switch3,'default-router',If_vlan1_s3_ipv4)
    SetCmd(switch3,'exit')
    
    EnterConfigMode(switch3)
    for i in range(total_apnum):
        SetCmd(switch3,'interface',ap_s3port_list[i])
        SetCmd(switch3,'switchport mode trunk')
        SetCmd(switch3,'switchport trunk native vlan '+Vlan1)

#----------------------- PC1，STA1，STA2 配置实验网路由,保持控制连接-------------------------------
# 配置PC1默认网关
SetCmd(pc1,'route add -net default gw',If_vlan192_s3_ipv4)
#----------------------- 初始化STA1，STA2，开启wpa_supplicant-------------------------------
SetCmd(sta1,'ifconfig ' + Netcard_sta1 + ' up')
SetCmd(sta1,'rm -rf /tmp/capture/*.cap')
SetCmd(sta1,'rm -rf /tmp/wpa_log/*.log')
SetCmd(sta1,'rm -rf /root/nohup.out')
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

SetCmd(sta2,'ifconfig ' + Netcard_sta2 + ' up')
SetCmd(sta2,'rm -rf /tmp/capture/*.cap')
SetCmd(sta2,'rm -rf /tmp/wpa_log/*.log')
SetCmd(sta2,'rm -rf /root/nohup.out')
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
SetCmd(switch1,'show run')

EnterEnableMode(switch3)
SetCmd(switch3,'clock set 09:00:00 2012.12.21')
IdleAfter('1')   
EnterEnableMode(switch3)
data = SetCmd(switch3,'write',timeout=1)
SetCmd(switch3,'y',timeout=2)
SetCmd(switch3,'show run')
#检测AC1是否成功管理AP1
EnterEnableMode(switch1)
# CheckSutCmd(switch1,'show wireless ap status', \
            # check=[(ap1mac,'Managed','Success')], \
            # waittime=5,retry=20,interval=5,IC=True)
# WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
profile_list = []
for i in range(total_apnum):
    CheckSutCmd(switch1,'show wireless ap status | include ' + ap_mac_list[i], \
                check=[(ap_mac_list[i],'Managed','Success')], \
                waittime=2,retry=5,interval=5,IC=True)
    profile_list.append(str(i+1))
WirelessApplyProfileWithCheck(switch1,profile_list,ap_mac_list)
    
data6 = SetCmd(switch1,'show wireless')
if re.search('CN - China',data6) is None:
    wx.MessageBox('AP not set to country code CN - China')


printInitialTimer('TestCase Initial','End')