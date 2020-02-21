#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_mt5053_portal.py 
#
# Author: 
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# mt5053
# 测试目的：无线用户STA1认证通过后获取到IP1,手工更改无线用户STA1 IP1地址为IP2后,
# 手工设置无线用户STA2的IP地址为IP1,无线用户STA2能成功通过portal认证。
# 测试环境：同测试拓扑
# 测试描述：1.客户端STA1连接无线网络后成功通过认证。
# 2.更改STA1的IP地址STA1IP为静态IP地址STA1IP1,在AC上查看CP-client表STA1的IP为更改后的IP。
# 3.手工设置客户端STA2的IP为STA1IP,STA2连接无线网络后能成功通过认证。
# 4.恢复初始设置
#
#*******************************************************************************
# Change log:
#     - creadte by zhangjxp 2017.5.22
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase mt5053_portal'
avoiderror(testname)
printTimer(testname,'Start')
###############################################################################
#Step 1
#操作
#在AC1上配置radius相关配置和portal相关配置
# 在Profile 1和Profile 2下开启快速IP上报功能，重新下发Profile 1。
#
#预期
#AP1和AP2成功被AC1管理
# ，显示两条记录为
# MAC Address为AP1MAC，IP Address为AP1IP，Profile显示为1
# 和
# MAC Address为AP2MAC，IP Address为AP2IP，Profile显示为2
################################################################################
printStep(testname,'Step 1',
          'Config Extrnal portal Configuration on AC1',
          'Config quick-ip-report in profile 1 and 2',
          'Apply ap profile 1 and 2')
res1=res2=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'radius source-ipv4 ' + StaticIpv4_ac1)
SetCmd(switch1,'radius-server key test')
SetCmd(switch1,'radius-server authentication host ' + Radius_server)
SetCmd(switch1,'radius-server accounting host ' + Radius_server)
SetCmd(switch1,'radius nas-ipv4 ' + StaticIpv4_ac1)
SetCmd(switch1,'aaa group server radius wlan')
SetCmd(switch1,'server ' + Radius_server)
EnterConfigMode(switch1)
SetCmd(switch1,'aaa enable')
SetCmd(switch1,'aaa-accounting enable')
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'enable')
SetCmd(switch1,'authentication-type external')
SetCmd(switch1,'external portal-server server-name eportal ipv4 ' + Radius_server)
SetCmd(switch1,'free-resource 1 destination ipv4 ' + Radius_server +'/32 source any')
SetCmd(switch1,'configuration 1 ')
SetCmd(switch1,'enable')
SetCmd(switch1,'radius accounting ')
SetCmd(switch1,'protocol http')
SetCmd(switch1,'radius-acct-server wlan')
SetCmd(switch1,'radius-auth-server wlan')
SetCmd(switch1,'redirect attribute ssid enable ')
SetCmd(switch1,'redirect attribute nas-ip enable')
SetCmd(switch1,'redirect attribute url-after-login enable   ')
SetCmd(switch1,'redirect attribute apmac enable')
SetCmd(switch1,'redirect attribute usermac enable')
SetCmd(switch1,'ac-name 0100.0010.0'+EnvNo+'0.01')
SetCmd(switch1,'redirect url-head http://192.168.10.101/a79.htm')
SetCmd(switch1,'portal-server ipv4 eportal')
SetCmd(switch1,'free-resource 1')
SetCmd(switch1,'interface ws-network 1')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 1')
SetCmd(switch1,'quick-ip-report')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 2')
SetCmd(switch1,'quick-ip-report')

WirelessApplyProfileWithCheck(switch1,['1','2'],[ap1mac,ap2mac])
# check
data = SetCmd(switch1,'show wireless ap status')
res1 = CheckLine(data,ap1mac,Ap1_ipv4,'1','Managed','Success',IC=True)
res2 = CheckLine(data,ap2mac,Ap2_ipv4,'2','Managed','Success',IC=True)
#result
printCheckStep(testname, 'Step 1',res1,res2)

