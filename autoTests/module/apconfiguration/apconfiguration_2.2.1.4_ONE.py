#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.1.4.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features:
# 2.2.1.4	非controler管理AC上可以重启自己所有ap
# 测试目的：管理AC上可以wireless ap reset重启所有自己管理ap，peer管理的ap不会重启（AC不是Controller）。
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

testname = 'apconfiguration_2.2.1.4'
avoiderror(testname)
printTimer(testname,'Start','ac(not controller) can reset the aps that is managed by itself, and peer\'s aps should not reboot')

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
#result
printCheckStep(testname, 'Step 1',res1,res2)        
###############################################################################
#Step 2
#操作
# 在AC2上重启所有管理AP
# 预期
# AP2重启成功，AP1不受影响
################################################################################
printStep(testname,'Step 2',
          'ac2 reset all aps that is managed by itself',
          'ap2 reboot successfully',
          'ap1 should not be influenced by ap2 rebooting')
res1=res2=1
#operate
StartDebug(ap1)
StartDebug(ap2)

# AC2重启所有被管理AP
EnterEnableMode(switch2)
SetCmd(switch2, 'wireless ap reset', promotePatten='Y/N',promoteTimeout=10)
SetCmd(switch2,'y')
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

# 检查AP2是否被AC2重新管理
res3=CheckSutCmd(switch2,'show wireless ap status', 
                 check=[(ap2mac,'Managed','Success')],
                 retry=20,interval=10,waitflag=False,IC=True)
if res2 != 0:
    ApLogin(ap1,retry=20)
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