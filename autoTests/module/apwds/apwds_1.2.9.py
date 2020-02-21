#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apwds_1.2.9.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 1.2.9	配置下发测试-rootap
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.24
#*******************************************************************************

#Package

#Global Definition
otherwlan = 'wlan1' if wlan=='wlan0' else 'wlan0'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase apwds_1.2.9'
avoiderror(testname)
printTimer(testname,'Start','Test apply ap profile to rootap')

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
#AC1上配置
# network 1
# ssid xxxxx
#预期
#下发配置到AP1
# 配置下发过程中2.4G radio状态为up，5G ridao状态为down
################################################################################
printStep(testname,'Step 3',\
                    'Config network 1 ssid xxxxx',\
                    'Apply ap profile 1')
res1=res2=1
# operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'ssid xxxxx')
EnterEnableMode(switch1)
SetCmd(switch1, 'wireless ap profile apply 1', promotePatten='Y/N',promoteTimeout=10)
SetCmd(switch1,'y')
res1 = CheckSutCmd(ap1,'get radio '+otherwlan,\
                    check=[('\nstatus','down')],retry=50,interval=1,waitflag=False)
res2 = CheckSutCmd(ap1,'get radio '+wlan,\
                    check=[('\nstatus','up')],retry=1,waitflag=False)
CheckSutCmd(switch1,'show wireless ap status', \
            check=[(ap1mac,'Managed','Success')], \
            waittime=5,retry=20,interval=5,IC=True)                    
#result
printCheckStep(testname, 'Step 3',res1,res2)
################################################################################
#Step 4
#操作
#AC上检查WDS连接
#预期
# wds连接没有断开
################################################################################
printStep(testname,'Step 4',\
                    'Check wds is still linked')
res1=1
# operate
res1 = CheckSutCmd(switch1,'show wireless wds link status', \
                    check=[(ap1mac,radionum,'1',ap2mac,radionum,'2','Managed','Managed','Connected')], \
                    retry=5,waitflag=False,IC=True)     
#result
printCheckStep(testname, 'Step 4',res1)
################################################################################
#Step 5
#操作
#AP1上检查vap 0的ESSID 为xxxxx
#预期
#ESSID显示为xxxxx
################################################################################
printStep(testname,'Step 5',\
                    'Check AP1 vap0 Essid is xxxxx')
res1=1
# operate
data = SetCmd(ap1,'iwconfig ath0')
res1 = CheckLine(data,'ESSID:"xxxxx"')
#result
printCheckStep(testname, 'Step 5',res1)
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
#恢复Network1
EnterNetworkMode(switch1,1)
SetCmd(switch1,'ssid ' + Network_name1)
# 清除network100配置
ClearNetworkConfig(switch1,100)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# 恢复AP2初始化配置
RebootAp(connectTime=1,setdefaut=True,AP=ap2,apcmdtype=Ap2cmdtype)
Initial_ap2()
#end
printTimer(testname, 'End')