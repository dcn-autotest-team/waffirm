 #-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.4.6.py - test case 4.4.6 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2013 Digital China Networks Co. Ltd
#
# Features:
# 4.4.6	Client威胁检测
# 测试目的：支持client威胁检测
# 测试环境：同测试拓扑
# 测试描述：AP能够检测出client的各种威胁
#
#*******************************************************************************
# Change log:
#     - qidb
#     - 2017.2.27 lupingc RDM48810修改step2
#     - lupingc RDM49074 2017.5.17
#     - zhangjxp RDM50224 2017.10.25
#     - zhangjxp 2017.11.9 RDM50346 修改step10
#     - zhangjxp 2017.11.10 RDM50304 修改step8
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
#*******************************************************************************

#Package

#Global Definition
Rfscan_interval = '5'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.4.6'
avoiderror(testname)
printTimer(testname,'Start','test detection of Client Threat')

suggestionList = []
# 2.4G、5G差异化配置,test24gflag为True代表执行2.4G脚本，False代表执行5G脚本
# if test24gflag ==  True:
    # wlan='wlan0'
    # radio = 'radio 1'
# else:
    # wlan='wlan1'
    # radio = 'radio 2'
################################################################################
#Step 1
#操作
#在 AC1 配置network1的SSID为test1，关联vlan4091。
#
#预期
#配置成功
################################################################################
printStep(testname,'Step 1',
          'set network 1 ssid test1 vlan 4091')

res1=res2=1
#operate
# network1配置与初始化配置相同，不需重复配置
# EnterInterfaceMode(switch2,s2p1)
# SetCmd(switch2,'shutdown')

# EnterNetworkMode(switch1,'1')
# SetCmd(switch1,'ssid ' + Network_name1)
# SetCmd(switch1,'vlan '+Vlan4091)

# WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# SetCmd(switch2,'no shutdown')

data1 = SetCmd(switch1,'show wireless network','1',timeout=5)

#check
res1 = CheckLine(data1,'Default VLAN',Vlan4091,IC=True)
res2 = CheckLine(data1,'SSID',Network_name1,IC=True)

#result
printCheckStep(testname, 'Step 1',res1,res2)

################################################################################
#Step 2
#操作
#从ac1 kown client表中删除sta2，并且设置kown client为白名单(mac-authentication-mode white-list)
#
#预期
#查看detected-client列表，sta2显示为rogue client
################################################################################

printStep(testname,'Step 2',
          'delete sta2 from know-client table and set known client action white-list,',
          'show client status table and check sta2 is rogue client.')

res1=0
res2=1
res3 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap1mac_lower)
#operate
#开启know_client_database安全检查
EnterWirelessMode(switch1)
SetCmd(switch1,'known-client',sta2mac)
SetCmd(switch1,'wids-security client known-client-database')

#EnterNetworkMode(switch1,'1')
#SetCmd(switch1,'mac authentication local')

#EnterApProMode(switch1,'1')
#SetCmd(switch1,'radio 1')
#SetCmd(switch1,'rf-scan other-channels interval',Rfscan_interval)

EnterEnableMode(switch1)
data0 = SetCmd(switch1,'clear wireless detected-client non-auth',timeout=1)
#if 0 == CheckLine(data0,'Y/N'):
SetCmd(switch1,'y',timeout=1)
# 
# IdleAfter(Wait_rf_scan_time)
# 
# i_time = 0
# while i_time < 5:
#     data1 = SetCmd(switch1,'show wireless client detected-client status',' |  include ',sta2mac)
#     data2 = SetCmd(switch1,'show wirmelessmeeless client detected-client status',' |  include ',sta1mac)
#     res1 = CheckLine(data1,sta2mac,'Detected')
#     res2 = CheckLine(data2,sta1mac,'Detected')
#     if 0==res1 and 0==res2:
#         break
#     i_time = i_time + 1
#     IdleAfter(3)

#初始配置sta2不在known-client列表中，不需要删除,AC缺省配置即为 white-list
EnterWirelessMode(switch1)
SetCmd(switch1,'no known-client',sta2mac)
SetCmd(switch1,'mac-authentication-mode white-list')

IdleAfter(Wait_rf_scan_time)

#STA2关联 AP1，即使能关联上，但dhcp得不到地址，手动配置也无法ping通网关
#res1 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap1mac_lower)
#res1 = 0 if 0 != res1 else 1

