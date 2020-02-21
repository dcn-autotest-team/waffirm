# -*- coding: UTF-8 -*-#
#
# *******************************************************************************
# waffirm_mt4762_WDS.py
#
# Author:  (zhangjxp)
#
# Version 1.0.0
#
# Date:  2017-3-30 9:54:28
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# mt4762  Satellite Aps管理状态从success变为fail
# 测试目的：测试Satellite Aps和root AP建立WDS链路
# 测试环境：同测试拓扑
# 测试描述：1.设置AP1为root ap，AP2为satelliateap。
# 2.分别在root ap和satelliateap上查看wds链路状态。
# 3.在AC1上查看satellite ap的管理状态。
# 4.无线用户关联AP1和AP2后能互通。
#
# *******************************************************************************
# Change log:
#     - creadte by zhangjxp 2017.4.27
# *******************************************************************************
# Package

# Global Definition

# Source files

# Procedure Definition

# Functional Code

testname = 'TestCase mt4762_WDS'
avoiderror(testname)
printTimer(testname, 'Start')
# 2.4G、5G差异化配置,test24gflag为True代表执行2.4G脚本，False代表执行5G脚本
if test24gflag:
    radio = 'radio 1'
else:
    radio = 'radio 2'
################################################################################
# Step 1
#
# 操作
# 断开AP2和S3的物理链路，检查AP1是否正常上线
# AC1上通过命令show wireless  ap status查看AP1的列表
#
# 预期
# AP1成功被AC1管理，显示记录为
# MAC Address为AP1MAC，IP Address为AP1IP，Profile显示为1
#
################################################################################
printStep(testname, 'Step 1',
          'Shutdown s3p4',
          'Check AP2 is not managed by AC1')
res1 = 1
res2 = 1
# operate
# S3配置
EnterConfigMode(switch3)
SetCmd(switch3, 'interface', s3p4)
SetCmd(switch3, 'shutdown')
# s1配置
ap2newip = '20.1.1.6'
EnterWirelessMode(switch1)
SetCmd(switch1, 'discovery ip-list', ap2newip)
# AC1 配置
i = 1
while i < 10:
    EnterEnableMode(switch1)
    data1 = SetCmd(switch1, 'show wireless ap status')
    res1 = CheckLine(data1, ap1mac, Ap1_ipv4, '1', 'Managed', 'Success', IC=True)
    res2 = CheckLine(data1, ap2mac, Ap2_ipv4, '2', 'Failed', 'Not\s+Config', IC=True)
    if res1 == 0 and res2 == 0:
        break
    IdleAfter('5')
    i = i + 1
# result
printCheckStep(testname, 'Step 1', res1, res2)

################################################################################
# Step 2
# 操作
# AC1在network 1中配置wds相关配置，下发配置到AP1
# wireless
# network 1
# ssid test1
# wds-mode rootap
# wds-remote-vapAP2 MAC
# Wireless ap profile apply 1
# 在AP1上用getwds wds0查看wds配置。
#
# 预期
# 在AP1上用getwds wds0查看：wds-mode显示为rootap，wds-security-policy显示为plain-text，
# remote-mac显示为AP2 MAC。
################################################################################
printStep(testname, 'Step 2',
          'Config WDS configaration in network 1 on AC1',
          'Apply ap profile 1')

res1 = 1
# operate
EnterConfigMode(switch1)
SetCmd(switch1, 'wireless')
SetCmd(switch1, 'network 1')
SetCmd(switch1, 'wds-mode rootap')
SetCmd(switch1, 'wds-remote-vap', ap2mac)
SetCmd(switch1, 'ssid testWDS')
WirelessApProfileApply(switch1, '1')
IdleAfter(Apply_profile_wait_time)

# check
ap2MAC, number = re.subn('-', ':', ap2mac)
SetCmd(ap1, '\n')
data = SetCmd(ap1, 'get wds wds0')
checklist1 = []
checklist1.append(('wds-mode', 'rootap'))
checklist1.append(('wds-ssid', 'testWDS'))
checklist1.append(('wds-security-policy', 'plain-text'))
checklist1.append(('remote-mac', ap2MAC))
res1 = CheckLineList(data, checklist1)

# result
printCheckStep(testname, 'Step 2', res1)

