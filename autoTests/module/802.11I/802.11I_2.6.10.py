#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# 802.11I_2.6.10.py
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2020 Digital China Networks Co. Ltd
#
# Features:
# 2.6.10 非漫游关联成功后的处理:关联成功后,给radius发送计费报文
# 测试描述：如果UWS开启了计费功能，则关联成功后会给radius发送计费报文开始计费
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.2.8
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 802.11I_2.6.10'
avoiderror(testname)
printTimer(testname,'Start','Test aaa acounting packet')

################################################################################
#Step 1
#操作
#配置AC1的network1的安全接入方式为WPA-Enterprise，WPA version为WPA，认证服务器使用wlan：
#Wireless
#Network 1
#security mode wpa-enterprise
#wpa versions wpa
#radius server-name acct wlan
#radius server-name auth wlan
#
#配置成功。在AC1上面show wireless network 1可以看到相关的配置。
################################################################################
printStep(testname,'Step 1',\
          'set security mde of network 1 wpa-enterprise,',\
          'set wpa versions wpa,',\
          'set radius server-name acct wlan,',\
          'set radius setver-name auth wlan,',\
          'and u should config others and so on,',\
          'check config success.')
#operate
#配置network模式下的radius配置参数
EnterNetworkMode(switch1,1)
SetCmd(switch1,'security mode wpa-enterprise')
SetCmd(switch1,'wpa ciphers TKIP')
SetCmd(switch1,'wpa versions wpa')
SetCmd(switch1,'radius server-name auth wlan')
SetCmd(switch1,'radius server-name acct wlan')
SetCmd(switch1,'radius accounting')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#check
data1 = SetCmd(switch1,'show wireless network 1',timeout=10)
res1 = CheckLine(data1,'Security Mode','WPA Enterprise')
res2 = CheckLine(data1,'RADIUS Authentication Server Name','wlan')
res3 = CheckLine(data1,'RADIUS Accounting Server Name','wlan')
res4 = CheckLine(data1,'WPA Versions','WPA2')
res5 = CheckLine(data1,'WPA Versions','WPA')
res4 = 0 if res4 != 0 else -1
#result
printCheckStep(testname, 'Step 1',res1,res2,res3,res4,res5)

################################################################################
#Step 2
#操作
#AC上开启debug wireless client-auth radius-info sta1mac
# STA1关联test1。
#预期
#成功关联，并获取192.168.91.X网段的IP地址。
# Show wireless client summery可以看到sta1，IP地址的网段正确。
# AC上有radius计费报文的debug打印
################################################################################
printStep(testname,'Step 2',\
          'debug wireless client-auth radius-info sta1mac on AC1',\
          'STA1 connect to test1',\
          'STA1 get a 192.168.91.X ipaddress',\
          'there is radius accounting packet on AC1')
res1=res2=1
# operate
EnterEnableMode(switch1)
SetCmd(switch1,'debug wireless client-auth radius-info',sta1mac)
StartDebug(switch1)
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='custom',
                                key_mgmt='WPA-EAP',proto='WPA',pairwise='TKIP',group='TKIP',
                                eap='PEAP',identity=Dot1x_identity,password=Dot1x_password,
                                checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res1 == 0:
    SetCmd(switch1,'\n',promotePatten='Entering wirelessClientRadiusAccountingStart',promoteTimeout=200)
data = StopDebug(switch1)
res2=CheckLine(data,'Entering wirelessClientRadiusAccountingStart',IC=True)
EnterEnableMode(switch1)
SetCmd(switch1,'no debug all')
printCheckStep(testname, 'Step 2',res1,res2)

################################################################################
#Step 3
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 3',\
          'Recover initial config for switches.')

#operate
# sta1解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
CheckWirelessClientOnline(switch1,sta1mac,'offline',retry=20)

# 恢复network1配置
ClearNetworkConfig(switch1,1)
EnterNetworkMode(switch1,1)
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan ' + Vlan4091)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

#end
printTimer(testname, 'End')