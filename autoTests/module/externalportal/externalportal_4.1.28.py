#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.28.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# 4.1.28	开启mac-ip-based后的portal认证
# 测试目的：在mac-ip-based模式下，portal在线用户使用过程中IP地址发生变化，AC和AP更新在线用户表项，用户需要重新认证之后才能上网
# 测试描述：
# 1.	开启mac-ip-based后，在线用户STA1的地址发生变化后，用户需要重新认证才能上网。
# 2.	关闭mac-ip-based后，客户端STA1连接网络进行portal认证，客户端的ip地址发生变化，AC上的CP表更新，客户端仍然处于认证状态
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.3
#*******************************************************************************

#Package

#Global Definition
Sta1_staticip = Dhcp_pool1+'145'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase externalportal_4.1.28'
avoiderror(testname)
printTimer(testname,'Start','Test auth-method mac-ip-based')
################################################################################
#Step 1
#操作
# AC1上开启mac-ip-based功能
# AC1(config)#captive-portal                                                                                                          
# AC1(config-cp)#configuration 1                                                                                                      
# AC1(config-cp-instance)#auth-method mac-ip-based
#预期
# 配置成功
# AC1上通过命令show captive-portal  configuration  1 status查看
# Authentication Method显示为 Mac-Ip-Based
################################################################################
printStep(testname,'Step 1','Config auth-method mac-ip-based')
res1=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'auth-method mac-ip-based')
# check
data=SetCmd(switch1,'show captive-portal configuration 1 status')
res1 = CheckLineList(data,[('Authentication Method','Mac-Ip-Based')])
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
#获取STA1的地址
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
    web_close(web)
    ###############################################################################
    #Step 5
    #操作
    # 修改客户端STA1的地址为同网段的另外一个地址
    # 检查STA1是否仍然在线 
    #预期
    # 客户端STA1下线
    # AC1上通过命令show captive-portal  client  status查看不到任何表项
    # AC1上通过命令show captive-portal  aip status可以查看到STA1的表项，其中ip显示为STA1的修改后ip，mac显示为STA1MAC
    # STA1无法ping通PC1
    ################################################################################
    printStep(testname,'Step 5',\
                        'sta1 config statis ip',\
                        'sta1 is not in captive-portal client list',\
                        'sta1 ping pc1 failed')
    res1=res2=res3=1
    #operate
    SetCmd(sta1,'\n')
    SetCmd(sta1,'dhclient -r '+Netcard_sta1)
    SetCmd(sta1,'ifconfig',Netcard_sta1,Sta1_staticip,'netmask 255.255.255.0')
    SetCmd(sta1,'route add -net 0.0.0.0/0 gw',If_vlan4091_s1_ipv4)
    # 客户端ping free resource触发IP上报
    SetCmd(sta1,'ping',Radius_server,'-c 5')
    IdleAfter(10)
    res1 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=10,waitflag=False)
    res2 = CheckSutCmd(switch1,'show captive-portal aip status',\
                        check=[(Sta1_staticip,sta1mac)],retry=5,waitflag=False)
    res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res3 = 0 if res3 != 0 else 1
    #result
    printCheckStep(testname, 'Step 5',res1,res2,res3)
    ################################################################################
    #Step 6
    #操作
    #STA1断开与网络Network_name1的连接
    #预期
    #断开网络成功
    # 通过show wireless client status查看不到任何表项
    ################################################################################
    printStep(testname,'Step 6','sta1 disconnect network1')
    res1=1
    # operate
    WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
    IdleAfter(10)
    res1 = CheckSutCmdWithNoExpect(switch1,'show wireless client status',\
                            check=[(sta1mac)],retry=10,waitflag=False)
    #result
    printCheckStep(testname, 'Step 6',res1)
###############################################################################
#Step 7
#操作
# AC1上关闭mac-ip-based功能
# AC1(config)#captive-portal                                                                                                          
# AC1(config-cp)#configuration 1                                                                                                      
# AC1(config-cp-instance)#auth-method mac-based 
#预期
# 配置成功
# AC1上通过命令show captive-portal  configuration  1 status查看
# Authentication Method显示为 Mac-Based
################################################################################
printStep(testname,'Step 7','Config auth-method mac-based')
res1=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'auth-method mac-based')
# check
data=SetCmd(switch1,'show captive-portal configuration 1 status')
res1 = CheckLineList(data,[('Authentication Method','Mac-Based')])
#result
printCheckStep(testname, 'Step 7',res1)
################################################################################
#Step 8
#操作
#客户端STA1连接到网络Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端获取到192.168.X.X(Dhcp_pool1)网段的地址
################################################################################
printStep(testname,'Step 8','STA1 connect to test1')
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res1 == 0:
    res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
#获取STA1的地址
sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
#result
printCheckStep(testname, 'Step 8',res1,res2)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 9
    #操作
    # 客户端STA1打开web页面访问1.1.1.1（该地址为变量web_ip）
    #预期
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 9','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    # operate
    # sta1打开1.1.1.1，并检查是否重定向到外置portal认证页面
    web = web_init(sta1_host)
    res1 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 9',res1)
    if res1 == 0:
        ################################################################################
        #Step 10
        #操作
        # 客户端STA1在推送出的重定向页面输入正确的用户名和密码进行认证
        # portal认证用户名：portal_username = ‘aaa’
        # portal认证密码：portal_password = ‘111
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
    # 关闭网页
    web_close(web)
    ###############################################################################
    #Step 11
    #操作
    # 修改客户端STA1的地址为同网段的另外一个地址
    # 检查STA1是否仍然在线
    #预期
    # 客户端STA1仍然在线
    # AC1上通过命令show captive-portal  client  status查看到STA1的表项
    # 其中ip显示为STA1的修改后ip，mac显示为STA1MAC
    # STA1可以ping通PC1
    ################################################################################
    printStep(testname,'Step 11',\
                        'sta1 config statis ip',\
                        'sta1 is still in captive-portal client list',\
                        'sta1 ping pc1 successully')
    res1=res2=1
    #operate
    SetCmd(sta1,'\n')
    SetCmd(sta1,'dhclient -r '+Netcard_sta1)
    SetCmd(sta1,'ifconfig',Netcard_sta1,Sta1_staticip,'netmask 255.255.255.0')
    SetCmd(sta1,'route add -net 0.0.0.0/0 gw',If_vlan4091_s1_ipv4)
    IdleAfter(10)
    res1 = CheckSutCmd(switch1,'show captive-portal client status',\
                        check=[(sta1mac,Sta1_staticip)],retry=10,waitflag=False)
    res2 = CheckPing(sta1,pc1_ipv4,mode='linux')
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
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)

#end
printTimer(testname, 'End')