#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.13.py - test case 4.13 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Date: 2013-09-23 10:41:12
#
# Copyright (c) 2004-2013 Digital China Networks Co. Ltd
#
# Features:
# 4.13	1+1备份功能测试（手工测试）
# 测试目的：测试无线控制器1+1热备份的基本功能。
# 测试环境：同测试拓扑
# 测试描述：AC1与AC2构成备份组。当AC1出现故障，AC2可以代替AC1管理AP。
#         当AP1故障恢复后能够重新管理AP，而AC2恢复为备份设备。要求AC
#         之间发生切换时，数据基本上没有丢失
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

testname = 'TestCase 4.13'
printTimer(testname,'Start','1+1 backup ')

################################################################################
#Step 1
#操作
#在AC1上面配置network 1的SSID为test1，关联vlan 4092。配置下发到AP1。
#配置下发成功，AC1管理了AP1。
################################################################################
printStep(testname,'Step 1',\
          'set ssid test1 vlan 4092')

res1=res2=0
#operate


#check
#result
printCheckStep(testname, 'Step 1',res1,res2)

################################################################################
#Step 2
#操作
#通过配置推送，将AC1的无线配置推送到AC2。手动保证AC2和AC1的vlan配置相同。
#预期
#无线配置推送成功（通过show run比对，无线配置相同）。
################################################################################
printStep(testname,'Step 2',\
          'Enable L3 multicast protocol on S1 and AC1')

res1=0

#result
printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#STA1关联到网络test1。
#
#预期
#STA1关联成功，获取192.168.91.X网段的IP地址。
################################################################################
printStep(testname,'Step 3',\
          'STA1 connect to network 1,',\
          'STA1 dhcp and get 192.168.91.X ip address.')

res1=res2=1
#operate
sta1_ipv4 = ''

#STA1关联 network 1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
IdleAfter(10)

#STA1获取地址
data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)

#check
if None != SearchResult1:
    sta1_ipv4 = SearchResult1.group(1)
    if None != re.search(Dhcp_pool1,sta1_ipv4):
        printRes('STA1 ip address: ' + sta1_ipv4)
        res2 = 0  
else:
    res2 = 1
    printRes('Failed: Get ipv4 address of STA1 failed')

#result
printCheckStep(testname,'Step 3',res1,res2)

################################################################################
#Step 4
#操作
#STA1 ping pc1 –t (连续ping)
#
#预期
#可以ping通
################################################################################
printStep(testname,'Step 4',\
          'Sta1 ping pc1')

res1 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')

#result
printCheckStep(testname, 'Step 4',res1)
        
################################################################################
#Step 5
#操作
#分别在AC1和AC2配置冗备功能。AC1为master，AC2为backup：
#switch-redundancy master 1.1.1.1 backup 1.1.1.2
#
#预期
#通过show wireless switch redundancy status查看冗备配置正确。
################################################################################
printStep(testname,'Step 5',\
          'get igmp-snooping-fwd on AP1,',\
          'check there is multicast table of client with some args.')
          
res1=1
#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'switch-redundancy master ' + StaticIpv4_ac1 + ' backup ' + StaticIpv4_ac2)
SetCmd(switch1,'discovery ip-list ' + StaticIpv4_ac2)
EnterWirelessMode(switch2)
SetCmd(switch2,'switch-redundancy master ' + StaticIpv4_ac1 + ' backup ' + StaticIpv4_ac2)
SetCmd(switch2,'discovery ip-list ' + StaticIpv4_ac1)

#wait for cluster created
IdleAfter(180)
data1 = SetCmd(switch1,'show wireless switch redundancy status',timeout=3)
res1 = CheckLineList(data1,[(StaticIpv4_ac1 + '\(Active\)')],IC=True)

#config push
EnterEnableMode(switch1)
SetCmd(switch1,'write',timeout=1)
SetCmd(switch1,'y',timeout=1)
IdleAfter(20)

#check

#result
printCheckStep(testname, 'Step 5',res1)

################################################################################
#Step 6
#操作
#断开AC1和S3的网络连接，
#
#预期
#AC1和AC2之间发生主备切换。AC2成为master。通过show wireless switch redundancy status查看冗备状态正确。
#STA 1 和pc1的ping包丢1-2个。
################################################################################
printStep(testname,'Step 6',\
          'Disconnect connection between ac1 and s3')
          
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'shutdown')
IdleAfter(60)
res1 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
data1 = SetCmd(switch1,'show wireless switch redundancy status',timeout=3)
res2 = CheckLineList(data1,[(StaticIpv4_ac2 + '\(Active\)')],IC=True)
#check

#result
printCheckStep(testname, 'Step 6',res1,res2)
################################################################################
#Step 7
#操作
#在S2上面查看AP和Client相关的信息。
#
#预期
#AP1和AP2关联在AC2。STA1和STA2不会掉线，仍然与原来的AP关联。
################################################################################
printStep(testname,'Step 7',\
          'Check ap and client info on s2')

#operate

data1 = SetCmd(switch2,'show wireless ap status')
res1 = CheckLineList(data1,[(re.sub(':','-',ap1mac_lower),'Success')],IC=True)

data1 = SetCmd(switch2,'show wireless client status')
res2 = CheckLineList(data1,[(re.sub(':','-',sta1mac))],IC=True)

#check
#result
printCheckStep(testname, 'Step 7',res1,res2)

################################################################################
#Step 8
#操作
#AC1恢复和S3的网络连接，等待3分钟。
#
#预期
#AC1和AC2重新发生主备切换。AC1仍然为master。通过show wireless switch redundancy status查看冗备配置正确。
#STA 1 和pc1的ping包丢1-2个。
################################################################################
printStep(testname,'Step 8',\
          'Reconnect ac1 and s3')

EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'no shutdown',promoteTimeout=30)
IdleAfter(60)
res1 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')

data = SetCmd(switch1,'show wireless switch redundancy status')

#check

#result
printCheckStep(testname, 'Step 8',res1)

################################################################################
#Step 9
#操作
#在AC1上面查看AP和Client相关的信息。
#
#预期
#AP1和AP2关联在AC1。STA1和STA2不会掉线，仍然与原来的AP关联。
################################################################################
printStep(testname,'Step 9',\
          'Check client info on ac1')
          
data1 = SetCmd(switch1,'show wireless ap status')
res1 = CheckLineList(data1,[(re.sub(':','-',ap1mac_lower),'Success')],IC=True)

data1 = SetCmd(switch1,'show wireless client status')
res2 = CheckLineList(data1,[(re.sub(':','-',sta1mac))],IC=True)

#check

#result
printCheckStep(testname, 'Step 9',res1,res2)

################################################################################
#Step 10
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 10',\
          'Recover initial config for switches.')
#operate
##解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

EnterWirelessMode(switch1)
SetCmd(switch1,'no switch-redundancy ')
EnterWirelessMode(switch2)
SetCmd(switch2,'no switch-redundancy ')

#RDM37511
EnterWirelessMode(switch2)
SetCmd(switch2,'peer-group 2')
IdleAfter(5)
SetCmd(switch2,'peer-group 1')

SetCmd(switch1,'no discovery ip-list ' + StaticIpv4_ac2)
SetCmd(switch2,'no discovery ip-list ' + StaticIpv4_ac1)

#下发配置
# WirelessApProfileApply(switch1,'1')
# IdleAfter(Ac_ap_syn_time)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#end
printTimer(testname, 'End')