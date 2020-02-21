#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.3.11.py - test case 4.3.11 of waffirm
#
# Author:  fuzf@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.3.11 基于AP位置的客户端连接
# 测试目的：验证“基于AP位置的客户端连接”功能是否生效，该功能主要是在AC上实现，同时需要城市热点配合。
# 测试环境：同测试拓扑
# 测试描述：1、无线终端使用符合条件的用户名进行认证可以成功。
#          2、无线终端使用不符合条件的用户名认证失败。
#          （STA1的MAC地址：STA1MAC）
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.3.11'
avoiderror(testname)
printTimer(testname,'Start',"Client connection based on AP location ")

################################################################################
#Step 1
#操作
#配置AC1的network1的安全接入方式为WPA-Enterprise，WPA version为默认的混合模式，认证服务器使用wlan：
#wireless
#security mode wpa-enterprise
#wpa versions
#radius server-name acct wlan
#radius server-name auth wlan
#exit
#将配置下发到AP1。
#wireless ap profile apply 1
#设置STA1无线网卡的属性为WPA2-Enterprise认证，关联网络test1，使用Radius服务器上面配置好的用户名和密码。
#配置成功。在AC1上面show wireless network 1可以看到相关的配置。
################################################################################
printStep(testname,'Step 1',
          'set security mde of network 1 wpa-enterprise,',
          'set wpa versions wpa,',
          'set radius server-name acct wlan,',
          'set radius setver-name auth wlan,',
          'and u should config others and so on,',
          'check config success.')
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
SetCmd(switch1,'security mode wpa-enterprise ')
SetCmd(switch1,'wpa versions')


#check
data1 = ShowRun(switch1)
#printRes("data1="+ data1)
res1 = CheckLineList(data1,["radius source-ipv4 " + StaticIpv4_ac1,"radius-server key 0 test","radius-server authentication host " + Radius_server,
                            "radius-server accounting host " + Radius_server,"aaa-accounting enable","aaa enable","radius nas-ipv4 " + StaticIpv4_ac1,
                            "aaa group server radius wlan","server " + Radius_server])
data2 = SetCmd(switch1,'show wireless network 1',timeout=3)
res2 = CheckLine(data2,"Security Mode","WPA Enterprise")
res3 = CheckLine(data2,"RADIUS Authentication Server Name","wlan")
res4 = CheckLine(data2,"RADIUS Accounting Server Name","wlan")
res5 = CheckLine(data2,"WPA Versions","WPA/WPA2")

#result
printCheckStep(testname, 'Step 1',res1,res2,res3,res4,res5)

################################################################################
#Step 2
#operate
#在AC1上配置“基于AP位置的用户接入”：
#无线配置模式：
#ap-group g1
#permit-ap-name AP1_MAC
#exit
#user-profile AP1
#permit-ap-group g1
#exit
#ap-group g2
#permit-ap-name AP2_MAC
#exit
#user-profile AP2
#permit-ap-group g2
#exit
#user-profile enable
#预期
#配置成功，在AC 1上show run可以看到以上配置.
################################################################################

printStep(testname,'Step 2',
          'add user-profile configuration,',
          'and enable user-profile function,')

#add user-profile configuration
EnterWirelessMode(switch1)
SetCmd(switch1,'ap-group g1')
SetCmd(switch1,'permit-ap-name '+ap1mac)

EnterWirelessMode(switch1)
SetCmd(switch1,'user-profile AP1')
SetCmd(switch1,'permit-ap-group g1')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap-group g2')
SetCmd(switch1,'permit-ap-name '+ap2mac)

EnterWirelessMode(switch1)
SetCmd(switch1,'user-profile AP2')
SetCmd(switch1,'permit-ap-group g2')

#enable user-profile
EnterWirelessMode(switch1)
SetCmd(switch1,'user-profile enable')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

#check user-profile configure result

user_profile_configuration = []
user_profile_configuration.append('ap-group g1')
user_profile_configuration.append('permit-ap-name '+ap1mac)                                 
user_profile_configuration.append('user-profile AP1')
user_profile_configuration.append('permit-ap-group g1')

user_profile_configuration.append('ap-group g2')
user_profile_configuration.append('permit-ap-name '+ap2mac)
user_profile_configuration.append('user-profile AP2')
user_profile_configuration.append('permit-ap-group g2')

user_profile_configuration.append('user-profile enable')

EnterWirelessMode(switch1)
data1=SetCmd(switch1,'show running-config current-mode')

res1 = CheckLineList(data1,user_profile_configuration,IC=True)

if res1 != 0:
    printRes('Failed:user-profile configure failed')

#result
printCheckStep(testname,'step 2',res1)

################################################################################
#Step 3
#操作
#Sta1使用用户名user1关联到AP1的network 1并通过DHCP获取IP
#
#预期
#Sta1关联成功，在AC1上show wireless client status可以看到sta1已经成功关联到AP1的vap0;
#Sta1获取到IP地址
################################################################################

