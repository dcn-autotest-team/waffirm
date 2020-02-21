#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.4.5.py - test case 4.4.5 of waffirm_new
#
# Author:  (jinpfb)
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Date: 2012-12-13 14:11:34
#
# Features:
# 4.4.5 AP威胁检测
# 测试目的：测试AP对各种威胁的检测
# 测试环境：见测试拓扑
# 测试描述：系统可以检测的AP的威胁有11种，此处并不对全部的11种进行测试。
# 由于条件限制，此处用AP2作为rouge ap
#
#*******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.4.5'
avoiderror(testname)
printTimer(testname,'Start','test detection of AP threat')

suggestionList = []
# 2.4G、5G差异化配置,test24gflag为True代表执行2.4G脚本，False代表执行5G脚本
# if test24gflag ==  True:
    # wlan='wlan0'
# else:
    # wlan='wlan1'
################################################################################
#Step 1
#操作
# 在ac1配置network1的SSID为test1，关联vlan4091，下发配置。
# AP2断开网络连接
#
#预期
# 配置成功，show wireless ap status，
# AP1的管理状态为managed
################################################################################
printStep(testname,'Step 1',
          'Set network1 related to vlan 4091',
          'AP2 connect to AC2')

res1=res2=1
#operate
# network1配置与初始化配置相同，不需重复配置
# #修改network1关联vlan为4091
# EnterNetworkMode(switch1, '1')
# SetCmd(switch1,'vlan '+Vlan4091)

# ##SetCmd(switch1,'wireless ap profile apply 1',timeout=1)
# ##SetCmd(switch1,'y',timeout=1)
# ## RDM36362
# WirelessApProfileApply(switch1,'1')

#增加断开集群
EnterWirelessMode(switch2)
SetCmd(switch2,'peer-group 2')
IdleAfter(3)
SetCmd(switch2,'peer-group 1')

#AP2 断开网络连接，此处采取shutdown s3p4端口

EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery ip-list ' + Ap2_ipv4)

EnterWirelessMode(switch2)
SetCmd(switch2,'discovery ip-list ' + Ap2_ipv4)

EnterInterfaceMode(switch3,s3p4)
SetCmd(switch3,'shutdown')

IdleAfter(80)

SetCmd(switch3,'no shutdown')

IdleAfter(20)
EnterEnableMode(switch1)
EnterEnableMode(switch2)
res1=CheckSutCmd(switch1,'show wireless ap status',
                 check=[(ap1mac,'Managed','Success')],
                 waittime=5,retry=10,interval=5,IC=True)
                
res2=CheckSutCmd(switch2,'show wireless ap status',
                 check=[(ap2mac,'Managed','Success')],
                 waittime=5,retry=20,interval=5,IC=True)
                
data = SetCmd(switch1,'show wireless network 1',timeout=5)
res3 = CheckLine(data,'Default VLAN',Vlan4091,IC=True)                


# #check
# for i in range(16): 
	# data1 = SetCmd(switch1,'show wireless ap status')
	# data2 = SetCmd(switch1,'show wireless network 1')
	# data3 = SetCmd(switch2,'show wireless ap status')
	# res1 = CheckLine(data1,ap1mac,'Managed','Success',IC=True)
	# res2 = CheckLine(data2,'Default VLAN',Vlan4091,IC=True)
	# res3 = CheckLine(data3,ap2mac,'Managed','Success',IC=True) 
	# if res1==0 and res2 == 0 and res3==0:
		# break
	# IdleAfter(5)

EnterEnableMode(switch1)
SetCmd(switch1,'clear wireless AP failed',timeout=1)
SetCmd(switch1,'y',timeout=1)

#result
printCheckStep(testname, 'Step 1',res1,res2,res3)

################################################################################
#Step 2
#操作
#开启无线安全，并且打开所有的检查项；并且将AP1设置为Sentry Mode
#
#预期
#配置并下发成功，AP1的状态还是managed
################################################################################

printStep(testname,'Step 2',
          'Open wireless security,lanuch all entries',
          'Set AP1 to Sentry Mode')

res1=res2=1
#operate

#无线安全功能默认已经打开
EnterWirelessMode(switch1) 
SetCmd(switch1,'wids-security admin-config-rogue')
SetCmd(switch1,'wids-security ap-chan-illegal')
SetCmd(switch1,'wids-security fakeman-ap-chan-invalid')
SetCmd(switch1,'wids-security fakeman-ap-managed-ssid')
SetCmd(switch1,'wids-security fakeman-ap-no-ssid')
SetCmd(switch1,'wids-security managed-ap-ssid-invalid')
SetCmd(switch1,'wids-security managed-ssid-secu-bad')
SetCmd(switch1,'wids-security standalone-cfg-invalid')
SetCmd(switch1,'wids-security unknown-ap-managed-ssid')
SetCmd(switch1,'wids-security unmanaged-ap-wired')
SetCmd(switch1,'wids-security wds-device-unexpected')
SetCmd(switch1,'wids-security ap-de-auth-attack')

