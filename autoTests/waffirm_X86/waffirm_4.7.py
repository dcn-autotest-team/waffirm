#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.7.py - test case 4.7 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Date: 2013-1-23 10:41:12
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 4.7	AP IGMP Snooping功能测试
# 测试目的：测试AP上面的IGMP Snooping以及M2U功能。
# 测试环境：同测试拓扑
# 测试描述：AP上面启用IGMP Snoopning功能以后，能够实现对客户端的组播点播以及组播转单播。
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

testname = 'TestCase 4.7'
printTimer(testname,'Start','test igmp snooping of AP')

################################################################################
#Step 1
#操作
#在AC1上面无线全局使能ap igmp Snooping，并使能vap0下面的igmp snooping功能，配置下发AP1。
##DCWS-6028(config)#wireless 
##DCWS-6028(config-wireless)#igmp snooping 
##DCWS-6028(config-wireless)#network 1
##DCWS-6028(config-network)#igmp snooping m2u 
##DCWS-6028(config-network)#
##DCWS-6028#wireless ap profile apply 1
#
#预期
#Show run查看无线全局的igmp snooping已经使能，show wireless network 1显示network 1的m2u功能也已经使能。
################################################################################
printStep(testname,'Step 1',\
          'enable igmp snooping,',\
          'enable igmp snooping m2u,',\
          'apply ap profile 1 to ap,',\
          'show run and check igmp snooping enabled, show wireless network 1 check m2u enabled.')

res1=res2=1
#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'igmp snooping')
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'igmp snooping m2u')

EnterConfigMode(switch3)
SetCmd(switch3,'ip igmp snooping')
SetCmd(switch3,'ip igmp snooping vlan',Vlan20)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')
# IdleAfter(Ac_ap_syn_time)

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless')
data2 = SetCmd(switch1,'show wireless network 1')

#check
res1 = CheckLine(data1,'AP Igmp Snooping Mode','Enable',IC=True)
res2 = CheckLine(data2,'Network Igmp Snooping M2u','Enable',IC=True)

#result
printCheckStep(testname, 'Step 1',res1,res2)

################################################################################
#Step 2
#操作
#AC1,S3使能三层组播协议：
##DCWS-6028(config)#ip pim multicast-routing 
##DCWS-6028(config)#interface vlan 4091
##DCWS-6028(config-if-vlan4091)#ip pim dense-mode
##DCWS-6028(config-if-vlan4091)#exit
##DCWS-6028(config)#interface vlan 10
##DCWS-6028(config-if-vlan10)#ip pim dense-mode
##DCWS-6028(config-if-vlan10)#exit
##DCWS-6028(config)#interface vlan 192
##DCWS-6028(config-if-vlan192)#ip pim dense-mode
##DCWS-6028(config-if-vlan192)#exit
#
#预期
#Show run显示配置正确。
################################################################################

printStep(testname,'Step 2',\
          'Enable L3 multicast protocol on S1 and AC1')

res1=res2=res3=res4=res5=1
#operate

#AC1,S3全局使能PIM-DM 协议
EnterConfigMode(switch1)
SetCmd(switch1,'ip pim multicast-routing')
EnterConfigMode(switch3)
SetCmd(switch3,'ip pim multicast-routing')

#AC1 各三层接口开启 PIM-DM
EnterConfigMode(switch3)
EnterInterfaceMode(switch3,'vlan '+ Vlan4091)
SetCmd(switch3,'ip pim dense-mode')
EnterInterfaceMode(switch3,'vlan '+ Vlan40)
SetCmd(switch3,'ip pim dense-mode')

#S3 各三层接口开启 PIM-DM
EnterInterfaceMode(switch3,'vlan '+ Vlan20)
SetCmd(switch3,'ip pim dense-mode')
EnterInterfaceMode(switch3,'vlan '+ Vlan192)
SetCmd(switch3,'ip pim dense-mode')
EnterInterfaceMode(switch3,'vlan '+ Vlan40)
SetCmd(switch3,'ip pim dense-mode')

#check
data = ShowRun(switch3)

res1 = CheckLineInOrder(data,['interface Vlan20','ip pim dense-mode'],IC=True)
res2 = CheckLineInOrder(data,['interface Vlan40','ip pim dense-mode'],IC=True)
res3 = CheckLineInOrder(data,['interface Vlan192','ip pim dense-mode'],IC=True)

#result
printCheckStep(testname, 'Step 2',res1,res2,res3)

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

#STA1,STA2关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
IdleAfter(10)

