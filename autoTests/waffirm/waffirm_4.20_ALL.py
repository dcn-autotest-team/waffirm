#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.20.py - test case 4.20 of waffirm
#
# Author:  qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.20 无线控制器N+1备份
# 测试目的：测试AC宕机的情况下，AP是否能够正常切换到备份AC。
# 测试环境：同测试拓扑
# 测试描述：S1（AC1）和S2（AC2）有相同的network（SSID：wlan_n+1）配置， 
#           AP开始被S1管理，STA关联后可以访问网络；S1断开后，AP保活超时后经过重新
#           发现被S2管理，STA重新关联后可以访问网络。（AC1的无线地址：AC1_无线地址；
#           AC2的无线地址：AC2_无线地址；加入集中隧道的vlan id：vlan_集中隧道。）
#
#*******************************************************************************
# Change log:
#     - zhangjxp 2017.11.10 RDM50304 修改step2
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.20'
avoiderror(testname)
printTimer(testname,'Start','Test function of wireless controler n plus 1 backup')

################################################################################
#Step 1
#操作
#AC1和AC2配置相同的network（SSID：wlan_n+1）：
#S1#con
#S1(config)#wireless 
#S1(config-wireless)#l2tunnel vlan-list add vlan_集中隧道
#S1(config-wireless)#network 1
#S1(config-network)#ssid wlan_n+1
#S1(config-network)#vlan vlan_集中隧道

#S2#con
#S2(config)#wireless 
#S2(config-wireless)#l2tunnel vlan-list add vlan_集中隧道
#S2(config-wireless)#network 1
#S2(config-network)#ssid wlan_n+1
#S2(config-network)#vlan vlan_集中隧道
#配置成功
################################################################################
printStep(testname,'Step 1',
          'Config dhcpv6 server on ac1 and disable auto discovery')

EnterConfigMode(switch2)
SetCmd(switch2,'service dhcp')
SetCmd(switch2,'ip dhcp pool pool4091')
SetCmd(switch2,'network-address ' + Dhcp_pool1 + '0 255.255.255.0')
SetCmd(switch2,'default-router ' + If_vlan4091_s1_ipv4)

#AC1
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'ssid','wlan_nplus1')
SetCmd(switch1,'vlan '+Vlan4091)

#AC2
EnterNetworkMode(switch2,'1')
SetCmd(switch2,'ssid','wlan_nplus1')
SetCmd(switch2,'vlan '+Vlan4091)

data1 = ShowRun(switch1)
data2 = ShowRun(switch2)
res1 = CheckLine(data1,'ssid','wlan_nplus1')
res2 = CheckLine(data2,'ssid','wlan_nplus1')

# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    EnterWirelessMode(switch1)
    SetCmd(switch1,'l2tunnel vlan-list add',Vlan4091)
    EnterWirelessMode(switch2)
    SetCmd(switch2,'l2tunnel vlan-list add',Vlan4091)
else:
    EnterConfigMode(switch2)
    SetCmd(switch2,'ip dhcp pool pool4092')
    SetCmd(switch2,'network-address ' + Dhcp_pool2 + '0 255.255.255.0')
    SetCmd(switch2,'default-router ' + If_vlan4092_s1_ipv4)
    SetCmd(switch2,'exit')
    SetCmd(switch2,'ip dhcp pool pool4093')
    SetCmd(switch2,'network-address ' + Dhcp_pool3 + '0 255.255.255.0')
    SetCmd(switch2,'default-router ' + If_vlan4093_s1_ipv4)
    SetCmd(switch2,'exit')

#result
printCheckStep(testname, 'Step 1',res1,res2)

################################################################################
#Step 2
#在AC上关闭AC发现AP方式：
#S1(config-wireless)#no discovery method
#S2(config-wireless)#no discovery method
#在AP上配置AC的无线地址：
#set managed-ap switch-address-1 AC1_无线地址
#set managed-ap switch-address-2 AC2_无线地址
#AP被AC1管理上，在AC1上show wireless ap status确认AP状态为Managed 
################################################################################

