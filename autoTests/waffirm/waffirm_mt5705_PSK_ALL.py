#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_mt5705_PSK.py
#
# Author:  (zhangjxp)
#
# Version 1.0.0
#
# Date:  2017-4-27 9:54:28
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# mt5705  PSK密码中包含特殊字符测试
# 测试目的：采用PSK认证方式时，PSK的密码配置成特殊字符，无线用户STA1可以成功接入
# 测试环境：同测试拓扑
# 测试描述：1.把PSK密码配置成特殊字符，无线用户STA1可以成功接入并获取IP地址
# 2.AC重启后，配置的PSK密码不丢失且无线用户可以成功接入并获取IP地址
# 3.恢复默认配置
#
#*******************************************************************************
# Change log:
#     - creadte by zhangjxp 2017.4.27
#     - modified by zhangjxp 2017.11.16 RDM50376
#*******************************************************************************
#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase mt5705_PSK'
avoiderror(testname)
printTimer(testname,'Start')

################################################################################
#Step 1
#
#操作
# 配置AC1的network1的安全接入方式为WPA-Personal，密码为@ # $ % ^ & * ( ) - _ = + ` ~ \ | [ { ] } ; : ' " , < . > / 
#
#预期
# 配置成功，在AC1上面Show wireless network 1可以看到相关的配置。
#
################################################################################
printStep(testname,'Step 1',
          'set security mode of network 1 WPA-Personal,',
          'set psk @ # $ % ^ & * ( ) - _ = + ` ~ \ | [ { ] } ; : \' \" , < . > / ',
          'check configuration')
res1=1
#operate
#AC1配置
passwordpsk1='@ # $ % ^ & * ( ) - _ = + ` ~ \ | [ { ] } ; : , < . > /'
EnterWirelessMode(switch1)
SetCmd(switch1,'network 1')
SetCmd(switch1,'Security mode wpa-personal')
SetCmd(switch1,'Wpa key',passwordpsk1)
SetCmd(switch1,'Wpa versions wpa')
data=Receiver(switch1,'show run c',timeout=3)
res1=CheckLine(data,
               'security mode wpa-personal',
               'wpa key encrypted',
               'wpa versions wpa',
               ML = True)

#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#操作
# 将配置下发到AP1
#
#预期
# 配置下发成功
################################################################################
printStep(testname,'Step 2',
          'Apply ap profile 1')

#operate
# WirelessApProfileApply(switch1,'1')
# IdleAfter(Apply_profile_wait_time)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#result
printCheckStep(testname, 'Step 2', 0)

################################################################################
#Step 3

#操作
# 设置STA1无线网卡的属性为WPA-PSK认证，正确输入密码，关联网络test1。
#
#预期
# 成功关联，并获取192.168.91.X网段的IP地址。Show wireless client summery
# 可以看到STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
################################################################################
printStep(testname,'Step 3',
          'STA1 connect to test1')

res1=1
res2=1
#operate

res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='wpa_psk',psk=passwordpsk1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
IdleAfter(10)
# check
res2 = CheckWirelessClientOnline(switch1,sta1mac,'online',retry=12,interval=10)
#result
printCheckStep(testname, 'Step 3',res1,res2)

################################################################################
#Step 4
#操作
# 在STA1上面ping PC1
#
#预期
# 能够ping通。
################################################################################

printStep(testname,'Step 4',
          'sta1 ping pc1 successfully')
          
res1=1
#operate&check
res1 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
#result
printCheckStep(testname, 'Step 4',res1)

################################################################################
#Step 5
#操作
# 配置AC1的network1的安全接入方式为WPA-Personal，密码为%%%%%%%%
#
#预期
#配置成功。在AC1上面Show wireless network 1可以看到相关的配置
################################################################################

printStep(testname,'Step 5',
          'set security mode of network 1 WPA-Personal,',
          'set psk %%%%%%%%',
          'check configuration')

res1=1
#operate
# AC1配置
#AC1配置
passwordpsk2='%%%%%%%%'
EnterWirelessMode(switch1)
SetCmd(switch1,'network 1')
SetCmd(switch1,'Security mode wpa-personal')
SetCmd(switch1,'Wpa key',passwordpsk2)
SetCmd(switch1,'Wpa versions wpa')
data=Receiver(switch1,'show run c',timeout=3)
res1=CheckLine(data,
               'security mode wpa-personal',
               'wpa key encrypted',
               'wpa versions wpa',
               ML = True)
