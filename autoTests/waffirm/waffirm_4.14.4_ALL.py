#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.14.4.py - test case 4.14.4 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
# 
# Date 2012-12-7 14:37:33
#
# Features:
# 4.14.4	基于 radio 的 UTC 限时策略
# 测试目的：测试基于radio UTC 限时策略
# 测试环境：同测试拓扑
# 测试描述：通过配置UTC策略关闭radio进行限制client的接入
#
#*******************************************************************************
# Change log:
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
#*******************************************************************************

#Package
import time
import datetime
#Global Definition
CurrentTime = '13:00:00 2012.12.21'
UTC_time_from = '2012-12-21 13:01'
UTC_time_to = '2012-12-21 13:06'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.14.4'
avoiderror(testname)
printTimer(testname,'Start','test UTC time-limit strategy based on radio')

# 2.4G、5G差异化配置,test24gflag为True代表执行2.4G脚本，False代表执行5G脚本
# if test24gflag ==  True:
    # radionum='1'
    # wlan='wlan0'
# else:
    # radionum='2'
    # wlan='wlan1'
################################################################################
#Step 1
#操作
# 设置当前时间为13:00:00
#  switch#clock set 13:00:00
# Current time is Tue Nov 20 13:00:02 2012
#
#预期
# 当前时间被设置为13:00:00
# switch#show clock 
# Current time is Tue Nov 20 13:00:02 2012

################################################################################
printStep(testname,'Step 1',
          'Set clock to be 13:00:00 on AC1')

res1=res2=1

#operate
#result
try:
    curtime = GetSwitchTime(switch1)
    print 'curtime=',curtime
    timeStruct = time.strptime(curtime)
    print 'timeStruct=',timeStruct
    calcTime = datetime.datetime(timeStruct.tm_year,timeStruct.tm_mon,timeStruct.tm_mday,timeStruct.tm_hour,timeStruct.tm_min,timeStruct.tm_sec)
    print 'calcTime=',calcTime
    startTime = calcTime + datetime.timedelta(seconds=90)
    print 'startTime=',startTime
    endTime = calcTime + datetime.timedelta(seconds=1890)
    print 'endTime=',endTime
    fromTime = str(startTime)
    print 'fromTime=',fromTime
    toTime = str(endTime)
    print 'toTime=',toTime
    res1 = 0
except Exception:
    fromTime = '2001-01-01 01:01:01'
    toTime = '2001-01-01 01:01:01'
    res1 =1
print fromTime
print toTime
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#操作
# 配置策略生效时间为13:01分至13:06分，策略持续时间为5分钟；
# switch(config-wireless)#network 1
# switch(config-network)#time-limit-UTC from 2012-11-20 11:1 to 2012-11-20 11:3 off
#
#预期
# 通过命令查看配置成功
# switch#show wireless time-limit ssid 
# Network SSID       Weekday   UTC-on(off)  From-Time         To-Time
# ------- ------- -- --------   ------      ---------          ------        
# 1       dcn        N/A          off     2012-11-20 11:01   2012-11-20 11:03
################################################################################
printStep(testname,'Step 2',
          'Config the time of strategy take effect from 11:01 t0 11:03 on network 1')
UTC_time_from = fromTime[:16]
UTC_time_to = toTime[:16]
res1 = 1
#operate
EnterApProMode(switch1,'1')
SetCmd(switch1,'radio '+radionum)
SetCmd(switch1,'time-limit-UTC','from',UTC_time_from,'to',UTC_time_to,'off')
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless time-limit ap-profile',timeout=5)

#check
res1 = CheckLine(data1,'1',radionum,'off',UTC_time_from,UTC_time_to)           

#result
printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#等待
#
#预期
#13:1分配置生效，radio1关闭，client无法接入，13:6分钟radio1重新开启，client可以重新接入；
################################################################################
printStep(testname,'Step 3',
          'Wait for the effect of the configuration',
          'Check if client was denied since 13:1,and permitted after 13:6 to network 1')

res1=res3=res4=1
res2=0

#operate
i_time = 0
EnterEnableMode(switch1)
IdleAfter(1)
while i_time < 20:
    data0 = SetCmd(switch1,'show clock')
    SearchResult = re.search('\s*'+ UTC_time_from[-5:],data0)
    if None != SearchResult:
        break
        
    i_time += 1    
    if 60 == i_time:
        SetCmd(switch1,'clock set',UTC_time_from[-5:]+':00')        
    IdleAfter(3)

#AP1上查看 radio1状态
IdleAfter(120)
data1 = SetCmd(ap1,'get radio',wlan)

#在 13:01至 13:06时间段内，radio 1 关闭，client无法接入
res2 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,reconnectflag=0,bssid=ap1mac_lower)            


###等待至13:06之后
##i_time = 0

##IdleAfter(1)
##while i_time < 50:
##    data0 = SetCmd(switch1,'show clock')
##    SearchResult = re.search('\s*'+ UTC_time_to[-5:],data0)
##    if None != SearchResult:
##        break
##        
##    i_time += 1    
##    if 50 == i_time:
##        SetCmd(switch1,'clock set',UTC_time_from[-5:]+':00')        
##    IdleAfter(6)
##
###AP1上查看 radio1状态
##IdleAfter(120)
##IdleAfter(15)
data3 = SetCmd(ap1,'get radio',wlan)
##    
###在13:06之后，radio 1 开启，client可以接入
##res4 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)

#check
res1 = CheckLine(data1,'status\s*down',IC=True)
res2 = 0 if 0 != res2 else 1
res3 = CheckLine(data3,'status\s*up',IC=True)


#result
printCheckStep(testname,'Step 3',res2)

################################################################################
#Step 4
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 4',
          'Recover initial config')

#operate

#解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

#删除时间策略
EnterApProMode(switch1,'1')
SetCmd(switch1,'radio '+radionum)
SetCmd(switch1,'no','time-limit-UTC') 
   
# 
# #恢复系统时间
# EnterEnableMode(switch1)
# SetCmd(switch1,'clock set',init_Time)

#end
printTimer(testname, 'End')