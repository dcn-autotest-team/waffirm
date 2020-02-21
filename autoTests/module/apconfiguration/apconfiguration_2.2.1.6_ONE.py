#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.1.6_ONE.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features:(合并方案2.2.1.6和2.2.1.7)
# 2.2.1.6	Controller上可以重启自己管理的AP2
# 测试目的： Controller上可以wireless ap reset <ap2_mac>重启指定自己管理的ap2，ap2重启后重新上线，被AC管理。
# 2.2.1.7	Controller重启指定ap1其他不重启
# 测试目的： Controller上可以wireless ap reset <ap1_mac>重启指定ap1，其它ap不会重启。
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.3.29
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'apconfiguration_2.2.1.6'
avoiderror(testname)
printTimer(testname,'Start','ac(controller) can reset the aps that are managed by itself,and other aps should not be influenced')
###############################################################################
#Step 1
#操作
# 在AC1上配置discovery ip-list StaticIpv4_ac2
# 预期
# AC1和AC2建立集群关系
################################################################################
printStep(testname,'Step 1',
          'config discovery ip-list StaticIpv4_ac2 on ac1',
          'ac1 and ac2 are in a cluster')
res1=res2=1
#operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'cluster-priority 10')
SetCmd(switch1,'discovery ip-list',StaticIpv4_ac2)
IdleAfter(30)

# 检查AC1和AC2建立集群关系
res1=CheckSutCmd(switch1,'show wireless peer-switch', 
                 check=[(StaticIpv4_ac2)],
                 retry=20,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname, 'Step 1',res1)  
###############################################################################
#Step 2
#操作
# 在AC1上重启AP2
# 预期
# AP2重启成功，并且被AC1成功管理
# AP1不受影响
################################################################################
printStep(testname,'Step 2',
          'ac1 reset ap2',
          'ap2 reboot successfully',
          'ap1 should not be influenced by ap2 rebooting')
res1=res2=1
#operate
StartDebug(ap1)
StartDebug(ap2)
# AC1重启AP2
EnterEnableMode(switch1)
SetCmd(switch1, 'wireless ap reset', ap2mac, promotePatten='Y/N',promoteTimeout=10)
SetCmd(switch1,'y')
IdleAfter(ap_reset_time)
# 检查AP2是否重启
data1 = StopDebug(ap2)
resa = CheckLine(data1,'Starting kernel',IC=True)
resb = CheckLine(data1,'login:',IC=True)
if resa==0 or resb==0:
    res1 = 0
ApLogin(ap2,retry=20)
# 检查AP1没有重启
data2 = StopDebug(ap1)
resc = CheckLine(data2,'Starting kernel',IC=True)
resd = CheckLine(data2,'login:',IC=True)  
if resc != 0 and resd != 0:
    res2 = 0  
# 检查AP1，AP2是否被AC1管理
res3=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                 retry=20,interval=10,waitflag=False,IC=True)
if res2 != 0:
    ApLogin(ap1,retry=20)
#result
printCheckStep(testname, 'Step 2',res1,res2)
################################################################################
# Step 3
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 3',
          'Recover initial config')
# operate
# 恢复AC1配置
EnterWirelessMode(switch1)
SetCmd(switch1, 'no cluster-priority')
SetCmd(switch1, 'no discovery ip-list',StaticIpv4_ac2)
SetCmd(switch1, 'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
IdleAfter(30)

CheckSutCmd(switch1,'show wireless peer-switch', 
            check=[('No peer wireless switch exists')],
            retry=10,interval=5,waitflag=False,IC=True)
#end
printTimer(testname, 'End')