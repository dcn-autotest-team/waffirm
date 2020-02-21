#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.14.3.py - test case 4.14.3 of waffirm_new
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
# 4.14.3	基于Radio的普通限时策略
# 测试目的：测试基于 radio 普通限时策略
# 测试环境：同测试拓扑
# 测试描述：配置基于 radio 的普通限时策略，在设定时间段内限制client的接入
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package

#Global Definition
CurrentTime = '12:00:00'
Time_from = '12:01'
Time_to = '12:06'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.14.3'
printTimer(testname,'Start','test general time-limit strategy based on radio')

suggestionList = []

################################################################################
#Step 1
#操作
# 设置当前时间为12:00:00
#  switch#clock set 12:00:00
# Current time is Tue Nov 20 12:00:02 2012
#
#预期
# 当前时间被设置为12:00:00
# switch#show clock 
# Current time is Tue Nov 20 12:00:02 2012

################################################################################
printStep(testname,'Step 1',\
          'Set clock to be 12:00:00 on AC1')
EnterEnableMode(switch1)
SetCmd(switch1,'clock set 12:00:00')
res1=res2=1

#result
data2 = SetCmd(switch1,'show clock')
try:
    re1 = re.search('\w\w\w\s\w\w\w\s\d\d\s\d\d:\d\d:\d\d\s\d\d\d\d',data2)
    curtime = re1.group(0)
    timeStruct = time.strptime(curtime)
    calcTime = datetime.datetime(timeStruct.tm_year,timeStruct.tm_mon,timeStruct.tm_mday,timeStruct.tm_hour,timeStruct.tm_min,timeStruct.tm_sec)
    startTime = calcTime + datetime.timedelta(seconds=90)
    endTime = calcTime + datetime.timedelta(seconds=390)
    fromTime = str(startTime)
    toTime = str(endTime)
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
# 配置策略生效时间为12:01分至12:06分，策略持续时间为5分钟；
# switch(config-ap-profile)#radio 1
# switch(config-ap-profile-radio)#time-limit from 12:1 to 12:6 weekday all
#
#预期
# 通过命令查看配置成功
# switch#show wireless time-limit ap-profile   
# 
# AP Profile Radio Weekday    UTC-on(off)  From-Time       To-Time
# ---------- ----- --------- ------------ ------------   ------------       
# 1          1     all          N/A          12:01         12:6
################################################################################
printStep(testname,'Step 2',\
          'Config the time of strategy take effect from 12:01 t0 12:06 on radio 1')

res1 = 1
Time_from = fromTime[11:16]
Time_to = toTime[11:16]
#operate
EnterApProMode(switch1,'1')
SetCmd(switch1,'radio 1')
SetCmd(switch1,'time-limit','from',Time_from,'to',Time_to,'weekday all')
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless time-limit ap-profile')

#check
res1 = CheckLine(data1,'1','1','all',Time_from,Time_to)           

#result
printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#等待
#
#预期
#12:1分配置生效，radio1关闭，client无法接入，12:6分radio1重新开启，client可以重新接入
################################################################################
printStep(testname,'Step 3',\
          'Wait for the effect of the configuration',\
          'Check if client was denied since 12:1,and permitted after 12:6 to network 1')

res1=res3=res4=1
res2=0

#operate
i_time = 0
EnterEnableMode(switch1)
IdleAfter(1)
while i_time < 20:
    data0 = SetCmd(switch1,'show clock')
    SearchResult = re.search('\s*'+ Time_from,data0)
    if None != SearchResult:
        break
        
    i_time += 1    
    if 20 == i_time:
        SetCmd(switch1,'clock set',Time_from+':00')        
    IdleAfter(3)
#?????????????????????????????此处 get radio wlan0 在由up 转down时，有时会延时10几秒，有时严格执行时间限制
#AP1上查看radio1 状态
IdleAfter(70)
data1 = SetCmd(ap1,'get radio wlan0')
res2 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)            

#等待至12:06之后
i_time = 0
EnterEnableMode(switch1)
IdleAfter(1)
while i_time < 50:
    data0 = SetCmd(switch1,'show clock')
    SearchResult = re.search('\s*'+ Time_to,data0)
    if None != SearchResult:
        break
        
    i_time += 1    
    if 50 == i_time:
        SetCmd(switch1,'clock set',Time_to+':00')        
    IdleAfter(6)

#AP1上查看 radio1状态
IdleAfter(120)
IdleAfter(15)
data3 = SetCmd(ap1,'get radio wlan0')
   
#在12:06之后，radio 1开启，client可以接入network1
res4 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
if res4 == 5:
    suggestionList.append('Suggestions: Step 3 failed reason MAYBE RDM17089')

#check
res1 = CheckLine(data1,'status\s*down',IC=True)
res2 = 0 if 0 != res2 else 1
res3 = CheckLine(data3,'status\s*up',IC=True)

#result
printCheckStep(testname,'Step 3',res1,res2,res3,res4)

################################################################################
#Step 4
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 4',\
          'Recover initial config')

#operate

#解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

#删除时间策略
EnterApProMode(switch1,'1')
SetCmd(switch1,'radio 1')
SetCmd(switch1,'no','time-limit') 

# #恢复系统时间

#end
printTimer(testname, 'End')