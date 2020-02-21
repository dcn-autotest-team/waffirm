# -*- coding: UTF-8 -*-#
#
# *******************************************************************************
# waffirm_4.8.10_ALL.py - test case 4.8.10 of waffirm
#
# Author:
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.8.10	 https重定向功能测试
# 测试目的：测试客户端https重定向功能。
# 测试描述：测试客户端通过https访问网站时，https重定向功能是否生效。  
# 测试环境：见测试拓扑。
#
# *******************************************************************************
# Change log:
#     - created by zhangjxp 2017.11.23
# *******************************************************************************

# Package
# Global Definition

# Source files

# Procedure Definition

# Functional Code

testname = 'TestCase 4.8.10'
avoiderror(testname)
printTimer(testname, 'Start', 'Test extrnal portal,especially for https')

###############################################################################
# Step 1（合并方案step1/2)
# 操作
# 在AC1配置network1的SSID为test1，关联vlan4091，配置下发到AP1，
# 配置Radius服务器
# 配置外置Portal
#
#
# 预期
# 配置成功
################################################################################
printStep(testname, 'Step 1 Step 2', \
          'set radius server-name acct wlan,', \
          'set radius setver-name auth wlan,', \
          'and u should config others and so on,', \
          'check config success,' \
          'config captive-portal,')

EnterConfigMode(switch1)
SetCmd(switch1, 'radius source-ipv4 ' + StaticIpv4_ac1)
SetCmd(switch1, 'radius-server key test')
SetCmd(switch1, 'radius-server authentication host ' + Radius_server)
SetCmd(switch1, 'radius-server accounting host ' + Radius_server)
SetCmd(switch1, 'radius nas-ipv4 ' + StaticIpv4_ac1)
SetCmd(switch1, 'aaa group server radius wlan')
SetCmd(switch1, 'server ' + Radius_server)
EnterConfigMode(switch1)
SetCmd(switch1, 'aaa enable')
SetCmd(switch1, 'aaa-accounting enable')
EnterConfigMode(switch1)
SetCmd(switch1, 'captive-portal')
SetCmd(switch1, 'enable')
SetCmd(switch1, 'authentication-type external')
SetCmd(switch1, 'external portal-server server-name eportal ipv4 ' + Radius_server)
SetCmd(switch1, 'free-resource 1 destination ipv4 ' + Radius_server + '/32 source any')
SetCmd(switch1, 'configuration 1 ')
SetCmd(switch1, 'enable')
SetCmd(switch1, 'radius accounting ')
SetCmd(switch1, 'protocol http')
SetCmd(switch1, 'radius-acct-server wlan')
SetCmd(switch1, 'radius-auth-server wlan')
SetCmd(switch1, 'redirect attribute ssid enable ')
SetCmd(switch1, 'redirect attribute nas-ip enable')
SetCmd(switch1, 'redirect attribute url-after-login enable')
SetCmd(switch1, 'redirect attribute apmac enable')
SetCmd(switch1, 'redirect attribute usermac enable')
SetCmd(switch1, 'ac-name 0100.0010.0' + EnvNo + '0.01')
SetCmd(switch1, 'redirect url-head http://192.168.10.101/a79.htm')
SetCmd(switch1, 'portal-server ipv4 eportal')
SetCmd(switch1, 'free-resource 1')
SetCmd(switch1, 'interface ws-network 1')
res1 = 0

# result
printCheckStep(testname, 'Step 1 Step 2', res1)
################################################################################
# Step 3
# 操作
# 在STA1上连接test1
#
# 预期
# 关联成功。客户端获取192.168.91.X网段的IP地址
################################################################################

printStep(testname, 'Step 3', \
          'STA1connect to network 1,', \
          'STA1dhcp and get 192.168.91.x ip')

sta1_ipv4 = ''

res1 = res2 = 1

# operate
# STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1, Netcard_sta1, Network_name1, checkDhcpAddress=Netcard_ipaddress_check,
                                 bssid=ap1mac_lower)

