#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.5.2.py - test case 4.5.2 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 4.5.2	Client QoS基本功能测试1（限速）
# 测试目的：Client QoS基本功能测试-限速
# 测试环境：同测试拓扑
# 测试描述：测试AP上面能够通过bandwidth limit对每个无线用户的的带宽限制，
#           可以分别对上行和下行的流量进行限制。
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package
s1vlanmac = GetVlanMac(switch1)
#Global Definition
Var_bandwidth_limit_500 = '1984'
Var_bandwidth_limit_700 = '3008'

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.5.2'
printTimer(testname,'Start','test speed limit, the basic function of client qos.')

################################################################################
#Step 1
#操作
#在UWS1配置network1的SSID为test1，关联vlan4092
#
#预期
#配置成功。
################################################################################
printStep(testname,'Step 1',\
          'set network 1 ssid test1 and vlan 4092,',\
          'config success.')
          
res1=res2=1
#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap client-qos')
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan '+Vlan4092)

data1 = SetCmd(switch1,'show wireless network','1')

#check
res1 = CheckLine(data1,'Default VLAN',Vlan4092,IC=True)
res2 = CheckLine(data1,'SSID',Network_name1,IC=True)

#result
printCheckStep(testname, 'Step 1',res1,res2)

################################################################################
#Step 2
#操作
#开启network1的Client Qos功能，并且设置上行带宽为500kbps。配置下发到AP1。
#
#预期
#Show wireless network 1显示有：
# Client QoS Bandwidth Limit Up.................. 448
# 配置下发成功, AP1，管理状态为managed
################################################################################

printStep(testname,'Step 2',\
          'enable client qos and set upload bandwith 500kbps,',\
          'apply ap profile to ap,',\
          'Check config success.')
          
res1=res2=1
#operate
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'client-qos enable')
SetCmd(switch1,'client-qos bandwidth-limit up',Var_bandwidth_limit_500)
res2 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')

# IdleAfter(Ac_ap_syn_time)      
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless network','1')
# data2 = SetCmd(switch1,'show wireless ap status')
    
#check
res1 = CheckLineList(data1,[('Client QoS Mode','Enable'), \
                            ('Client QoS Bandwidth Limit Up',Var_bandwidth_limit_500)],IC=True)
# res2 = CheckLine(data2,ap1mac,'Managed','Success',IC=True)
# if res2 != 0:
    # for tmpCounter in xrange(0,6):
        # IdleAfter('10')
        # data2 = SetCmd(switch1,'show wireless ap status')
        # res2 = CheckLine(data2,ap1mac,'Managed','Success',IC=True)
        # if res2 == 0:
            # break

#result
printCheckStep(testname, 'Step 2',res1,res2)

################################################################################
#Step 3
#操作
#STA1连接网络test1，在STA1上启动ixchariot向PC1发包，速率为1Mbps。
#
#预期
#上行转发速率为448kbps（5%偏差）
################################################################################
printStep(testname,'Step 3',\
          'STA1 connect to network 1,',\
          'STA1 send packets 10Mbps to pc1,',\
          'the packets upload speed is bandwith to 1984kps.')

res1=res2=res3=1
sta1_ipv4 = ''

#operate
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower) 

#获取STA1的地址
data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
if None != SearchResult1:
    sta1_ipv4 = SearchResult1.group(1)
    if None != re.search(Dhcp_pool2,sta1_ipv4):
        printRes('STA1 ip address: ' + sta1_ipv4)
        res2 = 0
    else:
        res2 = 1
        printRes('get address success but not match ip of vlan 4092')
else:
    res2 = 1
    sta1_ipv4 = '7.7.7.7'
    printRes('Failed: Get ipv4 address of STA1 failed')
  
res = CheckPing(pc1,sta1_ipv4,mode='linux',srcip=pc1_ipv4)
if res != 0:
    for tmpcounter in xrange(0,3):
        IdleAfter('2')
        res = CheckPing(pc1,sta1_ipv4,mode='linux',srcip=pc1_ipv4)
        if res == 0:
            break
if res == 0:
    data3 = SetCmd(pc1,'downloadtest -u http://' + sta1_ipv4 + '/upgrade.tar')
    re3 = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s',data3)
    if re3 is not None:
        speed = re3.group(1)
    else:
        speed = 0
    if (float(speed) > float(0.23)) and (float(speed) < float(0.27)):
        res3 = 0
    else:
        res3 = 1
else:
    res3 = 1
#result
printCheckStep(testname, 'Step 3',res1,res2,res3)

################################################################################
#Step 4
#操作
#更改network1的上行带宽为700kbps，配置下发到AP1
#
#预期
#配置成功。
################################################################################
printStep(testname,'Step 4',\
          'set upload bindwith 700kbps,',\
          'apply ap profile to ap,',\
          'Check config success.')
          
res1=res2=1
#operate
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'client-qos enable')
SetCmd(switch1,'client-qos bandwidth-limit up',Var_bandwidth_limit_700)
res2 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')
# IdleAfter(Ac_ap_syn_time)      
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless network','1')
data2 = SetCmd(switch1,'show wireless ap status')
    