EnterEnableMode(switch1)
i_time = 0
while i_time < 10:
    data2 = SetCmd(switch1,'show wireless client detected-client status | include ',sta2mac)
    res2 = CheckLine(data2,sta2mac,'Rogue',IC=True)
    if 0 == res2:
        break
    i_time = i_time + 1
    IdleAfter(3)

#check

#result
printCheckStep(testname, 'Step 2',res1,res2,res3)

################################################################################
#Step 3
#操作
#在known client表中添加sta2，并且设置为grant。
#
#预期
#查看client列表，sta2显示为managed client
################################################################################

printStep(testname,'Step 3',
          'add sta2 in known client and set action grant,',
          'show client status table and sta2 status is managed client.')

res1=res2=1
#operate
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)
EnterWirelessMode(switch1)
SetCmd(switch1,'known-client ' + sta2mac + ' action grant')
#删除上次扫描结果
EnterEnableMode(switch1)
data0 = SetCmd(switch1,'clear wireless detected-client non-auth',timeout=1)
#if 0 == CheckLine(data0,'Y/N'):
SetCmd(switch1,'y',timeout=1)

IdleAfter(Wait_rf_scan_time)

# i_time = 0
# while i_time < 10:
#     data1 = SetCmd(switch1,'show wireless client detected-client status',' |  include ',sta2mac)
#     res1 = CheckLine(data1,sta2mac,'Authenticated')
#     if 0==res1:
#         break
#     i_time = i_time + 1
#     IdleAfter(3)
# SetCmd(switch6,CMD_Wpacli_Disable_network)    

#res1 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap1mac_lower)

##sta2 解关联（等待自动被踢下去需要时间较长），如果不解关联，状态应该是 'Authenticated'
#WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

EnterEnableMode(switch1)
i_time = 0
while i_time < 15:
    data2 = SetCmd(switch1,'show wireless client detected-client status',' |  include ',sta2mac)
    res2 = CheckLine(data2,sta2mac,'Known',IC=True)
##    if res2 == 1:
##        res2 = CheckLine(data2,sta2mac,'Detected',IC=True)
    if 0 == res2:
        break
    i_time = i_time + 1
    IdleAfter(5)
#check
#IdleAfter(Pc_client_login_wait_time)
###状态好像不是management，是known
#data1 = SetCmd(switch1,'show wireless client detected-client status',' |  include ',sta2mac)
#res1 = CheckLine(data1,sta2mac,'Known')

#result
if res2 != 0:
    suggestionList.append('Suggestions: Step 3 failed reason MAYBE RDM19630')
printCheckStep(testname, 'Step 3',res2)

################################################################################
#Step 4
#操作
#在kown client表中添加sta2，并且设置为deny。
#
#预期
#查看client列表，sta2显示为rogue client
################################################################################
printStep(testname,'Step 4',
          'set sta2mac know-client action deny,',
          'show client table and check sta2 status is rogue client.')
WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap1mac_lower)
res1=0
res2=1
#operate

EnterWirelessMode(switch1)
SetCmd(switch1,'known-client ' + sta2mac + ' action deny')

#删除上次扫描结果
EnterEnableMode(switch1)
data0 = SetCmd(switch1,'clear wireless detected-client non-auth',timeout=1)
#if 0 == CheckLine(data0,'Y/N'):
SetCmd(switch1,'y',timeout=1)
    
IdleAfter(Wait_rf_scan_time)

#check
#IdleAfter(Pc_client_login_wait_time)
#data1 = SetCmd(switch1,'show wireless client detected-client status',' |  include ',sta2mac)
#res1 = CheckLine(data1,sta2mac,'Rogue')
#IdleAfter(Wait_rf_scan_time)

#res1 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap1mac_lower)
#res1 = 0 if 0 != res1 else 1

EnterEnableMode(switch1)
i_time = 0
while i_time < 10:
    data2 = SetCmd(switch1,'show wireless client detected-client status',' |  include ',sta2mac)
    res2 = CheckLine(data2,sta2mac,'Rogue',IC=True)
    if 0 == res2:
        break
    i_time = i_time + 1
    IdleAfter(3)
    
#result
printCheckStep(testname, 'Step 4',res1,res2)

