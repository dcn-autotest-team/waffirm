#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.1.1.1.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features:
# 2.1.1.1	手动重启AP
# 测试目的：在管理AC上可以手动重启AP，AP重启后重新上线，被AC管理
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

testname = 'apconfiguration_2.1.1.1'
avoiderror(testname)
printTimer(testname,'Start','Reboot ap from ac')

###############################################################################
#Step 1
#操作
# 在AC1上重启AP1
# 预期
# AP1重启成功，并且被AC1成功管理
################################################################################
printStep(testname,'Step 1',
          'reboot ap1 from ac1',
          'ap1 reboot successfully',
          'ac1 managed ap1 successfully')
res1=res2=1
#operate
StartDebug(ap1)
# AC1重启AP1
EnterEnableMode(switch1)
SetCmd(switch1, 'wireless ap reset', ap1mac, promotePatten='Y/N',promoteTimeout=10)
SetCmd(switch1,'y')
IdleAfter(ap_reset_time)
# 检查AP1是否重启
data = StopDebug(ap1)
resa = CheckLine(data,'Starting kernel',IC=True)
resb = CheckLine(data,'login:',IC=True)
if resa==0 or resb==0:
    res1 = 0
ApLogin(ap1,retry=20)
# 检查AP1是否被AC1管理
res2=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,Ap1_ipv4,'1','Managed','Success')],
                 retry=20,interval=10,waitflag=False,IC=True)
#result
printCheckStep(testname, 'Step 1',res1,res2)

#end
printTimer(testname, 'End')