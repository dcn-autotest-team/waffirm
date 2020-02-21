#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.24.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.24	客户端下线功能
# 测试目的：外置portal认证场景下，客户端认证成功后，可以正常下线
# 测试描述：
# 1.	客户端STA1接网络后输入正确的用户名和密码认证通过
# 2.	AC1上可以强制客户端STA1下线
# 3.	客户端STA1下线后再次发起认证请求可以得到重定向页面并且认证成功
# 4.	客户端上线后将network从instance中删掉客户端下线可成功
# 5.	客户端上线后被AC1强制从无线层踢下线后CP列表更新正常
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.2
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase externalportal_4.1.24'
avoiderror(testname)
printTimer(testname,'Start','Test client deauthenticate')

###############################################################################
#Step 1
#操作
# 客户端STA1连接到网络Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端获取到192.168.X.X（Dhcp_pool1）网段的地址
################################################################################
printStep(testname,'Step 1','STA1 connect to test1')
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res1 == 0:
    res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
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
    printStep(testname,'Step 2','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    #operate
    web = web_init(sta1_host)
    res1 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 2',res1)
    ################################################################################
    #Step 3
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
    ################################################################################
    #Step 4
    # 客户端上线后在AC1上强制其下线
    # AC1#captive-portal client deauthenticate STA1MAC ipv4 STA1IP                                                                                                                                                                                 
    # The specified clients will be deauthenticated. Are you sure you want to deauthenticate clients? [Y/N] y 
    #预期
    # 客户端下线成功
    # AC1上通过命令show captive-portal  client  status查看不到任何表项
    # STA1无法ping通PC1
    ################################################################################
    printStep(testname,'Step 4','client deauthenticate')
    # opertate
    EnterEnableMode(switch1)
    SetCmd(switch1,'captive-portal client deauthenticate '+sta1mac+' ipv4 '+sta1_ipv4,promotePatten='Y/N',promoteTimeout=5) 
    SetCmd(switch1,'y')
    # AC1上检查不存在sta1的portal用户表项
    res1 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=10,waitflag=False)
    IdleAfter(10)
    # 检查sta1无法ping通pc1
    res2 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res2=0 if res2 !=0 else -1  
    #result
    printCheckStep(testname, 'Step 4',res1,res2)
    ################################################################################
    #Step 5
    #操作
    # 客户端STA1再次打开web页面访问1.1.1.1（该地址为变量web_ip）
    #
    #预期
    # S客户端下线后再次发起认证请求可得到重定向界面
    ################################################################################
    printStep(testname,'Step 5','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    #operate
    web = web_init(sta1_host)
    res1 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 5',res1)
    ################################################################################
    #Step 6
    #操作
    # 输入正确的用户名和密码进行认证
    # portal认证用户名：portal_username = 'aaa'
    # portal认证密码：portal_password = '111' 
    # AC1上查看CP列表
    # 检查AC1是否放行STA1的流量
    #预期
    # 提示用户认证成功，通过show captive-portal  client  status命令查看CP client列表，
    # 显示出STA1的信息（“MAC Address”显示“STA1MAC”）
    # STA1可以ping通PC1
    ################################################################################
    printStep(testname,'Step 6',\
                        'input correct username and password',\
                        'login successully')
    res1=res2=res3=1
    # operate
    res1 = exportal_login_withcheck(web,portal_username,portal_password)
    res2 = CheckSutCmd(switch1,'show captive-portal client status',\
                                check=[(sta1mac)],retry=5,waitflag=False)
    res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
    #result
    printCheckStep(testname, 'Step 6',res1,res2,res3)
    # 关闭网页
    web_close(web)
    ################################################################################
    #Step 7
    # 客户端上线后将network从instance中删掉
    # AC1(config)#captive-portal                                                                                                          
    # AC1(config-cp)#configuration 1                                                                                                                                                                                                                 
    # AC1(config-cp-instance)#no interface ws-network 1 
    #预期
    # 客户端下线成功
    # AC1上通过命令show captive-portal  client status查看不到任何表项
    # STA1可以ping通PC1
    ################################################################################
    printStep(testname,'Step 7','clear network 1 form configuration 1',\
                                'sta1 is not in portal client list',\
                                'sta1 ping pc1 successully')
    res1=res2=1
    # opertate
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'configuration 1')
    SetCmd(switch1,'no interface ws-network 1')
    # AC1上检查不存在sta1的portal用户表项
    res1 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=10,waitflag=False)
    # 检查sta1可以ping通pc1
    res2 = CheckPing(sta1,pc1_ipv4,mode='linux')
    #result
    printCheckStep(testname, 'Step 7',res1,res2)
    ################################################################################
    #Step 8
    # 将network1绑定到实例下
    # AC1(config)#captive-portal                                                                                                          
    # AC1(config-cp)#configuration 1                                                                                                      
    # AC1(config-cp-instance)#interface ws-network 1
    #预期
    # STA1处于待认证状态
    # AC1上通过命令show captive-portal  aip status可以查看到AIP表项，其中ip=STA1IP  mac=STA1MAC
    # STA1无法ping通PC1
    ################################################################################
    printStep(testname,'Step 8','add network 1 to configuration 1',\
                                'sta1 is in portal aip  client list',\
                                'sta1 ping pc1 failed')
    # opertate
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'configuration 1')
    SetCmd(switch1,'interface ws-network 1')
    IdleAfter(10)
    # sta1先进行ping操作，触发captive-portal aip表项的建立
    # 检查sta1无法ping通pc1
    res2 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res2 = 0 if res2 != 0 else 1
    # AC1上检查STA1处于待认证状态
    res1 = CheckSutCmd(switch1,'show captive-portal aip status',\
                                check=[(sta1_ipv4,sta1mac)],retry=10,waitflag=False)
    #result
    printCheckStep(testname, 'Step 8',res1,res2)
    ################################################################################
    #Step 9
    #操作
    # 客户端STA1再次打开web页面访问1.1.1.1（该地址为变量web_ip）
    #
    #预期
    # 客户端下线后再次发起认证请求可得到重定向界面
    ################################################################################
    printStep(testname,'Step 9','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    #operate
    web = web_init(sta1_host)
    res1 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 9',res1)
    ################################################################################
    #Step 10
    #操作
    # 输入正确的用户名和密码进行认证
    # portal认证用户名：portal_username = 'aaa'
    # portal认证密码：portal_password = '111' 
    # AC1上查看CP列表
    # 检查AC1是否放行STA1的流量
    #预期
    # 提示用户认证成功，通过show captive-portal  client  status命令查看CP client列表，
    # 显示出STA1的信息（“MAC Address”显示“STA1MAC”）
    # STA1可以ping通PC1
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
    # 关闭网页
    web_close(web)
    ################################################################################
    #Step 11
    # 客户端被AC1强制从无线层踢下线
    # AC1#wireless client disassociate STA1MAC                                                                                
    # Process with disassociate the local client? [Y/N] y 
    #预期
    # 客户端下线成功
    # AC1上通过命令show wireless  client  status显示表项为空
    # AC1上通过命令show captive-portal  client  status查看不到任何表项
    # STA1无法ping通PC1
    ################################################################################
    printStep(testname,'Step 11','client deauthenticate',\
                                'sta1 is not in client list',\
                                'sta1 ping pc1 failed')
    # opertate
    EnterEnableMode(switch1)
    SetCmd(switch1,'wireless client disassociate '+sta1mac,promotePatten='Y/N',promoteTimeout=5) 
    SetCmd(switch1,'y')
    # 由于linux客户端存在自动重连的现象，因此不检查show wireless client status表项
    # AC1上检查不存在sta1的portal用户表项
    res1 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=10,waitflag=False)
    # 检查sta1无法ping通pc1
    res2 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res2=0 if res2 !=0 else -1  
    #result
    printCheckStep(testname, 'Step 11',res1,res2)
################################################################################
#Step 12
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 12',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
CMDKillFirefox(sta1)
#end
printTimer(testname, 'End')