EnterApProMode(switch1,'1')
SetCmd(switch1,'radio '+radionum)
SetCmd(switch1,'rf-scan sentry')

## RDM36362
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless wids-security')
data2 = SetCmd(switch1,'show wireless ap profile 1 radio '+radionum)

#check
checklist = []
for i in range(11):
    checklist.append('Rogue.*\.\s+Enable')

res1 = CheckLineList(data1,checklist,IC=True)
res2 = CheckLine(data2,'Sentry Mode','Enable',IC=True)

#result
printCheckStep(testname, 'Step 2',res1,res2)

################################################################################
#Step 3
#操作
#在ac1，将 ap1 的authentication mode设置为mac，将AP2 在ap database上设置为rouge AP
#
#预期
# 用命令 show wireless ap <ap2 mac>  rf-scan rogue-classification
# 查看，AP2显示为rogue AP，类型为Administrator configured rogue AP
################################################################################

printStep(testname,'Step 3',
          'Set AP1 authentication mode to be mac',
          'Set AP2 to be rouge AP on ap database')

res1=res2=1

#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap authentication mac')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap2mac)
SetCmd(switch1,'mode rogue')

data1 = SetCmd(switch1,'show wireless')
EnterEnableMode(switch1)
SetCmd(switch1,'clear wireless AP failed',timeout=1)
SetCmd(switch1,'y',timeout=1)

SetCmd(switch1,'clear wireless ap rf-scan list',timeout=1)
SetCmd(switch1,'y',timeout=1)
# IdleAfter(80)

#check
res1 = CheckLine(data1,'Authentication Mode','Mac',IC=True)
for i in range(16): 
	data2 = SetCmd(switch1,'show wireless ap',ap2mac,'rf-scan rogue-classification')
	res2 = CheckLine(data2,'WIDSAPROGUE01 True')
	if res1==0 and res2 == 0:
		break
	IdleAfter(5)	

#result
printCheckStep(testname,'Step 3',res1,res2)

################################################################################
#Step 4 
# 操作
# 将在ac2配置network1的SSID为test1，下发配置。
# 在ac1的ap database中删除AP2的信息。
#
# 预期
# 用命令 show wireless ap <ap2 mac>  rf-scan rogue-classification
# 查看，该AP2显示为rogue AP，类型为Managed SSID from an unknown AP
################################################################################
printStep(testname,'Step 4',
          'Use AP2 as fat ap,set ssid to be test1',
          'Delete AP2 info in ap database of AC1',
          'Check AP2 status on AC1')

res1=1

#operate
SetCmd(ap2,'set interface '+wlan+' ssid',Network_name1)
SetCmd(ap2,'ifconfig ath1 down')
IdleAfter(30)
EnterWirelessMode(switch1)
SetCmd(switch1,'no ap database',ap2mac)
EnterEnableMode(switch1)
SetCmd(switch1,'clear wireless ap rf-scan list',timeout=1)
SetCmd(switch1,'y',timeout=1)

# IdleAfter(60)

# data1 = SetCmd(switch1,'show wireless ap',ap2mac,'rf-scan rogue-classification') 

#check
# res1 = CheckLine(data1,'WIDSAPROGUE02 True')
# if res1 != 0:
    # IdleAfter(30)
    # data1 = SetCmd(switch1,'show wireless ap',ap2mac,'rf-scan rogue-classification') 
    # res1 = CheckLine(data1,'WIDSAPROGUE02 True')
# if res1 != 0:
    # IdleAfter(30)
    # data1 = SetCmd(switch1,'show wireless ap',ap2mac,'rf-scan rogue-classification') 
    # res1 = CheckLine(data1,'WIDSAPROGUE02 True')

for i in range(24): 
	data1 = SetCmd(switch1,'show wireless ap',ap2mac,'rf-scan rogue-classification')
	res1 = CheckLine(data1,'WIDSAPROGUE02 True')
	if res1==0:
		break
	IdleAfter(5)	
	
#result
printCheckStep(testname, 'Step 4',res1)

