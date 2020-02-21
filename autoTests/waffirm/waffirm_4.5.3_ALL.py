# -*- coding: UTF-8 -*-#
#
# *******************************************************************************
# waffirm_4.5.3.py - test case 4.5.3 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 4.5.3	Client QoS基本功能测试2（IP ACL）
# 测试目的：Client QoS基本功能测试-IP ACL
# 测试环境：同测试拓扑
# 测试描述：在AP的vap上绑定ip acl，可以控制特定IP流量的转发，
#           绑定acl可以分为up方向和down方向，分别对通过ap的上行流量和下行流量进行控制
#
# *******************************************************************************
# Change log:
#     - 2017.5.16 lupingc RDM49103
#     - lupingc RDM49074 2017.5.17
#     - zhangjxp RDM50657 2017.12.20
# *******************************************************************************
# Package
# Global Definition
CMD_Set_acl_100_deny_icmp_net91_to_host10 = 'access-list 100 deny icmp ' + Dhcp_pool1 + '0' + \
                                            ' 0.0.0.255 host-destination ' + pc1_ipv4
CMD_Set_acl_101_deny_icmp_host10_to_net91 = 'access-list 101 deny icmp host-source ' + pc1_ipv4 + ' ' + \
                                            Dhcp_pool1 + '0' + ' 0.0.0.255'

# Source files

# Procedure Definition

# Functional Code

testname = 'TestCase 4.5.3'
avoiderror(testname)
printTimer(testname, 'Start', 'test ip-acl, the basic function of client qos.')

################################################################################
# Step 1
# 操作
# AC1 上面配置ip ACL，：
##access-list 100 deny icmp source 192.168.91.0 0.0.0.255 host-destination 192.168.10.2
##access-list 100 permit any-source any-destination
##access-list 101 deny icmp host-source 192.168.10.2 destination 192.168.91.0 0.0.0.255
##access-list 101 permit any-source any-destination
# 无线全局开启Client QoS功能。
##Wireless
##Ap client-qos
# 开启network1的Client Qos功能,并设置使用VLAN 4091。
##Network 1
##Client-qos enable
# 将ACL 100绑定到network 1上行方向，ACL 101绑定到network 1的下行方向并把配置下发到AP1。
##Wireless
##Network 1
##client-qos access-control up ip 100\
##vlan 4091
##exit
##exit
##exit
##wireless ap profile apply 1
#
# 预期
# 配置成功。
################################################################################
printStep(testname, 'Step 1',
          'set ip acl 100 deny icmp source 192.168.91.0 0.0.0.255 host-destination 25.1.1.1192.168.10.2,',
          'access-list 100 permit any-source any-destination,',
          'access-list 101 deny icmp host-source 192.168.10.2 destination 192.168.91.0 0.0.0.255,',
          'access-list 101 permit any-source any-destination,',
          'config success.')

# res1 = res2 = res3 = res4 = 1
# operate

EnterNetworkMode(switch1, '1')
SetCmd(switch1, 'ssid ' + Network_name1)
SetCmd(switch1, 'vlan ' + Vlan4091)

EnterConfigMode(switch1)
SetCmd(switch1, CMD_Set_acl_100_deny_icmp_net91_to_host10)
SetCmd(switch1, CMD_Set_acl_101_deny_icmp_host10_to_net91)
SetCmd(switch1, 'access-list 100 permit ip any-source any-destination')
SetCmd(switch1, 'access-list 101 permit ip any-source any-destination')

# 无线全局开启 qos
EnterWirelessMode(switch1)
SetCmd(switch1, 'ap client-qos')
# 开启network 1 qos
EnterNetworkMode(switch1, '1')
SetCmd(switch1, 'client-qos enable')

# Client-qos enable将ACL 100绑定到network 1上行方向
SetCmd(switch1, 'client-qos access-control up ip 100')

# 配置下发
WirelessApplyProfileWithCheck(switch1, ['1'], [ap1mac])
EnterEnableMode(switch1)
data1 = SetCmd(switch1, 'show access-lists')
data2 = SetCmd(switch1, 'show wireless')
data3 = SetCmd(switch1, 'show wireless network', '1')

# check
res1 = CheckLineInOrder(data1, ['access-list 100',
                                'deny icmp ' + Dhcp_pool1 + '0' + ' 0.0.0.255 host-destination ' + pc1_ipv4,
                                'permit ip any-source any-destination'], IC=True)