printStep(testname,'Step 2',
          'Config managed-ap address 1 and 2 for ap1')
res1 = 1
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery method')
EnterWirelessMode(switch2)
SetCmd(switch2,'no discovery method')
SetCmd(ap1,'set managed-ap switch-address-1',StaticIpv4_ac1)
SetCmd(ap1,'set managed-ap switch-address-2',StaticIpv4_ac2)
SetCmd(ap1,'save-running')
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap1,ap1mac,switch1)
IdleAfter(20)
for i in range(20):
	data1 = SetCmd(switch1,'show wireless ap status')
	res1 = CheckLine(data1,ap1mac,'Managed Success')
	if res1 == 0:
		break
	else:	
		IdleAfter(5)
#result
printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#STA关联SSID：wlan_n+1 
#STA关联成功，ping通网关
################################################################################

printStep(testname,'Step 3',
          'Check show wi ap status')

res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,'wlan_nplus1',connectType='open',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)

res2 = CheckPing(sta1,If_vlan4091_s1_ipv4,mode='linux')

printCheckStep(testname, 'Step 3',res1)

################################################################################
#Step 4
#操作
#S3上shutdown掉与S1链接的端口s3p1
#S3(config-if-s3p1)#shut
#L3与AC1网络断开
################################################################################

printStep(testname,'Step 4',
          'S3 disconnect with ac1')

EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'shutdown')

printCheckStep(testname, 'Step 4',0)

################################################################################
#Step 5
#操作
#AP保活超时后经过重新发现被S2管理
#AP被AC2管理上，在AC2上show wireless ap status确认AP状态为Managed
################################################################################

printStep(testname,'Step 5',
          'Ap managed by ac2 finally')
res1 = 1
# IdleAfter(Ap_manage_timeout)
# data1 = SetCmd(switch2,'show wireless ap status')
# res1 = CheckLine(data1,ap1mac,'Managed Success')
IdleAfter(40)
for i in range(25):
	data1 = SetCmd(switch2,'show wireless ap status')
	res1 = CheckLine(data1,ap1mac,'Managed Success')
	if res1 == 0:
		break
	else:	
		IdleAfter(5)
printCheckStep(testname, 'Step 5',res1)

################################################################################
#Step 6
#操作
#STA关联SSID：wlan_n+1 
#STA关联成功，ping通AC2的网关
################################################################################

printStep(testname,'Step 6',
          'Connect to wlan_n+1 and ping successful')

res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,'wlan_nplus1',connectType='open',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)

# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    res2 = CheckPing(sta1,If_vlan4091_s2_ipv4,mode='linux')
else:
    res2 = CheckPing(sta1,If_vlan4091_s1_ipv4,mode='linux')

printCheckStep(testname, 'Step 6',res1,res2)

################################################################################
#Step 7
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 7',
          'Recover initial config for switches.')

#operate
EnterConfigMode(switch2)

SetCmd(switch2,'no','ip dhcp pool pool4091')
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    pass
else:
    SetCmd(switch2,'no','ip dhcp pool pool4092')
    SetCmd(switch2,'no','ip dhcp pool pool4093')
    
SetCmd(switch2,'no','service dhcp')

EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'no','shutdown')

EnterNetworkMode(switch1,'1')
SetCmd(switch1,'ssid',Network_name1)
SetCmd(switch1,'vlan ' + Vlan4091)

EnterNetworkMode(switch2,'1')
SetCmd(switch2,'ssid',Network_name1)
SetCmd(switch2,'vlan ' + Vlan4091)

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery method')
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery method')

SetCmd(ap1,'set managed-ap switch-address-1')
SetCmd(ap1,'set managed-ap switch-address-2')
SetCmd(ap1,'save-running')

WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
RebootAp(AP=ap1)


printTimer(testname, 'End')