################################################################################
#Step 5
#操作
#使用client模拟器，按超过配置的认证请求帧发送率发送认证请求帧。
#
#预期
#查看client列表，该client模拟器显示为rogue client
################################################################################
printStep(testname,'Step 5',
          'sta1 send auth-request packets with rate more than the rate limited,',
          'show client and check client status is rogue.')

res1=res2=1
#operate

EnterWirelessMode(switch1)
SetCmd(switch1,'mac-authentication-mode black-list')

#关闭know_client_database安全检查并删除上次检查结果
EnterWirelessMode(switch1)
SetCmd(switch1,'no wids-security client known-client-database')

#从known-client 列表删除STA2
EnterWirelessMode(switch1)
SetCmd(switch1,'no','known-client',sta2mac)

#删除上次扫描结果
EnterEnableMode(switch1)
data0 = SetCmd(switch1,'clear wireless detected-client non-auth',timeout=1)
#if 0 == CheckLine(data0,'Y/N'):
SetCmd(switch1,'y',timeout=1)
    
IdleAfter(Wait_rf_scan_time)
WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap1mac_lower)
#等待一段时间检查状态是否恢复成了Detected
#WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)

#i_time = 0
#while i_time < 15:
    #data1 = SetCmd(switch1,'show wireless client detected-client status',' |  include ',sta1mac)
    #res1 = CheckLine(data1,sta1mac,'Authenticated',IC=True)
    #if 0 == res1:
        #break
    #i_time = i_time + 1
    #IdleAfter(3)
#WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)    
#i_time = 0
#while i_time < 15:
    #data1 = SetCmd(switch1,'show wireless client detected-client status',' |  include ',sta1mac)
    #res1 = CheckLine(data1,sta1mac,'Detected',IC=True)
    #if 0 == res1:
        #break
    #i_time = i_time + 1
    #IdleAfter(3)

#开启认证请求发送速率安全检查
EnterWirelessMode(switch1)
SetCmd(switch1,'wids-security client configured-auth-rate')
#修改client端认证报文发送速率限制的配置
EnterWirelessMode(switch1)
#SetCmd(switch1,CMD_Set_widssecurity_client_threshold_interval_probe)
#SetCmd(switch1,'wids-security client threshold-value-probe 20')
SetCmd(switch1,'wids-security client threshold-interval-auth 5')
SetCmd(switch1,'wids-security client threshold-value-auth',2)
#SetCmd(switch1,CMD_Set_widssecurity_client_threshold_value_deauth)
#SetCmd(switch1,CMD_Set_widssecurity_client_threshold_interval_deauth)
#不需要下发配置
#EnterEnableMode(switch1)
#SetCmd(switch1,'wireless ap profile apply 1',promotePatten='Y/N')
#SetCmd(switch1,'y')
#IdleAfter(Pc_client_login_wait_time)

#发送请求帧
for itemp in xrange(50):
    SetCmd(sta2,'wpa_cli -i' + Netcard_sta2 + ' disable_network 0')
    IdleAfter(0.2)
    SetCmd(sta2,'wpa_cli -i' + Netcard_sta2 + ' enable_network 0')
    IdleAfter(0.2)
#res = ConnectDsendWireless(testerip_sta1)
#if 0==res:
    #printRes('start Transmit')
    #Pktstr= ReadPcapWireless(Filename=Var_file_auth,Pktnum=auth_index,Initnum1=auth_initnum_index,Finalnum1=auth_finalnum_index,Replacevalue1=auth_replace_value)
    #SetDsendStreamWireless(Port=testerp1_sta1,PortTypeConfig=PortType_moni,StreamMode='0',StreamRateMode='pps',StreamRate=Var_test_auth_send_rate,Pcapvalue=Pktstr) 
    #StartTransmitWireless(testerp1_sta1,PortType=PortType_moni)
    #IdleAfter(Rate_stable_wait_time)
    
        #StopDsendCaptureWireless(testerp1_sta2)   

#check
#检查cliet列表
#IdleAfter(Wait_rf_scan_time_packet_rate)
i_time = 0
while i_time < 5:
    data2 = SetCmd(switch1,'show wireless client ' + sta2mac + ' detected-client rogue-classification')
    res2 = CheckLine(data2,'Enable\s+Rogue',IC=True)
    if 0 == res2:
        break
    i_time = i_time + 1
    IdleAfter(5)
    
