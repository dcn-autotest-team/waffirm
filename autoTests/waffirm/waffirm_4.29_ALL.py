#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.29.py - test case 4.29 of waffirm_new
#
# Author:  (fuzf@dc.com)
#
# Version 1.0.0
#
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 4.29  AP逃生用户不下线功能
# 测试目的：测试AC AP断开连接重连后用户不下线
# 测试环境：同测试拓扑
# 测试描述：AC上开启AP逃生和AP逃生用户不下线功能，当AP掉线后，已关联用户不掉线，新终端可以继续接入；
#          当AP重新被AC管理后，跳过配置自动下发过程，已关联用户不掉线
#（AP1的MAC地址：AP1MAC ；AP1的ip地址是20.1.1.3）
#
#*******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
#*******************************************************************************

###########

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.29'
avoiderror(testname)
printTimer(testname,'Start','test ap-escape client-persist')
# 2.4G、5G差异化配置,test24gflag为True代表执行2.4G脚本，False代表执行5G脚本
if test24gflag:
    ath0 = 'ath0'
    ath1 = 'ath1'
else:
    ath0 = 'ath16'
    ath1 = 'ath17'
################################################################################
#Step 1
#
#操作
# AP逃生初始配置，L3和AC1通过trunk相连，STA网关在L3上，dhcp server在L3上，配置如下：
# AC1上配置：
#config
#vlan 4081
#interface vlan 4081
#ip address 192.168.81.1 255.255.255.0
#interface ethernet s1p2
#switchport mode trunk
#exit
#wireless 
#l2tunnel vlan-list add 4081
#network 1
#vlan 4081
#network2
#vlan 4081
#L3上配置：
#config
#vlan 4081
#interface vlan 4081
#ip address 192.168.81.254 255.255.255.0
#interface ethernet s3p2
#switchport mode trunk
#interface ethernet s3p1
#shutdown
#exit
#service dhcp
#ip dhcp excluded-address 192.168.81.1
#ip dhcp excluded-address 192.168.81.254
#ip dhcp pool vlan4081
#network-address 192.168.81.0 24
#default-router 192.168.81.254
#
#预期
# AC1 L3上show run检查配置结果，由于基本是基础配置，只检查集中转发vlan配置情况
################################################################################
printStep(testname,'Step 1',
          'Reconfig the topu',
          'show run Check the result')

res1=1
#operate
#配置AC1
EnterConfigMode(switch1)
SetCmd(switch1,'vlan 4081')
SetCmd(switch1,'interface vlan 4081')
SetCmd(switch1,'ip address 192.168.81.1 255.255.255.0')
#SetCmd(switch1,'interface',s1p2)
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport mode trunk')

EnterWirelessMode(switch1)
SetCmd(switch1,'network 1')
SetCmd(switch1,'vlan 4081')
SetCmd(switch1,'network 2')
SetCmd(switch1,'vlan 4081')

# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    EnterWirelessMode(switch1)
    SetCmd(switch1,'l2tunnel vlan-list add 4081')
else:
    pass
#配置L3
EnterConfigMode(switch3)
SetCmd(switch3,'vlan 4081')
SetCmd(switch3,'interface vlan 4081')
SetCmd(switch3,'ip address 192.168.81.254 255.255.255.0')
SetCmd(switch3,'interface',s3p1)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'interface',s3p2)
SetCmd(switch3,'shutdown')
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan20)
SetCmd(switch3,'interface',s3p4)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan30)

EnterConfigMode(switch3)
SetCmd(switch3,'service dhcp')
SetCmd(switch3,'ip dhcp excluded-address 192.168.81.1')
SetCmd(switch3,'ip dhcp excluded-address 192.168.81.254')
SetCmd(switch3,'ip dhcp pool vlan4081')
SetCmd(switch3,'network-address 192.168.81.0 24')
SetCmd(switch3,'default-router 192.168.81.254')


#check
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    EnterEnableMode(switch1)
    data1 = SetCmd(switch1,'show wireless l2tunnel vlan-list',timeout=5)
    res1 = CheckLine(data1,'4081')
else:
    res1 = 0
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#操作
# 配置Ac1 profile1:
# ap escape
# ap escape client-persist
# 配置AC1 profile2:
# ap escape
#
#预期
# show wireless ap profile 1显示的内容中包括：
#   AP Escape...................................... Enable
#   AP Escape Client Persist Mode.................. Enable
# show wireless ap profile 2显示的内容中包括：
#   AP Escape...................................... Enable
#   AP Escape Client Persist Mode.................. Disable
################################################################################
printStep(testname,'Step 2',
          'ap profile 1',
          'ap escape',
          'ap escape client-persist',
          'ap profile 2',
          'ap escape')

