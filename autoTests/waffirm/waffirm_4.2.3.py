#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.2.3.py - test case 4.2.3 of waffirm_new
#
# Author:  (jinpfb)
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Date: 2012-12-12 13:28:14
#
# Features:
# 4.2.3	AP手动功率调整 
# 测试目的：AP能够手动设置功率的大小。
# 测试环境：同测试拓扑
# 测试描述：AP能够通过手动的方式来设置功率的大小，设定后AP工作正常。
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package

#Global Definition

Power_1 = '1'
Power_90 = '90'
Power_50 = '50'

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.2.3'
avoiderror(testname)
printTimer(testname,'Start','test ajustment the power of ap by hand')

################################################################################
#Step 1
#操作
#关闭AP1的自动功率调整功能,通过AC1将AP1的功率设置为1%，下发至AP1
#
#预期
#配置成功。在AC1上面查看AP1当前的功率默认为100%。
################################################################################
printStep(testname,'Step 1',
          'close the auto-ajustment function of ap ',
          'set power of ap 1% and apply to ap')

res1=res2=1
#operate
EnterApProMode(switch1,1)
SetCmd(switch1,'radio 1')
SetCmd(switch1,'no power auto')
data1 = SetCmd(switch1,'show wireless ap radio status',promotePatten='#')

EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap power set',ap1mac,'radio 1',Power_1)
IdleAfter(20)
data2 = SetCmd(switch1,'show wireless ap radio status',promotePatten='#')

#check
res1 = CheckLine(data1,ap1mac,1,'\d+',100,RS=True)
res2 = CheckLine(data2,ap1mac,1,'\d+',Power_1,RS=True)

#result
printCheckStep(testname, 'Step 2', res1,res2)

################################################################################
#Step 2
#操作
#在客户端STA1扫描无线网络test1
#
#预期
#显示test1的信号强度，记录该值
################################################################################

printStep(testname,'Step 2',
          'STA1 scanning test1',
          'record the power1 of test1.')

res1=1
#operate

#因为信号不稳定，所以建议改成扫描一分钟，每5s扫描一次，然后取平均值
i_time = 0
level_list = list()
power1_total = 0
while i_time < Signal_scan_times:
    power = 0
    StaScanSSID(sta1,Netcard_sta1)
    data = SetCmd(sta1,'wpa_cli -i '+ Netcard_sta1 +' scan_results')
    power = int(str(GetValueBetweenTwoValuesInData (data,ap1mac_lower+'\s+\d+','\[.*?'+Network_name1)).lstrip().rstrip())
    if power > 0:
        level_list.append(power)
    IdleAfter(Signal_scan_diff_time)
    i_time = i_time + 1
    
if 0 < len(level_list):
    for index in range(len(level_list)):
        power1_total = power1_total + level_list[index]
    power1 = power1_total / len(level_list)
else:
    printRes('Failed: the network can not scan as power too low')
    power1 = 0
    
printRes('power1 = '+ str(power1))
#check
if 0 < power1:
    res1 = 0

#result
printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#通过AC1修改AP1的功率，设置为90%，下发至AP1。
#
#预期
#下发成功。在UWS1上面查看AP1的功率为60%。
################################################################################

printStep(testname,'Step 3',
          'set power of ap 90% and apply ap profile to ap,',
          'config success and show the power of ap is 90%.')

res1=1
#operate
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap power set',ap1mac,'radio 1',Power_90)
IdleAfter(20)
data1 = SetCmd(switch1,'show wireless ap radio status',promotePatten='#')

#check
res1 = CheckLine(data1,ap1mac,1,'\d+',Power_90,RS=True)

#result
printCheckStep(testname, 'Step 3',res1)

################################################################################
#Step 4
#操作
#在客户端STA1扫描无线网络test1。
#
#预期
#test1的信号强度大于 Step2
################################################################################

printStep(testname,'Step 4',
          'STA1 scanning test1',
          'record the power90 of test1,power90 should larger than power1.')

res1=1
#operate
#因为信号不稳定，所以建议改成扫描一分钟，每5s扫描一次，然后取平均值
i_time = 0
level_list = list()
power90_total = 0
while i_time < Signal_scan_times:
    power = 0    
    StaScanSSID(sta1,Netcard_sta1)
    data = SetCmd(sta1,'wpa_cli -i '+ Netcard_sta1 +' scan_results')
    power = int(str(GetValueBetweenTwoValuesInData (data,ap1mac_lower+'\s+\d+','\[.*?'+Network_name1)).lstrip().rstrip())
    if power > 0:
        level_list.append(power)
    IdleAfter(Signal_scan_diff_time)
    i_time = i_time+1
    
if 0 < len(level_list):
    for index in range(len(level_list)):
        power90_total = power90_total + level_list[index]
    power90 = power90_total / len(level_list)
else:
    printRes('Failed: the network can not scan as power too low')
    power90 = 0

printRes('power1 = '+ str(power1))
printRes('power90 = '+ str(power90))

#check
res1 = 0 if power90 > power1 else 1    

#result
printCheckStep(testname, 'Step 4',res1)

################################################################################
#Step 5
#操作
#通过AC1修改AP1的功率，设置为50%，下发至AP1。
#
#预期
#下发成功。在UWS1上面查看AP1的功率为50%。
################################################################################
printStep(testname,'Step 5',
          'set power of ap 50% and apply ap profile to ap,',
          'config success and show the power of ap is 50%.')

res1=1
#operate
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap power set',ap1mac,'radio 1',Power_50)
IdleAfter(20)
data1 = SetCmd(switch1,'show wireless ap radio status',promotePatten='#')

#check
res1 = CheckLine(data1,ap1mac,1,'\d+',Power_50,RS=True)

#result
printCheckStep(testname, 'Step 5',res1)

################################################################################
#Step 6
#操作
#在客户端STA1扫描无线网络test1
#
#预期
#信号强度大于Step2,小于 Step4
################################################################################

printStep(testname,'Step 6',
          'STA1 scanning test1',
          'record the power50 of test1,power50 should larger than power1,',
          'and lower than power90')

res1=1

#operate
i_time = 0
level_list = list()
power50_total = 0
while i_time < Signal_scan_times:
    power = 0
    StaScanSSID(sta1,Netcard_sta1)
    data = SetCmd(sta1,'wpa_cli -i '+ Netcard_sta1 +' scan_results')
    power = int(str(GetValueBetweenTwoValuesInData (data,ap1mac_lower+'\s+\d+','\[.*?'+Network_name1)).lstrip().rstrip())
    if power > 0:
        level_list.append(power)
    IdleAfter(Signal_scan_diff_time)
    i_time = i_time+1
    
if 0 < len(level_list):
    for index in range(len(level_list)):
        power50_total = power50_total + level_list[index]
    power50 = power50_total / len(level_list)

printRes('power1 = '+ str(power1))
printRes('power90 = '+ str(power90))
printRes('power50 = ' + str(power50))

#check
if (power50 > power1) and (power50 < power90):
    res1 = 0

#result
printCheckStep(testname, 'Step 6',res1)

################################################################################
#Step 7
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 7',
          'Recover initial config for switches.')

#operate

#Power auto
EnterApProMode(switch1,1)
SetCmd(switch1,'radio 1')
SetCmd(switch1,'power auto')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'radio 1 power 0')
IdleAfter(10)
RebootAp(AP=ap1)

#end
printTimer(testname, 'End')