#关闭发包工具    
#res = ConnectDsendWireless(testerip_sta1)
#if 0==res:
    #printRes('stop Transmit')
    #StopTransmitWireless(testerp1_sta1)
    #DisconnectDsendWireless()
    
#关闭认证请求发送速率的安全检查,默认是开启的，所以此步骤不操作
#恢复认证请求报文的发送速率配置
EnterWirelessMode(switch1)
SetCmd(switch1,'no wids-security client threshold-interval-auth')
SetCmd(switch1,'no wids-security client threshold-value-auth')

#result
printCheckStep(testname, 'Step 5',res2)

################################################################################
#Step 6
#操作
#使用client模拟器，按超过配置的探求帧发送率发送探求帧。
#
#预期
#查看client列表，该client模拟器显示为rogue client
################################################################################
printStep(testname,'Step 6',
          'sta1 send request packets with rate more than the rate limited,',
          'show client and check client status is rogue.')
          
res1=res2=1         
#operate

#删除上次扫描结果
IdleAfter(30)
EnterEnableMode(switch1)
data0 = SetCmd(switch1,'clear wireless detected-client non-auth',timeout=1)
#if 0 == CheckLine(data0,'Y/N'):
SetCmd(switch1,'y',timeout=1)
IdleAfter(Wait_rf_scan_time)

#等待一段时间检查状态是否恢复成了Detected
IdleAfter(Pc_client_login_wait_time)
WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap1mac_lower)
#data1 = SetCmd(switch1,'show wireless client detected-client status',' |  include ',sta1mac)
#res1 = CheckLine(data1,sta1mac,'Authenticated',IC=True)

#WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)

i_time = 0
while i_time < 10:
    data1 = SetCmd(switch1,'show wireless client detected-client status',' |  include ',sta2mac)
    res1 = CheckLine(data1,sta2mac,'Authenticated',IC=True)
    if res1 == 1:
        res1 = CheckLine(data1,sta2mac,'Detected',IC=True)
    if 0 == res1:
        break
    i_time = i_time + 1
    IdleAfter(3)
    
#WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

#IdleAfter(10)
#i_time = 0
#while i_time < 5:
    #data1 = SetCmd(switch1,'show wireless client detected-client status',' |  include ',sta1mac)
    #res1 = CheckLine(data1,sta1mac,'Detected',IC=True)
    #if 0 == res1:
        #break
    #i_time = i_time + 1
    #IdleAfter(3)

#开启探求帧发送速率安全检查,并配置安全速率参数
EnterWirelessMode(switch1)
SetCmd(switch1,'wids-security client configured-probe-rate')
SetCmd(switch1,'wids-security client threshold-value-probe 2')

#发送探求帧
#res = ConnectDsendWireless(testerip_sta1)
#if 0==res:
    #printRes('start Transmit')
    #Pktstr= ReadPcapWireless(Filename=Var_file_probe_request,Pktnum=probe_request_index,Initnum1=probe_initnum1_index,Finalnum1=probe_finalnum1_index,Replacevalue1=probe_request_replace_value)
    #SetDsendStreamWireless(Port=testerp1_sta1,PortTypeConfig=PortType_moni,StreamMode='0',StreamRateMode='pps',StreamRate=Var_test_probe_send_rate,Pcapvalue=Pktstr) 
    #StartTransmitWireless(testerp1_sta1,PortType=PortType_moni)
    #IdleAfter(Rate_stable_wait_time)

for itemp in xrange(50):
    SetCmd(sta2,'wpa_cli -i' + Netcard_sta2 + ' disable_network 0')
    IdleAfter(0.2)
    SetCmd(sta2,'wpa_cli -i' + Netcard_sta2 + ' enable_network 0')
    IdleAfter(0.2)
#check
#检查cliet列表
#IdleAfter(Wait_rf_scan_time_packet_rate)
i_time = 0
while i_time<5:
    data2 = SetCmd(switch1,'show wireless client detected-client status | include ',sta2mac)
    res2 = CheckLine(data2,sta2mac,'Rogue',IC=True)
    if 0 == res2:
        break
    i_time = i_time + 1
    IdleAfter(5)
    
#关闭发包工具连接    
#res = ConnectDsendWireless(testerip_sta1)
#if 0==res:
    #printRes('stop Transmit')
    #StopTransmitWireless(testerp1_sta1)
    #DisconnectDsendWireless()
    