res1=res2=res3=res4=1
#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile','1')
SetCmd(switch1,'ap escape')
SetCmd(switch1,'ap escape client-persist')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile','2')
SetCmd(switch1,'ap escape')

#check
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless ap profile','1',timeout=10)
data2 = SetCmd(switch1,'show wireless ap profile','2',timeout=10)

res1 = CheckLine(data1,'AP Escape\.','Enable',IC=True)
res2 = CheckLine(data1,'AP Escape Client Persist Mode','Enable',IC=True)
res3 = CheckLine(data2,'AP Escape\.','Enable',IC=True)
res4 = CheckLine(data2,'AP Escape Client Persist Mode','Disable',IC=True)

#result
printCheckStep(testname, 'Step 2', res1,res2,res3,res4)

################################################################################
#Step 3
#
#操作
# AC1下发profile1和profile2,
#
#预期
# 配置下发成功，AP没有掉线
################################################################################
printStep(testname,'Step 3',
          'wireless ap profile apply 1',
          'wireless ap profile apply 2')

res=1
#operate

res = WirelessApplyProfileWithCheck(switch1,['1','2'],[ap1mac,ap2mac])
#check
#IdleAfter(Var_ap_connect_after_reboot)

# EnterEnableMode(switch1)
# for i in xrange(0,3):
    # data1 = SetCmd(switch1,'show wireless ap status')
    # res1 = CheckLine(data1,ap1mac,Ap1_ipv4,'1','Managed','Success',IC=True)
    # res2 = CheckLine(data1,ap2mac,Ap2_ipv4,'2','Managed','Success',IC=True)
    # if 0==res1 or 0==res2:
        # break    

#result
printCheckStep(testname, 'Step 3',res)

################################################################################
#Step 4
#操作
# sta1连接ap1的test1
# sta2连接ap2的test2
#
#预期
# 关联成功，并获取192.168.81.x网段地址
################################################################################
printStep(testname,'Step 4',
          'Let sta1 connect to ap1 test1',
          'Let sta2 connect to ap2 test2',
          'both connect succeed')

res1=res2=1
#operate
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower,checkDhcpAddress='192.168.81.') 
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,bssid=ap2mac_type1_network2,checkDhcpAddress='192.168.81.')

if res1 != 0:
    printRes('Fail:sta1 connect test1 failed!')
if res2 != 0:
    printRes('Fail:sta2 connect test2 failed!')


#check


#result
printCheckStep(testname, 'Step 4',res1,res2)

################################################################################
#Step 5
#操作
# Sta1 sta2 ping pc1（集中转发)
# Sta1 sta2 ping网关（本地转发）
# 
#预期
# 可以ping通
################################################################################
printStep(testname,'Step 5',
          'sta1 ping pc1 pass',
          'sta2 ping pc1 pass')

res1=res2=1

#operate
# PC1添加路由
gw='192.168.10.'+EnvNo+'1'
SetCmd(pc1,'route add -net 192.168.81.0/24 gw '+gw)

# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
# 集中转发ping pc1,本地转发ping网关
if testcentral:
    destination_ipv4 = pc1_ipv4
else:
    destination_ipv4 = '192.168.81.254'

res1 = CheckPing(sta1,destination_ipv4,mode='linux')
res2 = CheckPing(sta2,destination_ipv4,mode='linux')
#check
if res1 != 0:
    printRes('Fail:sta1 ping '+destination_ipv4+' failed!')
if res2 != 0:
    printRes('Fail:sta2 ping '+destination_ipv4+' failed!')
#result
printCheckStep(testname, 'Step 5', res1,res2)

################################################################################
#Step 6
#操作
# AC1上配置：
# network 1
# ssid test1_new
# network2
# ssid test2_new
#预期
# 配置成功
################################################################################
printStep(testname,'Step 6',
          'set network1 ssid test1_new',
          'set network2 ssid test2_new')

#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'network 1')
SetCmd(switch1,'ssid test1_new')
SetCmd(switch1,'network 2')
SetCmd(switch1,'ssid test2_new')

