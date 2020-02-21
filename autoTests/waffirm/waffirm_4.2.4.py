#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.2.4.py - test case 4.2.4 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
# 
# Date 2017-5-15 14:37:33
#
# Features:
# 4.2.1	DFS功能测试
# 测试目的：AP的DFS功能
# 测试环境：同测试拓扑
# 测试描述：AP检测到5G频段的工作信道有雷达信号，AP会自动切换到其它信道。（AP1的MAC地址为AP1MAC）
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

testname = 'TestCase 4.2.4'
avoiderror(testname)
printTimer(testname,'Start','test DFS function')

################################################################################
#Step 1
#操作
# AC1配置国家码为CN
#AP1重新上线
#预期
#等待2分钟后，show wireless ap status显示AP1MAC的AP的“Status”为“Managed Success”
# （注：更改国家码后AP需要重新上线）

################################################################################
printStep(testname,'Step 1')

res1=1
#operate

#AC1配置国家码为CN
EnterWirelessMode(switch1)
SetCmd(switch1,'country-code cn')
SetCmd(switch1,'channel enhance enable')
i = 1
while i<13:
	EnterEnableMode(switch1)
	data1 = SetCmd(switch1,'show wireless ap status')
	res1 = CheckLine(data1,ap1mac,Ap1_ipv4,'1','Managed','Success',IC=True)
	res2 = CheckLine(data1,ap2mac,Ap2_ipv4,'2','Managed','Success',IC=True)
	if res1 == 0 and res2 == 0:
		break
	IdleAfter('10')
	i = i + 1

#result
printCheckStep(testname, 'Step 1', res1,res2)


################################################################################
#Step 2
#操作
# AC1上固定AP1的5G信道为52
#
#预期
#等待90秒后，AC1上show wireless ap radio status 显示AP1MAC的AP的5G信道为52
# （注：配置DFS信道后，有60秒的等待）
################################################################################
printStep(testname,'Step 2')

res1=1
#operate
#check
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap channel set '+ap1mac+' radio 2 52')
# AP1重新上线
SetCmd(ap1,'\n')
SetCmd(ap1,'set managed-ap mode down')
IdleAfter(5)
SetCmd(ap1,'set managed-ap mode up')
IdleAfter(20)
i = 1
while i<10:
	EnterEnableMode(switch1)
	data1 = SetCmd(switch1,'show wireless ap status')
	res = CheckLine(data1,ap1mac,Ap1_ipv4,'1','Managed','Success',IC=True)
	if res == 0:
		break
	IdleAfter('5')
	i = i + 1

i=0
while i<30:
	data1 = SetCmd(switch1,'show wireless ap '+ap1mac+' radio status')
	res1 = CheckLine(data1,'2\s+52\s+\d+\s+\d+')
	if res1==0:
		break
	IdleAfter(5)
	i=i+1
#result
printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#STA1关联AP1的5G radio
#
#预期
#STA1关联成功
################################################################################

printStep(testname,'Step 3')

res1=res2=res3=res4=1
#operate
for tmpCounter in xrange(0,10):
    StaScanSSID(sta1,Netcard_sta1)
    IdleAfter('5')
    data = SetCmd(sta1,'wpa_cli -i '+ Netcard_sta1 +' scan_results')
    if 0 == CheckLine(data,ap1mac_lower_5g,Network_name1):
        break
    
# res1 = CheckLine(data,ap1mac_lower_5g,Network_name1)
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower_5g)
data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
res2 = CheckLine(data1,'inet.+?'+Netcard_ipaddress_check,IC=True)
res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
#check
#result
printCheckStep(testname, 'Step 3',res1,res2,res3)

################################################################################
#Step 4（修改）
#操作
#AP1上执行以下命令，模拟52信道有雷达信号：
# WLAN-AP1#iwpriv wifi1 dfs_debug 1
#预期
#AC1上show wireless ap <AP1MAC>
# radio 2 radar status显示52信道的“Radar Detected Status”为“Yes”
# 修改为
#操作
#设置AP2静态信道为52
#预期
#AC1上show wireless ap <AP1MAC>
# radio 2 radar status显示52信道的“Radar Detected Status”为“Yes”
################################################################################

