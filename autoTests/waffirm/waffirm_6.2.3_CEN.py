#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_6.2.3.py - test case 4.2.3 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2016 Digital China Networks Co. Ltd
#
# Date: 2016-4-27 9:45:00
#
# Features:
# 6.2.3	AP设置特定IP集中转发测试(组播转发)
# 测试目的：测试组播数据通过集中式隧道能够被正常转发
# 测试环境：同测试拓扑
# 测试描述：测试组播数据通过集中式隧道能够被正常转发，客户端能够点播到服务器发送的组播数据流
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

testname = 'TestCase 6.2.3'
avoiderror(testname)
printTimer(testname,'Start','test l3-stream of client forwards about Focus-forwarding')

################################################################################
#Step 1 Step 2
#操作
#在AC1配置network1的SSID为test1，关联vlan4091，配置下发到AP1。
#在AC1上面将vlan4091加入到l2-tunnel vlan-list中
#
#(都是初始配置，无需操作)
#
#预期
#配置下发成功。
################################################################################
printStep(testname,'Step 1,Step 2',
          'set network 1 ssid test1 and vlan 4091,',
          'apply ap profile to ap1')

res1=res2=res3=1
#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan '+Vlan4091)

##配置集中转发拓扑

#AC1上创建vlan20 及三层接口,s1p1划入vlan 20
EnterConfigMode(switch1)
SetCmd(switch1,'vlan',Vlan20)
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport access vlan',Vlan20)
EnterInterfaceMode(switch1,'vlan '+Vlan20)
SetCmd(switch1,'ip address 172.16.20.1 255.255.254.0')
IdleAfter(Vlan_Idle_time)

#配置AP1
SetCmd(ap1,'set management vlan-id',Vlan20)
SetCmd(ap1,'set untagged-vlan vlan-id',Vlan20)
SetCmd(ap1,'set management static-ip 172.16.20.38')
SetCmd(ap1,'set management static-mask 255.255.254.0')
SetCmd(ap1,'set static-ip-route gateway 172.16.20.1')
SetCmd(ap1,'set management dhcp-status down')


#配置L3
EnterInterfaceMode(switch3,'vlan '+Vlan20)
SetCmd(switch3,'no ip address')
SetCmd(switch3,'ip address 172.16.20.2 255.255.254.0')
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport access vlan',Vlan20)

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list 172.16.20.38')
EnterApProMode(switch1,'1')
SetCmd(switch1,'management vlan',Vlan20)
SetCmd(switch1,'ethernet native-vlan 20')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless network','1')
data2 = SetCmd(switch1,'show wireless l2tunnel vlan-list')

#check
res1 = CheckLine(data1,'Default VLAN',Vlan4091,IC=True)
res2 = CheckLine(data1,'SSID',Network_name1,IC=True)
res3 = CheckLine(data2,Vlan4091)
#result
printCheckStep(testname, 'Step 1 Step 2',res1,res2,res3)

################################################################################
#Step 3
#操作
#STA1和STA2连接到网络test1。
#
#预期
#关联成功。客户端能够获取192.168.91.X网段的IP地址。
################################################################################
printStep(testname,'Step 3',
          'STA1 and STA2 connect to network 1,',
          'connect success adn clients dhcp and get 192.168.91.x ip address.')

sta1_ipv4 = ''
sta2_ipv4 = ''

res1=res2=res3=res4=1

#operate
#STA1,STA2关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap1mac_lower)

#获取STA1,STA2的地址
data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
data2 = SetCmd(sta2,'ifconfig -v',Netcard_sta2)
SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
SearchResult2 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data2,re.I)

#check
if None != SearchResult1:
    sta1_ipv4 = SearchResult1.group(1)
    if None != re.search(Dhcp_pool1,sta1_ipv4):
        printRes('STA1 ip address: ' + sta1_ipv4)
        res3 = 0  
else:
    res3 = 1
    printRes('Failed: Get ipv4 address of STA1 failed') 
    
if None != SearchResult2:
    sta2_ipv4 = SearchResult2.group(1)
    if None != re.search(Dhcp_pool1,sta2_ipv4):
        printRes('STA2 ip address: ' + sta2_ipv4)
        res4 = 0  
