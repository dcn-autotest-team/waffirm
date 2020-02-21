#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.14.1.py - test case 4.14.1 of waffirm_new
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
# 4.14.1	基于SSID的普通限时策略
# 测试目的：测试基于SSID普通限时策略
# 测试环境：同测试拓扑
# 测试描述：配置基于SSID的普通限时策略，在设定时间段内限制client的接入
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package
import time
import datetime
#Global Definition
CurrentTime = '10:00:00'
Time_from = '10:01'
Time_to = '10:03'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.14.1'
avoiderror(testname)
printTimer(testname,'Start','test general time-limit strategy based on SSID')

suggestionList = []

################################################################################
#Step 1
#操作
# 设置当前时间为10:00:00
#  switch#clock set 10:00:00
# Current time is Tue Nov 20 10:00:02 2012
#
#预期
# 当前时间被设置为10:00:00
# switch#show clock 
# Current time is Tue Nov 20 10:00:02 2012

################################################################################
printStep(testname,'Step 1',
          'Set clock to be 10:00:00 on AC1')

res1=res2=1
#operate
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
#check
#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#操作
# 配置策略生效时间为10:01分至10:03分，策略持续时间为2分钟；
# switch(config-wireless)#network 1
# switch(config-network)#time-limit from 10:1 to  10:3  weekday all
#
#预期
# 通过命令查看配置成功 
# switch#show wireless time-limit ssid  
# Network SSID     Weekday    UTC-on(off)  From-Time   To-Time
# ------- -------  --------   ------------ ----------  -------
# 1       dcn            all      N/A      10:01      10:03
################################################################################
printStep(testname,'Step 2',
          'Config the time of strategy take effect from 10:01 t0 10:03 on network 1')

res1 = 1
Time_from = fromTime[11:16]
Time_to = toTime[11:16]
#operate
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'time-limit','from',Time_from,'to',Time_to,'weekday all')
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless time-limit ssid',timeout=5)

#check
res1 = CheckLine(data1,'1',Network_name1,'all',Time_from,Time_to)           

#result
printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#等待
#
#预期
#10:1分配置生效，client无法接入network1,10:3分钟后client可以重新接入network1；
################################################################################
printStep(testname,'Step 3',
          'Wait for the effect of the configuration',
          'Check if client was denied since 10:1,and permitted after 10:3 to network 1')

res1=0
res2=1

#operate
i_time = 0
EnterEnableMode(switch1)
IdleAfter(1)
while i_time < 60:
    data0 = SetCmd(switch1,'show clock')
    SearchResult = re.search('\s*'+ Time_from,data0)
    if None != SearchResult:
        break
        
    i_time += 1    
    if 20 == i_time:
        SetCmd(switch1,'clock set',Time_from+':00')        
    IdleAfter(3)
IdleAfter(60)
#在 10:01至 10:03时间段内，client无法接入network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,reconnectflag=0,bssid=ap1mac_lower)            
res1 = 0 if 0 != res1 else 1

###等待至10:03之后
##i_time = 0

##IdleAfter(1)
##while i_time < 20:
##    data0 = SetCmd(switch1,'show clock')
##    SearchResult = re.search('\s*'+ Time_to,data0)
##    if None != SearchResult:
##        break
##        
##    i_time += 1    
##    if 20 == i_time:
##        SetCmd(switch1,'clock set',Time_to+':00')        
##    IdleAfter(6)
##IdleAfter(120)
###在10:03之后，client可以接入network1
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
# 设置当前时间为10:00:00
#  switch#clock set 10:00:00
# Current time is Tue Nov 20 10:00:02 2012
#
#预期
# 当前时间被设置为10:00:00
# switch#show clock 
# Current time is Tue Nov 20 10:00:02 2012

################################################################################
##printStep(testname,'Step 4',\
##          'Set clock to be 10:00:00 on AC1')
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
##res1 = CheckLine(data1,'Current time',CurrentTime[:-2],IC=True)
##res2 = CheckLine(data2,'Current time',CurrentTime[:-2],IC=True)
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
SetCmd(switch1,'no','time-limit') 

#end
printTimer(testname, 'End',suggestion = suggestionList)
