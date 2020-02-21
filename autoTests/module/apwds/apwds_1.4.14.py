#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apwds_1.4.14.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 1.4.14	wpa-personal方式下建立wds,重启各个设备后仍能建立wds
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.25
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase apwds_1.4.14'
avoiderror(testname)
printTimer(testname,'Start','psk mode wds is still linked after reboot AC and AP')
###############################################################################
#Step 1
#操作
# AP2上进行psk模式的WDS配置
# set wds wds2 wds-mode satelliteap    
# set wds wds2 wds-status up
# set wds wds2 wds-ssid ${wds_ssid}    
# set wds wds2 remote-mac ap1mac
# set wds wds2 wds-security-policy wpa-personal    
# set wds wds2 wds-wpa-personal-key ${psk_key}
# AC上在network2 配置wds并下发给ap1
# network 1   
# wds-mode rootap    
# security mode wpa-personal    
# wpa key  ${psk_key}    
# wds-remote-vap  ap2mac_network3
# ssid ${wds_ssid}
#预期
# 配置成功
################################################################################
printStep(testname,'Step 1','AP2 config wds2 as wpa-personal mode',\
                    'Config wds in network 1 on AC1',\
                    'Apply ap profile 1')
res1=1
#operate
# AP2上配置wds2,mode为satelliteap
Ap_pskwds_config(ap2,Ap2cmdtype,
                wds2num,
                ssid=wds_ssid,
                remotemac=ap1mac_type1,
                psk_key=wds_psk_key)
# AC上配置network1为wds，apmode为rootap，并下发profile 1
Ac_wds_config(switch1,1,
                ssid=wds_ssid,
                remotemac=ap2vapmac_network3,
                securitymode='wpa-personal',
                psk_key=wds_psk_key)            
res1=WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#操作
#检查AC1是否成功管理AP2,WDS连接是否建立
#预期
#AC1 上show wireless ap status可以看到AP2被成功管理
# AC1上show wireless wds link status可以看到AP1和AP2建立起wds连接
################################################################################

printStep(testname,'Step 2',\
                    'Check WDS is linked and AC1 managed ap2 successfully')
res1=res2=1
#operate
res1 = CheckSutCmd(switch1,'show wireless ap status', \
                    check=[(ap2mac,'Managed','Success')], \
                    retry=40,interval=5,waitflag=False,IC=True)
res2 = CheckSutCmd(switch1,'show wireless wds link status', \
                    check=[(ap1mac,radionum,'0',ap2mac,radionum,'2','Managed','Managed','Connected')], \
                    waittime=5,retry=5,interval=1,IC=True)                    
#result
printCheckStep(testname, 'Step 2',res1,res2)
################################################################################
#Step 3
#操作
#保存配置重启AC1
#预期
# AC1重启后WDS连接恢复
################################################################################
printStep(testname,'Step 3','Reload AC1',\
                            'After AC1 reload,WDS link recover')
res1=res2=1
#operate
# 保存配置并重启ac1
EnterEnableMode(switch1)
SetCmd(switch1,'write',timeout=1)
SetCmd(switch1,'y',timeout=2)  
ReloadMultiSwitch([switch1]) 
# AC1重启后wDS连接恢复
EnterEnableMode(switch1)
res1 = CheckSutCmd(switch1,'show wireless ap status', \
                    check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')], \
                    retry=40,interval=5,waitflag=False,IC=True)
res2 = CheckSutCmd(switch1,'show wireless wds link status', \
                    check=[(ap1mac,radionum,'0',ap2mac,radionum,'2','Managed','Managed','Connected')], \
                    waittime=5,retry=5,interval=1,IC=True)                      
#result
printCheckStep(testname, 'Step 3',res1,res2)
################################################################################
#Step 4
#操作
#保存配置重启AP1
#预期
# AP1重启后WDS连接恢复
################################################################################
printStep(testname,'Step 4','Reboot AP1',\
                            'After AP1 reboot,WDS link recover')
res1=res2=1
#operate
# 保存配置并重启AP1
SetCmd(ap1,'\n')
ApSetcmd(ap1,Ap1cmdtype,'saverunning')
RebootAp(AP=ap1)
# AP1重启后wDS连接恢复
res1 = CheckSutCmd(switch1,'show wireless ap status', \
                    check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')], \
                    retry=40,interval=5,waitflag=False,IC=True)
res2 = CheckSutCmd(switch1,'show wireless wds link status', \
                    check=[(ap1mac,radionum,'0',ap2mac,radionum,'2','Managed','Managed','Connected')], \
                    waittime=5,retry=5,interval=1,IC=True)                      
#result
printCheckStep(testname, 'Step 4',res1,res2)
################################################################################
#Step 5
#操作
#保存配置重启AP2
#预期
# AP2重启后WDS连接恢复
################################################################################
printStep(testname,'Step 5','Reboot AP2',\
                            'After AP2 reboot,WDS link recover')
res1=res2=1
#operate
# 保存配置并重启AP2
SetCmd(ap2,'\n')
ApSetcmd(ap2,Ap2cmdtype,'saverunning')
RebootAp(AP=ap2)
# AP1重启后wDS连接恢复
res1 = CheckSutCmd(switch1,'show wireless ap status', \
                    check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')], \
                    retry=40,interval=5,waitflag=False,IC=True)
res2 = CheckSutCmd(switch1,'show wireless wds link status', \
                    check=[(ap1mac,radionum,'0',ap2mac,radionum,'2','Managed','Managed','Connected')], \
                    waittime=5,retry=5,interval=1,IC=True)                       
#result
printCheckStep(testname, 'Step 5',res1,res2)
################################################################################
#Step 6
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 6',\
          'Recover initial config for switches.')

#operate
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