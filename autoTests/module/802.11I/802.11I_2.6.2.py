#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# 802.11I_2.6.2.py
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2020 Digital China Networks Co. Ltd
#
# Features:
# 2.6.2 非漫游关联成功后的处理:关联成功后,802.11n属性正确
# 测试描述：在关联AP的管理UWS上查看associated client表，该client是否支持802.11n（802.11n capable）属性正确
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.2.7
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 802.11I_2.6.2'
avoiderror(testname)
printTimer(testname,'Start','Test client that connect to ap with open-mode support 802.11n')

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
    #AC上show wireless client sta1mac status
    #预期
    #查看sta1支持802.11n
    ################################################################################
    printStep(testname,'Step 3',\
              'Check sta1 support 802.11n on AC1')
    res1=1
    # operate
    res1 = CheckSutCmd(switch1,'show wireless client '+sta1mac+' status',
                        check=[('802.11n Capable','Yes')],retry=10,waitflag=False)

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
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
CheckWirelessClientOnline(switch1,sta1mac,'offline')
#end
printTimer(testname, 'End')