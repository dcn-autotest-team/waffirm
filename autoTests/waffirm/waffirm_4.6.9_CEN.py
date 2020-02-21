#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.6.9.py - test case 4.6.9 of waffirm_new
#
# Author:  (jinpfb)
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Date: 2012-12-24 9:45:00
#
# Features:
# 4.6.9	采用采用IPv6管理地址的集中式转发--组播转发
# 测试目的：测试组播数据通过IPv6集中式隧道能够被正常转发
# 测试环境：同测试拓扑
# 测试描述：测试组播数据通过IPv6集中式隧道能够被正常转发，客户端能够点播到服务器发送的组播数据流
#
#*******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.6.9'
avoiderror(testname)
printTimer(testname,'Start','test l3-stream of client forwards about Focus-forwarding via ipv6')

suggestionList = []

################################################################################
#Step 1
#操作
# 配置AC1通过静态配置的方式获取无线地址，删除AC1的无线IPv4地址，配置AC1的无线ipv6地址：
# switch(config-wireless)#no auto-ip-assign
# switch(config-wireless)#no static-ip
# switch(config-wireless)#static-ipv6 2001::1
#
#预期
#Show wireless能够查看到无线配置的成功
################################################################################
printStep(testname,'Step 1',
          'Delete static ipv4 address on AC1',
          'Add static ipv6 address configuration on AC1')

res1=res2=1
#operate

EnterWirelessMode(switch1)
SetCmd(switch1,'no','static-ip')
IdleAfter(5)
data1 = SetCmd(switch1,'show wireless')

#check
res1 = CheckLine(data1,'WS IPv6 Address',StaticIpv6_ac1,IC=True)
res2 = CheckNoLineList(data1,[('WS IP Address',StaticIpv4_ac1)],IC=True)

#result
printCheckStep(testname, 'Step 1',res1,res2)

################################################################################
#Step 2
#操作
#在AC1配置network1的SSID为test1，关联vlan4091，配置下发到AP1。
#在AC1上面将vlan4091加入到l2-tunnel vlan-list中
#在AC1配置network1的SSID为test1，关联vlan4091，并配置下发到AP1
#
#
#预期
#配置下发成功。
################################################################################
printStep(testname,'Step 2',
          'set network 1 ssid test1 and vlan 4091,',
          'apply ap profile to ap1,',
          'set betwork .')

res1=res2=res3=1
#operate

##配置集中转发拓扑

#AC1上创建vlan20 及三层接口,s1p1划入vlan 20
EnterConfigMode(switch1)
SetCmd(switch1,'vlan',Vlan20)
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport access vlan',Vlan20)
EnterInterfaceMode(switch1,'vlan '+Vlan20)
IdleAfter(Vlan_Idle_time)
SetCmd(switch1,'ipv6 address',If_vlan20_s1_ipv6 + '/64')                                   
SetIpAddress(switch1,If_vlan20_s1_ipv4,'255.255.255.0')

#添加v6路由
#AC1
EnterConfigMode(switch1)
SetCmd(switch1,'ipv6 route',Ap1_ipv6 + '/64',If_vlan20_s3_ipv6)
#S3
EnterConfigMode(switch3)
SetCmd(switch3,'ipv6 route',StaticIpv6_ac1 + '/128',If_vlan20_s1_ipv6)

#修改 AP1 default gateway
SetCmd(ap1,'set static-ipv6-route gateway',If_vlan20_s1_ipv6)

#s3p1划入 vlan20
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport access vlan',Vlan20)

#下发配置
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan '+Vlan4091)

IdleAfter(50)
## RDM36362
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless network','1')
data2 = SetCmd(switch1,'show wireless l2tunnel vlan-list')

#check
res1 = CheckLine(data1,'Default VLAN',Vlan4091,IC=True)
res2 = CheckLine(data1,'SSID',Network_name1,IC=True)
res3 = CheckLine(data2,Vlan4091)

#result
printCheckStep(testname, 'Step 2',res1,res2,res3)

################################################################################
#Step 3
#操作
# 在ac1的发现列表中添加ap1的ipv6地址，让ac1发现ap1并建立ipv6集中式隧道：
# switch(config-wireless)#discovery ipv6-list 2001:20::3
#
#预期
# sho wireless discovery ip-list能够查看到发现列表中添加成功。
# sho wireless l2tunnel tunnel-list能够查看到ap和ac隧道建立成功，
#SIP地址为ac1的无线ipv6地址，DIP地址为ap1的ipv6地址
################################################################################
printStep(testname,'Step 3',
          'Add ipv6 address of AP1 to discovery ipv6-list on AC1',
          'Check if tunnel created succeed between AP and AC1')

