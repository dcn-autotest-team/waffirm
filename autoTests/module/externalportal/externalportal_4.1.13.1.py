#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.13.1.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.13.1 WPA-Personal模式下客户端的外置portal认证((2.4GHz覆盖)
# 测试目的：验证SSID采用WPA-Personal加密后开启portal认证，客户端连接网络能够正常进行外置portal认证
# 测试描述：
# 1.	修改network1的加密方式为WPA
# 2.	STA1连接网络后可以正常进行外置portal认证
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

testname = 'TestCase externalportal_4.1.13.1'
avoiderror(testname)
printTimer(testname,'Start','Test portal with wpa-personal mode')
###############################################################################
#Step 1(合并方案step1,2)
#操作
# AC1上设置network1的加密方式为混合模式：WPA -Personal，密码为abcd1234                                                                                                                    
# AC1(config)#wireless 
# AC1(config-wireless)#network 1                                                                                                      
# AC1(config-network)#security mode wpa-personal                                                                                                                            
# AC1(config-network)#wpa key abcd1234                                                                                                                                                                                                                                                                                                             
# AC1(config-network)#wpa versions wpa                                                                                                  
# AC1(config-network)#exit 
#预期
# 配置成功。在AC1上面Show wireless network 1可以看到相关的配置
################################################################################
printStep(testname,'Step 1 Step 2',\
          'set network security mode wep-personal mode,',\
          'set wpa versions wpa.',\
          'show wireless network 1 and config success.')
res1,res2,res3,res4=1,1,0,1
#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'security mode wpa-personal')
SetCmd(switch1,'wpa key abcd1234')
SetCmd(switch1,'wpa versions wpa')
#check
data1 = SetCmd(switch1,'show wireless network 1',timeout = 10)
res1 = CheckLine(data1,'Security Mode','WPA Personal')
res2 = CheckLine(data1,'WPA Versions','WPA')
res3 = CheckLine(data1,'WPA Versions','WPA2')
res4 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# result
printCheckStep(testname, 'Step 1 Step 2',res1,res2,not res3,res4)
###############################################################################
#Step 2
#操作
# 设置STA1无线网卡的属性为WPA-PSK认证，正确输入密码，关联网络Network_name1。
#预期
# 成功关联，并获取192.168.X.X网段的IP地址。Show wireless client summery
# 可以看到STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
################################################################################
printStep(testname,'Step 2',\
          'STA1 connect to network 1,',\
          'connect success.')
res1=res2=1
#operate
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='wpa_psk',psk='abcd1234',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
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
        # 退出登陆
        portal_logout_withcheck(web)
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

EnterNetworkMode(switch1,1)
SetCmd(switch1,'security mode none')
SetCmd(switch1,'no wpa key')
SetCmd(switch1,'no wpa versions')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)
#end
printTimer(testname, 'End')