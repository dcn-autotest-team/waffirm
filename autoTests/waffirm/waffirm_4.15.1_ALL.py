#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.15.1.py - test case 4.15.1 of waffirm
#
# Author:  qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2013 Digital China Networks Co. Ltd
#
# Features:
# 4.15.1 基于会话模式的负载均衡
# 测试目的：测试AC上面的会话模式负载均衡功能。
# 测试环境：同测试拓扑1
# 测试描述：AC上面启用会话模式的负载均衡功能以后，能够实现不同客户端均衡的连接不同的ap。
#
#*******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.15.1'
avoiderror(testname)
printTimer(testname,'Start','Load balance of session mode')

################################################################################
#Step 1
#操作
#确保ap1和ap2被ac1管理，并且被分别管理到profile 1和profle2下面。两个ap有相同的ssid：test
#Profile1和proflie2都设置扫描参数（xuwf：由于缺省扫描间隔变更为86400
#导致ac上的client的三角状态表可能为空，无法触发负载均衡。）：
#radio 1
#rf-scan other-channels interval 10
#配置ssid的加密方式为wpa个人级（防止空中其他sta自动关联的影响）
#wireless
#network 1
#security mode wpa-personal
#wpa key abcd1234
#wpa versions wpa
#将配置下发到AP1：
#Wireless ap profile apply 1
#将配置下发到AP2：
#Wireless ap profile apply 2

#预期
#sho wireless ap status查看有两个ap被正常管理。
################################################################################
printStep(testname,'Step 1',
          'Set ap1 in profile 1,set ap2 in profile 2')
res = 1
EnterApProMode(switch1,1)
# SetCmd(switch1,'radio 1')
SetCmd(switch1,'radio '+radionum)
SetCmd(switch1,'rf-scan other-channels interval 10')
SetCmd(switch1,'exit')
SetCmd(switch1,'exit')
EnterApProMode(switch1,2)
# SetCmd(switch1,'radio 1')
SetCmd(switch1,'radio '+radionum)
SetCmd(switch1,'rf-scan other-channels interval 10')
SetCmd(switch1,'exit')
SetCmd(switch1,'exit')

EnterNetworkMode(switch1,1)
SetCmd(switch1,'security mode wpa-personal')
SetCmd(switch1,'wpa key abcd1234')
SetCmd(switch1,'wpa versions wpa')
res = WirelessApplyProfileWithCheck(switch1,['1','2'],[ap1mac,ap2mac])

printCheckStep(testname, 'Step 1',res)

################################################################################
#Step 2
#操作
#在无线全局模式下创建负载均衡模板，开启会话模式的负载均衡功能：
#switch(config-wireless)#ap load-balance template 1
#switch(config-load-balance)#load-balance session
#
#预期
#Show run查看无线全局的ap load-balance template 1已经创建并且load session功能已经开启。
#sho wireless load-balance template 1显示load session功能已经开启。
################################################################################

printStep(testname,'Step 2',
          'Config load balance template')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap load-balance template 1')
SetCmd(switch1,'load-balance session')
data = SetCmd(switch1,'show wireless load-balance template')
res1 = CheckLine(data,'1\s+Enable\s+Session')

printCheckStep(testname, 'Step 2',res1)


################################################################################
#Step 3
#操作
#在负载均衡配置模版下，设置门限值和拒绝次数：
#switch(config-load-balance)#load-balance session window 1 threshold 1
#switch(config-load-balance)#load-balance denial unlimited
#
#预期
#Show run显示门限值和拒绝次数配置正确。sho wireless load-balance template 1显示门限值和拒绝次数配置正确。
################################################################################

printStep(testname,'Step 3',
          'Config load balance session denial and threshold')

SetCmd(switch1,'load-balance session window 1 threshold 1')
SetCmd(switch1,'load-balance denial Unlimited')
data = SetCmd(switch1,'show wireless load-balance template 1')
res1 = CheckLine(data,'Session Window\.+? 1')
res2 = CheckLine(data,'Session Threshold\.+? 1')
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

printStep(testname,'Step 4',
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

printStep(testname,'Step 5',
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

printStep(testname,'Step 6',
          'STA1 connect to test1',
          'STA1 get a 192.168.91.X ipaddress and show client summery can see client.')

res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='wpa_psk',psk='abcd1234',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)

res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')

printCheckStep(testname, 'Step 6',res1,res2)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 7
    #操作
    #
    #Client2关联ssid：test。Client2关联成功且有如下debug信息打印：“Apply Load Balance(Session)”
    #看不到debug打印，client2解除关联重新关联，重复10次，直到看到debug信息。
    #
    #预期
    #可以看到debug打印：“Apply Load Balance(Session)”
    ################################################################################

    printStep(testname,'Step 7',
              'STA2 connect to ssid and trigger load balance')

    StartDebug(switch1)

    res1 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,connectType='wpa_psk',psk='abcd1234',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)

    res2 = CheckWirelessClientOnline(switch1,sta2mac,'online')

    data = StopDebug(switch1)

    res3 = CheckLine(data,'Apply Load Balance\(Session\)')

    if res3 != 0:
        for tmpCounter in xrange(0,10):
            StartDebug(switch1)
            res0 = WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)
            res1 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,connectType='wpa_psk',psk='abcd1234',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
            res2 = CheckWirelessClientOnline(switch1,sta2mac,'online')
            data = StopDebug(switch1)
            res3 = CheckLine(data,'Apply Load Balance\(Session\)')
            if res3 == 0:
                break  

    printCheckStep(testname, 'Step 7',res3)


################################################################################
#Step 8
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 8',
          'Recover initial config for switches.')

res1 = WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
res1 = WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)
SetCmd(switch1,'\x0F')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap load-balance template 1')
SetCmd(switch1,'no load-balance session')
SetCmd(switch1,'no load-balance traffic')
SetCmd(switch1,'no load-balance denial')
SetCmd(switch1,'no load-balance')
##EnterWirelessMode(switch1)
##SetCmd(switch1,'ap database ' + ap2mac)
##
##SetCmd(switch1,'profile 2')
##
EnterNetworkMode(switch1,1)
SetCmd(switch1,'security mode none')
SetCmd(switch1,'no wpa key')
SetCmd(switch1,'no wpa versions')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 1')
SetCmd(switch1,'no load-balance template')
# SetCmd(switch1,'radio 1')
SetCmd(switch1,'radio '+radionum)
SetCmd(switch1,'rf-scan other-channels interval 5')
SetCmd(switch1,'exit')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 2')
SetCmd(switch1,'no load-balance template')
# SetCmd(switch1,'radio 1')
SetCmd(switch1,'radio '+radionum)
SetCmd(switch1,'no rf-scan other-channels interval')
SetCmd(switch1,'exit')
WirelessApplyProfileWithCheck(switch1,['1','2'],[ap1mac,ap2mac])

# IdleAfter(30)
#operate

#end
printTimer(testname, 'End')