res1=res2=res3=1

#operate
# 
# #AC1删除对AP1,AP2 ipv4自动发现  (ipv6发现已经存在)
# EnterWirelessMode(switch1)
# SetCmd(switch1,'no','discovery ip-list',Ap1_ipv4)
# SetCmd(switch1,'no','discovery ip-list',Ap2_ipv4)
# 
# #重启AP1
# RebootAp('AP',AP=ap1)
    
#IdleAfter(Ac_ap_syn_time)

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless discovery ip-list',timeout=5)
data2 = SetCmd(switch1,'show wireless ap status',timeout=5)
data3 = SetCmd(switch1,'show wireless l2tunnel tunnel-list',timeout=5)

#check
res1 = CheckLine(data1,Ap1_ipv6)
res2 = CheckLine(data2,ap1mac,Ap1_ipv6,'Managed','Success',IC=True)
res3 = CheckLineList(data3,[(StaticIpv6_ac1),(Ap1_ipv6)],IC=True)
#RDM34910
if res2 != 0:
    for tmpCounter in xrange(0,6):
        IdleAfter('10')
        data2 = SetCmd(switch1,'show wireless ap status')
        res2 = CheckLine(data2,ap1mac,Ap1_ipv6,'Managed','Success',IC=True)
        if res2 == 0:
            break 

#result
printCheckStep(testname, 'Step 3',res1,res2,res3)

################################################################################
#Step 4
#操作
#STA1和STA2连接到网络test1。
#
#预期
#关联成功。客户端能够获取192.168.91.X网段的IP地址。
################################################################################
printStep(testname,'Step 4',
          'STA1 and STA2 connect to network 1,',
          'connect success adn clients dhcp and get 192.168.91.x ip address.')

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

if (res1 == 5) or (res2 == 5):
    suggestionList.append('Suggestions: Step 3 failed reason MAYBE RDM17089')
if (res1 == 3) or (res2 == 3):
    suggestionList.append('Suggestions: Step 3 failed reason MAYBE RDM17192')

