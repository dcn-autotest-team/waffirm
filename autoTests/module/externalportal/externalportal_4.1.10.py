#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.10.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.10	内置portal切换到外置portal功能验证
# 测试目的：验证AC从内置portal认证切换到外置portal认证后，客户端连接网络能够正常进行外置portal认证
# 测试描述：
# 1.	AC1上从外置portal认证切换到内置portal认证
# 2.	STA1连接网络后可以正常进行内置portal认证
# 3.	再次修改portal认证为外置portal认证
# 4.	STA1连接网络后可以正常进行外置portal认证
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.21
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase externalportal_4.1.10'
avoiderror(testname)
printTimer(testname,'Start','Test external portal convert to internal portal')
###############################################################################
#Step 1
#操作
# AC1上设置portal认证为内置portal认证                                                                                                                     
# AC1(config)#captive-portal                                                                                                                                                                                                           
# AC1(config-cp)#authentication-type internal
#预期
# 设置成功
# AC1上通过命令show captive-portal  status                                                                                       
# 显示Authentication Type 为Internal
################################################################################
printStep(testname,'Step 1','config internal portal')
res1=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'authentication-type internal')
data = SetCmd(switch1,'show captive-portal status')
res1 = CheckLine(data,'Authentication','Internal')
#result
printCheckStep(testname, 'Step 1',res1)
###############################################################################
#Step 2
#操作
# 客户端STA1连接到网络Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端STA1获取到192.168.X.X(Dhcp_pool1)网段的地址
################################################################################
printStep(testname,'Step 2','STA1 connect to test1')
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res1 == 0:
	res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
#result
printCheckStep(testname, 'Step 2',res1,res2)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag): 
    ################################################################################
    #Step 3
    #操作
    # 客户端STA1打开web页面访问1.1.1.1（该地址为变量web_ip）
    #预期
    # STA1上可以看到重定向页面，并且该重定向页面为内置portal的重定向页面 
    # STA1上抓包，可以查看到重定向地址头部为http://1.1.1.11:8080/captive_portal格式
    # （其中1.1.1.11为AC1的无线接口ip地址，是变量StaticIpv4_ac1）
    ################################################################################
    printStep(testname,'Step 3','sta1 open 1.1.1.1 and can redirect to internal portal auth page')
    res1=1
    # operate
    # sta1打开1.1.1.1，并检查是否重定向到内置portal认证页面
    web = web_init(sta1_host)
    res1 = inportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 3',res1)
    if res1 == 0:
        ################################################################################
        #Step 4
        #操作
        # 客户端STA1在推送出的重定向页面输入正确的用户名和密码进行认证
        # portal认证用户名：portal_username = ‘aaa’
        # portal认证密码：portal_password = ‘111
        #预期
        # STA1认证成功
        # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）。
        # STA1ping PC1可以ping通
        ################################################################################
        printStep(testname,'Step 4',\
                            'input correct username and password',\
                            'login successully')
        res1=res2=res3=1
        # operate
        res1 = inportal_login_withcheck(web,portal_username,portal_password)
        res2 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        #result
        printCheckStep(testname, 'Step 4',res1,res2,res3)
    # 关闭网页
    web_close(web)
    ###############################################################################
    #Step 5
    #操作
    # AC1上设置portal认证为外置portal认证 
    # AC1(config)#captive-portal                                                                                                       
    # AC1(config-cp)#authentication-type external
    #预期
    # 设置成功
    # AC1上通过命令show captive-portal  status                                                                                       
    # 显示Authentication Type 为External 
    # STA1下线
    # 通过show captive-portal  client  status命令查看CP client列表为空
    # STA1无法ping通PC1
    ################################################################################
    printStep(testname,'Step 5','config external portal')
    res1=res2=res3=1
    #operate
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'authentication-type external')
    data = SetCmd(switch1,'show captive-portal status')
    res1 = CheckLine(data,'Authentication','External')
    res2 = CheckSutCmdWithNoExpect(switch1,'show captive-portal status ',\
                                    check=[(sta1mac)],retry=10,waitflag=False)
    res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res3 = 0 if res3 != 0 else 1
    #result
    printCheckStep(testname, 'Step 5',res1,res2,res3)
    ################################################################################
    #Step 6
    #操作
    # 客户端STA1打开web页面访问1.1.1.1（该地址为变量web_ip）
    #预期
    # STA1上可以看到重定向页面，并且该重定向页面为外置portal的重定向页面 
    # STA1上抓包，可以查看到重定向地址为：http://192.168.10.101/a79.htm?wlanuserip=192.168.70.3&wlanacname=123&ssid=test1&apmac=00-03-0f-37-92-a0&usermac=58-94-6b-1a-6b-34&srcurl=http://1.2.3.4/
    # （上面重定向地址有部分是变量：192.168.10.101为portal服务器地址；192.168.70.3为客户端实际ip地址；
    # 123为实际实例下配置的ac name；
    # test1是连接的ssid的名称；
    # 00-03-0f-37-92-a0为AP1的mac地址
    # 58-94-6b-1a-6b-34为客户端STA1mac）
    ################################################################################
    printStep(testname,'Step 6','sta1 open 1.1.1.1 and can redirect to external portal auth page')
    res1=1
    # operate
    # sta1打开1.1.1.1，并检查是否重定向到外置portal认证页面
    web = web_init(sta1_host)
    res1 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 6',res1)
    if res1 == 0:
        ################################################################################
        #Step 7
        #操作
        # 客户端STA1在推送出的重定向页面输入正确的用户名和密码进行认证
        # portal认证用户名：portal_username = ‘aaa’
        # portal认证密码：portal_password = ‘111
        #预期
        # STA1认证成功
        # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）。
        # STA1ping PC1可以ping通
        ################################################################################
        printStep(testname,'Step 7',\
                            'input correct username and password',\
                            'login successully')
        res1=res2=res3=1
        # operate
        res1 = exportal_login_withcheck(web,portal_username,portal_password)
        res2 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        #result
        printCheckStep(testname, 'Step 7',res1,res2,res3)
        # 退出登陆
        portal_logout_withcheck(web)
    # 关闭网页
    web_close(web)
################################################################################
#Step 8
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 8',\
          'Recover initial config for switches.')

#operate
# sta1断开连接
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
CMDKillFirefox(sta1)
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)
#end
printTimer(testname, 'End')