#恢复探求帧安全检查开关,默认开启，所以此步不关闭该检查,并配置安全探求帧发送速率
EnterWirelessMode(switch1)
SetCmd(switch1,'no wids-security client threshold-interval-probe')
SetCmd(switch1,'no wids-security client threshold-value-probe')

#result
printCheckStep(testname, 'Step 6',res1,res2)

# RDM50224跳过第7步
# ################################################################################
# #Step 7
# #操作
# #使用client模拟器，按超过配置的解认证帧发送率发送解认证帧。
# #
# #预期
# #查看client列表，该client模拟器显示为rogue client
# ################################################################################
# printStep(testname,'Step 7',\
          # 'sta2 send deauth packets with rate more than the rate limited,',\
          # 'show client and check client status is rogue.')
          
# res1=res2=1

# #operate

# #删除上次扫描结果
# IdleAfter(20)
# EnterEnableMode(switch1)
# data0 = SetCmd(switch1,'clear wireless detected-client non-auth',timeout=1)
# if 0 == CheckLine(data0,'Y/N'):
    # SetCmd(switch1,'y',timeout=1)
# IdleAfter(30)
# WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,bssid=ap1mac_lower)
# #等待一段时间检查状态是否恢复成了Detected
# #IdleAfter(Pc_client_login_wait_time)
# #data1 = SetCmd(switch1,'show wireless client detected-client status',' |  include ',sta1mac)
# #res1 = CheckLine(data1,sta2mac,'Detected',IC=True)

# #WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)

# i_time = 0
# while i_time < 10:
    # data1 = SetCmd(switch1,'show wireless client detected-client status',' |  include ',sta2mac)
    # res1 = CheckLine(data1,sta2mac,'Authenticated',IC=True)
    # if res1 == 1:
        # res1 = CheckLine(data1,sta2mac,'Detected',IC=True)
    # if 0 == res1:
        # break
    # i_time = i_time + 1
    # IdleAfter(3)
    
# #WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)    

# #i_time = 0
# #while i_time < 5:
    # #data1 = SetCmd(switch1,'show wireless client detected-client status',' |  include ',sta1mac)
    # #res1 = CheckLine(data1,sta1mac,'Detected',IC=True)
    # #if 0 == res1:
        # #break
    # #i_time = i_time + 1
    # #IdleAfter(3)

# #开启解认证发送速率安全检查并配置速率参数
# EnterWirelessMode(switch1)
# SetCmd(switch1,'wids-security client configured-deauth-rate')
# SetCmd(switch1,'wids-security client threshold-interval-deauth 2')

# #发送解认证帧
# #res = ConnectDsendWireless(testerip_sta1)
# #if 0==res:
    # #printRes('start Transmit')
    # #Pktstr= ReadPcapWireless(Filename=Var_file_deauth,Pktnum=deauth_index,Initnum1=deauth_initnum_index,Finalnum1=deauth_finalnum_index,Replacevalue1=deauth_replace_value)
    # #SetDsendStreamWireless(Port=testerp1_sta1,PortTypeConfig=PortType_moni,StreamMode='0',StreamRateMode='pps',StreamRate=Var_test_deauth_send_rate,Pcapvalue=Pktstr) 
    # #StartTransmitWireless(testerp1_sta1,PortType=PortType_moni)
    # #IdleAfter(Rate_stable_wait_time)

# for itemp in xrange(50):
    # SetCmd(sta2,'wpa_cli -i' + Netcard_sta2 + ' disable_network 0')
    # IdleAfter(0.2)
    # SetCmd(sta2,'wpa_cli -i' + Netcard_sta2 + ' enable_network 0')
    # IdleAfter(0.2)    

# #check
# #检查cliet列表
# #IdleAfter(Wait_rf_scan_time_packet_rate)
# i_time = 0
# while i_time < 5:
    # data1 = SetCmd(switch1,'show wireless client detected-client status | include ',sta2mac)
    # res2 = CheckLine(data1,sta2mac,'Rogue',IC=True)
    # if 0 == res2:
        # break
    # i_time = i_time + 1
    # IdleAfter(5)
    
