#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# internal_portal_4.1.14.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.14	WPA2-Enterprise模式下客户端内置portal认证
# 测试目的：验证SSID采用WPA2-Enterprise加密后开启portal认证，客户端连接网络能够正常进行内置portal认证
# 测试描述：
# 1、	开启内置portal认证。
# 2、	修改network1的加密方式为WPA2-Enterprise
# 3、	STA1连接网络后可以正常进行内置portal认证
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.8
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase internalportal_4.1.14'
avoiderror(testname)
printTimer(testname,'Start','Test portal with WPA2-Enterprise mode')
###############################################################################
#Step 1(合并方案step1,2)
#操作
# AC1上设置network1的加密方式为混合模式：WPA-Enterprise，WPA version为WPA2，认证服务器使用wlan：                                                                                                                   
# AC1(config)#wireless                                                                                                                      
# AC1(config-wireless)#network 1                                                                                                      
# AC1(config-network)#security mode wpa-enterprise                                                                                                                                                                                         
# AC1(config-network)#wpa versions wpa2                                                                                                                                                                                                                                                                                                            
# AC1(config-network)#radius server-name acct wlan                                                                                                  
# AC1(config-network)#radius server-name auth wlan 
# 将配置下发到AP1。
# Wireless ap profile apply 1
#预期
# 配置成功。在AC1上面Show wireless network 1可以看到相关的配置
################################################################################
printStep(testname,'Step 1 Step 2',\
          'set security mde of network 1 wpa-enterprise,',\
          'set wpa versions wpa2,',\
          'check config success.')
#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'radius server-name auth wlan')
SetCmd(switch1,'radius server-name acct wlan')
SetCmd(switch1,'radius accounting')
SetCmd(switch1,'security mode wpa-enterprise')
SetCmd(switch1,'wpa versions wpa2')
#check
data = SetCmd(switch1,'show wireless network 1',timeout=10)
res1 = CheckLine(data,'Security Mode','WPA Enterprise',IC=True)
res2 = CheckLine(data,'RADIUS Authentication Server Name','wlan',IC=True)
res3 = CheckLine(data,'RADIUS Accounting Server Name','wlan',IC=True)
res4 = CheckLine(data,'WPA Versions','WPA2',IC=True)
# 配置下发
res5 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#result
printCheckStep(testname, 'Step 1 Step 2',res1,res2,res3,res4,res5)
###############################################################################
#Step 2
#操作
# 设置STA1无线网卡的属性为WPA2-Enterprise认证，关联网络Network_name1，使用在Radius服务器配置的用户名和密码。
#预期
# 成功关联，并获取192.168.X.X网段的IP地址。Show wireless client summery
# 可以看到STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
################################################################################
printStep(testname,'Step 2',\
          'STA1 connect to network 1,',\
          'connect success.')
res1=res2=1
#operate
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='wpa2_eap',identity=Dot1x_identity,password=Dot1x_password,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res1==0:
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
        # 退出登陆
        portal_logout_withcheck(web)
    # 关闭网页
    res = web_close(web)
    if res['status'] != True:
        printRes(res)
        CMDKillFirefox(sta1)
################################################################################
#Step 5(合并原方案step6,step7)
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 5',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

EnterNetworkMode(switch1,1)
SetCmd(switch1,'no radius server-name auth')
SetCmd(switch1,'no radius server-name acct')
SetCmd(switch1,'no radius accounting')
SetCmd(switch1,'security mode none')
SetCmd(switch1,'no wpa versions')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)
#end
printTimer(testname, 'End')