#result
printCheckStep(testname, 'Step 4',res1,res2,res3,res4)      
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2 + res3 + res4
if GetWhetherkeepon(keeponflag):                      
    ################################################################################
    #Step 5
    #操作
    #在AC1上面开启三层组播协议PIM，三层接口4091使能pim-dm。全局及vlan4091使能IGMP Snooping。
    #在S3上开启三层组播协议PIM,三层接口192使能pim-dm。全局及vlan192使能IGMP Snooping
    #
    #预期
    #配置成功。
    ################################################################################
    printStep(testname,'Step 5',
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
    EnterInterfaceMode(switch3,'vlan '+ Vlan20)
    SetCmd(switch3,'ip pim dense-mode')
    EnterInterfaceMode(switch3,'vlan '+ Vlan192)
    SetCmd(switch3,'ip pim dense-mode')

    #全局及vlan 4091开启 igmp snooping
    EnterConfigMode(switch1)
    SetCmd(switch1,'ip igmp snooping')
    SetCmd(switch1,'ip igmp snooping vlan',Vlan4091)

    EnterWirelessMode(switch1)
    SetCmd(switch1,'igmp snooping')

    #EnterNetworkMode(switch1,1)
    #SetCmd(switch1,'igmp snooping m2u')
    #check
    #data1 = SetCmd(switch1,'show ip igmp snooping')
    #res1 = CheckLine(data1,'Global igmp','Enabled')
    #res2 = CheckLine(data1,'Igmp snooping is turned on for vlan 4091')
    data1 = ShowRun(switch1)
    res1 = CheckLineList(data1,[('ip igmp snooping'),
                                ('ip igmp snooping vlan',Vlan4091),
                                ('ip pim multicast-routing')],IC=True)
                                
    #result
    printCheckStep(testname, 'Step 5',res1)

    ################################################################################
    #Step 6
    #操作
    #PC1作为组播源发送组播流量（如视频），STA1和STA2进行点播。
    #
    #预期
    #STA1和STA2点播成功。AC1上面查看ip mroute、igmp snooping等表项正确。
    ################################################################################
    printStep(testname,'Step 6',
              'pc1 send multicast packets,sta1 and sta2 point,',
              'sta1 and sta2 point success,',
              'show ip mroute and show ip igmp snooping,',
              'check info returned is right.')

    res1=res2=-1
    #operate

    #发包工具发组播流量
    # res = ConnectDsend(testerip_wired,testerp1_wired_port)
    # if 0==res:
    #     printRes('start Transmit group stream')
    #     SetDsendStream(Port=testerp1_wired,StreamMode='0',StreamRateMode = 'pps',StreamRate='100', \
    #                 SouMac='00-00-00-00-00-01',DesMac='01-00-5e-01-01-01',Protocl='ipv4',SouIp=multicast_srcip,DesIp='225.1.1.1')
    #     StartTransmit(testerp1_wired)
    #     DisconnectDsend()

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

    #     
    # #检查STA1是否收到组播报文
    # res = ConnectDsendWireless(testerip_sta1)
    # if 0==res:
    #     StartDsendCaptureWireless(Port=testerp1_sta1)
    #     IdleAfter(Rate_stable_wait_time)
    #     StopDsendCaptureWireless(testerp1_sta1) 
    #     res1 = CheckDsendCaptureStreamWireless(testerp1_sta1,SrcIp=multicast_srcip,DstMac='01-00-5e-01-01-01')
    #     DisconnectDsendWireless()
    #     printRes('capture 1')
    # else:
    #     res1 = 0
    # IdleAfter(Var_ap_connect_diff)
    # 
    # #检查STA2是否收到组播报文
    # res = ConnectDsendWireless(testerip_sta2)
    # if 0==res:
    #     StartDsendCaptureWireless(Port=testerp1_sta2)
    #     IdleAfter(Rate_stable_wait_time)
    #     StopDsendCaptureWireless(testerp1_sta2) 
    #     res2 = CheckDsendCaptureStreamWireless(testerp1_sta2,SrcIp=multicast_srcip,DstMac='01-00-5e-01-01-01')
    #     DisconnectDsendWireless()
    #     printRes('capture 2')
    # else:
    #     res2 = 0
    #     
    # #check
    # res1 = 0 if res1>0 else -1
    # res2 = 0 if res2>0 else -1

    IdleAfter(5)
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

    ##停止发包
    # res = ConnectDsend(testerip_wired,testerp1_wired_port)
    # if 0==res:
    #     StopTransmit(testerp1_wired)
    #     DisconnectDsend()  
        
    #result
    printCheckStep(testname, 'Step 6',res1,res2)

################################################################################
#Step 7
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 7',
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

#删除v6路由
#AC1
EnterConfigMode(switch1)
SetCmd(switch1,'no','ipv6 route',Ap1_ipv6 + '/64',If_vlan20_s3_ipv6)
#S3
EnterConfigMode(switch3)
SetCmd(switch3,'no','ipv6 route',StaticIpv6_ac1 + '/128',If_vlan20_s1_ipv6)

EnterConfigMode(switch1)
SetCmd(switch1,'no ip igmp snooping')
EnterWirelessMode(switch1)
SetCmd(switch1,'no igmp snooping')

EnterConfigMode(switch1)
SetCmd(switch1,'no ip pim multicast-routing')
EnterConfigMode(switch3)
SetCmd(switch3,'no ip pim multicast-routing')

EnterInterfaceMode(switch1,'vlan '+ Vlan4091)
SetCmd(switch1,'no ip pim dense-mode')
EnterInterfaceMode(switch1,'vlan '+ Vlan20)
SetCmd(switch1,'no ip pim dense-mode')
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

#修改 AP1 ipv6 default gateway
SetCmd(ap1,'set static-ipv6-route gateway',If_vlan20_s3_ipv6)
SetCmd(ap1,'save-running')

#s3p1 划入vlan40
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport access vlan',Vlan40)

EnterNetworkMode(switch1,'1')
SetCmd(switch1,'vlan ' + Vlan4091)

#配置AC1 静态v4地址    
EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip',StaticIpv4_ac1)

#将发现方式更改为 v4 发现
EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(5)
SetCmd(switch1,'enable')
IdleAfter(5)
for i in range(10):
	EnterEnableMode(switch1)
	data1 = SetCmd(switch1,'show wireless ap status')
	res = CheckLine(data1,ap1mac,Ap1_ipv4,'1','Managed','Success',IC=True)
	if res==0:
		break
	IdleAfter(5)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

#end
printTimer(testname, 'End',suggestion = suggestionList)