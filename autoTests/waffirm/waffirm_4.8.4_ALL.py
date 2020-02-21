#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.8.4.py - test case 4.8.4 of waffirm
#
# Author: 
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.8.4	Captive Portal free-resource功能测试
# 测试目的：测试客户端在未通过Portal认证的情况下可以访问free-resource资源
# 测试环境：同测试拓扑
# 测试描述：测试客户端在未通过Portal认证的情况下可以访问free-resource资源。
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

testname = 'TestCase 4.8.4'
avoiderror(testname)
printTimer(testname,'Start','Test free-resource')

###############################################################################
#Step 1
#操作
#在AC1配置network1的SSID为test1，关联vlan4091，配置下发到AP1，
#配置Radius服务器
#配置外置Portal,配置下发到AP1
#
#
#预期
#配置成功
################################################################################
printStep(testname,'Step 1',
          'Config Extrnal portal Configuration on AC1')
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
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'enable')
SetCmd(switch1,'authentication-type external')
SetCmd(switch1,'external portal-server server-name eportal ipv4 ' + Radius_server)
SetCmd(switch1,'free-resource 1 destination ipv4 ' + Radius_server +'/32 source any')
SetCmd(switch1,'configuration 1 ')
SetCmd(switch1,'enable')
SetCmd(switch1,'radius accounting ')
SetCmd(switch1,'protocol http')
SetCmd(switch1,'radius-acct-server wlan')
SetCmd(switch1,'radius-auth-server wlan')
SetCmd(switch1,'redirect attribute ssid enable ')
SetCmd(switch1,'redirect attribute nas-ip enable')
SetCmd(switch1,'redirect attribute url-after-login enable   ')
SetCmd(switch1,'redirect attribute apmac enable')
SetCmd(switch1,'redirect attribute usermac enable')
SetCmd(switch1,'ac-name 0100.0010.0'+EnvNo+'0.01')
SetCmd(switch1,'redirect url-head http://192.168.10.101/a79.htm')
SetCmd(switch1,'portal-server ipv4 eportal')
SetCmd(switch1,'free-resource 1')
SetCmd(switch1,'interface ws-network 1')

res1 = 0
#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#操作
#客户端STA1连接到网络test1
#
#预期
#关联成功。客户端获取192.168.91.X网段的IP地址。
################################################################################

printStep(testname,'Step 2',
          'STA1 connect to test1')
res1=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
IdleAfter(10)

#result
printCheckStep(testname, 'Step 2',res1)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 3
    #操作
    #STA1 ping 20.1.1.2
    #
    #预期
    #不能ping通
    ################################################################################

    printStep(testname,'Step 3',
              'sta1 ping pc1 failed')
    res1=1
    #operate
    res1 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
    res1=0 if res1 !=0 else -1
    #result
    printCheckStep(testname, 'Step 3',res1)

    ################################################################################
    #Step 4
    #操作
    #STA1 ping free-resource
    #
    #预期
    #可以ping通
    ################################################################################

    printStep(testname,'Step 4',
              'sta1 ping free-resource successfully')
    res1=1
    #operate
    res1 = CheckPing(sta1,Radius_server,mode='linux',pingPara=' -c 10')
    #result
    printCheckStep(testname, 'Step 4',res1)
################################################################################
#Step 5
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 5',
          'Recover initial config for switches.')

#operate

WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'disable')
SetCmd(switch1,'no configuration 1')
SetCmd(switch1,'no external portal-server ipv4 server-name eportal')
SetCmd(switch1,'no free-resource 1')
EnterConfigMode(switch1)
SetCmd(switch1,'no radius source-ipv4')
SetCmd(switch1,'no radius-server key')
SetCmd(switch1,'no aaa group server radius wlan')
SetCmd(switch1,'no radius nas-ipv4')
SetCmd(switch1,'no aaa enable')
SetCmd(switch1,'no aaa-accounting enable')
SetCmd(switch1,'no radius-server authentication host ' + Radius_server)
SetCmd(switch1,'no radius-server accounting host ' + Radius_server)

EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'disable')
#end
printTimer(testname, 'End')