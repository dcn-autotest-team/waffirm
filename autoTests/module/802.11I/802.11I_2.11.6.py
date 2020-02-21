#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# 802.11I_2.11.6.py
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2020 Digital China Networks Co. Ltd
#
# Features:
# 2.11.6 WPA2-802.1x-CCMP：wep方式关联失败
# 测试描述：WPA2-802.1x-CCMP：client使用wep方式时（密码一致），关联失败
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.2.8
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 802.11I_2.11.6'
avoiderror(testname)
printTimer(testname,'Start','client can not connect to ap with wpa2-enterprise CCMP mode when using wep shared auth method')

################################################################################
#Step 1
#操作
#配置AC1的network1的安全接入方式为WPA-Enterprise，WPA version为WPA2，认证服务器使用wlan：
#Wireless
#Network 1
#security mode wpa-enterprise
#wpa versions wpa2
#wpa ciphers CCMP
#radius server-name acct wlan
#radius server-name auth wlan
#
#配置成功。在AC1上面show wireless network 1可以看到相关的配置。
################################################################################
printStep(testname,'Step 1',\
          'set security mde of network 1 wpa-enterprise,',\
          'set wpa versions wpa2,',\
          'set radius server-name acct wlan,',\
          'set radius setver-name auth wlan,',\
          'and u should config others and so on,',\
          'check config success.')
#operate
#配置network模式下的radius配置参数
EnterNetworkMode(switch1,1)
SetCmd(switch1,'security mode wpa-enterprise')
SetCmd(switch1,'wpa ciphers CCMP')
SetCmd(switch1,'wpa versions wpa2')
SetCmd(switch1,'radius server-name auth wlan')
SetCmd(switch1,'radius server-name acct wlan')
SetCmd(switch1,'radius accounting')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#check
data1 = SetCmd(switch1,'show wireless network 1')
res1 = CheckLine(data1,'Security Mode','WPA Enterprise')
res2 = CheckLine(data1,'RADIUS Authentication Server Name','wlan')
res3 = CheckLine(data1,'RADIUS Accounting Server Name','wlan')
res4 = CheckLine(data1,'WPA Versions','WPA\s')
res5 = CheckLine(data1,'WPA Versions','WPA2')
res6 = CheckLine(data1,'WPA Ciphers','CCMP')
#result
printCheckStep(testname, 'Step 1',res1,res2,res3,not res4,res5,res6)

################################################################################
#Step 2
#操作
#设置STA1为WEP shared-key方式认证
#
#预期
#客户端关联失败
################################################################################
printStep(testname,'Step 2',\
          'STA1 connect to network 1 using shared-key authentication method',\
          'connect failed')
res1=1
# operate
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='custom',
                                dhcpFlag=False,reconnectflag=0,
                                key_mgmt='NONE',wep_key0='admin@123',auth_alg='SHARED',
                                wep_tx_keyidx='0',bssid=ap1mac_type1)

printCheckStep(testname, 'Step 2',not res1)

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