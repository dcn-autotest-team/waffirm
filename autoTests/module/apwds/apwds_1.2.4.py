#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apwds_1.2.4.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 1.2.3	AP基本配置-wpa-personal认证方式
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

testname = 'TestCase apwds_1.2.4'
avoiderror(testname)
printTimer(testname,'Start','Check AP basic wds configuration in wpa-personal mode')

###############################################################################
#Step 1
#操作
# AP2上进行psk模式的WDS配置
# set wds wds2 wds-mode satelliteap    
# set wds wds2 wds-status up
# set wds wds2 wds-ssid ${wds_ssid}    
# set wds wds2 remote-mac ap1mac_network2
# set wds wds2 wds-security-policy wpa-personal    
# set wds wds2 wds-wpa-personal-key ${psk_key}
#预期
# AP2上get wds wds2
# 显示
# radio wlan0 
# wds-mode satelliteap 
# wds-ssid ${wds_ssid}
# wds-security-policy wpa-personal  
# remote-mac ap1mac
################################################################################
printStep(testname,'Step 1','AP2 config wds2 as wpa-personal mode')
res1=1
#operate
# AP2上配置wds2,mode为satelliteap
Ap_pskwds_config(ap2,Ap2cmdtype,
                wds2num,
                ssid=wds_ssid,
                remotemac=ap1mac_type1,
                psk_key=wds_psk_key)
res1 = Check_ap_wdsconfig(ap2,Ap2cmdtype,wds2num,
                        check=[('radio',wlan),
                            ('wds-status','up'),
                            ('wds-mode','satelliteap'),
                            ('wds-ssid',wds_ssid),
                            ('wds-security-policy','wpa-personal'),
                            ('remote-mac',ap1mac_type1)],
                            IC=True)
#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#操作
# AP2保存配置重启
#预期
#重启后配置没有丢失
################################################################################
printStep(testname,'Step 2',\
                    'AP2 save running and reload',\
                    'the configuration is not lost')
res1=1
#operate
ApSetcmd(ap2,Ap2cmdtype,'saverunning')
RebootAp(connectTime=1,AP=ap2,apcmdtype=Ap2cmdtype)
res1 = Check_ap_wdsconfig(ap2,Ap2cmdtype,wds2num,
                        check=[('radio',wlan),
                            ('wds-status','up'),
                            ('wds-mode','satelliteap'),
                            ('wds-ssid',wds_ssid),
                            ('wds-security-policy','wpa-personal'),
                            ('remote-mac',ap1mac_type1)],
                            IC=True) 
#result
printCheckStep(testname, 'Step 2',res1)
################################################################################
#Step 3
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 3',\
          'Recover initial config for switches.')

#operate
# 恢复AP2初始化配置
RebootAp(connectTime=1,setdefaut=True,AP=ap2,apcmdtype=Ap1cmdtype)
Initial_ap2()
#end
printTimer(testname, 'End')