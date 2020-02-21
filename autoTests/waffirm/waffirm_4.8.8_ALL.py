#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.8.8.py - test case 4.8.8 of waffirm
#
# Author: 
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.8.8	portal逃生功能测试
# 测试目的：测试在captive portal功能开启式，如果AC与外置portal服务器之间的链接发生故障，
# web认证的用户STA关联后可以访问外网
# 测试环境：同测试拓扑
# 测试描述：测试在captive portal功能开启式，如果AC与外置portal服务器之间的链接发生故障，
# web认证的用户STA关联后无需进行认证就够能直接访问外网，无需进行认证
#
#*******************************************************************************
# Change log:
#     - creadte by zhangjxp 2017.5.26
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.8.8'
avoiderror(testname)
printTimer(testname,'Start','Test extrnal portal escape function')

###############################################################################
#Step 1
#操作
#在AC1配置network1的SSID为test1，关联vlan4091，配置下发到AP1，
#配置Radius服务器
#配置外置Portal
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
#配置Portal逃生功能，并配置探测周期和最大失败次数
#
#预期
#配置成功，通过show captive-portal ext-portal-server server-name <name> status
# 检查Portal server的Detect Mode应该为enable。
################################################################################
printStep(testname,'Step 2',
          'Config portal-server-detect')
res1=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'enable')
SetCmd(switch1,'portal-server-detect server-name eportal interval 20 retry 2 action log permit-all trap')
# check
data=SetCmd(switch1,'show captive-portal ext-portal-server server-name eportal status')
res1=CheckLineList(data,[('Detect Mode','Enable')],IC=True)
#result
printCheckStep(testname, 'Step 2',res1)
################################################################################
#Step 3
#操作
#客户端STA1连接到网络test1
#
#预期
#关联成功。客户端获取192.168.91.X网段的IP地址
################################################################################

printStep(testname,'Step 3',
          'STA1 connect to test1')
res1=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
IdleAfter(10)

#result
printCheckStep(testname, 'Step 3',res1)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 4
    #操作
    #STA1 上ping vlan 4091的网关地址192.168.91.1，同时访问1.1.1.1。
    #
    #预期
    #STA1无法ping通网关地址。(访问页面被重定向到Portal认证页面)
    ################################################################################

    printStep(testname,'Step 4',
              'sta1 open 1.1.1.1 and can redirect to portal auth page')
    res=res1=res2=res3=1
    #operate
    res = CheckPing(sta1,If_vlan4091_s1_ipv4,mode='linux',pingPara=' -c 10')
    res=0 if res !=0 else -1
    web = web_init(sta1_host)
    if None != web:
        res1 = web_open(web,'http://1.1.1.1')
        if res1['status']:
            res2 = is_portal_page(web)
            if res2['status']:
                res3 = 0
            else:
                res3 = 1
                printRes('is_portal_page(web) status false')
        else:
            res3 = 1
            printRes('web_open(web,\'http://1.1.1.1\')')
    else:
        res3 =1
        printRes('web_init(sta1) status false')

    res4 = web_close(web)
    printRes(res1)
    if not res4['status']:
        CMDKillFirefox(sta1)
    printCheckStep(testname, 'Step 4',res,res3)

    ################################################################################
    #Step 5
    #操作
    #禁用portal服务器，断开AC和portal服务器之间的连接，触发portal逃生功能启动。
    # 查看portal服务器连接状态show captive-portal ext-portal-server server-name <name> status
    # 中的Detect Operational Status参数
    #
    #预期
    #Portal逃生功能已经开启，检查Detect Operational Status的状态应该为down。
    ################################################################################
    printStep(testname,'Step 5',
              'Shutdown s3p5',
              'trigger portal escape function')
    res1=1
    #operate
    EnterInterfaceMode(switch3,s3p5)
    SetCmd(switch3,'shutdown')
    # check
    IdleAfter(20)
    EnterEnableMode(switch1)
    i=0
    while i<6:
        data=SetCmd(switch1,'show captive-portal ext-portal-server server-name eportal status')
        res1=CheckLineList(data,[('Detect Operational Status','Down')],IC=True)
        if res1 == 0:
            break
        IdleAfter(5)
        i = i + 1
    #result
    printCheckStep(testname, 'Step 5',res1)

    ################################################################################
    #Step 6
    #操作
    #STA1去关联，并等待漫游判定时间（缺省30s）超时后show captive client status
    #
    #预期
    #captive client表中没有STA1
    ################################################################################
    printStep(testname,'Step 6',
              'sta1 disconnect test1')
    res1=1
    #operate
    WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
    IdleAfter(35)
    EnterEnableMode(switch1)
    data=SetCmd(switch1,'show captive-portal client status')
    res1=CheckLine(data,sta1mac)
    res1 = 0 if res1 != 0 else 1
    #result
    printCheckStep(testname, 'Step 6',res1)

    ################################################################################
    #Step 7
    #操作
    #客户端STA1连接到网络test1
    #
    #预期
    #关联成功。客户端获取192.168.91.X网段的IP地址
    ################################################################################

    printStep(testname,'Step 7',
              'STA1 connect to test1')
    res1=1
    #operate
    #STA1关联 network1
    res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
    IdleAfter(10)

    #result
    printCheckStep(testname, 'Step 7',res1)
    ################################################################################
    #Step 8
    #操作
    #STA1 上ping vlan 4091的网关地址192.168.91.1，同时访问1.1.1.1。
    #
    #预期
    #可以ping通的网关。（访问页面没有被重定向，无法打开）。
    ################################################################################
    printStep(testname,'Step 8',
              'sta1 ping pc1 successfully'
              'sta1 open 1.1.1.1 and could not redirect to portal auth page')
    res=res1=1
    #operate
    res = CheckPing(sta1,If_vlan4091_s1_ipv4,mode='linux',pingPara=' -c 10')

    web = web_init(sta1_host)
    if None != web:
        res1 = web_open(web,'http://1.1.1.1')
        if res1['status']:
            res1 = 1
        else:
            res1 = 0
            printRes('fail to open(web,\'http://1.1.1.1\')')
    else:
        res1 =1
        printRes('web_init(sta1) status false')

    printCheckStep(testname, 'Step 8',res,res1)
    # 关闭firefox窗口
    res1 = web_close(web)
    printRes(res1)
    if not res1['status']:
        CMDKillFirefox(sta1)
################################################################################
#Step 9
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 9',
          'Recover initial config for switches.')

#operate
EnterInterfaceMode(switch3,s3p5)
SetCmd(switch3,'no shutdown')

WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'disable')
SetCmd(switch1,'no configuration 1')
SetCmd(switch1,'no external portal-server ipv4 server-name eportal')
SetCmd(switch1,'no free-resource 1')
SetCmd(switch1,'no portal-server-detect server-name eportal')
EnterConfigMode(switch1)
SetCmd(switch1,'no radius source-ipv4')
SetCmd(switch1,'no radius-server key')
SetCmd(switch1,'no aaa group server radius wlan')
SetCmd(switch1,'no radius nas-ipv4')
SetCmd(switch1,'no aaa enable')
SetCmd(switch1,'no aaa-accounting enable')
SetCmd(switch1,'no radius-server authentication host ' + Radius_server)
SetCmd(switch1,'no radius-server accounting host ' + Radius_server)

#end
printTimer(testname, 'End')