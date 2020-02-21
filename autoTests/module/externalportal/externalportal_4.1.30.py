#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.30.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.30	集群场景下的外置portal认证
# 测试目的：集群形成后, 验证controller上显示portal客户端信息正确
# 测试描述：
# 1.	让AC1和AC2形成集群关系
# 2.	客户端STA1连接网络进行portal认证
# 3.	controller上显示portal客户端信息正确
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.3
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase externalportal_4.1.30'
avoiderror(testname)
printTimer(testname,'Start','Test cluster')
###############################################################################
#Step 1
#操作
# 集群初始环境配置： (AC1变为controller，AP1和AP2都被AC2管理)
# AC1配置
# AC1(config)#wireless                                                                                                                                                                                                          
# AC1(config-wireless)#discovery ip-list StaticIpv4_ac2
# AC1(config-wireless)#no discovery ip-list Ap1_ipv4
# AC1(config-wireless)#no discovery ipv6-list Ap1_ipv6
# AC1(config-wireless)#no discovery ip-list Ap2_ipv4
# AC1(config-wireless)#no discovery ipv6-list Ap2_ipv6
# AC2配置
# AC2(config)#wireless 
# AC2(config-wireless)#discovery ip-list Ap1_ipv4
# AC2(config-wireless)#discovery ipv6-list Ap1_ipv6
# AC2(config-wireless)#discovery ip-list Ap2_ipv4
# AC2(config-wireless)#discovery ipv6-list Ap2_ipv6                                                                                                                                                                                                        
# AC2(config-wireless)#discovery ip-list StaticIpv4_ac1
# 重启AP1、AP2 
#预期
# 配置成功
# AC1上通过命令show wireless  peer-switch显示
# IP Address为StaticIpv4_ac2
# AC2上通过命令show wireless  peer-switch显示
# IP Address为StaticIpv4_ac1
################################################################################
printStep(testname,'Step 1','Config cluster')
res1=res2=res3=1
# operate
# 配置S1
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',StaticIpv4_ac2)
SetCmd(switch1,'no discovery ip-list',Ap1_ipv4)
SetCmd(switch1,'no discovery ipv6-list',Ap1_ipv6)
SetCmd(switch1,'no discovery ip-list',Ap2_ipv4)
SetCmd(switch1,'no discovery ipv6-list',Ap2_ipv6)
SetCmd(switch1,'cluster-priority 255')

# 配置S2
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery ip-list',Ap1_ipv4)
SetCmd(switch2,'discovery ipv6-list',Ap1_ipv6)
SetCmd(switch2,'discovery ip-list',Ap2_ipv4)
SetCmd(switch2,'discovery ipv6-list',Ap2_ipv6)
SetCmd(switch2,'discovery ip-list',StaticIpv4_ac1)
# 重启AP1、AP2
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap1,ap1mac,switch1,Ap1cmdtype)
ChangeAPMode(ap2,ap2mac,switch1,Ap2cmdtype)
IdleAfter(20)
EnterEnableMode(switch1)
res1=CheckSutCmd(switch1,'show wireless peer-switch', \
                check=[(StaticIpv4_ac2)], waittime=5,retry=20,interval=5,IC=True)
res2=CheckSutCmd(switch2,'show wireless peer-switch', \
                check=[(StaticIpv4_ac1)], retry=1,waitflag=False,IC=True)   
res3=CheckSutCmd(switch2,'show wireless ap status', \
                check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],retry=20,waitflag=False,IC=True)    
# 检查AC1为集群controller
res4=CheckSutCmd(switch1,'show wireless', \
                check=[('Cluster Controller','Yes')],retry=1,waitflag=False,IC=True)                
