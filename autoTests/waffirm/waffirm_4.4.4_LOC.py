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
#     - lupingc RDM49074 2017.5.17
#     - zhangjxp RDM50657,RDM50617 2017.12.20
#*******************************************************************************

#Package

#Global Definition
staticIp_sta1 = '192.168.91.100'
staticIp_sta2 = '192.168.91.200'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.4.4'
avoiderror(testname)
printTimer(testname,'Start','test isolation to station of vap in local switch mode')

################################################################################
#Step 1
#操作
#Vlan 4091从tunnel vlan删除
# 在ac1修改network2的关联vlan为4091，下发配置。
# Sp3p3 ,s3p4改为trunk口，允许vlan 4091通过，s3p3 native vlan为20 s3p4 native vlan为30
#
#预期
#Ac1：tunnel vlan list中没有4091
# Show wireless network 2看到default vlan 为4091。
# S3： Show interface Ethernet s3p3/s3p4,看到为trunk，allow vlan中包含4091
################################################################################
printStep(testname,'Step 1',
          'Delete vlan 4091 from tunnel vlan',
          'apply ap profile to ap1,',
          'Change s3p3,s3p4 to Trunk')

res1=res2=res3=res4=1
#operate
# 
# #关闭AP1管理,重启AP1
# EnterWirelessMode(switch1)
# SetCmd(switch1,'no','ap database',ap1mac)
# RebootAp('AC',AC=switch1,MAC=ap1mac,AP=ap1)

# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    #tunnel vlan中删除 4091
    EnterWirelessMode(switch1)
    SetCmd(switch1,'l2tunnel vlan-list remove',Vlan4091)

#修改network2关联vlan为4091
EnterNetworkMode(switch1, '2')
SetCmd(switch1,'vlan '+Vlan4091)
EnterEnableMode(switch1)
IdleAfter(5)
# IdleAfter(60)

#配置s3p3,s3p4为Trunk口，allowed vlan 4091，native vlan为20
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk allowed vlan',Vlan4091)
SetCmd(switch3,'switchport trunk native vlan',Vlan20)
EnterInterfaceMode(switch3,s3p4)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk allowed vlan',Vlan4091)
SetCmd(switch3,'switchport trunk native vlan',Vlan30)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless l2tunnel vlan-list')
data2 = SetCmd(switch1,'show wireless network 1',timeout=5)

EnterEnableMode(switch3)
data3 = SetCmd(switch3,'show running-config interface',s3p3)
data4 = SetCmd(switch3,'show running-config interface',s3p4)


#check
res1 = CheckLine(data1,Vlan4091)
res1 = 0 if 0 != res1 else 1

res2 = CheckLine(data2,'Default VLAN',Vlan4091,IC=True)
res3 = CheckLineList(data3, [('switchport mode trunk'),
                             ('switchport trunk allowed vlan',Vlan4091),
                             ('switchport trunk native vlan',Vlan20)],IC=True)
res4 = CheckLineList(data4, [('switchport mode trunk'),
                             ('switchport trunk allowed vlan',Vlan4091),
                             ('switchport trunk native vlan',Vlan30)],IC=True)                            

#result
printCheckStep(testname, 'Step 1',res1,res2,res3,res4)

################################################################################
#Step 2
#操作
#将STA1和STA2均关联到 ap1 的网络test1
#（sta1和sta2网络地址为192,168.91.x，网关为192.168.91.1）
#
#预期
#
#成功关联
################################################################################

printStep(testname,'Step 2',
          'STA1 and STA2 connect to network 1,',
          'STA1 and STA2 dhcp and get 192.168.91.x ip')

res1=res2=res3=res4=1

#operate
#STA1 network1, STA2关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)
# IdleAfter(10)
IdleAfter(5)

#手动配置STA1,STA2地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask 255.255.255.0')
SetCmd(sta2,'\x03')
SetCmd(sta2,'dhclient -r',Netcard_sta2,promotePatten='#',promoteTimeout=60)
SetCmd(sta2,'ifconfig',Netcard_sta2,staticIp_sta2,'netmask 255.255.255.0')

#获取已配置地址
sta1_ipresult = GetStaIp(sta1,checkippool=staticIp_sta1)
sta1_ipv4 = sta1_ipresult['ip']
res3 = sta1_ipresult['res']

sta2_ipresult = GetStaIp(sta2,checkippool=staticIp_sta2)
sta2_ipv4 = sta2_ipresult['ip']
res4 = sta2_ipresult['res'] 

#result
printCheckStep(testname, 'Step 2',res1,res2,res3,res4)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2 + res3 + res4
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
# STA1 和 STA2 下线后分别关联到 test1,test2，互ping
#
# 预期
# STA1,STA2互相能 ping 通
################################################################################
printStep(testname,'Step 4',
          'STA1,STA2 disconnect',
          'STA1 connect to test1, STA2 connect to test2',
          'STA1,STA2 ping each other succeed')

res1=res2=res3=res4=res5=res6=1

