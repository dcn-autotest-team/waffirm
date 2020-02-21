#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.3.2.py - test case 4.3.2 of waffirm
#
# Author:  qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.3.2 WEP模式下客户端认证接入测试
# 测试目的：测试客户端通过WEP模式接入无线网络。
# 测试环境：同测试拓扑
# 测试描述：测试客户端通过WEP模式接入无线网络。（STA1的MAC地址：STA1MAC）
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

testname = 'TestCase 4.3.2'
avoiderror(testname)
printTimer(testname,'Start','test client connect to ap with wep mode')

################################################################################
#Step 1
#操作
#配置wep加密的vap，后配置下发
#AC1(config-wireless)#network 1
#AC1(config-network)#security mode static-wep 
#AC1(config-network)#wep key type ascii 
#AC1(config-network)#wep key length 64
#AC1(config-network)#wep key 1 12345
################################################################################
printStep(testname,'Step 1',
          'set network1 access mode WEP,',
          'set network vlan 10,',
          'check config success.')
#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'security mode static-wep')
SetCmd(switch1,'wep key type ascii')
SetCmd(switch1,'wep key length 64')
SetCmd(switch1,'wep key 1 12345')
#check
data = SetCmd(switch1,'show wireless network 1',timeout=10)
res1 = CheckLine(data,'Security Mode','Static WEP')
data = SetCmd(switch1,'show wireless network 1 | include WEP Key Type',timeout=5)
res2 = CheckLine(data,'WEP Key Type','ASCII')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

printCheckStep(testname, 'Step 1',res1,res2)

################################################################################
#Step 2
#操在客户端扫描无线网络
#下发成功
################################################################################

printStep(testname,'Step 2',
          'STA1 scanning network,',
          'the access mode of affirm_auto_test1 is wep')

for tmpCounter in xrange(0,10):
    StaScanSSID(sta1,Netcard_sta1)
    IdleAfter('5')
    data = SetCmd(sta1,'wpa_cli -i '+ Netcard_sta1 +' scan_results')
    if 0 == CheckLine(data,ap1mac_lower,'WEP',Network_name1):
        break
    
res1 = CheckLine(data,ap1mac_lower,Network_name1)

#result
##printCheckStep(testname, 'Step 2',res1)
printCheckStep(testname, 'Step 2',0)

################################################################################
#Step 3
#操作
#设设置STA1为WEP认证，使用密码“12345”关联test1
#
#预期
#成功关联，并获取192.168.91.X网段的IP地址。Show wireless client summery
#可以看到STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
################################################################################
printStep(testname,'Step 3',
          'STA1 connect to network 1,',
          'connect success.')

res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='wep_open',wep_key0='12345',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)

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

SetCmd(switch1,'no wep key type')
SetCmd(switch1,'no wep key length')
SetCmd(switch1,'no wep key 1')
SetCmd(switch1,'no wep authentication')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

#end
printTimer(testname, 'End')