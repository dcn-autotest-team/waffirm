#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.1.py 
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.1	基本环境检查
# 测试目的：检查自动确认测试环境符合自动化测试要求
# 测试描述：
# 1.	初始化完成后，检查AP1和AP2是否能够正常上线
# 2.	客户端STA1和STA2可以搜素到到网络test1和test2并能够关联成功
# 测试环境：见测试环境拓扑图1
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.18
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase externalportal_4.1.1'
avoiderror(testname)
printTimer(testname,'Start','Basic Configuration check')

###############################################################################
#Step 1
#操作
# 初始化完成后，检查AP1和AP2是否正常上线
# AC1上通过命令show wireless  ap status查看AP1和AP2的列表
#预期
# AP1和AP2成功被AC1管理,显示两条记录为
# MAC Address为AP1MAC，IP Address为AP1IP，Profile显示为1
# MAC Address为AP2MAC，IP Address为AP2IP，Profile显示为2
################################################################################
printStep(testname,'Step 1','check ac managed ap1 and ap2')
#operate
res1=CheckSutCmd(switch1,'show wireless ap status', \
                check=[(ap1mac,Ap1_ipv4,'1','Managed','Success'),(ap2mac,Ap2_ipv4,'2','Managed','Success')], \
                waittime=5,retry=1,interval=5,IC=True)
#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#操作
#客户端STA1连接到网络test1
#
#预期
#关联成功。客户端获取192.168.91.X网段的IP地址。
################################################################################

printStep(testname,'Step 2',\
                    'STA1 connect to test1')
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
#result
printCheckStep(testname, 'Step 2',res1)
################################################################################
#Step 3
#操作
#客户端STA2连接到网络test2
#
#预期
#关联成功。客户端获取192.168.92.X网段的IP地址。
################################################################################

printStep(testname,'Step 3',\
                    'STA2 connect to test2')
res1=res2=1
#operate
#STA2关联 network2
res1 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,checkDhcpAddress=Netcard_ipaddress_check2,bssid=ap1mac_type1_network2)
#result
printCheckStep(testname, 'Step 3',res1)
################################################################################
#Step 4
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 4',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)
#end
printTimer(testname, 'End')