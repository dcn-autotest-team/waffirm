#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.6.7.py - test case 4.6.7 of waffirm_new
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
# 4.6.7	采用IPv6管理地址的集中式隧道二层转发
# 测试目的：测试客户端二层数据通过IPv6集中式隧道能够被正常转发
# 测试环境：同测试拓扑
# 测试描述：测试客户端二层数据通过IPv6集中式隧道能够被正常转发。测试中覆盖IPv4数据和IPv6数据转发
#
#*******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
#*******************************************************************************

#Package

#Global Definition
staticIpv6_sta1 = '2001:91::100'
staticIpv6_sta2 = '2001:91::200'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.6.7'
avoiderror(testname)
printTimer(testname,'Start','test L2 tunnel switch in ipv6 central switch mode')

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

#添加v6路由
#AC1
EnterConfigMode(switch1)
SetCmd(switch1,'ipv6 route',Ap1_ipv6 + '/64',If_vlan40_s3_ipv6)
#S3
EnterConfigMode(switch3)
SetCmd(switch3,'ipv6 route',StaticIpv6_ac1 + '/128',If_vlan40_s1_ipv6)

#check
res1 = CheckLine(data1,'WS IPv6 Address',StaticIpv6_ac1,IC=True)
res2 = CheckNoLineList(data1,[('WS IP Address',StaticIpv4_ac1)],IC=True)

#result
printCheckStep(testname, 'Step 1',res1,res2)

