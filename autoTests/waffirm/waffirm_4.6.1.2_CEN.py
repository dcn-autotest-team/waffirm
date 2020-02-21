#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.6.1.2.py - test case 4.6.1.2 of waffirm_new
#
# Author:  (qidb)
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
# 
# Date 2012-12-7 14:37:33
#
# Features:
# 4.6.1.2	IPv4隧道三层转发
# 测试目的：测试客户端三层数据通过IPv4集中式隧道能够被正常转发
# 测试环境：同测试拓扑
# 测试描述：测试客户端三层数据通过IPv4集中式隧道能够被正常转发。测试中覆盖IPv4数据和IPv6数据
#
#*******************************************************************************
# Change log:
#     - zhaohj 2014-12-17 根据RDM33444修改
#*******************************************************************************

#Package

#Global Definition
staticIpv6_sta1 = '2001:91::100'
staticIpv6_sta2 = '2001:92::200'

#三层隧道转发 ipv6路由配置
CMD_Add_ipv6_route_test1_to_test2_sta1 = 'route -A inet6 add '+ staticIpv6_sta2 + '/64 gw '+ If_vlan4091_s1_ipv6 +' dev '+ Netcard_sta1
CMD_Add_ipv6_route_test2_to_test1_sta2 = 'route -A inet6 add '+ staticIpv6_sta1 + '/64 gw '+ If_vlan4092_s1_ipv6 +' dev '+ Netcard_sta2
CMD_Del_ipv6_route_test1_to_test2_sta1 = 'route -A inet6 del '+ staticIpv6_sta2 + '/64 gw '+ If_vlan4091_s1_ipv6 +' dev '+ Netcard_sta1
CMD_Del_ipv6_route_test2_to_test1_sta2 = 'route -A inet6 del '+ staticIpv6_sta1 + '/64 gw '+ If_vlan4092_s1_ipv6 +' dev '+ Netcard_sta2

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.6.1.2'
avoiderror(testname)
printTimer(testname,'Start','test L3 tunnel switch in central switch mode')

################################################################################
#Step 1 step2
#操作
#在AC1配置network1的SSID为test1，关联vlan4091，配置下发到AP1，
#配置network2的SSID为test2，关联vlan4092，配置下发到AP2
#在AC1上面将vlan4091和vlan4092加入到l2-tunnel vlan-list中
#
#(以上均包含在初始配置之中)
#
#
#预期
#通过show wireless l2-tunnel vlan-list可以看到vlan4091和vlan4092
################################################################################
printStep(testname,'Step 1,Step 2',
          'Show wireless l2tunnel vlan-list',
          'Check if contain vlan 4091,4092')

res1=1
#operate
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless l2tunnel vlan-list',timeout=5)

#check
res1 = CheckLineList(data1,[(Vlan4091),(Vlan4092)],IC=True)

#result
printCheckStep(testname, 'Step 1 Step 2',res1)

################################################################################
#Step 3
#操作
#将STA1,STA2 分别关联到AP1的网络test1，AP2的 test2
#
#预期
#关联成功
#客户端STA1能够获取192.168.91.X网段的IP地址，STA2能够获取192.168.92.X网段的IP地址。
################################################################################

printStep(testname,'Step 3',
          'STA1 connect to test1, get 192.168.91.x ip via dhcp',
          'STA2 connect to test1, get 192.168.92.x ip via dhcp')

sta1_ipv4 = ''
sta2_ipv4 = ''

res1=res2=res3=res4=1

#operate
#STA1,STA2关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,bssid=ap2mac_type1_network2)
IdleAfter(10)