#result
printCheckStep(testname, 'Step 5', res1)
################################################################################
#Step 6
#重复步骤2-4
################################################################################
printStep(testname,'Step 6',
          'repeat step 2-4')
res1=1
res2=1
res3=1
#operate
# WirelessApProfileApply(switch1,'1')
# IdleAfter(Apply_profile_wait_time)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='wpa_psk',psk=passwordpsk2,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
IdleAfter(10)
# check
res2 = CheckWirelessClientOnline(switch1,sta1mac,'online',retry=12,interval=10)
res3 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
#result
printCheckStep(testname, 'Step 6',res1,res2,res3)
################################################################################
#Step 7
#操作
# 配置AC1的network1的安全接入方式为WPA-Personal，密码为%%%%%%%%^
#
#预期
#配置成功。在AC1上面Show wireless network 1可以看到相关的配置
################################################################################

printStep(testname,'Step 7',
          'set security mode of network 1 WPA-Personal,',
          'set psk %%%%%%%%^',
          'check configuration')

res1=1
#operate
# AC1配置
passwordpsk3='%%%%%%%%^'
EnterWirelessMode(switch1)
SetCmd(switch1,'network 1')
SetCmd(switch1,'Security mode wpa-personal')
SetCmd(switch1,'Wpa key',passwordpsk3)
SetCmd(switch1,'Wpa versions wpa')
data=Receiver(switch1,'show run c',timeout=3)
res1=CheckLine(data,
               'security mode wpa-personal',
               'wpa key encrypted',
               'wpa versions wpa',
               ML = True)
#result
printCheckStep(testname, 'Step 7', res1)
################################################################################
#Step 8
#重复步骤2-4
################################################################################
printStep(testname,'Step 8',
          'repeat step 2-4')
res1=1
res2=1
res3=1
#operate
# WirelessApProfileApply(switch1,'1')
# IdleAfter(Apply_profile_wait_time)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='wpa_psk',psk=passwordpsk3,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
IdleAfter(10)
# check
res2 = CheckWirelessClientOnline(switch1,sta1mac,'online',retry=12,interval=10)
res3 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
#result
printCheckStep(testname, 'Step 8',res1,res2,res3)

################################################################################
#Step 9
#保存AC配置，重启AC	AC重启后，在AC1上面Show wireless network 1可以看到AC重启后配置没有丢失。
################################################################################
printStep(testname,'Step 9',
          'Write and reload AC1',
          'The psk configuration is not lost')
res1=1
#operate
EnterEnableMode(switch1)
Receiver(switch1,'write',timeout=1)
IdleAfter(1)
Receiver(switch1,'y')
IdleAfter(5)
ReloadMultiSwitch([switch1])
EnterWirelessMode(switch1)
SetCmd(switch1,'network 1')
data=Receiver(switch1,'show run c',timeout=3)
res1=CheckLine(data,
               'security mode wpa-personal',
               'wpa key encrypted',
               'wpa versions wpa',
               ML = True)
printCheckStep(testname, 'Step 9',res1)
################################################################################
#Step 10
# 当AP被成功管理后，重复步骤3-4	
# STA1可以成功关联并获取192.168.91.X网段的IP地址。
# Show wireless client summery可以看到STA1（“MAC Address”显示“STA1MAC”），
# IP地址的网段正确。STA1能ping通PC1。
################################################################################
printStep(testname,'Step 10',
          'repeat step3-4')

res1=1
res2=1
res3=1
#operate
i = 1
while i<30:
	EnterEnableMode(switch1)
	data1 = SetCmd(switch1,'show wireless ap status')
	res = CheckLine(data1,ap1mac,Ap1_ipv4,'1','Managed','Success',IC=True)
	if res == 0:
		break
	IdleAfter('5')
	i = i + 1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='wpa_psk',psk=passwordpsk3,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
IdleAfter(10)
# check
res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
res3 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
#result
printCheckStep(testname, 'Step 10',res1,res2,res3)
################################################################################
#Step 11
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 11',
          'Recover initial config')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
# AC1恢复
EnterConfigMode(switch1)
SetCmd(switch1,'wireless')
SetCmd(switch1,'network 1')
SetCmd(switch1,'no security mode')
SetCmd(switch1,'no wpa versions')
SetCmd(switch1,'no wpa key')
SetCmd(switch1,'end')

WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#end
printTimer(testname, 'End')