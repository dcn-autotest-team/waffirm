#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apwds_1.2.3.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 1.2.3	AP基本配置-open认证方式
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

testname = 'TestCase apwds_1.2.3'
avoiderror(testname)
printTimer(testname,'Start','Check AP basic wds configuration in open mode')

###############################################################################
#Step 1
#操作
# AP2配置set wds wds2 wds-mode satelliteap
#预期
# AP2上 get wds wds2
# 显示
# wds-mode    satelliteap
################################################################################
printStep(testname,'Step 1','set wds wds2 wds-mode satelliteap on AP2')
res1=1
#operate
# SetCmd(ap2,'set wds',wds2num,'wds-mode satelliteap')
Ap_set_wds(ap2,Ap2cmdtype,wds2num,'wds-mode','satelliteap')
# data = SetCmd(ap2,'get wds',wds2num)
# res1 = CheckLine(data,'wds-mode','satelliteap')
res1 = Check_ap_wdsconfig(ap2,Ap2cmdtype,wds2num,
                        check=[('wds-mode','satelliteap')],IC=True)
#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#操作
#AP2配置  set wds wds1 wds-mode satelliteap
#预期
#提示Failed:wlan0 already has one vap on satelliteap mode!
################################################################################
printStep(testname,'Step 2',\
                    'set wds wds1 wds-mode satelliteap on AP2 failed')
res1=1
#operate
# data = SetCmd(ap2,'set wds',wds1num,'wds-mode satelliteap')  
data = Ap_set_wds(ap2,Ap2cmdtype,wds1num,'wds-mode','satelliteap')    
res1 = CheckLine(data,'Failed:.*? already has one vap on satelliteap mode',IC=True)         
#result
printCheckStep(testname, 'Step 2',res1)
################################################################################
#Step 3
#操作
# AP2上配置
# set wds wds2 wds-mode satelliteap
# set wds wds2 wds-ssid ${wds_ssid}    
# set wds wds2 remote-mac   ap1mac    
# set wds wds2 wds-security-policy plain-text    
# set wds wds2 wds-status up
#预期
#AP2上get wds wds2
# 显示
# wds-status       up    
# wds-mode   satelliteap    
# wds-ssid    ${wds_ssid}    
# wds-security-policy   plain-text
# remote-mac   ap1mac
################################################################################
printStep(testname,'Step 3',\
                    'AP2 config wds2 as open mode')
res1=1
# operate
# AP2上配置wds2,mode为satelliteap
Ap_openwds_config(ap2,Ap2cmdtype,
                    wds2num,
                    ssid=wds_ssid,
                    remotemac=ap1mac_type1)
res1 = Check_ap_wdsconfig(ap2,Ap2cmdtype,wds2num,
                        check=[('wds-status','up'),
                            ('wds-mode','satelliteap'),
                            ('wds-ssid',wds_ssid),
                            ('wds-security-policy','plain-text'),
                            ('remote-mac',ap1mac_type1)],
                            IC=True)               
#result
printCheckStep(testname, 'Step 3',res1)
################################################################################
#Step 4
#操作
# AP2保存配置重启
#预期
#重启后配置没有丢失
################################################################################
printStep(testname,'Step 4',\
                    'AP2 save running and reload',\
                    'the configuration is not lost')
res1=1
#operate
ApSetcmd(ap2,Ap2cmdtype,'saverunning')
RebootAp(connectTime=1,AP=ap2,apcmdtype=Ap2cmdtype)
res1 = Check_ap_wdsconfig(ap2,Ap2cmdtype,wds2num,
                        check=[('wds-status','up'),
                            ('wds-mode','satelliteap'),
                            ('wds-ssid',wds_ssid),
                            ('wds-security-policy','plain-text'),
                            ('remote-mac',ap1mac_type1)],
                            IC=True)  
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
# 恢复AP2初始化配置
RebootAp(connectTime=1,setdefaut=True,AP=ap2,apcmdtype=Ap1cmdtype)
Initial_ap2()
#end
printTimer(testname, 'End')