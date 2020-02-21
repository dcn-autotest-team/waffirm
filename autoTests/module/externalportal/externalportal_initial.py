#-*- coding: UTF-8 -*-#
#*******************************************************************************
# testcase.py
#
# Author:  zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2008 Digital China Networks Co. Ltd
#
# Features: 存放模块的测试例
#
#*******************************************************************************
# Change log:
#     - 2017.12.7 created by zhangjxp
#*******************************************************************************
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

print(' external portal initialing ')
avoiderror('Initialial')
#交换机初始配置

#---------------------------  初始化AC1  ---------------------------------------
# vlan、端口、三层接口配置
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan 1')
SetCmd(switch1,'vlan',Vlan40)
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport access vlan',Vlan40)
EnterInterfaceMode(switch1,'vlan '+Vlan40)
IdleAfter(Vlan_Idle_time)
SetCmd(switch1,'ip address',If_vlan40_s1_ipv4,'255.255.255.0')
SetCmd(switch1,'ipv6 address',If_vlan40_s1_ipv6+'/64')
EnterInterfaceMode(switch1,'loopback 1')
SetCmd(switch1,'ip address',StaticIpv4_ac1,'255.255.255.255')
SetCmd(switch1,'ipv6 address',StaticIpv6_ac1+'/128')
# 路由配置
EnterConfigMode(switch1)
SetCmd(switch1,'router rip')
SetCmd(switch1,'network 0.0.0.0/0')
#配置wireless视图下的参数
EnterWirelessMode(switch1)
SetCmd(switch1,'enable')
SetCmd(switch1,'static-ip',StaticIpv4_ac1)
SetCmd(switch1,'static-ipv6',StaticIpv6_ac1)
SetCmd(switch1,'no auto-ip-assign')
SetCmd(switch1,'keep-alive-interval 10000')
SetCmd(switch1,'keep-alive-max-count 3')
SetCmd(switch1,'country-code cn')
SetCmd(switch1,'channel enhance disable')
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
SetCmd(switch1,'end')
#配置Ap-profile2
EnterApProMode(switch1,2)
SetCmd(switch1,'hwtype',hwtype2)
SetCmd(switch1,'radio '+radio1num)
SetCmd(switch1,'vap 1')
SetCmd(switch1,'enable')
SetCmd(switch1,'exit')
SetCmd(switch1,'exit')
SetCmd(switch1,'radio '+radio2num)
SetCmd(switch1,'mode ac')
SetCmd(switch1,'vap 1')
SetCmd(switch1,'enable')
SetCmd(switch1,'end')
# 配置ap database
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
SetCmd(switch1,'discovery ipv6-list',Ap1_ipv6)
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',Ap2_ipv4)
SetCmd(switch1,'discovery ipv6-list',Ap2_ipv6)
# 配置Radius
EnterConfigMode(switch1)
SetCmd(switch1,'radius source-ipv4 ' + StaticIpv4_ac1)
SetCmd(switch1,'radius-server key test')
SetCmd(switch1,'radius-server authentication host ' + Radius_server)
SetCmd(switch1,'radius-server accounting host ' + Radius_server)
SetCmd(switch1,'aaa enable')
SetCmd(switch1,'aaa-accounting enable')
SetCmd(switch1,'radius nas-ipv4 ' + StaticIpv4_ac1)
SetCmd(switch1,'aaa group server radius wlan')
SetCmd(switch1,'server ' + Radius_server)
# Portal配置
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'enable')
SetCmd(switch1,'authentication-type external')
SetCmd(switch1,'external portal-server server-name eportal ipv4 ' + Radius_server)
SetCmd(switch1,'free-resource 1 destination ipv4 ' + Radius_server +'/32 source any')
SetCmd(switch1,'configuration 1 ')
SetCmd(switch1,'enable')
SetCmd(switch1,'radius accounting ')
SetCmd(switch1,'protocol http')
SetCmd(switch1,'radius-acct-server wlan')
SetCmd(switch1,'radius-auth-server wlan')
SetCmd(switch1,'redirect attribute url-after-login enable')
SetCmd(switch1,'redirect attribute ssid enable')
SetCmd(switch1,'redirect attribute nas-ip enable')
SetCmd(switch1,'redirect attribute apmac enable')
SetCmd(switch1,'redirect attribute usermac enable')
SetCmd(switch1,'ac-name 0100.0010.0'+EnvNo+'0.01')
SetCmd(switch1,'redirect url-head http://192.168.10.101/a79.htm')
SetCmd(switch1,'portal-server ipv4 eportal')
SetCmd(switch1,'free-resource 1')
SetCmd(switch1,'interface ws-network 1')