################################################################################
# Step 3
#
# 操作
# 在AP2上配置wds相关配置：
# set wds wds0wds-ssid test1
# set wds wds0wds-security-policyplain-text
# set wds wds0remote-macAP1MAC
# set wds wds0wds-status up
# set wds wds0wds-modesatelliteap
# 在AP1和AP2上用getwds wds0查看wds连接状态。
#
# 预期
# 在AP1和AP2上查看wds连接状态：
# wds-link显示为linked。
################################################################################
printStep(testname, 'Step 3',
          'Config WDS configuration on AP2',
          'WDS link between AP1 and AP2 is successfully established')

res1 = 1
# operate
# MAC格式为00:00:00:00:00:00
ap1MAC, number = re.subn('-', ':', ap1mac)
# FactoryResetMultiAp([ap2])
SetCmd(ap2, '\n')
Receiver(ap2, 'factory-reset', promotePatten='y/n', promoteTimeout=10)
IdleAfter(1)
Receiver(ap2, 'y')
IdleAfter(50)
ApLogin(ap2, retry=30)

SetCmd(ap2, '\n')
SetCmd(ap2, 'set management static-ip', ap2newip)
SetCmd(ap2, 'set static-ip-route gateway', If_vlan20_s3_ipv4)
SetCmd(ap2, 'set wds wds0 wds-ssid testWDS')
SetCmd(ap2, 'set wds wds0 wds-security-policy plain-text')
SetCmd(ap2, 'set wds wds0 remote-mac', ap1MAC)
SetCmd(ap2, 'set wds wds0 wds-mode satelliteap')
SetCmd(ap2, 'set wds wds0 wds-status up')
# check
i = 1
while i < 30:
    data = SetCmd(ap2, 'get wds wds0')
    res1 = CheckLine(data, 'wds-link', 'linked', RS=True, IC=True)
    if res1 == 0:
        break
    IdleAfter('5')
    i = i + 1

if res1 != 0:
    print('If step3 fail, please pull out the cable connecting AP2 with S3P4, and run this case again')
# result
printCheckStep(testname, 'Step 3', res1)
if res1 == 0:
    ################################################################################
    # Step 4
    # 操作
    # 在AC1上查看AP2的状态。
    #
    # 预期
    # AP2成功被AC1管理，显示两条记录为
    # MAC Address为AP2MAC，IP Address为AP2IP，Profile显示为2

    ################################################################################
    printStep(testname, 'Step 4',
              'AC1 managed AP2 sucessfully')

    res1 = 1
    res2 = 1
    # operate&check
    i = 1
    while i < 60:
        EnterEnableMode(switch1)
        data1 = SetCmd(switch1, 'show wireless ap status')
        res1 = CheckLine(data1, ap1mac, Ap1_ipv4, '1', 'Managed', 'Success', IC=True)
        res2 = CheckLine(data1, ap2mac, ap2newip, '2', 'Managed', 'Success', IC=True)
        if res1 == 0 and res2 == 0:
            break
        IdleAfter('10')
        i = i + 1
    # result
    printCheckStep(testname, 'Step 4', res1, res2)
    if res2 == 0:
        ################################################################################
        # Step 5
        # 操作
        # 无线客户STA1关联到AP1的network2，无线客户STA2关联到AP2的network2，在STA1上pingSTA2。
        #
        # 预期
        # STA1和STA2能互通。
        ################################################################################
        printStep(testname, 'Step 5',
                  'STA1 connect to AP1',
                  'STA2 connect to AP2',
                  'STA1 ping STA2 successfully')

        res1 = 1
        # operate
        # AC1配置
        EnterConfigMode(switch1)
        SetCmd(switch1, 'wireless')
        SetCmd(switch1, 'network 101')
        SetCmd(switch1, 'ssid testR')
        SetCmd(switch1, 'vlan 4091')
        SetCmd(switch1, 'network 102')
        SetCmd(switch1, 'ssid testS')
        SetCmd(switch1, 'vlan 4091')
        SetCmd(switch1, 'exit')
        SetCmd(switch1, 'ap profile 1')
        SetCmd(switch1, radio)
        SetCmd(switch1, 'vap 1')
        SetCmd(switch1, 'network 101')
        SetCmd(switch1, 'enable')
        SetCmd(switch1, 'end')
        EnterConfigMode(switch1)
        SetCmd(switch1, 'wireless')
        SetCmd(switch1, 'ap profile 2')
        SetCmd(switch1, radio)
        SetCmd(switch1, 'vap 1')
        SetCmd(switch1, 'network 102')
        SetCmd(switch1, 'enable')
        SetCmd(switch1, 'end')
        WirelessApProfileApply(switch1, '1')
        IdleAfter(Apply_profile_wait_time)
        WirelessApProfileApply(switch1, '2')
        IdleAfter(Apply_profile_wait_time)
        # sta1，sta2配置
        res1 = WpaConnectWirelessNetwork(sta1, Netcard_sta1, 'testR', bssid=ap1mac_type1_network2)
        res2 = WpaConnectWirelessNetwork(sta2, Netcard_sta2, 'testS', bssid=ap2mac_type1_network2)
        IdleAfter(10)
    # check
    # 获取STA1,STA2的地址
    sta1_ipresult = GetStaIp(sta1, checkippool=Dhcp_pool1)
    sta1_ipv4 = sta1_ipresult['ip']
    res3 = sta1_ipresult['res']

    sta2_ipresult = GetStaIp(sta2, checkippool=Dhcp_pool1)
    sta2_ipv4 = sta2_ipresult['ip']
    res4 = sta2_ipresult['res']

    # STA1和STA2是否能互通
    res6 = CheckPing(sta2, sta1_ipv4, mode='linux')
    res5 = CheckPing(sta1, sta2_ipv4, mode='linux')

    # result
    printCheckStep(testname, 'Step 5', res1, res2, res3, res4, res5, res6)

