#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.8.7.py - test case 4.8.7 of waffirm
#
# Author: 
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.8.7	portal内置用户认证功能测试
# 测试目的：测试客户端发起HTTP请求时，能够成功重定向到内置Portal的认证页面
# 测试环境：同测试拓扑
# 测试描述：测试客户端发起HTTP请求时，能够成功重定向到内置Portal的认证页面，客户端能够成功的上/下线
#
#*******************************************************************************
# Change log:
#     - - creadte by zhangjxp 2017.5.26
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.8.7'
avoiderror(testname)
printTimer(testname,'Start','Test interal portal(local user)')

###############################################################################
#Step 1
#操作
#开启Captive Portal功能，network 1映射到实例1，配置netwrok1的vlan
# 为4091,认证类型为内置Portal,配置configuration 1
#
#预期
#配置成功
################################################################################
printStep(testname,'Step 1',
          'Config internal portal Configuration on AC1')
#operate
localusername='abc'
localuserpw='abc'
EnterConfigMode(switch1)
# SetCmd(switch1,'ip http server')
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'enable')
SetCmd(switch1,'authentication-type internal')
SetCmd(switch1,'configuration 1 ')
SetCmd(switch1,'enable')
SetCmd(switch1,'protocol http')
SetCmd(switch1,'verification local')
SetCmd(switch1,'interface ws-network 1')
SetCmd(switch1,'group 1')
SetCmd(switch1,'exit')
SetCmd(switch1,'user '+localusername)
SetCmd(switch1,'password '+localuserpw)
SetCmd(switch1,'group 1')

if Ap1cmdtype == 'uci':
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'free-resource 1 destination ipv4 ' + StaticIpv4_ac1 +'/32 source any')
    SetCmd(switch1,'configuration 1 ')
    SetCmd(switch1,'free-resource 1')
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
    res1=res2=res3=1
    #operate
    res1 = portal_login(web,localusername,localuserpw)
    if res1['status']:
        res2 = 0
    else:
        printRes(res1)

    EnterEnableMode(switch1)
    data1=SetCmd(switch1,'show captive-portal client status')
    res3=CheckLine(data1,sta1mac,localusername)
    #result
    printCheckStep(testname, 'Step 4',res2,res3)

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
    #result
    printCheckStep(testname, 'Step 5',res2,res3)
    # 关闭firefox窗口
    res1 = web_close(web)
    printRes(res1)
    if not res1['status']:
        CMDKillFirefox(sta1)
################################################################################
#Step 6
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 6',
          'Recover initial config for switches.')

#operate

WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'disable')
SetCmd(switch1,'no configuration 1')
SetCmd(switch1,'no authentication-type')
SetCmd(switch1,'no user '+localusername,timeout=1)
SetCmd(switch1,'y',timeout=1)

if Ap1cmdtype == 'uci':
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'no free-resource 1')
#end
printTimer(testname, 'End')