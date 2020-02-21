#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.1.1.4.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features:
# 2.1.1.4	在AC上能够为AP更新Profile
# 测试目的： 在AC上面能够为AP更新profile。
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.3.28
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'apconfiguration_2.1.1.4'
avoiderror(testname)
printTimer(testname,'Start','AC can update ap profile')

###############################################################################
#Step 1
#操作
# 修改network 1的ssid为 profiletest
# 下发profile 1和profile 2的配置
# 预期
# 配置下发成功，AP1和AP2 ath0的ssid修改为 profiletest
################################################################################
printStep(testname,'Step 1',
          'change network 1 ssid',
          'apply ap profile 1 and 2',
          'ap1 and ap2 ath0 ssid change to new ssid')
res1=res2=1
#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'ssid profiletest')
res1 = WirelessApplyProfileWithCheck(switch1,['1','2'],[ap1mac,ap2mac])
data1 = SetCmd(ap1,'iwconfig ath0')
res2 = CheckLine(data1,'ESSID:"profiletest"',IC=True)
data2 = SetCmd(ap2,'iwconfig ath0')
res3 = CheckLine(data2,'ESSID:"profiletest"',IC=True)
#result
printCheckStep(testname, 'Step 1',res1,res2,res3)

###############################################################################
#Step 2
#恢复初始配置
################################################################################
printStep(testname,'Step 2',
          'Recover initial config for switches.')
EnterNetworkMode(switch1,1)
SetCmd(switch1,'ssid', Network_name1)
res1 = WirelessApplyProfileWithCheck(switch1,['1','2'],[ap1mac,ap2mac])          
#end
printTimer(testname, 'End')