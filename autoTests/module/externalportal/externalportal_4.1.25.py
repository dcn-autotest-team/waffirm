#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.25.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.25	客户端认证时与portal、radius服务器网络不通ac和ap不会出现异常
# 测试目的：客户端认证时使其与portal server和radius服务器网络不通，认证不成功且ac和ap不会出现异常 
# 测试描述：
# 1.	断开AC跟portal服务器、radius服务器的连接
# 2.	客户端连接到无线网络进行portal认证，认证不成功且AC和AP不会出现异常。
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

testname = 'TestCase externalportal_4.1.25'
avoiderror(testname)
printTimer(testname,'Start','Test portal-server abnormity')
################################################################################
#Step 1
#操作
# 断开测试环境和portal、radius服务器的通信：
# S3与portal服务器连接口：s3p5 
# S3(config)#interface  ethernet  s3p5                                                                                    
# S3(config-if-s3p5)#shutdown
#预期
# 成功断开AC与portal、radius服务器的通信
# AC1无法ping通portal服务器和radius服务器
################################################################################
printStep(testname,'Step 1','Shutdown s3p5')
res1=1
#operate
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p5)
SetCmd(switch3,'shutdown')
IdleAfter(5)
# check
res1 = CheckPing(switch1,Radius_server,mode='img',srcip=StaticIpv4_ac1)
res1 = 0 if res1 != 0 else 1

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
    # 客户端STA1上无法看到重定向页面，并且ac和ap不会出现异常重启
    # STA1无法ping通PC1
    ################################################################################
    printStep(testname,'Step 3','sta1 open 1.1.1.1 and can not redirect to portal auth page')
    res1=res2=1
    # operate
    # sta1打开1.1.1.1，不能重定向到外置portal认证页面
    web = web_init(sta1_host)
    res1 = exportal_redirect_success(web,web_ip)
    res2 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res1 = 0 if res1 != 0 else 1
    res2 = 0 if res2 != 0 else 1
    #result
    printCheckStep(testname, 'Step 3',res1,res2)
    # 关闭网页
    res = web_close(web)
    if res['status'] != True:
        printRes(res)
        CMDKillFirefox(sta1)
################################################################################
#Step 4
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 4',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p5)
SetCmd(switch3,'no shutdown')
IdleAfter(30)
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)
#end
printTimer(testname, 'End')