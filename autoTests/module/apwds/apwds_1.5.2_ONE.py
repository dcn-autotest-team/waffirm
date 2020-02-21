#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apwds_1.5.2.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 1.5.2	rootap在5G，satelliteap在2.4G，不能建立wds
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.25
#*******************************************************************************

#Package

#Global Definition
ap1mac_type1_5G =incrmac(ap1mac_type1,16).lower()
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase apwds_1.5.2'
avoiderror(testname)
printTimer(testname,'Start','WDS can not be estalished when rootap use radio 5G and satelliteap use radio 2.4G')
###############################################################################
#Step 1
#操作
# 在AC1上关闭AP1的2.4G radio
# AC上在network1 配置wds并下发给ap1
# network 1   
# wds-mode rootap    
# security mode none    
# wds-remote-vap ap2mac
# ssid ${wds_ssid}
# AP2上进行open模式的WDS配置
# set wds wds0 wds-mode satelliteap
# set wds wds0 wds-ssid ${wds_ssid}    
# set wds wds0 remote-mac ap1mac_5G
# set wds wds0 wds-security-policy plain-text    
# set wds wds0 wds-status up
#预期
# 配置成功
################################################################################
printStep(testname,'Step 1','AP2 config wds0 as open mode',\
                    'Config wds in network 1 on AC1',\
                    'No enable profile 1 radio 1',\
                    'Apply ap profile 1')
res1=1
#operate
# 在AC1上关闭AP1的5G radio
EnterApProMode(switch1,1)
SetCmd(switch1,'radio',radio1num)
SetCmd(switch1,'no enable')
# AC上配置network1为wds，apmode为rootap，并下发profile 1
Ac_wds_config(switch1,1,
                ssid=wds_ssid,
                remotemac=ap2vapmac)
res1=WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# AP2上配置wds16,mode为satelliteap,remote-mac为ap1mac_5G，
Ap_openwds_config(ap2,Ap2cmdtype,
                    'wds0',
                    ssid=wds_ssid,
                    remotemac=ap1mac_type1_5G)

#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#操作
#等待30秒
#预期
#Ap2无法ping通Ap1，WDS建立无法建立
################################################################################
printStep(testname,'Step 2',\
                    'Wait 30 seconds',
                    'WDS link is not estalished')
res1=res2=1
#operate
CheckPing(ap2,Ap1_ipv4,mode='linux')
IdleAfter(30)
res1 = CheckSutCmd(ap1,'get wds wds16',\
                    check=[('wds-link','unlinked')],retry=1,waitflag=False) 
res2 = CheckSutCmd(ap2,'get wds wds0',\
                    check=[('wds-link','unlinked')],retry=1,waitflag=False)                  
#result
printCheckStep(testname, 'Step 2',res1,res2)

################################################################################
#Step 3
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 3',\
          'Recover initial config for switches.')

#operate
EnterApProMode(switch1,1)
SetCmd(switch1,'radio '+radio1num)
SetCmd(switch1,'enable')
SetCmd(switch1,'vap 1')
SetCmd(switch1,'enable')
SetCmd(switch1,'vap 2')
SetCmd(switch1,'enable')
# 恢复network1配置
ClearNetworkConfig(switch1,1)
EnterNetworkMode(switch1,1)
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan ' + Vlan4091)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# 恢复AP2初始化配置
RebootAp(connectTime=1,setdefaut=True,AP=ap2,apcmdtype=Ap2cmdtype)
Initial_ap2()
#end
printTimer(testname, 'End')