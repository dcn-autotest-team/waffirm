#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# internal_portal_4.1.34py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# 4.1.34	内置portal外置web页面认证
# 测试目的：验证开启内置portal外置web页面功能后，portal认证正常
# 测试描述：
# 1、	开启并配置内置portal外置web页面功能
# 2、	STA进行内置portal认证，重定向的是外置web页面，输入正确的用户名密码认证成功
# 3、	STA主动下线成功
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.10
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code
def inportal_expage_login(sel,username,password):
    try:
        if sel.is_element_present('name=PtUser'):
            sel.type("name=PtUser", username)
        else:
            return {'status':False,'Message':'Can NOT find space to type username'}
        if sel.is_element_present('name=PtPwd'):
            sel.type("name=PtPwd", password)
        else:
            return {'status':False,'Message':'Can NOT find space to type password'}
        if sel.is_element_present('name=PtButton'):
            sel.click("name=PtButton")
        else:
            return {'status':False,'Message':'Can NOT find button to commit username and password'}
        time.sleep(20)
        checkstring = '登陆成功'
        if sel.is_text_present(checkstring):
            return {'status':True,'Message':'Inner Portal login success'}
        else:
            return {'status':False,'Message':'Something wrong when portal login'}
    except Exception:
        return {'status':False,'Message':'Warning: throw exception when run portal_login'}
        
def inportal_expage_logout(sel):
    try:
        checkstring='登陆成功'
        if sel.is_text_present(checkstring):
            if sel.is_element_present('name=PtButton'):
                sel.click("name=PtButton")
                return {'status':True,'Message':'Inner portal logout success!'}
            else:
                return {'status':False,'Message':'Can NOT find logout button in this page'}
        else:
            return {'status':False,'Message':'Page is not the login success page'}
    except Exception:
        return {'status':False,'Message':'Warning: throw exception when run portal_logout'}
        
testname = 'TestCase internalportal_4.1.34'
avoiderror(testname)
printTimer(testname,'Start','Test ext-web-server')
################################################################################
#Step 1
#操作
# AC1上开启并配置内置portal外置web页面功能：
# captive-portal                                                                                                          
# configuration 1                                                                                                      
# ext-web-server enable
# ext-web-server login-url http://ext_web_server/login.htm
# ext-web-server logout-url http://ext_web_server/logout.htm
# ext-web-server login-failure-url http://ext_web_server/login_failure.htm
# ext-web-server logout-success-url http://ext_web_server/logout_success.htm 
#预期
# 配置成功
# AC1上通过命令show captive-portal configuration 1 status查看：
# Ext-web-server Mode............................ Enable                                                                              
# Ext-web-server Login-url....................... http://ext_web_server/login.htm                                                     
# Ext-web-server Login-failure-url............... http://ext_web_server/login_failure.htm                                             
# Ext-web-server Logout-url...................... http://ext_web_server/logout.htm                                                    
# Ext-web-server Logout-success-url.............. http://ext_web_server/logout_success.htm 
################################################################################
printStep(testname,'Step 1','Config ext-web-server')
res1=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'ext-web-server enable')
SetCmd(switch1,'ext-web-server login-url http://192.168.10.104/portal/logon.htm')
SetCmd(switch1,'ext-web-server login-failure-url http://192.168.10.104/portal/logonFail.htm')
SetCmd(switch1,'ext-web-server logout-url http://192.168.10.104/portal/logonSuccess.htm')
SetCmd(switch1,'ext-web-server logout-success-url http://192.168.10.104/portal/logoffSuccess.htm')
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'free-resource 2 destination ipv4 192.168.10.104/32 source any')
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'free-resource 2')
# check
IdleAfter(5)
data=SetCmd(switch1,'show captive-portal configuration 1 status')
res1 = CheckLineList(data,[('Ext-web-server Mode','Enable'),
                           ('Ext-web-server Login-url','http://192.168.10.104/portal/logon.htm'),
                           ('Ext-web-server Login-failure-url'),('http://192.168.10.104/portal/logonFail.htm'),
                           ('Ext-web-server Logout-url'),('http://192.168.10.104/portal/logonSuccess.htm'),
                           ('Ext-web-server Logout-success-url'),('http://192.168.10.104/portal/logoffSuccess.htm')])
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
    # STA1上可以看到重定向页面，重定向的页面是“http://ext_web_server/”并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 3','sta1 open 1.1.1.1 and can redirect to external_portal auth page')
    res1=1
    # operate
    # sta1打开1.1.1.1，并检查是否重定向到外置portal认证页面
    web = web_init(sta1_host)
    res1 = open_url_withcheck(web,web_ip,title = '欢迎登录北京林业大学无线网络认证页面 Welcome to Bjfu-WIFI logon Portal')
    #result
    printCheckStep(testname, 'Step 3',res1)
    if res1 == 0:
        ################################################################################
        #Step 4
        #操作
        # 输入正确的用户名和密码进行认证
        # portal认证用户名：portal_username = 'aaa'
        # portal认证密码：portal_password = '111' 
        #预期
        # STA1认证成功
        # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）。
        # STA1ping PC1可以ping通
        ################################################################################
        printStep(testname,'Step 4',
                            'input correct username and password',
                            'login successully')
        res1=res2=res3=1
        # operate
        resa = inportal_expage_login(web,'aaaaaa','111111')
        if resa['status'] == True:
            res1 = 0
        else:
            print(resa)
        res2 = CheckSutCmd(switch1,'show captive-portal client status',
                           check=[(sta1mac)],retry=5,waitflag=False)
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        #result
        printCheckStep(testname, 'Step 4',res1,res2,res3)
        ################################################################################
        #Step 5
        #操作
        # STA1主动进行portal下线
        #预期
        # 下线成功
        # show captive-portal  client  status命令查看CP client列表为空；
        # STA1 ping pc1_ipv4不通
        ################################################################################
        printStep(testname,'Step 5','sta1 logout')
        res1=res2=res3=1
        # opertate
        # 退出登陆
        resa = inportal_expage_logout(web)
        if resa['status'] == True:
            res1 = 0
        else:
            print(resa)
        # AC1上检查不存在sta1的portal用户表项
        res2 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',
                                       check=[(sta1mac)],retry=10,waitflag=False)
        # 检查sta1无法ping通pc1
        IdleAfter(10)
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        res3=0 if res3 !=0 else -1  
        #result
        printCheckStep(testname, 'Step 5',res1,res2,res3)
        # 关闭网页
        res = web_close(web)
        if res['status'] != True:
            printRes(res)
            CMDKillFirefox(sta1)
################################################################################
#Step 6
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 6',
          'Recover initial config for switches.')

#operate
# sta1解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'no ext-web-server enable')
SetCmd(switch1,'no ext-web-server login-url')
SetCmd(switch1,'no ext-web-server login-failure-url')
SetCmd(switch1,'no ext-web-server')
SetCmd(switch1,'no ext-web-server logout-success-url')
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'no free-resource 2')
SetCmd(switch1,'exit')
SetCmd(switch1,'no free-resource 2')

CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',
                        check=[(sta1mac)],retry=10,waitflag=False)

#end
printTimer(testname, 'End')