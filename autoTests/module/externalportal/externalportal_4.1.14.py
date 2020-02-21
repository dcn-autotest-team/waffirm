#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.14.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.14	客户端设置静态ip地址进行外置portal认证
# 测试目的：外置portal场景下，当客户端设置静态地址连接到网络，能够正常进行portal认证
# 测试描述：
# 1.	STA1设置静态ip地址连接到无线网络。
# 2.	检查STA1是否可以进行重定向 。
# 3.	STA1进行外置portal认证成功。
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.22
#*******************************************************************************

#Package

#Global Definition
Sta1_staticip = Dhcp_pool1+'134'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase externalportal_4.1.14'
avoiderror(testname)
printTimer(testname,'Start','Test STA use static ip to auth')
###############################################################################
#Step 1
#操作
# 客户端STA1设置静态地址192.168.X.X(该地址为静态地址,必须跟Dhcp_pool1 = '192.168.'+EnvNo+'1.'中地址为一个网段)
# 连接到网络Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端STA1获取到192.168.X.X网段的地址
################################################################################
printStep(testname,'Step 1',\
                    'sta1 connect to test1',\
                    'Config static Sta1IP instead of dhcp',\
                    'Show captive-portal client status on AC1 and check whether Sta1IP is right')
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_type1)
SetCmd(sta1,'\n')
SetCmd(sta1,'ifconfig',Netcard_sta1,Sta1_staticip,'netmask 255.255.255.0')
SetCmd(sta1,'route add -net 0.0.0.0/0 gw',If_vlan4091_s1_ipv4)
# 客户端ping free resource触发IP上报
SetCmd(sta1,'ping',Radius_server,'-c 5')
IdleAfter(10)
if res1 == 0:
    res2 = CheckSutCmd(switch1,'show wireless client summary',\
                        check=[(sta1mac,Sta1_staticip)],retry=5,waitflag=False)
#result
printCheckStep(testname, 'Step 1',res1,res2)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ###############################################################################
    #Step 2
    #操作
    # 检查STA1是否可以进行重定向
    # STA1去ping portal服务器
    # 检查STA1是否处于AIP表项中
    #预期
    # STA1可以ping通portal服务器（free-sources1）
    # AC1上通过命令show captive-portal  aip status可以看到表项，mac=STA1MAC
    ################################################################################
    printStep(testname,'Step 2','sta1 ping portal-server successully')
    res1=res2=1
    #operate
    res1 = CheckPing(sta1,Radius_server,mode='linux')
    res2 = CheckSutCmd(switch1,'show captive-portal aip status',\
                        check=[(sta1mac)],retry=5,waitflag=False)
    #result
    printCheckStep(testname, 'Step 2',res1,res2)
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
################################################################################
#Step 5
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 5',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)
#end
printTimer(testname, 'End')