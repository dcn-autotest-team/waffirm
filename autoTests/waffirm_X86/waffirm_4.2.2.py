#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.2.2.py - test case 4.2.3 of waffirm_new
#
# Author:  jinpfb
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Date: 2012-12-11 14:06:44
#
# Features:
# 4.2.2	自动信道调整功能 
# 测试目的：AP能够使用自动信道选择分配信道。
# 测试环境：同测试拓扑
# 测试描述：测试AP能够根据周围其他AP的信道，合理的选择和调整自身的工作信道。AP自
# 动分配信道后能正常工作。（AP1的MAC地址：AP1MAC；AP2 的MAC地址：AP2MAC）
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package

#Global Definition
Bgn_interval = 4

Ap1channel_x = ''
Ap2channel_y = ''
Ap2channel_z = ''
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.2.2'
printTimer(testname,'Start','test automatic channel ajustment of ap')

################################################################################
#Step 1
#操作
#AC1上察看目前2个AP工作信道
#  show wireless ap radio status
#
#预期
#AC1上show wireless ap radio status 显示2个AP的“Radio Channel”依次为'1 x','1 y'
#（AP1的2.4G radio工作在信道x，AP2的2.4G radio工作在信道y）
################################################################################
printStep(testname,"Step 1',\
          'Show wireless ap radio status,', \
          'Check 'Radio Channel' of AP1 and AP2")

res1=res2=res3=1
#operate
IdleAfter(60)
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless ap status')
res1 = CheckLineList(data1,[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],IC=True)
if res1 != 0:
    IdleAfter(30)
    EnterEnableMode(switch1)
    data1 = SetCmd(switch1,'show wireless ap status')
    res1 = CheckLineList(data1,[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],IC=True)
if res1 != 0:
    IdleAfter(30)
    EnterEnableMode(switch1)
    data1 = SetCmd(switch1,'show wireless ap status')
    res1 = CheckLineList(data1,[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],IC=True)
if res1 != 0:
    IdleAfter(30)
    EnterEnableMode(switch1)
    data1 = SetCmd(switch1,'show wireless ap status')
    res1 = CheckLineList(data1,[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],IC=True)
if res1 != 0:
    IdleAfter(30)
    EnterEnableMode(switch1)
    data1 = SetCmd(switch1,'show wireless ap status')
    res1 = CheckLineList(data1,[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],IC=True)
#获取AP1，AP2的channel
EnterEnableMode(switch1)
data2 = SetCmd(switch1,'show wireless ap radio status',promotePatten='#')
SearchResult1 = re.search(ap1mac + '\s*(\d+)\s*(\d+)',data2,re.I)
SearchResult2 = re.search(ap2mac + '\s*(\d+)\s*(\d+)',data2,re.I)

#check

if None != SearchResult1:
    if '1' == SearchResult1.group(1).strip():
        Ap1channel_x = SearchResult1.group(2).strip()
        if '' != Ap1channel_x:
            printRes('Succeed:  AP1 Radio Channel '+ Ap1channel_x)
            res2 = 0
        else:
            printRes('Failed:  AP1 Radio Channel not right')
            res2 = 1
    else:
        res2 = 1
        printRes('Failed:  AP1 Radio not 1')
else:
    res2 = 1
    printRes('Failed: Get AP1 Radio Channel failed')
    
if None != SearchResult2:
    if '1' == SearchResult2.group(1).strip():
        Ap2channel_y = SearchResult2.group(2).strip()  
        if '' != Ap2channel_y:
            printRes('Succeed:  AP2 Radio Channel '+ Ap2channel_y)            
            res3 = 0
        else:
            printRes('Failed:  AP2 Radio Channel not right')
            res3 = 1      
    else:
        res3 = 1
        printRes('Failed:  AP2 Radio not 1')
else:
    res3 = 1
    printRes('Failed: Get AP2 Radio Channel failed')

#result
printCheckStep(testname, 'Step 1', res1,res2,res3)

################################################################################
#Step 2
#操作
#AC1上设置固定AP1的工作信道为y（y就是AP2目前的工作信道），后重起AP1
# AC1(config-wireless)#ap database <AP1MAC>
# AC1(config-ap)#radio 1 channel y
# AC1(config-ap)#end
# AC1#wireless ap reset <AP1MAC>
#
#预期
#AP1被AC1管理后，AC1上show wireless ap radio status 
#显示2个AP的“Radio Channel”依次为'1  y','1  y'
################################################################################

printStep(testname,'Step 2',\
          'Change AP1 Radio Channel to y',\
          'Reset AP1 and check the configuration')

res1=1

#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'radio 1 channel',Ap2channel_y)
printRes('Change AP1 Radio channel to '+ Ap2channel_y)

#重启AP1
RebootAp('AC',AC=switch1,MAC=ap1mac,AP=ap1)
IdleAfter(30)
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless ap radio status',promotePatten='#')

