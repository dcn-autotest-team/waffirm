#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apwds_1.2.5.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 1.2.5	统计信息上报-wds未建立
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

testname = 'TestCase apwds_1.2.5'
avoiderror(testname)
printTimer(testname,'Start','Ap report to AC when wds is not linked')

###############################################################################
#Step 1
#操作
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
#AC1上开启debug wireless wds packet-receive
#预期
#AC1 上可以看到打印
# Received WDS AP Report Message from AP:${WIFI_AFFIRM_AP1_MAC}, radio:1, vap:1, wdsMode:1.*?remoteVap:00-00-00-00-00-00, connectedState:0
################################################################################

printStep(testname,'Step 2',\
                    'debug wireless wds packet-receive on AC1',\
                    'there is the info from ap1 that wds link is not connected')
res1=1
#operate
StartDebug(switch1)      
EnterEnableMode(switch1)
# SetCmd(switch1,'debug wireless wds packet-receive',promotePatten='Received WDS AP Report Message from AP:'+ap1mac+', radio:'+radionum+'.*?00-00-00-00-00-00.*?connectedState:0',promoteTimeout=30)
SetCmd(switch1,'debug wireless wds packet-receive',promotePatten='Received WDS AP Report Message from AP:'+ap1mac+', radio:'+radionum+'.*?connectedState:0',promoteTimeout=30)
data = StopDebug(switch1)
res1 = CheckLine(data,'Received WDS AP Report Message from AP:'+ap1mac+', radio:'+radionum+'.*?vap:1,.*?connectedState:0',IC=True) 
SetCmd(switch1,'no debug all')          
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
# 清除network2配置
ClearNetworkConfig(switch1,2)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#end
printTimer(testname, 'End')