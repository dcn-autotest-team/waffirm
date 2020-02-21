#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# 802.11I_2.2.9.py
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2020 Digital China Networks Co. Ltd
#
# Features:
# 2.2.9 开放式认证+WEP加密：成功关联发送client Authentication消息
# 测试描述：开放式认证+WEP加密：当client成功关联到AP时，UWS将会收到AP发送的client Authentication消息（debug查看）
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.2.2
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 802.11I_2.2.9'
avoiderror(testname)
printTimer(testname,'Start','check client authentication pakcet ap send to ac\n when client connect to ap with wep mode')

################################################################################
#Step 1
#操作
#配置wep open-system加密模式的vap，后配置下发
#AC1(config-wireless)#network 1
#AC1(config-network)#security mode static-wep 
#AC1(config-network)#wep authentication open-system
#AC1(config-network)#wep key type hex
#AC1(config-network)#wep key length 64
#AC1(config-network)#wep key 0 111111111a
#AC1(config-network)#wep key 1 222222222b
#AC1(config-network)#wep key 2 333333333c
#AC1(config-network)#wep key 3 444444444d
#AC1(config-network)#wep tx-key 1
################################################################################
printStep(testname,'Step 1',\
          'set network1 access mode WEP',\
          'check config success',\
          'Apply ap profile 1')
res1=res2=res3=res4=res5=1         
#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'security mode static-wep')
SetCmd(switch1,'wep authentication open-system')
SetCmd(switch1,'wep key type hex')
SetCmd(switch1,'wep key length 64')
SetCmd(switch1,'wep key 1',web_key1_hex)
SetCmd(switch1,'wep key 2',web_key2_hex)
SetCmd(switch1,'wep key 3',web_key3_hex)
SetCmd(switch1,'wep key 4',web_key4_hex)
SetCmd(switch1,'wep tx-key 1')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#check
data = SetCmd(switch1,'show wireless network 1')
res1 = CheckLine(data,'Security Mode','Static WEP')
res2 = CheckLine(data,'WEP Authentication Type','Open System')
res3 = CheckLine(data,'WEP Key Type','HEX')
res4 = CheckLine(data,'WEP Key Length','64')
res5 = CheckLine(data,'WEP Transfer Key Index','\s1\s')

printCheckStep(testname, 'Step 1',res1,res2,res3,res4,res5)

################################################################################
#Step 2
#操作
# AC开启 debug wireless client-auth packet dump ap1mac
#设置STA1为WEP认证，关联test1
#
#预期
#成功关联，并获取192.168.91.X网段的IP地址。Show wireless client summery
#可以看到STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
# AC上可以看到sta1认证成功的报文
################################################################################
printStep(testname,'Step 2',\
          'debug wireless client-auth packet receive ap1mac on AC1',\
          'STA1 connect to network 1,',\
          'connect success.'
          'client auth packet can be seen on AC1')
res1=res2=res3=1
# operate
EnterEnableMode(switch1)
SetCmd(switch1,'debug wireless client-auth packet dump',ap1vapmac)
StartDebug(switch1)
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='custom',
                                key_mgmt='NONE',wep_key0=web_key1_hex,wep_key_type='hex',wep_tx_keyidx='0',
                                checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
IdleAfter(10)
EnterEnableMode(switch1)
SetCmd(switch1,'no debug all')
data=StopDebug(switch1)
if CheckLine(data,'wireless_auth_client',IC=True) == 0:
    res2 = 0
if res1 == 0:
    res3 = CheckWirelessClientOnline(switch1,sta1mac,'online')

printCheckStep(testname, 'Step 2',res1,res2,res3)

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