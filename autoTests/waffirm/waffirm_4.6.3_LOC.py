#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.6.3.py - test case 4.6.3 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
# 
# Date 2012-12-7 14:37:33
#
# Features:
# 4.6.3	本地转发功能测试1（二层转发）
# 测试目的：测试二层报文的本地转发
# 测试环境：同测试拓扑
# 测试描述：测试二层报文的本地转发
#
#*******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
#*******************************************************************************

#Package

#Global Definition
staticIpv6_sta1 = '2001:92::100'
staticIpv6_sta2 = '2001:92::200'
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if not testcentral:
    CMD_Add_ipv6_route_test1_to_test2_sta1 = 'route -A inet6 add '+ staticIpv6_sta2 + '/64 gw '+ If_vlan4091_s1_ipv6 +' dev '+ Netcard_sta1
    CMD_Add_ipv6_route_test2_to_test1_sta2 = 'route -A inet6 add '+ staticIpv6_sta1 + '/64 gw '+ If_vlan4092_s1_ipv6 +' dev '+ Netcard_sta2
    CMD_Del_ipv6_route_test1_to_test2_sta1 = 'route -A inet6 del '+ staticIpv6_sta2 + '/64 gw '+ If_vlan4091_s1_ipv6 +' dev '+ Netcard_sta1
    CMD_Del_ipv6_route_test2_to_test1_sta2 = 'route -A inet6 del '+ staticIpv6_sta1 + '/64 gw '+ If_vlan4092_s1_ipv6 +' dev '+ Netcard_sta2

#Source files

#Procedure Definition

#Functional Code

testname = 'TestCase 4.6.3'
avoiderror(testname)
printTimer(testname,'Start','test L2 switch in local switch mode')

################################################################################
#Step 1
#操作
# 修改AP1的管理vlan为vlan10，untagged-vlan为vlan 10。
# 修改三层交换机连接AP1的端口为trunk口，native vlan为vlan 10。
# 在AC1配置network1的SSID为test1，关联vlan4092，配置下发到AP1
#
#预期
#AP1能够被AC1管理，配置下发成功
################################################################################
printStep(testname,'Step 1',
          'Set AP1 management vlan-id to vlan 20,and untagged',
          'Switchport s3p3 to be trunk,native vlan 20')

res1=1

#operate
#在AC2上开启对AC1的三层发现
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery ip-list',StaticIpv4_ac1)  

i_times = 0
while i_times < 10:
    data0 = SetCmd(switch1,'show wireless peer-switch')
    if 0 == CheckLine(data0,StaticIpv4_ac2,'IP Poll',IC=True):
        break   
    i_times += 1
    IdleAfter(2)  
    
EnterWirelessMode(switch1)
EnterApProMode(switch1,'1')
SetCmd(switch1,'management vlan',Vlan20)
SetCmd(switch1,'ethernet native-vlan 20')
# SetCmd(ap1,'set management vlan-id',Vlan20)
# SetCmd(ap1,'set untagged-vlan vlan-id',Vlan20)
ApSetcmd(ap1,Ap1cmdtype,'set_management_vlanid',Vlan20)
ApSetcmd(ap1,Ap1cmdtype,'set_untagged_vlanid',Vlan20,commitflag=True)

EnterNetworkMode(switch1,1)
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan '+ Vlan4092)

#配置s3p3为Trunk 口,native vlan
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan20)
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan40)

#S3 上配置 vlan 4092
EnterConfigMode(switch3)
SetCmd(switch3,'vlan',Vlan4092)

#配置s1p1为Trunk 口,native vlan为40
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport mode trunk')
SetCmd(switch1,'switchport trunk native vlan',Vlan40)
#配置下发到AP1
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if not testcentral:
    WirelessApProfileApply(switch1,'1')
    res1 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac],eth_parameter=True)
else:
    res1 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#操作
#在AC1上面将vlan4092从l2-tunnel vlan-list中删除
#
#预期
#通过show wireless l2-tunnel vlan-list看不到vlan4092
################################################################################

printStep(testname,'Step 2',
          'Delete vlan 4092 from l2tunnel vlan')

res1=0

#operate
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    #tunnel vlan中删除 4092
    EnterWirelessMode(switch1)
    SetCmd(switch1,'l2tunnel vlan-list remove',Vlan4092)

    EnterEnableMode(switch1)
    data1 = SetCmd(switch1,'show wireless l2tunnel vlan-list')

    #check
    res1 = CheckLine(data1,Vlan4092)
    res1 = 0 if 0 != res1 else 1
