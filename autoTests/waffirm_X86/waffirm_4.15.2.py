#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.15.2.py - test case 4.15.2 of waffirm
#
# Author:  qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2013 Digital China Networks Co. Ltd
#
# Features:
# 4.15.2 基于流量的负载均衡
# 测试目的：测试AC上面的流量模式负载均衡功能。
# 测试环境：同测试拓扑1
# 测试描述：AC上面启用流量模式的负载均衡功能以后，能够实现客户端的连接通过流量小的ap上去。
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

testname = 'TestCase 4.15.2'
printTimer(testname,'Start','Load balance of traffic mode')

################################################################################
#Step 1
#操作
#确保ap1和ap2被ac1管理，并且被管理到profile 1下面。两个ap有相同的ssid：test
#
#预期
#sho wireless ap status查看有两个ap被正常管理。
################################################################################
printStep(testname,'Step 1',\
          'Set 2 aps in the same profile 1')


SetCmd(switch1,'show wireless ap status')

printCheckStep(testname, 'Step 1',0)

################################################################################
#Step 2
#操作
#在无线全局模式下创建负载均衡模板，开启会话模式的负载均衡功能：
#switch(config-wireless)#ap load-balance template 1
#switch(config-load-balance)#load-balance traffic
#
#预期
#Show run查看无线全局的ap load-balance template 1已经创建并且load session功能已经开启。
#sho wireless load-balance template 1显示load traffic功能已经开启。
################################################################################

printStep(testname,'Step 2',\
          'Config load balance template')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap load-balance template 1')
SetCmd(switch1,'load-balance traffic')
data = SetCmd(switch1,'show wireless load-balance template')
res1 = CheckLine(data,'1\s+Enable\s+Traffic')

printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#在负载均衡配置模版下，设置门限值和拒绝次数：
#switch(config-load-balance)#load-balance traffic window 4 threshold 1
#switch(config-load-balance)#load-balance denial 10
#
#预期
#Show run显示门限值和拒绝次数配置正确。sho wireless load-balance template 1显示门限值和拒绝次数配置正确。
################################################################################

printStep(testname,'Step 3',\
          'Config load balance session denial and threshold')

SetCmd(switch1,'load-balance traffic window 1 threshold 1')
SetCmd(switch1,'load-balance denial Unlimited')
data = SetCmd(switch1,'show wireless load-balance template 1')
res1 = CheckLine(data,'Traffic Window\.+? 1')
res2 = CheckLine(data,'Traffic Threshold\.+? 1')
res3 = CheckLine(data,'Unlimited')

printCheckStep(testname, 'Step 3',res1,res2,res3)

################################################################################
#Step 4
#操作
#将创建的负载均衡配置模板添加到ap profile 1下面：
#switch(config-ap-profile)#load-balance template 1
#
#预期
#Show run和show wireless ap profile 1能够查看到负载均衡配置模板1已经添加到ap profile 1下面。
################################################################################

printStep(testname,'Step 4',\
          'Config load balance template to ap profile 1')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 1')
SetCmd(switch1,'load-balance template 1')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 2')
SetCmd(switch1,'load-balance template 1')
data = SetCmd(switch1,'show wireless ap profile 1')
res1 = CheckLine(data,'Load-balance Template ID\.+? 1')

printCheckStep(testname, 'Step 4',res1)

################################################################################
#Step 5
#操作
#打开负载均衡debug：
#switch#debug wireless load-balance internal ap1MAC
#switch#debug wireless load-balance internal ap2MAC
#
#预期
#switch#show debugging other能够看到打开的debug
################################################################################

printStep(testname,'Step 5',\
          'Start debug ap load balance.')

EnterEnableMode(switch1)
SetCmd(switch1,'debug wireless load-balance internal ' + ap2mac)
SetCmd(switch1,'debug wireless load-balance internal ' + ap1mac)
data = SetCmd(switch1,'show debugging other')
res1 = CheckLine(data,'internal WD_LEVEL')

printCheckStep(testname, 'Step 5',res1)

################################################################################
#Step 6
#操作
#STA1关联test1。
#
#预期
#成功关联，并获取192.168.91.X网段的IP地址。Show wireless client summery可以看到sta1，IP地址的网段正确。
################################################################################

printStep(testname,'Step 6',\
          'STA1 connect to test1',\
          'STA1 get a 192.168.91.X ipaddress and show client summery can see client.')

res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='open',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')

data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
if None != SearchResult1:
    sta1_ipv4 = SearchResult1.group(1)
    if None != re.search(Dhcp_pool2,sta1_ipv4):
        printRes('STA1 ip address: ' + sta1_ipv4)
        res3 = 0  
else:
    res3 = 1
    sta1_ipv4 = '7.7.7.7'
    printRes('Failed: Get ipv4 address of STA1 failed') 

printCheckStep(testname, 'Step 6',res1,res2,res3)

################################################################################
#Step 7
#操作
#
#Client2关联ssid：test。Client2关联成功且有如下debug信息打印：“Apply Load Balance(Traffic)”
#看不到debug打印，client2解除关联重新关联，重复10次，直到看到debug信息。
#
#预期
#可以看到debug打印：“Apply Load Balance(Session)”
################################################################################

printStep(testname,'Step 7',\
          'STA2 connect to ssid and trigger load balance')

data3 = SetCmd(pc1,'downloadtest -u http://' + sta1_ipv4 + '/mbrs.zip',timeout=0.5)

StartDebug(switch1)

res1 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,connectType='open',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)

data = StopDebug(switch1)

res3 = CheckLine(data,'Apply Load Balance\(Traffic\)')

if res3 != 0:
    for tmpCounter in xrange(0,10):
        StartDebug(switch1)
        res0 = WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)
        res1 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,connectType='open',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
        data = StopDebug(switch1)
        res3 = CheckLine(data,'Apply Load Balance\(Traffic\)')
        if res3 == 0:
            break 

printCheckStep(testname, 'Step 7',res3)

################################################################################
#Step 8
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 8',\
          'Recover initial config for switches.')

res1 = WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
res1 = WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)
EnterWirelessMode(switch1)
SetCmd(switch1,'ap load-balance template 1')
SetCmd(switch1,'no load-balance')
SetCmd(switch1,'\x0F')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 1')
SetCmd(switch1,'no load-balance template')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 2')
SetCmd(switch1,'no load-balance template')
# WirelessApProfileApply(switch1,'1')
# IdleAfter(5)
# WirelessApProfileApply(switch1,'2')
# IdleAfter(Apply_profile_wait_time)
WirelessApplyProfileWithCheck(switch1,['1','2'],[ap1mac,ap2mac])
SetCmd(ap2,'admin',timeout=1)
SetCmd(ap2,'admin',timeout=1)
SetCmd(ap2,'admin',timeout=1)
SetCmd(ap2,'admin',timeout=1)

#operate

#end
printTimer(testname, 'End')