#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.15.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.15	不同MAC的客户端使用相同的IP向ac发起认证
# 测试目的：外置portal场景下，不同MAC的客户端使用相同的IP向ac发起认证,第二个客户端不能通过portal认证
# 测试描述：
# 1.	STA1连接到网络认证成功。
# 2.	STA2设置跟STA1同样的ip地址，连接到网络，无法认证成功。
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.22
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase externalportal_4.1.15'
avoiderror(testname)
printTimer(testname,'Start','Test two sta use same ip to auth')
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
    res = web_close(web)
    if res['status'] != True:
        printRes(res)
        CMDKillFirefox(sta1)
###############################################################################
#Step 4
#操作
# 客户端STA2设置跟STA1相同的静态地址STA1IP（192.168.X.X）
# 连接到网络Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  status可以查看客户端STA1和STA2的表项
################################################################################
printStep(testname,'Step 4',\
                    'sta2 connect to test1',\
                    'Config the same ip with sta1 instead of dhcp')
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,dhcpFlag=False,bssid=ap1mac_type1)
SetCmd(sta2,'\n')
SetCmd(sta2,'ifconfig',Netcard_sta1,sta1_ipv4,'netmask 255.255.255.0')
SetCmd(sta2,'route add -net 0.0.0.0/0 gw',If_vlan4091_s1_ipv4)
IdleAfter(10)
if res1 == 0:
    res2 = CheckSutCmd(switch1,'show wireless client summary',\
                        check=[(sta1mac),(sta2mac)],retry=5,waitflag=False)
#result
printCheckStep(testname, 'Step 4',res1,res2)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ###############################################################################
    #Step 5
    #操作
    # 查看STA2是否处于AIP表项
    # 检查STA2是否可以ping通free-resources1
    #预期
    # AC1上通过命令show captive-portal aip status无法看到STA2的表项
    # STA2无法ping通free-resources1
    ################################################################################
    printStep(testname,'Step 5','sta2 ping portal-server failed')
    res1=res2=1
    #operate
    res1 = CheckPing(sta2,Radius_server,mode='linux')
    res1 = 0 if res1 != 0 else 1
    res2 = CheckSutCmdWithNoExpect(switch1,'show captive-portal aip status',\
                                    check=[(sta1_ipv4,sta2mac)],retry=1,waitflag=False)
    #result
    printCheckStep(testname, 'Step 5',res1,res2)
    ################################################################################
    #Step 6
    #操作
    # 客户端STA2打开web页面访问1.1.1.1（该地址为变量web_ip）
    #预期
    # STA2上无法出现重定向页面
    ################################################################################
    printStep(testname,'Step 6','sta2 can notredirect to portal auth page')
    res1=0
    # operate
    # sta2打开1.1.1.1，不能重定向到外置portal认证页面
    web = web_init(sta2_host)
    res1 = exportal_redirect_success(web,web_ip)
    res1 = 0 if res1 != 0 else 1
    #result
    printCheckStep(testname, 'Step 6',res1)
    # 关闭网页
    res = web_close(web)
    if res['status'] != True:
        printRes(res)
        CMDKillFirefox(sta2)
################################################################################
#Step 7
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 7',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta2mac)],retry=10,waitflag=False)
#end
printTimer(testname, 'End')