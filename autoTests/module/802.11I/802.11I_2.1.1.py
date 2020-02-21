#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# 802.11I_2.1.1.py
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2020 Digital China Networks Co. Ltd
#
# Features:
# 2.1.1 OPEN方式client认证成功
# 测试描述：无线系统采用开放认证方式时，client使用OPEN方式能够认证成功
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.31
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 802.11I_2.1.1'
avoiderror(testname)
printTimer(testname,'Start','test wireless client connect to network with open-mode')

################################################################################
#Step 1
#操作
#AC1的network1采用默认的安全接入方式none，即open方式。配置下发到AP1。
#wireless ap profile apply 1
#预期
#配置下发成功。
################################################################################
printStep(testname,'Step 1',\
          'set network1 access mode open as default,',\
          'apply ap profile1 to ap,',\
          'check config success.')
#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'security mode none')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

#check
data = SetCmd(switch1,'show wireless network 1')
res1 = CheckLine(data,'Security Mode\.+\s*None')
#result
printCheckStep(testname, 'Step 1',res1)
################################################################################
#Step 2
#操作
#STA1关联test1。
#
#预期
#成功关联，并获取192.168.91.X网段的IP地址。
# Show wireless client summery可以看到sta1，IP地址的网段正确。
################################################################################
printStep(testname,'Step 2',\
          'STA1 connect to test1',\
          'STA1 get a 192.168.91.X ipaddress'\
          'show client summery can see client')
res1=res2=0
# operate
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='open',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res1==0:
    res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')

printCheckStep(testname, 'Step 2',res1,res2)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 3
    #操作
    #在STA1上ping Radius_server
    #
    #预期
    #能够ping通。
    ################################################################################
    printStep(testname,'Step 3',\
              'STA1 ping Radius_server',\
              'ping success.')
    res1=1
    # operate
    res1 = CheckPing(sta1,Radius_server,mode='linux')

    printCheckStep(testname, 'Step 3',res1)

################################################################################
#Step 4
#操作
#客户端STA1断开与test1的连接。
#
#预期
#客户端下线成功。Show wireless client summery不能看到sta1。
################################################################################
printStep(testname,'Step 4',\
          'STA1 close the connecting with network1,',\
          'show wireless client summary and no STA1 client.')
res1=res2=1
# operate
res1 = WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

res2 = CheckWirelessClientOnline(switch1,sta1mac,'offline')

printCheckStep(testname, 'Step 4',res1,res2)


#end
printTimer(testname, 'End')