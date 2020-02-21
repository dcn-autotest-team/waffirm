#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# 802.11I_2.5.2.py
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2020 Digital China Networks Co. Ltd
#
# Features:
# 2.5.2 WPA-PSK-CCMP：wpa-psk方式，错误密码关联失败
# 测试描述： WPA-PSK-CCMP：client使用wpa-psk方式，使用错误的密码时，关联失败
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.2.7
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 802.11I_2.5.2'
avoiderror(testname)
printTimer(testname,'Start','client can not connect to ap with wpa-personal CCMP mode when using wrong key')

################################################################################
#Step 1
#操作
#配置AC1的network1的安全接入方式为WPA-Personal，密码为abcd1234。
#Wireless
#Network 1
#Security mode wpa-personal
#Wpa key abcd1234
#Wpa versions wpa
#wpa ciphers CCMP
#Exit
#配置成功。在AC1上面Show wireless network 1可以看到相关的配置。
################################################################################
printStep(testname,'Step 1',\
          'set network security mode wep-personal mode,',\
          'set wpa versions wpa.',\
          'show wireless network 1 and config success.')
#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'security mode wpa-personal')
SetCmd(switch1,'wpa key abcd1234')
SetCmd(switch1,'wpa versions wpa')
SetCmd(switch1,'wpa ciphers CCMP')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#check
data1 = SetCmd(switch1,'show wireless network 1')
res1 = CheckLine(data1,'Security Mode','WPA Personal')
res2 = CheckLine(data1,'WPA Versions','WPA')
res3 = CheckLine(data1,'WPA Versions','WPA2')
res4 = CheckLine(data1,'WPA Ciphers','CCMP')

printCheckStep(testname, 'Step 1',res1,res2,not res3,res4)

################################################################################
#Step 2
#操作
#设置STA1无线网卡的属性为WPA-PSK CCMP认证，输入错误的密码，关联网络test1。
#预期
#关联失败
################################################################################
printStep(testname,'Step 2',\
          'STA1 connect to network 1 using wrong key',\
          'connect failed')

res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='custom',
                                dhcpFlag=False,reconnectflag=0,key_mgmt='WPA-PSK',
                                proto='WPA', pairwise='CCMP',group='CCMP', psk='abcd1233',
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