else:
    res1 = 0

#result
printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#STA1和STA2连接到网络test1
#
#预期
#关联成功。客户端能够获取192.168.92.X网段的IP地址
################################################################################

printStep(testname,'Step 3',
          'STA1 and STA2 connect to network test1',
          'Check if STA1,STA2 can obtain 192.168.92.x address via dhcp')

res1=res2=res3=res4=-1

sta1_ipv4 = ''
sta2_ipv4 = ''

#operate
#STA1,STA2关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap1mac_lower)
#获取STA1,STA2的地址
sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool2)
sta1_ipv4 = sta1_ipresult['ip']
res3 = sta1_ipresult['res']

sta2_ipresult = GetStaIp(sta2,checkippool=Dhcp_pool2)
sta2_ipv4 = sta2_ipresult['ip']
res4 = sta2_ipresult['res']

#result
printCheckStep(testname, 'Step 3',res1,res2,res3,res4)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2 + res3 + res4
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 4
    #操作
    #STA1 ping STA2
    #
    #预期
    #能够 ping 通
    ################################################################################
    printStep(testname,'Step 4',
              'STA1 ping STA2')

    res1=1

    #operate
    res1 = CheckPing(sta1,sta2_ipv4,mode='linux')

    #check

    #result
    printCheckStep(testname,'Step 4',res1)

################################################################################
#Step 5
#操作
# 在AC2上面配置network 2的SSID为test2，关联vlan4092。
# 修改AP2的管理vlan为vlan 30，untagged-vlan为vlan 30。
# 修改三层交换机连接AP2的端口为trunk口，native vlan为vlan 30。
# 在AC2上面将配置下发到AP2
#
#预期
#AP2能够被AC2管理，配置下发成功
################################################################################
printStep(testname,'Step 5',
          'Set AP2 management vlan-id to vlan 30,and untagged',
          'Switchport s3p4 to be trunk,native vlan 30')

res1=res2=1
# !!!!!!!!!!!!!!!!!如果要是AC2能够管理AP2那么 有两种方法，AC1上自动部署，或者在
#!!!!!!!!!!!!!!!!!!AP2上直接配置，采用后者

#operate
EnterWirelessMode(switch2)
EnterApProMode(switch2,'2')
SetCmd(switch2,'management vlan',Vlan30)
SetCmd(switch2,'ethernet native-vlan 30')
# SetCmd(ap2,'set management vlan-id',Vlan30)
# SetCmd(ap2,'set untagged-vlan vlan-id',Vlan30)
ApSetcmd(ap2,Ap2cmdtype,'set_management_vlanid',Vlan30)
ApSetcmd(ap2,Ap2cmdtype,'set_untagged_vlanid',Vlan30,commitflag=True)

#AC1删除对AP2自动发现
EnterWirelessMode(switch1)
SetCmd(switch1,'no','discovery ip-list',Ap2_ipv4)
SetCmd(switch1,'no','discovery ipv6-list',Ap2_ipv6)

#配置AC2管理AP2，重启AP2
# SetCmd(ap2,'set managed-ap switch-address-1',StaticIpv4_ac2)
# SetCmd(ap2,'save-running')
ApSetcmd(ap2,Ap2cmdtype,'set_switch_address1',StaticIpv4_ac2)
ApSetcmd(ap2,Ap2cmdtype,'saverunning')
RebootAp('AP',AP=ap2)

if testcentral:
    #AC2 从tunnel vlan中删除 4092
    EnterWirelessMode(switch2)
    SetCmd(switch2,'l2tunnel vlan-list remove',Vlan4092)
else:
    pass

#配置s3p4,s3p2为Trunk 口,native vlan
EnterInterfaceMode(switch3,s3p4)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan30)
EnterInterfaceMode(switch3,s3p2)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan30)

#配置s2p1为Trunk 口,native vlan
EnterInterfaceMode(switch2,s2p1)
SetCmd(switch2,'switchport mode trunk')
SetCmd(switch2,'switchport trunk native vlan',Vlan30)
WirelessApplyProfileWithCheck(switch2,['2'],[ap2mac])
EnterEnableMode(switch2)
#check
for tmpCounter in xrange(0,30):	
	data1 = SetCmd(switch2,'show wireless ap status')
	res1 = CheckLine(data1,ap2mac,Ap2_ipv4,'Managed','Success',IC=True)
	res2 = CheckNoLineList(data1,[('\*'+ap2mac,Ap2_ipv4,'Managed','Success')],IC=True)
	if res1 == 0 and res2 == 0:
		break
	IdleAfter('5')

