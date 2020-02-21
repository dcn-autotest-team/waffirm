#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apwds_1.6.3.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 1.6.3	胖AP模式，psk方式下2.4G/5G建立wds连接
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.26
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase apwds_1.6.3'
avoiderror(testname)
printTimer(testname,'Start','Config ap as fat ap,establish WDS link in psk mode and radio 2.4G/5G')
###############################################################################
#Step 1
#操作
# 将s3p3 shutdown
# 配置AP1和AP2为胖AP
#预期
# 配置成功
################################################################################
printStep(testname,'Step 1','Shutdown s3p3',\
                            'Config ap1 and ap2 as fat ap')

#operate
# 将s3p3 shutdown
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'shutdown')
IdleAfter(3)
# 配置AP1和AP2为胖AP
# 修改AP的胖瘦模式使用命令switch-apmode fat/fit，命令下发后会自动将AP恢复出厂设置并重启（IP和网关配置不会恢复出厂）
# 命令set system apmode fat/fit不再使用
Set_apmode(ap1,Ap1cmdtype,'fat')
Set_apmode(ap2,Ap2cmdtype,'fat')
IdleAfter(50)
ApLogin(ap1,retry=30)
ApLogin(ap2,retry=30)
ApSetcmd(ap1,Ap1cmdtype,'getsystem','detail')
ApSetcmd(ap2,Ap2cmdtype,'getsystem','detail')
#result
printCheckStep(testname, 'Step 1',0)
###############################################################################
#Step 2
#操作
# AP1上进行psk模式的WDS配置,wds-mode为rootap  
# set wds wds0 wds-mode rootap   
# set wds wds0 wds-status up
# set wds wds0 wds-ssid ${wds_ssid}    
# set wds wds0 remote-mac ap2mac
# set wds wds0 wds-security-policy wpa-personal    
# set wds wds0 wds-wpa-personal-key ${psk_key}
# AP2上进行psk模式的WDS配置,wds-mode为satelliteap 
# set wds wds0 wds-mode satelliteap    
# set wds wds0 wds-status up
# set wds wds0 wds-ssid ${wds_ssid}    
# set wds wds0 remote-mac ap1mac
# set wds wds0 wds-security-policy wpa-personal    
# set wds wds0 wds-wpa-personal-key ${psk_key}
#预期
# 配置成功
################################################################################
printStep(testname,'Step 2','AP1 and AP2 config wds0 as psk mode')
res1=1
#operate
# AP1上配置wds0,mode为rootap
Ap_pskwds_config(ap1,Ap1cmdtype,
                wds0num,
                ssid=wds_ssid,
                remotemac=ap2mac_type1,
                psk_key=wds_psk_key,
                apmode='rootap')
# AP2上配置wds0,mode为satelliteap
Ap_pskwds_config(ap2,Ap2cmdtype,
                wds0num,
                ssid=wds_ssid,
                remotemac=ap1mac_type1,
                psk_key=wds_psk_key)
CheckPing(ap2,Ap1_ipv4,mode='linux')
#result
printCheckStep(testname, 'Step 2',0)

################################################################################
#Step 3
#操作
#检查WDS连接建立成功
#预期
# AP1，AP2上查看wds-link状态为linked
################################################################################

printStep(testname,'Step 3',\
                    'Check WDS is linked')
res1=res2=1
#operate
IdleAfter(10)
res1 = CheckSutCmd(ap1,'get wds '+wds0num,\
                    check=[('radio',wlan),('wds-link','\slinked')],retry=20,waitflag=False)
res2 = CheckSutCmd(ap2,'get wds '+wds0num,\
                    check=[('radio',wlan),('wds-link','\slinked')],retry=1,waitflag=False)   
                   
#result
printCheckStep(testname, 'Step 3',res1,res2)

################################################################################
#Step 4
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 4',\
          'Recover initial config for switches.')

#operate
# 将s3p3 no shutdown
EnterConfigMode(switch3)
SetCmd(switch3,'interface',s3p3)
SetCmd(switch3,'no shutdown')
IdleAfter(3)
# 恢复AP2初始化配置
RebootAp(connectTime=1,setdefaut=True,AP=ap1,apcmdtype=Ap1cmdtype)
Initial_ap1()
# 恢复AP2初始化配置
RebootAp(connectTime=1,setdefaut=True,AP=ap2,apcmdtype=Ap2cmdtype)
Initial_ap2()
#end
printTimer(testname, 'End')