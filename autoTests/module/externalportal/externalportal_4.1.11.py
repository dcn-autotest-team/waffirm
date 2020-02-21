#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.11.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.11	多vap的portal功能验证
# 测试目的：验证开启多个vap 的portal功能
# 测试描述：
# 1.	新建多个network并且开启多个vap
# 2.	将新建立的network绑定到实例下
# 3.	STA1连接到任意一个SSID都可以成功进行portal认证
# 4.	关闭部分vap的portal功能
# 5.	STA1连接没有开启portal功能的vap无需认证可以直接上网
# 6.	STA1连接开启了portal功能的vap可以成功进行portal认证
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.21
#*******************************************************************************

#Package

#Global Definition
ap1mac_type1_network3 = incrmac(ap1mac_type1,2)
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase externalportal_4.1.11'
avoiderror(testname)
printTimer(testname,'Start','Test multi-vap portal')
###############################################################################
#Step 1
#操作
# 新建1个network，并且开启对应的vap                                                                                      
# AC1(config-network)#network 3                                                                                                    
# AC1(config-network)#ssid Network_name3                                                                                                  
# AC1(config-network)#vlan Vlan4093                                                                                                                                                                                                          
# AC1(config-wireless)#ap profile 1                                                                                               
# AC1(config-ap-profile)#radio 1                                                                                                                                                                                                  
# AC1 (config-ap-profile-radio)#vap 2                                                                                               
# AC1 (config-ap-profile-vap)#enable                                                                                                                                                                                               
# AC1 (config-ap-profile-vap)#end                                                                                                   
# AC1#wireless ap profile apply 1 
#预期
# 配置成功。
# 在AC1上通过命令
# show wireless network 3 status
# 可以看到network3的相关配置
# SSID为Network_name3  Default VLAN为Vlan4093  
################################################################################
printStep(testname,'Step 1','config vap')
res1=1
#operate
EnterNetworkMode(switch1,3)
SetCmd(switch1,'ssid',Network_name3)
SetCmd(switch1,'vlan',Vlan4093)
EnterApProMode(switch1,1)
SetCmd(switch1,'radio',radionum)
SetCmd(switch1,'vap 2')
SetCmd(switch1,'enable')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

data = SetCmd(switch1,'show wireless network 3')
res1 = CheckLine(data,'Default VLAN',Vlan4093)
#result
printCheckStep(testname, 'Step 1',res1)
###############################################################################
#Step 2
#操作
# 将新建立的network绑定到实例下
# AC1(config)#captive-portal                                                                                                       
# AC1(config-cp)#configuration 1                                                                                                   
# AC1(config-cp-instance)#interface  ws-network  2                                                                                                                                                                                                                                                                                                   
# AC1(config-cp-instance)#interface  ws-network  3
#预期
# 绑定成功。
# AC1上通过命令show run可以查看到命令：
 # interface ws-network 1                                                                                                            
 # interface ws-network 2                                                                                                            
 # interface ws-network 3 
################################################################################
printStep(testname,'Step 2','band network 2,3 to configuration 1')
res1=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'interface ws-network 2')
SetCmd(switch1,'interface ws-network 3')
data = SetCmd(switch1,'show run c')
res1 = CheckLine(data,'interface ws-network 1','interface ws-network 2','interface ws-network 3',ML=True)

#result
printCheckStep(testname, 'Step 2',res1)
###############################################################################
#Step 3
#操作
# 客户端STA1连接到网络Network_name2
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端STA1获取到192.168.X.X(Dhcp_pool2)网段的地址
################################################################################
printStep(testname,'Step 3','STA1 connect to test2')
res1=res2=1
#operate
#STA1关联 network2
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name2,checkDhcpAddress=Netcard_ipaddress_check2,bssid=ap1mac_type1_network2)
if res1 == 0:
	res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
#result
printCheckStep(testname, 'Step 3',res1,res2)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag): 
    ################################################################################
    #Step 4
    #操作
    # 客户端STA1打开web页面访问1.1.1.1（该地址为变量web_ip）
    #预期
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 4','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    # operate
    # sta1打开1.1.1.1，并检查是否重定向到外置portal认证页面
    web = web_init(sta1_host)
    res1 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 4',res1)
    if res1 == 0:
        ################################################################################
        #Step 5
        #操作
        # 客户端STA1在推送出的重定向页面输入正确的用户名和密码进行认证
        # portal认证用户名：portal_username = ‘aaa’
        # portal认证密码：portal_password = ‘111
        #预期
        # STA1认证成功
        # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）。
        # STA1ping PC1可以ping通
        ################################################################################
        printStep(testname,'Step 5',\
                            'input correct username and password',\
                            'login successully')
        res1=res2=res3=1
        # operate
        res1 = exportal_login_withcheck(web,portal_username,portal_password)
        res2 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        #result
        printCheckStep(testname, 'Step 5',res1,res2,res3)
    # 关闭网页
    web_close(web)
###############################################################################
#Step 6
#操作
# 客户端STA1连接到网络Network_name3
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端STA1获取到192.168.X.X(Dhcp_pool3)网段的地址。    
# 通过命令show captive-portal  client  status查看不到任何表项
################################################################################
printStep(testname,'Step 6','STA1 connect to test3')
res1=res2=res3=1
#operate
#STA1关联 network3
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name3,checkDhcpAddress=Dhcp_pool3,bssid=ap1mac_type1_network3)
if res1 == 0:
	res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