else:
    res4 = 1
    printRes('Failed: Get ipv4 address of STA2 failed')
             

#result
printCheckStep(testname, 'Step 3',res1,res2,res3,res4)      
                      
################################################################################
#Step 4
#操作
#在AC1上面开启三层组播协议PIM，三层接口4091使能pim-dm。全局及vlan4091使能IGMP Snooping。
#在S3上开启三层组播协议PIM,三层接口192使能pim-dm。全局及vlan192使能IGMP Snooping
#
#预期
#配置成功。
################################################################################
printStep(testname,'Step 4',
          'enable ip pim multicast-routing,',
          'set pim-dm on vlan 4091,',
          'enable igmp snooping on vlan 4091.')

res1=1
#operate

#AC1,S3全局使能PIM-DM 协议
EnterConfigMode(switch1)
SetCmd(switch1,'ip pim multicast-routing')
EnterConfigMode(switch3)
SetCmd(switch3,'ip pim multicast-routing')

#各三层接口开启 PIM-DM
EnterInterfaceMode(switch1,'vlan '+ '4091')
SetCmd(switch1,'ip pim dense-mode')
EnterInterfaceMode(switch1,'vlan '+ Vlan20)
SetCmd(switch1,'ip pim dense-mode')

EnterInterfaceMode(switch1,'vlan '+ Vlan40)
SetCmd(switch1,'shut')

EnterInterfaceMode(switch3,'vlan '+ Vlan20)
SetCmd(switch3,'ip pim dense-mode')
EnterInterfaceMode(switch3,'vlan '+ Vlan192)
SetCmd(switch3,'ip pim dense-mode')

#全局及vlan 4092开启 igmp snooping
EnterConfigMode(switch1)
SetCmd(switch1,'ip igmp snooping')
SetCmd(switch1,'ip igmp snooping vlan',Vlan4091)

#无线功能开启 igmp snooping
EnterWirelessMode(switch1)
SetCmd(switch1,'igmp snooping')

data1 = ShowRun(switch1)
res1 = CheckLineList(data1,[('ip igmp snooping'),
                            ('ip igmp snooping vlan',Vlan4091),
                            ('ip pim multicast-routing')],IC=True)
                            
#result
printCheckStep(testname, 'Step 4',res1)

################################################################################
#Step 5
#操作
#PC1作为组播源发送组播流量（如视频），STA1和STA2进行点播。
#
#预期
#STA1和STA2点播成功。AC1上面查看ip mroute、igmp snooping等表项正确。
################################################################################
printStep(testname,'Step 5',
          'pc1 send multicast packets,sta1 and sta2 point,',
          'sta1 and sta2 point success,',
          'show ip mroute and show ip igmp snooping,',
          'check info returned is right.')

res1=res2=-1
#operate

#发包工具发组播流量
res = ConnectDsendWireless(testerip_wired)
if 0==res:
    printRes('start Transmit group stream')
    SetDsendStreamWireless(Port=testerp1_wired,PortTypeConfig='0',StreamMode='0',StreamRateMode = 'pps',StreamRate='10',
                           SouMac='00-00-00-00-00-01',DesMac='01-00-5e-01-01-01',Protocl='ipv4',SouIp=multicast_srcip,DesIp='225.1.1.1')
    StartTransmitWireless(testerp1_wired)
    DisconnectDsendWireless()
    
#STA1 发送V2点播点播报文
res = ConnectDsendWireless(testerip_sta1)
if 0==res:
    printRes('start Transmit igmp stream1')
    SetDsendStreamWireless(Port=testerp1_sta1,PortTypeConfig='0',StreamMode='0',StreamRateMode='pps',StreamRate=Report_rate,
                           SouMac=sta1mac, DesMac='01-00-5e-01-01-01',Protocl='ipv4',SouIp=sta1_ipv4,DesIp='225.1.1.1',ProtoclEx='igmp',
                           Type='report',IgmpVersion='2',IgmpGroupAddress = '225.1.1.1')
    StartTransmitWireless(testerp1_sta1)
    DisconnectDsendWireless()
    
