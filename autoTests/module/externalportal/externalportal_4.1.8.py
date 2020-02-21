#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.8.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.8	block功能验证
# 测试目的：外置portal场景下，当阻塞Captive Portal配置的所有通信，已经通过portal认证的用户被强制下线，然后与无线认证接入点解关联，未通过portal认证的客户端不能被重定向和认证，并且其与无线控制器和无线认证接入点解关联。
# 测试描述：
# 1.	STA1和STA2都关联到无线网络
# 2.	STA1进行portal认证，STA2不进行portal认证
# 3.	阻塞CP流量
# 4.	检查STA1和STA2跟网络的连接情况
# 5.	取消阻塞CP流量
# 6.	STA1和STA2再次连接网络
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

testname = 'TestCase externalportal_4.1.8'
avoiderror(testname)
printTimer(testname,'Start','Test portal block function')

###############################################################################
#Step 1
#操作
# 客户端STA1连接到网络Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端STA1获取到192.168.X.X(Dhcp_pool1)网段的地址
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
###############################################################################
#Step 2
#操作
# 客户端STA2连接到网络Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端STA2获取到192.168.X.X(Dhcp_pool1)网段的地址
################################################################################
printStep(testname,'Step 1','STA2 connect to test1')
res3=res4=1
#operate
#STA1关联 network1
res3 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res3 == 0:
	res4 = CheckWirelessClientOnline(switch1,sta2mac,'online')
#result
printCheckStep(testname, 'Step 2',res3,res4)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1+res3
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 3
    #操作
    # 客户端STA1打开web页面访问1.1.1.1
    #
    #预期
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 3','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    #operate
    web = web_init(sta1_host)
    res1 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 3',res1)
    if res1 == 0:
        ################################################################################
        #Step 4
        #操作
        # 客户端STA1在推送出的重定向页面输入正确的用户名和密码进行认证
        # portal认证用户名：portal_username = 'aaa'
        # portal认证密码：portal_password = '111
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
    web_close(web)
    ################################################################################
    #Step 5
    #操作
    # 阻塞Captive Portal的通信
    # AC1(config)#captive-portal         
    # AC1(config-cp)#configuration 1                  
    # AC1(config-cp-instance)#block  
    #预期
    # 配置成功
    # AC1上在实例configuration1下通过
    # show running-config  current-mode 可以查看到block的命令 
    ################################################################################
    printStep(testname,'Step 5','block captive portal')
    res1=1
    # operate
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'configuration 1')
    SetCmd(switch1,'block')
    IdleAfter(3)
    data = SetCmd(switch1,'show run c')
    res1 = CheckLine(data,'block')
    #result
    printCheckStep(testname, 'Step 5',res1)
    ################################################################################
    #Step 6
    #操作
    # 检查客户端STA1、STA2跟网络Network_name1的连接状态
    #预期
    # 客户端STA1、STA2跟网络Network_name1的连接断开了
    # AC1上通过show captive-portal  client  status和show wireless  client  status查看不到表项
    # STA1无法ping通PC1
    ################################################################################
    printStep(testname,'Step 6','the connection between sta and AP break')
    res1=res2=res3=res4=res5=1
    res4=0
    # opertate
    res1 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                        check=[(sta1mac)],retry=10,waitflag=False)
    res2 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                        check=[(sta2mac)],retry=10,waitflag=False)
    res3 = CheckWirelessClientOnline(switch1,sta1mac,'offline')
    res4 = CheckWirelessClientOnline(switch1,sta2mac,'offline')
    res5 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res5 = 0 if res5 != 0 else 1
    #result
    printCheckStep(testname, 'Step 6',res1,res2,res3,res4,res5)
################################################################################
#Step 7
#操作
# 取消阻塞Captive Portal的通信
# AC1(config)#captive-portal         
# AC1(config-cp)#configuration 1                  
# AC1(config-cp-instance)#no block  
#预期
# 配置成功
# AC1上在实例configuration1下通过
# show running-config  current-mode 查看不到block的命令
################################################################################
printStep(testname,'Step 7','cancel block captive portal')
res1=1
# operate
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'no block')
IdleAfter(3)
data = SetCmd(switch1,'show run c')
res1 = CheckLine(data,'block')
res1 = 0 if res1 != 0 else 1
#result
printCheckStep(testname, 'Step 7',res1)
###############################################################################
#Step 8
#操作
# 客户端STA1连接到网络Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端STA1获取到192.168.X.X(Dhcp_pool1)网段的地址
################################################################################
printStep(testname,'Step 8','STA1 connect to test1')
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res1 == 0:
	res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
#result
printCheckStep(testname, 'Step 8',res1,res2)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 9
    #操作
    # 客户端STA1打开web页面访问1.1.1.1
    #
    #预期
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 9','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    #operate
    web = web_init(sta1_host)
    res1 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 9',res1)
    if res1 == 0:
        ################################################################################
        #Step 10
        #操作
        # 客户端STA1在推送出的重定向页面输入正确的用户名和密码进行认证
        # portal认证用户名：portal_username = 'aaa'
        # portal认证密码：portal_password = '111
        #预期
        # STA1认证成功
        # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）。
        # STA1ping PC1可以ping通
        ################################################################################
        printStep(testname,'Step 10',\
                            'input correct username and password',\
                            'login successully')
        res1=res2=res3=1
        # operate
        res1 = exportal_login_withcheck(web,portal_username,portal_password)
        res2 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        #result
        printCheckStep(testname, 'Step 10',res1,res2,res3)
        # 退出登陆
        portal_logout_withcheck(web)
    # 关闭网页
    web_close(web)
################################################################################
#Step 11
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 11',\
          'Recover initial config for switches.')

#operate
# sta解关联  
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)
CMDKillFirefox(sta1)

CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta2mac)],retry=10,waitflag=False)
#end
printTimer(testname, 'End')