#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.3.8.py - test case 4.3.8 of waffirm
#
# Author:  qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.3.8 WPA/WPA2-Enterprise混合模式下客户端认证接入测试
# 测试目的：测试客户端通过WPA/WPA2-Enterprise混合模式接入无线网络。
# 测试环境：同测试拓扑
# 测试描述：测试客户端通过WPA2-Enterprise模式接入无线网络。
#          （STA1的MAC地址：STA1MAC）
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.3.8'
printTimer(testname,'Start','Test wpa/wpa2-enterprise mode with wireless client')

################################################################################
#Step 1
#操作
#配置AC1的network1的安全接入方式为WPA-Enterprise，WPA version为默认的混合模式，认证服务器使用wlan：
#wireless
#security mode wpa-enterprise
#wpa versions
#radius server-name acct wlan
#radius server-name auth wlan
#exit
#将配置下发到AP1。
#wireless ap profile apply 1
#设置STA1无线网卡的属性为WPA2-Enterprise认证，关联网络test1，使用Radius服务器上面配置好的用户名和密码。
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
EnterConfigMode(switch1)
SetCmd(switch1,'radius source-ipv4 ' + StaticIpv4_ac1)
SetCmd(switch1,'radius-server key test')
SetCmd(switch1,'radius-server authentication host ' + Radius_server)
SetCmd(switch1,'radius-server accounting host ' + Radius_server)
SetCmd(switch1,'radius nas-ipv4 ' + StaticIpv4_ac1)
SetCmd(switch1,'aaa group server radius wlan')
SetCmd(switch1,'server ' + Radius_server)
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
SetCmd(switch1,'wpa versions')

#check
data1 = ShowRun(switch1)
#printRes('data1='+ data1)
res1 = CheckLineList(data1,['radius source-ipv4 ' + StaticIpv4_ac1,'radius-server key 0 test','radius-server authentication host ' + Radius_server,\
                            'radius-server accounting host ' + Radius_server,'aaa-accounting enable','aaa enable','radius nas-ipv4 ' + StaticIpv4_ac1,\
                            'aaa group server radius wlan','server ' + Radius_server])
data2 = SetCmd(switch1,'show wireless network 1',timeout=3)
res2 = CheckLine(data2,'Security Mode','WPA Enterprise')
res3 = CheckLine(data2,'RADIUS Authentication Server Name','wlan')
res4 = CheckLine(data2,'RADIUS Accounting Server Name','wlan')
res5 = CheckLine(data2,'WPA Versions','WPA/WPA2')

#result
printCheckStep(testname, 'Step 1',res1,res2,res3,res4,res5)

################################################################################
#Step 2
#设置STA1无线网卡的属性为WPA2-Enterprise认证，关联网络test1，使用Radius服务器上面配置好的用户名和密码。
#成功关联，并获取192.168.91.X网段的IP地址。Show wireless client summery
#可以看到STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
################################################################################

printStep(testname,'Step 2',\
          'STA1 scanning network,',\
          'and connect to affirm_auto_test1 using encrypt wpa2')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')
# IdleAfter(Apply_profile_wait_time)
res1 = 1
for tmpCounter in xrange(0,10):
    StaScanSSID(sta1,Netcard_sta1)
    IdleAfter('5')
    data = SetCmd(sta1,'wpa_cli -i '+ Netcard_sta1 +' scan_results')
    if 0 == CheckLine(data,ap1mac_lower,'WPA-EAP.+?WPA2-EAP',Network_name1):
        res1 = 0
        break
if res1 != 0:
    SetCmd(ap1,'admin')
    SetCmd(ap1,'admin')
    SetCmd(ap1,'iwconfig')
for tmpCounter in xrange(0,10):
    StaScanSSID(sta1,Netcard_sta1)
    IdleAfter('5')
    data = SetCmd(sta1,'wpa_cli -i '+ Netcard_sta1 +' scan_results')
    if 0 == CheckLine(data,ap1mac_lower,'WPA-EAP.+?WPA2-EAP',Network_name1):
        res1 = 0
        break
if res1 != 0:
    SetCmd(ap1,'admin')
    SetCmd(ap1,'admin')
    SetCmd(ap1,'iwconfig')