#获取STA1,STA2的地址
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
#有线PC发送组播流量，192.168.10.2-->229.1.1.1。客户端点播组229.1.1.1的流量。
#
#预期
#客户端点播成功。在客户端抓包查看 的目的mac为客户端的mac地址。
################################################################################
printStep(testname,'Step 4',\
          'pc send multicast packets 192.168.10.2->229.1.1.1,',\
          'client send demand packets to 229.1.1.1 group,',\
          'client demand success and can capture packets with dstmac sta1mac.')

res1=res2=-1
#operate

res = ConnectDsendWireless(testerip_wired)
if 0==res:
    printRes('start Transmit group stream')
    SetDsendStreamWireless(Port=testerp1_wired,PortTypeConfig='0',StreamMode='0',StreamRateMode = 'pps',StreamRate='100', \
                SouMac='00-00-00-00-00-01',DesMac='01-00-5e-01-01-01',Protocl='ipv4',SouIp=multicast_srcip,DesIp='229.1.1.1')
    StartTransmitWireless(testerp1_wired)
    DisconnectDsendWireless()

#STA1 发送V2点播点播报文
ConnectDsendWireless(testerip_sta1)
SetDsendStreamWireless(Port=testerp1_sta1,PortTypeConfig='0',StreamMode='0',StreamRateMode='pps',StreamRate=Report_rate, \
               SouMac=sta1mac, DesMac='01-00-5e-01-01-01',Protocl='ipv4',SouIp=sta1_ipv4,DesIp='229.1.1.1',ProtoclEx='igmp',\
               Type='report',IgmpVersion='2',IgmpGroupAddress = '229.1.1.1')
StartTransmitWireless(testerp1_sta1)
DisconnectDsendWireless()

#检查STA1是否收到组播报文
ConnectDsendWireless(testerip_sta1)
StartDsendCaptureWireless(Port=testerp1_sta1)
IdleAfter(Rate_stable_wait_time)
StopDsendCaptureWireless(testerp1_sta1) 

#检测抓到的包，是否包含目的mac是sta1的mac地址
res1 = CheckDsendCaptureStreamWireless(testerp1_sta1,SrcIp=multicast_srcip,DstMac=sta1mac)
res2 = CheckDsendCaptureStreamWireless(testerp1_sta1,SrcIp=multicast_srcip,DstMac='01-00-5e-01-01-01')

printRes('res1='+str(res1)+'\nres2='+str(res2))
DisconnectDsendWireless()

#check
res1 = 0 if res1 > 0 else -1

#result
printCheckStep(testname, 'Step 4',res1,res2)
        
################################################################################
#Step 5
#操作
#在AP1上面get igmp-snooping-fwd查看组播转发表项。
#
#预期
#AP上面建立关于客户端的组播表项，各个参数正确。
################################################################################
printStep(testname,'Step 5',\
          'get igmp-snooping-fwd on AP1,',\
          'check there is multicast table of client with some args.')
          
res1=1
#operate
SetCmd(ap1,'\x03')

IdleAfter(2)
data1 = SetCmd(ap1,'get igmp-snooping-fwd')
res1 = CheckLineList(data1,[('vlan-id',Vlan4091),\
                            ('group-address','229.1.1.1'),\
                            ('station',sta1mac_type1),\
                            ('type','Local')],IC=True)
#check

#result
printCheckStep(testname, 'Step 5',res1)

################################################################################
#Step 6
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 6',\
          'Recover initial config for switches.')


##停止发包
res = ConnectDsendWireless(testerip_wired)
if 0==res:
    StopTransmitWireless(testerp1_wired)
    DisconnectDsendWireless()   
res = ConnectDsendWireless(testerip_sta1)
if 0==res:
    StopTransmitWireless(testerp1_wired)
    DisconnectDsendWireless()

#operate
##解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no igmp snooping m2u')
EnterWirelessMode(switch1)
SetCmd(switch1,'no igmp snooping')

EnterConfigMode(switch1)
SetCmd(switch1,'no ip pim multicast-routing')
EnterConfigMode(switch3)
SetCmd(switch3,'no ip pim multicast-routing')
SetCmd(switch3,'no ip igmp snooping')

EnterInterfaceMode(switch3,'vlan '+ Vlan4091)
SetCmd(switch3,'no ip pim dense-mode')
EnterInterfaceMode(switch3,'vlan '+ Vlan40)
SetCmd(switch3,'no ip pim dense-mode')
EnterInterfaceMode(switch3,'vlan '+ Vlan192)
SetCmd(switch3,'no ip pim dense-mode')
EnterInterfaceMode(switch3,'vlan '+ Vlan20)
SetCmd(switch3,'no ip pim dense-mode')
EnterInterfaceMode(switch3,'vlan '+ Vlan40)
SetCmd(switch3,'no ip pim dense-mode')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')
# IdleAfter(Ac_ap_syn_time)
  
#end
printTimer(testname, 'End')