 #-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.4.7.py - test case 4.4.7 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 4.4.7	动态黑名单
# 测试目的：测试AC上面的动态黑名单功能
# 测试环境：同测试拓扑
# 测试描述：AC上面启用动态黑名单功能以后，能够实现动态黑名单，黑名单的客户端，
#           在线的会被踢下线，不在线的不能关联成功
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package

#Global Definition
Dynamic_blacklist_lifetime_360 = '360'
Auth_threshold_value_2 = '2'
Auth_threshold_value_600 = '600'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.4.7'
printTimer(testname,'Start','test dynamic black list feature')

################################################################################
#Step 1
#操作
#在无线全局模式下设置mac认证模式为黑名单，network1下认证为mac本地认证，
#并且下发配置到AP
#
#预期
# Show wireless network 1有：
# MAC Authentication......... Local
# show running-config |include black有： 
#  mac-authentication-mode black-list
# 下发配置后，show wireless ap status 显示AP能正常上线
################################################################################
printStep(testname,'Step 1',\
                   'Config "mac-authentication-mode" to be black-list')

res1=res2=res3=1
#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no known-client ' + sta1mac)
SetCmd(switch1,'mac-authentication-mode black-list')
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'mac authentication local')
IdleAfter(60)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')
    
# IdleAfter(Ac_ap_syn_time)
    
data1 = SetCmd(switch1,'show wireless network 1')
data2 = SetCmd(switch1,'show running-config | include black')
data3 = SetCmd(switch1,'show wireless ap status')

#check
res1 = CheckLine(data1,'MAC Authentication','Local',IC=True)
res2 = CheckLine(data2,'mac-authentication-mode black-list',IC=True)
res3 = CheckLine(data3,ap1mac,Ap1_ipv4,'Managed','Success',IC=True)

if res3 != 0:
    for tmpCounter in xrange(0,6):
        IdleAfter('10')
        data3 = SetCmd(switch1,'show wireless ap status')
        res3 = CheckLine(data3,ap1mac,Ap1_ipv4,'Managed','Success',IC=True)
        if res3 == 0:
            break

#result
printCheckStep(testname, 'Step 1',res1,res2,res3)

################################################################################
#Step 2
#操作
#Sta1关联test1
#
#预期
#show wireless client status显示sta1能关联成功
################################################################################
printStep(testname,'Step 2',\
          'STA1 connect to test1',\
          'show wireless client status to check if STA1 connected succeed')

res1=res2=1

#operate

#STA1关联 test1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)

#!!!!!!!!!!!!!!!!此处直接show无结果
EnterEnableMode(switch1)
i_times = 0
while i_times < 10:
    data1 = SetCmd(switch1,'show wireless client status')
    if 0 == CheckLine(data1,sta1mac,ap1mac,Network_name1,'Auth',IC=True):
        res2 = 0
        break
    IdleAfter(5)
    i_times += 1    

#check

#result
printCheckStep(testname, 'Step 2',res1,res2)

################################################################################
#Step 3
#操作
#无线全局模式打开动态黑名单，并且设置动态黑名单的存活时间为360s
# Switch(config-wireless)#dynamic-blacklist 
# Switch(config-wireless)#dynamic-blacklist lifetime 360

#预期
#show running-config |include dynamic显示lifetime 为360
################################################################################
printStep(testname,'Step 3',\
          'Enable dynamic-blacklist',\
          'Config dynamic-blacklist lifetime to 360s')

res1=1
#operate

EnterWirelessMode(switch1)
SetCmd(switch1,'dynamic-blacklist')
SetCmd(switch1,'dynamic-blacklist lifetime',Dynamic_blacklist_lifetime_360)

data1 = SetCmd(switch1,'show running-config | include','dynamic')

#check
res1 = CheckLine(data1,Dynamic_blacklist_lifetime_360)

#result
printCheckStep(testname,'Step 3',res1)

################################################################################
#Step 4
#操作
#在无线全局模式设置客户端认证帧检测的阈值为2
#
#预期
#show wireless wids-security client显示 Auth threshold value 为2
################################################################################
printStep(testname,'Step 4',\
          'Set "wids-security client threshold-value-auth" to 2')

