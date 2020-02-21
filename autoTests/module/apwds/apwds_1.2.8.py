#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apwds_1.2.8.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 1.2.8	WDS AP客户端接入测试-satelliteap
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.24
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase apwds_1.2.8'
avoiderror(testname)
printTimer(testname,'Start','Test sta connect to satelliteap')

###############################################################################
#Step 1
#操作
# AC上将network100绑定到profile 1的vap1中
# 在network100 配置wds并下发给ap1
# network 100   
# wds-mode rootap    
# security mode none    
# wds-remote-vap ap2mac_network3    
# ssid ${wds_ssid}
# AP2上进行open模式的WDS配置
# set wds wds2 wds-mode satelliteap
# set wds wds2 wds-ssid ${wds_ssid}    
# set wds wds2 remote-mac ap1mac_network2    
# set wds wds2 wds-security-policy plain-text    
# set wds wds2 wds-status up
#预期
# 配置成功
################################################################################
printStep(testname,'Step 1','AP2 config wds as open mode',\
                    'Config wds in network 100 on AC1',\
                    'Apply ap profile 1')
res1=1
#operate
# AC上配置network100为wds，apmode为rootap，并下发profile 1
EnterApProMode(switch1,1)
SetCmd(switch1,'radio',radionum)
SetCmd(switch1,'vap 1')
SetCmd(switch1,'enable')
SetCmd(switch1,'network 100')
Ac_wds_config(switch1,100,
                ssid=wds_ssid,
                remotemac=ap2vapmac_network3)
res1=WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# AP2上配置wds2,mode为satelliteap
Ap_openwds_config(ap2,Ap2cmdtype,
                    wds2num,
                    ssid=wds_ssid,
                    remotemac=ap1mac_type1_network2)

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
#客户端STA1关联AP2的ath0
#预期
#关联成功。客户端获取192.168.91.X网段的IP地址。
# STA1可以ping通ac1
################################################################################
printStep(testname,'Step 3',\
                    'STA1 connect to AP2',\
                    'STA1 ping AC1 successfully')
res1=res2=res3=1
# operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap2mac_type1)
if res1 == 0:
    res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
    res3=CheckPing(sta1,If_vlan10_s1_ipv4,mode='linux')
#result
printCheckStep(testname, 'Step 3',res1,res2,res3)
################################################################################
#Step 4
#操作
#在AP2上将wds1的wds-mode配置为rootap
#预期
#get wds wds1可以看到
# wds-mode   rootap
################################################################################
printStep(testname,'Step 4',\
                    'Set wds1 wds-mode rootap on AP2')
res1=1
# operate
Ap_set_wds(ap2,Ap2cmdtype,wds1num,'wds-mode','rootap')
res1 = Check_ap_wdsconfig(ap2,Ap2cmdtype,wds1num,
                        check=[('wds-mode','rootap')],IC=True)
#result
printCheckStep(testname, 'Step 4',res1)
################################################################################
#Step 5
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 5',\
          'Recover initial config for switches.')

#operate
EnterApProMode(switch1,1)
SetCmd(switch1,'radio',radionum)
SetCmd(switch1,'vap 1')
SetCmd(switch1,'enable')
SetCmd(switch1,'network 2')
# 清除network100配置
ClearNetworkConfig(switch1,100)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# 恢复AP2初始化配置
RebootAp(connectTime=1,setdefaut=True,AP=ap2,apcmdtype=Ap2cmdtype)
Initial_ap2()
#end
printTimer(testname, 'End')