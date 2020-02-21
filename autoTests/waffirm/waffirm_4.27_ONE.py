#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.27.py - test case 4.27 of waffirm
#
# Author:  zhaohj@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.27 SSH访问
# 测试目的：测试可以通过ssh方式访问AC和AP
# 测试环境：同测试拓扑
# 测试描述：可以通过ssh方式访问AC（ip地址1.1.1.1）和AP（20.1.1.3）。
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.27'
avoiderror(testname)
printTimer(testname,'Start','Test SSH')

################################################################################
#Step 1
#操作
#S1（Ac1）上ssh server缺省为关闭
#预期
#s1上show ssh-server显示“ssh server is disabled”。Pc1无法ssh访问ac1（ip地址1.1.1.1）
################################################################################
printStep(testname,'Step 1',
          'show ssh-server on s1,',
          'ssh server is disabled on s1,',
          'pc1 can not ssh s1.')
#operate
EnterEnableMode(switch1)
#check
data1 = SetCmd(switch1,'show ssh-server | include ssh server is',timeout=10)
res1 = CheckLine(data1,'ssh server is disabled')
data2 = SetCmd(pc1,'ssh '+Ssh_login_name+'@'+StaticIpv4_ac1)
res2 = CheckLine(data2,'ssh','connect to host '+StaticIpv4_ac1,'Connection refused')
#result
printCheckStep(testname, 'Step 1',res1,res2)

################################################################################
#Step 2
#操作
#S1上开启ssh：
#config 
#ssh-server enable
#
#预期
#s1上show ssh-server显示“ssh server is enabled”。
################################################################################

printStep(testname,'Step 2',
          'set ssh-server enable on s1,',
          'config success.')

EnterConfigMode(switch1)
SetCmd(switch1,'ssh-server enable')
#check
data = SetCmd(switch1,'show ssh-server')
res = CheckLine(data,'ssh server is enabled')
#result
printCheckStep(testname, 'Step 2',res)

################################################################################
#Step 3
#操作
#Pc1上ssh方式访问ac1（用户名密码都是admin），
#（ssh方式访问ac1后）在ac1上show wireless ap status。
#
#预期
#Pc1可以ssh访问ac1。show wireless ap status显示ap1为“Managed Success”状态。
################################################################################

printStep(testname,'Step 3',
          'pc1 ssh login ac1,',
          'pc1 ssh login ac1 success,',
          'show wireless ap status on pc1, ap1 is Managed Success.')
#check
SetCmd(pc1,'rm -f /root/.ssh/known_hosts',timeout=5)
SshLogin(pc1,StaticIpv4_ac1,Ssh_login_name,Ssh_login_password)
data = SetCmd(pc1,'show wireless ap status')
res = CheckLine(data,ap1mac,'Managed','Success',IC=True)
#result
printCheckStep(testname, 'Step 3',res)

#PC1 logout s1
res = CheckLine(data,'command','not found',IC=True)
if res != 0:
    SetCmd(pc1,'exit')

################################################################################
#Step 4
#操作
#Ap1上ssh缺省为开启SSH
#
#预期
#Ap1上 AP# get ssh 显示为“up”
################################################################################

printStep(testname,'Step 4',
          'get ssh on ap1,',
          'state is up.')
#check
data = SetCmd(ap1,'get ssh')
res = CheckLine(data,'up')
#result
printCheckStep(testname, 'Step 4',res)

################################################################################
#Step 5
#操作
#Pc1上ssh方式访问ap1（用户名密码都是admin，ip地址20.1.1.3）
#预期
#Pc1可以ssh访问ap1。Ap1上get management显示ip地址为20.1.1.3
################################################################################

printStep(testname,'Step 5',
          'pc1 ssh login ap1,',
          'login success and get management success.')
#check
SshLogin(pc1,Ap1_ipv4,Ssh_login_name,Ssh_login_password)
# data1 = SetCmd(pc1,'ssh '+Ssh_login_name+'@'+Ap1_ipv4,timeout=5)
# if 0 == CheckLine(data1,'yes/no'):
    # SetCmd(pc1,'yes',timeout=5)
# SetCmd(pc1,Ssh_login_password,timeout=5)
data = SetCmd(pc1,'get management')
res = CheckLine(data,'ip',Ap1_ipv4,IC=True)

#result
printCheckStep(testname, 'Step 5',res)

#PC1 logout ap1
res = CheckLine(data,'command','not found',IC=True)
if res != 0:
    SetCmd(pc1,'exit')

################################################################################
#Step 6
#操作
#Ap1上关闭ssh：
#set ssh status down
#
#预期
#Ap1上AP# get ssh 显示为“down”
#Pc1无法ssh访问ap1
################################################################################

printStep(testname,'Step 6',
          'disable ssh on ap1',
          'config success and pc1 can not ssh login ap1.')

SetCmd(ap1,'set ssh status down')
#check
data1 = SetCmd(ap1,'get ssh')
res1 = CheckLine(data1,'down')
data2 = SetCmd(pc1,'ssh '+Ssh_login_name+'@'+Ap1_ipv4)
res2 = CheckLine(data2,'ssh','connect to host '+Ap1_ipv4,'Connection refused')

#result
printCheckStep(testname, 'Step 6',res1,res2)

################################################################################
#Step 7
#操作
#恢复初始配置
################################################################################
printStep(testname,'Step 7',
          'Recover initial config for switches.')

#operate
SetCmd(switch1,'no ssh-server enable')
SetCmd(ap1,'set ssh status up')

#end
printTimer(testname, 'End')