################################################################################
#Step 7 
#配置wids-security ap-de-auth-attack，当有client连接到以上rogue AP时，在空口抓包
#能够看到AP发送的反制报文
################################################################################
##printStep(testname,'Step 7',\
##          'sta connect to rogue ap and continue receive deauthentication packet')
##

##
##SetCmd(sta1,'tcpdump -i mon0 -vvv | grep 'DeAuthentication.*' + ap2mac_lower + ''',timeout=1)
##StartDebug(sta1)
##IdleAfter(30)
##SetCmd(sta1,'\x03',timeout=1)
##data1 = StopDebug(sta1)
##
###check
##res1 = CheckLine(data1,'DeAuthentication \(' + ap2mac_lower)
##if res1 != 0:
##    SetCmd(sta1,'tcpdump -i mon0 -vvv | grep 'DeAuthentication.*' + ap2mac_lower + ''',timeout=1)
##    StartDebug(sta1)
##    IdleAfter(30)
##    SetCmd(sta1,'\x03',timeout=1)
##    data1 = StopDebug(sta1)
##    res1 = CheckLine(data1,'DeAuthentication \(' + ap2mac_lower)
##if res1 != 0:
##    SetCmd(sta1,'tcpdump -i mon0 -vvv | grep 'DeAuthentication.*' + ap2mac_lower + ''',timeout=1)
##    StartDebug(sta1)
##    IdleAfter(30)
##    SetCmd(sta1,'\x03',timeout=1)
##    data1 = StopDebug(sta1)
##    res1 = CheckLine(data1,'DeAuthentication \(' + ap2mac_lower)
##if res1 != 0:
##    SetCmd(sta1,'tcpdump -i mon0 -vvv | grep 'DeAuthentication'',timeout=1)
##    StartDebug(sta1)
##    IdleAfter(30)
##    SetCmd(sta1,'\x03',timeout=1)
##    data1 = StopDebug(sta1)
##    suggestionList.append('Suggestions: Step 7 failed reason MAYBE RDM27627')
###result
##printCheckStep(testname, 'Step 7',res1)

################################################################################
#Step 5 
# 操作
#在ac2配置network1的SSID为test1，隐藏ssid，下发配置。
#发送不带SSID的beacon帧
#
# 预期
# 用命令 show wireless ap <ap2 mac>  rf-scan rogue-classification
# ，该AP2显示为rogue AP，类型为AP without an SSID
################################################################################
printStep(testname,'Step 5',
          'Use AP2 as fat ap,hide ssid',
          'Send beacon frame without SSID',
          'Check AP2 status on AC1')

res1=1
# WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap2mac_lower)
# WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap2mac_lower)
#operate
EnterWirelessMode(switch2)
SetCmd(switch2,'network 1')
SetCmd(switch2,'hide-ssid')
##EnterEnableMode(switch2)
##SetCmd(switch2,'wireless ap profile apply','2',timeout=1)
##SetCmd(switch2,'y',timeout=1)
## RDM36362
# WirelessApProfileApply(switch2,'2')

# IdleAfter(120)

# data1 = SetCmd(switch1,'show wireless ap',ap2mac,'rf-scan rogue-classification') 

#check
# res1 = CheckLine(data1,'WIDSAPROGUE04 True')
WirelessApplyProfileWithCheck(switch2,['2'],[ap1mac])
for i in range(16): 
	data1 = SetCmd(switch1,'show wireless ap',ap2mac,'rf-scan rogue-classification') 
	res1 = CheckLine(data1,'WIDSAPROGUE04 True')
	if res1==0:
		break
	IdleAfter(5)	
#result
printCheckStep(testname, 'Step 5',res1)

#################################################################################
##Step 6  
## 操作
##将AP2连接到网络，等待一段时间
##
## 预期
## 用命令 show wireless ap <ap2 mac>  rf-scan rogue-classification
## ，AP2显示为rogue AP，类型为Unmanaged AP detected on wired network
#################################################################################
#printStep(testname,'Step 6',\
          #'AC1 connect to AP2',\
          #'Check AP2 status on AC1')

#res1=res2=1

##operate
#EnterWirelessMode(switch2)
#SetCmd(switch2,'no discovery ip-list ' + Ap2_ipv4)
#EnterInterfaceMode(switch3,s3p4)
#SetCmd(switch3,'shutdown')
#SetCmd(switch3,'no','shutdown')

##添加AP2
#EnterWirelessMode(switch1)
##SetCmd(switch1,'ap database',ap2mac)
##SetCmd(switch1,'profile 2')

##IdleAfter(60)

##data1 = SetCmd(switch1,'show wireless ap status')

#IdleAfter(60)
#data2 = SetCmd(switch1,'show wireless ap',ap2mac,'rf-scan rogue-classification') 

