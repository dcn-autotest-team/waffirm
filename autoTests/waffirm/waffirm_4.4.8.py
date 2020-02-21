#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.4.8.py - test case 4.4.8 of waffirm
#
# Author:  fuzf@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.4.8 本地转发模式下，对AP下所有用户进行二层隔离
# 测试目的：本地转发模式对AP下所有用户实现隔离。
# 测试环境：同测试拓扑
# 测试描述：本地转发模式，通过profile配置隔离功能，可以让该AP同一vlan不同vap下的无线用户实现二层隔离，
#          同时开启radio下的二层隔离功能，隔离同一vap下的用户，从而实现对AP下的所有用户二层隔离。
#          （STA1的MAC地址：STA1MAC）
#
#*******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
#*******************************************************************************

#Package

#Global Definition
staticIp_sta1 = '192.168.91.100'
staticIp_sta2 = '192.168.91.200'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.4.8'
avoiderror(testname)
printTimer(testname,'Start',"test l2 isolation of stations through the whole ap in local switch mode")


################################################################################
#Step 1
#操作
#Vlan 4091从tunnel vlan删除
# 在ac1修改network2的关联vlan为4091，下发配置。
# Sp3p3 ,s3p4改为trunk口，允许vlan 4091通过，s3p3 native vlan为20
#
#预期
#Ac1：tunnel vlan list中没有4091
# Show wireless network 2看到default vlan 为4091。
# S3： Show interface Ethernet s3p3/s3p4,看到为trunk，allow vlan中包含4091
################################################################################
printStep(testname,'Step 1',
          'Delete vlan 4091 from tunnel vlan',
          'Change s3p3,s3p4 to Trunk,'
          'Change s3p3 native vlan 20')

res1=res2=res3=res4=1
#operate

#tunnel vlan中删除 4091
EnterWirelessMode(switch1)
SetCmd(switch1,'l2tunnel vlan-list remove','4091')

#修改network2关联vlan为4091
EnterNetworkMode(switch1, '2')
SetCmd(switch1,'vlan 4091')
EnterEnableMode(switch1)
IdleAfter(60)

#下发ap profile 1
# WirelessApProfileApply(switch1,1)
# for i in xrange(10):
    # IdleAfter(10)
    # data1 = SetCmd(switch1,'show wireless ap status')
    # if re.search('1\s+Managed Success',data1) is not None:
        # break

#配置s3p3,s3p4为Trunk 口，allowed vlan 4091，s3p3 native vlan为20, s3p4 native vlan为30
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk allowed vlan','4091')
SetCmd(switch3,'switchport trunk native vlan',Vlan20)
EnterInterfaceMode(switch3,s3p4)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk allowed vlan','4091')
SetCmd(switch3,'switchport trunk native vlan',Vlan30)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless l2tunnel vlan-list')
data2 = SetCmd(switch1,'show wireless network',1,timeout=3)

EnterEnableMode(switch3)
data3 = SetCmd(switch3,'show running-config','interface',s3p3)
data4 = SetCmd(switch3,'show running-config','interface',s3p4)
# IdleAfter(Ac_ap_syn_time)

#check
res1 = CheckLine(data1,'4091')
res1 = 0 if 0 != res1 else 1

res2 = CheckLine(data2,'Default VLAN','4091',IC=True)
res3 = CheckLineList(data3, [('switchport mode trunk'),
                             ('switchport trunk allowed vlan','4091'),
                             ('switchport trunk native vlan',Vlan20)],IC=True)
res4 = CheckLineList(data4, [('switchport mode trunk'),
                             ('switchport trunk allowed vlan','4091'),
                             ('switchport trunk native vlan',Vlan30)],IC=True)                            

#result
printCheckStep(testname, 'Step 1',res1,res2,res3,res4)

################################################################################
#Step 2
#操作
#将STA1关联到test1,STA2关联网络test2
#（sta1和sta2网络地址为192,168.91.x，网关为192.168.91.1）
#
#预期
#
#成功关联
################################################################################

printStep(testname,'Step 2',
          'STA1 and STA2 connect to network 1,',
          'STA1 and STA2 get static ip 192.168.91.100 and 192.168.91.200')

res1=res2=res3=res4=1

#operate
#STA1 network1, STA2关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,dhcpFlag=False,bssid=ap1mac_type1_network2)
IdleAfter(10)