#operate

#STA1,STA2下线
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

#STA1,STA2重新都关联到 test1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,dhcpFlag=False,bssid=ap1mac_type1_network2)
IdleAfter(10)

#手动配置STA1,STA2地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask 255.255.255.0')
SetCmd(sta2,'\x03')
SetCmd(sta2,'dhclient -r',Netcard_sta2,promotePatten='#',promoteTimeout=60)
SetCmd(sta2,'ifconfig',Netcard_sta2,staticIp_sta2,'netmask 255.255.255.0')

#获取已配置地址
sta1_ipresult = GetStaIp(sta1,checkippool=staticIp_sta1)
sta1_ipv4 = sta1_ipresult['ip']
res3 = sta1_ipresult['res']

sta2_ipresult = GetStaIp(sta2,checkippool=staticIp_sta2)
sta2_ipv4 = sta2_ipresult['ip']
res4 = sta2_ipresult['res'] 

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
printStep(testname,'Step 5',
          'STA1,STA2 disconnect',
          'STA1,STA2 connect to test2',
          'STA1,STA2 ping each other succeed')

res1=res2=res3=res4=res5=res6=1

#operate

#STA1,STA2下线
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

#STA1,STA2重新都关联到 test1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name2,dhcpFlag=False,bssid=ap1mac_type1_network2)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,dhcpFlag=False,bssid=ap1mac_type1_network2)
IdleAfter(10)

#手动配置STA1,STA2地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask 255.255.255.0')
SetCmd(sta2,'\x03')
SetCmd(sta2,'dhclient -r',Netcard_sta2,promotePatten='#',promoteTimeout=60)
SetCmd(sta2,'ifconfig',Netcard_sta2,staticIp_sta2,'netmask 255.255.255.0')

#获取已配置地址
sta1_ipresult = GetStaIp(sta1,checkippool=staticIp_sta1)
sta1_ipv4 = sta1_ipresult['ip']
res3 = sta1_ipresult['res']

sta2_ipresult = GetStaIp(sta2,checkippool=staticIp_sta2)
sta2_ipv4 = sta2_ipresult['ip']
res4 = sta2_ipresult['res']

#STA1,STA2互ping
res5 = CheckPing(sta1,staticIp_sta2,mode='linux')
res6 = CheckPing(sta2,staticIp_sta1,mode='linux')
IdleAfter(30)
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
# 配置下发成功，ap1的配置状态为success
################################################################################
printStep(testname,'Step 6',
          'Config station-isolation on network1',
          'Apply the profiles to APs, check the configuration')

res1=res2=1

#operate

#配置 station-isolation
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'station-isolation')

#下发至 ap1
res1 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
EnterEnableMode(switch1)
data2 = SetCmd(switch1,'show wireless network 1')

#check
res2 = CheckLine(data2,'Station-isolation','Enable',IC=True)

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
printStep(testname,'Step 7',
          'STA1 and STA2 can ping each other succeed')

res1=res2=1
#operate
#STA1,STA2下线
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

#STA1,STA2重新都关联到 test1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name2,dhcpFlag=False,bssid=ap1mac_type1_network2)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,dhcpFlag=False,bssid=ap1mac_type1_network2)
IdleAfter(10)

#手动配置STA1,STA2地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask 255.255.255.0')
SetCmd(sta2,'\x03')
SetCmd(sta2,'dhclient -r',Netcard_sta2,promotePatten='#',promoteTimeout=60)
SetCmd(sta2,'ifconfig',Netcard_sta2,staticIp_sta2,'netmask 255.255.255.0')


res3 = CheckPing(sta1,staticIp_sta2,mode='linux')
res4 = CheckPing(sta2,staticIp_sta1,mode='linux')
IdleAfter(30)
res3 = CheckPing(sta1,staticIp_sta2,mode='linux')
res4 = CheckPing(sta2,staticIp_sta1,mode='linux')   
                                             
#result
printCheckStep(testname, 'Step 7',res1,res2,res3,res4)

################################################################################
#Step 8 
# 操作
# STA1 和 STA2 下线后分别关联到 test1,test2，互ping
#
# 预期
# STA1,STA2互相能够 ping 通 （network1和network 2之间可以通）
################################################################################
printStep(testname,'Step 8',
          'STA1,STA2 disconnect',
          'STA1 connect to test1, STA2 connect to test2',
          'STA1,STA2 ping each other succeed')

res1=res2=res3=res4=res5=res6=1

#operate

#STA1,STA2下线
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

#STA1,STA2重新都关联到 test1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,dhcpFlag=False,bssid=ap1mac_type1_network2)
IdleAfter(10)

#手动配置STA1,STA2地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask 255.255.255.0')
SetCmd(sta2,'\x03')
SetCmd(sta2,'dhclient -r',Netcard_sta2,promotePatten='#',promoteTimeout=60)
SetCmd(sta2,'ifconfig',Netcard_sta2,staticIp_sta2,'netmask 255.255.255.0')