res1=1

#operate
EnterWirelessMode(switch1)         
SetCmd(switch1,'wids-security client threshold-value-auth',Auth_threshold_value_2)

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless wids-security client')

#check
res1 = CheckLine(data1,'Auth threshold value',Auth_threshold_value_2)
    
#result
printCheckStep(testname, 'Step 4',res1)

################################################################################
#Step 5
#操作
#sta1，sta2在1分钟之内发送3次以上的认证报文
#
#预期
#show wireless dynamic-blacklist显示sta1和sta2都在动态黑名单里面
################################################################################
printStep(testname,'Step 5',\
          'STA1 and STA2 send auth packets more than 3 times in 1 minute',\
          'Check if the blacklist contain STA1 and STA2')

res1=1

#operate
SetCmd(sta1,'dhclient -r '+ Netcard_sta1)
SetCmd(sta1,'wpa_cli -i '+Netcard_sta1+' disable_network 0')
SetCmd(sta1,'wpa_cli -i '+ Netcard_sta1 + ' remove_network 0')
SetCmd(sta1,'wpa_cli -i '+ Netcard_sta1 + ' add_network 0')
SetCmd(sta1,'wpa_cli -i ' + Netcard_sta1 + ' set_network 0 key_mgmt NONE')
SetCmd(sta1,'wpa_cli -i ' + Netcard_sta1 + ' set_network 0 ssid','\'"'+ Network_name1 +'"\'')                                                      
SetCmd(sta1,'wpa_cli -i ' + Netcard_sta1 + ' set_network 0 bssid',ap1mac_lower)
SetCmd(sta2,'dhclient -r '+ Netcard_sta2)
SetCmd(sta2,'wpa_cli -i '+ Netcard_sta2 + ' remove_network 0')
SetCmd(sta2,'wpa_cli -i '+ Netcard_sta2 + ' add_network 0')
SetCmd(sta2,'wpa_cli -i ' + Netcard_sta2 + ' set_network 0 key_mgmt NONE')
SetCmd(sta2,'wpa_cli -i ' + Netcard_sta2 + ' set_network 0 ssid','\'"'+ Network_name1 +'"\'')                                                      
SetCmd(sta2,'wpa_cli -i ' + Netcard_sta2 + ' set_network 0 bssid',ap1mac_lower)

#关联操作，sta会发送认证报文
for i in range(6):
    SetCmd(sta1,'wpa_cli -i '+Netcard_sta1+' enable_network 0')
    SetCmd(sta2,'wpa_cli -i '+Netcard_sta2+' enable_network 0')
    SetCmd(sta1,'wpa_cli -i '+Netcard_sta1+' enable_network 0')
    SetCmd(sta2,'wpa_cli -i '+Netcard_sta2+' enable_network 0')
    SetCmd(sta1,'wpa_cli -i '+Netcard_sta1+' enable_network 0')
    SetCmd(sta2,'wpa_cli -i '+Netcard_sta2+' enable_network 0')
    IdleAfter(3)
    SetCmd(sta1,'wpa_cli -i '+Netcard_sta1+' disable_network 0')
    SetCmd(sta2,'wpa_cli -i '+Netcard_sta2+' disable_network 0') 
    IdleAfter(2)
 
#发完认证报文之后，需要等待一定时间，s 级别    
EnterEnableMode(switch1)
i_times = 0
while i_times < 20: 
    data1 = SetCmd(switch1,'show wireless dynamic-blacklist')
    if 0 ==  CheckLineList(data1,[(sta1mac),(sta2mac)],IC=True):
        res1 = 0
        break
    i_times += 1
    IdleAfter(3)

#check

#result
printCheckStep(testname, 'Step 5',res1)

################################################################################
#Step 6
#操作
#上一步过2分钟后，sta2去认证test1
#
#预期
#show wireless client status显示sta1已经下线，sta2不能够认证上test1
################################################################################
printStep(testname,'Step 6',\
          'Wait for 2 minutes after the last step,then STA2 connect to test1',\
          'Check if STA2 was denied and STA1 was deauthed')
          
res1=0
res2=1 
#operate
IdleAfter(120)
res1 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap1mac_lower)
res1 = 0 if 0 != res1 else 1

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless client status')
    