################################################################################
#Step 2
#操作
#客户端STA1连接到网络Network_name1
#
#预期
#关联成功。
# 通过命令show wireless  client  summary可以查看客户端STA1获取到
# 192.168.X.X（Dhcp_pool1）网段的地址
################################################################################
printStep(testname,'Step 2',
          'STA1 connect to test1')

sta1_ipv4 = ''
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
IdleAfter(10)
#获取STA1的地址
# data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
# SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
EnterEnableMode(switch1)
data1=SetCmd(switch1,'show wireless client summary')
SearchResult1 = re.search(sta1mac+'\s+(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
#check
if None != SearchResult1:
    sta1_ipv4 = SearchResult1.group(1)
    if None != re.search(Dhcp_pool1,sta1_ipv4):
        printRes('STA1 ip address: ' + sta1_ipv4)
        res2 = 0  
else:
    res2 = 1
    printRes('Failed: Get ipv4 address of STA1 failed') 

#result
printCheckStep(testname, 'Step 2',res1,res2)
################################################################################
#Step 3
#操作
#检查AC1是否放行STA1的流量
#
#预期
#STA1无法ping通PC1
################################################################################
printStep(testname,'Step 3',
          'sta1 ping pc1 failed')
res1=1
#operate&check
res1 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
res1=0 if res1 !=0 else -1
#result
printCheckStep(testname, 'Step 3',res1)
# 不同型号AP打印内容不同，不对Ap上的debug打印进行检查
# ###############################################################################
# # Step 4
# # 操作
# # 在ap上查看客户端的portal状态
# # cp_debug sta
# # dmesg -c

# # 预期
# # Ap的串口打印中CP Client Table下显示出客户端STA1的
# # mac地址为：STA1MAC
# # ip地址为：STA1IP
# # state :UNAUTHED
# ###############################################################################
# printStep(testname,'Step 4',\
                    # 'ap1:cp_debug sta;dmesg -c',\
                    # 'check STA1MAC、STA1IP、UNAUTHED in CP Client Table on AP1')
# res1=1
# #operate&check
# # AP上CP Client Table表项需要有客户端流量触发，使用客户端ping portal服务器的操作来触发
# SetCmd(sta1,'\n')
# SetCmd(sta1,'ping '+Radius_server+' -c 5')

# checklist1 = []
# checklist1.append((sta1mac))
# checklist1.append((sta1_ipv4))
# checklist1.append(('UNAUTHED'))
# i=0
# while i<5:
	# IdleAfter(5)
	# SetCmd(ap1,'\n')
	# # SetCmd(ap1,'cp_debug sta')
	# data=SetCmd(ap1,'cp_debug sta;dmesg -c')
	# res1 = CheckLineList(data,checklist1)
	# if res1==0:
		# break
	# i=i+1
# #result
# printCheckStep(testname, 'Step 4',res1)
################################################################################
#Step 5
#操作
#客户端STA1访问1.1.1.1 root
#
#预期
#STA1被重定向到Portal认证页面,并且提示输入用户名和密码
################################################################################
printStep(testname,'Step 5',
          'sta1 open 1.1.1.1 and can redirect to portal auth page')
res3=1
#operate&check
web = web_init(sta1_host)
if None != web:
	res1 = web_open(web,'http://1.1.1.1/')
	print 'res1=',res1
	if res1['status']:
		print 'OKOKOK'
		res2 = is_portal_page(web)
		if res2['status']:
			res3 = 0
		else:
			res3 = 1
			printRes('is_portal_page(web) status false')
	else:
		res3 = 1
		print 'NONONO'
		printRes('web_open(web,\'http://1.1.1.1\')')
else:
	res3 =1
	printRes('web_init(sta1) status false')
#result
printCheckStep(testname, 'Step 5',res3)
################################################################################
#Step 6
#操作
#输入正确的用户名和密码进行认证
#预期
#提示用户认证成功，通过show captive-portal  client  status命令查看CP client列表，
# 显示出STA1的信息（“MAC Address”显示“STA1MAC”）
# STA1可以ping通PC1
################################################################################
printStep(testname,'Step 6',
          'enter the right username and password',
          'auth successfully',
          'sta1 ping pc1 successfully')

#operate
res1=res2=res3=res4=1
res1 = portal_login(web,'aaa','111')
if res1['status']:
    res2 = 0
else:
    printRes(res1)

EnterEnableMode(switch1)
data1=SetCmd(switch1,'show captive-portal client status')
res3=CheckLine(data1,sta1mac)
res4 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
#result
printCheckStep(testname, 'Step 6',res2,res3,res4)

# 不同型号AP打印内容不同，不对Ap上的debug打印进行检查
# ################################################################################
# #Step 7
# #操作
# #在ap上查看客户端的portal状态
# # cp_debug sta
# # dmesg -c
# #
# #预期
# #Ap的串口打印中CP Client Table下显示出客户端STA1的信息
# # mac地址为：STA1MAC
# # ip地址为：STA1IP
# # state :AUTHED

# ################################################################################
# printStep(testname,'Step 7',\
                    # 'ap1:cp_debug sta;dmesg -c',\
                    # 'check STA1MAC、STA1IP、AUTHED in CP Client Table on AP1')
# res1=1
# #operate&check
# checklist1 = []
# checklist1.append((sta1mac))
# checklist1.append((sta1_ipv4))
# checklist1.append(('AUTHED'))
# for i in range(5):
    # SetCmd(ap1,'\n')
    # # SetCmd(ap1,'cp_debug sta')
    # data=SetCmd(ap1,'cp_debug sta;dmesg -c')
    # res1 = CheckLineList(data,checklist1)
    # if res1 == 0:
        # break
# checklist2 = []
# checklist2.append((sta1mac))
# checklist2.append((sta1_ipv4))
# checklist2.append(('UNAUTHED'))
# res2 = CheckLineList(data,checklist2)
# res2=0 if res2 !=0 else 1
# #result
# printCheckStep(testname, 'Step 7',res1,res2)

################################################################################
#Step 8
#操作
#手工更改客户端STA1IP为静态地址为STA1IP1(该地址为静态地址,必须跟
# Dhcp_pool1 = '192.168.'+EnvNo+'1.'中地址为一个网段)
#
#预期
#通过show captive-portal  client  status命令查看CP client列表，
# 显示出STA1的IP变为手工更改后的IP地址STA1IP1。
# STA1可以ping通PC1
################################################################################
printStep(testname,'Step 8',
          'Config static Sta1IP instead of dhcp',
          'Show captive-portal client status on AC1 and check whether Sta1IP is right',
          'Sta1 ping pc1 successfully' )
res1=res2=1
#operate&check
SetCmd(sta1,'\n')
SetCmd(sta1,'ifconfig '+Netcard_sta1+' '+Dhcp_pool1+'123 netmask 255.255.255.0')
SetCmd(sta1,'route add -net 0.0.0.0/0 gw '+Dhcp_pool1+'1')
EnterEnableMode(switch1)
res1=CheckSutCmd(switch1,'show captive-portal client status',
                 check=[(sta1mac,Dhcp_pool1+'123')],
                 waittime=5,retry=5,interval=5,IC=True)
# data1=SetCmd(switch1,'show captive-portal client status')
# res1 = CheckLineList(data1,[(sta1mac,Dhcp_pool1+'123')])
res2 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
#result
printCheckStep(testname, 'Step 8',res1,res2)
################################################################################
#Step 9
#操作
#手工设置客户端STA2的IP地址为静态地址STA1IP，客户端STA2连接到网络Network_name1
#
#预期
#关联成功。
# 通过命令show wireless  client  summary可以查看客户端STA2地址为STA1IP。
################################################################################
printStep(testname,'Step 9',
          'STA2 connect to test1',
          'Config static Sta2IP which is the same as dhcp Sta1IP',
          'show wireless client summary on AC1 and check whether Sta2IP is right')
res1=res2=1
#operate&check
res1 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap1mac_lower,dhcpFlag=False)
SetCmd(sta2,'\n')
SetCmd(sta2,'ifconfig '+Netcard_sta1+' '+sta1_ipv4+' netmask 255.255.255.0')
SetCmd(sta2,'route add -net 0.0.0.0/0 gw '+Dhcp_pool1+'1')
IdleAfter(3)
EnterEnableMode(switch1)
i=0
while i<5:
	data1=SetCmd(switch1,'show wireless client summary')
	res2 = CheckLineList(data1,[(sta2mac,sta1_ipv4)])
	if res2 == 0:
		break
	IdleAfter(3)
	i = i+1
