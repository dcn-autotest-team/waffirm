#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.18.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.18	listen portal-server-port与portal server不同时客户端无法认证成功
# 测试目的：当AC上的listen portal-server-port值与portal server上值不相同，客户端无法认证成功
# 测试描述：
# 1.	修改AC上的listen portal-server-port值与portal server上值不相同
# 2.	客户端连接网络进行portal认证
# 3.	修改AC上的listen portal-server-port值与portal server上值相同
# 4.	客户端连接网络进行portal认证
# 5.	AC上查看认证成功后STA的信息
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

testname = 'TestCase externalportal_4.1.18'
avoiderror(testname)
printTimer(testname,'Start','Test when listen portal-server-port and portal server are different, sta can not auth')
################################################################################
#Step 1
#操作
# 修改AC上的listen portal-server-port与portal server上值不相同（热点服务器默认监听端口为2000）
# AC1(config)#captive-portal                                                                                                          
# AC1(config-cp)#configuration 1                                                                                                      
# AC1(config-cp-instance)#listen portal-server-port 2001
#预期
# 配置成功。
# 在AC1上通过命令show captive-portal  configuration 1 status显示Listen Portal-Server-Port的值为2001 
################################################################################
printStep(testname,'Step 1','Change listen portal-server-port',\
                            'and listen portal-server-port now is different to portal server')
res1=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1 ')
SetCmd(switch1,'listen portal-server-port 2001')
# check
data=SetCmd(switch1,'show captive-portal configuration 1 status')
res1=CheckLineList(data,[('Listen Portal-Server-Port','2001')],IC=True)
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
sta1_ipresult = GetStaIp(sta1,checkippool=Netcard_ipaddress_check)
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
    res1 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 3',res1)
    if res1 == 0:
        ################################################################################
        #Step 4
        #操作
        # 客户端STA1在推送出的重定向页面输入正确的用户名和密码进行portal认证
        # portal认证用户名：portal_username = 'aaa'
        # portal认证密码：portal_password = '111
        # 查看AC1上的CP列表
        # 检查STA1是否可以上网
        #预期
        # STA1认证不成功
        # 输入用户名密码点击认证，页面提示“无线网络问题，请联系管理员”
        # AC1上通过命令show captive-portal  client  status查看不到任何表项
        # STA1无法ping通PC1
        ################################################################################
        printStep(testname,'Step 4',\
                            'input correct username and password',\
                            'login failed')
        res1=res2=res3=0
        # operate
        res1 = exportal_login_withcheck(web,portal_username,portal_password)
        res1 = 0 if res1 != 0 else 1
        res2 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res2 = 0 if res2 != 0 else 1
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        res3 = 0 if res3 != 0 else 1
        #result
        printCheckStep(testname, 'Step 4',res1,res2,res3)
     # 关闭网页
    web_close(web)
    ################################################################################
    #Step 5
    #操作
    # 修改AC上的listen portal-server-port与portal server上值相同（热点服务器默认监听端口为2000）
    # AC1(config)#captive-portal                                                                                                          
    # AC1(config-cp)#configuration 1                                                                                                      
    # AC1(config-cp-instance)#listen portal-server-port 2000
    #预期
    # 配置成功。
    # 在AC1上通过命令show captive-portal  configuration 1 status显示Listen Portal-Server-Port的值为2000
    ################################################################################
    printStep(testname,'Step 5','Change listen portal-server-port',\
                                'and listen portal-server-port now is same with portal server')
    res1=1
    #operate
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'configuration 1 ')
    SetCmd(switch1,'listen portal-server-port 2000')
    # check
    data=SetCmd(switch1,'show captive-portal configuration 1 status')
    res1=CheckLineList(data,[('Listen Portal-Server-Port','2000')],IC=True)
    #result
    printCheckStep(testname, 'Step 5',res1)
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
        # portal认证用户名：portal_username = 'aaa'
        # portal认证密码：portal_password = '111
        # 查看AC1上的CP列表
        # 检查STA1是否可以上网 
        #预期
        # STA1认证成功
        # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）。
        # 通过命令show captive-portal  configuration 1 client status查看，显示:
        # Client MAC Address为STA1MAC
        # Client IP Address为STA1IP
        # 通过命令show captive-portal interface ws-network 1 client status查看，显示
        # Client MAC Address为STA1MAC
        # Client IP Address为STA1IP
        # 通过命令show captive-portal client STA1MAC ipv4 STA1IP status查看，显示：
        # Client MAC Address为STA1MAC
        # Client IP Address为STA1IP
        # STA1 ping PC1可以ping通
        ################################################################################
        printStep(testname,'Step 7',\
                            'input correct username and password',\
                            'login successully')
        res1=res2=res3=res4=res5=res6=1
        # operate
        res1 = exportal_login_withcheck(web,portal_username,portal_password)
        res2 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res3 = CheckSutCmd(switch1,'show captive-portal configuration 1 client status',\
                                    check=[(sta1mac,sta1_ipv4)],retry=5,waitflag=False)
        res4 = CheckSutCmd(switch1,'show captive-portal interface ws-network 1 client status',\
                                    check=[(sta1mac,sta1_ipv4)],retry=1,waitflag=False)
        res5 = CheckSutCmd(switch1,'show captive-portal client '+sta1mac+' ipv4 '+sta1_ipv4+' status',\
                                    check=[(sta1mac),(sta1_ipv4)],retry=1,waitflag=False)
        res6 = CheckPing(sta1,pc1_ipv4,mode='linux')
        #result
        printCheckStep(testname, 'Step 7',res1,res2,res3,res4,res5,res6)
     # 关闭网页
    web_close(web)
else:
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'configuration 1')
    SetCmd(switch1,'listen portal-server-port 2000')
################################################################################
#Step 8
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 8',\
          'Recover initial config')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
CMDKillFirefox(sta1)
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)

#end
printTimer(testname, 'End')