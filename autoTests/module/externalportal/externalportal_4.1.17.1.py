#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.17.1.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.17.1	客户端从开启portal的 network切换到没有开启portal的网络
# 测试目的：客户端在开启portal认证和没有开启portal认证的网络之间切换时功能正常
# 测试描述：
# 1.	STA1连接到network1可以成功进行portal认证
# 2.	STA1不主动断开网络直接连接network2，AC1上表项正常
# 3.	STA1再次连接到开启portal认证的network1可以正常进行portal认证
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

testname = 'TestCase externalportal_4.1.17.1'
avoiderror(testname)
printTimer(testname,'Start','Test sta switchover network that one have portal and another does not have portal')
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
    # 客户端STA1打开web页面访问1.1.1.1（该地址为变量web_ip）
    #预期
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 2','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    # operate
    # sta1打开1.1.1.1，并检查是否重定向到外置portal认证页面
    web = web_init(sta1_host)
    res1 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 2',res1)
    if res1 == 0:
        ################################################################################
        #Step 3
        #操作
        # 客户端STA1在推送出的重定向页面输入正确的用户名和密码进行认证
        # portal认证用户名：portal_username = ‘aaa’
        # portal认证密码：portal_password = ‘111
        #预期
        # STA1认证成功
        # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）。
        # STA1ping PC1可以ping通
        ################################################################################
        printStep(testname,'Step 3',\
                            'input correct username and password',\
                            'login successully')
        res1=res2=res3=1
        # operate
        res1 = exportal_login_withcheck(web,portal_username,portal_password)
        res2 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        #result
        printCheckStep(testname, 'Step 3',res1,res2,res3)
    # 关闭网页
    web_close(web)
###############################################################################
#Step 4
#操作
# 客户端STA1连接到Network_name2   
# 查看AC1上的CP列表
# 检查STA1是否可以上网
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端STA1获取到192.168.X.X(Dhcp_pool2)网段的地址。
# 通命令show wireless  client  status可查看到管理的SSID为 Network_name2     
# 通过命令show captive-portal  client  status查看不到任何表项  
# STA1ping PC1可以ping通 
################################################################################
printStep(testname,'Step 4',\
                    'sta1 connect to test2')
res1=res2=res3=res4=res5=1
#operate
#STA1关联 network2
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name2,checkDhcpAddress=Netcard_ipaddress_check2,bssid=ap1mac_type1_network2)
if res1 == 0:
    res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
    res3 = CheckSutCmd(switch1,'show wireless client status',\
                        check=[(sta1mac,Network_name2)],retry=1,waitflag=False)
    # AC1上检查不存在sta1的portal用户表项
    res4 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=10,waitflag=False)
    res5 = CheckPing(sta1,pc1_ipv4,mode='linux')
#result
printCheckStep(testname, 'Step 4',res1,res2,res3,res4,res5)
################################################################################
#Step 5
#操作
# 客户端STA1连接到Network_name1
# 查看AC1上的CP列表
# 检查STA1是否可以上网
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端STA1获取到192.168.X.X(Dhcp_pool1)网段的地址。
# 通过命令show captive-portal  aip status可以查看到STA1的表项，其中mac=STA1MAC
# 通过命令show captive-portal  client  status查看不到任何表项
# STA1无法ping通PC1
################################################################################
printStep(testname,'Step 5','STA1 connect to test1')
res1=res2=res3=res4=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res1 == 0:
    res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
    # 客户端ping free resource触发IP上报
    SetCmd(sta1,'ping',Radius_server,'-c 5')
    res3 = CheckSutCmd(switch1,'show captive-portal aip status',\
                        check=[(sta1mac)],retry=5,waitflag=False)
    # AC1上检查不存在sta1的portal用户表项
    res4 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
    res5 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res5 = 0 if res5 != 0 else 1
#result
printCheckStep(testname, 'Step 5',res1,res2,res3,res4,res5)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 6
    #操作
    # 客户端STA1打开web页面访问1.1.1.1（该地址为变量web_ip）
    #预期
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 6','sta1 open 1.1.1.1 and can redirect to portal auth page')
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
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
CMDKillFirefox(sta1)
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)

#end
printTimer(testname, 'End')