#result
printCheckStep(testname, 'Step 9',res1,res2)
################################################################################
#Step 10
#操作
#客户端STA2打开web页面访问1.1.1.1
#
#预期
#STA2上可以看到重定向页面，并且提示输入用户名和密码
################################################################################
printStep(testname,'Step 10',
          'sta2 open 1.1.1.1 and can redirect to portal auth page')
res3=1
#operate&check
web = web_init(sta2_host)
if None != web:
    res1 = web_open(web,'http://1.1.1.1')
    if res1['status']:
        res2 = is_portal_page(web)
        if res2['status']:
            res3 = 0
        else:
            res3 = 1
            printRes('is_portal_page(web) status false')
    else:
        res3 = 1
        printRes('web_open(web,\'http://1.1.1.1\')')
else:
    res3 =1
    printRes('web_init(sta1) status false')
#result
printCheckStep(testname, 'Step 10',res3)
################################################################################
#Step 11
#操作
#重新输入正确的用户名和密码进行认证
# portal认证用户名：portal_username = 'aaa'
# portal认证密码：portal_password = '111' 
# AC1上查看CP列表
# 检查AC1是否放行STA2的流量
#
#预期
#提示用户认证成功，通过show captive-portal  client  status命令查看CP client列表，
# 显示出STA2的信息（“MAC Address”显示“STA2MAC”）
# STA2可以ping通PC1

