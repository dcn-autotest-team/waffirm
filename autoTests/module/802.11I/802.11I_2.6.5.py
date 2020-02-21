#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# 802.11I_2.6.5.py
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2020 Digital China Networks Co. Ltd
#
# Features:
# 2.6.5 非漫游关联成功后的处理:关联成功后,client和UWS对应关系正确
# 测试描述：在关联AP的管理UWS上查看UWS-Client Mapping表，该client和UWS的对应关系正确
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.2.7
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 802.11I_2.6.5'
avoiderror(testname)
printTimer(testname,'Start','Test SSID-Client Mapping')

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
# step1配置与初始化配置相同，不需要单独下发配置
data = SetCmd(switch1,'show wireless network 1')
#result
printCheckStep(testname, 'Step 1',0)
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
          'STA1 get a 192.168.91.X ipaddress')

# operate
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='open',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)

printCheckStep(testname, 'Step 2',res1)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 3
    #操作
    #AC上查看UWS-Client Mapping表
    #预期
    #该client和UWS的对应关系正确
    ################################################################################
    printStep(testname,'Step 3',\
              'show wireless client status switch ac1_wireless_ip on AC1',
              'sta1\'s ssid is in list')
    res1=1
    # operate
    res1 = CheckSutCmd(switch1,'show wireless client status switch '+StaticIpv4_ac1,
                        check=[(StaticIpv4_ac1,sta1mac)],retry=10,waitflag=False)

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

# operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
CheckWirelessClientOnline(switch1,sta1mac,'offline')

#end
printTimer(testname, 'End')