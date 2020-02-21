#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_5.7.py - test case 5.7 of waffirm
#
# Author:  qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 5.7 AP通过静态IPv4地址发现AC
# 测试目的：测试AP通过配置AC地址发现AC 
# 测试环境：同测试拓扑
# 测试描述：AP1上配置AC1的地址后，AP主动发现AC。AC1的无线地址：1.1.1.1
#
#*******************************************************************************
# Change log:
#     - zhangjxp 2017.11.10 RDM50304 修改step2、6
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 5.7'
avoiderror(testname)
printTimer(testname,'Start','Test manage ap via static ip')

################################################################################
#Step 1
#操作
#AC1上关闭主动发现
#S1(config-wireless)#no discovery method
#AC1上show wireless discovery看到“IP Polling Mode”显示“Disable”，
#“L2 Multicast Discovery Mode”显示“Disable”
################################################################################
printStep(testname,'Step 1',
          'set managed-ap managed-type 1 on ap1')
#operate

EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery method')

data1 = SetCmd(switch1,'show wireless discovery',timeout=5)
res1 = CheckLine(data1,'IP Polling Mode','Disable',IC=True)
res2 = CheckLine(data1,'L2 Multicast Discovery Mode','Disable',IC=True)

#result
printCheckStep(testname, 'Step 1',res1,res2)

################################################################################
#Step 2
#AP1上配置上AC1的无线地址
#后重起AP1
#WLAN-AP# set managed-ap switch-address-1 1.1.1.1
#WLAN-AP# save-running 
#WLAN-AP# reboot

################################################################################

printStep(testname,'Step 2',
          'Remove configuration of auto discovery on ac1')

# SetCmd(ap1,'set managed-ap switch-address-1',StaticIpv4_ac1)
# SetCmd(ap1,'save-running')
ApSetcmd(ap1,Ap1cmdtype,'set_switch_address1',StaticIpv4_ac1)
ApSetcmd(ap1,Ap1cmdtype,'saverunning')
if Ap1cmdtype == 'set':
    data1 = SetCmd(ap1,'get managed-ap')
    res1 = CheckLine(data1,'switch-address-1\s+' + StaticIpv4_ac1)
elif Ap1cmdtype == 'uci':
    data1 = SetCmd(ap1,'uci show mapd',timeout=10)
    res1 = CheckLine(data1,'mapd.@staticAcIp\[0\].static_acip_1=.*' + StaticIpv4_ac1)
else:
    pass
  
# RebootAp(AP=ap1)
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap1,ap1mac,switch1,Ap1cmdtype)
IdleAfter(10)
#result
printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#AC1上查看AP1的状态
#S1#show wi ap statu
#预期
#AC1上show wi ap status显示AP的“Status”为“Managed”，“Configuration Status”为“Success”
################################################################################

printStep(testname,'Step 3',
          'Check show wi ap status')
res1 = 1
# check
res1 = CheckSutCmd(switch1,'show wireless ap status',check=[(ap1mac,Ap1_ipv4,'1','Managed','Success')],retry=20,interval=5,IC=True)

printCheckStep(testname, 'Step 3',res1)

################################################################################
#Step 4
#操作
#AC1上用命令show wireless ap AP1mac status查看Discovery Reason
#预期
#AC1上用命令show wireless ap AP1mac status显示“Discovery Reason”为“Switch IP Configured”
################################################################################

printStep(testname,'Step 4',
          'Check show wi ap status')

data1 = SetCmd(switch1,'show wireless ap',ap1mac,'status')

res1 = CheckLine(data1,'Discovery Reason','Switch IP Configured')

printCheckStep(testname, 'Step 4',res1)

################################################################################
#Step 5
#操作
#AP1上删除AC1的无线地址
#WLAN-AP# set managed-ap switch-address-1 
#WLAN-AP# save-running 
#预期
#AP1上WLAN-AP# get managed-ap switch-address-1查看显示为空
################################################################################

printStep(testname,'Step 5',
          'Remove switch-address-1 config of ap1')

# SetCmd(ap1,'set managed-ap switch-address-1')
# SetCmd(ap1,'save-running')
if Ap1cmdtype == 'set':
    ApSetcmd(ap1,Ap1cmdtype,'set_switch_address1')
    ApSetcmd(ap1,Ap1cmdtype,'saverunning')
    data1 = SetCmd(ap1,'get managed-ap',timeout=10)
    res1 = CheckLine(data1,'switch-address-1')
    res2 = CheckLine(data1,'switch-address-1\s+1\.1\.1\.1')
elif Ap1cmdtype == 'uci':
    ApSetcmd(ap1,Ap1cmdtype,'set_switch_address1','192.168.1.254')
    ApSetcmd(ap1,Ap1cmdtype,'saverunning')
    data1 = SetCmd(ap1,'uci show mapd',timeout=10)
    res1 = CheckLine(data1,'mapd.@staticAcIp\[0\].static_acip_1=.*' + '192.168.1.254')
    res2 = CheckLine(data1,'mapd.@staticAcIp\[0\].static_acip_1=.*' + StaticIpv4_ac1)
else:
    pass

printCheckStep(testname, 'Step 5',res1,not res2)

################################################################################
#Step 6
#操作
#重起AP1
#WLAN-AP# reboot
#预期
#重起后AP1无法被AC1管理
################################################################################

printStep(testname,'Step 6',
          'Reboot ap1 and ap1 cannot managed by ac1')

# RebootAp(AP=ap1)
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap1,ap1mac,switch1,Ap1cmdtype)
IdleAfter(30)
data1 = SetCmd(switch1,'show wireless ap status')
res1 = CheckLine(data1,ap1mac,'Failed  Not Config')

printCheckStep(testname, 'Step 6',res1)

################################################################################
#Step 7
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 7',
          'Recover initial config for switches.')

#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery method')
i_times = 0
while i_times < 20: 
    data1 = SetCmd(switch1,'show wireless ap status')
    if 0 ==  CheckLine(data1,ap1mac,'Managed','Success',IC=True) and 0 ==  CheckLine(data1,ap2mac,'Managed','Success',IC=True):
        res1 = 0
        break
    i_times += 1
    IdleAfter(5)
# IdleAfter(Apply_profile_wait_time)
#end
printTimer(testname, 'End')