#手动配置STA1,STA2地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask','255.255.255.0')
SetCmd(sta2,'\x03')
SetCmd(sta2,'dhclient -r',Netcard_sta2,promotePatten='#',promoteTimeout=60)
SetCmd(sta2,'ifconfig',Netcard_sta2,staticIp_sta2,'netmask','255.255.255.0')

#获取已配置地址
data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
data2 = SetCmd(sta2,'ifconfig -v',Netcard_sta2)
SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
SearchResult2 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data2,re.I)

#check
if None != SearchResult1: 
    if SearchResult1.group(1).strip() == staticIp_sta1:
        printRes('STA1 ip address: ' + staticIp_sta1)
        res3 = 0 
else:
    res3 = 1
    printRes('Failed: Config static ip for STA1 failed') 
    
if None != SearchResult2: 
    if SearchResult2.group(1).strip() == staticIp_sta2: 
        printRes('STA2 ip address: ' + staticIp_sta2)
        res4 = 0  
else:
    res4 = 1
    printRes('Failed: Config static ip for STA2 failed')             

#result
printCheckStep(testname, 'Step 2',res1,res2,res3,res4)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2 + res3 +res4
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
    res1 = CheckPing(sta1,staticIp_sta2,mode='linux')  
    res2 = CheckPing(sta2,staticIp_sta1,mode='linux')               
    #check

    #result
    printCheckStep(testname,'Step 3',res1,res2)

    ################################################################################
    #Step 4 
    # 操作
    # 在AC1 profile 1下配置station-isolation allowed vlan 4091
    # 在AC1 profile 1 radio 1下配置station-isolation 
    # 下发profile 1的配置
    # 预期
    # 配置成功，配置下发成功
    ################################################################################
    printStep(testname,'Step 4',
              'set station-isolation allowed vlan 4091 on ac1 profile 1',
              'set station-isolation on ac1 profile 1 radio 1',
              'set success')

    res1=res2=res3=1

    #operate

    #在AC1上配置station l2-isolation local switch mode
    EnterApProMode(switch1,1)
    SetCmd(switch1,'station-isolation allowed vlan add','4091')

    EnterApProMode(switch1,1)
    SetCmd(switch1,'radio 1')
    SetCmd(switch1,'station-isolation')

    #下发配置
    # WirelessApProfileApply(switch1,1)
    # IdleAfter(Ac_ap_syn_time)
    # for i in xrange(10):
        # IdleAfter(10)
        # data1 = SetCmd(switch1,'show wireless ap status')
        # if re.search('1\s+Managed Success',data1) is not None:
            # break
    res1 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

    EnterEnableMode(switch1)
    # data1 = SetCmd(switch1,'show wireless ap status')
    data2 = SetCmd(switch1,'show wireless ap profile',1)
    data3 = SetCmd(switch1,'show wireless ap profile 1 radio 1')
        
    #check
    # res1 = CheckLine(data1,ap1mac,'Managed','Success',IC=True)
    res2 = CheckLine(data2,'Station-isolation Allowed Vlan','4091',IC=True)
    res3 = CheckLine(data3,'Station Isolation','Enable',IC=True)


    #result
    printCheckStep(testname, 'Step 4',res1,res2,res3)

    ################################################################################
    #Step 5 
    # 操作
    # STA1 和 STA2 互ping
    #
    # 预期
    # STA1,STA2互相不能 ping 通
    ################################################################################
    printStep(testname,'Step 5',
              'STA1,STA2 ping each other failed')

    res5=res6=1

    #STA1,STA2互ping
    res5 = CheckPing(sta1,staticIp_sta2,mode='linux')
    res6 = CheckPing(sta2,staticIp_sta1,mode='linux')   
    res5 = 0 if res5 != 0 else 1
    res6 = 0 if res6 != 0 else 1

    #result
    printCheckStep(testname, 'Step 5',res5,res6)

    ################################################################################
    #Step 6 
    # 操作
    # 让sta都连接到ap 1的network1
    #
    # 预期
    # 关联成功，但两台sta无法ping通
    #########################################
    printStep(testname,'Step 6',
              'Let two stas connect to network1',
              'sta1 and sta2 ping each other failed') 

    res1=res2=1

    #operate
    #STA1 network1, STA2关联 network1
    res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)
    res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)
    IdleAfter(10)

    #手动配置STA1,STA2地址
    SetCmd(sta1,'\x03')
    SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
    SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask','255.255.255.0')
    SetCmd(sta2,'\x03')
    SetCmd(sta2,'dhclient -r',Netcard_sta2,promotePatten='#',promoteTimeout=60)
    SetCmd(sta2,'ifconfig',Netcard_sta2,staticIp_sta2,'netmask','255.255.255.0')

    #获取已配置地址
    data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
    data2 = SetCmd(sta2,'ifconfig -v',Netcard_sta2)
    SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
    SearchResult2 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data2,re.I)

    #check
    if None != SearchResult1: 
        if SearchResult1.group(1).strip() == staticIp_sta1:
            printRes('STA1 ip address: ' + staticIp_sta1)
            res3 = 0  
    else:
        res3 = 1
        printRes('Failed: Config static ip for STA1 failed') 
        
    if None != SearchResult2: 
        if SearchResult2.group(1).strip() == staticIp_sta2: 
            printRes('STA2 ip address: ' + staticIp_sta2)
            res4 = 0  
    else:
        res4 = 1
        printRes('Failed: Config static ip for STA2 failed')
                 
    res5 = CheckPing(sta1,staticIp_sta2,mode='linux')
    res6 = CheckPing(sta2,staticIp_sta1,mode='linux')
    res5 = 0 if 0 != res5 else 1
    res6 = 0 if 0 != res6 else 1


    #result
    printCheckStep(testname, 'Step 6',res1,res2,res3,res4,res5,res6)



    ################################################################################
    #Step 7 
    # 操作
    # STA1 和 STA2 下线后分别关联到 test1,test2，互ping
    #
    # 预期
    # STA1,STA2互相不能 ping 通
    ################################################################################
    printStep(testname,'Step 7',
              'STA1,STA2 disconnect',
              'STA1 connect to test1, STA2 connect to test2',
              'STA1,STA2 ping each other failed')

    res1=res2=res3=res4=res5=res6=1

    #operate

    #STA1,STA2下线
    WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
    WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

    #STA1,STA2重新分别关联到 test1 和test2
    res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)
    res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,dhcpFlag=False,bssid=ap1mac_type1_network2)
    IdleAfter(10)

    #手动配置STA1,STA2地址
    SetCmd(sta1,'\x03')
    SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
    SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask','255.255.255.0')
    SetCmd(sta2,'\x03')
    SetCmd(sta2,'dhclient -r',Netcard_sta2,promotePatten='#',promoteTimeout=60)
    SetCmd(sta2,'ifconfig',Netcard_sta2,staticIp_sta2,'netmask','255.255.255.0')

    #获取已配置地址
    data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
    data2 = SetCmd(sta2,'ifconfig -v',Netcard_sta2)
    SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
    SearchResult2 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data2,re.I)

    #check
    if None != SearchResult1: 
        if SearchResult1.group(1).strip() == staticIp_sta1:
            printRes('STA1 ip address: ' + staticIp_sta1)
            res3 = 0  
    else:
        res3 = 1
        printRes('Failed: Config static ip for STA1 failed') 
        
    if None != SearchResult2: 
        if SearchResult2.group(1).strip() == staticIp_sta2: 
            printRes('STA2 ip address: ' + staticIp_sta2)
            res4 = 0  
    else:
        res4 = 1
        printRes('Failed: Config static ip for STA2 failed')

    #STA1,STA2互ping
    res5 = CheckPing(sta1,staticIp_sta2,mode='linux')
    res6 = CheckPing(sta2,staticIp_sta1,mode='linux')   
    res5 = 0 if 0 != res5 else 1
    res6 = 0 if 0 != res6 else 1

    #result
    printCheckStep(testname, 'Step 7',res1,res2,res3,res4,res5,res6)

    ################################################################################
    #Step 8
    # 操作
    # 在ac1上通过 profile->radio->命令station-isolation，关闭二层隔离
    # 在ac1上通过 profile命令station-isolation allowed vlan remove 4091，关闭二层隔离，并下发配置
    #
    # 预期
    # Show wireless ap profile 1 radio 1显示
    # 有：Station Isolation................ Disable
    # show wireless ap profile 1显示
    # 有Station-isolation Allowed Vlan................. -----
    # 配置下发成功，AP1的配置状态为success
    ################################################################################
    printStep(testname,'Step 8',
              'Config "no station-isolation" on profile',
              'Config "station-isolation allowed vlan remove 4091"',
              'Apply the profiles to APs, check the configuration')

    res1=res2=1

    #operate

    #配置 station-isolation
    EnterApProMode(switch1,1)
    SetCmd(switch1,'station-isolation allowed vlan remove 4091')
    SetCmd(switch1,'radio 1')
    SetCmd(switch1,'no station-isolation')



    #下发至 AP

    # WirelessApProfileApply(switch1,1)

    # IdleAfter(Ac_ap_syn_time)
    res1 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
    EnterEnableMode(switch1)
    # data1 = SetCmd(switch1,'show wireless ap status')
    data2 = SetCmd(switch1,'show wireless ap profile 1 radio 1')
    data3 = SetCmd(switch1,'show wireless ap profile',1)

    #check
    # res1 = CheckLine(data1,ap2mac,'Managed','Success',IC=True)
    res2 = CheckLine(data2,'Station Isolation','Disable',IC=True)
    res3 = CheckLine(data3,'Station-isolation Allowed Vlan','-----',IC=True)

    #RDM34910
    # if res1 != 0:
        # for tmpCounter in xrange(0,6):
            # IdleAfter('10')
            # data1 = SetCmd(switch1,'show wireless ap status')
            # res1 = CheckLine(data1,ap2mac,'Managed','Success',IC=True)
            # if res1 == 0:
                # break

    #result
    printCheckStep(testname, 'Step 8',res1,res2,res3)


    ################################################################################
    #Step 9 
    # 操作
    # sta1 sta2互ping
    #
    # 预期
    # 互相可以ping通
    #########################################
    printStep(testname,'Step 9',
              'sta1 and sta2 ping each other succeed') 

    res1=res2=1

    ##operate
    ##STA1 network1, STA2关联 network1
    #res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Var_network_name1,dhcpFlag=False,bssid=ap1mac_lower)
    #res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Var_network_name2,dhcpFlag=False,bssid=ap1mac_lower)
    #IdleAfter(10)

    ##手动配置STA1,STA2地址
    #SetCmd(sta1,'\x03')
    #SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
    #SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask','255.255.255.0')
    #SetCmd(sta2,'\x03')
    #SetCmd(sta2,'dhclient -r',Netcard_sta2,promotePatten='#',promoteTimeout=60)
    #SetCmd(sta2,'ifconfig',Netcard_sta2,staticIp_sta2,'netmask','255.255.255.0')

    ##获取已配置地址
    #data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
    #data2 = SetCmd(sta2,'ifconfig -v',Netcard_sta2)
    #SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
    #SearchResult2 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data2,re.I)

    ##check
    #if None != SearchResult1: 
        #if SearchResult1.group(1).strip() == staticIp_sta1:
            #printRes('STA1 ip address: ' + staticIp_sta1)
            #res3 = 0  
    #else:
        #res3 = 1
        #printRes('Failed: Config static ip for STA1 failed') 

    #if None != SearchResult2: 
        #if SearchResult2.group(1).strip() == staticIp_sta2: 
            #printRes('STA2 ip address: ' + staticIp_sta2)
            #res4 = 0  
    #else:
        #res4 = 1
        #printRes('Failed: Config static ip for STA2 failed')

    res5 = CheckPing(sta1,staticIp_sta2,mode='linux')
    res6 = CheckPing(sta2,staticIp_sta1,mode='linux')


    #result
    printCheckStep(testname, 'Step 9',res5,res6)

    ################################################################################
    #Step 10 
    # 操作
    # 让sta都下线后连接到ap 1的network1
    # sta1 sta2互相ping
    # 预期
    # 关联成功，两台sta可以互相ping通
    #########################################
    printStep(testname,'Step 10',
              'Let two stas connect to network1',
              'sta1 and sta2 ping each other succeed') 

    res1=res2=res3=res4=res5=res6=1

    #operate
    #STA1 network1, STA2关联 network1
    res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)
    res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)
    IdleAfter(10)

    #手动配置STA1,STA2地址
    SetCmd(sta1,'\x03')
    SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
    SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask','255.255.255.0')
    SetCmd(sta2,'\x03')
    SetCmd(sta2,'dhclient -r',Netcard_sta2,promotePatten='#',promoteTimeout=60)
    SetCmd(sta2,'ifconfig',Netcard_sta2,staticIp_sta2,'netmask','255.255.255.0')

    #获取已配置地址
    data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
    data2 = SetCmd(sta2,'ifconfig -v',Netcard_sta2)
    SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
    SearchResult2 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data2,re.I)

    #check
    if None != SearchResult1: 
        if SearchResult1.group(1).strip() == staticIp_sta1:
            printRes('STA1 ip address: ' + staticIp_sta1)
            res3 = 0  
    else:
        res3 = 1
        printRes('Failed: Config static ip for STA1 failed') 

    if None != SearchResult2: 
        if SearchResult2.group(1).strip() == staticIp_sta2: 
            printRes('STA2 ip address: ' + staticIp_sta2)
            res4 = 0  
    else:
        res4 = 1
        printRes('Failed: Config static ip for STA2 failed')

    res5 = CheckPing(sta1,staticIp_sta2,mode='linux')
    res6 = CheckPing(sta2,staticIp_sta1,mode='linux')

    #result
    printCheckStep(testname, 'Step 10',res1,res2,res3,res4,res5,res6)

    ################################################################################
    #Step 11
    #操作
    #Sta1,sta2下线后分别关联AP1的test1、test2，在sta1上ping sta2
    #
    #预期
    #能够 ping 通
    ################################################################################
    printStep(testname,'Step 11',
              'STA1 ping STA2',
              'Check if succeed')

    res1=res2=res3=res4=res5=res6=1

    #operate

    #STA1,STA2下线
    WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
    WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

    #STA1,STA2分别重新关联到 test1\test2
    res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)
    res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,dhcpFlag=False,bssid=ap1mac_type1_network2)
    IdleAfter(10)

    #手动配置STA1,STA2地址
    SetCmd(sta1,'\x03')
    SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
    SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask','255.255.255.0')
    SetCmd(sta2,'\x03')
    SetCmd(sta2,'dhclient -r',Netcard_sta2,promotePatten='#',promoteTimeout=60)
    SetCmd(sta2,'ifconfig',Netcard_sta2,staticIp_sta2,'netmask','255.255.255.0')

    #获取已配置地址
    data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
    data2 = SetCmd(sta2,'ifconfig -v',Netcard_sta2)
    SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
    SearchResult2 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data2,re.I)

    #check
    if None != SearchResult1: 
        if SearchResult1.group(1).strip() == staticIp_sta1:
            printRes('STA1 ip address: ' + staticIp_sta1)
            res3 = 0  
    else:
        res3 = 1
        printRes('Failed: Config static ip for STA1 failed') 
        
    if None != SearchResult2: 
        if SearchResult2.group(1).strip() == staticIp_sta2: 
            printRes('STA2 ip address: ' + staticIp_sta2)
            res4 = 0  
    else:
        res4 = 1
        printRes('Failed: Config static ip for STA2 failed')

    #STA1,STA2互ping
    res5 = CheckPing(sta1,staticIp_sta2,mode='linux')
    res6 = CheckPing(sta2,staticIp_sta1,mode='linux')   

    #result
    printCheckStep(testname, 'Step 11',res1,res2,res3,res4,res5,res6)

################################################################################
#Step 12
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 12',
          'Recover initial config')

#operate

# STA1,STA2解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

EnterNetworkMode(switch1,'2')
SetCmd(switch1,'vlan 4092')

#tunnel vlan中添加 4091
EnterWirelessMode(switch1)
SetCmd(switch1,'l2tunnel vlan-list add','4091')
# 
# #添加AP1
# EnterWirelessMode(switch1)
# SetCmd(switch1,'ap database',ap1mac)
# SetCmd(switch1,'profile 1')

#S3恢复初始配置
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'no switchport mode')
SetCmd(switch3,'switchport access vlan',Vlan20)
EnterInterfaceMode(switch3,s3p4)
SetCmd(switch3,'no switchport mode')
SetCmd(switch3,'switchport access vlan',Vlan30)
#下发至AP
WirelessApplyProfileWithCheck(switch1,['1','2'],[ap1mac,ap2mac])

#end
printTimer(testname, 'End')
