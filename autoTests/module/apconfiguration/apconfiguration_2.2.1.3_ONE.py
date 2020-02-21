#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.1.3.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features:
# 2.2.1.3	AC上重启所有自己管理AP
# 测试目的：管理AC上可以wireless ap reset重启所有自己管理ap，ap重启后重新上线，被AC管理。
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

testname = 'apconfiguration_2.2.1.3'
avoiderror(testname)
printTimer(testname,'Start','A ac can reset all of the aps that is managed itself')

###############################################################################
#Step 1
#操作
# 在AC1上重启所有AP
# 预期
# AP1，AP2重启成功，并被AC1成功管理
################################################################################
printStep(testname,'Step 1',
          'ac1 reset all aps that is managed by itself',
          'ap1,ap2 reboot successfully',
          'ac1 managed ap1,ap2 successfully')
res1=res2=1
#operate
StartDebug(ap1)
StartDebug(ap2)
# AC1重启所有AP
EnterEnableMode(switch1)
SetCmd(switch1, 'wireless ap reset', promotePatten='Y/N',promoteTimeout=10)
SetCmd(switch1,'y')
IdleAfter(ap_reset_time)
# 检查AP1是否重启
data1 = StopDebug(ap1)
resa = CheckLine(data1,'Starting kernel',IC=True)
resb = CheckLine(data1,'login:',IC=True)
if resa==0 or resb==0:
    res1 = 0
ApLogin(ap1,retry=20)
# 检查AP2是否重启
data2 = StopDebug(ap2)
resc = CheckLine(data2,'Starting kernel',IC=True)
resd = CheckLine(data2,'login:',IC=True)  
if resc==0 or resd==0:
    res2 = 0  
ApLogin(ap2,retry=20)
# 检查AP1，AP2是否被AC1管理
res3=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                 retry=20,interval=10,waitflag=False,IC=True)

#result
printCheckStep(testname, 'Step 1',res1,res2,res3)

#end
printTimer(testname, 'End')