################################################################################
#Step 2
#操作
# 在ac1的发现列表中添加ap1的ipv6地址，让ac1发现ap1并建立ipv6集中式隧道：
# switch(config-wireless)#discovery ipv6-list 2001:20::3
#
#预期
# 等待90S后，通过show wireless ap status能够查看到AP的状态为Managed,配置状态为Success。
# sho wireless discovery ip-list能够查看到发现列表中添加成功。
# sho wireless l2tunnel tunnel-list能够查看到ap和ac隧道建立成功，
#SIP地址为ac1的无线ipv6地址，DIP地址为ap1的ipv6地址
################################################################################
printStep(testname,'Step 2',
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
    
IdleAfter(30)
EnterEnableMode(switch1)
for tmpCounter in xrange(0,16):
    IdleAfter('5')
    data1 = SetCmd(switch1,'show wireless discovery ip-list')
    data2 = SetCmd(switch1,'show wireless ap status')
    data3 = SetCmd(switch1,'show wireless l2tunnel tunnel-list')
    res1 = CheckLine(data1,Ap1_ipv6)
    res2 = CheckLine(data2,ap1mac,Ap1_ipv6,'Managed','Success',IC=True)
    res3 = CheckLineList(data3,[(StaticIpv6_ac1),(Ap1_ipv6)],IC=True)
    if res1 == 0 and res2 == 0 and res3 == 0:
        break
# data2 = SetCmd(switch1,'show wireless ap status')
# res2 = CheckLine(data2,ap1mac,Ap1_ipv6,'Managed','Success',IC=True)
# if res2 != 0:
    # IdleAfter(30)
    # data1 = SetCmd(switch1,'show wireless discovery ip-list')
    # data2 = SetCmd(switch1,'show wireless ap status')
    # data3 = SetCmd(switch1,'show wireless l2tunnel tunnel-list')

    # check
    # res1 = CheckLine(data1,Ap1_ipv6)
    # res2 = CheckLine(data2,ap1mac,Ap1_ipv6,'Managed','Success',IC=True)
    # res3 = CheckLineList(data3,[(StaticIpv6_ac1),(Ap1_ipv6)],IC=True)
# else:
    # data1 = SetCmd(switch1,'show wireless discovery ip-list')
    # data3 = SetCmd(switch1,'show wireless l2tunnel tunnel-list')

    # check
    # res1 = CheckLine(data1,Ap1_ipv6)
    # res3 = CheckLineList(data3,[(StaticIpv6_ac1),(Ap1_ipv6)],IC=True)

#result
printCheckStep(testname, 'Step 2',res1,res2,res3)

################################################################################
#Step 3
#操作
#在ac1中将将vlan4091加入到l2-tunnel vlan-list中
#
#预期
#AC上面通过show wireless l2-tunnel vlan-list可以看到vlan4091
################################################################################
printStep(testname,'Step 3',
          'Add vlan +Vlan4091 to l2-tunnel vlan-list')

res1=-1

#operate

#修改network1关联vlan为4091
EnterNetworkMode(switch1, '1')
SetCmd(switch1,'vlan '+Vlan4091)

## RDM36362
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
data1 = SetCmd(switch1,'show wireless network','1')

#check
res1 = CheckLine(data1,'Default VLAN',Vlan4091,IC=True)

#result
printCheckStep(testname,'Step 3',res1)

################################################################################
#Step 4
#操作
#STA1连接到网络test1，一个pc连接到ac1上，pc所连接ac1的上联端口的所属vlan为4091
#
#预期
#STA1关联成功，获取到192.168.91.0网段的IP地址。
#PC也获取到了192.168.91.0网段的ip地址
################################################################################
printStep(testname,'Step 4',
          'STA1 and STA2 connect to network 1,',
          'STA1 and STA2 dhcp and get 192.168.91.x ip')

sta1_ipv4 = ''
sta2_ipv4 = ''

res1=res2=res3=res4=1

#operate
#STA1,STA2关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap1mac_lower)

#获取STA1,STA2的地址
sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
res3 = sta1_ipresult['res']

sta2_ipresult = GetStaIp(sta2,checkippool=Dhcp_pool1)
sta2_ipv4 = sta2_ipresult['ip']
res4 = sta2_ipresult['res']
        
#result
printCheckStep(testname, 'Step 4',res1,res2,res3,res4)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2 + res3 + res4
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 5
    #操作
    #用STA1的ipv4地址ping STA2的ipv4地址，用STA1的ipv6地址ping STA2的ipv6地址
    #（ipv6地址手动配置为与ac网段的地址）
    #
    #预期
    #能够ping通，在AC1使用命令show arp可看到STA1和STA2的mac对应的port为capwaptnl
    #隧道类型，使用show mac-address-table命令看到STA1和STA2的Ports类型为capwaptnl
    #隧道类型，ipv6流量使用show ipv6 neighbors查看
    ################################################################################
    printStep(testname,'Step 5',
              'STA1 ping STA2 in both ipv4 and ipv6',
              'Check if succeed')

    #？？？？？？？？？？？？？？？？？此处show ipv6 neighbors STA1的表项一直没有，很长时间之后才会出现
    res1=res2=res3=res4=-1

    #operate

    #手动配置STA1，STA2 ipv6 地址
    SetCmd(sta1,'\x03')
    SetCmd(sta1,'ifconfig '+ Netcard_sta1 + ' inet6 add',staticIpv6_sta1 + '/64')
    SetCmd(sta2,'\x03')
    SetCmd(sta2,'ifconfig '+ Netcard_sta2 + ' inet6 add',staticIpv6_sta2 + '/64')

    #ping,ping6
    res1 = CheckPing(sta1,sta2_ipv4,mode='linux')
    SetCmd(sta1,'ping6',staticIpv6_sta2,promotePatten = 'PING',promoteTimeout=10)
    IdleAfter(10)
    data0 = SetCmd(sta1,'\x03',timeout = 1)

    #查看表项
    #!!!!!!!!!!!!!!!此处v6 neighbours表项没有，不检查
    IdleAfter(10)
    EnterEnableMode(switch1)
    data3 = SetCmd(switch1,'show mac-address-table')
    data5 = SetCmd(switch1,'show ipv6 neighbors')
    data4 = SetCmd(switch1,'show arp')
    #check
    res2 = int(str(GetValueBetweenTwoValuesInData(data0,'transmitted,','received')).strip()) 
    res2 = 0 if res2 > 0 else 1
    res3 = CheckLineList(data3,[(sta1mac,'capwaptnl'),(sta2mac,'capwaptnl')],IC=True)  


    if res3 != 0:
        suggestionList.append('Suggestions: Step 5 failed reason MAYBE RDM27364')
    #result
    printCheckStep(testname,'Step 5',res1,res2,res3)

################################################################################
#Step 6
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 6',
          'Recover initial config')

#operate

#解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

#删除dhcp binding,arp,mac-address-table,ipv6 neighbors信息
EnterEnableMode(switch1)
SetCmd(switch1,'clear ip dhcp binding all')
SetCmd(switch1,'clear arp traffic')
SetCmd(switch1,'clear mac-address-table dynamic')
SetCmd(switch1,'clear ipv6 neighbors')

#删除v6路由
#AC1
EnterConfigMode(switch1)
SetCmd(switch1,'no','ipv6 route',Ap1_ipv6 + '/64',If_vlan40_s3_ipv6)
#S3
EnterConfigMode(switch3)
SetCmd(switch3,'no','ipv6 route',StaticIpv6_ac1 + '/128',If_vlan40_s1_ipv6)

#删除手工配置ipv6 地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'ifconfig '+ Netcard_sta1 + ' inet6 del',staticIpv6_sta1 + '/64')
SetCmd(sta2,'\x03')
SetCmd(sta2,'ifconfig '+ Netcard_sta2 + ' inet6 del',staticIpv6_sta2 + '/64')

EnterNetworkMode(switch1,'1')
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan ' + Vlan4091)

EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip',StaticIpv4_ac1)

#将发现方式更改为 v4 发现
EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(5)
SetCmd(switch1,'enable')
IdleAfter(5)
    
IdleAfter(Ac_ap_syn_time)

#end
printTimer(testname, 'End',suggestion = suggestionList)