#check
res1 = CheckLineList(data1,[(ap1mac,'1',Ap2channel_y),(ap2mac,'1',Ap2channel_y)],IC=True)
if res1 != 0:
    IdleAfter(30)
    EnterEnableMode(switch1)
    data1 = SetCmd(switch1,'show wireless ap radio status',promotePatten='#')

    #check
    res1 = CheckLineList(data1,[(ap1mac,'1',Ap2channel_y),(ap2mac,'1',Ap2channel_y)],IC=True)
if res1 != 0:
    IdleAfter(30)
    EnterEnableMode(switch1)
    data1 = SetCmd(switch1,'show wireless ap radio status',promotePatten='#')

    #check
    res1 = CheckLineList(data1,[(ap1mac,'1',Ap2channel_y),(ap2mac,'1',Ap2channel_y)],IC=True)
if res1 != 0:
    IdleAfter(30)
    EnterEnableMode(switch1)
    data1 = SetCmd(switch1,'show wireless ap radio status',promotePatten='#')

    #check
    res1 = CheckLineList(data1,[(ap1mac,'1',Ap2channel_y),(ap2mac,'1',Ap2channel_y)],IC=True)
if res1 != 0:
    IdleAfter(30)
    EnterEnableMode(switch1)
    data1 = SetCmd(switch1,'show wireless ap radio status',promotePatten='#')

    #check
    res1 = CheckLineList(data1,[(ap1mac,'1',Ap2channel_y),(ap2mac,'1',Ap2channel_y)],IC=True)

#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#操作
#AC1上配置信道调整为周期调整，周期4分钟
# AC1(config)#wireless 
# AC1(config-wireless)#channel-plan bgn interval 4
#
#预期
#配置成功
################################################################################

printStep(testname,'Step 3',\
          'Config channel-plan interval to 4 minutes')

res1=1
#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'channel-plan bgn interval',Bgn_interval)
SetCmd(switch1,'channel-plan bgn mode interval')

data1 = SetCmd(switch1,'show running-config | include channel')

#check
res1 = CheckLineList(data1,[('channel-plan bgn interval',Bgn_interval), \
                            ('channel-plan bgn mode interval')],IC=True)

#result
printCheckStep(testname, 'Step 3',res1)

################################################################################
#Step 4
#操作
#一个调整周期后，AP2的信道调整为 'z'
#
#预期
#AC1上show wireless ap radio status 显示2个AP的“Radio Channel”依次为'1 y','1 z'
################################################################################

printStep(testname,"Step 4',\
          'Check if AP2 Radio Channel was adjusted to 'z' after a interval")

res1=res2=1

#operate
IdleAfter(int(Bgn_interval+2)*60)
IdleAfter(60)

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless ap radio status',promotePatten='#')

#check
res1 = CheckLine(data1,ap1mac,'1',Ap2channel_y,IC=True)
SearchResult  = re.search(ap2mac + '\s*1\s*(\d+)',data1)
if None != SearchResult:
    Ap2channel_z = SearchResult.group(1).strip()
    if ('' != Ap2channel_z) and (Ap2channel_z != Ap2channel_y):
        res2 = 0
        printRes('Succeed: AP2 Radio Channel change to z: '+ Ap2channel_z +' succeed')  
    else:
        res2 = 1
        printRes('Failed: AP2 Radio Channel change to z failed') 
else:
    res2 = 1
    printRes('Failed: Get AP2 Radio Channel failed')         

#result
printCheckStep(testname, 'Step 4',res1,res2)

################################################################################
#Step 5
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 5',\
          'Recover initial config')

#operate

# 清除channel-plan配置
EnterWirelessMode(switch1)
SetCmd(switch1,'no','channel-plan bgn interval')
SetCmd(switch1,'channel-plan bgn mode manual')

#还原channel
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'radio 1 channel','0')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap2mac)
SetCmd(switch1,'radio 1 channel','0')

#重启AP1,AP2
SetCmd(ap1,'reboot',timeout=1)
SetCmd(ap1,'y',timeout=1)
SetCmd(ap2,'reboot',timeout=1)
SetCmd(ap2,'y',timeout=1)
IdleAfter(Ap_reboot_time)

data = SetCmd(ap1,'\n',promoteStop=False,timeout=1)
if 0==CheckLine(data,'login'):
    SetCmd(ap1,Ap_login_name,promotePatten='Password',promoteTimeout=5)
    SetCmd(ap1,Ap_login_password)
data = SetCmd(ap2,'\n',promoteStop=False,timeout=1)
if 0==CheckLine(data,'login'):
    SetCmd(ap2,Ap_login_name,promotePatten='Password',promoteTimeout=5)
    SetCmd(ap2,Ap_login_password)

IdleAfter(Ac_ap_syn_time)
        
#end
printTimer(testname, 'End')