printStep(testname,'Step 3',
          'STA1 connect to ap1 network1 using username user1',
          'and get ip success.')

res1=res2=res3=1

#sta1关联到ap1 network 1 using username 'user1'
res1=WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='wpa2_eap',identity='user1',password='user1',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)

#检查STA1是否在线
res2=CheckWirelessClientOnline(switch1,sta1mac,'online')

#获取STA1的IP地址
sta1_ipv4 = GetStaIpAddress(sta1,Netcard_sta1)
if sta1_ipv4 !='':
    if re.search(Dhcp_pool1,sta1_ipv4) != None:
        res3 = 0

#result
printCheckStep(testname,'step 3',res1,res2,res3)

################################################################################
#Step 4
#操作
#在STA1上面ping PC1，
#预期
#可以ping通
################################################################################

printStep(testname,'Step 4',
          'STA1 ping PC1,',
          'check if succeed.')

res1=1

#sta1 ping pc1
res1 = CheckPing(sta1,pc1_ipv4,mode='linux')
if res1 != 0:
    printRes('Failed:sta1 ping pc1 failed!')
#result
printCheckStep(testname,'step 4',res1)


################################################################################
#Step 5
#操作
#Sta2使用用户名user2关联到AP1的network 1
#
#预期
#Sta2关联失败
################################################################################

printStep(testname,'Step 5',
          'STA2 connect to ap1 network1 using username user2')

res1=1

#sta2关联到ap1 network 1 using username 'user2'，预期连接失败
res1=WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,connectType='wpa2_eap',dhcpFlag=False,identity='user2',password='user2',bssid=ap1mac_lower)
res1 = 0 if res1 != 0 else 1

#检查STA2是否在线
#res2=CheckWirelessClientOnline(switch1,sta2mac,'online')
#res2 = 0 if res2 !=0 else 1

if res1==1:
    printRes('failed:sta2 should not connected with ap1 network1 using username use2')
    
#result
printCheckStep(testname,'step 5',res1)


################################################################################
#Step 6
#操作
#Sta2使用用户名user3关联到AP1的network 1并成功获取IP
#
#预期
#Sta2关联成功，获取IP成功
################################################################################

printStep(testname,'Step 6',
          'STA2 connect to ap1 network1 using username user3')

res1=res2=1

#sta2关联到ap1 network 1 using username 'user3'
res1=WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,connectType='wpa2_eap',identity='user3',password='user3',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)


#检查STA2是否在线
res2=CheckWirelessClientOnline(switch1,sta2mac,'online')

if res2==1:
    printRes("Failed:sta2 not connected on ap1 network 1")

#result
printCheckStep(testname,'step 6',res1,res2)

################################################################################
#Step 7
#操作
#客户端STA2 ping PC1。
#
#预期
#STA2可以ping通PC1。
################################################################################

printStep(testname,'Step 7',
          'STA2 ping PC1,',
          'check if succeed.')

res1=res2=1

#sta2 ping pc1
res1 = CheckPing(sta2,pc1_ipv4,mode='linux')

if res1!=0:
    printRes("Failed:sta2 ping pc1 failed")

#result
printCheckStep(testname,'step 7',res1)



################################################################################
#Step 8
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 8',
          'Recover initial config for switches.')

#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'no radius server-name auth')
SetCmd(switch1,'no radius server-name acct')
SetCmd(switch1,'no radius accounting')
SetCmd(switch1,'security mode none')
SetCmd(switch1,'wpa versions')
#配置wireless模式下的radius配置参数
EnterWirelessMode(switch1)
SetCmd(switch1,'no radius server-name auth')
SetCmd(switch1,'no radius server-name acct')
SetCmd(switch1,'no radius accounting')

#清除network模式下的radius配置
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no radius server-name auth')
SetCmd(switch1,'no radius server-name acct')
SetCmd(switch1,'no radius accounting')
SetCmd(switch1,'security mode none')

EnterConfigMode(switch1)
SetCmd(switch1,'no radius source-ipv4')
SetCmd(switch1,'no radius-server key')
SetCmd(switch1,'no aaa group server radius wlan')
SetCmd(switch1,'no radius nas-ipv4')
SetCmd(switch1,'no aaa enable ')
SetCmd(switch1,'no aaa-accounting enable')
SetCmd(switch1,'no radius-server authentication host',Radius_server)
SetCmd(switch1,'no radius-server accounting host',Radius_server)

EnterWirelessMode(switch1)
SetCmd(switch1,'no user-profile enable')
SetCmd(switch1,'no user-profile AP1')
SetCmd(switch1,'no user-profile AP2')
SetCmd(switch1,'no ap-group g1')
SetCmd(switch1,'no ap-group g2')

WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#end
printTimer(testname, 'End')





