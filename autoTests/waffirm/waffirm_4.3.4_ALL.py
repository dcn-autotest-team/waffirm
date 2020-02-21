#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.3.4.py - test case 4.3.4 of waffirm
#
# Author:  qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.3.4 WPA2-Personal模式下客户端认证接入测试
# 测试目的：测试客户端通过WPA2-Personal模式接入无线网络。
# 测试环境：同测试拓扑
# 测试描述：测试客户端通过WPA2-Personal模式接入无线网络。Wpa version为WPA2。
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

testname = 'TestCase 4.3.4'
avoiderror(testname)
printTimer(testname,'Start','Test wpa2-personal mode with wireless client')

################################################################################
#Step 1
#操作
#配置AC的network1的安全接入方式为WPA2-Personal，密码为abcd1234。
#Wireless
#Network 1
#Security mode wpa-personal
#Wpa key abcd1234
#Wpa versions wpa2
#Exit
#配置成功。在AC1上面Show wireless network 1可以看到相关的配置。
################################################################################
printStep(testname,'Step 1',
          'set network security mode wep-personal mode,',
          'set wpa versions wpa2.',
          'show wireless network 1 and config success.')
#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'security mode wpa-personal')
SetCmd(switch1,'wpa key abcd1234')
SetCmd(switch1,'wpa versions wpa2')
#check
data1 = SetCmd(switch1,'show wireless network 1',timeout = 10)
res1 = CheckLine(data1,'Security Mode','WPA Personal')
#res2 = CheckLine(data1,'WPA Versions','WPA')
res3 = CheckLine(data1,'WPA Versions','WPA2')

printCheckStep(testname, 'Step 1',res1,res3)

################################################################################
#Step 2
#将配置下发到AP1。
#Wireless ap profile apply 1
#下发成功
################################################################################

printStep(testname,'Step 2',
          'STA1 scanning network,',
          'the access mode of affirm_auto_test1 is wpa2')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

for tmpCounter in xrange(0,10):
    StaScanSSID(sta1,Netcard_sta1)
    IdleAfter('5')
    data = SetCmd(sta1,'wpa_cli -i '+ Netcard_sta1 +' scan_results')
    if 0 == CheckLine(data,ap1mac_lower,'WPA2-PSK-TKIP',Network_name1):
        break
    
#res1 = CheckLine(data,ap1mac_lower,'WPA',Network_name1)
res2 = CheckLine(data,ap1mac_lower,'WPA2',Network_name1)
res3 = CheckLine(data,ap1mac_lower,'PSK',Network_name1)

#result
##printCheckStep(testname, 'Step 2',res2,res3)
printCheckStep(testname, 'Step 2',0)

################################################################################
#Step 3
#操作
#设置STA1无线网卡的属性为WPA2-PSK认证，关联网络test1，正确输入密码。
#预期
#成功关联，并获取192.168.91.X网段的IP地址。Show wireless client summery
#可以看到STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。AC
################################################################################
printStep(testname,'Step 4',
          'STA1 connect to network 1,',
          'connect success.')

res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='wpa2_psk',psk='abcd1234',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)

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
SetCmd(switch1,'security mode none')
SetCmd(switch1,'no wpa key')
SetCmd(switch1,'no wpa versions')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

#end
printTimer(testname, 'End')