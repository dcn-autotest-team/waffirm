#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.23.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.23	集中转发下的外置portal认证
# 测试目的：集中转发下，客户端连接网络能够正常进行外置portal认证
# 测试描述：
# 1.	修改测试环境为集中转发
# 2.	客户端STA1在认证页面填写正确的用户名和密码能够通过认证
# 3.	客户端STA1通过认证后可以主动下线
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.28
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase externalportal_4.1.23'
avoiderror(testname)
printTimer(testname,'Start','Test centralized forwarding')
###############################################################################
#Step 1
#操作
# 添加Vlan 4091到集中隧道
# 修改S3p3 access vlan 为vlan20，S3p4 access vlan为vlan30
# AC1(config-wireless)#l2tunnel vlan-list vlan4091  
# 客户端STA1连接到网络Network_name1
#预期
# 设置成功
# AC上通过命令show wireless l2-tunnel vlan-list可以看到vlan4091
################################################################################
printStep(testname,'Step 1','add l2tunnel vlan-list vlan4091 ')
res1 = 1
# operate
# 配置S1
EnterConfigMode(switch1)
SetCmd(switch1,'vlan',Vlan4091)
EnterInterfaceMode(switch1,'vlan '+Vlan4091)
IdleAfter(Vlan_Idle_time)
SetCmd(switch1,'ip address',Dhcp_pool1+'180','255.255.255.0')
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport mode trunk')
SetCmd(switch1,'switchport trunk native vlan',Vlan40)

# 配置S3
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan40)
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'switchport mode access')
SetCmd(switch3,'switchport access vlan',Vlan20)
EnterInterfaceMode(switch3,s3p4)
SetCmd(switch3,'switchport mode access')
SetCmd(switch3,'switchport access vlan',Vlan30)

EnterWirelessMode(switch1)
SetCmd(switch1,'l2tunnel vlan-list',Vlan4091)
# check
data = SetCmd(switch1,'show wireless l2tunnel vlan-list ')
res1 = CheckLine(data,Vlan4091)
# result
printCheckStep(testname, 'Step 1',res1)
###############################################################################
#Step 2(合并方案step2/step3)
#操作
# 客户端STA1连接到网络Network_name1
# 检查AC1是否放行STA1的流量
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端获取到192.168.X.X（Dhcp_pool1）网段的地址
# STA1无法ping通PC1
################################################################################
printStep(testname,'Step 2','STA1 connect to test1 and ping pc1 failed')
res1=res2=res3=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res1 == 0:
    res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
    # 检查sta1无法ping通pc1
    res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res3=0 if res3 !=0 else -1
#result
printCheckStep(testname, 'Step 2',res1,res2,res3)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ###############################################################################
    #Step 3
    #操作
    # 在ap上查看客户端的portal状态
    # cp_debug sta;dmesg -c
    #预期
    # Ap的串口打印中CP Client Table下显示出STA1的
    # mac地址为：sta1_mac
    # ip地址为：sta1_ipv4
    # state : UNAUTHED
    ################################################################################
    printStep(testname,'Step 3','cp_debug sta;dmesg -c on AP1')
    # operate
    # 为兼容不同型号AP，AP上只打印信息，不做检查
    SetCmd(ap1,'cp_debug sta;dmesg -c')
    #result
    printCheckStep(testname, 'Step 3',0)
    ################################################################################
    #Step 4
    #操作
    # 客户端STA1打开web页面访问1.1.1.1
    #
    #预期
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 4','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    #operate
    web = web_init(sta1_host)
    res1 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 4',res1)
    ################################################################################
    #Step 5
    #操作
    # 重新输入正确的用户名和密码进行认证
    # portal认证用户名：portal_username = 'aaa'
    # portal认证密码：portal_password = '111' 
    # AC1上查看CP列表
    # 检查AC1是否放行STA1的流量
    #预期
    # 提示用户认证成功，通过show captive-portal  client  status命令查看CP client列表，
    # 显示出STA1的信息（“MAC Address”显示“STA1MAC”）
    # STA1可以ping通PC1
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
    ###############################################################################
    #Step 6
    #操作
    # 在ap上查看客户端的portal状态
    # cp_debug sta;dmesg -c
    #预期
    # Ap的串口打印中CP Client Table下显示出STA1的信息
    # mac地址为：sta1_mac
    # ip地址为：sta1_ipv4
    # state : AUTHED
    ################################################################################
    printStep(testname,'Step 6','cp_debug sta;dmesg -c on AP1')
    # operate
    # 为兼容不同型号AP，AP上只打印信息，不做检查
    SetCmd(ap1,'cp_debug sta;dmesg -c')
    #result
    printCheckStep(testname, 'Step 6',0)
    ################################################################################
    #Step 7
    #操作
    # 在推送出来的认证成功页面点击“下线”，STA1能够成功下线
    # 查看AC1上的CP列表
    # 检查STA1是否可以上网 
    #预期
    # 页面提示“成功下线”；
    # 通过show captive-portal  client  status命令查看没有CP client列表
    # STA1无法ping通PC1
    ################################################################################
    printStep(testname,'Step 7','sta1 logout')
    # opertate
    # 退出登陆
    res1 = portal_logout_withcheck(web)
    # AC1上检查不存在sta1的portal用户表项
    res2 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=10,waitflag=False)
    IdleAfter(10)
    # 检查sta1无法ping通pc1
    res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res3=0 if res3 !=0 else -1  
    #result
    printCheckStep(testname, 'Step 7',res1,res2,res3)
    # 关闭网页
    res = web_close(web)
    if res['status'] != True:
        printRes(res)
        CMDKillFirefox(sta1)
################################################################################
#Step 8
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 8',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
# 配置S1
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport mode access')
SetCmd(switch1,'switchport access vlan',Vlan40)
EnterWirelessMode(switch1)
SetCmd(switch1,'no l2tunnel vlan-list')
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan',Vlan4091)
SetCmd(switch1,'no vlan',Vlan4091)
# 配置S3
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport mode access')
SetCmd(switch3,'switchport access vlan',Vlan40)
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan20)
EnterInterfaceMode(switch3,s3p4)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan30)

#end
printTimer(testname, 'End')