##check
#res1 = CheckLine(data2,ap2mac,'WIDSAPROGUE12 True')
##res2 = CheckLine(data1,)

##result
#printCheckStep(testname, 'Step 6',res1)

#################################################################################
##Step 7
##
## 操作 
##配置wids-security ap-de-auth-attack，当有client连接到以上rogue AP时，在空口抓包
##
## 预期
## 能够看到AP发送的反制报文
#################################################################################
#printStep(testname,'Step 7',\
          #'Set 'ap-de-auth-attack' on AC1,STA1 connect to AP2',\
          #'Capture packet')

#res1=res2=1
##operate

#EnterWirelessMode(switch1)
#SetCmd(switch1,'wids-security ap-de-auth-attack')


##AC 上开启debug，查看是否有AP的反制报文
#EnterEnableMode(switch1)
#SetCmd(switch1,'debug wireless client-disasso packet all')
#StartDebug(switch1)
#res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap2mac_lower)

#IdleAfter(10)
#data1 = StopDebug(switch1)
#res2 = CheckLine(data1,)
     
##result
#printCheckStep(testname, 'Step 7',res1,res2)

################################################################################
#Step 8
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 8',
          'Recover initial config')

#operate

# STA1 解关联
# WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
# WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

#network1 关联至4091
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'vlan '+Vlan4091)

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list ' + Ap2_ipv4)

EnterWirelessMode(switch2)
SetCmd(switch2,'no discovery ip-list ' + Ap2_ipv4)

EnterWirelessMode(switch1)
SetCmd(switch1,'ap authentication none') 
# SetCmd(switch1,'no wids-security admin-config-rogue')
SetCmd(switch1,'no wids-security ap-chan-illegal')
SetCmd(switch1,'no wids-security fakeman-ap-chan-invalid')
SetCmd(switch1,'no wids-security fakeman-ap-managed-ssid')
SetCmd(switch1,'no wids-security fakeman-ap-no-ssid')
SetCmd(switch1,'no wids-security managed-ap-ssid-invalid')
SetCmd(switch1,'no wids-security managed-ssid-secu-bad')
SetCmd(switch1,'no wids-security standalone-cfg-invalid')
SetCmd(switch1,'no wids-security unknown-ap-managed-ssid')
SetCmd(switch1,'no wids-security unmanaged-ap-wired')
SetCmd(switch1,'no wids-security wds-device-unexpected')
SetCmd(switch1,'no wids-security ap-de-auth-attack')

#关闭 AP1 sentry mode
EnterApProMode(switch1,'1')
# SetCmd(switch1,'radio 1')
SetCmd(switch1,'radio '+radionum)
SetCmd(switch1,'no rf-scan sentry')

#SetCmd(ap2,'set bss wlan0bssvap0 ignore-broadcast-ssid on')

#配置AP2 管理模式为 ws-managed  
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap2mac)
SetCmd(switch1,'profile 2')
SetCmd(switch1,'mode ws-managed')

EnterWirelessMode(switch2)
SetCmd(switch2,'network 1')
SetCmd(switch2,'no hide-ssid')
#RDM37511
EnterWirelessMode(switch2)
SetCmd(switch2,'peer-group 2')
IdleAfter(5)
SetCmd(switch2,'peer-group 1')
##EnterEnableMode(switch2)
##SetCmd(switch2,'wireless ap profile apply','2',timeout=1)
##SetCmd(switch2,'y',timeout=1)
## RDM36362
WirelessApProfileApply(switch2,'2')

#下发至AP
EnterInterfaceMode(switch3,s3p4)
SetCmd(switch3,'shutdown')

IdleAfter(80)

SetCmd(switch3,'no shutdown')
CheckSutCmd(switch1,'show wireless ap status',
            check=[(ap2mac,'Managed','Success')],
            waittime=5,retry=20,interval=5,IC=True)
##SetCmd(switch1,'wireless ap profile apply 1',timeout=1)
##SetCmd(switch1,'y',timeout=1)
## RDM36362
# WirelessApProfileApply(switch1,'1')
# IdleAfter(60)
#SetCmd(switch1,'wireless ap profile apply','2',timeout=1)
#SetCmd(switch1,'y',timeout=1)
# RDM36362
# WirelessApProfileApply(switch1,'2')
# IdleAfter(80)
WirelessApplyProfileWithCheck(switch1,['1','2'],[ap1mac,ap2mac])
#RebootAp('AC',AC=switch1,MAC=ap2mac,AP=ap2)

#end
printTimer(testname, 'End',suggestion = suggestionList)