################################################################################
printStep(testname,'Step 11',
          'enter the right username and password',
          'auth successfully',
          'sta2 ping pc1 successfully')

#operate
res1=res2=res3=res4=1
res1 = portal_login(web,'aaa','111')
if res1['status']:
    res2 = 0
else:
    printRes(res1)

EnterEnableMode(switch1)
data1=SetCmd(switch1,'show captive-portal client status')
res3=CheckLine(data1,sta2mac)
res4 = CheckPing(sta2,pc1_ipv4,mode='linux',pingPara=' -c 10')
#result
printCheckStep(testname, 'Step 11',res2,res3,res4)
################################################################################
#Step 12
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 12',
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'disable')
SetCmd(switch1,'no configuration 1')
SetCmd(switch1,'no external portal-server ipv4 server-name eportal')
SetCmd(switch1,'no free-resource 1')
EnterConfigMode(switch1)
SetCmd(switch1,'no radius source-ipv4')
SetCmd(switch1,'no radius-server key')
SetCmd(switch1,'no aaa group server radius wlan')
SetCmd(switch1,'no radius nas-ipv4')
SetCmd(switch1,'no aaa enable')
SetCmd(switch1,'no aaa-accounting enable')
SetCmd(switch1,'no radius-server authentication host ' + Radius_server)
SetCmd(switch1,'no radius-server accounting host ' + Radius_server)


res1 = web_close(web)
printRes(res1)
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'disable')

EnterWirelessMode(switch1)
SetCmd(switch1,'no network 101')
SetCmd(switch1,'no network 102')
SetCmd(switch1,'ap profile 1')
SetCmd(switch1,'no quick-ip-report')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 2')
SetCmd(switch1,'no quick-ip-report')

WirelessApplyProfileWithCheck(switch1,['1','2'],[ap1mac,ap2mac])
#end
printTimer(testname, 'End')