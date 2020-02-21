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
#*******************************************************************************
import random
#AC1额外配置（性能测试专用）
# 配置radius
EnterConfigMode(switch1)
SetCmd(switch1,'ssh-server enable')
SetCmd(switch1,'radius source-ipv4 '+StaticIpv4_ac1)
SetCmd(switch1,'radius-server key 0 test')
SetCmd(switch1,'radius-server authentication host '+Radius_server)
SetCmd(switch1,'radius-server accounting host '+Radius_server)
SetCmd(switch1,'radius nas-ipv4 ' + StaticIpv4_ac1)
SetCmd(switch1,'aaa enable')
SetCmd(switch1,'aaa-accounting enable')
SetCmd(switch1,'aaa group server radius wlan')
SetCmd(switch1,'server '+Radius_server)
# 配置snmp
EnterConfigMode(switch1)
SetCmd(switch1,'snmp-server enable')
SetCmd(switch1,'snmp-server securityip '+pc1_ipv4)
SetCmd(switch1,'snmp-server host '+pc1_ipv4+' v2c public')
SetCmd(switch1,'snmp-server community rw 0 public')
SetCmd(switch1,'snmp-server enable traps')
SetCmd(switch1,'snmp-server enable traps wireless')
# 无线配置
EnterWirelessMode(switch1)
SetCmd(switch1,'no auto-ip-assign')
SetCmd(switch1,'ap authentication none')
SetCmd(switch1,'channel enhance enable')
# SetCmd(switch1,'no discovery method l2-multicast')
SetCmd(switch1,'no discovery vlan-list 1')
SetCmd(switch1,'ap client-qos')
SetCmd(switch1,'trapflags ap-failure')
SetCmd(switch1,'trapflags ap-state')
SetCmd(switch1,'syslogflags ap-failure')
SetCmd(switch1,'syslogflags ap-state')
SetCmd(switch1,'syslogflags client-failure')
SetCmd(switch1,'syslogflags client-state')
SetCmd(switch1,'syslogflags peer-ws')
SetCmd(switch1,'syslogflags ws-status')
ClearNetworkConfig(switch1,1)
EnterWirelessMode(switch1)
SetCmd(switch1,'network 1')
SetCmd(switch1,'hide-ssid')
EnterWirelessMode(switch1)
SetCmd(switch1,'network 100')
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan ' + Vlan4091)
SetCmd(switch1,'client-qos enable')
SetCmd(switch1,'client-qos bandwidth-limit down 1028')
SetCmd(switch1,'client-qos bandwidth-limit up 1024')
SetCmd(switch1,'security mode wpa-personal')
SetCmd(switch1,'wpa key 12345678')
SetCmd(switch1,'station-isolation')
EnterWirelessMode(switch1)
SetCmd(switch1,'network 101')
SetCmd(switch1,'radius accounting')
SetCmd(switch1,'radius-accounting update interval 60')
SetCmd(switch1,'radius server-name auth wlan')
SetCmd(switch1,'radius server-name acct wlan')
SetCmd(switch1,'security mode wpa-enterprise')
SetCmd(switch1,'ssid ' + Network_name2)
SetCmd(switch1,'vlan ' + Vlan4092)
SetCmd(switch1,'station-isolation')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap air-match template 1')
SetCmd(switch1,'air-match ap-deny-client')
SetCmd(switch1,'air-match load-balance session')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap load-balance template 1')
SetCmd(switch1,'load-balance session window 30 threshold 8')
SetCmd(switch1,'load-balance denial 5')

for i in range(total_apnum):
    EnterApProMode(switch1,i+1)
    SetCmd(switch1,'ap escape')
    SetCmd(switch1,'ap escape client-persist')
    SetCmd(switch1,'air-match template 1')
    SetCmd(switch1,'load-balance template 1')
    SetCmd(switch1,'station-isolation allowed vlan '+Vlan4091)
    if test5gflag == True:
        SetCmd(switch1,'band-select enable')
    SetCmd(switch1,'lan port vlan '+Vlan4091)
    SetCmd(switch1,'redundancy mode preempt')
    SetCmd(switch1,'radio '+radio1num)
    SetCmd(switch1,'no power auto')
    SetCmd(switch1,'power default 80')
    SetCmd(switch1,'no channel auto')
    SetCmd(switch1,'schedule-mode fair')
    SetCmd(switch1,'dot11n channel-bandwidth 20')
    SetCmd(switch1,'vap 0')
    SetCmd(switch1,'network 100')
    SetCmd(switch1,'vap 1')
    SetCmd(switch1,'network 101')
    SetCmd(switch1,'exit')
    SetCmd(switch1,'exit')
    SetCmd(switch1,'radio '+radio2num)
    SetCmd(switch1,'no channel auto')
    SetCmd(switch1,'schedule-mode fair')
    SetCmd(switch1,'dot11n channel-bandwidth 40')
    SetCmd(switch1,'vap 0')
    SetCmd(switch1,'network 100')
    SetCmd(switch1,'vap 1')
    SetCmd(switch1,'network 101')
    EnterWirelessMode(switch1)
    SetCmd(switch1,'ap database '+ap_mac_list[i])
    SetCmd(switch1,'profile',i+1)
    SetCmd(switch1,'location '+'DCNtest'+str(i))
    SetCmd(switch1,'radio '+radio1num+' channel '+random.choice(['1','6','11']))
    SetCmd(switch1,'radio '+radio2num+' channel '+random.choice(['149','153','157']))
EnterEnableMode(switch1)
data = SetCmd(switch1,'write',timeout=1)
SetCmd(switch1,'y',timeout=2)
SetCmd(switch1,'show run')

for i in range(total_apnum):
    SetCmd(switch1,'wireless ap reset '+ap_mac_list[i],timeout=1)
    SetCmd(switch1,'y')
IdleAfter(50)
for i in range(total_apnum):
    # try:
        # ApLogin(ap_name_list[i],retry=20)
    # except Exception,e:
        # pass
    CheckSutCmd(switch1,'show wireless ap status | include ' + ap_mac_list[i], \
                check=[(ap_mac_list[i],'Managed','Success')], \
                waittime=2,retry=40,interval=5,IC=True)
    