#result
printCheckStep(testname, 'Step 5',res1,res2)

################################################################################
#Step 6
#操作
#客户端STA2连接到网络test2
#
#预期
#关联成功，STA2能够获取192.168.92.X网段的IP地址
################################################################################
printStep(testname,'Step 6',
          'STA2 connect to network test2',
          'Check if STA2 can obtain 192.168.92.x address via dhcp')

res1=res2=-1

sta2_ipv4 = ''

#operate
#STA2关联 network1
res1 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,bssid=ap2mac_type1_network2)

#获取STA2的地址
sta2_ipresult = GetStaIp(sta2,checkippool=Dhcp_pool2)
sta2_ipv4 = sta2_ipresult['ip']
res2 = sta2_ipresult['res']

#result
printCheckStep(testname, 'Step 6',res1,res2)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 7
    #操作
    #用STA1的ipv4地址ping STA2的ipv4地址，用STA1的ipv6地址ping STA2的ipv6地址
    #（ipv6地址手动配置为与ac网段的地址）
    #
    #预期
    #能够ping通，在AC1使用命令show arp可看到STA1和STA2的mac对应的port为capwaptnl
    #隧道类型，使用show mac-address-table命令看到STA1和STA2的Ports类型为capwaptnl
    #隧道类型，ipv6流量使用show ipv6 neighbors查看
    ################################################################################

    printStep(testname,'Step 7',
              'STA1 ping STA2 via ipv4 and ipv6')

    res1=res2=res3=res4=-1

    #operate

    #手动配置STA1，STA2 ipv6 地址
    SetCmd(sta1,'\x03')
    SetCmd(sta1,'ifconfig '+ Netcard_sta1 + ' inet6 add',staticIpv6_sta1 + '/64')
    SetCmd(sta2,'\x03')
    SetCmd(sta2,'ifconfig '+ Netcard_sta2 + ' inet6 add',staticIpv6_sta2 + '/64')

    #ping,ping6
    res1 = CheckPing(sta1,sta2_ipv4,mode='linux')
    CheckPing(sta2,sta1_ipv4,mode='linux')
    SetCmd(sta1,'ping6',staticIpv6_sta2,promotePatten = 'PING',promoteTimeout=10)
    IdleAfter(15)
    data0 = SetCmd(sta1,'\x03',timeout = 1)

    #查看表项
    IdleAfter(10)
    EnterEnableMode(switch1)
    data3 = SetCmd(switch1,'show mac-address-table')
    data4 = SetCmd(switch1,'show arp')
    #data4 = SetCmd(switch1,'show ipv6 neighbors')

    #check
    res2 = int(str(GetValueBetweenTwoValuesInData(data0,'transmitted,','received')).strip()) 
    res2 = 0 if res2 > 0 else 1
    # res3 = CheckLineList(data3,[(sta1mac),(sta2mac)],IC=True)                 
    #check
    #result
    printCheckStep(testname,'Step 7',res1,res2)

################################################################################
#Step 8
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 8',
          'Recover initial config')
#operate

#AC2关闭对AC1 的发现
EnterWirelessMode(switch2)
SetCmd(switch2,'no','discovery ip-list',StaticIpv4_ac1)

#解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)
    
#删除手工配置ipv6 地址
SetCmd(sta1,'\x03')                                                                                                    
SetCmd(sta1,'ifconfig '+ Netcard_sta1 + ' inet6 del',staticIpv6_sta1 + '/64')
SetCmd(sta2,'\x03')
SetCmd(sta2,'ifconfig '+ Netcard_sta2 + ' inet6 del',staticIpv6_sta2 + '/64')

#删除dhcp binding,arp,mac-address-table,ipv6 neighbors信息
EnterEnableMode(switch1)
SetCmd(switch1,'clear ip dhcp binding all')
SetCmd(switch1,'clear arp traffic')
SetCmd(switch1,'clear mac-address-table dynamic')
SetCmd(switch1,'clear ipv6 neighbors')

