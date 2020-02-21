#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.6.5.py - test case 4.6.5 of waffirm_new
#
# Author: qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2013 Digital China Networks Co. Ltd
#
# Date: 2012-12-24 9:45:00
#
# Features:
# 4.6.5 本地转发功能测试3（组播转发）
# 测试目的：测试组播报文的本地转发。
# 测试环境：同测试拓扑
# 测试描述：测试组播报文的本地转发。
#
#*******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.6.5'
avoiderror(testname)
printTimer(testname,'Start','Test forwarding function of multicast')

################################################################################
#Step 1
#操作
#在修改AP1的管理vlan为vlan10，untagged-vlan为vlan 10。
#修改三层交换机连接AP1的端口为trunk口，native vlan为vlan 10。
#在AC1配置network1的SSID为test1，关联vlan4091，配置下发到AP1。AC
#AP1能够被AC1管理，配置下发成功。AC
################################################################################
printStep(testname,'Step 1',
          'Set management vlan 10 on ac1 and ap1')

#operate

EnterApProMode(switch1,'1')
SetCmd(switch1,'management vlan',Vlan10)
SetCmd(switch1,'ethernet native-vlan 10')
EnterConfigMode(switch1)
SetCmd(switch1,'vlan',Vlan10)
EnterInterfaceMode(switch1,'vlan 10')
SetCmd(switch1,'ip address 20.1.1.1 255.255.255.0')

EnterConfigMode(switch3)
SetCmd(switch3,'vlan',Vlan10)
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport mode trunk')
SetCmd(switch1,'switchport trunk native vlan 10')

EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan 10')

EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan 10')

# SetCmd(ap1,'set static-ip-route gateway',If_vlan20_s1_ipv4)
# SetCmd(ap1,'set management vlan-id',Vlan10)
# SetCmd(ap1,'set untagged-vlan vlan-id',Vlan10)
ApSetcmd(ap1,Ap1cmdtype,'set_ip_route',If_vlan20_s1_ipv4,commitflag=True)
ApSetcmd(ap1,Ap1cmdtype,'set_management_vlanid',Vlan10)
ApSetcmd(ap1,Ap1cmdtype,'set_untagged_vlanid',Vlan10,commitflag=True)

EnterConfigMode(switch3)
SetCmd(switch3,'vlan',Vlan4091)
EnterInterfaceMode(switch3,'vlan '+Vlan4091)
SetCmd(switch3,'ip address ' + If_vlan4091_s2_ipv4 + ' 255.255.255.0')


res1 = 1
## RDM36362
res1 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])  
if not testcentral:
    WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac],eth_parameter=True)  

#result
printCheckStep(testname, 'Step 1',res1)


################################################################################
#Step 2
#操作
#在AC1上面将vlan4091从l2-tunnel vlan-list中删除。AC
#
#预期
#通过show wireless l2-tunnel vlan-list看不到vlan4092。
################################################################################
printStep(testname,'Step 2',
          'Delete l2 tunnel vlan list')

#operate
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    EnterWirelessMode(switch1)
    SetCmd(switch1,'no l2tunnel vlan-list')
    #check
    data1 = SetCmd(switch1,'show wireless l2tunnel vlan-list')
    res1 = CheckLine(data1,Vlan4091,'VLAN4091')
    res1 = 0 if res1 != 0 else -1

    IdleAfter('30')
    EnterEnableMode(switch1)
    res2 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
else:
    EnterEnableMode(switch1)
    SetCmd(switch1,'wireless ap eth-parameter apply profile 1')
        
    IdleAfter(30)
    EnterEnableMode(switch1)
    for tmpCounter in xrange(0,16):
        IdleAfter('5')
        data1 = SetCmd(switch1,'show wireless ap status')
        res1 = CheckLine(data1,ap1mac,Ap1_ipv4,'Managed','Success',IC=True)
        if res1 == 0:
            break
    res2 = 0
#result
printCheckStep(testname, 'Step 2',res1,res2)
                      