################################################################################
# Step 6
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 6',
          'Recover initial config')

# operate

# S3、AP2恢复
SetCmd(ap2, '\n')
Receiver(ap2, 'factory-reset', promotePatten='y/n', promoteTimeout=10)
IdleAfter(1)
Receiver(ap2, 'y')
IdleAfter(40)
EnterConfigMode(switch3)
SetCmd(switch3, 'interface', s3p4)
SetCmd(switch3, 'no shutdown')
ApLogin(ap2, retry=30)

# AP2恢复
SetCmd(ap2, '\n')
SetCmd(ap2, 'set management static-ip', Ap2_ipv4)
SetCmd(ap2, 'set management static-ipv6', Ap2_ipv6)
SetCmd(ap2, 'set management dhcp-status down')
SetCmd(ap2, 'set management dhcpv6-status down')
SetCmd(ap2, 'set static-ip-route gateway', If_vlan30_s3_ipv4)
SetCmd(ap2, 'set static-ipv6-route gateway', If_vlan30_s3_ipv6)
SetCmd(ap2, 'set management static-ipv6-prefix-length 64')
SetCmd(ap2, 'save-running')

# AC1恢复
EnterWirelessMode(switch1)
SetCmd(switch1, 'network 1')
SetCmd(switch1, 'no wds-mode')
SetCmd(switch1, 'no wds-remote-vap')
SetCmd(switch1, 'no security mode')
SetCmd(switch1, 'no wpa key')
SetCmd(switch1, 'ssid ' + Network_name1)
SetCmd(switch1, 'vlan 4091')
EnterWirelessMode(switch1)
SetCmd(switch1, 'ap profile 1')
SetCmd(switch1, radio)
SetCmd(switch1, 'vap 1')
SetCmd(switch1, 'network 2')
SetCmd(switch1, 'enable')
EnterWirelessMode(switch1)
SetCmd(switch1, 'ap profile 2')
SetCmd(switch1, radio)
SetCmd(switch1, 'vap 1')
SetCmd(switch1, 'network 2')
SetCmd(switch1, 'enable')
EnterWirelessMode(switch1)
SetCmd(switch1, 'no network 101')
SetCmd(switch1, 'no network 102')

WirelessApplyProfileWithCheck(switch1, ['1', '2'], [ap1mac, ap2mac])

EnterConfigMode(switch1)
SetCmd(switch1, 'wireless')
SetCmd(switch1, 'no discovery ip-list', ap2newip)

# end
printTimer(testname, 'End')
