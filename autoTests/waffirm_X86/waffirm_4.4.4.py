#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.4.4.py - test case 4.4.4 of waffirm_new
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
# 4.4.4	本地转发模式下对vap下的所有用户实现隔离
# 测试目的：本地转发模式下对vap下的所有用户实现隔离
# 测试环境：见测试拓扑
# 测试描述：本地转发模式下，通过在network下配置隔离功能，可以让该vap下关联的
# 所有无线用户实现二层隔离，该vap和其他vap的用户不隔离
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package

#Global Definition
staticIp_sta1 = '192.168.92.100'
staticIp_sta2 = '192.168.92.200'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.4.4'
printTimer(testname,'Start','test isolation to station of vap in local switch mode')

################################################################################
#Step 1
#操作
#Vlan 4092从tunnel vlan删除
# 在ac1修改network1的关联vlan为4092，下发配置。
# Sp3p3 ,s3p4改为trunk口，允许vlan 4092通过，native vlan为20
#
#预期
#Ac1：tunnel vlan list中没有4092
# Show wireless network 2看到default vlan 为4092。
# S3： Show interface Ethernet s3p3/s3p4,看到为trunk，allow vlan中包含4092
################################################################################
printStep(testname,'Step 1',\
          'Delete vlan 4092 from tunnel vlan',\
          'apply ap profile to ap2,',\
          'Change s3p3,s3p4 to Trunk')

res1=res2=res3=res4=1
#operate
#tunnel vlan中删除 4092
EnterWirelessMode(switch1)
SetCmd(switch1,'l2tunnel vlan-list remove',Vlan4092)

#修改network2关联vlan为4092
EnterNetworkMode(switch1, '1')
SetCmd(switch1,'vlan '+Vlan4092)
# WirelessApProfileApply(switch1,'2')

#配置s3p3,s3p4为Trunk口，allowed vlan 4091，native vlan为20
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk allowed vlan',Vlan4092)
SetCmd(switch3,'switchport trunk native vlan',Vlan20)
EnterInterfaceMode(switch3,s3p4)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk allowed vlan',Vlan4092)
SetCmd(switch3,'switchport trunk native vlan',Vlan30)

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless l2tunnel vlan-list')
data2 = SetCmd(switch1,'show wireless network 1',timeout=3)

EnterEnableMode(switch3)
data3 = SetCmd(switch3,'show running-config interface',s3p3)
data4 = SetCmd(switch3,'show running-config interface',s3p4)
# IdleAfter(Ac_ap_syn_time)
WirelessApplyProfileWithCheck(switch1,['2'],[ap2mac])
#check
res1 = CheckLine(data1,Vlan4092)
res1 = 0 if 0 != res1 else 1

res2 = CheckLine(data2,'Default VLAN',Vlan4092,IC=True)
res3 = CheckLineList(data3, [('switchport mode trunk'), \
                             ('switchport trunk allowed vlan',Vlan4092), \
                             ('switchport trunk native vlan',Vlan20)],IC=True)
res4 = CheckLineList(data4, [('switchport mode trunk'), \
                             ('switchport trunk allowed vlan',Vlan4092), \
                             ('switchport trunk native vlan',Vlan30)],IC=True)                            

#result
printCheckStep(testname, 'Step 1',res1,res2,res3,res4)

################################################################################
#Step 2
#操作
#将STA1和STA2均关联到 AP2 的网络test1
#（sta1和sta2网络地址为192,168.92.x，网关为192.168.92.1）
#
#预期
#
#成功关联
################################################################################

printStep(testname,'Step 2',\
          'STA1 and STA2 connect to network 1,',\
          'STA1 and STA2 dhcp and get 192.168.92.x ip')

res1=res2=res3=res4=1

#operate
#STA1 network1, STA2关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap2mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,dhcpFlag=False,bssid=ap2mac_lower)
IdleAfter(10)

#手动配置STA1,STA2地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask 255.255.255.0')
SetCmd(sta2,'\x03')
SetCmd(sta2,'dhclient -r',Netcard_sta2,promotePatten='#',promoteTimeout=60)
SetCmd(sta2,'ifconfig',Netcard_sta2,staticIp_sta2,'netmask 255.255.255.0')

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

################################################################################
#Step 3
#操作
#STA1和STA2互ping
#
#预期
#能够 ping 通
################################################################################