################################################################################
#Step 3
#操作
#STA1和STA2连接到网络test1。
#
#预期
#配置成功。
################################################################################

printStep(testname,'Step 3',
          'Sta1 and sta2 connect to test1.')

#operate
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='open',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)

res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')

res3 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,connectType='open',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)

res4 = CheckWirelessClientOnline(switch1,sta2mac,'online')
#result
printCheckStep(testname, 'Step 3',res1,res2,res3,res4)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res3 
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 4
    #操作
    #在三层交换机上面开启三层组播协议PIM，三层接口int v25、int v4091使能pim-dm。全局和vlan 4091开启IGMP Snooping。
    #配置成功。
    ################################################################################

    printStep(testname,'Step 4',
              'Config igmp on switch1 and switch3')

    EnterConfigMode(switch3)
    SetCmd(switch3,'ip pim multicast-routing')
    EnterInterfaceMode(switch3,'vlan '+Vlan4091)
    SetCmd(switch3,'ip pim dense-mode')
    EnterInterfaceMode(switch3,'vlan 192')
    SetCmd(switch3,'ip pim dense-mode')

    EnterConfigMode(switch3)
    SetCmd(switch3,'ip igmp snooping')
    SetCmd(switch3,'ip igmp snooping vlan',Vlan4091)
    EnterWirelessMode(switch1)
    SetCmd(switch1,'igmp snooping')
    #
    #EnterNetworkMode(switch1,1)
    #SetCmd(switch1,'igmp snooping m2u')

    #check
    data1 = ShowRun(switch3)
    res1 = CheckLineList(data1,['ip igmp snooping vlan 4091','ip pim multicast-routing'])

    printCheckStep(testname, 'Step 4',res1)


    ################################################################################
    #Step 5
    #操作
    #PC1作为组播源发送组播流量。STA1和STA2点播。
    #点播成功，STA1和STA2都能够收到组播流量。在三层交换机上面查看组播表项正确。
    ################################################################################

    printStep(testname,'Step 5',
              'Start multicast and unicast stream')
              

    #获取STA1,STA2的地址
    sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool1)
    sta1_ipv4 = sta1_ipresult['ip']
    res3 = sta1_ipresult['res']

    sta2_ipresult = GetStaIp(sta2,checkippool=Dhcp_pool1)
    sta2_ipv4 = sta2_ipresult['ip']
    res4 = sta2_ipresult['res']

    print ConnectDsendWireless(testerip_wired)
    SetDsendStreamWireless(Port=testerp1_wired,PortTypeConfig='0',StreamMode='0',StreamRateMode = 'pps',StreamRate='10',
                           SouMac='00-00-00-00-00-01',DesMac='01-00-5e-01-01-01',Protocl='ipv4',SouIp=Radius_server,DesIp='225.1.1.1')
    StartTransmitWireless(testerp1_wired)

    ConnectDsendWireless(testerip_sta1)
    SetDsendStreamWireless(Port=testerp1_sta1,PortTypeConfig='0',StreamMode='0',StreamRateMode='pps',StreamRate='10',
                           SouMac=sta1mac, DesMac='01-00-5e-01-01-01',Protocl='ipv4',SouIp=sta1_ipv4,DesIp='225.1.1.1',ProtoclEx='igmp',
                           Type='report',IgmpVersion='2',IgmpGroupAddress = '225.1.1.1')
    StartTransmitWireless(testerp1_sta1)

    ConnectDsendWireless(testerip_sta2)
    SetDsendStreamWireless(Port=testerp1_sta2,PortTypeConfig='0',StreamMode='0',StreamRateMode='pps',StreamRate='10',
                           SouMac=sta2mac, DesMac='01-00-5e-01-01-01',Protocl='ipv4',SouIp=sta2_ipv4,DesIp='225.1.1.1',ProtoclEx='igmp',
                           Type='report',IgmpVersion='2',IgmpGroupAddress = '225.1.1.1')
    StartTransmitWireless(testerp1_sta2)

    IdleAfter(30)

    data1 = SetCmd(switch3,'show ip igmp snooping vlan 4091') 
    res3 = CheckLine(data1,'225.1.1.1',s3p3,'V2')
    data2 = SetCmd(switch3,'show ip mroute')
    out_interface_name = str(GetValueBetweenTwoValuesInData(data2,Vlan4091+'.*Index:',', State')).lstrip().rstrip()
    res4 = CheckLine(data2,'225.1.1.1',multicast_srcip,Vlan192,out_interface_name)

    printCheckStep(testname, 'Step 5',res3,res4)

