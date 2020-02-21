#-*- coding: UTF-8 -*-#
#*******************************************************************************
# apwds_initial.py
#
# Author:  zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2008 Digital China Networks Co. Ltd
#
# Features: apwds模块初始化配置
#
#*******************************************************************************
# Change log:
#     - 2018.1.12 created by zhangjxp
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
    SetDefault(switch3)
    Receiver(switch1,'write',timeout=1)
    Receiver(switch3,'write',timeout=1)
    IdleAfter(1)
    Receiver(switch1,'y',timeout=2)
    Receiver(switch3,'y',timeout=2)
    #使用多线程对各设备同时进行重启操作
    reloadallsut(AP=[ap1,ap2],SWITCH=[switch1,switch3]) 

SetTerminalLength(switch1)
SetWatchdogDisable(switch1)
SetExecTimeout(switch1)
SetTerminalLength(switch3)
SetWatchdogDisable(switch3)
SetExecTimeout(switch3)


printRes('Check the software version of s1...')
ShowVersion(switch1)

print('ap wds initialing ')
avoiderror('Initialial')
#交换机初始配置
#---------------------------  初始化 S3  ---------------------------------------
print('s3 initial')
# VLAN配置
EnterConfigMode(switch3)
SetCmd(switch3,'no interface vlan 1')
SetCmd(switch3,'vlan',Vlan10+';'+Vlan20+';'+Vlan4091 + '-' + Vlan4092)
#vlan10
EnterInterfaceMode(switch3,'vlan '+Vlan10)
IdleAfter(Vlan_Idle_time)
SetIpAddress(switch3,If_vlan10_s3_ipv4,'255.255.255.0')
#vlan20
EnterInterfaceMode(switch3,'vlan '+Vlan20)
IdleAfter(Vlan_Idle_time)
SetIpAddress(switch3,If_vlan20_s3_ipv4,'255.255.255.0')
#vlan4091
EnterInterfaceMode(switch3,'vlan '+Vlan4091)
IdleAfter(Vlan_Idle_time)
SetCmd(switch3,'ip address',If_vlan4091_s3_ipv4,'255.255.255.0')
#vlan4092
EnterInterfaceMode(switch3,'vlan '+Vlan4092)
IdleAfter(Vlan_Idle_time)
SetCmd(switch3,'ip address',If_vlan4092_s3_ipv4,'255.255.255.0')
# DHCP
EnterConfigMode(switch3)
SetCmd(switch3,'service dhcp')
SetCmd(switch3,'ip dhcp excluded-address',If_vlan20_s3_ipv4)
SetCmd(switch3,'ip dhcp excluded-address ' + If_vlan4091_s3_ipv4)
SetCmd(switch3,'ip dhcp excluded-address ' + If_vlan4092_s3_ipv4)
SetCmd(switch3,'ip dhcp conflict ping-detection enable')

EnterConfigMode(switch3)
SetCmd(switch3,'ip dhcp pool vlan'+Vlan20)
SetCmd(switch3,'network 20.1.1.0 255.255.255.0')
SetCmd(switch3,'default-router',If_vlan20_s3_ipv4)

EnterConfigMode(switch3)
SetCmd(switch3,'ip dhcp pool vlan'+Vlan4091)
SetCmd(switch3,'network',Dhcp_pool1+'0 255.255.255.0')
SetCmd(switch3,'default-router',If_vlan4091_s3_ipv4)

EnterConfigMode(switch3)
SetCmd(switch3,'ip dhcp pool vlan'+Vlan4092)
SetCmd(switch3,'network',Dhcp_pool2+'0 255.255.255.0')
SetCmd(switch3,'default-router',If_vlan4092_s3_ipv4)

# 端口配置
# s3p1
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p1)
SetCmd(switch3,'switchport mode access')
SetCmd(switch3,'switch access vlan',Vlan10)
# s3p3
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan20)
# s3p4
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p4)
SetCmd(switch3,'shutdown')

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
  
# 保存配置 
EnterEnableMode(switch3)
data = SetCmd(switch3,'write',timeout=1)
SetCmd(switch3,'y',timeout=2)

