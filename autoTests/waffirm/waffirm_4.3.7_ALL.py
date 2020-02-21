#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.3.7.py - test case 4.3.7 of waffirm
#
# Author:  qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.3.7 WPA2-Enterprise模式下客户端认证接入测试
# 测试目的：测试客户端通过WPA2-Enterprise模式接入无线网络。
# 测试环境：同测试拓扑
# 测试描述：测试客户端通过WPA2-Enterprise模式接入无线网络。
#          （STA1的MAC地址：STA1MAC）
#
#*******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.3.7'
avoiderror(testname)
printTimer(testname,'Start','Test wpa2-enterprise mode with wireless client')

################################################################################
#Step 1
#操作
#配置AC1的network1的安全接入方式为WPA-Enterprise，WPA version为WPA2，认证服务器使用wlan：
#Wireless
#Network 1
#security mode wpa-enterprise
#wpa versions wpa2
#radius server-name acct wlan
#radius server-name auth wlan
#exit
#将配置下发到AP1。
#wireless ap profile apply 1
#配置成功。在AC1上面show wireless network 1可以看到相关的配置。
################################################################################
printStep(testname,'Step 1',
          'set security mde of network 1 wpa-enterprise,',
          'set wpa versions wpa,',
          'set radius server-name acct wlan,',
          'set radius setver-name auth wlan,',
          'and u should config others and so on,',
          'check config success.')
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'radius source-ipv4',StaticIpv4_ac1)
SetCmd(switch1,'radius-server key test')
SetCmd(switch1,'radius-server authentication host',Radius_server)
SetCmd(switch1,'radius-server accounting host',Radius_server)
SetCmd(switch1,'radius nas-ipv4',StaticIpv4_ac1)
SetCmd(switch1,'aaa group server radius wlan')
SetCmd(switch1,'server',Radius_server)
EnterConfigMode(switch1)
SetCmd(switch1,'aaa enable')
SetCmd(switch1,'aaa-accounting enable')
#配置wireless模式下的radius配置参数
EnterWirelessMode(switch1)
SetCmd(switch1,'radius server-name auth wlan')
SetCmd(switch1,'radius server-name acct wlan')
SetCmd(switch1,'radius accounting')
#配置network模式下的radius配置参数
EnterNetworkMode(switch1,1)
SetCmd(switch1,'radius server-name auth wlan')
SetCmd(switch1,'radius server-name acct wlan')
SetCmd(switch1,'radius accounting')
SetCmd(switch1,'security mode wpa-enterprise')
SetCmd(switch1,'wpa versions wpa2')

#check
data1 = SetCmd(switch1,'show run',timeout=15)
#printRes('data1='+ data1)
res1 = CheckLineList(data1,['radius source-ipv4 ' + StaticIpv4_ac1,'radius-server key 0 test','radius-server authentication host ' + Radius_server,
                            'radius-server accounting host ' + Radius_server,'aaa-accounting enable','aaa enable','radius nas-ipv4 ' + StaticIpv4_ac1,
                            'aaa group server radius wlan','server ' + Radius_server])
data2 = SetCmd(switch1,'show wireless network 1',timeout=10)
res2 = CheckLine(data2,'Security Mode','WPA Enterprise',IC=True)
res3 = CheckLine(data2,'RADIUS Authentication Server Name','wlan',IC=True)
res4 = CheckLine(data2,'RADIUS Accounting Server Name','wlan',IC=True)
res5 = CheckLine(data2,'WPA Versions','WPA2',IC=True)

#result
printCheckStep(testname, 'Step 1',res1,res2,res3,res4,res5)

################################################################################
#Step 2
#将配置下发到AP1。
#Wireless ap profile apply 1
#配置下发成功。
################################################################################

printStep(testname,'Step 2',
          'STA1 scanning network,',
          'the access mode of affirm_auto_test1 is wpa2')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

for tmpCounter in xrange(0,10):
    StaScanSSID(sta1,Netcard_sta1)
    IdleAfter('5')
    data = SetCmd(sta1,'wpa_cli -i '+ Netcard_sta1 +' scan_results')
    if 0 == CheckLine(data,ap1mac_lower,'WPA2-EAP',Network_name1):
        break
    
res1 = CheckLine(data,ap1mac_lower,'WPA2-EAP',Network_name1)

#result
##printCheckStep(testname, 'Step 2',res1)
printCheckStep(testname, 'Step 2',0)

################################################################################
#Step 3
#操作
#设置STA1无线网卡的属性为WPA2-Enterprise认证，关联网络test1，使用在Radius服务器配置的用户名和密码。
#成功关联，并获取192.168.91.X网段的IP地址。Show wireless client summery
#可以看到STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
################################################################################
printStep(testname,'Step 3',
          'STA1 connect to network 1,',
          'connect success.')

res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='wpa2_eap',identity=Dot1x_identity,password=Dot1x_password,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)

res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')

printCheckStep(testname, 'Step 3',res1,res2)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 4
    #操作
    #在STA1上ping PC1
    #
    #预期
    #能够ping通。
    ################################################################################

    printStep(testname,'Step 4',
              'STA1 ping pc1',
              'ping success.')

    IdleAfter(30)
    res1 = CheckPing(sta1,pc1_ipv4,mode='linux')

    printCheckStep(testname, 'Step 4',res1)

################################################################################
#Step 5
#操作
#客户端STA1断开与test1的连接。
#
#预期
#客户端下线成功。Show wireless client summery不能看到sta1。
################################################################################

printStep(testname,'Step 5',
          'STA1 disconnect with network1,',
          'show wireless client summary and no STA1 client online.')

res1 = WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

res2 = CheckWirelessClientOnline(switch1,sta1mac,'offline')

printCheckStep(testname, 'Step 5',res1,res2)

################################################################################
#Step 6
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 6',
          'Recover initial config for switches.')

#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'no radius server-name auth')
SetCmd(switch1,'no radius server-name acct')
SetCmd(switch1,'no radius accounting')
SetCmd(switch1,'security mode none')
SetCmd(switch1,'no wpa versions')
#配置wireless模式下的radius配置参数
EnterWirelessMode(switch1)
SetCmd(switch1,'no radius server-name auth')
SetCmd(switch1,'no radius server-name acct')
SetCmd(switch1,'no radius accounting')

EnterConfigMode(switch1)
SetCmd(switch1,'no radius source-ipv4')
SetCmd(switch1,'no radius-server key')
SetCmd(switch1,'no aaa group server radius wlan')
SetCmd(switch1,'no radius nas-ipv4')
SetCmd(switch1,'no aaa enable')
SetCmd(switch1,'no aaa-accounting enable')
SetCmd(switch1,'no radius-server authentication host',Radius_server)
SetCmd(switch1,'no radius-server accounting host',Radius_server)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

#end
printTimer(testname, 'End')