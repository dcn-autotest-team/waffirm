#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.19.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.19	客户端关联到非默认configuration 1下的网络可以认证成功
# 测试目的：客户端关联到任何一个configuration下（非默认configuration 1），填写正确的用户名和密码后，能够通过认证
# 测试描述：
# 1.	建立新的network并且绑定到新添加的实例下
# 2.	客户端STA1连接网络network1可以进行portal认证
# 3.	客户端STA2连接网络network2可以进行portal认证
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.25
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase externalportal_4.1.19'
avoiderror(testname)
printTimer(testname,'Start','Test sta can auth successully when not using configuration 1')
################################################################################
#Step 1
#操作
# 添加另外一个实例2，将network2绑定到实例2下
# AC1(config-cp)#configuration 2
# AC1(config-cp-instance)#enable                                                                                                   
# AC1(config-cp-instance)#radius accounting                                                                                        
# AC1(config-cp-instance)#protocol http                                                                                            
# AC1(config-cp-instance)#radius-acct-server wlan                                                                                  
# AC1(config-cp-instance)#radius-auth-server wlan
# AC1(config-cp-instance)#redirect attribute url-after-login enable
# AC1(config-cp-instance)#redirect attribute ssid enable                                                                                                    
# AC1(config-cp-instance)#redirect attribute apmac enable                                                                                                   
# AC1(config-cp-instance)#redirect attribute usermac enable
# AC1(config-cp-instance)#ac-name 0100.0010.010.01                                                                                 
# AC1(config-cp-instance)#redirect url-head http:// Portal_server /a79.htm                                                          
# AC1(config-cp-instance)#portal-server ipv4 eportal                                                                               
# AC1(config-cp-instance)#free-resource 1                                                                                          
# AC1(config-cp-instance)#interface  ws-network  2 
#预期
# 添加成功
# AC1上通过命令show captive-portal configuration 2 status可以看到实例2 的相关信息
################################################################################
printStep(testname,'Step 1','Bind network2 to captive-portal configuration 1')
res1=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 2')
SetCmd(switch1,'enable')
SetCmd(switch1,'radius accounting ')
SetCmd(switch1,'protocol http')
SetCmd(switch1,'radius-acct-server wlan')
SetCmd(switch1,'radius-auth-server wlan')
SetCmd(switch1,'redirect attribute url-after-login enable')
SetCmd(switch1,'redirect attribute ssid enable')
SetCmd(switch1,'redirect attribute nas-ip enable')
SetCmd(switch1,'redirect attribute apmac enable')
SetCmd(switch1,'redirect attribute usermac enable')
SetCmd(switch1,'ac-name 0100.0010.0'+EnvNo+'0.01')
SetCmd(switch1,'redirect url-head http://192.168.10.101/a79.htm')
SetCmd(switch1,'portal-server ipv4 eportal')
SetCmd(switch1,'free-resource 1')
SetCmd(switch1,'interface ws-network 2')
# check
data=SetCmd(switch1,'show run c')
#result
printCheckStep(testname, 'Step 1',0)
################################################################################
#Step 2
#操作
#客户端STA1连接到网络Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端获取到192.168.X.X(Dhcp_pool1)网段的地址
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
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 3','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    # operate
    # sta1打开1.1.1.1，并检查是否重定向到外置portal认证页面
    web = web_init(sta1_host)
    res1 = exportal_redirect_success(web,web_ip)
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
        res1 = exportal_login_withcheck(web,portal_username,portal_password)
        res2 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        #result
        printCheckStep(testname, 'Step 4',res1,res2,res3)
    # 关闭网页
    res = web_close(web)
    if res['status'] != True:
        printRes(res)
        CMDKillFirefox(sta1)
###############################################################################
#Step 5
#操作
# 客户端STA2连接到Network_name2   
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端STA2获取到192.168.X.X(Dhcp_pool2)网段的地址
################################################################################
printStep(testname,'Step 5',\
                    'sta2 connect to test2')
res1=res2=res3=res4=1
#operate
res1 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,checkDhcpAddress=Netcard_ipaddress_check2,bssid=ap1mac_type1_network2)
if res1 == 0:
    res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
#result
printCheckStep(testname, 'Step 5',res1,res2)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 6
    #操作
    # 客户端STA2打开web页面访问1.1.1.1（该地址为变量web_ip）
    #预期
    # STA2上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 6','sta2 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    # operate
    # sta1打开1.1.1.1，并检查是否重定向到外置portal认证页面
    web = web_init(sta2_host)
    res1 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 6',res1)
    if res1 == 0:
        ################################################################################
        #Step 7
        #操作
        # 输入正确的用户名和密码进行认证
        # portal认证用户名：portal_username = 'aaa'
        # portal认证密码：portal_password = '111' 
        # 查看AC1上的CP列表
        # 检查STA1、STA2是否可以上网 
        #预期
        # 提示用户认证成功，通过show captive-portal  client  status命令查看CP client列表，显示出STA1和STA2的信息（“MAC Address”显示“STA1MAC和STA2MAC”）
        # STA1和STA2都可以ping通PC1
        ################################################################################
        printStep(testname,'Step 7',\
                            'input correct username and password',\
                            'login successully')
        res1=res2=res3=1
        # operate
        res1 = exportal_login_withcheck(web,portal_username,portal_password)
        res2 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac),(sta2mac)],retry=5,waitflag=False)
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        res4 = CheckPing(sta2,pc1_ipv4,mode='linux')
        #result
        printCheckStep(testname, 'Step 7',res1,res2,res3,res4)
    # 关闭网页
    res = web_close(web)
    if res['status'] != True:
        printRes(res)
        CMDKillFirefox(sta2)
################################################################################
#Step 8
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 8',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'no configuration 2')
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',
                        check=[(sta1mac)],retry=20,waitflag=False)
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',
                        check=[(sta2mac)],retry=20,waitflag=False)
#end
printTimer(testname, 'End')