for tmpCounter in xrange(0,10):
    StaScanSSID(sta1,Netcard_sta1)
    IdleAfter('5')
    data = SetCmd(sta1,'wpa_cli -i '+ Netcard_sta1 +' scan_results')
    if 0 == CheckLine(data,ap1mac_lower,'WPA-EAP.+?WPA2-EAP',Network_name1):
        res1 = 0
        break
if res1 != 0:
    SetCmd(ap1,'admin')
    SetCmd(ap1,'admin')
    SetCmd(ap1,'iwconfig')
    
##res1 = CheckLine(data,ap1mac_lower,'WPA-',Network_name1)
##res2 = CheckLine(data,ap1mac_lower,'WPA2',Network_name1)

res3 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='wpa2_eap',identity=Dot1x_identity,password=Dot1x_password,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
if res3 != 0:
    timestring = str(int(time.time()))
    capfile = '/home/capture/capture' + timestring + '.pcap'
    SetCmd(sta1,'tcpdump -i mon0 -w ' + capfile,timeout=1)
    IdleAfter(30)
    SetCmd(sta1,'\x03')
    print 'File save to ' + capfile 

res4 = CheckWirelessClientOnline(switch1,sta1mac,'online')

#result
printCheckStep(testname, 'Step 2',res3,res4)

################################################################################
#Step 3
#操作
#在STA1上ping PC1
#
#预期
#能够ping通。
################################################################################

printStep(testname,'Step 3',\
          'STA1 ping pc1',\
          'ping success.')

res1 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')

printCheckStep(testname, 'Step 3',res1)

################################################################################
#Step 4
#操作
#客户端STA1断开与test1的连接。
#
#预期
#客户端下线成功。Show wireless client summery不能看到sta1。
################################################################################

printStep(testname,'Step 4',\
          'STA1 disconnect with network1,',\
          'show wireless client summary and no STA1 client online.')

res1 = WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

res2 = CheckWirelessClientOnline(switch1,sta1mac,'offline')

printCheckStep(testname, 'Step 4',res1,res2)

################################################################################
#Step 5
#设置STA1无线网卡的属性为WPA-Enterprise认证，关联网络test1，使用Radius服务器上面配置好的用户名和密码。
#成功关联，并获取192.168.91.X网段的IP地址。Show wireless client summery
#可以看到STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
################################################################################

printStep(testname,'Step 5',\
          'STA1 scanning network,',\
          'and connect to affirm_auto_test1 using encrypt wpa')

for tmpCounter in xrange(0,10):
    StaScanSSID(sta1,Netcard_sta1)
    IdleAfter('5')
    data = SetCmd(sta1,'wpa_cli -i '+ Netcard_sta1 +' scan_results')
    if 0 == CheckLine(data,ap1mac_lower,'WPA-EAP.+?WPA2-EAP',Network_name1):
        break
    
res1 = CheckLine(data,ap1mac_lower,'WPA-',Network_name1)
res2 = CheckLine(data,ap1mac_lower,'WPA2',Network_name1)

res3 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='wpa_eap',identity=Dot1x_identity,password=Dot1x_password,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)

res4 = CheckWirelessClientOnline(switch1,sta1mac,'online')

#result
printCheckStep(testname, 'Step 5',res1,res2,res3,res4)

################################################################################
#Step 6
#操作
#在STA1上ping PC1
#
#预期
#能够ping通。
################################################################################

printStep(testname,'Step 6',\
          'STA1 ping pc1',\
          'ping success.')

res1 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')

printCheckStep(testname, 'Step 6',res1)

################################################################################
#Step 7
#操作
#客户端STA1断开与test1的连接。
#
#预期
#客户端下线成功。Show wireless client summery不能看到sta1。
################################################################################

printStep(testname,'Step 7',\
          'STA1 disconnect with network1,',\
          'show wireless client summary and no STA1 client online.')

res1 = WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

res2 = CheckWirelessClientOnline(switch1,sta1mac,'offline')

printCheckStep(testname, 'Step 7',res1,res2)

################################################################################
#Step 8
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 8',\
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
SetCmd(switch1,'no radius-server authentication host ' + Radius_server)
SetCmd(switch1,'no radius-server accounting host ' + Radius_server)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')
# IdleAfter(Apply_profile_wait_time)
#end
printTimer(testname, 'End')