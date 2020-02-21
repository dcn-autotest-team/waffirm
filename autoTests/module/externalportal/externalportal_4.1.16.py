#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.16.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.16	客户端可以连续打开多个重定向页面
# 测试目的：AC1配置外置portal认证，客户端连接SSID后，可以连续打开多个重定向页面
# 测试描述：
# 1.	AC1上面配置外置portal认证，客户端连接SSID后，发起http请求后可以得到重定向页面。
# 2.	客户端STA1不认证，重新打开web页面输入任意ip地址进行重定向
# 3.	客户端STA1不认证，重新打开web页面输入任意ip地址进行重定向
# 4.	在重定向页面输入用户名密码可以正常进行portal认证
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.24
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase externalportal_4.1.16'
avoiderror(testname)
printTimer(testname,'Start','Test sta can be redirected to portal login page repeatedly')
################################################################################
#Step 1
#操作
#客户端STA1连接到网络Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端获取到192.168.X.X(Dhcp_pool1)网段的地址
################################################################################
printStep(testname,'Step 1','STA1 connect to test1')
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res1 == 0:
    res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
#result
printCheckStep(testname, 'Step 1',res1,res2)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 2
    #操作
    # 检查AC1是否放行STA1的流量
    #预期
    # STA1无法ping通PC1
    ################################################################################
    printStep(testname,'Step 2','STA1 ping pc1 failed')
    res1=1
    #operate
    # 检查sta1无法ping通pc1
    res1 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res1=0 if res1 !=0 else -1
    #result
    printCheckStep(testname, 'Step 2',res1)
    ################################################################################
    #Step 3
    #操作
    # 客户端STA1打开web页面访问1.1.1.1（该地址为变量web_ip）
    #预期
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 3','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    # operate
    # sta1打开1.1.1.1，并检查是否重定向到外置portal认证页面
    web1 = web_init(sta1_host)
    res1 = exportal_redirect_success(web1,web_ip)
    #result
    printCheckStep(testname, 'Step 3',res1)
    ################################################################################
    #Step 4
    #操作
    # 客户端STA1重新打开web页面访问1.1.1.1（该地址为变量web_ip）
    #预期
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 4','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    # operate
    for i in range(2):
        IdleAfter(5)
        # sta1打开1.1.1.1，并检查是否重定向到外置portal认证页面
        web2 = web_init(sta1_host)
        res1 = exportal_redirect_success(web2,web_ip)
        if res1 == 0:
            break
        web_close(web2)
    #result
    printCheckStep(testname, 'Step 4',res1)
    ################################################################################
    #Step 5
    #操作
    # 客客户端STA1再次打开web页面访问1.1.1.1（该地址为变量web_ip）
    #预期
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 5','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    # operate
    for i in range(2):
        IdleAfter(5)
        # sta1打开1.1.1.1，并检查是否重定向到外置portal认证页面
        web3 = web_init(sta1_host)
        res1 = exportal_redirect_success(web3,web_ip)
        if res1 == 0:
            break
        web_close(web3)
    #result
    printCheckStep(testname, 'Step 5',res1)

    ################################################################################
    #Step 6
    #操作
    # 客户端STA1在推送出的多个重定向页面中选择任意一个输入正确的用户名和密码进行认证
    # portal认证用户名：portal_username = 'aaa'
    # portal认证密码：portal_password = '111
    # 检查AC1是否放行STA1的流量
    #预期
    # STA1认证成功
    # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）。
    # STA1ping PC1可以ping通
    ################################################################################
    printStep(testname,'Step 6',\
                        'input correct username and password',\
                        'login successully')
    res1=res2=res3=1
    # operate
    IdleAfter(5)
    web = random.choice([web1,web2,web3])
    exportal_login_withcheck(web,portal_username,portal_password)
    res1 = CheckSutCmd(switch1,'show captive-portal client status',\
                                check=[(sta1mac)],retry=5,waitflag=False)
    res2 = CheckPing(sta1,pc1_ipv4,mode='linux')
    #result
    printCheckStep(testname, 'Step 6',res1,res2)
    # 退出登陆
    portal_logout_withcheck(web)
################################################################################
#Step 7
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 7',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

web_close(web1)
web_close(web2)
web_close(web3)
CMDKillFirefox(sta1)
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)
#end
printTimer(testname, 'End')