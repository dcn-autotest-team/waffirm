#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# internalportal_4.1.5.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.5	mac portal认证
# 测试目的：验证开启mac portal认证后，被添加到mac portal known表项中的客户端可以直接通过认证
# 测试描述：
# 1、	开启mac portal认证功能
# 2、	STA1的mac添加到mac portal known表项，STA2的mac不添加到mac portal know列表
# 3、	STA1和STA2都连接到无线网络，查看STA1可以直接上网，STA2需要输入用户名密码认证后才能上网
# 4、	关闭mac portal功能后，STA1需要输入用户名密码认证后才能上网
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

testname = 'TestCase internalportal_4.1.5'
avoiderror(testname)
printTimer(testname,'Start','Test mac authentication')

###############################################################################
#Step 1
#操作
# 开启mac portal功能，STA1的mac添加到mac portal know列表
# AC1(config)#captive-portal                                                                                                       
# AC1(config-cp)#mac-portal known-client STA1MAC                                                                                                                                                                                                                                                                                                                                                                                                 
# AC1(config-cp)#configuration 1                                                                                                                                                               
# AC1(config-cp-instance)#mac-portal authentication 
#预期
# 配置成功。
# AC上show captive-portal  configuration 1 status显示Mac-portal Authentication状态为Enable
# AC上show run可以查看到命令
# mac-portal known-client STA1MAC
################################################################################
printStep(testname,'Step 1','add sta1mac to known-client list')
res1=res2=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'mac-portal known-client',sta1mac)
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'mac-portal authentication')
data1 = SetCmd(switch1,'show captive-portal configuration 1 status')
res1 = CheckLine(data1,'Mac-portal Authentication','Enable')
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
data2 = SetCmd(switch1,'show run c')
res2 = CheckLine(data2,'mac-portal known-client',sta1mac)
#result
printCheckStep(testname, 'Step 1',res1,res2)
################################################################################
#Step 2
#操作
# 客户端STA1和STA2都连接到网络Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端STA1和STA2都获取到192.168.X.X（Dhcp_pool1）网段的地址。
################################################################################
printStep(testname,'Step 2','STA1,STA2 connect to test1')
res1=res2=res3=res4=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res1 == 0:
    res3 = CheckWirelessClientOnline(switch1,sta1mac,'online')
if res2 == 0:
    res4 = CheckWirelessClientOnline(switch1,sta2mac,'online') 
#result
printCheckStep(testname, 'Step 2',res1,res2,res3,res4)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1+res2
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 3
    #操作
    # STA1已经通过认证，而客户端STA2没有通过认证
    #预期
    # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）,
    # 列表中没有STA2的信息
    # STA1ping PC1可以ping通
    # STA2无法ping通PC1
    ################################################################################
    printStep(testname,'Step 3',\
                        'STA1 ping pc1 successully',\
                        'STA2 ping pc1 failed')
    res1=res2=res3=res4=1
    #operate
    # 查看CP client列表，存在出STA1
    res1 = CheckSutCmd(switch1,'show captive-portal client status',\
                                check=[(sta1mac)],retry=5,waitflag=False)
    # 查看CP client列表，不存在出STA2
    res2 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                        check=[(sta2mac)],retry=1,waitflag=False)
    res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res4 = CheckPing(sta2,pc1_ipv4,mode='linux')
    res4 = 0 if res4 != 0 else 1
    #result
    printCheckStep(testname, 'Step 3',res1,res2,res3,res4)
    ################################################################################
    #Step 4
    #操作
    # STA2访问web_ip，使用正确的用户名和密码登录
    # portal认证用户名：portal_username = 'aaa'
    # portal认证密码：portal_password = '111'
    #预期
    # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1和STA2的信息，STA1和STA2ping PC1都可以ping通
    ################################################################################
    printStep(testname,'Step 4',\
                        'sta2 open http://1.1.1.1',\
                        'sta2 input correct username and password',\
                        'sta2 login successully')
    res1=res2=res3=1
    # operate
    web = web_init(sta2_host)
    res1 = inportal_redirect_success(web,web_ip)
    if res1 == 0:
        res2 = inportal_login_withcheck(web,portal_username,portal_password)
    res3 = CheckSutCmd(switch1,'show captive-portal client status',\
                                check=[(sta1mac),(sta2mac)],retry=5,waitflag=False)
                                
    #result
    printCheckStep(testname, 'Step 4',res1,res2,res3)
    # 关闭网页
    web_close(web)
