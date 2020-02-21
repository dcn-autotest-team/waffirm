#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.14.2.py - test case 4.14.2 of waffirm_new
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
# 4.14.2	基于SSID的 UTC 限时策略
# 测试目的：测试基于SSID UTC 限时策略
# 测试环境：同测试拓扑
# 测试描述：配置基于SSID的UTC的限时策略，在设定时间段内限制client的接入
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package
import time
import datetime
#Global Definition
CurrentTime = '11:00:00 2012.12.21'
UTC_time_from = '2012-12-21 11:01'
UTC_time_to = '2012-12-21 11:03'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.14.2'
avoiderror(testname)
printTimer(testname,'Start','test UTC time-limit strategy based on SSID')

suggestionList = []

################################################################################
#Step 1
#操作
# 设置当前时间为11:00:00
#  switch#clock set 11:00:00
# Current time is Tue Nov 20 11:00:02 2012
#
#预期
# 当前时间被设置为11:00:00
# switch#show clock 
# Current time is Tue Nov 20 11:00:02 2012

################################################################################
printStep(testname,'Step 1',
          'Set clock to be 11:00:00 on AC1')

res1=res2=1

###operate
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

#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#操作
# 配置策略生效时间为11:01分至11:03分，策略持续时间为2分钟；
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
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'time-limit-UTC','from',UTC_time_from,'to',UTC_time_to,'off')
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless time-limit ssid',timeout=5)

#check
res1 = CheckLine(data1,'1',Network_name1,'off',UTC_time_from,UTC_time_to)           

#result
printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#等待
#
#预期
#11:1分配置生效，client无法接入network1,11:3分钟后client可以重新接入network1；
################################################################################

printStep(testname,'Step 3',
          'Wait for the effect of the configuration',
          'Check if client was denied since 11:1,and permitted after 11:3 to network 1')

res1=0
res2=1

#operate
i_time = 0
EnterEnableMode(switch1)
IdleAfter(1)
while i_time < 60:
    data0 = SetCmd(switch1,'show clock')
    SearchResult = re.search('\s*'+ UTC_time_from[-5:],data0)
    if None != SearchResult:
        break
        
    i_time += 1    
    if 20 == i_time:
        SetCmd(switch1,'clock set',UTC_time_from[-5:]+':00')        
    IdleAfter(3)
IdleAfter(60)
#在 11:01至 11:03时间段内，client无法接入network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,reconnectflag=0,bssid=ap1mac_lower)            
res1 = 0 if 0 != res1 else 1

###等待至10:03之后
##i_time = 0

##IdleAfter(1)
##while i_time < 20:
##    data0 = SetCmd(switch1,'show clock')
##    SearchResult = re.search('\s*'+ UTC_time_to[-5:],data0)
##    if None != SearchResult:
##        break
##        
##    i_time += 1    
##    if 20 == i_time:
##        SetCmd(switch1,'clock set',UTC_time_from[-5:]+':00')        
##    IdleAfter(6)
##IdleAfter(120)    
###在11:03之后，client可以接入network1
##res2 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
##
##if res2 == 5:
##    suggestionList.append('Suggestions: Step 3 failed reason MAYBE RDM17089')

#check

#result
printCheckStep(testname,'Step 3',res1)

################################################################################
#Step 4
#操作
# 设置当前时间为11:00:00
#  switch#clock set 11:00:00
# Current time is Tue Nov 20 11:00:02 2012
#
#预期
# 当前时间被设置为11:00:00
# switch#show clock 
# Current time is Tue Nov 20 11:00:02 2012

################################################################################
##printStep(testname,'Step 4',\
##          'Set clock to be 11:00:00 on AC1')
##
##res1=res2=1
##
###operate
##

##data1 = SetCmd(switch1,'clock set',CurrentTime)
##IdleAfter(1)
##data2 = SetCmd(switch1,'show clock')
##
###check
##res1 = CheckLine(data1,'Current time',CurrentTime[:6],IC=True)
##res2 = CheckLine(data2,'Current time',CurrentTime[:6],IC=True)
###result
##printCheckStep(testname, 'Step 4',res1,res2)

################################################################################
#Step 5
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 5',
          'Recover initial config')

#operate

#解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

#删除时间策略
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no','time-limit-UTC')    

#系统时间不再恢复，无意义

#end
printTimer(testname, 'End',suggestion = suggestionList)