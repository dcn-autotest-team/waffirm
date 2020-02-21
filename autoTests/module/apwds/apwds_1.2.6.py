#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apwds_1.2.6.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 1.2.6	统计信息上报-wds建立
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

testname = 'TestCase apwds_1.2.6'
avoiderror(testname)
printTimer(testname,'Start','Ap report to AC when wds is linked')

###############################################################################
#Step 1
#操作
# AP2上进行open模式的WDS配置
# set wds wds2 wds-mode satelliteap
# set wds wds2 wds-ssid ${wds_ssid}    
# set wds wds2 remote-mac ap1mac_network2    
# set wds wds2 wds-security-policy plain-text    
# set wds wds2 wds-status up
# AC上在network2 配置wds并下发给ap1
# network 2   
# wds-mode rootap    
# security mode none    
# wds-remote-vap ap2mac_network3    
# ssid ${wds_ssid}
#预期
# 配置成功
################################################################################
printStep(testname,'Step 1','AP2 config wds as open mode',\
                    'Config wds in network 2 on AC1',\
                    'Apply ap profile 1')
res1=1
#operate
# AP2上配置wds2,mode为satelliteap
Ap_openwds_config(ap2,Ap2cmdtype,
                    wds2num,
                    ssid=wds_ssid,
                    remotemac=ap1mac_type1_network2)
# AC上配置network2为wds，apmode为rootap，并下发profile 1
Ac_wds_config(switch1,2,
                ssid=wds_ssid,
                remotemac=ap2vapmac_network3)
res1=WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#result
printCheckStep(testname, 'Step 1',res1)
################################################################################
#Step 2
#操作
#检查AC1是否成功管理AP2
#预期
#AC1 上show wireless ap status可以看到AP2被成功管理
# AC1上show wireless wds link status可以看到AP1和AP2建立起wds连接
################################################################################
printStep(testname,'Step 2',\
                    'Check AC1 managed ap2 successfully')
res1=res2=1
#operate
res1 = CheckSutCmd(switch1,'show wireless ap status', \
                    check=[(ap2mac,'Managed','Success')], \
                    retry=40,interval=5,waitflag=False,IC=True)
res2 = CheckSutCmd(switch1,'show wireless wds link status', \
                    check=[(ap1mac,radionum,'1',ap2mac,radionum,'2','Managed','Managed','Connected')], \
                    waittime=5,retry=5,interval=1,IC=True)                    
#result
printCheckStep(testname, 'Step 2',res1,res2)
################################################################################
#Step 3
#操作
#AC1上开启debug wireless wds packet-receive
#预期
#AC1 上可以看到打印
# Received WDS AP Report Message from AP:${WIFI_AFFIRM_AP1_MAC}, radio:1, vap:1, wdsMode:1\\(0:disable; 1:rootAP; 2:satelliteAP\\), remoteVap:${ap2_remote_mac}, connectedState:1
# Received WDS AP Report Message from AP:${WIFI_AFFIRM_AP2_MAC}, radio:1, vap:2, wdsMode:2.*?remoteVap:${ap_remote_mac}, connectedState:1
################################################################################
printStep(testname,'Step 3',\
                    'debug wireless wds packet-receive on AC1',\
                    'there is the info from ap1 and ap2 that wds link is connected')
res1=res2=1
#operate
StartDebug(switch1)      
EnterEnableMode(switch1)
SetCmd(switch1,'debug wireless wds packet-receive')
IdleAfter(15)
data = StopDebug(switch1)      
res1 = CheckLine(data,'Received WDS AP Report Message from AP:'+ap1mac+', radio:'+radionum+'.*?wdsMode:1.*?remoteVap:'+ap2vapmac_network3+'.*?connectedState:1',IC=True)   
res2 = CheckLine(data,'Received WDS AP Report Message from AP:'+ap2mac+', radio:'+radionum+'.*?wdsMode:2.*?remoteVap:'+ap1vapmac_network2+'.*?connectedState:1',IC=True)      
SetCmd(switch1,'no debug all')  
#result
printCheckStep(testname, 'Step 3',res1,res2)
################################################################################
#Step 4
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 3',\
          'Recover initial config for switches.')

#operate
# 清除network2配置
ClearNetworkConfig(switch1,2)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# 恢复AP2初始化配置
RebootAp(connectTime=1,setdefaut=True,AP=ap2,apcmdtype=Ap2cmdtype)
Initial_ap2()
#end
printTimer(testname, 'End')