#-*- coding: UTF-8 -*-#
#
#******************************************************************************
# waffirm_4.4.1.py - test case 4.4.1 of waffirm_new
#
# Author:  (jinpfb)
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Date: 2012-12-13 14:11:34
#
# Features:
# 4.4.1	集中转发模式下通过AC实现的二层隔离功能
# 测试目的：集中转发模式下通过AC实现的二层隔离功能
# 测试环境：见测试拓扑
# 测试描述：在集中转发方式，用户的二层隔离通过在ac上实现，实现的结果是隔离vlan下
#           的所有无线用户之间被隔离。AP能够隔离二层单播和广播
#
#*******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
#	  - zhangjxp RDM42383 2017.11.3 
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.4.1'
avoiderror(testname)
printTimer(testname,'Start','test L2 isolation in central switch mode via AC1')

################################################################################
#Step 1
#操作
#在AC1配置network1的SSID为test1，关联vlan4091。配置下发到AP1。
#
#预期
#配置下发成功
################################################################################
printStep(testname,'Step 1',
          'set network 1 ssid test1 and vlan 4091,',
          'apply ap profile to ap1,',
          'check config success.')
#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan '+Vlan4091)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

data1 = SetCmd(switch1,'show wireless network 1')

#check
res1 = CheckLine(data1,'Default VLAN',Vlan4091,IC=True)
res2 = CheckLine(data1,'SSID',Network_name1,IC=True)

#result
printCheckStep(testname, 'Step 1',res1,res2)

################################################################################
#Step 2
#操作
#将STA1和STA2均关联到AP1的网络test1。
#
#预期
#成功关联并获取192.168.91.X网段的IP地址。
################################################################################

printStep(testname,'Step 2',
          'STA1 and STA2 connect to network 1,',
          'STA1 and STA2 dhcp and get 192.168.91.x ip')

sta1_ipv4 = ''
sta2_ipv4 = ''

res1=res2=res3=res4=1

#operate
#STA1,STA2关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap1mac_lower)
IdleAfter(10)

#获取STA1,STA2的地址
sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
res3 = sta1_ipresult['res']

sta2_ipresult = GetStaIp(sta2,checkippool=Dhcp_pool1)
sta2_ipv4 = sta2_ipresult['ip']
res4 = sta2_ipresult['res']

#result
printCheckStep(testname, 'Step 2',res1,res2,res3,res4)

