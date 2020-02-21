#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.1.8.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features:
# 2.2.1.8	Controller上可以重启所有Ap，Peer上ap重新上线
# 测试目的：Controller上可以wireless ap reset重启所有ap，peer上ap重启后重新上线，被AC管理。
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

testname = 'apconfiguration_2.2.1.8'
avoiderror(testname)
printTimer(testname,'Start','ac(controller) can reset all of the aps that are managed by itself and peers')

###############################################################################
#Step 1
#操作
# 在AC1上配置discovery ip-list StaticIpv4_ac2
# 在AP2上配置管理AC的地址为AC2的IP
# set managed-ap switch-address-1 ac2_ip
# 重启AP2
# 预期
# AC1和AC2建立集群关系
# AP2被AC2成功管理
################################################################################
printStep(testname,'Step 1',
          'config discovery ip-list StaticIpv4_ac2 on ac1',
          'ap2 set managed-ap switch-address-1 ac2_ip',
          'reboot ap2',
          'ac1 and ac2 are in a cluster',
          'ac2 manages ap2 successfully')
res1=res2=1
#operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'cluster-priority 10')
SetCmd(switch1,'discovery ip-list',StaticIpv4_ac2)

# AP2上配置管理AC的地址为AC2的IP
ApSetcmd(ap2,Ap2cmdtype,'set_switch_address',StaticIpv4_ac2,addressnum='1')
ApSetcmd(ap2,Ap2cmdtype,'saverunning')
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap2, ap2mac, switch1, Ap2cmdtype)
IdleAfter(30)

# 检查AC1和AC2建立集群关系
res1=CheckSutCmd(switch1,'show wireless peer-switch', 
                 check=[(StaticIpv4_ac2)],
                 retry=20,interval=5,waitflag=False,IC=True)
# 检查AP2是否被AC2管理
res2=CheckSutCmd(switch2,'show wireless ap status', 
                 check=[(ap2mac,'Managed','Success')],
                 retry=20,interval=10,waitflag=False,IC=True)
# AC1上也可以查看到AP2的信息
res3=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[('\*'+ap2mac,'Managed','Success')],
                 retry=1,interval=1,waitflag=False,IC=True)                 
#result
printCheckStep(testname, 'Step 1',res1,res2,res3)                 
###############################################################################
#Step 2
#操作
# 在AC1上重启所有AP
# 预期
# AP1，AP2重启成功，并重新被管理
################################################################################
printStep(testname,'Step 2',
          'ac1 reset all aps that is managed by itself and peers',
          'ap1,ap2 reboot successfully')
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

# 检查AP2是否被AC2重新管理
res2=CheckSutCmd(switch2,'show wireless ap status', 
                 check=[(ap2mac,'Managed','Success')],
                 retry=20,interval=10,waitflag=False,IC=True)
# AC1上也可以查看到AP2的信息
res2=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'),('\*'+ap2mac,'Managed','Success')],
                 retry=10,interval=10,waitflag=False,IC=True) 
#result
printCheckStep(testname, 'Step 2',res1,res2,res3)
################################################################################
# Step 3
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 3',
          'Recover initial config')
# operate
# 恢复AP2配置
ApSetcmd(ap2,Ap2cmdtype,'set_switch_address',StaticIpv4_ac1,addressnum='1')
ApSetcmd(ap2,Ap2cmdtype,'saverunning')
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap2, ap2mac, switch2, Ap2cmdtype)
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

CheckSutCmd(switch2,'show wireless ap status', 
            check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
            retry=20,interval=10,waitflag=False,IC=True)
#end
printTimer(testname, 'End')