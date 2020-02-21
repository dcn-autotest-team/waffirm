#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# internal_portal_4.1.19.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.19	客户端在开启portal认证的network（不同SSID）间切换网络
# 测试目的：验证客户端在开启了portal认证的网络间的切换功能
# 测试描述：
# 1、	新建1个network并且开启相应的vap，绑定到portal模块的实例下面
# 2、	STA1连接network1可以成功进行portal认证
# 3、	STA1直接连接network2，AC1上表项正常，并且可以成功进行portal认证
# 4、	STA1再次连接到开启portal认证的network1可以正常进行portal认证
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.9
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase internalportal_4.1.19'
avoiderror(testname)
printTimer(testname,'Start','Test sta switchover network that have different ssid')
################################################################################
#Step 1
#操作
# 将network2绑定到实例下
# AC1(config)#captive-portal                                                                                                       
# AC1(config-cp)#configuration 1                                                                                                   
# AC1(config-cp-instance)#interface  ws-network  2   
#预期
# 绑定成功。
# AC1上通过命令show run可以查看到命令：
 # interface ws-network 1                                                                                                            
 # interface ws-network 2 
################################################################################
printStep(testname,'Step 1','Bind network2 to captive-portal configuration 1')
res1=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1 ')
SetCmd(switch1,'interface ws-network 2 ')
# check
data=SetCmd(switch1,'show run c')
res1=CheckLineList(data,[('interface ws-network 1'),('interface ws-network 2')],IC=True)
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
sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
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
# 客户端STA1连接到Network_name2   
# 查看AC1上的CP列表
# 检查STA1是否可以上网
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看STA1获取到192.168.X.X(Dhcp_pool2)网段的地址。
# 通命令show wireless  client  status可查看到管理的SSID为 Network_name2     
# 通过命令show captive-portal  client  status查看不到任何表项 
# 通过命令show captive-portal  aip status可以查看到STA1的表项，其中mac=sta1_mac
# STA1无法ping通 pc1_ipv4
################################################################################
printStep(testname,'Step 5',\
                    'sta1 connect to test2')
res1=res2=res3=res4=res5=res6=1
#operate
#STA1关联 network2
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name2,checkDhcpAddress=Netcard_ipaddress_check2,bssid=ap1mac_type1_network2)
if res1 == 0:
    # 通过命令show wireless  client  summary可以查看客户端STA1获取到192.168.X.X(Dhcp_pool2)网段的地址
    res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
    # 通命令show wireless  client  status可查看到管理的SSID为 Network_name2  
    res3 = CheckSutCmd(switch1,'show wireless client status',\
                        check=[(sta1mac,Network_name2)],retry=1,waitflag=False)
    # 通过命令show captive-portal  client  status查看不到任何表项 
    res4 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
    res5 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res5 = 0 if res5 != 0 else 1
    SetCmd(switch1,'show captive-portal aip status')
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
    res1 = inportal_redirect_success(web,web_ip)
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
        # 通过命令show captive-portal  aip status查看不到任何表项
        # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）。
        # STA1 ping PC1可以ping通
        ################################################################################
        printStep(testname,'Step 7',\
                            'input correct username and password',\
                            'login successully')
        res1=res2=res3=1
        # operate
        res1 = inportal_login_withcheck(web,portal_username,portal_password)
        # 通过命令show captive-portal  aip status查看不到任何表项
        res2 = CheckSutCmdWithNoExpect(switch1,'show captive-portal aip status',\
                                        check=[(sta1_ipv4,sta1mac)],retry=10,waitflag=False)
        res3 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res4 = CheckPing(sta1,pc1_ipv4,mode='linux')
        #result
        printCheckStep(testname, 'Step 7',res1,res2,res3,res4)
    # 关闭网页
    web_close(web)
################################################################################
#Step 8(合并原方案step8,step9)
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 8',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
CMDKillFirefox(sta1)
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1 ')
SetCmd(switch1,'no interface ws-network 2 ')
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)

#end
printTimer(testname, 'End')