################################################################################
#Step 5
#操作
# STA1和STA2断开跟网络Network_name1的连接
#预期
# STA1和STA2断开网络成功
# AC1上show wireless client status看不到用户列表
################################################################################
printStep(testname,'Step 5','sta1,sta2 disconnect test1')
res1=res2=1
# opertate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)
res1 = CheckWirelessClientOnline(switch1,sta1mac,'offline')
res2 = CheckWirelessClientOnline(switch1,sta2mac,'offline')
#result
printCheckStep(testname, 'Step 5',res1,res2)
################################################################################
#Step 6
#操作
# 关闭mac portal功能，从mac portal know表项中删除STA1的mac信息
# AC1(config)#captive-portal   
# AC1(config-cp)#no mac-portal known-client STA1MAC                                                                                                        
# AC1(config-cp)#configuration 1                                                                                                                                                              
# AC1(config-cp-instance)#no mac-portal authentication  
#预期
# 配置成功。
# AC上show captive-portal  configuration 1 status显示Mac-portal Authentication状态为Disable
# AC上面show run无法查看到命令：
# mac-portal known-client STA1MAC
################################################################################
printStep(testname,'Step 6','no mac-portal authentication')
res1=res2=1
# operate
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'no mac-portal known-client',sta1mac)
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'no mac-portal authentication')
data1 = SetCmd(switch1,'show captive-portal configuration 1 status')
res1 = CheckLine(data1,'Mac-portal Authentication','Disable')
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
data2 = SetCmd(switch1,'show run c')
res2 = CheckLine(data2,'mac-portal known-client')
res2 = 0 if res2 != 0 else 1
#result
printCheckStep(testname, 'Step 6',res1,res2)
################################################################################
#Step 7
#操作
# STA1连接AP1的Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端STA1获取到Dhcp_pool1网段的地址。
# STA1ping PC1无法ping通
################################################################################
printStep(testname,'Step 7','STA1 connect to test1 and ping pc1 failed')
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
# 检查sta1无法ping通pc1
res2 = CheckPing(sta1,pc1_ipv4,mode='linux')
res2=0 if res2 !=0 else -1
#result
printCheckStep(testname, 'Step 7',res1,res2)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 8
    #操作
    # STA1打开web页面访问web_ip，使用正确的用户名和密码登录
    # portal认证用户名：portal_username = 'aaa'
    # portal认证密码：portal_password = '111'
    #预期
    # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息，STA1 ping PC1可以ping通
    ################################################################################
    printStep(testname,'Step 8','sta1 open 1.1.1.1 and can redirect to portal auth page',\
                                'input correct username and password',\
                                'login successully')
    res1=res2=res3=res4=1
    #operate
    web = web_init(sta1_host)
    res1 = inportal_redirect_success(web,web_ip)
    if res1 == 0:
        res2 = inportal_login_withcheck(web,portal_username,portal_password)
        res3 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res4 = CheckPing(sta1,pc1_ipv4,mode='linux')
    #result
    printCheckStep(testname, 'Step 8',res1,res2,res3,res4)
    # 退出登陆并关闭网页
    portal_logout_withcheck(web)
    web_close(web)
################################################################################
#Step 9
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 9',\
          'Recover initial config for switches.')

#operate
# sta1断开网络
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
CMDKillFirefox(sta1)
CheckSutCmdWithNoExpect(switch1,'show wireless client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=1,waitflag=False)
#end
printTimer(testname, 'End')