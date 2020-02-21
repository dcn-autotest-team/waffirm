#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apwds_1.2.2.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 1.2.2	AC基本配置-wpa-personal认证方式
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.23
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase apwds_1.2.2'
avoiderror(testname)
printTimer(testname,'Start','Check Ac basic wds configuration in wpa-personal mode')

################################################################################
#Step 1
#操作
# AC配置
# network 2   
# wds-mode rootap    
# security mode wpa-personal    
# wpa key  ${psk_key}    
# wds-remote-vap  ap2mac
# ssid ${wds_ssid}
#预期
# AC上show wireless network 2，显示
# SSID........................................... ${wds_ssid}
# WDS Mode....................................... RootAP 
# WDS Remote VAP MAC............................. ap2mac
# Security Mode.................................. WPA Personal
# WPA Versions................................... WPA/WPA2 
# WPA Ciphers.................................... TKIP/CCMP
################################################################################
printStep(testname,'Step 1',\
                    'Config network 2 as wds and wpa-personal mode')
res1=1
#operate
# AC上配置network2为wds，apmode为rootap
Ac_wds_config(switch1,2,
                ssid=wds_ssid,
                remotemac=ap2vapmac,
                securitymode='wpa-personal',
                psk_key=wds_psk_key)  
data = SetCmd(switch1,'show wireless network 2')
res1 = CheckLineList(data,[('SSID',wds_ssid),
                        ('WDS Mode','RootAP'),
                        ('WDS Remote VAP MAC',ap2vapmac),
                        ('Security Mode','WPA Personal'),
                        ('WPA Versions','WPA/WPA2'),
                        ('WPA Ciphers','TKIP/CCMP')],
                        IC=True)
#result
printCheckStep(testname, 'Step 1',res1)
################################################################################
#Step 2
#操作
# AC配置
# network 2
# wpa key 12345
#预期
# 显示
# Error! Invalid key size. Key length must be more than 8 characters and less than 63 characters.
################################################################################
printStep(testname,'Step 2',\
                    'Config wpa key shorter than 8 characters')
res1=1
#operate
EnterNetworkMode(switch1,2)    
data = SetCmd(switch1,'wpa key 12345')
res1 = CheckLine(data,'Invalid key size. Key length must be more than 8 characters and less than 63 characters',IC=True)
#result
printCheckStep(testname, 'Step 2',res1)
################################################################################
#Step 3
#操作
# AC配置
# network 2
# no wds-mode
#预期
# AC上show wireless network 2，显示
# 显示WDS Mode....................................... Disable
################################################################################
printStep(testname,'Step 3',\
                    'No wds mode in network 2')
res1=1
#operate
EnterNetworkMode(switch1,2)    
data = SetCmd(switch1,'no wds-mode')
IdleAfter(5)
data = SetCmd(switch1,'show wireless network 2')
res1 = CheckLine(data,'WDS Mode','Disable',IC=True)
#result
printCheckStep(testname, 'Step 3',res1)
################################################################################
#Step 4
#操作
# AC配置
# network 2   
# wds-mode rootap    
# security mode wpa-personal    
# wpa key  ${psk_key}    
# wds-remote-vap  ap2mac
# ssid ${wds_ssid}
# 下发配置apply ap profile 1
#预期
# AP1上get wds wds1
# 显示
# radio wlan0 
# wds-status up 
# wds-mode rootap 
# wds-ssid ${wds_ssid}
# wds-security-policy wpa-personal 
# remote-mac ap2mac
################################################################################
printStep(testname,'Step 4',\
                    'Config network 2 as wds and open mode',\
                    'Apply ap profile 1')
res1=res2=1
#operate
# AC上配置network2为wds，apmode为rootap，并下发profile 1
Ac_wds_config(switch1,2,
                ssid=wds_ssid,
                remotemac=ap2vapmac,
                securitymode='wpa-personal',
                psk_key=wds_psk_key)  
res1=WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
res2 = Check_ap_wdsconfig(ap1,Ap1cmdtype,wds1num,
                        check=[('radio',wlan),
                            ('wds-status','up'),
                            ('wds-mode','rootap'),
                            ('wds-ssid',wds_ssid),
                            ('wds-security-policy','wpa-personal'),
                            ('remote-mac',ap2mac_type1)],
                            IC=True)
#result
printCheckStep(testname, 'Step 4',res1,res2)
################################################################################
#Step 5
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 5',\
          'Recover initial config for switches.')

#operate
# 清除network2配置
ClearNetworkConfig(switch1,2)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#end
printTimer(testname, 'End')