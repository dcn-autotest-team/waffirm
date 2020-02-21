#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# internal_portal_4.1.33.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# 4.1.33	CP verification local本地用户认证
# 测试目的：验证STA可以使用本地用户进行内置portal认证
# 测试描述：
# 1、	配置verification local 以及local user
# 2、	STA使用local user认证成功
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.10
#*******************************************************************************

#Package

#Global Definition
localuser = 'test1234'
localpwd = 'test1234'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase internalportal_4.1.33'
avoiderror(testname)
printTimer(testname,'Start','Test verification local')
################################################################################
#Step 1
#操作
# AC1上开启verification local功能
# AC1(config)#captive-portal                                                                                                          
# AC1(config-cp)#configuration 1                                                                                                      
# AC1(config-cp-instance)#verification local
# AC1配置local user：
# AC1(config-cp)#user test1234
# AC1 (config-cp-local-user)#password test1234
# AC1 (config-cp-local-user)#group 1
# AC1(config-cp)#configuration 1
# AC1(config-cp-instance)#group 1
#预期
# 配置成功
# AC1上通过命令show captive-portal  configuration  1 status查看：
# Verification Mode.............................. Local
# Group Name..................................... 1
################################################################################
printStep(testname,'Step 1','Config verification local')
res1=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'verification local')
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'user',localuser)
SetCmd(switch1,'password',localpwd)
SetCmd(switch1,'group 1')
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'group 1')
# check
IdleAfter(5)
data=SetCmd(switch1,'show captive-portal configuration 1 status')
res1 = CheckLineList(data,[('Verification Mode','Local'),('Group Name','1')])
#result
printCheckStep(testname, 'Step 1',res1)
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
    res1 = inportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 3',res1)
    if res1 == 0:
        ################################################################################
        #Step 4
        #操作
        # 输入正确的用户名和密码进行认证
        # portal认证用户名：test1234
        # portal认证密码：test1234 
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
        res1 = inportal_login_withcheck(web,localuser,localpwd)
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
#STA1断开与网络Network_name1的连接
#预期
#断开网络成功
# 通过show wireless client status查看不到任何表项
################################################################################
printStep(testname,'Step 5','sta1 disconnect network1')
res1=1
# operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
IdleAfter(10)
res1 = CheckSutCmdWithNoExpect(switch1,'show wireless client status',
                               check=[(sta1mac)],retry=20,waitflag=False)
#result
printCheckStep(testname, 'Step 5',res1)
################################################################################
#Step 6
#操作
#等待30s，STA1连接到AP1的Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端获取到192.168.X.X(Dhcp_pool1)网段的地址
################################################################################
printStep(testname,'Step 6','STA1 connect to test1')
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res1 == 0:
    res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
#result
printCheckStep(testname, 'Step 6',res1,res2)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 7
    #操作
    # 客户端STA1打开web页面访问1.1.1.1（该地址为变量web_ip）
    #预期
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 7','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    # operate
    # sta1打开1.1.1.1，并检查是否重定向到外置portal认证页面
    web = web_init(sta1_host)
    res1 = inportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 7',res1)
    if res1 == 0:
        ################################################################################
        #Step 8
        #操作
        # 输入错误的用户名和密码进行认证
        # portal认证用户名：test123
        # portal认证密码：test123
        #预期
        # 提示用户认证失败，通过show captive-portal  client  status命令查看CP client列表，没有任何表项
        # STA1不能够ping通pc1_ipv4
        ################################################################################
        printStep(testname,'Step 8',\
                            'input wrong username and password',\
                            'login failed')

        #operate
        # 登陆portal页面
        res1 = inportal_login_withcheck(web,'test123','test123')
        res1 = 0 if res1 != 0 else 1
        # AC1上检查不存在sta1的portal用户表项
        res2 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                        check=[(sta1mac)],retry=2,waitflag=False)
        # 检查sta1无法ping通pc1
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        res3=0 if res3 !=0 else -1                                
        #result
        printCheckStep(testname, 'Step 8',res1,res2,res3)
        # 关闭网页
        web_close(web)

################################################################################
#Step 9(合并原方案step9,step10)
#操作
#恢复默认配置
# AC1(config)#captive-portal                                                                                                          
# AC1(config-cp)#configuration 1                                                                                                      
# AC1(config-cp-instance)#verification radius
# AC1(config-cp-instance)#no group
# AC1(config-cp-instance)#exit
# AC1(config-cp)#user test1234
# AC1 (config-cp-local-user)#no password
# AC1 (config-cp-local-user)#no group
# AC1 (config-cp-local-user)#exit
# AC1 (config-cp)#no user test1234
# AC1(config-cp)#
################################################################################
printStep(testname,'Step 9',\
          'Recover initial config for switches.')

#operate
# sta1解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
CMDKillFirefox(sta1)
# 恢复AC1配置
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'no group')
SetCmd(switch1,'verification radius')
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'user',localuser)
SetCmd(switch1,'no password')
SetCmd(switch1,'no group',promotePatten='Y/N',promoteTimeout=10)
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'no user',localuser,timeout=2)
SetCmd(switch1,'y')
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)

#end
printTimer(testname, 'End')