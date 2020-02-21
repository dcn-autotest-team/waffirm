#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.2.1.py - test case 4.2.1 of waffirm_new
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
# 4.2.1	静态信道调整功能
# 测试目的：测试通过静态配置的方式为AP指定工作信道
# 测试环境：同测试拓扑
# 测试描述：AP手动设置信道后工作正常，客户端能够正常关联。
#
#*******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
#     - zhangjxp 2017.11.10 RDM50304 修改step2、5
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
#     - zhangjxp 2018.3.21 RDM50803 修改step2、5
#*******************************************************************************

#Package

#Global Definition
 
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.2.1'
avoiderror(testname)
printTimer(testname,'Start','test static-channel adjust function')

################################################################################
#Step 1
#操作
# AC1上为AP1设定工作信道为channel 1，AC1(config-wireless)#ap database <AP1MAC>
# AC1(config-ap)#radio 1 channel 1
#
#预期
#配置成功
################################################################################
printStep(testname,'Step 1',
          'AC1 set channel 1 for AP1',
          'check the configuration')

res1=1
#operate

#关闭channel auto
EnterApProMode(switch1,1)
SetCmd(switch1,'radio 1')
SetCmd(switch1,'no channel auto')
#设定工作信道为 channel 1
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'radio 1 channel 1')

data1 = SetCmd(switch1,'show running-config current-mode',timeout=5)
#check

res1 = CheckLineList(data1,[('ap database',ap1mac),('radio 1 channel 1')],IC=True)

#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#操作
# 重起AP1
# WLAN-AP# reboot
#
#预期
#AP1重起后被AC1管理。show wireless ap radio status显示AP1的“Radio Channel”为“1     1”
################################################################################
printStep(testname,'Step 2',
          'Reboot AP1',
          'Check if AC1 managed AP1 and channel of AP1')

res1=res2=1

#operate
RebootAp('AP',AP=ap1,apcmdtype=Ap1cmdtype)
EnterEnableMode(switch1)
for i in range(20):
	data1 = SetCmd(switch1,'show wireless ap status')
	data2 = SetCmd(switch1,'show wireless ap radio status')
	res1 = CheckLine(data1,ap1mac,'Managed','Success',IC=True)
	res2 = CheckLine(data2,ap1mac,'\s+1\s+1\s+',RS=True)
	if res1 == 0 and res2 == 0:
		break
	else:
		IdleAfter(5)
#result
printCheckStep(testname, 'Step 2', res1,res2)

################################################################################
#Step 3
#操作
#STA1关联网络test1
#
#预期
#成功关联并获取192.168.91.X网段的IP地址。
################################################################################

printStep(testname,'Step 3',
          'STA1 connect to network1',
          'STA1 get 192.168.91.X address.')

res1=res2=1
#operate
IdleAfter(30)
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
data2 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
res2 = CheckLine(data2,'inet.+?'+Netcard_ipaddress_check,IC=True)
#check

#result
printCheckStep(testname, 'Step 3',res1,res2)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res2
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 4
    #操作
    #在STA1上ping PC1
    #
    #预期
    #能够ping通。
    ################################################################################

    printStep(testname,'Step 4',
              'STA1 ping PC1',
              'STA1 can ping PC1 success.')

    res1=res2=1
    #operate

    #默认采用集中式转发，pc1 已配置默认路由
    res1 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res2 = WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

    ##检查是否已经分配ip
    data = SetCmd(switch1,'show ip dhcp binding')
    res = CheckLine(data,sta1mac_upcase)
    if 0==res:
        EnterEnableMode(switch1)
        SetCmd(switch1,'clear ip dhcp binding all')
        IdleAfter(Ac_ap_syn_time)

    #result
    printCheckStep(testname, 'Step 4',res1,res2)

################################################################################
#Step 5
#操作
#在AC1上面调整AP1的工作信道为channel 6并下发profile 1给AP1。
##Ap database AP1mac
##Radio 1 channel 6
##Wireless ap profile apply 1
#
#预期
#设置成功，在UWS上面show wireless ap radio status查看AP1工作信道为channel 6。
################################################################################
printStep(testname,'Step 5',
          'set ap1 channel 6',
          'apply ap profile 1 to ap 1',
          'check config success.')

#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'radio 1 channel 6')

#重启AP1
RebootAp('AP',AP=ap1,apcmdtype=Ap1cmdtype)
for i in range(20):
	data1 = SetCmd(switch1,'show wireless ap status')
	data2 = SetCmd(switch1,'show wireless ap radio status')
	res1 = CheckLine(data1,ap1mac,'Managed','Success',IC=True)
	res2 = CheckLine(data2,ap1mac,'1','6',RS=True)
	if res1 == 0 and res2 == 0:
		break
	else:
		IdleAfter(5)
		
#result
printCheckStep(testname, 'Step 5',res1,res2)

################################################################################
#Step 6
#操作
#STA1关联网络test1
#
#预期
#成功关联并获取192.168.91.X网段的IP地址。
################################################################################

printStep(testname,'Step 6',
          'STA1 connect to network1',
          'connect success and STA1 get 192.169.91.X ipaddress.')

res1=res2=1

#operate
IdleAfter(30)
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
data2 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
res2 = CheckLine(data2,'inet.+?',Netcard_ipaddress_check,IC=True)

#check

#result
printCheckStep(testname, 'Step 6',res1,res2)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res2
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 7
    #操作
    #在STA1上ping PC1
    #
    #预期
    #能够ping通
    ################################################################################

    printStep(testname,'Step 7',
              'STA1 ping PC1',
              'STA1 ping PC1 success.')

    res1=1
    #operate

    # ping操作  
    res1 = CheckPing(sta1,pc1_ipv4,mode='linux')

    #result
    printCheckStep(testname, 'Step 7',res1)

################################################################################
#Step 8
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 8',
          'Recover initial config for switches.')

#operate

##解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

##检查是否已经分配ip
data = SetCmd(switch1,'show ip dhcp binding')
res = CheckLine(data,sta1mac_upcase)
if 0==res:
    EnterEnableMode(switch1)
    SetCmd(switch1,'clear ip dhcp binding all')
    IdleAfter(Ac_ap_syn_time)

#还原channel
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'radio 1 channel 0')

#打开channel auto
EnterApProMode(switch1,1)
SetCmd(switch1,'radio 1')
SetCmd(switch1,'channel auto')

WirelessApProfileApply(switch1,'1')

#重启AP1
RebootAp('AP',AP=ap1,apcmdtype=Ap1cmdtype)

#end
printTimer(testname, 'End')