#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apwds_1.1.1.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 1.1.1	open方式下2.4G/5G建立wds连接
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.8
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase apwds_1.1.1'
avoiderror(testname)
printTimer(testname,'Start','Establish WDS link in open mode and radio 2.4G')

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
#客户端STA1关联AP1的ath0
# STA2关联AP2的ath0
#预期
#关联成功。客户端获取192.168.91.X网段的IP地址。
# sta2可以ping通sta1
################################################################################
printStep(testname,'Step 3',\
                    'STA1 connect to AP1',\
                    'STA2 connect to AP2',\
                    'STA2 ping STA1 successfully')
res1=res2=res3=res4=res5=1
# operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
if res1 == 0:
    res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
res3 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap2mac_type1)
if res3 == 0:
    res4 = CheckWirelessClientOnline(switch1,sta2mac,'online')
res5=CheckPing(sta2,sta1_ipv4,mode='linux')
#result
printCheckStep(testname, 'Step 3',res1,res2,res3,res4,res5)
################################################################################
#Step 4
#操作
# AP2上配置
# set wds wds2 wds-status down
#预期
#等待1min后，AC上show wireless wds link status显示
# AP1和AP2的wds连接断开
################################################################################
printStep(testname,'Step 4',\
                    'set wds wds2 wds-status down on Ap2',\
                    'wds link between AP1 and AP2 break')
res1=1
#operate
Ap_set_wds(ap2,Ap2cmdtype,wds2num,'wds-status','down')
# SetCmd(ap2,'set wds wds2 wds-status down')
IdleAfter(10)
res1 = CheckSutCmd(switch1,'show wireless wds link status', \
                    check=[(ap1mac,ap2mac,'Managed','Failed','Not Connected')], \
                    retry=20,interval=5,waitflag=False,IC=True)
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
# 清除network2配置
ClearNetworkConfig(switch1,2)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# 恢复AP2初始化配置
RebootAp(connectTime=1,setdefaut=True,AP=ap2,apcmdtype=Ap2cmdtype)
Initial_ap2()
#end
printTimer(testname, 'End')