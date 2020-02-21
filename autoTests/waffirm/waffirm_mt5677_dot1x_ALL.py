#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_mt5677_dot1x.py
#
# Author:  (zhangjxp)
#
# Version 1.0.0
#
# Date:  2017-4-28 9:54:28
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# [MT5677] ip-modify dot1x-acct-report测试(自动化不测试改变STA IP是否会触发计费停止和计费开始报文，只测试命令)
# 测试目的：测试ip-modify dot1x-acct-report命令
# 测试环境：同测试拓扑
# 1.客户端STA1连接802.1x无线网络后成功通过认证,STA1 ping PC1能通。
# 2.更改STA1的IP地址后，STA1 ping PC1能通。
# 3.重启AC后，ip-modify dot1x-acct-report命令不丢失。
# 4.可以删除ip-modify dot1x-acct-report命令。
# 5.恢复默认配置
#
#*******************************************************************************
# Change log:
#     - creadte by zhangjxp 2017.5.2
#*******************************************************************************
#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase mt5677_dot1x'
avoiderror(testname)
printTimer(testname,'Start')

################################################################################
#Step 1
#
#操作
# 1	配置AC1的network1的安全接入方式为WPA-Enterprise，WPA version为WPA，认证服务器使用wlan：
# 在AC1上配置ip-modify dot1x-acct-report命令。
#
#预期
#检查AP1和AP2是否正常上线	配置成功。在AC1上面show wireless network 1可以看到相关的配置。
# AC1上通过命令show wireless  ap status查看AP1和AP2的列表：AP1和AP2成功被AC1管理
#
################################################################################
printStep(testname,'Step 1',
          'set security mode of network 1 wpa-enterprise,',
          'set wpa versions wpa,',
          'set radius server-name acct wlan,',
          'set radius setver-name auth wlan,',
          'and u should config others and so on,',
          'check config success.')
res=res1=res2=res3=res4=res5=res6=res7=res8=1
#operate
#AC1配置
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'radius source-ipv4',StaticIpv4_ac1)
SetCmd(switch1,'radius-server key test')
SetCmd(switch1,'radius-server authentication host',Radius_server)
SetCmd(switch1,'radius-server accounting host',Radius_server)
SetCmd(switch1,'radius nas-ipv4',StaticIpv4_ac1)
SetCmd(switch1,'aaa group server radius wlan')
SetCmd(switch1,'server',Radius_server)
EnterConfigMode(switch1)
SetCmd(switch1,'aaa enable')
SetCmd(switch1,'aaa-accounting enable')
#配置wireless模式下的radius配置参数
EnterWirelessMode(switch1)
SetCmd(switch1,'radius server-name auth wlan')
SetCmd(switch1,'radius server-name acct wlan')
SetCmd(switch1,'radius accounting')
#配置network模式下的radius配置参数
EnterNetworkMode(switch1,1)
SetCmd(switch1,'radius server-name auth wlan')
SetCmd(switch1,'radius server-name acct wlan')
SetCmd(switch1,'radius accounting')
SetCmd(switch1,'security mode wpa-enterprise')
SetCmd(switch1,'wpa versions wpa')
EnterWirelessMode(switch1)
SetCmd(switch1,'ip-modify dot1x-acct-report')
# check
EnterEnableMode(switch1)
data3 = SetCmd(switch1,'show wireless ap status')
print 'data=',data3
res7 = CheckLine(data3,ap1mac,Ap1_ipv4,'1','Managed','Success',IC=True)
res8 = CheckLine(data3,ap2mac,Ap2_ipv4,'2','Managed','Success',IC=True)
data1 = ShowRun(switch1)
res1 = CheckLineList(data1,['radius source-ipv4 ' + StaticIpv4_ac1,'radius-server key 0 test','radius-server authentication host ' + Radius_server,
                            'radius-server accounting host ' + Radius_server,'aaa-accounting enable','aaa enable','radius nas-ipv4 ' + StaticIpv4_ac1,
                            'aaa group server radius wlan','server ' + Radius_server])
res=CheckLine(data1,'ip-modify dot1x-acct-report')
data2 = SetCmd(switch1,'show wireless network 1',timeout=10)
res2 = CheckLine(data2,'Security Mode','WPA Enterprise')
res3 = CheckLine(data2,'RADIUS Authentication Server Name','wlan')
res4 = CheckLine(data2,'RADIUS Accounting Server Name','wlan')
res5 = CheckLine(data2,'WPA Versions','WPA2')
res6 = CheckLine(data2,'WPA Versions','WPA')
res5 = 0 if res5!=0 else -1