#check
res2 = CheckNoLineList(data1,[(sta1mac,ap1mac,Network_name1,'Auth')],IC=True)

#disable掉sta1,sta2的关联操作，否则会在后台一直尝试关联，导致black-list无法清空
SetCmd(sta1,'dhclient -r '+ Netcard_sta1)
SetCmd(sta2,'dhclient -r '+ Netcard_sta2)
SetCmd(sta1,'wpa_cli -i '+Netcard_sta1+' disable_network 0')
SetCmd(sta2,'wpa_cli -i '+Netcard_sta2+' disable_network 0')

#result
printCheckStep(testname, 'Step 6',res1,res2)

################################################################################
#Step 7
#操作
# 在无线全局模式设置客户端认证帧检测的阈值为600
# Switch(config-wireless)#wids-security client threshold-value-auth 600
# 并等待 361
#
#预期
#show wireless wids-security client显示 Auth threshold value 为600
#361秒以后，show wireless dynamic-blacklist显示sta1和sta2都不在动态黑名单里面
################################################################################
printStep(testname,'Step 7',\
          'Set "wids-security client threshold-value-auth" to 600',\
          'Wait for 361s and check dynamic-blacklist')
          
res1=res2=1

#operate

#设置客户端认证帧检测的阈值
EnterWirelessMode(switch1)         
SetCmd(switch1,'wids-security client threshold-value-auth',Auth_threshold_value_600)
SetCmd(switch1,'wids-security client threat-mitigation')
SetCmd(switch1,'wids-security client auth-with-unknown-ap')
SetCmd(switch1,'wids-security client known-client-database ')

#等待至blacklist包含STA1、STA2
EnterEnableMode(switch1)
i_times = 0
while i_times < 20: 
    data1 = SetCmd(switch1,'show wireless dynamic-blacklist')
    if 0 == CheckLineList(data1,[(sta1mac),(sta2mac)],IC=True):
        break
    i_times += 1
    IdleAfter(2)
    
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless wids-security client')
data2 = SetCmd(switch1,'show wireless dynamic-blacklist')

#check
res1 = CheckLine(data1,'Auth threshold value',Auth_threshold_value_600,IC=True)     
res2 = CheckNoLineList(data2,[(sta1mac),(sta2mac)],IC=True)
IdleAfter(30)
data2 = SetCmd(switch1,'show wireless dynamic-blacklist')
res3 = CheckNoLineList(data2,[(sta1mac),(sta2mac)],IC=True)
IdleAfter(30)
data2 = SetCmd(switch1,'show wireless dynamic-blacklist')
res4 = CheckNoLineList(data2,[(sta1mac),(sta2mac)],IC=True)
    
#result
printCheckStep(testname, 'Step 7',res1,res3,res4)

################################################################################
#Step 8
#操作
#使用sta1,sta2关联到test1
#
#预期
#可以关联成功
###############################################################################
printStep(testname,'Step 8',\
          'STA1,STA2 connects to test1')
                   
res1=res2=1

#operate
  
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap1mac_lower)

#check

#result
printCheckStep(testname, 'Step 8',res1,res2)
###############################################################################
#Step 9
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 9',\
          'Recover initial config for switches.')

#operate

#解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

#清除 mac authentication local配置
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no mac authentication')
EnterWirelessMode(switch1)
SetCmd(switch1,'no mac-authentication-mode')

#清除dynamic-blacklist 表项
EnterEnableMode(switch1)
SetCmd(switch1,'clear wireless dynamic-blacklist')

# WirelessApProfileApply(switch1,'1')

EnterWirelessMode(switch1)
SetCmd(switch1,'no dynamic-blacklist')
SetCmd(switch1,'no dynamic-blacklist lifetime')
SetCmd(switch1,'no wids-security client threshold-value-auth')
SetCmd(switch1,'no wids-security client threat-mitigation')
SetCmd(switch1,'no wids-security client auth-with-unknown-ap')
SetCmd(switch1,'no wids-security client known-client-database ')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# IdleAfter(Ac_ap_syn_time)

#end
printTimer(testname, 'End')