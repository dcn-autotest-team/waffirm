#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# internal_portal_4.1.35.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# 4.1.35	切换内置portal的chap和pap鉴权模式
# 测试目的：验证内置portal的chap/pap鉴权模式都可以正常工作
# 测试描述：
# 1、	配置authentication-mode为pap模式
# 2、	STA进行内置portal认证，输入正确的用户名密码认证成功
# 3、	配置authentication-mode为chap模式
# 4、	STA进行内置portal认证，输入正确的用户名密码认证成功
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.10
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase internalportal_4.1.35'
avoiderror(testname)
printTimer(testname,'Start','Test authentication-mode pap and chap')
################################################################################
#Step 1
#操作
# AC1配置pap：
# captive-portal                                                                                                          
# authentication-mode pap
#预期
# 配置成功
# AC1上show captive-portal status显示：
# Authentication Mode............................ Pap
################################################################################
printStep(testname,'Step 1','Config authentication-mode pap')
res1=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'authentication-mode pap')
# check
IdleAfter(5)
data=SetCmd(switch1,'show captive-portal status')
res1 = CheckLineList(data,[('Authentication Mode','Pap')])
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
        # portal认证用户名：portal_username = 'aaa'
        # portal认证密码：portal_password = '111' 
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
        ################################################################################
        #Step 5
        #操作
        # STA1主动进行portal下线
        #预期
        # 下线成功
        # show captive-portal  client  status命令查看CP client列表为空；
        # STA1 ping pc1_ipv4不通
        ################################################################################
        printStep(testname,'Step 5','sta1 logout')
        # opertate
        # 退出登陆
        res1 = portal_logout_withcheck(web)
        # AC1上检查不存在sta1的portal用户表项
        res2 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                        check=[(sta1mac)],retry=10,waitflag=False)
        # 检查sta1无法ping通pc1
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        res3=0 if res3 !=0 else -1  
        #result
        printCheckStep(testname, 'Step 5',res1,res2,res3)
        # 关闭网页
        web_close(web)
    ################################################################################
    #Step 6
    #操作
    # AC1配置chap：
    # captive-portal                                                                                                          
    # authentication-mode chap 
    #预期
    # 配置成功
    # AC1上show captive-portal status显示：
    # Authentication Mode............................ Chap
    ################################################################################
    printStep(testname,'Step 6','Config authentication-mode chap')
    res1=1
    #operate
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'authentication-mode chap')
    # check
    IdleAfter(5)
    data=SetCmd(switch1,'show captive-portal status')
    res1 = CheckLineList(data,[('Authentication Mode','Chap')])
    #result
    printCheckStep(testname, 'Step 6',res1)
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
        # 输入正确的用户名和密码进行认证
        # portal认证用户名：portal_username = 'aaa'
        # portal认证密码：portal_password = '111' 
        #预期
        # STA1认证成功
        # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）。
        # STA1ping PC1可以ping通
        ################################################################################
        printStep(testname,'Step 8',\
                            'input correct username and password',\
                            'login successully')
        res1=res2=res3=1
        # operate
        res1 = inportal_login_withcheck(web,portal_username,portal_password)
        res2 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        #result
        printCheckStep(testname, 'Step 8',res1,res2,res3)
        # 关闭网页
        web_close(web)
else:
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'authentication-mode chap')
################################################################################
#Step 9(合并原方案step9,step10)
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 9',\
          'Recover initial config for switches.')

#operate
# sta1解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
CMDKillFirefox(sta1)
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)

#end
printTimer(testname, 'End')