printStep(testname,'Step 3',\
          'STA1 and STA2 ping each other',\
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
# STA1 和 STA2 下线后分别关联到 test1,test2，互ping
#
# 预期
# STA1,STA2互相能 ping 通
################################################################################
printStep(testname,'Step 4',\
          'STA1,STA2 disconnect',\
          'STA1 connect to test1, STA2 connect to test2',\
          'STA1,STA2 ping each other succeed')

res1=res2=res3=res4=res5=res6=1

#operate

#STA1,STA2下线
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

#STA1,STA2重新都关联到 test1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap2mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,dhcpFlag=False,bssid=ap2mac_type1_network2)
IdleAfter(10)

#手动配置STA1,STA2地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask 255.255.255.0')
SetCmd(sta2,'\x03')
SetCmd(sta2,'dhclient -r',Netcard_sta2,promotePatten='#',promoteTimeout=60)
SetCmd(sta2,'ifconfig',Netcard_sta2,staticIp_sta2,'netmask 255.255.255.0')

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
printCheckStep(testname, 'Step 4',res1,res2,res3,res4,res5,res6)

################################################################################
#Step 5 
# 操作
# STA1 和 STA2 下线后都关联到 test2，互ping
#
# 预期
# STA1,STA2互相能 ping 通
################################################################################
printStep(testname,'Step 5',\
          'STA1,STA2 disconnect',\
          'STA1,STA2 connect to test2',\
          'STA1,STA2 ping each other succeed')

res1=res2=res3=res4=res5=res6=1
#operate

#STA1,STA2下线
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

#STA1,STA2重新都关联到 test1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name2,dhcpFlag=False,bssid=ap2mac_type1_network2)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,dhcpFlag=False,bssid=ap2mac_type1_network2)
IdleAfter(10)

#手动配置STA1,STA2地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask 255.255.255.0')
SetCmd(sta2,'\x03')
SetCmd(sta2,'dhclient -r',Netcard_sta2,promotePatten='#',promoteTimeout=60)
SetCmd(sta2,'ifconfig',Netcard_sta2,staticIp_sta2,'netmask 255.255.255.0')

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
printCheckStep(testname, 'Step 5',res1,res2,res3,res4,res5,res6)

################################################################################
#Step 6 
# 操作
# 在AC1 network1 配置命令station-isolation，设置二层隔离，并下发配置。
#
# 预期
# Show wireless network 1显示有：
# Station-isolation................ Enable
# 配置下发成功，AP2的配置状态为success
################################################################################
printStep(testname,'Step 6',\
          'Config station-isolation on network1',\
          'Apply the profiles to APs, check the configuration')

res1=res2=1

#operate

#配置 station-isolation
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'station-isolation')

#下发至 AP2
# WirelessApProfileApply(switch1,'2')

# IdleAfter(Ac_ap_syn_time)
res1 = WirelessApplyProfileWithCheck(switch1,['2'],[ap2mac])
EnterEnableMode(switch1)
# data1 = SetCmd(switch1,'show wireless ap status')
data2 = SetCmd(switch1,'show wireless network 1')

#check
# res1 = CheckLine(data1,ap2mac,'Managed','Success',IC=True)
res2 = CheckLine(data2,'Station-isolation','Enable',IC=True)
#RDM34910
# if res1 != 0:
    # for tmpCounter in xrange(0,6):
        # IdleAfter('10')
        # data1 = SetCmd(switch1,'show wireless ap status')
        # res1 = CheckLine(data1,ap2mac,'Managed','Success',IC=True)
        # if res1 == 0:
            # break

#result
printCheckStep(testname, 'Step 6',res1,res2)

################################################################################
#Step 7
#
# 操作 
# STA1和STA2互ping
#
# 预期
# STA1和STA2能够ping通 （network 2没有配置隔离）
################################################################################
printStep(testname,'Step 7',\
          'STA1 and STA2 can ping each other succeed')

res1=res2=1
#operate
res1 = CheckPing(sta1,staticIp_sta2,mode='linux')
res2 = CheckPing(sta2,staticIp_sta1,mode='linux')
IdleAfter(30)
res1 = CheckPing(sta1,staticIp_sta2,mode='linux')
res2 = CheckPing(sta2,staticIp_sta1,mode='linux')   
                                             
#result
printCheckStep(testname, 'Step 7',res1,res2)

################################################################################
#Step 8 
# 操作
# STA1 和 STA2 下线后分别关联到 test1,test2，互ping
#
# 预期
# STA1,STA2互相能够 ping 通 （network1和network 2之间可以通）
################################################################################
printStep(testname,'Step 8',\
          'STA1,STA2 disconnect',\
          'STA1 connect to test1, STA2 connect to test2',\
          'STA1,STA2 ping each other succeed')