#check
res1 = CheckLineList(data1,[('Client QoS Mode','Enable'), \
                            ('Client QoS Bandwidth Limit Up',Var_bandwidth_limit_700)],IC=True)
# res2 = CheckLine(data2,ap1mac,'Managed','Success',IC=True)
# if res2 != 0:
    # for tmpCounter in xrange(0,6):
        # IdleAfter('10')
        # data2 = SetCmd(switch1,'show wireless ap status')
        # res2 = CheckLine(data2,ap1mac,'Managed','Success',IC=True)
        # if res2 == 0:
            # break

#result
printCheckStep(testname, 'Step 4',res1,res2)

################################################################################
#Step 5
#操作
#STA1连接网络test1，在STA1上启动ixchariot向PC1发包，速率1Mbps。
#
#预期
#上行转发速率为640kbps。
################################################################################
printStep(testname,'Step 5',\
          'STA1 connect to network 1,',\
          'STA1 send packets tp pc 10Mbps,',\
          'The speed of packets is bandwith to 3008kbps.')

res1=1

#operate

#清除AC1上端口s1p2的数据信息
res = CheckPing(pc1,sta1_ipv4,mode='linux',srcip=pc1_ipv4)
if res != 0:
    for tmpcounter in xrange(0,3):
        IdleAfter('2')
        res = CheckPing(pc1,sta1_ipv4,mode='linux',srcip=pc1_ipv4)
        if res == 0:
            break
if res == 0:        
    data3 = SetCmd(pc1,'downloadtest -u http://' + sta1_ipv4 + '/upgrade.tar')
    re3 = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s',data3)
    if re3 is not None:
        speed = re3.group(1)
    else:
        speed = 0
    if (float(speed) > float(0.35)) and (float(speed) < float(0.40)):
        res3 = 0
    else:
        res3 = 1
else:
    res3 = 1

#result
printCheckStep(testname, 'Step 5',res3)

################################################################################
#Step 6
#操作
#关闭Client Qos功能。
#
#预期
#配置成功。
################################################################################
printStep(testname,'Step 6',\
          'close client-qos,',\
          'Check config success.')

res1=1
#operate
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no client-qos enable')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')
# IdleAfter(Ac_ap_syn_time) 

data1 = SetCmd(switch1,'show wireless network','1')

#check
res1 = CheckLine(data1,'Client QoS Mode','Disable',IC=True)

#result
printCheckStep(testname, 'Step 6',res1)

################################################################################
#Step 7
#操作
#STA1连接网络test1，在STA1上启动ixchariot向PC1发包，1Mbps
#
#预期
#上行速率为1Mbps。
################################################################################
printStep(testname,'Step 7',\
          'STA1 send packets to pc 1Mbps,',\
          'upload packets speed is about 1Mbps.')

res1=1

#operate
res = CheckPing(pc1,sta1_ipv4,mode='linux',srcip=pc1_ipv4)
if res != 0:
    for tmpcounter in xrange(0,3):
        IdleAfter('2')
        res = CheckPing(pc1,sta1_ipv4,mode='linux',srcip=pc1_ipv4)
        if res == 0:
            break
if res == 0:
    data3 = SetCmd(pc1,'downloadtest -u http://' + sta1_ipv4 + '/upgrade.tar')
    re3 = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s',data3)
    if re3 is not None:
        speed = re3.group(1)
    else:
        speed = 0
    if (float(speed) > float(1)):
        res3 = 0
    else:
        res3 = 1
else:
    res3 = 1
  
#result
printCheckStep(testname, 'Step 7',res3)

################################################################################
#Step 8
#操作
#开启network1的Client Qos功能，并且设置下行带宽为500kbps。配置下发到AP1。
#
#预期
#配置成功。
################################################################################
printStep(testname,'Step 8',\
          'enable client-qos and set down speed 500kbps,',\
          'Check config success.')
          
res1=res2=1
#operate
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'client-qos enable')
SetCmd(switch1,'client-qos bandwidth-limit down',Var_bandwidth_limit_500)
res2 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')

# IdleAfter(Ac_ap_syn_time)      
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless network 1')
data2 = SetCmd(switch1,'show wireless ap status')
    
#check
res1 = CheckLineList(data1,[('Client QoS Mode','Enable'), \
                            ('Client QoS Bandwidth Limit Down',Var_bandwidth_limit_500)],IC=True)
# res2 = CheckLine(data2,ap1mac,'Managed','Success',IC=True)
#RDM34910
# if res2 != 0:
    # for tmpCounter in xrange(0,6):
        # IdleAfter('10')
        # data2 = SetCmd(switch1,'show wireless ap status')
        # res2 = CheckLine(data2,ap1mac,'Managed','Success',IC=True)
        # if res2 == 0:
            # break

#result
printCheckStep(testname, 'Step 8',res1,res2)

################################################################################
#Step 9
#操作
#STA1连接网络test1，在PC1上启动ixchariot向STA1发包，速率为1Mbps。
#
#预期
#下行转发速率为1984kbps。
################################################################################
printStep(testname,'Step 9',\
          'STA1 connect to network 1,',\
          'pc1 send packets with ixchariot with speed 1Mbps,',\
          'the speed of down direction is 500kbps.')
