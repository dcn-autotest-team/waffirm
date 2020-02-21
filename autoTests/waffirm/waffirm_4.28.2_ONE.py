#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.28.2.py - test case 4.28.2 of waffirm_new
#
# Author:  (fuzf@dc.com)
#
# Version 1.0.0
#
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 4.28.2  AP使用ap database下配置的profile
# 测试目的：验证ap database下配置的profile优先级高于自动选择
# 测试环境：同测试拓扑
# 测试描述：验证ap database下配置的profile优先级高于自动选择:包括根据AP地址选择和hwtype选择
#（AP1的MAC地址：AP1MAC ；AP1的ip地址是20.1.1.3）
#
#*******************************************************************************
# Change log:
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
#*******************************************************************************

###########

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.28.2'
avoiderror(testname)
printTimer(testname,'Start','test ap use profile configured under the ap database')

################################################################################
#Step 1
#
#操作
# 配置AC1 profile1的硬件类型为any
# 
#
#预期
# 配置成功，show wireless ap profile 1进行确认
#
################################################################################
printStep(testname,'Step 1',
          'Config AC1 Profile1 hwtype with any',
          'show wireless ap profile 1 check the results')

res1=1
#operate
#配置profile 1的hwtype为AP1的hwtype
EnterApProMode(switch1,1)
SetCmd(switch1,'hwtype any')
data1 = SetCmd(switch1,'show wireless ap profile 1',timeout=10)


#把AP1 Database下指定的profile删除
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'no profile')

#check
res1 = CheckLine(data1,'Hardware Type','Any',IC=True)
if 0 != res1:
    printRes('Fail:Config profile 1 hwtype failed!')

#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#操作
# 配置Ac1 profile2的hwtype为any
# 
#
#预期
# 配置成功，show wireless ap profile 2可以看到：
# Hardware Type.................................. 0 - Any
# 
################################################################################
printStep(testname,'Step 2',
          'Config AC1 Profile2 hwtype with any',
          'show wireless ap profile 2 check the results')

res1=1
#operate
EnterApProMode(switch1,2)
SetCmd(switch1,'hwtype any')
data1 = SetCmd(switch1,'show wireless ap profile 2')

#check
res1 = CheckLine(data1,'Hardware Type','Any',IC=True)

if res1 != 0:
    printRes('Fail:set profile 2 hwtype any failed!')

#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#操作
# 配置AP1的IP地址对应profile 1
# ap address Ap1_ipv4 Ap1_ipv4 profile 1
#
#预期
# show run查看配置成功
################################################################################
printStep(testname,'Step 3',
          'set ap address Ap1_ipv4 Ap1_ipv4 profile 1',
          'show run Check the result')

res1=1
#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap address',Ap1_ipv4,Ap1_ipv4,'profile 1')
data1 = SetCmd(switch1,'show running-config current-mode')

#check
res1 = CheckLine(data1,'ap address',Ap1_ipv4,Ap1_ipv4,'profile 1',IC=True)

#result
printCheckStep(testname, 'Step 3',res1)


################################################################################
#Step 4
#
#操作
# 在ap database下指定AP1使用profile 2
# ap database ap1mac
#    profile 2
#
#预期
# show wireless ap database ap1mac可以看到：
# Profile........................................ 2 - Default
################################################################################
printStep(testname,'Step 4',
          'ap database ap1mac',
          'profile 2',
          'show wireless ap database ap1mac')

res1=1
#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'profile',2)

#check
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless ap database',ap1mac)
res1 = CheckLine(data1,'Profile','2 - Default')

#result
printCheckStep(testname, 'Step 4',res1)


################################################################################
#Step 5
#操作
# 重起AP1
# WLAN-AP# reboot
#
#预期
#重起后AP1被AC1的profile 2管理，
################################################################################
printStep(testname,'Step 5',
          'Reboot AP1',
          'Check if AC1 managed AP1 with profile2')

res1=1

#operate
RebootAp(AP=ap1)

#IdleAfter(Var_ap_connect_after_reboot)

EnterEnableMode(switch1)
i=0
while i<10:
	data1 = SetCmd(switch1,'show wireless ap status')
	res1 = CheckLine(data1,ap1mac,Ap1_ipv4,'2','Managed','Success',IC=True)
	if res1==0:
		break
	IdleAfter(5)
	i=i+1


#result
printCheckStep(testname, 'Step 5', res1)

################################################################################
#Step 6
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 6',
          'Recover initial config')

#operate

# AC1恢复
EnterWirelessMode(switch1)
SetCmd(switch1,'no ap address',Ap1_ipv4,Ap1_ipv4,'profile 1')
#配置Ap-profile1
EnterApProMode(switch1,1)
SetCmd(switch1,'hwtype',hwtype1)
# SetCmd(switch1,'radio 1')
SetCmd(switch1,'radio '+radio1num)
SetCmd(switch1,'rf-scan other-channels interval 5')
SetCmd(switch1,'rf-scan duration 50')
SetCmd(switch1,'vap 1')
SetCmd(switch1,'enable')
SetCmd(switch1,'exit')
SetCmd(switch1,'exit')
# SetCmd(switch1,'radio 2')
SetCmd(switch1,'radio '+radio2num)
SetCmd(switch1,'mode ac')
SetCmd(switch1,'vap 1')
SetCmd(switch1,'enable')
SetCmd(switch1,'exit')
SetCmd(switch1,'exit')
SetCmd(switch1,'exit')
#配置Ap-profile2
EnterApProMode(switch1,2)
SetCmd(switch1,'hwtype',hwtype2)
# SetCmd(switch1,'radio 1')
SetCmd(switch1,'radio '+radio1num)
SetCmd(switch1,'vap 1')
SetCmd(switch1,'enable')
SetCmd(switch1,'exit')
SetCmd(switch1,'exit')
# SetCmd(switch1,'radio 2')
SetCmd(switch1,'radio '+radio2num)
SetCmd(switch1,'mode ac')
SetCmd(switch1,'vap 1')
SetCmd(switch1,'enable')
SetCmd(switch1,'end')

#在 AP1 database下指定profile
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'profile 1')

#重启AP1 AP2
# RebootAp(AP=ap1)
# RebootAp(AP=ap2)
RebootMulitAp(AP=[ap1,ap2])
# IdleAfter(Ap_connect_after_reboot)

#end
printTimer(testname, 'End')
