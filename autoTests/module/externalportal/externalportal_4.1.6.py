#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# externalportal_4.1.6.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.6 黑白名单url-filter permit和url-filter deny(2.4GHz覆盖)
# 测试目的：验证外置portal认证场景下url黑白名单功能。
# 测试描述：
# 1、	开启外置portal认证,配置黑白名单，并且黑白名单绑定到实例下。
# 2、	STA1不通过认证可以访问白名单
# 3、	STA1通过认证不能访问黑名单
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.20
#*******************************************************************************

#Package

#Global Definition
title='Apache HTTP Server Test Page powered by CentOS'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase externalportal_4.1.6'
avoiderror(testname)
printTimer(testname,'Start','Test Captive-Portal url-filter whilelist and blacklist')

###############################################################################
#Step 1
#操作
# AC1上添加两条白名单、两条黑名单，并将建立好的规则绑定到实例下：
# AC1(config)#url-filter permit 1 *wtest1.com                                                                                      
# AC1(config)#url-filter permit 2 *wtest2.com                                                                                      
# AC1(config)#url-filter deny 1 *btest1.com                                                                                        
# AC1(config)#url-filter deny 2 *btest2.com                                                                                        
# AC1(config)#captive-portal                                                                                                       
# AC1(config-cp)#configuration 1                                                                                                   
# AC1(config-cp-instance)#url-filter permit 1                                                                                      
# AC1(config-cp-instance)#url-filter permit 2                                                                                     
# AC1(config-cp-instance)#url-filter deny 1                                                                                        
# AC1(config-cp-instance)#url-filter deny 2 
#预期
# 配置成功
# 在AC1上面show url-filter status可以看到四条规则
# RuleID为1，host为*wtest1.com,action为permit
# RuleID为2，host为*wtest2.com,action为permit
# RuleID为1，host为*btest1.com,action为deny
# RuleID为2，host为*btest2.com,action为deny
################################################################################
printStep(testname,'Step 1','Add two url-filter whitelist and two blacklist on AC1 and apply to portal')
res1=res2=res3=res4=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'url-filter permit 1 web1.dcntest.com')
SetCmd(switch1,'url-filter permit 2 web2.dcntest.com')
SetCmd(switch1,'url-filter deny 1 web3.dcntest.com')
SetCmd(switch1,'url-filter deny 2 *.abc.com')
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1 ')
SetCmd(switch1,'url-filter permit 1')
SetCmd(switch1,'url-filter permit 2')
SetCmd(switch1,'url-filter deny 1')
SetCmd(switch1,'url-filter deny 2')
EnterEnableMode(switch1)
data = SetCmd(switch1,'show url-filter status',timeout=5)
# print 'data=',data
res1 = CheckLineList(data,[('1','web1.dcntest.com','permit')])
res2 = CheckLineList(data,[('2','web2.dcntest.com','permit')])
res3 = CheckLineList(data,[('1','web3.dcntest.com','deny')])
res4 = CheckLineList(data,[('2',r'\*.abc.com','deny')])
#result
printCheckStep(testname, 'Step 1',res1,res2,res3,res4)
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
    # 客户端STA1未认证通过，使用浏览器访问www.wtest1.com
    #预期
    # www.wtest1.com可以打开
    ################################################################################
    printStep(testname,'Step 3',\
                        'STA1 does not login',\
                        'STA1 can open web1.dcntest.com')
    res1=1
    #operate
    web = web_init(sta1_host)
    if web:
        res1 = open_url_withcheck(web,'http://web1.dcntest.com:90',title=title)
    #result
    printCheckStep(testname, 'Step 3',res1)
    # 关闭网页
    web_close(web)
    ################################################################################
    #Step 4
    #操作
    # 客户端STA1再使用浏览器访问www.wtest2.com
    #预期
    # www.wtest2.com可以打开
    ################################################################################
    printStep(testname,'Step 4',\
                        'STA1 does not login',\
                        'STA1 can open web2.dcntest.com')
    res1=1
    #operate
    web = web_init(sta1_host)
    if web:
        res1 = open_url_withcheck(web,'http://web2.dcntest.com:90',title=title)
    #result
    printCheckStep(testname, 'Step 4',res1)
    # 关闭网页
    web_close(web)
    ################################################################################
    #Step 5
    #操作
    # 客户端STA1未认证通过，使用浏览器访问www.btest1.com
    #预期
    # www.btest1.com无法打开
    ################################################################################
    printStep(testname,'Step 5',\
                        'STA1 does not login',\
                        'STA1 can not open web3.dcntest.com')
    res1=1
    #operate
    web = web_init(sta1_host)
    if web:
        res1 = open_url_withcheck(web,'http://web3.dcntest.com',title=title)
        res1 = 0 if res1 != 0 else 1
    #result
    printCheckStep(testname, 'Step 5',res1)
    # 关闭网页
    web_close(web)
    ################################################################################
    #Step 6
    #操作
    # 客户端STA1未认证通过，使用浏览器访问www.btest2.com
    #预期
    # www.btest2.com无法打开
    ################################################################################
    printStep(testname,'Step 6',\
                        'STA1 does not login',\
                        'STA1 can not open web3.abc.com')
    res1=1
    #operate
    web = web_init(sta1_host)
    if web:
        res1 = open_url_withcheck(web,'http://web3.abc.com',title=title)
        res1 = 0 if res1 != 0 else 1
    #result
    printCheckStep(testname, 'Step 6',res1)
    # 关闭网页
    web_close(web)
    ################################################################################
    #Step 7
    #操作
    # 客户端STA1打开web页面访问1.1.1.1（该地址为变量web_ip），使用正确的用户名和密码登录
    # portal认证用户名：portal_username = 'aaa'
    # portal认证密码：portal_password = '111
    #预期
    # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息，STA1 ping PC1可以ping通
    ################################################################################
    printStep(testname,'Step 7',\
                        'sta1 open http://1.1.1.1',\
                        'sta1 input correct username and password',\
                        'sta1 login successully')
    res1=res2=res3=res4=1
    #operate
    web1 = web_init(sta1_host)
    res1 = exportal_redirect_success(web1,web_ip)
    if res1 == 0:
        res2 = exportal_login_withcheck(web1,portal_username,portal_password)
    res3 = CheckSutCmd(switch1,'show captive-portal client status',\
                                check=[(sta1mac)],retry=5,waitflag=False)
    res4 = CheckPing(sta1,pc1_ipv4,mode='linux')                            
    #result
    printCheckStep(testname, 'Step 7',res1,res2,res3,res4)
    ################################################################################
    #Step 8
    #操作
    # 客户端STA1使用浏览器访问www.btest1.com
    #预期
    # www.btest1.com无法打开
    ################################################################################
    printStep(testname,'Step 8','STA1 can not open web3.dcntest.com')
    res1=1
    #operate
    web = web_init(sta1_host)
    if web:
        res1 = open_url_withcheck(web,'http://web3.dcntest.com',title=title)
        res1 = 0 if res1 != 0 else 1
    #result
    printCheckStep(testname, 'Step 8',res1)
    # 关闭网页
    web_close(web)
    ################################################################################
    #Step 9
    #操作
    # 客户端STA1再次使用浏览器访问www.btest2.com
    #预期
    # www.btest2.com无法打开
    ################################################################################
    printStep(testname,'Step 9','STA1 can not open web3.abc.com')
    res1=1
    #operate
    web = web_init(sta1_host)
    if web:
        res1 = open_url_withcheck(web,'http://web3.abc.com',title=title)
        res1 = 0 if res1 != 0 else 1
    #result
    printCheckStep(testname, 'Step 9',res1)
    # 关闭网页
    web_close(web)
    ################################################################################
    #Step 10
    #操作
    # 客户端STA1使用浏览器访问www.wtest1.com
    #预期
    # www.wtest1.com可以打开
    ################################################################################
    printStep(testname,'Step 10','STA1 can open web1.dcntest.com')
    res1=1
    #operate
    web = web_init(sta1_host)
    if web:
        res1 = open_url_withcheck(web,'http://web1.dcntest.com:90',title=title)
    #result
    printCheckStep(testname, 'Step 10',res1)
    # 关闭网页
    web_close(web)
    ################################################################################
    #Step 11
    #操作
    # 客户端STA1再使用浏览器访问www.wtest2.com
    #预期
    # www.wtest2.com可以打开
    ################################################################################
    printStep(testname,'Step 11','STA1 can open web2.dcntest.com')
    res1=1
    #operate
    web = web_init(sta1_host)
    if web:
        res1 = open_url_withcheck(web,'http://web2.dcntest.com:90',title=title)
    #result
    printCheckStep(testname, 'Step 11',res1)
    # 关闭网页
    web_close(web)
    # 退出登陆并关闭网页
    portal_logout_withcheck(web1)
    web_close(web1)
################################################################################
#Step 12
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 12',\
          'Recover initial config for switches.')

#operate
# sta1解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
CMDKillFirefox(sta1)

EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1 ')
SetCmd(switch1,'no url-filter permit 1')
SetCmd(switch1,'no url-filter permit 2')
SetCmd(switch1,'no url-filter deny 1')
SetCmd(switch1,'no url-filter deny 2')
EnterConfigMode(switch1)
SetCmd(switch1,'no url-filter permit 1')
SetCmd(switch1,'no url-filter permit 2')
SetCmd(switch1,'no url-filter deny 1')
SetCmd(switch1,'no url-filter deny 2')

CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)
#end
printTimer(testname, 'End')