#STA2发送V2点播点播报文
res = ConnectDsendWireless(testerip_sta2)
if 0==res:
    printRes('start Transmit group stream2')
    SetDsendStreamWireless(Port=testerp1_sta2,PortTypeConfig='0',StreamMode='0',StreamRateMode='pps',StreamRate=Report_rate,
                           SouMac=sta2mac, DesMac='01-00-5e-01-01-01',Protocl='ipv4',SouIp=sta2_ipv4,DesIp='225.1.1.1',ProtoclEx='igmp',
                           Type='report',IgmpVersion='2',IgmpGroupAddress = '225.1.1.1')
    StartTransmitWireless(testerp1_sta2)
    DisconnectDsendWireless()

#检查组播表项
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless l2tunnel tunnel-list')   
tunnel_name = str(GetValueBetweenTwoValuesInData(data1,'\n','\s+'+StaticIpv4_ac1+'\s+'+Var_Staticip1)).strip()

data2 = SetCmd(switch1,'show ip igmp snooping vlan',Vlan4091) 
res1 = CheckLine(data2,'225.1.1.1','capwaptnl',IC=True)

i_times = 0
while i_times < 20:
    data3 = SetCmd(switch1,'show ip mroute')
    out_interface_name = str(GetValueBetweenTwoValuesInData(data3,Vlan4091+'.*Index:',', State')).strip()
    if 0 == CheckLine(data3,'225.1.1.1',multicast_srcip,out_interface_name,IC=True):
        res2 = 0
        break
    IdleAfter(3)
    i_times += 1


#result
printCheckStep(testname, 'Step 5',res1,res2)



################################################################################
#Step 6
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 6',
          'Recover initial config for switches.')

#operate

res = ConnectDsendWireless(testerip_wired)
if 0==res:
    StopTransmitWireless(testerp1_wired)
    DisconnectDsendWireless()   
res = ConnectDsendWireless(testerip_sta1)
if 0==res:
    StopTransmitWireless(testerp1_sta1)
    DisconnectDsendWireless()
res = ConnectDsendWireless(testerip_sta2)
if 0==res:
    StopTransmitWireless(testerp1_sta2)
    DisconnectDsendWireless()  

#解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

EnterConfigMode(switch1)
SetCmd(switch1,'no ip igmp snooping')
EnterWirelessMode(switch1)
SetCmd(switch1,'no igmp snooping')

EnterConfigMode(switch1)
SetCmd(switch1,'no ip pim multicast-routing')
EnterConfigMode(switch3)
SetCmd(switch3,'no ip pim multicast-routing')

EnterInterfaceMode(switch1,'vlan '+ '4091')
SetCmd(switch1,'no ip pim dense-mode')
EnterInterfaceMode(switch1,'vlan '+ Vlan20)
SetCmd(switch1,'no ip pim dense-mode')

EnterInterfaceMode(switch1,'vlan '+ Vlan40)
SetCmd(switch1,'no shut')

EnterInterfaceMode(switch3,'vlan '+ Vlan192)
SetCmd(switch3,'no ip pim dense-mode')
EnterInterfaceMode(switch3,'vlan '+ Vlan20)
SetCmd(switch3,'no ip pim dense-mode')

#AC1恢复
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan',Vlan20)
SetCmd(switch1,'no','vlan',Vlan20)
SetCmd(switch1,'vlan',Vlan40)
SetCmd(switch1,'switchport interface',s1p1)

#修改 AP1 default gateway
SetCmd(ap1,'set management static-ip 20.1.1.3')
SetCmd(ap1,'set management static-mask 255.255.255.0')
SetCmd(ap1,'set static-ip-route gateway',If_vlan20_s3_ipv4)
SetCmd(ap1,'save-running')

#s3p1 划入vlan40
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport access vlan',Vlan40)
EnterInterfaceMode(switch3,'vlan '+Vlan20)
IdleAfter(Vlan_Idle_time)
SetIpAddress(switch3,If_vlan20_s3_ipv4,'255.255.255.0')
SetCmd(switch3,'ipv6 address',If_vlan20_s3_ipv6 + '/64')

IdleAfter(60)

EnterNetworkMode(switch1,'1')
SetCmd(switch1,'vlan ' + Vlan4091)

EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery ip-list 172.16.20.38')
SetCmd(switch1,'ap profile 1')
SetCmd(switch1,'no management vlan')
SetCmd(switch1,'no ethernet native-vlan')

WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

#end
printTimer(testname, 'End')