#获取已配置地址
sta1_ipresult = GetStaIp(sta1,checkippool=staticIp_sta1)
sta1_ipv4 = sta1_ipresult['ip']
res3 = sta1_ipresult['res']

sta2_ipresult = GetStaIp(sta2, checkippool=staticIp_sta2)
sta2_ipv4 = sta2_ipresult['ip']
res4 = sta2_ipresult['res']

#STA1,STA2互ping
res5 = CheckPing(sta1,staticIp_sta2,mode='linux')   
res6 = CheckPing(sta2,staticIp_sta1,mode='linux')
IdleAfter(30)
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

printStep(testname,'Step 9',
          'STA1,STA2 disconnect and connect to test1',
          'STA1,STA2 cannot ping each other')

res1=res2=res3=res4=1
res5=res6=0

#operate

#STA1,STA2下线
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

#STA1,STA2重新都关联到 test1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)
IdleAfter(10)

#手动配置STA1,STA2地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask 255.255.255.0')
SetCmd(sta2,'\x03')
SetCmd(sta2,'dhclient -r',Netcard_sta2,promotePatten='#',promoteTimeout=60)
SetCmd(sta2,'ifconfig',Netcard_sta2,staticIp_sta2,'netmask 255.255.255.0')

#获取已配置地址
sta1_ipresult = GetStaIp(sta1,checkippool=staticIp_sta1)
sta1_ipv4 = sta1_ipresult['ip']
res3 = sta1_ipresult['res']

sta2_ipresult = GetStaIp(sta2,checkippool=staticIp_sta2)
sta2_ipv4 = sta2_ipresult['ip']
res4 = sta2_ipresult['res']

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
# 配置下发成功，ap1的配置状态为success
################################################################################
printStep(testname,'Step 10',
          'Config no station-isolation on network1 of AC1',
          'Apply the profiles to APs, check the configuration')

res1=res2=1

#operate

#配置 station-isolation
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no station-isolation')

#下发至 ap1
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless ap status')
data2 = SetCmd(switch1,'show wireless network 1')

#check
res1 = CheckLine(data1,ap1mac,'Managed','Success',IC=True)
res2 = CheckLine(data2,'Station-isolation','Disable',IC=True)
#RDM34910
if res1 != 0:
    for tmpCounter in xrange(0,6):
        IdleAfter('10')
        data1 = SetCmd(switch1,'show wireless ap status')
        res1 = CheckLine(data1,ap1mac,'Managed','Success',IC=True)
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
printStep(testname,'Step 11',
          'STA1 ping STA2',
          'Check if succeed')

res1=res2=1

#operate
#STA1,STA2下线
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

#STA1,STA2重新都关联到 test1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)
IdleAfter(10)

#手动配置STA1,STA2地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'dhclient -r',Netcard_sta1,promotePatten='#',promoteTimeout=60)
SetCmd(sta1,'ifconfig',Netcard_sta1,staticIp_sta1,'netmask 255.255.255.0')
SetCmd(sta2,'\x03')
SetCmd(sta2,'dhclient -r',Netcard_sta2,promotePatten='#',promoteTimeout=60)
SetCmd(sta2,'ifconfig',Netcard_sta2,staticIp_sta2,'netmask 255.255.255.0')

res3 = CheckPing(sta1,staticIp_sta2,mode='linux')  
res4 = CheckPing(sta2,staticIp_sta1,mode='linux')
IdleAfter(30)
res3 = CheckPing(sta1,staticIp_sta2,mode='linux')
res4 = CheckPing(sta2,staticIp_sta1,mode='linux')  

#check

#result
printCheckStep(testname,'Step 11',res1,res2,res3,res4)

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
SetCmd(switch1,'vlan '+Vlan4092)

# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    #tunnel vlan中添加 4091
    EnterWirelessMode(switch1)
    SetCmd(switch1,'l2tunnel vlan-list add',Vlan4091)
    #S3恢复初始配置
    EnterInterfaceMode(switch3,s3p3)
    SetCmd(switch3,'no switchport mode')
    SetCmd(switch3,'switchport access vlan',Vlan20)
    EnterInterfaceMode(switch3,s3p4)
    SetCmd(switch3,'no switchport mode')
    SetCmd(switch3,'switchport access vlan',Vlan30)
else:
    EnterConfigMode(switch3)
    SetCmd(switch3,'Interface ',s3p3)
    SetCmd(switch3,'switchport mode trunk')
    SetCmd(switch3,'switchport trunk allowed vlan all')
    SetCmd(switch3,'switchport trunk native vlan',Vlan20)
    SetCmd(switch3,'Interface ',s3p4)
    SetCmd(switch3,'switchport mode trunk')
    SetCmd(switch3,'switchport trunk allowed vlan all')
    SetCmd(switch3,'switchport trunk native vlan',Vlan30)
#下发至AP    
WirelessApplyProfileWithCheck(switch1,['1','2'],[ap1mac,ap2mac])

#end
printTimer(testname, 'End')