#获取STA1,STA2的地址
sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool1)
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
    #用STA1的ipv4地址ping STA2的ipv4地址，
    #用STA1的ipv6地址ping STA2的ipv6地址（ipv6地址手动配置为与ac网段的地址）。
    #
    #预期
    #能够ping通，在AC1使用命令show arp可看到STA1和STA2的mac对应的port为
    #capwaptnl隧道类型，使用show mac-address-table命令看到STA1和STA2的Ports类型为
    #capwaptnl隧道类型，ipv6流量使用show ipv6 neighbors查看；
    ################################################################################

    printStep(testname,'Step 4',
              'STA1 ping STA2 in both ipv4 and ipv6',
              'Check if succeed')

    res1=res2=res3=res4=res5=-1

    #operate

    #手动配置STA1，STA2 ipv6 地址
    SetCmd(sta1,'\x03')
    SetCmd(sta1,'ifconfig '+ Netcard_sta1 + ' inet6 add',staticIpv6_sta1 + '/64')
    SetCmd(sta2,'\x03')
    SetCmd(sta2,'ifconfig '+ Netcard_sta2 + ' inet6 add',staticIpv6_sta2 + '/64')
    IdleAfter(30)
    #配置test1 至 test2 ipv6 路由
    SetCmd(sta1,CMD_Add_ipv6_route_test1_to_test2_sta1)
    #配置test2 至 test1 ipv6 路由
    SetCmd(sta2,CMD_Add_ipv6_route_test2_to_test1_sta2)

    #ping,ping6
    res1 = CheckPing(sta1,sta2_ipv4,mode='linux')
    SetCmd(sta1,'ping6',staticIpv6_sta2,promotePatten = 'PING',promoteTimeout = 10)
    IdleAfter(10)
    data0 = SetCmd(sta1,'\x03',timeout = 1)

    #查看表项
    IdleAfter(10)
    EnterEnableMode(switch1)
    data3 = SetCmd(switch1,'show mac-address-table')
    data4 = SetCmd(switch1,'show ipv6 neighbors')
    data5 = SetCmd(switch1,'show arp')
    SetCmd(sta1,'arp -a')
    SetCmd(sta2,'arp -a')
    #check

    res2 = int(str(GetValueBetweenTwoValuesInData(data0,'transmitted,','received')).strip()) 
    res2 = 0 if res2 > 0 else 1
    res3 = CheckLineList(data3,[(sta1mac,'capwaptnl'),(sta2mac,'capwaptnl')],IC=True)  
    res4 = CheckLineList(data4,[(staticIpv6_sta1,sta1mac,'capwaptnl'),
                                (staticIpv6_sta2,sta2mac,'capwaptnl')],IC=True)               
    res5 = CheckLineList(data5,[(sta1_ipv4,sta1mac,'capwaptnl'),(sta2_ipv4,sta2mac,'capwaptnl')],IC=True)

    #result
    printCheckStep(testname,'Step 4',res1,res2,res3,res4,res5)

################################################################################
#Step 5
#在AC1的ap profile 1配置：
#Management vlan 20
#Ethernet native-vlan 20
#然后：
#wireless ap eth-parameter apply profile 1
#
#预期
#配置下发后，show wireless ap status看到ap1 上线成功。
################################################################################
printStep(testname,'Step 5',
          'set management vlan 20 for ap profile 1',
          'show wireless ap status,check ap1 on line')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 1')
SetCmd(switch1,'management vlan 20')
SetCmd(switch1,'ethernet native-vlan 20')
EnterEnableMode(switch1)
#SetCmd(switch1,'wireless ap profile apply 1',timeout=1)
#SetCmd(switch1,'y',timeout=1)
SetCmd(switch1,'wireless ap eth-parameter apply profile 1')
#check
data = SetCmd(switch1,'show wireless ap status')
res = CheckLine(data,ap1mac,Ap1_ipv4,'Managed','Success',IC=True)
printCheckStep(testname,'Step 5',res)

################################################################################
#Step 6
#操作
#将STA1,STA2 分别关联到AP1的网络test1，AP2的 test2
#
#预期
#关联成功
#客户端STA1能够获取192.168.91.X网段的IP地址，STA2能够获取192.168.92.X网段的IP地址。
################################################################################

printStep(testname,'Step 6',
          'STA1 connect to test1, get 192.168.91.x ip via dhcp',
          'STA2 connect to test1, get 192.168.92.x ip via dhcp')

sta1_ipv4 = ''
sta2_ipv4 = ''

res1=res2=res3=res4=1

#operate
#STA1,STA2关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,bssid=ap2mac_type1_network2)
IdleAfter(10)

#获取STA1,STA2的地址
sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
res3 = sta1_ipresult['res']