#check
data1 = SetCmd(switch1,'show wireless network 1',timeout=15)
data2 = SetCmd(switch1,'show wireless network 2',timeout=15)
res1 = CheckLine(data1,'SSID','test1_new',IC=True)
res2 = CheckLine(data2,'SSID','test2_new',IC=True)

#result
printCheckStep(testname, 'Step 6', res1,res2)

################################################################################
#Step 7
#操作
# shutdown s3p2
# wait 1min
#预期
# sta1 sta2都没有掉线，可以ping通pc1
# ap1 ap2掉线，AC1上没有客户端表项
################################################################################
printStep(testname,'Step 7',
          'shutdown s3p2',
          'wait 120s',
          'sta1 ping pc1',
          'sta2 ping pc1',
          'show wireless ap status',
          'show wireless client status')

res1=res2=res3=res4=1
#operate
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'shutdown ')
IdleAfter(120)

res1 = CheckPing(sta1,destination_ipv4,mode='linux')
res2 = CheckPing(sta2,destination_ipv4,mode='linux')
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless ap status')
data2 = SetCmd(switch1,'show wireless client status')
res3 = CheckLine(data1,'Managed','Success',IC=True)
res4 = CheckLine(data2,'Auth',IC=True)
res3 = 0 if res3 != 0 else 1
res4 = 0 if res4 != 0 else 1

#end
printCheckStep(testname, 'Step 7', res1,res2,res3,res4)

################################################################################
#Step 8
#操作
# no shutdown s3p2
# wait 2min
#预期
# 1) AP1、AP2重新被AC1管理，AC1上show wireless ap status显示AP1、AP2均为Managed Success ；
# 2) STA1不会掉线、仍然与AP1关联，能够ping通PC1，
#    AC1上show wireless client summary看到STA1（“MAC Address”显示“STA1MAC”、VAP MAC显示为AP1的MAC），IP地址的网段正确；STA2掉线，不能ping通PC1；
# 3)AP1上iwconfig ath0显示ESSID:"test1"，iwconfig ath1显示ESSID:"test2"；
#    AP2上iwconfig ath0显示ESSID:"test1_new"，iwconfig ath1显示ESSID:"test2_new"；（AP上只查看不判断）
################################################################################
printStep(testname,'Step 8',
          'no shutdown s3p1',
          'wait 120s',
          'sta1 ping pc1',
          'sta2 ping pc1',
          'show wireless ap status',
          'show wireless client status')

res1=res2=res3=res4=res5=res6=1
#operate
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'no shutdown')
IdleAfter(120)

#check
data1 = SetCmd(switch1,'show wireless ap status')
res1 = CheckLine(data1,ap1mac,Ap1_ipv4,'1','Managed','Success',IC=True)
res2 = CheckLine(data1,ap2mac,Ap2_ipv4,'2','Managed','Success',IC=True)

res3 = CheckWirelessClientOnline(switch1,sta1mac,'online')
res4 = CheckWirelessClientOnline(switch1,sta2mac,'offline')

res5 = CheckPing(sta1,destination_ipv4,mode='linux')
res6 = CheckPing(sta2,destination_ipv4,mode='linux')
res6 = 0 if res6 != 0 else 1
SetCmd(ap1,'iwconfig '+ath0)
SetCmd(ap1,'iwconfig '+ath1)
SetCmd(ap2,'iwconfig '+ath0)
SetCmd(ap2,'iwconfig '+ath1)


#result
printCheckStep(testname, 'Step 8', res1,res2,res3,res4,res5,res6)

################################################################################
#Step 9
#操作
# STA2连接test2_new，并获取到192.168.81.x网段的地址
# 
#预期
# 关联成功，ping pc1可通
################################################################################
printStep(testname,'Step 9',
          'sta2 connect test2_new',
          'sta2 get 192.168.81.x ip via dhcp',
          'sta2 ping pc1')

res1=res2=1
#operate
res1 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,'test2_new',bssid=ap2mac_type1_network2,checkDhcpAddress='192.168.81.')

#check
if res1 == 0:
    res2 = CheckPing(sta2,destination_ipv4,mode='linux')
    if res2 != 0:
        printRes('Fail:sta2 ping '+destination_ipv4+' failed!')
if res1 != 0:
    printRes('Fail:sta2 connect ssid test2_new failed!')

#result
printCheckStep(testname, 'Step 9', res1,res2)