res1=res2=res3=res4=res5=res6=1

#operate

#STA1,STA2下线
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

#STA1,STA2重新都关联到 test1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap2mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,dhcpFlag=False,bssid=ap2mac_type1_network2)
IdleAfter(10)

#手动配置STA1,STA2地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask 255.255.255.0')
SetCmd(sta2,'\x03')
SetCmd(sta2,'dhclient -r',Netcard_sta2,promotePatten='#',promoteTimeout=60)
SetCmd(sta2,'ifconfig',Netcard_sta2,staticIp_sta2,'netmask 255.255.255.0')

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
printCheckStep(testname, 'Step 8',res1,res2,res3,res4,res5,res6)

################################################################################
#Step 9 
# 操作
# STA1 和 STA2 下线后再都关联到 test1 后，互ping
#
# 预期
# STA1,STA2互相 ping 不通 （network 1配置了隔离）
################################################################################

printStep(testname,'Step 9',\
          'STA1,STA2 disconnect and connect to test1',\
          'STA1,STA2 cannot ping each other')

res1=res2=res3=res4=1
res5=res6=0

#operate

#STA1,STA2下线
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

#STA1,STA2重新都关联到 test1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap2mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,dhcpFlag=False,bssid=ap2mac_lower)
IdleAfter(10)

#手动配置STA1,STA2地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask 255.255.255.0')
SetCmd(sta2,'\x03')
SetCmd(sta2,'dhclient -r',Netcard_sta2,promotePatten='#',promoteTimeout=60)
SetCmd(sta2,'ifconfig',Netcard_sta2,staticIp_sta2,'netmask 255.255.255.0')

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
printCheckStep(testname, 'Step 9',res1,res2,res3,res4,res5,res6)

################################################################################
#Step 10
# 操作
# 在AC1 network1 执行no station-isolation关闭二层隔离功能，并下发配置
#
# 预期
# Show wireless network 1显示有：
# Station Isolation.................. disable
# 配置下发成功，AP2的配置状态为success
################################################################################
printStep(testname,'Step 10',\
          'Config no station-isolation on network1 of AC1',\
          'Apply the profiles to APs, check the configuration')

res1=res2=1

#operate

#配置 station-isolation
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no station-isolation')

#下发至 AP2
# WirelessApProfileApply(switch1,'2')

# IdleAfter(Ac_ap_syn_time)
WirelessApplyProfileWithCheck(switch1,['2'],[ap2mac])
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless ap status')
data2 = SetCmd(switch1,'show wireless network 1')

#check
res1 = CheckLine(data1,ap2mac,'Managed','Success',IC=True)
res2 = CheckLine(data2,'Station-isolation','Disable',IC=True)
#RDM34910
if res1 != 0:
    for tmpCounter in xrange(0,6):
        IdleAfter('10')
        data1 = SetCmd(switch1,'show wireless ap status')
        res1 = CheckLine(data1,ap2mac,'Managed','Success',IC=True)
        if res1 == 0:
            break

#result
printCheckStep(testname, 'Step 10',res1,res2)

################################################################################
#Step 11
#操作
#STA1 ping STA2
#
#预期
#能够 ping 通
################################################################################
printStep(testname,'Step 11',\
          'STA1 ping STA2',\
          'Check if succeed')

res1=res2=1

#operate

res1 = CheckPing(sta1,staticIp_sta2,mode='linux')  
res2 = CheckPing(sta2,staticIp_sta1,mode='linux')
#check

#result
printCheckStep(testname,'Step 11',res1,res2)

################################################################################
#Step 12
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 12',\
          'Recover initial config')

#operate

# STA1,STA2解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

EnterNetworkMode(switch1,'1')
SetCmd(switch1,'vlan '+Vlan4091)

#tunnel vlan中添加 4092
EnterWirelessMode(switch1)
SetCmd(switch1,'l2tunnel vlan-list add',Vlan4092)

#下发至AP
# WirelessApProfileApply(switch1,'1')
# IdleAfter(5)

#S3恢复初始配置
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'no switchport mode')
SetCmd(switch3,'switchport access vlan',Vlan20)
EnterInterfaceMode(switch3,s3p4)
SetCmd(switch3,'no switchport mode')
SetCmd(switch3,'switchport access vlan',Vlan30)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# IdleAfter(Ac_ap_syn_time)

#end
printTimer(testname, 'End')