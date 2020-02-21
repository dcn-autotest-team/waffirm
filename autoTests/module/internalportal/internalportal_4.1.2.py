#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# internal_portal_4.1.2.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.2	内置portal基本功能测试
# 测试目的：AC1配置内置portal认证，客户端连接SSID后，可以进行内置portal认证。
# 测试描述：
# 1、	AC1上面配置内置portal认证，客户端连接SSID后，发起http请求后可以得到重定向页面。
# 2、	STA1在认证页面填写错误的用户名和密码不能通过认证
# 3、	STA1在认证页面填写正确的用户名和密码能够通过认证
# 4、	STA1通过认证后可以主动下线
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.8
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase internalportal_4.1.2'
avoiderror(testname)
printTimer(testname,'Start','Test internal portal')
###############################################################################
#Step 1(删除原方案step1，合并原方案 step2，step3)
#操作
# 客户端STA1连接到网络Network_name1
# 检查AC1是否放行STA1的流量
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端获取到192.168.X.X（Dhcp_pool1）网段的地址
# STA1无法ping通PC1
################################################################################
printStep(testname,'Step 1','STA1 connect to test1 and ping pc1 failed')
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
# 检查sta1无法ping通pc1
res2 = CheckPing(sta1,pc1_ipv4,mode='linux')
res2=0 if res2 !=0 else -1
#result
printCheckStep(testname, 'Step 1',res1,res2)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 2
    #操作
    # 客户端STA1打开web页面访问1.1.1.1
    #
    #预期
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 2','sta1 open 1.1.1.1 and can redirect to internal portal auth page')
    res1=1
    #operate
    web = web_init(sta1_host)
    res1 = inportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 2',res1)
    ################################################################################
    #Step 3(原方案step6)
    #操作
    # 在推送出的重定向页面中输入错误的用户名和密码进行认证 aaaa/1111
    # AC1上查看CP列表
    # STA1尝试pingPC1
    #预期
    # 提示用户名或密码错误，无法认证成功
    # 通过show captive-portal  client  status命令查看没有CP client列表
    # STA1无法ping通PC1
    ################################################################################
    printStep(testname,'Step 3',
                        'input wrong username and password',
                        'login failed')

    #operate
    # 登陆portal页面
    res1 = inportal_login_withcheck(web,'zzzzzzzz','11111')
    res1 = 0 if res1 != 0 else 1
    # AC1上检查不存在sta1的portal用户表项
    res2 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',
                                    check=[(sta1mac)],retry=2,waitflag=False)
    # 检查sta1无法ping通pc1
    res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res3=0 if res3 !=0 else -1                                
    #result
    printCheckStep(testname, 'Step 3',res1,res2,res3)
    # 关闭网页
    web_close(web)
    ################################################################################
    #Step 4(原方案step7)
    #操作
    # 重新输入正确的用户名和密码进行认证
    # portal认证用户名：portal_username = 'aaa'
    # portal认证密码：portal_password = '111' 
    # AC1上查看CP列表
    # 检查AC1是否放行STA1的流量
    #预期
    # 提示用户认证成功，通过show captive-portal  client  status命令查看CP client列表，
    # 显示出STA1的信息（“MAC Address”显示“STA1MAC”）
    # STA1可以ping通PC1
    ################################################################################
    printStep(testname,'Step 4',
                        'input correct username and password',
                        'login successully')
    res1=res2=res3=1
    # operate
    web = web_init(sta1_host)
    resa = inportal_redirect_success(web,web_ip)
    if resa == 0:
        res1 = inportal_login_withcheck(web,portal_username,portal_password)
        res2 = CheckSutCmd(switch1,'show captive-portal client status',
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
    #result
    printCheckStep(testname, 'Step 4',res1,res2,res3)
    ################################################################################
    #Step 5(原方案step9)
    #操作
    # 在推送出来的认证成功页面点击“下线”
    # AC1上查看CP列表
    # STA1尝试ping PC1
    #预期
    # 页面提示“成功下线”；
    # 通过show captive-portal  client  status命令查看没有CP client列表
    # STA1无法ping通PC1
    ################################################################################
    printStep(testname,'Step 5','sta1 logout')
    # opertate
    # 退出登陆
    res1 = portal_logout_withcheck(web)
    # AC1上检查不存在sta1的portal用户表项
    res2 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',
                                    check=[(sta1mac)],retry=10,waitflag=False)
    # 检查sta1无法ping通pc1
    res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res3=0 if res3 !=0 else -1  
    #result
    printCheckStep(testname, 'Step 5',res1,res2,res3)
    # 关闭网页
    web_close(web)
################################################################################
#Step 6(原方案step10)
#操作
# STA1断开网络，等待30秒
#预期
# 断开无线成功
# show wireless  client  status查看表项为空“No clients associated to APs”
################################################################################
printStep(testname,'Step 6','sta1 disconnect network1')
# opertate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
IdleAfter(10)
res1 = CheckSutCmdWithNoExpect(switch1,'show wireless client status',
                                check=[(sta1mac)],retry=20,waitflag=False)
#result
printCheckStep(testname, 'Step 6',res1)
################################################################################
#Step 7
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 7',
          'Recover initial config for switches.')

#operate
CMDKillFirefox(sta1)
#end
printTimer(testname, 'End')