#result
printCheckStep(testname, 'Step 1',res,res1,res2,res3,res4,res5,res6,res7,res8)

################################################################################
#Step 2
#操作
# 设置STA1无线网卡的属性为WPA-Enterprise认证，关联网络test1，使用在Radius服务器配置的用户名和密码。	
#
#预期
# 成功关联，并获取192.168.91.X网段的IP地址。Show wireless client summery可以看到
# STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
################################################################################
printStep(testname,'Step 2',
          'STA1 connect to test1')
res1=1
res2=1
#operate
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='wpa_eap',identity=Dot1x_identity,password=Dot1x_password,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
#result

printCheckStep(testname, 'Step 2',res1,res2)


################################################################################
#Step 3
#操作
# 在STA1上面ping PC1。	
#
# #预期
# 能够ping通。
################################################################################
printStep(testname,'Step 3',
          'sta1 ping pc1 successfully')

res1=1
#operate
res1 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')

printCheckStep(testname, 'Step 3',res1)
################################################################################
#Step 4
#更改STA1的IP地址为静态IP1，在STA1上面ping PC1。	能够ping通。
################################################################################
printStep(testname,'Step 4',
          'Config static Sta1IP instead of dhcp',
          'Sta1 ping pc1 successfully' )
res1=1
#operate
Receiver(sta1,'\n')
Receiver(sta1,'ifconfig '+Netcard_sta1+' '+Dhcp_pool1+'111 netmask 255.255.255.0')
Receiver(sta1,'route add default gw '+If_vlan4091_s1_ipv4+' dev '+Netcard_sta1)
IdleAfter(2)
res1 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
#result
printCheckStep(testname, 'Step 4',res1)
################################################################################
#Step 5
# 操作
# 保存AC1配置后重启AC1，重启后show run查看AC1配置。
# 预期
# ip-modify dot1x-acct-report命令存在。
################################################################################
printStep(testname,'Step 5',
          'Write and reload AC1',
          'ip-modify dot1x-acct-report configuration is not lost')

res1=1
#operate
EnterEnableMode(switch1)
Receiver(switch1,'write',timeout=1)
IdleAfter(1)
Receiver(switch1,'y')
IdleAfter(5)
ReloadMultiSwitch([switch1])
EnterEnableMode(switch1, noMore=True)
# check
EnterWirelessMode(switch1)
data1 = SetCmd(switch1,'show run c')
res1 = CheckLine(data1,'ip-modify dot1x-acct-report')
#result
printCheckStep(testname, 'Step 5',res1)
################################################################################
#Step 6
# 操作
# 在AC1上可以删除ip-modify dot1x-acct-report命令
# 预期
# no ip-modify dot1x-acct-report	可以删除成功，show run查看不到
# ip-modify dot1x-acct-report命令。
################################################################################
printStep(testname,'Step 6',
          'no ip-modify dot1x-acct-report',
          'check configuration')

res1=1
#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no ip-modify dot1x-acct-report')

# check
data1 = SetCmd(switch1,'show run c')
res1 = CheckLine(data1,'ip-modify dot1x-acct-report')
res1=0 if res1 != 0 else 1
#result
printCheckStep(testname, 'Step 6',res1)
################################################################################
#Step 6
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 6',
          'Recover initial config')

#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'no radius server-name auth')
SetCmd(switch1,'no radius server-name acct')
SetCmd(switch1,'no radius accounting')
SetCmd(switch1,'security mode none')
SetCmd(switch1,'no wpa versions')
#配置wireless模式下的radius配置参数
EnterWirelessMode(switch1)
SetCmd(switch1,'no radius server-name auth')
SetCmd(switch1,'no radius server-name acct')
SetCmd(switch1,'no radius accounting')

EnterConfigMode(switch1)
SetCmd(switch1,'no radius source-ipv4')
SetCmd(switch1,'no radius-server key')
SetCmd(switch1,'no aaa group server radius wlan')
SetCmd(switch1,'no radius nas-ipv4')
SetCmd(switch1,'no aaa enable')
SetCmd(switch1,'no aaa-accounting enable')
SetCmd(switch1,'no radius-server authentication host',Radius_server)
SetCmd(switch1,'no radius-server accounting host',Radius_server)

WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#end
printTimer(testname, 'End')