# 集中转发、本地转发差异化配置，如测试集中转发，AC1需进行如下配置
if testcentral == True:
    print('s1 initial centralizedforwarding')
    EnterConfigMode(switch1)
    SetCmd(switch1,'vlan',Vlan4091 + '-' + Vlan4093)
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
    # 配置wireless模式，开启集中转发
    EnterWirelessMode(switch1)
    SetCmd(switch1,'l2tunnel vlan-list add',Vlan4091 + '-' + Vlan4093)

# 保存配置
EnterEnableMode(switch1)
SetCmd(switch1,'write',timeout=1)
SetCmd(switch1,'y',timeout=2)    

#---------------------------  初始化AC2  ---------------------------------------
# vlan、端口、三层接口配置
EnterConfigMode(switch2)
SetCmd(switch2,'no interface vlan 1')
SetCmd(switch2,'vlan',Vlan30)
EnterInterfaceMode(switch2,s2p1)
SetCmd(switch2,'switchport access vlan',Vlan30)
EnterInterfaceMode(switch2,'vlan '+Vlan30)
IdleAfter(Vlan_Idle_time)
SetCmd(switch2,'ip address',If_vlan30_s2_ipv4,'255.255.255.0')
SetCmd(switch2,'ipv6 address',If_vlan30_s2_ipv6+'/64')
EnterInterfaceMode(switch2,'loopback 1')
SetCmd(switch2,'ip address',StaticIpv4_ac2,'255.255.255.255')
SetCmd(switch2,'ipv6 address',StaticIpv6_ac2+'/128')
# 路由配置
EnterConfigMode(switch2)
SetCmd(switch2,'router rip')
SetCmd(switch2,'network 0.0.0.0/0')
#配置wireless视图下的参数
EnterWirelessMode(switch2)
SetCmd(switch2,'enable')
SetCmd(switch2,'static-ip',StaticIpv4_ac2)
SetCmd(switch2,'static-ipv6',StaticIpv6_ac2)
SetCmd(switch2,'no auto-ip-assign')
SetCmd(switch2,'country-code cn')
SetCmd(switch2,'keep-alive-interval 10000')
SetCmd(switch2,'keep-alive-max-count 3')
SetCmd(switch2,'channel enhance disable')
SetCmd(switch2,'no discovery vlan-list',1)

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
SetCmd(switch2,'radio '+radio1num)
SetCmd(switch2,'rf-scan other-channels interval 5')
SetCmd(switch2,'rf-scan duration 50')
SetCmd(switch2,'vap 1')
SetCmd(switch2,'enable')
SetCmd(switch2,'exit')
SetCmd(switch2,'exit')
SetCmd(switch2,'radio '+radio2num)
SetCmd(switch2,'mode ac')
SetCmd(switch2,'vap 1')
SetCmd(switch2,'enable')
SetCmd(switch2,'end')
#配置Ap-profile2
EnterApProMode(switch2,2)
SetCmd(switch2,'hwtype',hwtype2)
SetCmd(switch2,'radio '+radio1num)
SetCmd(switch2,'vap 1')
SetCmd(switch2,'enable')
SetCmd(switch2,'exit')
SetCmd(switch2,'exit')
SetCmd(switch2,'radio '+radio2num)
SetCmd(switch2,'mode ac')
SetCmd(switch2,'vap 1')
SetCmd(switch2,'enable')
SetCmd(switch2,'end')
# ap database配置
EnterConfigMode(switch2)
EnterWirelessMode(switch2)
SetCmd(switch2,'ap database',ap1mac)
SetCmd(switch2,'profile 1')
EnterWirelessMode(switch2)
SetCmd(switch2,'ap database',ap2mac)
SetCmd(switch2,'profile 2')