#清除management vlan 配置
EnterWirelessMode(switch1)
EnterApProMode(switch1,'1')
SetCmd(switch1,'no','management vlan')
SetCmd(switch1,'ethernet native-vlan 1')
# SetCmd(ap1,'set management vlan-id',1)
# SetCmd(ap1,'set untagged-vlan vlan-id',1)
ApSetcmd(ap1,Ap1cmdtype,'set_management_vlanid','1')
ApSetcmd(ap1,Ap1cmdtype,'set_untagged_vlanid','1',commitflag=True)

EnterWirelessMode(switch2)
EnterApProMode(switch2,'2')
SetCmd(switch2,'no','management vlan')
SetCmd(switch2,'ethernet native-vlan 1')
# SetCmd(ap2,'set management vlan-id',1)
# SetCmd(ap2,'set untagged-vlan vlan-id',1)
ApSetcmd(ap2,Ap2cmdtype,'set_management_vlanid','1')
ApSetcmd(ap2,Ap2cmdtype,'set_untagged_vlanid','1',commitflag=True)

#恢复拓扑配置
#AC1
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan ' + Vlan4091)
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'no switchport mode')
SetCmd(switch1,'switchport access vlan',Vlan40)

#AC2
EnterInterfaceMode(switch2,s2p1)
SetCmd(switch2,'no switchport mode')
SetCmd(switch2,'switchport access vlan',Vlan30)
#RDM37511
EnterWirelessMode(switch2)
SetCmd(switch2,'peer-group 2')
IdleAfter(5)
SetCmd(switch2,'peer-group 1')

# AC1&AC3集中转发、本地转发差异化配置，testcentral为True代表集中转发配置
if testcentral:
    #tunnel vlan中添加 4092
    EnterWirelessMode(switch1)
    SetCmd(switch1,'l2tunnel vlan-list add',Vlan4092)
    #tunnel vlan中添加 4092
    EnterWirelessMode(switch2)
    SetCmd(switch2,'l2tunnel vlan-list add',Vlan4092)
    EnterInterfaceMode(switch3,s3p3)
    SetCmd(switch3,'no switchport mode')
    SetCmd(switch3,'switchport access vlan',Vlan20)
    EnterInterfaceMode(switch3,s3p4)
    SetCmd(switch3,'no switchport mode')
    SetCmd(switch3,'switchport access vlan',Vlan30)
else:
    EnterInterfaceMode(switch3,s3p3)
    SetCmd(switch3,'switchport mode trunk')
    SetCmd(switch3,'switchport trunk native vlan 20')
    EnterInterfaceMode(switch3,s3p4)
    SetCmd(switch3,'switchport mode trunk')
    SetCmd(switch3,'switchport trunk native vlan 30')
    #删除test1 至 test2 ipv6 路由
    SetCmd(sta1,CMD_Del_ipv6_route_test1_to_test2_sta1)
    #删除test2 至 test1 ipv6 路由
    SetCmd(sta2,CMD_Del_ipv6_route_test2_to_test1_sta2)
    
EnterInterfaceMode(switch3,s3p2)
SetCmd(switch3,'no switchport mode')
SetCmd(switch3,'switchport access vlan',Vlan30)
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'no switchport mode')
SetCmd(switch3,'switchport access vlan',Vlan40)
#S3 上删除 vlan 4092
EnterConfigMode(switch3)
SetCmd(switch3,'no','vlan',Vlan4092)
# S3 Vlan20配置IP
EnterInterfaceMode(switch3,'vlan '+Vlan20)
IdleAfter(Vlan_Idle_time)
SetIpAddress(switch3,If_vlan20_s3_ipv4,'255.255.255.0')
SetCmd(switch3,'ipv6 address',If_vlan20_s3_ipv6 + '/64')
#配置下发到AP1
WirelessApProfileApply(switch1,'1')
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if not testcentral:
    WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac],eth_parameter=True)  
    
#AC1添加对AP2的三层发现
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',Ap2_ipv4)
SetCmd(switch1,'discovery ipv6-list',Ap2_ipv6)

#配置AC2管理AP2，重启AP2
# SetCmd(ap2,'set managed-ap switch-address-1')
# SetCmd(ap2,'save-running')
ApSetcmd(ap2,Ap2cmdtype,'set_switch_address1')
ApSetcmd(ap2,Ap2cmdtype,'saverunning')
RebootAp('AP',AP=ap2)


# SetCmd(switch1,'end')
# SetCmd(switch2,'end')
# SetCmd(switch3,'end')
    
#end
printTimer(testname, 'End')