res3 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                check=[(sta1mac)],retry=10,waitflag=False)
#result
printCheckStep(testname, 'Step 6',res1,res2,res3)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag): 
    ################################################################################
    #Step 7
    #操作
    # 客户端STA1打开web页面访问1.1.1.1（该地址为变量web_ip）
    #预期
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 7','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    # operate
    # sta1打开1.1.1.1，并检查是否重定向到外置portal认证页面
    web = web_init(sta1_host)
    res1 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 7',res1)
    if res1 == 0:
        ################################################################################
        #Step 8
        #操作
        # 客户端STA1在推送出的重定向页面输入正确的用户名和密码进行认证
        # portal认证用户名：portal_username = ‘aaa’
        # portal认证密码：portal_password = ‘111
        #预期
        # STA1认证成功
        # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）。
        # STA1ping PC1可以ping通
        ################################################################################
        printStep(testname,'Step 8',\
                            'input correct username and password',\
                            'login successully')
        res1=res2=res3=1
        # operate
        res1 = exportal_login_withcheck(web,portal_username,portal_password)
        res2 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        #result
        printCheckStep(testname, 'Step 8',res1,res2,res3)
    # 关闭网页
    web_close(web)
################################################################################
#Step 9
#操作
# 对network2的portal功能去绑定
# AC1(config)#captive-portal                                                                                                       
# AC1(config-cp)#configuration 1                                                                                                   
# AC1(config-cp-instance)#no interface  ws-network  2  
#预期
# 去绑定成功。
# AC1上通过命令show captive-portal  interface configuration 1 status，查看不到network 2的信息
################################################################################
printStep(testname,'Step 9','cancel band network 2 to configuration 1')
res1=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'no interface ws-network 2')
res1 = CheckSutCmdWithNoExpect(switch1,'show captive-portal interface configuration 1 status',\
                                        check=[('network 2')],retry=1,waitflag=False)

#result
printCheckStep(testname, 'Step 9',res1)
###############################################################################
#Step 10
#操作
# 客户端STA1连接到网络Network_name2
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端STA1获取到192.168.X.X(Dhcp_pool2)网段的地址
################################################################################
printStep(testname,'Step 10','STA1 connect to test2')
res1=res2=1
#operate
#STA1关联 network2
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name2,checkDhcpAddress=Netcard_ipaddress_check2,bssid=ap1mac_type1_network2)
if res1 == 0:
	res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
#result
printCheckStep(testname, 'Step 10',res1,res2)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ###############################################################################
    #Step 11
    #操作
    # 检查STA1上网是否可以上网
    #预期
    # STA1可以ping通PC1
    # 通过命令show captive-portal aip status查看不到任何表项
    # 通过命令show captive-portal client status查看不到任何表项
    ################################################################################
    printStep(testname,'Step 11','STA1 ping pc1 failed')
    res1=res2=res3=1
    #operate
    res1 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res2 = CheckSutCmdWithNoExpect(switch1,'show captive-portal aip status',\
                                    check=[(sta1_ipv4,sta1mac)],retry=10,waitflag=False)
    res3 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=10,waitflag=False)
    #result
    printCheckStep(testname, 'Step 11',res1,res2,res3)
###############################################################################
#Step 12
#操作
# 客户端STA1连接到网络Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端STA1获取到192.168.X.X(Dhcp_pool1)网段的地址
################################################################################
printStep(testname,'Step 12','STA1 connect to test1')
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res1 == 0:
	res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
#result
printCheckStep(testname, 'Step 12',res1,res2)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 13
    #操作
    # 客户端STA1打开web页面访问1.1.1.1
    #
    #预期
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 13','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    #operate
    web = web_init(sta1_host)
    res1 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 13',res1)
    if res1 == 0:
        ################################################################################
        #Step 14
        #操作
        # 客户端STA1在推送出的重定向页面输入正确的用户名和密码进行认证
        # portal认证用户名：portal_username = 'aaa'
        # portal认证密码：portal_password = '111
        #预期
        # STA1认证成功
        # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）。
        # STA1ping PC1可以ping通
        ################################################################################
        printStep(testname,'Step 14',\
                            'input correct username and password',\
                            'login successully')
        res1=res2=res3=1
        # operate
        res1 = exportal_login_withcheck(web,portal_username,portal_password)
        res2 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        #result
        printCheckStep(testname, 'Step 14',res1,res2,res3)
        # 退出登陆
        portal_logout_withcheck(web)
    # 关闭网页
    web_close(web)
################################################################################
#Step 15
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 15',\
          'Recover initial config for switches.')

#operate
# sta1解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
# 恢复配置
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'no interface ws-network 3')
EnterApProMode(switch1,1)
SetCmd(switch1,'radio',radionum)
SetCmd(switch1,'vap 2')
SetCmd(switch1,'no enable')
ClearNetworkConfig(switch1,3)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
CMDKillFirefox(sta1)
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)
#end
printTimer(testname, 'End')