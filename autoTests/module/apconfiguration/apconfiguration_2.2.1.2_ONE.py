#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.1.2.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features:
# 2.2.1.2	手动重启AP不影响其他AP
# 测试目的：管理AC上可以wireless ap reset <ap1_mac>重启指定ap1，其它ap不会重启。
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.3.29
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'apconfiguration_2.2.1.2'
avoiderror(testname)
printTimer(testname,'Start','ap2 should not be influenced by that ac1 reset ap1')

###############################################################################
#Step 1
#操作
# 在AC1上重启AP1
# 预期
# AP1重启成功，AP2不受影响
################################################################################
printStep(testname,'Step 1',
          'ac1 reset ap2',
          'ap1 reboot successfully',
          'ap2 should not be influenced by ap1 rebooting')
res1=res2=1
#operate
StartDebug(ap1)
StartDebug(ap2)
# AC1重启AP1
EnterEnableMode(switch1)
SetCmd(switch1, 'wireless ap reset', ap1mac, promotePatten='Y/N',promoteTimeout=10)
SetCmd(switch1,'y')
IdleAfter(ap_reset_time)
# 检查AP1是否重启
data1 = StopDebug(ap1)
resa = CheckLine(data1,'Starting kernel',IC=True)
resb = CheckLine(data1,'login:',IC=True)
if resa==0 or resb==0:
    res1 = 0
ApLogin(ap1,retry=20)
# 检查AP2没有重启
data2 = StopDebug(ap2)
resc = CheckLine(data2,'Starting kernel',IC=True)
resd = CheckLine(data2,'login:',IC=True)  
if resc != 0 and resd != 0:
    res2 = 0  
# 检查AP1，AP2是否被AC1管理
res3=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                 retry=20,interval=10,waitflag=False,IC=True)
if res2 != 0:
    ApLogin(ap2,retry=20)
#result
printCheckStep(testname, 'Step 1',res1,res2,res3)

#end
printTimer(testname, 'End')