#---------------------------  初始化AP1  ---------------------------------------
SetCmd(ap1,'\n')
ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_down')
ApSetcmd(ap1,Ap1cmdtype,'set_ip_route',If_vlan20_s3_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ip',Ap1_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'saverunning')

#---------------------------  初始化AP2  ---------------------------------------
SetCmd(ap2,'\n')
ApSetcmd(ap2,Ap2cmdtype,'set_dhcp_down')
ApSetcmd(ap2,Ap2cmdtype,'set_ip_route',If_vlan20_s3_ipv4)
ApSetcmd(ap2,Ap2cmdtype,'set_static_ip',Ap2_ipv4)
ApSetcmd(ap2,Ap2cmdtype,'saverunning')


#---------------------------  初始化AC1  ---------------------------------------
# vlan、端口、三层接口配置
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan 1')
SetCmd(switch1,'vlan',Vlan10+';'+Vlan4091 + '-' + Vlan4092)
#vlan10
EnterInterfaceMode(switch1,'vlan '+Vlan10)
IdleAfter(Vlan_Idle_time)
SetIpAddress(switch1,If_vlan10_s1_ipv4,'255.255.255.0')
EnterConfigMode(switch1)
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'switchport mode access')
SetCmd(switch1,'switch access vlan',Vlan10)

#配置router rip
EnterConfigMode(switch1)
SetCmd(switch1,'router rip')
SetCmd(switch1,'network 0.0.0.0/0')

# 配置wireless
EnterWirelessMode(switch1)
SetCmd(switch1,'enable')
SetCmd(switch1,'no auto-ip-assign')
SetCmd(switch1,'static-ip',If_vlan10_s1_ipv4)
SetCmd(switch1,'keep-alive-interval 10000')
SetCmd(switch1,'keep-alive-max-count 3')
SetCmd(switch1,'country-code cn')
SetCmd(switch1,'channel enhance disable')
SetCmd(switch1,'client roam-timeout 1')
EnterWirelessMode(switch1)
# SetCmd(switch1,'l2tunnel vlan-list add',Vlan4091 + '-' + Vlan4092)
#配置Network1
EnterNetworkMode(switch1,1)
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan ' + Vlan4091)
#添加Network1
EnterNetworkMode(switch1,100)
#配置Ap-profile1
EnterApProMode(switch1,1)
SetCmd(switch1,'hwtype',hwtype1)
SetCmd(switch1,'radio '+radio1num)
SetCmd(switch1,'enable')
# SetCmd(switch1,'rf-scan other-channels interval 5')
# SetCmd(switch1,'rf-scan duration 50')
SetCmd(switch1,'vap 1')
SetCmd(switch1,'enable')
SetCmd(switch1,'vap 2')
SetCmd(switch1,'enable')
SetCmd(switch1,'exit')
SetCmd(switch1,'exit')
SetCmd(switch1,'radio '+radio2num)
SetCmd(switch1,'enable')
SetCmd(switch1,'vap 1')
SetCmd(switch1,'enable')
SetCmd(switch1,'end')
#配置Ap-profile2
EnterApProMode(switch1,2)
# SetCmd(switch1,'hwtype',hwtype2)
SetCmd(switch1,'radio '+radio1num)
SetCmd(switch1,'vap 2')
SetCmd(switch1,'enable')
SetCmd(switch1,'exit')
SetCmd(switch1,'exit')
SetCmd(switch1,'radio '+radio2num)
SetCmd(switch1,'vap 2')
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
SetCmd(switch1,'discovery ip-list',Ap1_ipv4)                      
SetCmd(switch1,'discovery ip-list',Ap2_ipv4)

# 保存配置
EnterEnableMode(switch1)
SetCmd(switch1,'write',timeout=1)
SetCmd(switch1,'y',timeout=2)    

#----------------------- PC1，STA1，STA2 配置实验网路由,保持控制连接-------------------------------
# 配置PC1默认网关
SetCmd(pc1,'cd /root')
SetCmd(pc1,'service dhcpd stop')
SetCmd(pc1,'route add -net default gw',If_vlan192_s3_ipv4)
#----------------------- 初始化STA1，STA2，开启wpa_supplicant-------------------------------
#初始化sta1
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


#----------------------- 检测AC1是否成功管理AP1-------------------------------
EnterEnableMode(switch1)
CheckSutCmd(switch1,'show wireless ap status', \
            check=[(ap1mac,'Managed','Success')], \
            waittime=5,retry=20,interval=5,IC=True)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])


printInitialTimer('TestCase Initial','End')