################################################################################
#Step 6
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 6',
          'Recover initial config for switches.')

#operate
ConnectDsendWireless(testerip_wired)
StopTransmitWireless(testerp1_wired)
IdleAfter('2')
ConnectDsendWireless(testerip_sta1)
StopTransmitWireless(testerp1_sta1)
IdleAfter('2')
ConnectDsendWireless(testerip_sta2)
StopTransmitWireless(testerp1_sta2)
IdleAfter('2')
# sta1、sta2解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

# SetCmd(ap1,'set static-ip-route gateway',If_vlan20_s3_ipv4)
# SetCmd(ap1,'set management vlan-id','1')
# SetCmd(ap1,'set untagged-vlan vlan-id','1')
# SetCmd(ap1,'save-running')
ApSetcmd(ap1,Ap1cmdtype,'set_ip_route',If_vlan20_s3_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'set_management_vlanid','1')
ApSetcmd(ap1,Ap1cmdtype,'set_untagged_vlanid','1',commitflag=True)
ApSetcmd(ap1,Ap1cmdtype,'saverunning')

EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan 10')
SetCmd(switch1,'no vlan',Vlan10)
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport mode access')

EnterConfigMode(switch1)
SetCmd(switch1,'vlan',Vlan40)
SetCmd(switch1,'switchport interface',s1p1)
EnterWirelessMode(switch1)
SetCmd(switch1,'no igmp snooping')

EnterConfigMode(switch3)
SetCmd(switch3,'no ip igmp snooping')
SetCmd(switch3,'no vlan',Vlan10)
SetCmd(switch3,'no ip pim multicast-routing')
EnterInterfaceMode(switch3,'vlan 192')
SetCmd(switch3,'no ip pim dense-mode')
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport mode access')
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'switchport mode access')

EnterConfigMode(switch3)
SetCmd(switch3,'vlan',Vlan20)
SetCmd(switch3,'switchport interface',s3p3)
SetCmd(switch3,'vlan',Vlan40)
SetCmd(switch3,'switchport interface',s3p1)
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    EnterWirelessMode(switch1)
    SetCmd(switch1,'l2tunnel vlan-list add',Vlan4091 + '-' + Vlan4093)
    EnterConfigMode(switch3)
    SetCmd(switch3,'no interface vlan 4091')
    SetCmd(switch3,'no vlan',Vlan4091)
else:
    EnterEnableMode(switch3)
    SetCmd(switch3,'clear ip dhcp binding all')
    EnterInterfaceMode(switch3,'vlan '+Vlan4091)
    SetCmd(switch3,'ip address ' + If_vlan4091_s1_ipv4 +' 255.255.255.0')
    EnterConfigMode(switch3)
    SetCmd(switch3,'Interface ',s3p3)
    SetCmd(switch3,'switchport mode trunk')
    SetCmd(switch3,'switchport trunk native vlan 20')
    SetCmd(switch3,'Interface ',s3p4)
    SetCmd(switch3,'switchport mode trunk')
    SetCmd(switch3,'switchport trunk native vlan 30')

EnterApProMode(switch1,'1')
SetCmd(switch1,'management vlan','1')
SetCmd(switch1,'ethernet native-vlan 1')

WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
if not testcentral:
    WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac],eth_parameter=True)
#end
printTimer(testname, 'End')