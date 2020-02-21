#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apwds_1.3.2.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 1.3.2	Open方式下建立wds连接,使用wds0且数据vlan相同
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

testname = 'TestCase apwds_1.3.2'
avoiderror(testname)
printTimer(testname,'Start','Two ap both use vap0 to establish wds link and data traffic vlan is the same')
###############################################################################
#Step 1
#操作
# AP1上配置
# network 2   
# ssid test2
# vlan 4091
# network 3
# ssid test2
# vlan 4091
#预期
# 配置成功
################################################################################
printStep(testname,'Step 1','Config network 2 and network 3')
#operate
EnterNetworkMode(switch1,2)
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan ' + Vlan4091)
EnterNetworkMode(switch1,3)
SetCmd(switch1,'ssid ' + Network_name2)
SetCmd(switch1,'vlan ' + Vlan4091)
#result
printCheckStep(testname, 'Step 1',0)
###############################################################################
#Step 2
#操作
# AP2上进行open模式的WDS配置
# set wds wds0 wds-mode satelliteap
# set wds wds0 wds-ssid ${wds_ssid}    
# set wds wds0 remote-mac ap1mac    
# set wds wds0 wds-security-policy plain-text    
# set wds wds0 wds-status up
# AC上在network1 配置wds并下发给ap1
# network 1   
# wds-mode rootap    
# security mode none    
# wds-remote-vap ap2mac 
# ssid ${wds_ssid}
#预期
# 配置成功
################################################################################
printStep(testname,'Step 2','AP2 config wds0 as open mode',\
                    'Config wds in network 1 on AC1',\
                    'Apply ap profile 1')
res1=1
#operate
# AP2上配置wds0,mode为satelliteap
Ap_openwds_config(ap2,Ap2cmdtype,
                    wds0num,
                    ssid=wds_ssid,
                    remotemac=ap1mac_type1)
# AC上配置network1为wds，apmode为rootap，并下发profile 1
Ac_wds_config(switch1,1,
                ssid=wds_ssid,
                remotemac=ap2vapmac)
res1=WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#result
printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#检查AC1是否成功管理AP2,WDS连接是否建立
#预期
#AC1 上show wireless ap status可以看到AP2被成功管理
# AC1上show wireless wds link status可以看到AP1和AP2建立起wds连接
################################################################################

printStep(testname,'Step 3',\
                    'Check WDS is linked and AC1 managed ap2 successfully')
res1=res2=1
#operate
res1 = CheckSutCmd(switch1,'show wireless ap status', \
                    check=[(ap2mac,'Managed','Success')], \
                    retry=40,interval=5,waitflag=False,IC=True)
res2 = CheckSutCmd(switch1,'show wireless wds link status', \
                    check=[(ap1mac,radionum,'0',ap2mac,radionum,'0','Managed','Managed','Connected')], \
                    waittime=5,retry=5,interval=1,IC=True)                    
#result
printCheckStep(testname, 'Step 3',res1,res2)

################################################################################
#Step 4
#操作
#客户端STA1关联AP1
# STA2关联AP2
#预期
#关联成功。客户端获取192.168.91.X网段的IP地址。
# sta2可以ping通sta1
################################################################################
printStep(testname,'Step 4',\
                    'STA1 connect to AP1',\
                    'STA2 connect to AP2',\
                    'STA2 ping STA1 successfully')
res1=res2=res3=1
# operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Dhcp_pool1,bssid=ap1mac_type1_network2)
sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,checkDhcpAddress=Dhcp_pool1,bssid=ap2mac_type1_network3)
res3=CheckPing(sta2,sta1_ipv4,mode='linux')
#result
printCheckStep(testname, 'Step 4',res1,res2,res3)
################################################################################
#Step 5
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 5',\
          'Recover initial config for switches.')

#operate
# 恢复network1,2,3配置
ClearNetworkConfig(switch1,1)
ClearNetworkConfig(switch1,2)
ClearNetworkConfig(switch1,3)
EnterNetworkMode(switch1,1)
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan ' + Vlan4091)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# 恢复AP2初始化配置
RebootAp(connectTime=1,setdefaut=True,AP=ap2,apcmdtype=Ap2cmdtype)
Initial_ap2()
#end
printTimer(testname, 'End')