#operate
res1=1
res = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
if res != 0:
    for tmpcounter in xrange(0,3):
        IdleAfter('2')
        res = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
        if res == 0:
            break
if res == 0:
    data3 = SetCmd(sta1,'downloadtest -u http://' + pc1_ipv4 + ':90/upgrade.tar')
    re3 = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s',data3)
    if re3 is not None:
        speed = re3.group(1)
    else:
        speed = 0
    if (float(speed) > float(0.23)) and (float(speed) < float(0.27)):
        res3 = 0
    else:
        res3 = 1
else:
    res3 = 1
    
#result
printCheckStep(testname, 'Step 9',res3)

################################################################################
#Step 10
#操作
#更改network1的下行带宽为700kbps，配置下发到AP1。
#
#预期
#配置下发成功。
################################################################################
printStep(testname,'Step 10',\
          'set banwith 700 down,',\
          'apply ap profile 1 to ap,',\
          'Check config success.')

res1=res2=1
#operate
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'client-qos enable')
SetCmd(switch1,'client-qos bandwidth-limit down',Var_bandwidth_limit_700)
res2 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')
# IdleAfter(Ac_ap_syn_time)      
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless network','1')
data2 = SetCmd(switch1,'show wireless ap status')
    
#check
res1 = CheckLineList(data1,[('Client QoS Mode','Enable'), \
                            ('Client QoS Bandwidth Limit Down',Var_bandwidth_limit_700)],IC=True)
# res2 = CheckLine(data2,ap1mac,'Managed','Success',IC=True)
#RDM34910
# if res2 != 0:
    # for tmpCounter in xrange(0,6):
        # IdleAfter('10')
        # data2 = SetCmd(switch1,'show wireless ap status')
        # res2 = CheckLine(data2,ap1mac,'Managed','Success',IC=True)
        # if res2 == 0:
            # break

#result
printCheckStep(testname, 'Step 10',res1,res2)

################################################################################
#Step 11
#操作
#STA1连接网络test1，在PC1上启动ixchariot向STA1发包，速率1Mbps。
#
#预期
#下行转发速率为700kbps。
################################################################################
printStep(testname,'Step 11',\
          'STA1 connect to network 1,',\
          'pc1 send packets to STA1 with 1Mbps,',\
          'the speed of down direction is 640kbps.')

res1=1

#operate
res = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
if res != 0:
    for tmpcounter in xrange(0,3):
        IdleAfter('2')
        res = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
        if res == 0:
            break
if res == 0:
    data3 = SetCmd(sta1,'downloadtest -u http://' + pc1_ipv4 + ':90/upgrade.tar')
    re3 = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s',data3)
    if re3 is not None:
        speed = re3.group(1)
    else:
        speed = 0
    if (float(speed) > float(0.35)) and (float(speed) < float(0.40)):
        res3 = 0
    else:
        res3 = 1
else:
    res3 = 1
#result
printCheckStep(testname, 'Step 11',res3)

################################################################################
#Step 12
#操作
#关闭Client Qos功能。
#
#预期
#配置成功。
################################################################################
printStep(testname,'Step 12',\
          'close the client-qos,',\
          'check config success.')
          
res1=1
#operate
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no','client-qos enable')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')
# IdleAfter(Ac_ap_syn_time) 

data1 = SetCmd(switch1,'show wireless network','1')

#check
res1 = CheckLine(data1,'Client QoS Mode','Disable',IC=True)
#result
printCheckStep(testname, 'Step 12',res1)

################################################################################
#Step 13
#操作
#STA1连接网络test1，在PC1上启动ixchariot向STA1发包，1Mbps。
#
#预期
#下行转发速率为1Mbps。
################################################################################
printStep(testname,'Step 13',\
          'STA1 connect to network 1,',\
          'pc send packets to STA1 with 1Mbps,',\
          'check the down speed is about 1Mbps.')
res1=1
#operate
res = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
if res != 0:
    for tmpcounter in xrange(0,3):
        IdleAfter('2')
        res = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
        if res == 0:
            break
if res == 0:
    data3 = SetCmd(sta1,'downloadtest -u http://' + pc1_ipv4 + ':90/upgrade.tar')
    re3 = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s',data3)
    if re3 is not None:
        speed = re3.group(1)
    else:
        speed = 0
    if (float(speed) > float(1)):
        res3 = 0
    else:
        res3 = 1
else:
    res3 = 1
#result
printCheckStep(testname, 'Step 13',res3)

################################################################################
#Step 14
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 14',\
          'Recover initial config for switches.')

#operate

#清除AC1上端口s1p1的数据信息
EnterEnableMode(switch1)
SetCmd(switch1,'clear counters')

##解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

EnterWirelessMode(switch1)
SetCmd(switch1,'no ap client-qos')
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no client-qos bandwidth-limit up')
SetCmd(switch1,'no client-qos bandwidth-limit down')
SetCmd(switch1,'vlan ' + Vlan4091)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')
# IdleAfter(Ac_ap_syn_time) 

#end
printTimer(testname, 'End')