# #关闭发包工具连接
# #res = ConnectDsendWireless(testerip_sta1)
# #if 0==res:
    # #printRes('stop Transmit')
    # #StopTransmitWireless(testerp1_sta1)
    # #DisconnectDsendWireless()  
	
# #result
# printCheckStep(testname, 'Step 7',res1,res2)

################################################################################
#Step 8
#操作
#AP2断开网络，并且从ac1上的database中删除AP2的mac，在ac2上的database中添加AP2的mac，
#并且在database下配置它所对应的profile为2，AP2接入网络。
#预期
#在ac1上Show wireless ap rf-scan status显示AP2为unknown
#在ac2上显示AP2被管理上。
################################################################################
printStep(testname,'Step 8','AP2 worked as fat AP',
          'Delete mac of AP2 from database on AC1')

res1=1
#operate

#删除ap rf-scan list
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery ip-list ' + Ap2_ipv4)

EnterWirelessMode(switch2)
SetCmd(switch2,'discovery ip-list ' + Ap2_ipv4)
# RDM50224,修改AP2重新认证的方式（把shutdown s3p4改为使用ap上的隐藏命令）
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap2,ap2mac,switch1)
IdleAfter(20)
# EnterInterfaceMode(switch3,s3p4)
# SetCmd(switch3,'shutdown')
# IdleAfter(80)

# SetCmd(switch3,'no shutdown')

EnterEnableMode(switch1)
EnterEnableMode(switch2)
#check
for i in range(16): 
	data1 = SetCmd(switch1,'show wireless ap status')
	data3 = SetCmd(switch2,'show wireless ap status')
	res1 = CheckLine(data1,ap1mac,'Managed','Success',IC=True)
	res3 = CheckLine(data3,ap2mac,'Managed','Success',IC=True) 
	if res1==0 and res3==0:
		break
	IdleAfter(5)
#EnterEnableMode(switch2)
#data3 = SetCmd(switch2,'show wireless ap status')

#EnterWirelessMode(switch1)
#SetCmd(switch1,'ap database',ap2mac)
##SetCmd(switch1,'mode standalone')

##从AC1 database 删除AP2 mac
#SetCmd(switch1,'no','ap database',ap2mac)
#RebootAp('AC',AC=switch1,MAC=ap2mac,AP=ap2)

##配置AP2 ssid为test2
#SetCmd(ap2,'set interface wlan0 ssid',Network_name2)

#IdleAfter(Signal_scan_times)

#data2 = SetCmd(switch1,'show wireless network','1')



EnterEnableMode(switch1)
data0 = SetCmd(switch1,'clear wireless ap rf-scan list',timeout=1)
#if 0 == CheckLine(data0,'Y/N'):
SetCmd(switch1,'y',timeout=1)

#i_time = 0
#while i_time < 10:
    #data1 = SetCmd(switch1,'show wireless ap rf-scan status',' |  include ',ap2mac)
    #res1 = CheckLine(data1,ap2mac,'Unknown',IC=True)
    #if 0 == res1:
        #break
    #i_time = i_time + 1
    #IdleAfter(5)
 
#check

