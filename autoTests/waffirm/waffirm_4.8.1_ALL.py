#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.8.1.py - test case 4.8.1 of waffirm
#
# Author: 
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.8.1	外置Portal功能测试-
# 测试目的：测试客户端发起HTTP请求时，能够成功重定向到外置Portal的认证页面
# 测试环境：同测试拓扑
# 测试描述：测试客户端发起HTTP请求时，能够成功重定向到外置Portal的认证页面，客户端能够成功的上/下线。
#
#*******************************************************************************
# Change log:
#     - 2017.10.25 zhangjxp RDM49534 修改step6-7
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.8.1'
avoiderror(testname)
printTimer(testname,'Start','Test extrnal portal')

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


# EnterConfigMode(switch1)
# SetCmd(switch1,'radius source-ipv4 ' + StaticIpv4_ac1)
# SetCmd(switch1,'radius-server key test')
# SetCmd(switch1,'radius-server authentication host ' + Radius_server)
# SetCmd(switch1,'radius-server accounting host ' + Radius_server)
# SetCmd(switch1,'radius nas-ipv4 ' + StaticIpv4_ac1)
# SetCmd(switch1,'aaa group server radius wlan')
# SetCmd(switch1,'server ' + Radius_server)
# EnterConfigMode(switch1)
# SetCmd(switch1,'aaa enable')
# SetCmd(switch1,'aaa-accounting enable')
# EnterConfigMode(switch1)
# SetCmd(switch1,'captive-portal')
# SetCmd(switch1,'enable')
# SetCmd(switch1,'authentication-type external')
# SetCmd(switch1,'external portal-server server-name eportal ipv4 ' + Radius_server)
# SetCmd(switch1,'free-resource 1 destination ipv4 ' + Radius_server +'/32 source any')
# SetCmd(switch1,'configuration 1 ')
# SetCmd(switch1,'enable')
# SetCmd(switch1,'radius accounting ')
# SetCmd(switch1,'protocol http')
# SetCmd(switch1,'radius-acct-server wlan')
# SetCmd(switch1,'radius-auth-server wlan')
# SetCmd(switch1,'redirect attribute ssid enable ')
# SetCmd(switch1,'redirect attribute nas-ip enable')
# SetCmd(switch1,'redirect attribute url-after-login enable')
# SetCmd(switch1,'redirect attribute url-after-login encode base64')
# SetCmd(switch1,'redirect attribute url-after-login name redirect')
# SetCmd(switch1,'redirect attribute apmac enable')
# SetCmd(switch1,'redirect attribute usermac enable')
# SetCmd(switch1,'ac-name 0100.0010.0'+EnvNo+'0.01')
# SetCmd(switch1,'redirect url-head http://192.168.10.101/a79.htm')
# SetCmd(switch1,'portal-server ipv4 eportal')
# SetCmd(switch1,'free-resource 1')
# SetCmd(switch1,'interface ws-network 1')
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
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
IdleAfter(10)
res2 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
res2=0 if res2 !=0 else -1
#result
printCheckStep(testname, 'Step 2',res1,res2)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 3
    #操作
    #客户端STA1访问1.1.1.1
    #
    #预期
    #STA1被重定向到Portal认证页面
    ################################################################################

    printStep(testname,'Step 3',
              'sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=res2=res3=1
    #operate
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

    printCheckStep(testname, 'Step 3',res3)

    ################################################################################
    #Step 4
    #操作
    #输入用户名和密码
    #
    #预期
    #通过认证。在AC1上show captive portal client status可以看到用户
    ################################################################################

    printStep(testname,'Step 4',
              'enter the right username and password',
              'auth successfully')
    res1=res2=res3=res4=1
    #operate
    res1 = portal_login(web,'aaa','111')
    if res1['status']:
        res2 = 0
    else:
        printRes(res1)
    res3 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
    EnterEnableMode(switch1)
    data1=SetCmd(switch1,'show captive-portal client status')
    res4=CheckLine(data1,sta1mac)
    #result
    printCheckStep(testname, 'Step 4',res2,res3,res4)

    ################################################################################
    #Step 5
    #操作
    #客户端主动下线。
    #
    #预期
    #下线成功。AC1上show captive portal client status看不到用户。
    ################################################################################
    printStep(testname,'Step 5',
              'sta1 logout')
    res1=res2=res3=1
    #operate
    res1 = portal_logout(web)
    if res1 != None:
        if res1['status']:
            res2 = 0
        else:
            res2 =1
            printRes(res1)
    EnterEnableMode(switch1)
    IdleAfter(3)
    i = 0
    while i < 5:
        data1=SetCmd(switch1,'show captive-portal client status')
        res3=CheckLine(data1,sta1mac)
        res3 = 0 if res3 != 0 else 1
        if res3 == 0:
            break
        IdleAfter(3)
        i = i+1

    res4 = web_close(web)
    printRes(res1)
    if not res4['status']:
        CMDKillFirefox(sta1)
    #result
    printCheckStep(testname, 'Step 5',res2,res3)
    ################################################################################
    #Step 6
    #操作
    #配置额外的http端口为8081。
    # switch(config-cp-instance)#http port 8081

    #
    #预期
    #查看http重定向的端口为8080
    ################################################################################
    printStep(testname,'Step 6',
              'Config http port 8081')
    res1=1
    #operate
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'configuration 1')
    # SetCmd(switch1,'http port 8080')
    SetCmd(switch1,'http port 8081')
    data=SetCmd(switch1,'show run c')
    res1 = CheckLine(data,'http port 8081')
    #result
    printCheckStep(testname, 'Step 6',res1)

    ################################################################################
    #Step 7
    #操作
    #在客户端STA1上访问http://2.2.2.2:8081。
    #
    #预期
    #STA1被重定向到Portal认证页面
    ################################################################################

    printStep(testname,'Step 7',
              'sta1 open 2.2.2.2 and can redirect to portal auth page')
    res1=res2=res3=1
    #operate
    web = web_init(sta1_host)
    if None != web:
        res1 = web_open(web,'http://2.2.2.2:8081')
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

    printCheckStep(testname, 'Step 7',res3)

    ################################################################################
    #Step 8
    #操作
    #输入用户名和密码
    #
    #预期
    #通过认证。在AC1上面show captive portal client status可以看到用户
    ################################################################################

    printStep(testname,'Step 8',
              'enter the right username and password',
              'auth successfully')
    res1=res2=res3=1
    #operate
    res1 = portal_login(web,'aaa','111')
    if res1['status']:
        res2 = 0
    else:
        printRes(res1)
    EnterEnableMode(switch1)
    data1=SetCmd(switch1,'show captive-portal client status')
    res3=CheckLine(data1,sta1mac)
    #result
    printCheckStep(testname, 'Step 8',res2,res3)

    ################################################################################
    #Step 9
    #操作
    #客户端主动下线。
    #
    #预期
    #下线成功。AC1上show captive portal client status看不到用户。
    ################################################################################
    printStep(testname,'Step 9',
              'sta1 logout')
    res1=res2=res3=1
    #operate
    res1 = portal_logout(web)
    if res1 != None:
        if res1['status']:
            res2 = 0
        else:
            res2 =1
            printRes(res1)
    EnterEnableMode(switch1)
    IdleAfter(3)
    i = 0
    while i < 5:
        data1=SetCmd(switch1,'show captive-portal client status')
        res3=CheckLine(data1,sta1mac)
        res3 = 0 if res3 != 0 else 1
        if res3 == 0:
            break
        IdleAfter(3)
        i = i+1
    printCheckStep(testname, 'Step 9',res2,res3)
    # 关闭firefox窗口
    res1 = web_close(web)
    printRes(res1)
    if not res1['status']:
        CMDKillFirefox(sta1)
################################################################################
#Step 10
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 10',
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
	
#end
printTimer(testname, 'End')