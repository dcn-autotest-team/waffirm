# -*- coding: UTF-8 -*-#
#
# *******************************************************************************
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
# *******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
#     - zhangjxp RDM50329 2017.11.8
# *******************************************************************************
# Package
# Global Definition
s1vlanmac = GetVlanMac(switch1)
Var_bandwidth_limit_500 = '1984'
Var_bandwidth_limit_700 = '3008'

testname = 'TestCase 4.5.2'
avoiderror(testname)
printTimer(testname, 'Start', 'test speed limit, the basic function of client qos.')
# 防止sta的http服务异常停止
SetCmd(sta1, 'service httpd restart')
################################################################################
# Step 1
# 操作
# 在UWS1配置network1的SSID为test1，关联vlan4091
#
# 预期
# 配置成功。
################################################################################
printStep(testname, 'Step 1',
          'set network 1 ssid test1 and vlan 4091,',
          'config success.')

res1 = res2 = 1
# operate
# EnterInterfaceMode(switch3,s3p2)
# SetCmd(switch3,'shutdown')
# EnterInterfaceMode(switch3,s3p4)
# SetCmd(switch3,'shutdown')

# SetCmd(ap2,'set managed-ap mode down')

EnterWirelessMode(switch1)
SetCmd(switch1, 'ap client-qos')
EnterNetworkMode(switch1, '1')
SetCmd(switch1, 'ssid ' + Network_name1)
SetCmd(switch1, 'vlan ' + Vlan4091)

data1 = SetCmd(switch1, 'show wireless network', '1', timeout=5)

# check
res1 = CheckLine(data1, 'Default VLAN', Vlan4091, IC=True)
res2 = CheckLine(data1, 'SSID', Network_name1, IC=True)

# result
printCheckStep(testname, 'Step 1', res1, res2)

################################################################################
# Step 2
# 操作
# 开启network1的Client Qos功能，并且设置上行带宽为1984kbps。配置下发到AP1。
#
# 预期
# Show wireless network 1显示有：
# Client QoS Bandwidth Limit Up.................. 1984
# 配置下发成功, AP1，管理状态为managed
################################################################################

printStep(testname, 'Step 2',
          'enable client qos and set upload bandwith 1984kbps,',
          'apply ap profile to ap,',
          'Check config success.')

res1 = res2 = 1
# operate
EnterNetworkMode(switch1, '1')
SetCmd(switch1, 'client-qos enable')
SetCmd(switch1, 'client-qos bandwidth-limit up', Var_bandwidth_limit_500)
res2 = WirelessApplyProfileWithCheck(switch1, ['1'], [ap1mac])

EnterEnableMode(switch1)
data1 = SetCmd(switch1, 'show wireless network', '1')
# data2 = SetCmd(switch1,'show wireless ap status')

# check
res1 = CheckLineList(data1, [('Client QoS Mode', 'Enable'),
                             ('Client QoS Bandwidth Limit Up', Var_bandwidth_limit_500)], IC=True)

# result
printCheckStep(testname, 'Step 2', res1, res2)

################################################################################
# Step 3
# 操作
# STA1连接网络test1，在STA1上启动ixchariot向PC1发包，速率为10Mbps。
#
# 预期
# 上行转发速率为1984kbps（10%偏差）
################################################################################
printStep(testname, 'Step 3',
          'STA1 connect to network 1,',
          'STA1 send packets 10Mbps to pc1,',
          'the packets upload speed is bandwith to 1984kps.')

res1 = res2 = res3 = 1
sta1_ipv4 = ''