res2 = CheckLineInOrder(data1, ['access-list 101',
                                'deny icmp host-source ' + pc1_ipv4 + ' ' + Dhcp_pool1 + '0' + ' 0.0.0.255',
                                'permit ip any-source any-destination'], IC=True)
res3 = CheckLine(data2, 'AP Client QoS Mode', 'Enable', IC=True)
res4 = CheckLineList(data3, [('Client QoS Mode', 'Enable'),
                             ('Client QoS Access Control Up', 'IP - 100')], IC=True)

# result
printCheckStep(testname, 'Step 1', res1, res2, res3, res4)

################################################################################
# Step 2
# 操作
# STA1关联到网络test1
#
# 预期
# STA1关联成功，获取192.168.91.X网段的IP地址。
################################################################################
printStep(testname, 'Step 2',
          'STA1 connect to network 1,',
          'STA1 dhcp and get 192.168.91.X ip address,',
          'Check config success.')

# res1 = res2 = 1
# sta1_ipv4 = ''

# STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1, Netcard_sta1, Network_name1, bssid=ap1mac_lower)
# 获取STA1的地址
sta1_ipresult = GetStaIp(sta1, checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
res2 = sta1_ipresult['res']

# result
printCheckStep(testname, 'Step 2', res1, res2)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2
if GetWhetherkeepon(keeponflag):
    ################################################################################
    # Step 3
    # 操作
    # 在STA1上面ping PC1。
    #
    # 预期
    # 不能ping通。PC1不能收到STA1的ping包。
    ################################################################################

    printStep(testname, 'Step 3',
              'STA1 ping pc1,',
              'ping failed.')

    res1 = 0
    # operate

    # STA1 ping PC1
    res1 = CheckPing(sta1, pc1_ipv4, mode='linux')

    # check
    res1 = 0 if 0 != res1 else 1

    # result
    printCheckStep(testname, 'Step 3', res1)

################################################################################
# Step 4
# 操作
# 在ac1的network1下取消上行方向的acl绑定，并下发配置。
# 等待sta1关联test1后，在STA1上面ping PC1
#
# 预期
# 可以ping通，PC1能收到STA1的ping包
################################################################################
printStep(testname, 'Step 4',
          'Delete qos configuration on network1 up stream,',
          'pc1 ping STA1 succeed.')

# res1 = res2 = 1
# operate
# STA1 解关联
WpaDisconnectWirelessNetwork(sta1, Netcard_sta1)

# network1下取消上行方向的acl绑定
EnterNetworkMode(switch1, '1')
SetCmd(switch1, 'no client-qos access-control up')

# 配置下发
WirelessApplyProfileWithCheck(switch1, ['1'], [ap1mac])
# STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1, Netcard_sta1, Network_name1, bssid=ap1mac_lower)

# check
res2 = CheckPing(sta1, pc1_ipv4, mode='linux')

# result
printCheckStep(testname, 'Step 4', res1, res2)

################################################################################
# Step 5
# 操作
# 在AC1上将ACL 101绑定到network 1的下行方向
# STA1关联到网络test1
#
# 预期
# Show wireless network 1 能看到：
# Client QoS Mode............Enable
# Client QoS Access Control Down................... IP - 101
# STA1关联成功，获取192.168.91.X网段的IP地址
################################################################################
printStep(testname, 'Step 5',
          'Bind ACL 101 to network 1 down stream,',
          'STA1 connect to test1')

# res1 = res2 = 1
# sta1_ipv4 = ''
# operate

# STA1 解关联
WpaDisconnectWirelessNetwork(sta1, Netcard_sta1)

EnterNetworkMode(switch1, '1')
# 将ACL 101绑定到network 1下行方向
SetCmd(switch1, 'client-qos access-control down ip 101')

# 配置下发
WirelessApplyProfileWithCheck(switch1, ['1'], [ap1mac])
# STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1, Netcard_sta1, Network_name1, bssid=ap1mac_lower)

# 获取STA1的地址
sta1_ipresult = GetStaIp(sta1, checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
res2 = sta1_ipresult['res']

# result
printCheckStep(testname, 'Step 5', res1, res2)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2
if GetWhetherkeepon(keeponflag):
    ################################################################################
    # Step 6
    # 操作
    # 在PC1上ping STA1
    #
    # 预期
    # 不能ping通,STA1不能收到PC1的ping包
    ################################################################################
    printStep(testname, 'Step 6',
              'PC1 ping STA1 failed')

    res1 = 0
    # operate

    # STA1 ping PC1
    res1 = CheckPing(pc1, sta1_ipv4, mode='linux', srcip=pc1_ipv4)

    # check
    res1 = 0 if 0 != res1 else 1

    # result
    printCheckStep(testname, 'Step 6', res1)

################################################################################
# Step 7
# 操作
# 在ac1的network1下取消下行方向的acl绑定，并下发配置。
# 等待sta1关联test1后，在pc1上面ping STA1
#
# 预期
# 可以ping通，PC1能收到STA1的ping包
################################################################################
printStep(testname, 'Step 7',
          'Delete qos configuration on network1 down stream,',
          'pc1 ping STA1 succeed.')

# res1 = res2 = res3 = 1
sta1_ipv4 = ''
# operate

# STA1 解关联
WpaDisconnectWirelessNetwork(sta1, Netcard_sta1)

# network1下取消下行方向的acl绑定
EnterNetworkMode(switch1, '1')
SetCmd(switch1, 'no client-qos access-control down')

# 配置下发
WirelessApplyProfileWithCheck(switch1, ['1'], [ap1mac])
# STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1, Netcard_sta1, Network_name1, bssid=ap1mac_lower)

# 获取STA1的地址
sta1_ipresult = GetStaIp(sta1, checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
res2 = sta1_ipresult['res']

# check
res3 = CheckPing(pc1, sta1_ipv4, mode='linux', srcip=pc1_ipv4)

# result
printCheckStep(testname, 'Step 7', res1, res2, res3)

################################################################################
# Step 8
# 操作
# 关闭network 1的Client QoS。配置下发到AP1。
##Wireless
##Network 1
##No client-qos enable
##Exit
##Exit
##Exit
##Wireless ap profile apply 1
#
# 预期
# 配置下发成功
################################################################################
printStep(testname, 'Step 8',
          'close client-qos of network 1',
          'apply ap profile 1 to ap',
          'Check config success.')

# res1 = 1
# operate
EnterNetworkMode(switch1, '1')
SetCmd(switch1, 'no', 'client-qos enable')

# 配置下发
WirelessApplyProfileWithCheck(switch1, ['1'], [ap1mac])
data1 = SetCmd(switch1, 'show wireless network', '1')

# check
res1 = CheckLine(data1, 'Client QoS Mode', 'Disable', IC=True)

# result
printCheckStep(testname, 'Step 8', res1)

################################################################################
# Step 9
# 操作
# 在STA1上面ping PC1。
#
# 预期
# 可以ping通
################################################################################
printStep(testname, 'Step 9',
          'STA1 ping pc1,',
          'ping success.')

# res1 = 1
# operate
# STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1, Netcard_sta1, Network_name1, bssid=ap1mac_lower)
# 获取STA1的地址
sta1_ipresult = GetStaIp(sta1, checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']

res2 = CheckPing(sta1, pc1_ipv4, mode='linux')
# for i in range(5):
# res1 = CheckPing(sta1,pc1_ipv4,mode='linux')
# if res1 ==0:
# break
# IdleAfter(5)

# result
printCheckStep(testname, 'Step 9', res1, res2)

################################################################################
# Step 10
# 操作
# 在PC1上面ping STA1。
#
# 预期
# 可以ping通。
################################################################################
printStep(testname, 'Step 10',
          'pc ping STA1,',
          'ping success.')

res1 = 1
# operate

# check
res1 = CheckPing(pc1, sta1_ipv4, mode='linux', srcip=pc1_ipv4)

# result

printCheckStep(testname, 'Step 10', res1)

################################################################################
# Step 11
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 11',
          'Recover initial config for switches.')

# operate

# 解关联
WpaDisconnectWirelessNetwork(sta1, Netcard_sta1)

##删除qos配置

EnterWirelessMode(switch1)
SetCmd(switch1, 'no ap client-qos')
EnterNetworkMode(switch1, '1')
SetCmd(switch1, 'no client-qos access-control up')
SetCmd(switch1, 'no client-qos access-control down')
SetCmd(switch1, 'vlan ' + Vlan4091)

# 清除 acl 100,101
EnterConfigMode(switch1)
SetCmd(switch1, 'no access-list 100')
SetCmd(switch1, 'no access-list 101')

# 配置下发
WirelessApplyProfileWithCheck(switch1, ['1'], [ap1mac])
# end
printTimer(testname, 'End')