# 如果客户端无法获取IP，则不执行后续步骤
keeponflag = res3 + res4
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 3
    #操作
    #STA1和STA2互ping
    #
    #预期
    #能够 ping 通
    ################################################################################

    printStep(testname,'Step 3',
              'STA1 and STA2 ping each other',
              'Check if succeed')

    res1=res2=1

    #operate
    res1 = CheckPing(sta1,sta2_ipv4,mode='linux')
    res2 = CheckPing(sta2,sta1_ipv4,mode='linux')   

    #check

    #result
    printCheckStep(testname,'Step 3',res1,res2)

    ################################################################################
    #Step 4 
    # 操作
    # 在STA1上通过CommView发送广播报文
    #
    # 预期
    # STA2能够收到STA1的广播包
    ################################################################################

    printStep(testname,'Step 4',
              'STA1 send broadcast packets via commview,',
              'STA2 can receive broadcast packets from STA1')

    res1=-1
    #operate
    res = ConnectDsendWireless(testerip_sta1)

    if 0==res:
        SetDsendStreamWireless(Port=testerp1_sta1,PortTypeConfig='0',StreamMode='0',StreamRateMode='pps',StreamRate='50',
                               SouMac = sta1mac,DesMac='ff-ff-ff-ff-ff-ff',EthernetTypeNum = 'ffff')
        StartTransmitWireless(testerp1_sta1)
        DisconnectDsendWireless()
    res = ConnectDsendWireless(testerip_sta2)
    if 0==res:
        StartDsendCaptureWireless(Port=testerp1_sta2)
        IdleAfter(Rate_stable_wait_time)
        StopDsendCaptureWireless(testerp1_sta2)   
          
        res1 = CheckDsendCaptureStreamWireless(testerp1_sta2,DstMac='ff-ff-ff-ff-ff-ff',SrcMac=sta1mac)
        printRes('Capture number: '+ str(res1))    
        DisconnectDsendWireless()

    #check
    res1 = 0 if 0 < int(res1) else 1

    #result
    printCheckStep(testname, 'Step 4',res1)

    res = ConnectDsendWireless(testerip_sta1)
    if 0==res:
        StopTransmitWireless(testerp1_sta1)
        DisconnectDsendWireless()
        
    ################################################################################
    #Step 5
    #
    #操作
    #在ac1上配置对于4091vlan进行隔离，l2tunnel station-isolation allowed vlan add 4091. 
    #STA1和STA2互ping
    #
    #预期
    #Sta1和sta2不能ping通
    ################################################################################

    printStep(testname,'Step 5',
              'Enable L2 isolation on AC1,',
              'STA1 and STA2 ping each other')

    res1=res2=res3=1
    #operate
    EnterWirelessMode(switch1)
    SetCmd(switch1,'l2tunnel station-isolation allowed vlan add',Vlan4091)
    data1 = SetCmd(switch1,'show running-config | include station',timeout=5)
    IdleAfter(10)

    #check
    res1 = CheckLine(data1,'l2tunnel station-isolation allowed vlan',Vlan4091,IC=True,RS=True)
    res2 = CheckPing(sta1,sta2_ipv4,mode='linux')
    res3 = CheckPing(sta2,sta1_ipv4,mode='linux')   
    res2 = 0 if 0 != res2 else 1
    res3 = 0 if 0 != res3 else 1

    #result
    printCheckStep(testname, 'Step 5',res1,res2,res3)

    ################################################################################
    #Step 6 
    # 操作
    # 在STA1上通过CommView发送广播报文
    #
    # 预期
    # STA2收不到STA1的广播包
    ################################################################################

    printStep(testname,'Step 6',
              'STA1 send broadcast packets via commview,',
              'STA2 cannot receive broadcast packets from STA1')

    res1=-1
    #operate
    res = ConnectDsendWireless(testerip_sta1)

    if 0==res:
        SetDsendStreamWireless(Port=testerp1_sta1,PortTypeConfig='0',StreamMode='0',StreamRateMode='pps',StreamRate='50',
                               SouMac = sta1mac,DesMac='ff-ff-ff-ff-ff-ff',EthernetTypeNum = 'ffff')
        StartTransmitWireless(testerp1_sta1)
        DisconnectDsendWireless()
    res = ConnectDsendWireless(testerip_sta2)
    if 0==res:
        StartDsendCaptureWireless(Port=testerp1_sta2)
        IdleAfter(Rate_stable_wait_time)
        StopDsendCaptureWireless(testerp1_sta2)   
          
        res1 = CheckDsendCaptureStreamWireless(testerp1_sta2,DstMac='ff-ff-ff-ff-ff-ff',SrcMac=sta1mac)
        printRes('Capture number: '+ str(res1))   
        DisconnectDsendWireless()

    #check

    #result
    printCheckStep(testname, 'Step 6',res1)

    res = ConnectDsendWireless(testerip_sta1)
    if 0==res:
        StopTransmitWireless(testerp1_sta1)
        DisconnectDsendWireless()

    ################################################################################
    #Step 7
    #
    #操作
    #在ac1上关闭对于4091vlan的二层隔离，l2tunnel station-isolation allowed vlan remove 4091. 
    #STA1和STA2互ping
    #
    #预期
    #Sta1和sta2能ping通
    ################################################################################

    printStep(testname,'Step 7',
              'Disable L2 isolation on AC1,',
              'STA1 and STA2 ping each other')

    res1=res2=res3=1
    #operate
    EnterWirelessMode(switch1)
    SetCmd(switch1,'l2tunnel station-isolation allowed vlan remove',Vlan4091)
    data1 = SetCmd(switch1,'show running-config','|','include','station')
    IdleAfter(20)
    CheckPing(sta1,sta2_ipv4,mode='linux')
    CheckPing(sta2,sta1_ipv4,mode='linux')   

    #check
    res1 = CheckLine(data1,'l2tunnel station-isolation allowed vlan',Vlan4091,IC=True,RS=True)
    res1 = 0 if 0 != res1 else 1
    res2 = CheckPing(sta1,sta2_ipv4,mode='linux')
    res3 = CheckPing(sta2,sta1_ipv4,mode='linux')   

    #result
    printCheckStep(testname, 'Step 7',res1,res2,res3)

    ################################################################################
    #Step 8 
    # 操作
    # 在STA1上通过CommView发送广播报文
    #
    # 预期
    # STA2能够收到STA1的广播包
    ################################################################################

    printStep(testname,'Step 8',
              'STA1 send broadcast packets via commview,',
              'STA2 can receive broadcast packets from STA1')

    res1=-1
    #operate
    res = ConnectDsendWireless(testerip_sta1)

    if 0==res:
        SetDsendStreamWireless(Port=testerp1_sta1,PortTypeConfig='0',StreamMode='0',StreamRateMode='pps',StreamRate='50',
                               SouMac = sta1mac,DesMac='ff-ff-ff-ff-ff-ff',EthernetTypeNum = 'ffff')
        StartTransmitWireless(testerp1_sta1)
        DisconnectDsendWireless()
    res = ConnectDsendWireless(testerip_sta2)
    if 0==res:
        StartDsendCaptureWireless(Port=testerp1_sta2)
        IdleAfter(Rate_stable_wait_time)
        StopDsendCaptureWireless(testerp1_sta2)   
          
        res1 = CheckDsendCaptureStreamWireless(testerp1_sta2,DstMac='ff-ff-ff-ff-ff-ff',SrcMac=sta1mac)
        print 'Capture number: '+ str(res1)
        DisconnectDsendWireless()

    #check
    res1 = 0 if 0 < int(res1) else 1

    #result
    printCheckStep(testname, 'Step 8',res1)

    res = ConnectDsendWireless(testerip_sta1)
    if 0==res:
        StopTransmitWireless(testerp1_sta1)
        DisconnectDsendWireless()

################################################################################
#Step 9
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 9',
          'Recover initial config')

#operate
##pc解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

EnterNetworkMode(switch1,'1')
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan ' + Vlan4091)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

#end
printTimer(testname, 'End')