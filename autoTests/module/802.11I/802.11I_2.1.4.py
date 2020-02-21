#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# 802.11I_2.1.4.py
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2020 Digital China Networks Co. Ltd
#
# Features:
# 2.1.4 WPA-Enterprise模式下客户端认证接入测试
# 测试描述：无线系统采用WPA-ENTERPRISE方式时，client使用WPA-ENTERPRISE能够认证成功
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.2.1
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 802.11I_2.1.4'
avoiderror(testname)
printTimer(testname,'Start','Test wpa-enterprise mode with wireless client')

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
SetCmd(switch1,'wpa ciphers CCMP')
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
res6 = CheckLine(data1,'WPA Ciphers','CCMP')
#result
printCheckStep(testname, 'Step 1',res1,res2,res3,not res4,res5,res6)

################################################################################
#Step 2
#操作
#设置STA1无线网卡的属性为WPA-Enterprise认证，关联网络test1，使用在Radius服务器配置的用户名和密码。
#成功关联，并获取192.168.91.X网段的IP地址。Show wireless client summery
#可以看到STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
################################################################################
printStep(testname,'Step 2',\
          'STA1 connect to network 1,',\
          'connect success.')
res1=res2=1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='custom',
                                key_mgmt='WPA-EAP',proto='WPA',pairwise='CCMP',group='CCMP',
                                eap='PEAP',identity=Dot1x_identity,password=Dot1x_password,
                                checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res1 == 0:
    res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')

printCheckStep(testname, 'Step 2',res1,res2)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 3
    #操作
    #在STA1上ping Radius_server
    #
    #预期
    #能够ping通。
    ################################################################################

    printStep(testname,'Step 3',\
              'STA1 ping Radius_server',\
              'ping success.')

    res1 = CheckPing(sta1,Radius_server,mode='linux')

    printCheckStep(testname, 'Step 3',res1)

################################################################################
#Step 4
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 4',\
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