# operate
res1 = WpaConnectWirelessNetwork(sta1, Netcard_sta1, Network_name1, bssid=ap1mac_lower)
# 获取STA1的地址
sta1_ipresult = GetStaIp(sta1, checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
res2 = sta1_ipresult['res']

SetCmd(ap1, 'cat /proc/net/ap_qos/sta/' + sta2mac_type1.lower())
SetCmd(ap1, 'cat /proc/net/ap_qos/sta/' + sta1mac_type1.lower())
SetCmd(ap1, 'brctl show')

# 清除AC1上端口s1p1的数据信息

##SetCmd(switch1,'clear counters')

##发送1M速度的报文
##if 0==ConnectDsendWireless(testerip_sta1):
##    SetDsendStreamWireless(Port=testerp1_sta1,PortTypeConfig='0',StreamMode='0',StreamRateMode='pps',StreamRate='100', FrameSize='1250', \
##                   SouMac = sta1mac,DesMac=s1vlanmac,Protocl='ipv4',SouIp = sta1_ipv4, DesIp = pc1_ipv4)
##    StartTransmitWireless(testerp1_sta1)
##    IdleAfter(Rate_stable_wait_time)
##    DisconnectDsendWireless()

##检查交换机出端口的速率

##i_time = 0
##while i_time < 10:
##    data = SetCmd(switch1,'show interface',s1p1)
##    rate_output_s1p1 =  int(str(GetValueBetweenTwoValuesInData (data,'5 second input rate','bits')).lstrip().rstrip())
##    printRes('rate_output_s1p1= '+str(rate_output_s1p1))
##    res3 = 0 if rate_output_s1p1 <= (Var_bandwith_500kbit*(1+Var_banwith_differ)) and rate_output_s1p1 >= (Var_bandwith_500kbit*(1 - Var_banwith_differ)) else -1
##    if 0==res3:
##        break
##    i_time += 1
##    IdleAfter(Ac_ap_syn_time)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2
if GetWhetherkeepon(keeponflag):
    res = CheckPing(pc1, sta1_ipv4, mode='linux', srcip=pc1_ipv4, returnPercent=True)
    if res != 100:
        for tmpcounter in xrange(0, 3):
            IdleAfter('2')
            res = CheckPing(pc1, sta1_ipv4, mode='linux', srcip=pc1_ipv4, returnPercent=True)
            if res == 100:
                break
    if res > 0:
        for i in range(3):
            SetCmd(sta1, 'systemctl disable iptables.service')
            data3 = SetCmd(pc1, 'downloadtest -u http://' + sta1_ipv4 + '/upgrade1.tar')
            re3 = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s', data3)
            if re3 is not None:
                speed = re3.group(1)
            else:
                speed = 0
            print speed
            if (float(speed) > float(0.20)) and (float(speed) < float(0.27)):
                res3 = 0
            else:
                res3 = 1
            SetCmd(ap1, 'cat /proc/net/ap_qos/sta/' + sta2mac_type1.lower())
            SetCmd(ap1, 'cat /proc/net/ap_qos/sta/' + sta1mac_type1.lower())
            if res3 == 0:
                break
    else:
        res3 = 1
# result
printCheckStep(testname, 'Step 3', res1, res2, res3)

################################################################################
# Step 4
# 操作
# 更改network1的上行带宽为700kbps，配置下发到AP1
#
# 预期
# 配置成功。
################################################################################
printStep(testname, 'Step 4',
          'set upload bindwith 3008kbps,',
          'apply ap profile to ap,',
          'Check config success.')

res1 = res2 = 1
# operate
EnterNetworkMode(switch1, '1')
SetCmd(switch1, 'client-qos enable')
SetCmd(switch1, 'client-qos bandwidth-limit up', Var_bandwidth_limit_700)
WirelessApplyProfileWithCheck(switch1, ['1'], [ap1mac])

EnterEnableMode(switch1)
data1 = SetCmd(switch1, 'show wireless network', '1')
data2 = SetCmd(switch1, 'show wireless ap status')

# check
res1 = CheckLineList(data1, [('Client QoS Mode', 'Enable'),
                             ('Client QoS Bandwidth Limit Up', Var_bandwidth_limit_700)], IC=True)
res2 = CheckLine(data2, ap1mac, 'Managed', 'Success', IC=True)
# RDM34910
if res2 != 0:
    for tmpCounter in xrange(0, 6):
        IdleAfter('10')
        data2 = SetCmd(switch1, 'show wireless ap status')
        res2 = CheckLine(data2, ap1mac, 'Managed', 'Success', IC=True)
        if res2 == 0:
            break

# result
printCheckStep(testname, 'Step 4', res1, res2)

################################################################################
# Step 5
# 操作
# STA1连接网络test1，在STA1上启动ixchariot向PC1发包，速率10Mbps。
#
# 预期
# 上行转发速率为3008kbps。
################################################################################
printStep(testname, 'Step 5',
          'STA1 connect to network 1,',
          'STA1 send packets tp pc 10Mbps,',
          'The speed of packets is bandwith to 3008kbps.')

res1 = res2 = res3 = 1
# operate
res1 = WpaConnectWirelessNetwork(sta1, Netcard_sta1, Network_name1, bssid=ap1mac_lower)

# 获取STA1的地址
sta1_ipresult = GetStaIp(sta1, checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
res2 = sta1_ipresult['res']

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2
if GetWhetherkeepon(keeponflag):
    # 清除AC1上端口s1p1的数据信息
    res = CheckPing(pc1, sta1_ipv4, mode='linux', srcip=pc1_ipv4, returnPercent=True)
    if res != 100:
        for tmpcounter in xrange(0, 3):
            IdleAfter('2')
            res = CheckPing(pc1, sta1_ipv4, mode='linux', srcip=pc1_ipv4, returnPercent=True)
            if res == 100:
                break
    if res > 0:
        data3 = SetCmd(pc1, 'downloadtest -u http://' + sta1_ipv4 + '/upgrade1.tar')
        re3 = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s', data3)
        if re3 is not None:
            speed = re3.group(1)
        else:
            speed = 0
        if (float(speed) > float(0.29)) and (float(speed) < float(0.42)):
            res3 = 0
        else:
            res3 = 1
        SetCmd(ap1, 'cat /proc/net/ap_qos/sta/' + sta2mac_type1.lower())
        SetCmd(ap1, 'cat /proc/net/ap_qos/sta/' + sta1mac_type1.lower())
    else:
        res3 = 1
# result
printCheckStep(testname, 'Step 5', res3)

################################################################################
# Step 6
# 操作
# 关闭Client Qos功能。
#
# 预期
# 配置成功。
################################################################################
printStep(testname, 'Step 6',
          'close client-qos,',
          'Check config success.')

res1 = 1
# operate
EnterNetworkMode(switch1, '1')
SetCmd(switch1, 'no client-qos enable')
WirelessApplyProfileWithCheck(switch1, ['1'], [ap1mac])

data1 = SetCmd(switch1, 'show wireless network', '1')

# check
res1 = CheckLine(data1, 'Client QoS Mode', 'Disable', IC=True)

# result
printCheckStep(testname, 'Step 6', res1)

################################################################################
# Step 7
# 操作
# STA1连接网络test1，在STA1上启动ixchariot向PC1发包，1Mbps
#
# 预期
# 上行速率为1Mbps。
################################################################################
printStep(testname, 'Step 7',
          'STA1 send packets to pc larger than 1Mbps,',
          'upload packets speed is larger than 1Mbps.')

res1 = res2 = res3 = 1

# operate
res1 = WpaConnectWirelessNetwork(sta1, Netcard_sta1, Network_name1, bssid=ap1mac_lower)

# 获取STA1的地址
sta1_ipresult = GetStaIp(sta1, checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
res2 = sta1_ipresult['res']

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2
if GetWhetherkeepon(keeponflag):
    res = CheckPing(pc1, sta1_ipv4, mode='linux', srcip=pc1_ipv4, returnPercent=True)
    if res != 100:
        for tmpcounter in xrange(0, 3):
            IdleAfter('2')
            res = CheckPing(pc1, sta1_ipv4, mode='linux', srcip=pc1_ipv4, returnPercent=True)
            if res == 100:
                break
    if res > 0:
        data3 = SetCmd(pc1, 'downloadtest -u http://' + sta1_ipv4 + '/upgrade.tar')
        re3 = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s', data3)
        if re3 is not None:
            speed = re3.group(1)
        else:
            speed = 0
        if (float(speed) > float(1)):
            res3 = 0
        else:
            res3 = 1
        SetCmd(ap1, 'cat /proc/net/ap_qos/sta/' + sta2mac_type1.lower())
        SetCmd(ap1, 'cat /proc/net/ap_qos/sta/' + sta1mac_type1.lower())
    else:
        res3 = 1
# result
printCheckStep(testname, 'Step 7', res3)

################################################################################
# Step 8
# 操作
# 开启network1的Client Qos功能，并且设置下行带宽为1984kbps。配置下发到AP1。
#
# 预期
# 配置成功。
################################################################################
printStep(testname, 'Step 8',
          'enable client-qos and set down speed 1984kbps,',
          'Check config success.')

res1 = res2 = 1
# operate
EnterNetworkMode(switch1, '1')
SetCmd(switch1, 'client-qos enable')
SetCmd(switch1, 'client-qos bandwidth-limit down', Var_bandwidth_limit_500)
WirelessApplyProfileWithCheck(switch1, ['1'], [ap1mac])

EnterEnableMode(switch1)
data1 = SetCmd(switch1, 'show wireless network 1')
data2 = SetCmd(switch1, 'show wireless ap status')

# check
res1 = CheckLineList(data1, [('Client QoS Mode', 'Enable'),
                             ('Client QoS Bandwidth Limit Down', Var_bandwidth_limit_500)], IC=True)
res2 = CheckLine(data2, ap1mac, 'Managed', 'Success', IC=True)
# RDM34910
if res2 != 0:
    for tmpCounter in xrange(0, 6):
        IdleAfter('10')
        data2 = SetCmd(switch1, 'show wireless ap status')
        res2 = CheckLine(data2, ap1mac, 'Managed', 'Success', IC=True)
        if res2 == 0:
            break

# result
printCheckStep(testname, 'Step 8', res1, res2)

################################################################################
# Step 9
# 操作
# STA1连接网络test1，在PC1上启动ixchariot向STA1发包，速率为1Mbps。
#
# 预期
# 下行转发速率为1984kbps。
################################################################################
printStep(testname, 'Step 9',
          'STA1 connect to network 1,',
          'pc1 send packets with ixchariot with speed 10Mbps,',
          'the speed of down direction is 1984kbps.')
res1 = res2 = res3 = 1
# operate
res1 = WpaConnectWirelessNetwork(sta1, Netcard_sta1, Network_name1, bssid=ap1mac_lower)
# 获取STA1的地址
sta1_ipresult = GetStaIp(sta1, checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
res2 = sta1_ipresult['res']
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2
if GetWhetherkeepon(keeponflag):
    res = CheckPing(sta1, pc1_ipv4, mode='linux', returnPercent=True)
    if res != 100:
        for tmpcounter in xrange(0, 3):
            IdleAfter('2')
            res = CheckPing(sta1, pc1_ipv4, mode='linux', returnPercent=True)
            if res == 100:
                break
    if res > 0:
        data3 = SetCmd(sta1, 'downloadtest -u http://' + pc1_ipv4 + ':90/upgrade1.tar')
        re3 = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s', data3)
        if re3 is not None:
            speed = re3.group(1)
        else:
            speed = 0
        if (float(speed) > float(0.20)) and (float(speed) < float(0.27)):
            res3 = 0
        else:
            res3 = 1
        SetCmd(ap1, 'cat /proc/net/ap_qos/sta/' + sta2mac_type1.lower())
        SetCmd(ap1, 'cat /proc/net/ap_qos/sta/' + sta1mac_type1.lower())
    else:
        res3 = 1
# result
printCheckStep(testname, 'Step 9', res3)

################################################################################
# Step 10
# 操作
# 更改network1的下行带宽为3008kbps，配置下发到AP1。
#
# 预期
# 配置下发成功。
################################################################################
printStep(testname, 'Step 10',
          'set banwith 3008 down,',
          'apply ap profile 1 to ap,',
          'Check config success.')

res1 = res2 = 1
# operate
EnterNetworkMode(switch1, '1')
SetCmd(switch1, 'client-qos enable')
SetCmd(switch1, 'client-qos bandwidth-limit down', Var_bandwidth_limit_700)
WirelessApplyProfileWithCheck(switch1, ['1'], [ap1mac])

EnterEnableMode(switch1)
data1 = SetCmd(switch1, 'show wireless network', '1')
data2 = SetCmd(switch1, 'show wireless ap status')

# check
res1 = CheckLineList(data1, [('Client QoS Mode', 'Enable'),
                             ('Client QoS Bandwidth Limit Down', Var_bandwidth_limit_700)], IC=True)
res2 = CheckLine(data2, ap1mac, 'Managed', 'Success', IC=True)
# RDM34910
if res2 != 0:
    for tmpCounter in xrange(0, 6):
        IdleAfter('10')
        data2 = SetCmd(switch1, 'show wireless ap status')
        res2 = CheckLine(data2, ap1mac, 'Managed', 'Success', IC=True)
        if res2 == 0:
            break

# result
printCheckStep(testname, 'Step 10', res1, res2)

################################################################################
# Step 11
# 操作
# STA1连接网络test1，在PC1上启动ixchariot向STA1发包，速率1Mbps。
#
# 预期
# 下行转发速率为3008kbps。
################################################################################
printStep(testname, 'Step 11',
          'STA1 connect to network 1,',
          'pc1 send packets to STA1 with 1Mbps,',
          'the speed of down direction is 3008kbps.')

res1 = res2 = res3 = 1
# operate
res1 = WpaConnectWirelessNetwork(sta1, Netcard_sta1, Network_name1, bssid=ap1mac_lower)
# 获取STA1的地址
sta1_ipresult = GetStaIp(sta1, checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
res2 = sta1_ipresult['res']
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2
if GetWhetherkeepon(keeponflag):
    res = CheckPing(sta1, pc1_ipv4, mode='linux', returnPercent=True)
    if res != 100:
        for tmpcounter in xrange(0, 3):
            IdleAfter('2')
            res = CheckPing(sta1, pc1_ipv4, mode='linux', returnPercent=True)
            if res == 100:
                break
    if res > 0:
        data3 = SetCmd(sta1, 'downloadtest -u http://' + pc1_ipv4 + ':90/upgrade1.tar')
        re3 = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s', data3)
        if re3 is not None:
            speed = re3.group(1)
        else:
            speed = 0
        if (float(speed) > float(0.30)) and (float(speed) < float(0.42)):
            res3 = 0
        else:
            res3 = 1
        SetCmd(ap1, 'cat /proc/net/ap_qos/sta/' + sta2mac_type1.lower())
        SetCmd(ap1, 'cat /proc/net/ap_qos/sta/' + sta1mac_type1.lower())
    else:
        res3 = 1
    # result
    printCheckStep(testname, 'Step 11', res3)

################################################################################
# Step 12
# 操作
# 关闭Client Qos功能。
#
# 预期
# 配置成功。
################################################################################
printStep(testname, 'Step 12',
          'close the client-qos,',
          'check config success.')

res1 = 1
# operate
EnterNetworkMode(switch1, '1')
SetCmd(switch1, 'no', 'client-qos enable')
WirelessApplyProfileWithCheck(switch1, ['1'], [ap1mac])

data1 = SetCmd(switch1, 'show wireless network', '1')

# check
res1 = CheckLine(data1, 'Client QoS Mode', 'Disable', IC=True)
# result
printCheckStep(testname, 'Step 12', res1)

################################################################################
# Step 13
# 操作
# STA1连接网络test1，在PC1上启动ixchariot向STA1发包，10Mbps。
#
# 预期
# 下行转发速率为1Mbps。
################################################################################
printStep(testname, 'Step 13',
          'STA1 connect to network 1,',
          'pc send packets to STA1 larger than 10Mbps,',
          'check the down speed is larger than 10Mbps.')
res1 = res2 = res3 = 1
# operate
res1 = WpaConnectWirelessNetwork(sta1, Netcard_sta1, Network_name1, bssid=ap1mac_lower)
# 获取STA1的地址
sta1_ipresult = GetStaIp(sta1, checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
res2 = sta1_ipresult['res']
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2
if GetWhetherkeepon(keeponflag):
    res = CheckPing(sta1, pc1_ipv4, mode='linux', returnPercent=True)
    if res != 100:
        for tmpcounter in xrange(0, 3):
            IdleAfter('2')
            res = CheckPing(sta1, pc1_ipv4, mode='linux', returnPercent=True)
            if res == 100:
                break
    if res > 0:
        data3 = SetCmd(sta1, 'downloadtest -u http://' + pc1_ipv4 + ':90/upgrade.tar')
        re3 = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s', data3)
        if re3 is not None:
            speed = re3.group(1)
        else:
            speed = 0
        if (float(speed) > float(1)):
            res3 = 0
        else:
            res3 = 1
        SetCmd(ap1, 'cat /proc/net/ap_qos/sta/' + sta2mac_type1.lower())
        SetCmd(ap1, 'cat /proc/net/ap_qos/sta/' + sta1mac_type1.lower())
    else:
        res3 = 1
# result
printCheckStep(testname, 'Step 13', res3)

################################################################################
# Step 14
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 14',
          'Recover initial config for switches.')

# operate

# 清除AC1上端口s1p1的数据信息
EnterEnableMode(switch1)
SetCmd(switch1, 'clear counters')

##解关联
WpaDisconnectWirelessNetwork(sta1, Netcard_sta1)

EnterWirelessMode(switch1)
SetCmd(switch1, 'no ap client-qos')
EnterNetworkMode(switch1, '1')
SetCmd(switch1, 'no client-qos bandwidth-limit up')
SetCmd(switch1, 'no client-qos bandwidth-limit down')
SetCmd(switch1, 'vlan ' + Vlan4091)

WirelessApplyProfileWithCheck(switch1, ['1'], [ap1mac])

# EnterInterfaceMode(switch3,s3p2)
# SetCmd(switch3,'no shutdown')
# EnterInterfaceMode(switch3,s3p4)
# SetCmd(switch3,'no shutdown')

# SetCmd(ap2,'set managed-ap mode up')
# IdleAfter(20)
# CheckSutCmd(switch1,'show wireless ap status', \
# check=[(ap2mac,'Managed','Success')], \
# waittime=5,retry=20,interval=5,IC=True)
# end
printTimer(testname, 'End')