#result
printCheckStep(testname, 'Step 8',res1,res3)
# 如果AP2没有被AC2管理，则不执行后续步骤
keeponflag = res3
if GetWhetherkeepon(keeponflag):
	################################################################################
	#Step 9
	#操作
	#打开安全检测开关：
	#Wids-security client auth-with-unknow-ap
	#使用sta1关联到ssid test2。
	#
	#预期
	#查看client列表，STA1显示为rogue client
	################################################################################
	printStep(testname,'Step 9','STA1 connects to test2',
              'check client status of STA1 on AC1')
					   
	res1=1

	#operate

	#删除上次的扫描结果
	EnterWirelessMode(switch1)
	SetCmd(switch1,'wids-security client auth-with-unknown-ap')
	SetCmd(switch1,'wids-security client known-client-database')
	SetCmd(switch1,'mac-authentication-mod white-list')
	SetCmd(switch1,'known-client ' + sta1mac)
	SetCmd(switch1,'no ap database ' + ap2mac,timeout=1)
	SetCmd(switch1,'y')
	SetCmd(switch1,'ap profile 1')
	# SetCmd(switch1,radio)
	SetCmd(switch1,'radio '+radionum)
	SetCmd(switch1,'rf-scan other-channels interval 6')
	SetCmd(switch1,'rf-scan duration 500')
	EnterEnableMode(switch1)
	SetCmd(switch1,'clear wireless ap failed',timeout=1)
	SetCmd(switch1,'y',timeout=1)

	WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
	WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,dhcpFlag=False,bssid=ap2mac_lower)
	WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap2mac_lower)
	SetCmd(sta1,'ifconfig ' + Netcard_sta1 + ' 192.168.200.101 netmask 255.255.255.0')
	SetCmd(sta2,'ifconfig ' + Netcard_sta2 + ' 192.168.200.102 netmask 255.255.255.0')
	SetCmd(sta1,'ping 192.168.200.102',timeout=1)
	SetCmd(sta2,'ping 192.168.200.101',timeout=1)

	EnterEnableMode(switch1)
	data0 = SetCmd(switch1,'clear wireless detected-client non-auth',timeout=1)
	if 0 == CheckLine(data0,'Y/N'):
		SetCmd(switch1,'y',timeout=1)

	IdleAfter(30)

	i_time = 0
	while i_time < 30:
		data1 = SetCmd(switch1,'show wireless client detected-client status',' |  include ',sta1mac)
		res1 = CheckLine(data1,sta1mac,'Rogue',IC=True)
		if 0 == res1:
			break
		i_time = i_time + 1
		IdleAfter(10)

	SetCmd(sta1,'\x03')
	SetCmd(sta2,'\x03')

	if res1 != 0:
		suggestionList.append('Suggestions: Step 9 failed reason MAYBE RDM19630')

	#check

	#result
	printCheckStep(testname, 'Step 9',res1)

################################################################################
#Step 10
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 10',
          'Recover initial config for switches.')

WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)
#operate
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan ' + Vlan4091)

EnterWirelessMode(switch1)
SetCmd(switch1,'no wids-security client auth-with-unknown-ap')
SetCmd(switch1,'discovery ip-list ' + Ap2_ipv4)
SetCmd(switch1,'no known-client ' + sta1mac)

EnterWirelessMode(switch2)
SetCmd(switch2,'no discovery ip-list ' + Ap2_ipv4)

#此步骤先将AP2修改成ws-managed 状态
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap2mac)
SetCmd(switch1,'profile 2')
#SetCmd(switch1,'mode ws-managed',timeout=1)
SetCmd(ap2,'set managed-ap mode down')
IdleAfter(8)
SetCmd(ap2,'set managed-ap mode up')
IdleAfter(20)
CheckSutCmd(switch1,'show wireless ap status',
            check=[(ap2mac,'Managed','Success')],
            waittime=5,retry=20,interval=5,IC=True)

SetCmd(switch1,'show wireless client status')
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no mac authentication')

EnterWirelessMode(switch1)
SetCmd(switch1,'no mac-authentication-mode')

#恢复 interval 为默认配置
EnterApProMode(switch1,'1')
# SetCmd(switch1,radio)
SetCmd(switch1,'radio '+radionum)
SetCmd(switch1,'no','rf-scan other-channels interval')
EnterWirelessMode(switch1)
SetCmd(switch1,'no wids-security client threshold-interval-probe')
SetCmd(switch1,'no wids-security client threshold-interval-auth')
SetCmd(switch1,'no wids-security client threshold-interval-deauth')
SetCmd(switch1,'no wids-security client threshold-value-auth')
SetCmd(switch1,'no wids-security client threshold-value-probe')
SetCmd(switch1,'no wids-security client threshold-value-deauth ')
SetCmd(switch1,'no wids-security client known-client-database')

#删除扫描结果
EnterEnableMode(switch1)
data0 = SetCmd(switch1,'clear wireless detected-client non-auth',timeout=1)
#if 0 == CheckLine(data0,'Y/N'):
SetCmd(switch1,'y',timeout=1)
data0 = SetCmd(switch1,'clear wireless ap rf-scan list',timeout=1)
#if 0 == CheckLine(data0,'Y/N'):
SetCmd(switch1,'y',timeout=1)


###if 0 == CheckLine(data0,'Y/N'):
##SetCmd(switch1,'y',timeout=1)
## RDM36362
# WirelessApProfileApply(switch1,'1')
    
# IdleAfter(80)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])   
#需要重启ap2
#RebootAp('AP',AP=ap2)

#end
printTimer(testname, 'End',suggestion = suggestionList)