# result
printCheckStep(testname, 'Step 3', res1)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    # Step 4
    # 操作
    # 客户端STA1访问1.1.1.1
    #
    # 预期
    # STA1被重定向到Portal认证页面
    ################################################################################

    printStep(testname, 'Step 4', \
              'STA1 http connect 1.1.1.1,')

    # web = newweb_init(sta1_host)
    # if None != web:
    # res1 = newweb_open(web,'http://1.1.1.1')
    # if res1['status'] == True:
    # res2 = newis_extralportal_page(web)
    # if res2['status'] == True:
    # res3 = 0
    # else:
    # res3 = 1
    # printRes('is_portal_page(web) status false')
    # else:
    # res3 = 1
    # printRes('web_open(web,\'http://1.1.1.1\')')
    # else:
    # res3 =1
    # printRes('web_init(sta1) status false')

    web = web_init(sta1_host)
    if None != web:
        res1 = web_open(web, 'http://1.1.1.1')
        if res1['status']:
            res2 = is_portal_page(web)
            if res2['status']:
                res3 = 0
            else:
                res3 = 1
                printRes('is_portal_page(web) status false')
        else:
            res3 = 1
            printRes('web_open(web,\'http://1.1.1.1\') failed')
    else:
        res3 = 1
        printRes('web_init(sta1) status false')
    printCheckStep(testname, 'Step 4', res3)

    ################################################################################
    # Step 5
    # 操作
    # 输入用户名和密码
    #
    # 预期
    # 通过认证。在AC1上show captive portal client status可以看到用户
    ################################################################################

    printStep(testname, 'Step 5',
                        'input username and password',
                        'auth successfully')

    # operate
    res1 = res2 = res3 = 1
    res1 = portal_login(web, 'aaa', '111')
    if res1['status']:
        res2 = 0
    else:
        printRes(res1)
    data = SetCmd(switch1, 'show captive-portal client status')
    res3 = CheckLine(data, sta1mac)
    # result
    printCheckStep(testname, 'Step 5', res2, res3)

    ################################################################################
    # Step 6
    # 操作
    # 客户端主动下线。
    #
    # 预期
    # 下线成功。AC1上show captive portal client status看不到用户
    ################################################################################

    printStep(testname, 'Step 6',
              'STA1 logout.')
    res1 = res2 = res3 = 1
    res1 = portal_logout(web)
    if res1:
        if res1['status']:
            res2 = 0
        else:
            res2 = 1
            printRes(res1)
    EnterEnableMode(switch1)
    res3 = CheckSutCmdWithNoExpect(switch1, 'show captive-portal client status',
                                   check=[(sta1mac)], waittime=5, retry=10, interval=5, IC=True)

    printCheckStep(testname, 'Step 6', res2, res3)

    res1 = web_close(web)
    printRes(res1)
    if not res1['status']:
        CMDKillFirefox(sta1)
    ################################################################################
    # Step 7
    # 操作
    # 配置额外的https端口为8887。
    # switch(config-cp-instance)#https port 8887
    #
    # 预期
    # 查看https重定向的端口为8887
    ################################################################################

    printStep(testname, 'Step 7',
              'config https port')

    res1 = 1
    EnterConfigMode(switch1)
    SetCmd(switch1, 'captive-portal')
    SetCmd(switch1, 'configuration 1')
    SetCmd(switch1, 'https port 8887')
    data = SetCmd(switch1, 'show run c')
    res1 = CheckLine(data, 'https port 8887')
    # result
    printCheckStep(testname, 'Step 7', res1)

    ################################################################################
    # Step 8
    # 操作
    # 在客户端STA1上访问https://2.2.2.2:8887
    #
    # 预期
    # STA1被重定向到Portal认证页面
    ################################################################################

    printStep(testname, 'Step 8',
              'STA1 http connect https://2.2.2.2:8887')

    web = newweb_init(sta1_host)
    if None != web:
        res1 = newweb_open(web, 'https://2.2.2.2:8887')
        if res1['status']:
            # res2 = newis_extralportal_page(web)
            res2 = is_outer_portal_page(web)
            if res2['status']:
                res3 = 0
            else:
                res3 = 1
                printRes('is_portal_page(web) status false')
        else:
            res3 = 1
            printRes('web_open(web,\'https://2.2.2.2:8887\')')
    else:
        res3 = 1
        printRes('web_init(sta1) status false')

    if res3 != 0:
        printRes('if this step fail,please check this case manually!!!!!!!')
    printCheckStep(testname, 'Step 8', res3)

    ################################################################################
    # Step 9
    # 操作
    # 输入用户名和密码
    #
    # 预期
    # 输入用户名和密码，以及验证码。	通过认证。在AC1上面show captive portal client status可以看到用户。
    ################################################################################

    printStep(testname, 'Step 9', \
              'input username and password')

    # operate
    res1 = res2 = res3 = 1
    # res1 = newextportal_login(web, 'aaa', '111')
    res1 = outer_portal_login(web, 'aaa', '111')
    if res1['status']:
        res2 = 0
    else:
        printRes(res1)
    EnterEnableMode(switch1)
    data = SetCmd(switch1, 'show captive-portal client status')
    res3 = CheckLine(data, sta1mac)
    # result
    if res2 != 0:
        printRes('if this step fail,please check this case manually!!!!!!!')
    printCheckStep(testname, 'Step 9', res2, res3)

    ################################################################################
    # Step 10
    # 操作
    # 客户端主动下线。
    #
    # 预期
    # 下线成功。AC1上show captive portal client status看不到用户。
    ################################################################################

    printStep(testname, 'Step 10', \
              'STA1 logout.')

    # res1 = newextportal_logout(web)
    res1 = outer_portal_logout(web)
    if res1 is not None:
        if res1['status']:
            res2 = 0
        else:
            res2 = 1
            printRes(res1)
        res3 = CheckSutCmdWithNoExpect(switch1, 'show captive-portal client status', \
                                       check=[(sta1mac)], waittime=5, retry=10, interval=5, IC=True)
    WpaDisconnectWirelessNetwork(sta1, Netcard_sta1)
    if res2 != 0:
        printRes('if this step fail,please check this case manually!!!!!!!')

    printCheckStep(testname, 'Step 10', res2, res3)

################################################################################
# Step 11
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 11', \
          'Recover initial config for switches.')

# operate

WpaDisconnectWirelessNetwork(sta1, Netcard_sta1)

EnterConfigMode(switch1)
SetCmd(switch1, 'captive-portal')
SetCmd(switch1, 'disable')
SetCmd(switch1, 'no configuration 1')
SetCmd(switch1, 'no authentication-type')
SetCmd(switch1, 'no external portal-server ipv4 server-name eportal')
SetCmd(switch1, 'no free-resource 1')

EnterConfigMode(switch1)
SetCmd(switch1, 'no radius source-ipv4')
SetCmd(switch1, 'no radius-server key')
SetCmd(switch1, 'no aaa group server radius wlan')
SetCmd(switch1, 'no radius nas-ipv4')
SetCmd(switch1, 'no aaa enable')
SetCmd(switch1, 'no aaa-accounting enable')
SetCmd(switch1, 'no radius-server authentication host ' + Radius_server)
SetCmd(switch1, 'no radius-server accounting host ' + Radius_server)

CMDKillFirefox(sta1)
# end
printTimer(testname, 'End')