################################################################################
#Step 10
#操作
# AC1下发配置profile 1
# 
#预期
# 1) 配置下发成功，STA1掉线，不能ping通PC1，STA2不会掉线、能ping通PC1 ；
# 2) AP1上iwconfig ath0显示ESSID:"test1_new"，iwconfig ath1显示ESSID:"test2_new"；
#   （AP只查看不判断）

################################################################################
printStep(testname,'Step 10',
          'wireless ap profile apply 1')

res1=res2=res3=res4=1
#operate
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')
# for i in xrange(10):
    # IdleAfter(10)
    # data1 = SetCmd(switch1,'show wireless ap status')
    # if re.search('1\s+Managed Success',data1) is not None:
        # break
res1 = CheckWirelessClientOnline(switch1,sta1mac,'offline')
res2 = CheckWirelessClientOnline(switch1,sta2mac,'online')
res3 = CheckPing(sta1,destination_ipv4,mode='linux')
res4 = CheckPing(sta2,destination_ipv4,mode='linux')
res3=0 if res3 != 0 else 1
SetCmd(ap1,'iwconfig '+ath0)
SetCmd(ap1,'iwconfig '+ath1)
SetCmd(ap2,'iwconfig '+ath0)
SetCmd(ap2,'iwconfig '+ath1)
#check

if res1 != 0:
    printRes('Fail:sta1 is still online!')

#result
printCheckStep(testname, 'Step 10', res1,res2,res3,res4)

################################################################################
#Step 11
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 11',
          'Recover initial config')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)
# S3恢复
EnterConfigMode(switch3)
SetCmd(switch3,'no int vlan 4081')
SetCmd(switch3,'no vlan 4081')
EnterInterfaceMode(switch3,s3p2)
SetCmd(switch3,'no shutdown')

EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport mode access')
SetCmd(switch3,'switchport access vlan 40')

EnterConfigMode(switch3)
SetCmd(switch3,'no ip dhcp excluded-address 192.168.81.1')
SetCmd(switch3,'no ip dhcp excluded-address 192.168.81.254')
SetCmd(switch3,'no ip dhcp pool vlan4081')

# AC1恢复
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    EnterWirelessMode(switch1)
    SetCmd(switch1,'l2tunnel vlan-list remove 4081')
    EnterConfigMode(switch3)
    SetCmd(switch3,'no service dhcp')
    EnterInterfaceMode(switch3,s3p3)
    SetCmd(switch3,'switchport mode access')
    SetCmd(switch3,'switchport access vlan',Vlan20)
    EnterInterfaceMode(switch3,s3p4)
    SetCmd(switch3,'switchport mode access')
    SetCmd(switch3,'switchport access vlan',Vlan30)
else:
    EnterConfigMode(switch3)
    SetCmd(switch3,'service dhcp')
    SetCmd(switch3,'Interface ',s3p3)
    SetCmd(switch3,'switchport mode trunk')
    SetCmd(switch3,'switchport trunk allowed vlan all')
    SetCmd(switch3,'switchport trunk native vlan',Vlan20)
    SetCmd(switch3,'Interface ',s3p4)
    SetCmd(switch3,'switchport mode trunk')
    SetCmd(switch3,'switchport trunk allowed vlan all')
    SetCmd(switch3,'switchport trunk native vlan',Vlan30)

EnterWirelessMode(switch1)
SetCmd(switch1,'network 1')
SetCmd(switch1,'vlan 4091')
SetCmd(switch1,'ssid',Network_name1)
SetCmd(switch1,'network 2')
SetCmd(switch1,'vlan 4092')
SetCmd(switch1,'ssid',Network_name2)

EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan 4081')
SetCmd(switch1,'no vlan 4081')
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport mode access')
SetCmd(switch1,'switchport access vlan 40')


EnterApProMode(switch1,'1')
SetCmd(switch1,'no ap escape client-persist')
SetCmd(switch1,'no ap escape',timeout=1)
IdleAfter(1)
Receiver(switch1,'y',timeout=1)

EnterApProMode(switch1,'2')
SetCmd(switch1,'no ap escape',timeout=1)
IdleAfter(1)
Receiver(switch1,'y',timeout=1)


#下发配置Profile1和profile2
WirelessApplyProfileWithCheck(switch1,['1','2'],[ap1mac,ap2mac])
# pc1恢复
SetCmd(pc1,'route del -net 192.168.81.0/24 gw '+gw)
#end
printTimer(testname, 'End')