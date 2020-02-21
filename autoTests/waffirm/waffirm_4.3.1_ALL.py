#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.3.1.py - test case 4.3.1 of waffirm
#
# Author:  qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 4.3.1 Open方式下客户端接入测试
# 测试目的：测试客户端通过open方式接入无线网络。
# 测试环境：同测试拓扑1
# 测试描述：测试客户端能够通过open方式接入无线网络。
#
#*******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17s
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.3.1'
avoiderror(testname)
printTimer(testname,'Start','test wireless client connect to network with open-mode')

################################################################################
#Step 1
#操作
#UWS1的network1采用默认的安全接入方式none，即open方式。配置下发到AP1。
#wireless ap profile apply 1
#
#预期
#配置下发成功。
################################################################################
printStep(testname,'Step 1',
          'set network1 access mode open as default,',
          'apply ap profile1 to ap,',
          'check config success.')
#operate
IdleAfter(60)
EnterNetworkMode(switch1,1)
SetCmd(switch1,'security mode none')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

#check
data = SetCmd(switch1,'show wireless network 1',timeout = 10)
res1 = CheckLine(data,'Security Mode\.+\s*None')
#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#操作
#在客户端STA1扫描无线网络。
#
#预期
#显示test1为open的。
################################################################################

printStep(testname,'Step 2',
          'STA1 scanning test1',
          'the security of test1 is open.')

for tmpCounter in xrange(0,10):
    StaScanSSID(sta1,Netcard_sta1)
    IdleAfter('5')
    data = SetCmd(sta1,'wpa_cli -i '+ Netcard_sta1 +' scan_results')
    if 0 == CheckLine(data,ap1mac_lower,'\[ESS\] ' + Network_name1):
        break
res1 = CheckLine(data,ap1mac_lower,'WPA',Network_name1)
res2 = CheckLine(data,ap1mac_lower,'WEP',Network_name1)

printCheckStep(testname, 'Step 2',0)

################################################################################
#Step 3
#操作
#STA1关联test1。
#
#预期
#成功关联，并获取192.168.91.X网段的IP地址。Show wireless client summery可以看到sta1，IP地址的网段正确。
################################################################################

printStep(testname,'Step 3',
          'STA1 connect to test1',
          'STA1 get a 192.168.91.X ipaddress and show client summery can see client.')

res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='open',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)

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
          'STA1 close the connecting with network1,',
          'show wireless client summary and no STA1 client.')

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

#end
printTimer(testname, 'End')