# 配置Radius
EnterConfigMode(switch2)
SetCmd(switch2,'radius source-ipv4 ' + StaticIpv4_ac2)
SetCmd(switch2,'radius-server key test')
SetCmd(switch2,'radius-server authentication host ' + Radius_server)
SetCmd(switch2,'radius-server accounting host ' + Radius_server)
SetCmd(switch2,'aaa enable')
SetCmd(switch2,'aaa-accounting enable')
SetCmd(switch2,'radius nas-ipv4 ' + StaticIpv4_ac2)
SetCmd(switch2,'aaa group server radius wlan')
SetCmd(switch2,'server ' + Radius_server)
# Portal配置
EnterConfigMode(switch2)
SetCmd(switch2,'captive-portal')
SetCmd(switch2,'enable')
SetCmd(switch2,'authentication-type external')
SetCmd(switch2,'external portal-server server-name eportal ipv4 ' + Radius_server)
SetCmd(switch2,'free-resource 1 destination ipv4 ' + Radius_server +'/32 source any')
SetCmd(switch2,'configuration 1 ')
SetCmd(switch2,'enable')
SetCmd(switch2,'radius accounting ')
SetCmd(switch2,'protocol http')
SetCmd(switch2,'radius-acct-server wlan')
SetCmd(switch2,'radius-auth-server wlan')
SetCmd(switch2,'redirect attribute url-after-login enable')
SetCmd(switch2,'redirect attribute ssid enable')
SetCmd(switch2,'redirect attribute nas-ip enable')
SetCmd(switch2,'redirect attribute apmac enable')
SetCmd(switch2,'redirect attribute usermac enable')
SetCmd(switch2,'ac-name 0100.0010.0'+EnvNo+'0.02')
SetCmd(switch2,'redirect url-head http://192.168.10.101/a79.htm')
SetCmd(switch2,'portal-server ipv4 eportal')
SetCmd(switch2,'free-resource 1')
SetCmd(switch2,'interface ws-network 1')

# 集中转发、本地转发差异化配置，如测试集中转发，AC2需进行如下配置
if testcentral == True:
    print('s2 initial centralizedforwarding')
    EnterConfigMode(switch2)
    SetCmd(switch2,'vlan',Vlan4091 + '-' + Vlan4093)
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
    EnterWirelessMode(switch2)
    SetCmd(switch2,'l2tunnel vlan-list add',Vlan4091 + '-' + Vlan4093)
    