sta2_ipresult = GetStaIp(sta2,checkippool=Dhcp_pool2)
sta2_ipv4 = sta2_ipresult['ip']
res4 = sta2_ipresult['res']
           
#result
printCheckStep(testname, 'Step 6',res1,res2,res3,res4)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2 + res3 + res4
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 7
    #操作
    #用STA1的ipv4地址ping STA2的ipv4地址，
    #用STA1的ipv6地址ping STA2的ipv6地址（ipv6地址手动配置为与ac网段的地址）。
    #
    #预期
    #能够ping通，在AC1使用命令show arp可看到STA1和STA2的mac对应的port为capwaptnl隧道类型，
    #使用show mac-address-table命令看到STA1和STA2的Ports类型为capwaptnl隧道类型，
    #ipv6流量使用show ipv6 neighbors查看；
    ################################################################################

    printStep(testname,'Step 7',
              'STA1 ping STA2 in both ipv4 and ipv6',
              'Check if succeed')

    res1=res2=res3=res4=res5=-1

    #operate

    #手动配置STA1，STA2 ipv6 地址
    SetCmd(sta1,'\x03')
    SetCmd(sta1,'ifconfig '+ Netcard_sta1 + ' inet6 add',staticIpv6_sta1 + '/64')
    SetCmd(sta2,'\x03')
    SetCmd(sta2,'ifconfig '+ Netcard_sta2 + ' inet6 add',staticIpv6_sta2 + '/64')
    IdleAfter(30)
    #配置test1 至 test2 ipv6 路由
    SetCmd(sta1,CMD_Add_ipv6_route_test1_to_test2_sta1)
    #配置test2 至 test1 ipv6 路由
    SetCmd(sta2,CMD_Add_ipv6_route_test2_to_test1_sta2)

    #ping,ping6
    res1 = CheckPing(sta1,sta2_ipv4,mode='linux')
    SetCmd(sta1,'ping6',staticIpv6_sta2,promotePatten = 'PING',promoteTimeout = 10)
    IdleAfter(10)
    data0 = SetCmd(sta1,'\x03',timeout = 1)

    #查看表项
    IdleAfter(10)
    EnterEnableMode(switch1)
    data3 = SetCmd(switch1,'show mac-address-table')
    data4 = SetCmd(switch1,'show ipv6 neighbors')
    data5 = SetCmd(switch1,'show arp')
    SetCmd(sta1,'arp -a')
    SetCmd(sta2,'arp -a')
    #check

    res2 = int(str(GetValueBetweenTwoValuesInData(data0,'transmitted,','received')).strip()) 
    res2 = 0 if res2 > 0 else 1
    res3 = CheckLineList(data3,[(sta1mac,'capwaptnl'),(sta2mac,'capwaptnl')],IC=True)  
    res4 = CheckLineList(data4,[(staticIpv6_sta1,sta1mac,'capwaptnl'),
                                (staticIpv6_sta2,sta2mac,'capwaptnl')],IC=True)               
    res5 = CheckLineList(data5,[(sta1_ipv4,sta1mac,'capwaptnl'),(sta2_ipv4,sta2mac,'capwaptnl')],IC=True)

    #result
    printCheckStep(testname,'Step 7',res1,res2,res3,res4,res5)

################################################################################
#Step 8
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 8',
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

#删除手工配置ipv6 地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'ifconfig '+ Netcard_sta1 + ' inet6 del',staticIpv6_sta1 + '/64')
SetCmd(sta2,'\x03')
SetCmd(sta2,'ifconfig '+ Netcard_sta2 + ' inet6 del',staticIpv6_sta2 + '/64')

#删除test1 至 test2 ipv6 路由
SetCmd(sta1,CMD_Del_ipv6_route_test1_to_test2_sta1)
#删除test2 至 test1 ipv6 路由
SetCmd(sta2,CMD_Del_ipv6_route_test2_to_test1_sta2)

#删除step4的配置
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 1')
SetCmd(switch1,'no management vlan')
SetCmd(switch1,'no ethernet native-vlan')
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap eth-parameter apply profile 1',timeout=1)
SetCmd(switch1,'y',timeout=1)
IdleAfter(Ac_ap_syn_time)

#end
printTimer(testname, 'End')