printStep(testname,'Step 4')

res=1
#operate
RebootAp(AP=ap2)
EnterEnableMode(switch1)
i=0
while i<20:
	data = SetCmd(switch1,'show wireless ap status')
	res = CheckLine(data,ap2mac,Ap2_ipv4,'2','Managed','Success',IC=True)
	if res == 0:
		break
	IdleAfter('5')
	i = i + 1
SetCmd(ap2,'\n')
# SetCmd(ap1,'iwpriv wifi1 dfs_debug 1')
SetCmd(ap2,'set radio wlan1 static-channel 52')
for i in range(10):
	IdleAfter(5)
	data1 = SetCmd(switch1,'show wireless ap '+ap2mac+' radio status')
	res1 = CheckLine(data1,'2\s+52\s+\d+\s+\d+')
	if res1 == 0:
		break
		
# AP1重新上线
# SetCmd(ap1,'\n')
# SetCmd(ap1,'set managed-ap mode down')
# SetCmd(ap1,'set managed-ap mode up')
# IdleAfter(20)
IdleAfter(5)
i=0
while i<24:
	data = SetCmd(switch1,'show wireless ap '+ap1mac+' radio 2 radar status')
	res2 = CheckLine(data,'52\s+Yes\s+Yes',IC=True)
	if res2 == 0:
		break
	IdleAfter(5)
	i=i+1
#result
printCheckStep(testname, 'Step 4',res1,res2)

################################################################################
#Step 5
#操作
#等待90秒
#
#预期
#AC1上show wireless ap radio status 显示AP1MAC的AP的5G信道切换到其它信道
# （注：选择DFS信道的话，有60秒的等待）
################################################################################
printStep(testname,'Step 5')
res1=1
#operate
i=0
while i<24:
	data1 = SetCmd(switch1,'show wireless ap '+ap1mac+' radio status')
	res1 = CheckLine(data1,'2\s+52\s+\d+\s+\d+')
	res1=0 if res1 != 0 else 1
	if res1 == 0:
		break
	IdleAfter(5)
	i=i+1
#result
printCheckStep(testname, 'Step 5',res1)

################################################################################
#Step 6
#操作
#STA1关联AP1的5G radio
#
#预期
#STA1关联成功
################################################################################

printStep(testname,'Step 6')

res1=res2=res3=res4=1
#operate
for tmpCounter in xrange(0,20):
    StaScanSSID(sta1,Netcard_sta1)
    IdleAfter('5')
    data = SetCmd(sta1,'wpa_cli -i '+ Netcard_sta1 +' scan_results')
    if 0 == CheckLine(data,ap1mac_lower_5g,Network_name1):
        break
res1 = CheckLine(data,ap1mac_lower_5g,Network_name1)
res2 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower_5g)
data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
res3 = CheckLine(data1,'inet.+?'+Netcard_ipaddress_check,IC=True)
res4 = CheckPing(sta1,pc1_ipv4,mode='linux')
#check
#result
printCheckStep(testname, 'Step 6',res1,res2,res3,res4)


################################################################################
#Step 7
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 7',
          'Recover initial config for switches.')

#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'channel enhance disable')
SetCmd(switch1,'no country-code')
SetCmd(ap2,'\n')
SetCmd(ap2,'set radio wlan1 channel-policy best')
IdleAfter(1)
RebootAp('AP',AP=ap1)
i = 1
while i<13:
	EnterEnableMode(switch1)
	data1 = SetCmd(switch1,'show wireless ap status')
	res1 = CheckLine(data1,ap1mac,Ap1_ipv4,'1','Managed','Success',IC=True)
	if res1 == 0:
		break
	IdleAfter('10')
	i = i + 1
printTimer(testname, 'End')