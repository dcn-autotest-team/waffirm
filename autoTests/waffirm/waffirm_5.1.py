#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_5.1.py - test case 5.1 of waffirm
#
# Author:  qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 5.1 CAPWAP管理（仅R4 AP支持）
# 测试目的：测试AC和AP通过标准capwap协议，建立隧道，AP被AC管理
# 测试环境：同测试拓扑
# 测试描述：AC和AP通过标准capwap协议，建立隧道，AP1被AC1（S1）管理。（R3 AP不支持该功能）
#
#*******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 5.1'
avoiderror(testname)
printTimer(testname,'Start','Test manage ap via capwap protocol')

suggestionList = ['Suggestions: 5.1 testcase of capwap,NEW version now under developing,you can ignore this']

################################################################################
#Step 1
#操作
#配置AP1使用标准capwap协议
#WLAN-AP# set managed-ap managed-type 1
#WLAN-AP# save-running

#配置成功，get managed-ap显示“managed-type”为“1”
################################################################################
printStep(testname,'Step 1',
          'set managed-ap managed-type 1 on ap1')
#operate

SetCmd(ap1,'set managed-ap managed-type','1')
SetCmd(ap1,'set managed-ap switch-address-1',StaticIpv4_ac1)
SetCmd(ap1,'save-running')

#check
data1 = SetCmd(ap1,'get managed-ap')
res1 = CheckLine(data1,'managed-type\s+1')

#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#重起AP1
#WLAN-AP#reboot
#AP重起后重新被AC1管理，AC1上show wi ap status显示AP的“Status”为“Managed”，
#“Configuration Status”为“Success”
################################################################################

printStep(testname,'Step 2',
          'Reboot ap and managed successful')

RebootAp(AP=ap1)
data1 = SetCmd(switch1,'show wireless ap status')
res1 = CheckLine(data1,ap1mac,'Managed Success')

#result
printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#配置SSID：test_capwap后配置下发
#S1#config 
#S1(config)#wireless 
#S1(config-wireless)#network 92
#S1(config-network)#vlan 4092
#S1(config-network)#ssid test_capwap
#S1(config-network)#exit
#S1(config-wireless)#ap profile 1
#S1(config-ap-profile)#radio 1 
#S1(config-ap-profile-radio)#vap 4
#S1(config-ap-profile-vap)#network 92
#S1(config-ap-profile-vap)#enable
#S1(config-ap-profile-vap)#end
#S1#wireless ap profile apply 1
#预期
#配置下发成功，STA可以扫描到SSID：test_capwap
################################################################################

printStep(testname,'Step 3',
          'Config network 92 and ssid test_capwap')

EnterNetworkMode(switch1,'92')
SetCmd(switch1,'vlan',Vlan4092)
SetCmd(switch1,'ssid','test_capwap')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 1')
SetCmd(switch1,'radio 1')
SetCmd(switch1,'vap 4')
SetCmd(switch1,'network 92')
SetCmd(switch1,'enable')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')
# IdleAfter(Apply_profile_wait_time)

for tmpCounter in xrange(0,10):
    StaScanSSID(sta1,Netcard_sta1)
    IdleAfter('5')
    data = SetCmd(sta1,'wpa_cli -i '+ Netcard_sta1 +' scan_results')
    if 0 == CheckLine(data,ap1mac_lower,'\[ESS\] test_capwap'):
        break
res1 = CheckLine(data,ap1mac_lower,'WPA',Network_name1)
res2 = CheckLine(data,ap1mac_lower,'WEP',Network_name1)

printCheckStep(testname, 'Step 3',not res1,not res2)

################################################################################
#Step 4
#操作
#STA关联SSID：test_capwap
#
#预期
#STA关联成功，获取192.168.92.x的ip地址，AC上show wireless client summary可以看到STA，STA可以ping通网关
################################################################################

printStep(testname,'Step 4',
          'STA1 can connect with network1,',
          'show wireless client summary and STA1 client online.')

res3 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,'test_capwap',connectType='open',checkDhcpAddress=Netcard_ipaddress_check2,bssid=ap1mac_lower)

res4 = CheckWirelessClientOnline(switch1,sta1mac,'online',retry=6)

printCheckStep(testname, 'Step 4',res3,res4)

################################################################################
#Step 5
#STA主动下线
#STA下线成功，AC上show wireless client summary看不到STA
################################################################################

printStep(testname,'Step 5',
          'Wireless client offline should be success')

res1 = WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

res2 = CheckWirelessClientOnline(switch1,sta1mac,'offline')

#result
printCheckStep(testname, 'Step 5',res1,res2)

################################################################################
#Step 6
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 6',
          'Recover initial config for switches.')

#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 1')
SetCmd(switch1,'radio 1')
SetCmd(switch1,'vap 4')
SetCmd(switch1,'network 5')
SetCmd(switch1,'no enable')
EnterWirelessMode(switch1)
SetCmd(switch1,'no network 92')
SetCmd(ap1,'set managed-ap managed-type 0')
SetCmd(ap1,'set managed-ap switch-address-1')
SetCmd(ap1,'save-running')
RebootAp(AP=ap1)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')
# IdleAfter(Apply_profile_wait_time)
#end
printTimer(testname, 'End',suggestion = suggestionList)