# 保存配置
EnterEnableMode(switch2)
data = SetCmd(switch2,'write',timeout=1)
SetCmd(switch2,'y',timeout=2)
#---------------------------  初始化AP1  ---------------------------------------
SetCmd(ap1,'\n')
ApSetcmd(ap1,Ap1cmdtype,'set_static_ip',Ap1_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6',Ap1_ipv6)
ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_down')
ApSetcmd(ap1,Ap1cmdtype,'set_dhcpv6_down')
ApSetcmd(ap1,Ap1cmdtype,'set_ip_route',If_vlan20_s3_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'set_ipv6_route',If_vlan20_s3_ipv6)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6_prefix_len','64')
ApSetcmd(ap1,Ap1cmdtype,'saverunning')
#---------------------------  初始化AP2  ---------------------------------------
SetCmd(ap2,'\n')
ApSetcmd(ap2,Ap2cmdtype,'set_static_ip',Ap2_ipv4)
ApSetcmd(ap2,Ap2cmdtype,'set_static_ipv6',Ap2_ipv6)
ApSetcmd(ap2,Ap2cmdtype,'set_dhcp_down')
ApSetcmd(ap2,Ap2cmdtype,'set_dhcpv6_down')
ApSetcmd(ap2,Ap2cmdtype,'set_ip_route',If_vlan30_s3_ipv4)
ApSetcmd(ap2,Ap2cmdtype,'set_ipv6_route',If_vlan30_s3_ipv6)
ApSetcmd(ap2,Ap2cmdtype,'set_static_ipv6_prefix_len','64')
ApSetcmd(ap2,Ap2cmdtype,'saverunning')
#---------------------------  初始化 S3  ---------------------------------------
#vlan20
EnterConfigMode(switch3)
SetCmd(switch3,'vlan',Vlan20)
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

#router rip
EnterConfigMode(switch3)
SetCmd(switch3,'router rip')
SetCmd(switch3,'network 0.0.0.0/0')
# powerinline
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'power inline monitor off')
SetCmd(switch3,'interface',s3p4)
SetCmd(switch3,'power inline monitor off')
# 集中转发、本地转发差异化配置,如测试本地转发，S3需进行如下配置
if testcentral == False:
    print('s3 initial localforwarding')
    EnterConfigMode(switch3)
    SetCmd(switch3,'no interface vlan 1')
    SetCmd(switch3,'vlan',Vlan4091 + '-' + Vlan4093)
    EnterInterfaceMode(switch3,'vlan '+Vlan4091)
    IdleAfter(Vlan_Idle_time)
    SetCmd(switch3,'ip address',If_vlan4091_s1_ipv4,'255.255.255.0')
    SetCmd(switch3,'ipv6 address',If_vlan4091_s1_ipv6+'/64')
    EnterInterfaceMode(switch3,'vlan '+Vlan4092)
    IdleAfter(Vlan_Idle_time)
    SetCmd(switch3,'ip address',If_vlan4092_s1_ipv4,'255.255.255.0')
    SetCmd(switch3,'ipv6 address',If_vlan4092_s1_ipv6+'/64')
    EnterInterfaceMode(switch3,'vlan '+Vlan4093)
    IdleAfter(Vlan_Idle_time)
    SetCmd(switch3,'ip address',If_vlan4093_s1_ipv4,'255.255.255.0')
    SetCmd(switch3,'ipv6 address',If_vlan4093_s1_ipv6+'/64')
    SetCmd(switch3,'exit')
    #开启DHCP
    EnterConfigMode(switch3)
    SetCmd(switch3,'service dhcp')
    SetCmd(switch3,'ip dhcp excluded-address ' + If_vlan4091_s1_ipv4)
    SetCmd(switch3,'ip dhcp excluded-address ' + If_vlan4092_s1_ipv4)
    SetCmd(switch3,'ip dhcp excluded-address ' + If_vlan4093_s1_ipv4)
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

    EnterConfigMode(switch3)
    SetCmd(switch3,'interface',s3p3)
    SetCmd(switch3,'switchport mode trunk')
    SetCmd(switch3,'switchport trunk native vlan',Vlan20)
    SetCmd(switch3,'interface',s3p4)
    SetCmd(switch3,'switchport mode trunk')
    SetCmd(switch3,'switchport trunk native vlan',Vlan30)
    
# 保存配置 
EnterEnableMode(switch3)
data = SetCmd(switch3,'write',timeout=1)
SetCmd(switch3,'y',timeout=2)

#----------------------- PC1，STA1，STA2 配置实验网路由,保持控制连接-------------------------------
# 配置PC1默认网关
SetCmd(pc1,'cd /root')
SetCmd(pc1,'service dhcpd stop')
SetCmd(pc1,'route add -net default gw',If_vlan192_s3_ipv4)
#----------------------- 初始化STA1，STA2，开启wpa_supplicant-------------------------------
#初始化sta1
SetCmd(sta1,'cd /root')
SetCmd(sta1,'service dhcpd stop')
SetCmd(sta1,'rm -rf /tmp/capture/*.cap')
SetCmd(sta1,'rm -rf /tmp/wpa_log/*.log')
SetCmd(sta1,'rm -rf /root/nohup.out')
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

#初始化sta2
SetCmd(sta2,'cd /root')
SetCmd(sta2,'service dhcpd stop')
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


#检测AC1是否成功管理AP1和AP2
EnterEnableMode(switch1)
CheckSutCmd(switch1,'show wireless ap status',
            check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
            waittime=5,retry=20,interval=5,IC=True)
WirelessApplyProfileWithCheck(switch1,['1','2'],[ap1mac,ap2mac])

data6 = SetCmd(switch1,'show wireless')
if re.search('CN - China',data6) is None:
    wx.MessageBox('AP not set to country code CN - China')

printInitialTimer('TestCase Initial','End')
