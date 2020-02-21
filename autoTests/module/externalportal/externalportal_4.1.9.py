#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.9.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.9	http portal功能验证
# 测试目的：Portal用户在认证前，AP对目的端口为80的HTTP报文做重定向，当配置了额外的HTTP portal后，AP对目的端口为80和配置端口的HTTP做重定向 
# 测试描述：
# 1.	客户端STA1连接无线网络
# 2.	配置http port为80
# 3.	配置http port为1，客户端STA1进行重定向
# 4.	配置http port为81，客户端STA1进行重定向
# 5.	配置http port为65535，客户端STA1进行重定向
# 6.	客户端STA1使用一个没有添加过的端口进行重定向
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.21
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase externalportal_4.1.9'
avoiderror(testname)
printTimer(testname,'Start','Test http destination port')
###############################################################################
#Step 1
#操作
# 客户端STA1连接到网络Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端STA1获取到192.168.X.X(Dhcp_pool1)网段的地址
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
    # 配置http port为80 
    # AC1(config-cp)#configuration 1                                                                                                
    # AC1(config-cp-instance)#http port 80
    #预期
    # 配置下发不成功。
    # AC1上提示：Port 80 is already in use.                                        
    # 客户端sta1打开web页面输入1.1.1.1（该地址为变量web_ip）可以进行重定向得到重定向页面
    ################################################################################
    printStep(testname,'Step 2','ac1 can not config http port 80 because 80 is already in use',\
                                'sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=res2=1
    # operate
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'configuration 1')
    data = SetCmd(switch1,'http port 80')
    res1 = CheckLine(data,'Port 80 is already in use')
    # sta1打开1.1.1.1，并检查是否重定向到portal认证页面
    web = web_init(sta1_host)
    res2 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 2',res1,res2)
    # 关闭网页
    web_close(web)
    ################################################################################
    #Step 3
    #操作
    # 在ap上查看http port的状态
    # cp_debug vap_config
    # dmesg -c
    #预期
    # ap的串口打印中，The wlan0vap0 configuration:下Extra Http Port为0
    ################################################################################
    printStep(testname,'Step 3','cp_debug vap_config;dmesg -c on AP 1')
    # operate
    # 为兼容不同型号AP，AP上只打印信息，不做检查
    SetCmd(ap1,'cp_debug vap_config;dmesg -c')
    #result
    printCheckStep(testname, 'Step 3',0)
    # ################################################################################
    # #Step 4
    # #操作
    # # 配置http port为1 
    # # AC1(config-cp)#configuration 1                                                                                                
    # # AC1(config-cp-instance)#http port 1 
    # #预期
    # # 配置成功。
    # # 客户端sta1打开web页面输入web_ip:1可以进行重定向得到重定向页面
    # # 客户端sta1打开web页面输入web_ip可以进行重定向得到重定向页面
    # ################################################################################
    # printStep(testname,'Step 4','ac1 config http port 1',\
                                # 'sta1 open 1.1.1.1:1 and can redirect to portal auth page',\
                                # 'sta1 open 1.1.1.1 and can redirect to portal auth page')
    # res1=res2=res3=1
    # # operate
    # EnterConfigMode(switch1)
    # SetCmd(switch1,'captive-portal')
    # SetCmd(switch1,'configuration 1')
    # SetCmd(switch1,'http port 1')
    # data = SetCmd(switch1,'show run c')
    # res1 = CheckLine(data,'http port 1')
    # IdleAfter(10)
    # # sta1打开1.1.1.1:1，并检查是否重定向到portal认证页面
    # web = web_init(sta1_host)
    # res2 = exportal_redirect_success(web,'http://1.1.1.1:1')
    # # 关闭网页
    # web_close(web)
    # # sta1打开1.1.1.1，并检查是否重定向到portal认证页面
    # web = web_init(sta1_host)
    # res3 = exportal_redirect_success(web,web_ip)
    # # 关闭网页
    # web_close(web)
    # #result
    # printCheckStep(testname, 'Step 4',res1,res2,res3)
    # ################################################################################
    # #Step 5
    # #操作
    # # 在ap上查看http port的状态
    # # cp_debug vap_config
    # # dmesg -c
    # #预期
    # # ap的串口打印中，The wlan0vap0 configuration:下Extra Http Port为1
    # ################################################################################
    # printStep(testname,'Step 5','cp_debug vap_config;dmesg -c on AP 1')
    # # operate
    # # 为兼容不同型号AP，AP上只打印信息，不做检查
    # SetCmd(ap1,'cp_debug vap_config;dmesg -c')
    # #result
    # printCheckStep(testname, 'Step 5',0)
    ################################################################################
    #Step 6
    #操作
    # 配置http port为81
    # AC1(config-cp)#configuration 1                                                                                                
    # AC1(config-cp-instance)#http port 81
    #预期
    # 配置成功。
    # 客户端sta1打开web页面输入web_ip:81可以进行重定向得到重定向页面
    # 客户端sta1打开web页面输入web_ip可以进行重定向得到重定向页面
    ################################################################################
    printStep(testname,'Step 6','ac1 config http port 81',\
                                'sta1 open 1.1.1.1:81 and can redirect to portal auth page',\
                                'sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=res2=res3=1
    # operate
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'configuration 1')
    SetCmd(switch1,'http port 81')
    data = SetCmd(switch1,'show run c')
    res1 = CheckLine(data,'http port 81')
    IdleAfter(10)
    # sta1打开1.1.1.1:81，并检查是否重定向到portal认证页面
    web = web_init(sta1_host)
    res2 = exportal_redirect_success(web,'http://1.1.1.1:81')
    # 关闭网页
    web_close(web)
    # sta1打开1.1.1.1，并检查是否重定向到portal认证页面
    web = web_init(sta1_host)
    res3 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 6',res1,res2,res3)
    # 关闭网页
    web_close(web)
    ################################################################################
    #Step 7
    #操作
    # 在ap上查看http port的状态
    # cp_debug vap_config
    # dmesg -c
    #预期
    # ap的串口打印中，The wlan0vap0 configuration:下Extra Http Port为81
    ################################################################################
    printStep(testname,'Step 7','cp_debug vap_config;dmesg -c on AP 1')
    # operate
    # 为兼容不同型号AP，AP上只打印信息，不做检查
    SetCmd(ap1,'cp_debug vap_config;dmesg -c')
    #result
    printCheckStep(testname, 'Step 7',0)
    ################################################################################
    #Step 8
    #操作
    # 配置http port为65535
    # AC1(config-cp)#configuration 1                                                                                                
    # AC1(config-cp-instance)#http port 65535
    #预期
    # 配置成功。
    # 客户端sta1打开web页面输入web_ip:65535可以进行重定向得到重定向页面
    # 客户端sta1打开web页面输入web_ip可以进行重定向得到重定向页面
    ################################################################################
    printStep(testname,'Step 8','ac1 config http port 65535',\
                                'sta1 open 1.1.1.1:65535 and can redirect to portal auth page',\
                                'sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=res2=res3=1
    # operate
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'configuration 1')
    SetCmd(switch1,'http port 65535')
    data = SetCmd(switch1,'show run c')
    res1 = CheckLine(data,'http port 65535')
    IdleAfter(10)
    # sta1打开1.1.1.1:65535，并检查是否重定向到portal认证页面
    web = web_init(sta1_host)
    res2 = exportal_redirect_success(web,'http://1.1.1.1:65535')
    # 关闭网页
    web_close(web)
    # sta1打开1.1.1.1，并检查是否重定向到portal认证页面
    web = web_init(sta1_host)
    res3 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 8',res1,res2,res3)
    # 关闭网页
    web_close(web)
    ################################################################################
    #Step 9
    #操作
    # 在ap上查看http port的状态
    # cp_debug vap_config
    # dmesg -c
    #预期
    # ap的串口打印中，The wlan0vap0 configuration:下Extra Http Port为0
    ################################################################################
    printStep(testname,'Step 9','cp_debug vap_config;dmesg -c on AP 1')
    # operate
    # 为兼容不同型号AP，AP上只打印信息，不做检查
    SetCmd(ap1,'cp_debug vap_config;dmesg -c')
    #result
    printCheckStep(testname, 'Step 9',0)
    ################################################################################
    #Step 10
    #操作
    # 客户端STA1使用一个没有添加过的端口进行重定向
    #预期
    # 客户端sta1打开web页面输入web_ip:100无法进行重定向得到重定向页面
    ################################################################################
    printStep(testname,'Step 10','sta1 open 1.1.1.1:100 and can not redirect to portal auth page')
    res1=1
    # operate
    # sta1打开1.1.1.1:100，无法重定向到portal认证页面
    web = web_init(sta1_host)
    res1 = exportal_redirect_success(web,'http://1.1.1.1:100')
    res1 = 0 if res1 != 0 else 1
    #result
    printCheckStep(testname, 'Step 10',res1)
    # 关闭网页
    web_close(web)
################################################################################
#Step 11
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 11',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'no http port')
CMDKillFirefox(sta1)
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)
#end
printTimer(testname, 'End')