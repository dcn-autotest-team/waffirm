#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# 802.11I_2.3.20.py
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2020 Digital China Networks Co. Ltd
#
# Features:
# 2.3.20  WEP加密的Share Key：wpa-802.1x认证关联失败
# 测试描述： AP设置为WEP认证模式时，client使用wpa-802.1x认证，关联失败
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.2.6
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 802.11I_2.3.20'
avoiderror(testname)
printTimer(testname,'Start','client can not connect to ap with wep shared-key mode when using wpa-enterprise auth method')

################################################################################
#Step 1
#操作
#配置wep Share Key加密模式的vap，后配置下发
#AC1(config-wireless)#network 1
#AC1(config-network)#security mode static-wep 
#AC1(config-network)#wep authentication shared-key
#AC1(config-network)#wep key type ascii 
#AC1(config-network)#wep key length 64
#AC1(config-network)#wep key 0 1111a
#AC1(config-network)#wep key 1 2222b
#AC1(config-network)#wep key 2 3333c
#AC1(config-network)#wep key 3 4444d
#AC1(config-network)#wep tx-key 4
################################################################################
printStep(testname,'Step 1',\
          'set network1 access mode WEP shared-key,',\
          'config wep tx-key 4',\
          'check config success',\
          'Apply ap profile 1')
res1=res2=res3=res4=res5=1         
#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'security mode static-wep')
SetCmd(switch1,'wep authentication shared-key')
SetCmd(switch1,'wep key type ascii')
SetCmd(switch1,'wep key length 64')
SetCmd(switch1,'wep key 1',web_key1_ascii)
SetCmd(switch1,'wep key 2',web_key2_ascii)
SetCmd(switch1,'wep key 3',web_key3_ascii)
SetCmd(switch1,'wep key 4',web_key4_ascii)
SetCmd(switch1,'wep tx-key 4')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#check
data = SetCmd(switch1,'show wireless network 1')
res1 = CheckLine(data,'Security Mode','Static WEP')
res2 = CheckLine(data,'WEP Authentication Type','Shared Key')
res3 = CheckLine(data,'WEP Key Type','ASCII')
res4 = CheckLine(data,'WEP Key Length','64')
res5 = CheckLine(data,'WEP Transfer Key Index','\s4\s')

printCheckStep(testname, 'Step 1',res1,res2,res3,res4,res5)

################################################################################
#Step 2
#操作
#设置STA1为wpa-enterprise方式认证
#
#预期
#客户端关联失败
################################################################################
printStep(testname,'Step 2',\
          'STA1 connect to network 1 using wpa-enterprise authentication method',\
          'connect failed')
res1=1
# operate
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='custom',
                                dhcpFlag=False,reconnectflag=0,
                                key_mgmt='WPA-EAP',proto='WPA',pairwise='TKIP',
                                group='TKIP',eap='PEAP',
                                identity=Dot1x_identity,password=Dot1x_password,
                                bssid=ap1mac_type1)


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