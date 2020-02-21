#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# 802.11I_2.3.4.py
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2020 Digital China Networks Co. Ltd
#
# Features:
# 2.3.4 WEP加密的Share Key：密钥匹配
# 测试描述：设置wep的4个key分别为key1，key2，key3，key4，设置认证加密使用key1，
#           客户端设置4个key为key5，key2，key3，key4，不能关联上AP
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.2.5
#*******************************************************************************

#Package

#Global Definition
web_key5_hex='1111111111'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 802.11I_2.3.4'
avoiderror(testname)
printTimer(testname,'Start','Config four keys:key1,key2,key3,key4 in wep share key mode network1 on AC1\n \
                    Sta use four keys:key5,key2,key3,key4 to connect to network1 and connect failed')

################################################################################
#Step 1
#操作
#配置wep Share Key加密模式的vap，后配置下发
#AC1(config-wireless)#network 1
#AC1(config-network)#security mode static-wep 
#AC1(config-network)#wep authentication shared-key
#AC1(config-network)#wep key type hex
#AC1(config-network)#wep key length 64
#AC1(config-network)#wep key 0 111111111a
#AC1(config-network)#wep key 1 222222222b
#AC1(config-network)#wep key 2 333333333c
#AC1(config-network)#wep key 3 444444444d
#AC1(config-network)#wep tx-key 1
################################################################################
printStep(testname,'Step 1',\
          'set network1 access mode WEP shared-key,',\
          'check config success',\
          'Apply ap profile 1')
res1=res2=res3=res4=res5=1         
#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'security mode static-wep')
SetCmd(switch1,'wep authentication shared-key')
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
res2 = CheckLine(data,'WEP Authentication Type','Shared Key')
res3 = CheckLine(data,'WEP Key Type','HEX')
res4 = CheckLine(data,'WEP Key Length','64')
res5 = CheckLine(data,'WEP Transfer Key Index','\s1\s')

printCheckStep(testname, 'Step 1',res1,res2,res3,res4,res5)

################################################################################
#Step 2
#操作
#设设置STA1为WEP Share Key认证，设置4各密码分别为key5,key2,key3,key4，关联test1
#
#预期
#关联失败。
################################################################################
printStep(testname,'Step 2',\
          'STA1 config 4 keys:key5,key2,key3,key4 to connect to network 1,',\
          'connect failed.')
res1=1
# operate
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='custom',
                                dhcpFlag=False,reconnectflag=0,
                                key_mgmt='NONE',auth_alg='SHARED',wep_key_type='hex',
                                wep_key0=web_key5_hex,wep_key1=web_key2_hex,
                                wep_key2=web_key3_hex,wep_key3=web_key4_hex,wep_tx_keyidx='0',
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