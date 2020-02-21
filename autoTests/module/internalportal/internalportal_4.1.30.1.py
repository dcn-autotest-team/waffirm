#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# internal_portal_4.1.30.1.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# 4.1.30.1	AP逃生客户端不下线场景下的portal认证
# 测试目的：开启AP逃生功能，AP逃生后，AP直接放行客户端流量
# 测试描述：
# 1、	开启AP逃生功能，STA1连接到无线网络成功进行portal认证
# 2、	AP逃生后，STA2连接到无线网络
# 3、	AP逃生恢复后，检查STA1和STA2是否放行客户端流量
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

testname = 'TestCase internalportal_4.1.30.1'
avoiderror(testname)
printTimer(testname,'Start','Test ap escape and ap escape client-persist')
################################################################################
#Step 1（合并方案step1,step2)
#操作
# AC1上开启AP逃生客户端不下线
# AC1(config)#wireless                                                                                                                
# AC1(config-wireless)#ap profile  1                                                                                                  
# AC1(config-ap-profile)#ap escape                                                                                                    
# AC1(config-ap-profile)#ap escape client-persist
# 将配置下发到AP1。
# Wireless ap profile apply 1
#预期
# 配置成功
# AC1上通过命令show wireless  ap profile 1显示
# AP Escape为Enable
# AP Escape Client Persist Mode为Enable
# 配置下发成功。
# AP1上通过命令get system查看到apescape-client-persist 为up
################################################################################
printStep(testname,'Step 1','Config ap escape and ap escape client-persist')
res1=res2=1
#operate
EnterApProMode(switch1,1)
SetCmd(switch1,'ap escape')
SetCmd(switch1,'ap escape client-persist')

# check
data=SetCmd(switch1,'show wireless  ap profile 1')
res1 = CheckLineList(data,[('AP Escape','Enable'),('AP Escape Client Persist Mode','Enable')])
res2 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# 为兼容不同型号AP，AP上只打印get system detail，不做检查
ApSetcmd(ap1,Ap1cmdtype,'getsystem','detail')
#result
printCheckStep(testname, 'Step 1',res1,res2)
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
    ################################################################################
    #Step 4
    #操作
    # 客户端STA1在推送出的重定向页面输入正确的用户名和密码进行认证
    # portal认证用户名：portal_username = ‘aaa’
    # portal认证密码：portal_password = ‘111
    # 查看AC1上的CP列表
    # 检查STA1是否可以上网
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
    # 关闭网页
    web_close(web)
    ###############################################################################
    #Step 5
    #操作
    # AP逃生，让AP脱离AC管理
    # 关闭AC1连接AP的口s1p1
    # AC1(config)#interface s1p1                                                                                                
    # AC1(config-if- s1p1)#shutdown
    #预期
    # AP逃生
    # AC1上通过命令show wireless  ap status查看不到AP表项
    ################################################################################
    printStep(testname,'Step 5','Shutdown s1p1 and ap escape')
    res1=1
    #operate
    EnterConfigMode(switch1)
    SetCmd(switch1,'interface',s1p1)
    SetCmd(switch1,'shutdown')
    IdleAfter(10)
    res1 = CheckSutCmdWithNoExpect(switch1,'show wireless  ap status',\
                                check=[(ap1mac,'Managed','Success')],retry=10,waitflag=False)
    #result
    printCheckStep(testname, 'Step 5',res1)
    ################################################################################
    #Step 6
    # STA2连接到AP1的Network_name1
    #预期
    # 关联成功。
    # sta2可以正常上网
    ################################################################################
    printStep(testname,'Step 6','STA2 connect to test1')
    res1=res2=1
    #operate
    #STA2关联 network1
    res1 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
    res2 = CheckPing(sta2,pc1_ipv4,mode='linux')
    #result
    printCheckStep(testname, 'Step 6',res1,res2)
    ###############################################################################
    #Step 7
    #操作
    # 查看客户端STA1跟 AP的关联情况
    #预期
    # 客户端STA1仍然关联网络
    # AP1上使用命令get association可以看到关联的客户端STA1信息
    # station显示为STA1MAC
    # ip显示为STA1IP
    # STA1可以ping通PC1
    ################################################################################
    printStep(testname,'Step 7',\
                        'sta1 is still in client list',\
                        'sta1 ping pc1 successully')
    res1=res2=1
    #operate
    # 为兼容不同型号AP，AP上只打印信息，不做检查
    SetCmd(ap1,'get association')
    res2 = CheckPing(sta1,pc1_ipv4,mode='linux')                    
    #result
    printCheckStep(testname, 'Step 7',res2)
    ###############################################################################
    #Step 8
    #操作
    # 查看客户端STA2跟 AP的关联情况
    #预期
    # 客户端STA2仍然关联网络
    # AP1上使用命令get association可以看到关联的客户端STA2信息
    # station显示为STA2MAC
    # ip显示为STA2IP
    # STA2可以ping通PC1
    ################################################################################
    printStep(testname,'Step 8',\
                        'sta2 is still in client list',\
                        'sta2 ping pc1 successully')
    res1=res2=1
    #operate
    # 为兼容不同型号AP，AP上只打印信息，不做检查
    SetCmd(ap1,'get association')
    res2 = CheckPing(sta2,pc1_ipv4,mode='linux')                    
    #result
    printCheckStep(testname, 'Step 8',res2)
    ################################################################################
    #Step 9
    #操作
    # AP逃生恢复，AP再次被AC管理
    # 开启AC1连接AP的口s1p1
    # AC1(config)#interface s1p1                                                                                                
    # AC1(config-if- s1p1)#no shutdown
    #预期
    # AP成功被AC管理
    # AC1上通过命令show wireless  ap status查看到AP表项
    ################################################################################
    printStep(testname,'Step 9','No shutdown s1p1 and AC managed ap')
    res1=1
    EnterConfigMode(switch1)
    SetCmd(switch1,'interface',s1p1)
    SetCmd(switch1,'no shutdown')
    IdleAfter(15)
    # check
    res1 = CheckSutCmd(switch1,'show wireless ap status',\
                        check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],retry=10,waitflag=False)
    #result
    printCheckStep(testname, 'Step 9',res1)
    ################################################################################
    #Step 10
    #操作
    # 检查客户端STA1和STA2的网络连接状态
    #预期
    # 客户端STA1和STA2仍然在线
    # AC1上通过命令show wireless  client  status可以查看到STA1和STA2的表项
    # AC1上通过命令show captive-portal  client  status查看不到任何表项
    # STA1和STA2都可以ping通PC1
    ################################################################################
    printStep(testname,'Step 10','sta1 and sta2 are still in client list but not in portal client list',\
                                'sta1 and sta2 ping pc1 successully')
    res1=res2=res3=res4=res5=1
    # operate
    res1 = CheckSutCmd(switch1,'show wireless  client  status',\
                                check=[(sta1mac),(sta2mac)],retry=10,waitflag=False)
    res2 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                            check=[(sta1mac)],retry=1,waitflag=False)
    res3 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                            check=[(sta2mac)],retry=1,waitflag=False)
    res4 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res5 = CheckPing(sta2,pc1_ipv4,mode='linux')
    #result
    printCheckStep(testname, 'Step 10',res1,res2,res3,res4,res5)
    
################################################################################
#Step 11(合并原方案step12,step13)
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 11',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)
EnterApProMode(switch1,1)
SetCmd(switch1,'no ap escape',timeout=2)
SetCmd(switch1,'y')
SetCmd(switch1,'no ap escape client-persist',timeout=1)
SetCmd(switch1,'y')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

#end
printTimer(testname, 'End')