# result
printCheckStep(testname, 'Step 1',res1,res2,res3,res4)
###############################################################################
#Step 2
#操作
# 客户端STA1连接到网络Network_name1
#预期
# 关联成功。
# AC2通过命令show wireless  client  summary可以查看客户端获取到192.168.X.X（Dhcp_pool1）网段的地址
# STA1无法ping通PC1
################################################################################
printStep(testname,'Step 2','STA1 connect to test1')
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res1 == 0:
    res2 = CheckWirelessClientOnline(switch2,sta1mac,'online')
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
    # 客户端STA1打开web页面访问1.1.1.1
    #
    #预期
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 3','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    #operate
    web = web_init(sta1_host)
    res1 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 3',res1)
    ################################################################################
    #Step 4
    #操作
    # 输入正确的用户名和密码进行认证
    # portal认证用户名：portal_username = 'aaa'
    # portal认证密码：portal_password = '111' 
    # AC2上查看CP列表
    # 检查STA1是否可以上网
    #预期
    # 提示用户认证成功，通过show captive-portal  client  status命令查看CP client列表，
    # 显示出STA1的信息（“MAC Address”显示“STA1MAC”）
    # STA1可以ping通PC1
    ################################################################################
    printStep(testname,'Step 4',\
                        'input correct username and password',\
                        'login successully')
    res1=res2=res3=1
    # operate
    res1 = exportal_login_withcheck(web,portal_username,portal_password)
    res2 = CheckSutCmd(switch2,'show captive-portal client status',\
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
    # 在controller上show captive-portal client status可看到peer上报的portal用户信息
    #预期
    # 查看信息正确
    # AC1上通过show captive-portal  client  status命令查看到CP client列表，显示出STA1的信息（“MAC Address”显示“*STA1MAC”）
    ################################################################################
    printStep(testname,'Step 5',\
                        'check portal client on AC1',\
                        'sta1 is in portal client list')
    res1=1
    # operate
    res1 = CheckSutCmd(switch1,'show captive-portal client status',\
                                check=[(sta1mac)],retry=5,waitflag=False)
    #result
    printCheckStep(testname, 'Step 5',res1)
    ################################################################################
    #Step 6
    #操作
    # controller显示上portal客户端所在位置为peer switch
    #预期
    # AC1上通过show captive-portal client STA1MAC  ipv4  STA1IP status显示Switch Type为peer
    ################################################################################
    printStep(testname,'Step 6',\
                        'sta is managed by AC\'s peer switch')
    res1=1
    # operate
    res1 = CheckSutCmd(switch1,'show captive-portal client '+sta1mac+' ipv4 '+sta1_ipv4+' status',\
                        check=[('Switch Type','Peer')],retry=1,waitflag=False,IC=True)
    #result
    printCheckStep(testname, 'Step 6',res1)
    
################################################################################
#Step 7
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 7',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
# 配置S1
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',Ap1_ipv4)
SetCmd(switch1,'discovery ipv6-list',Ap1_ipv6)
SetCmd(switch1,'discovery ip-list',Ap2_ipv4)
SetCmd(switch1,'discovery ipv6-list',Ap2_ipv6)
SetCmd(switch1,'no discovery ip-list',StaticIpv4_ac2)
SetCmd(switch1,'no enable')
IdleAfter(3)
SetCmd(switch1,'enable')
# 配置S2
EnterWirelessMode(switch2)
SetCmd(switch2,'no discovery ip-list',StaticIpv4_ac1)
SetCmd(switch2,'no discovery ip-list',Ap1_ipv4)
SetCmd(switch2,'no discovery ipv6-list',Ap1_ipv6)
SetCmd(switch2,'no discovery ip-list',Ap2_ipv4)
SetCmd(switch2,'no discovery ipv6-list',Ap2_ipv6)
SetCmd(switch2,'no enable')
IdleAfter(3)
SetCmd(switch2,'enable')
# 重启AP1、AP2
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap1,ap1mac,switch2,Ap1cmdtype)
ChangeAPMode(ap2,ap2mac,switch2,Ap2cmdtype)
IdleAfter(20)
EnterEnableMode(switch1)  
CheckSutCmd(switch1,'show wireless ap status', \
            check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')], \
            waittime=5,retry=20,interval=5,IC=True)

#end
printTimer(testname, 'End')