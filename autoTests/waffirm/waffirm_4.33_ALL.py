#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
#  waffirm_4.33_ALL.py - test case 4.33 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
# 
# Date 2017-12-04 14:37:33
#
# Features:
# 4.33 终端指纹识别功能测试（5GHz覆盖）
# 测试目的：测试终端指纹识别基本功能。 
# 测试描述：测试在配置dhcp-option 55的指纹识别信息后，是否能正确识别终端，在指纹识别信息绑定acl策略后，策略是否生效。
# 测试环境：见测试拓扑。
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.04
#*******************************************************************************

#Package

#Global Definition
 
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.33'
avoiderror(testname)
printTimer(testname,'Start','test dhcp-option 55 device-finger ')

################################################################################
#Step 1
#操作
# 在network1下开启指纹识别功能。
# AC1(config-network)#device-finger enable
#预期
# 在AC1上show wireless network 1查看device-finger function为Enable
################################################################################
printStep(testname,'Step 1',\
          'Enable device-finger function in network 1')

res1=1
#operate
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'device-finger enable')
#check
EnterEnableMode(switch1)
data = SetCmd(switch1,'show wireless network 1')
res1 = CheckLine(data,'device-finger function','Enable')

#result
printCheckStep(testname, 'Step 1', res1)
################################################################################
#Step 2
#操作
# STA1关联到AP1上
#
#预期
# STA1成功关联到AP1，并获取192.168.91.X网段的IP地址。Show wireless client summery
# 可以看到STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
# 在AC1上show wireless client device-type显示STA1的os被识别为为other。
################################################################################
printStep(testname,'Step 2',\
          'STA1 connect to test1')

res1=res2=1
#operate
#check
EnterWirelessMode(switch1)
SetCmd(switch1,'device-finger dhcp-option 55 starts-with 370d011c02790f device-description TPLINK')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='open',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
data = SetCmd(switch1,'show wireless client device-type')
res2 = CheckLine(data,sta1mac,'other')
#result
printCheckStep(testname, 'Step 2',res1,res2)

################################################################################
#Step 3
#操作
# 在AC1上配置指纹识别的acl策略。
# access-list 100 permit ip any-source any-destination
# 把acl策略绑定到步骤2的终端识别表中。
# AC1(config-wireless)#ap client-qos
# AC1(config-wireless)#network 1
# AC1(config-wireless)#client-qos enable
# AC1(config-wireless)#device-finger-policy os other
# AC1(config-device-finger-policy)#access-control up ip 100
# 下发配置到AP1，终端STA1关联test1。
# AC1#wireless ap profile apply 1
#预期
# STA1成功关联到AP1，并获取192.168.91.X网段的IP地址。
# Show wireless client summery可以看到STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
################################################################################

printStep(testname,'Step 3',\
          'Cinfig access-list 100 deny ip any-source any-destination',\
          'Bind acl to device-finger',\
          'sta connect network 1')

res1=res2=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'access-list 100 deny ip any-source any-destination')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap client-qos')
SetCmd(switch1,'device-finger-policy os other')
SetCmd(switch1,'access-control up ip 100')
EnterWirelessMode(switch1)
SetCmd(switch1,'network 1')
SetCmd(switch1,'client-qos enable')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#check
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='open',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
#result
printCheckStep(testname, 'Step 3',res1,res2)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 4
    #操作
    #在STA1上ping PC1
    #
    #预期
    #不能ping通。PC1不能收到STA1的ping包
    ################################################################################

    printStep(testname,'Step 4',\
              'STA1 ping pc1',\
              'ping failed.')

    res1 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res1 = 0 if res1 != 0 else 1

    printCheckStep(testname, 'Step 4',res1)

################################################################################
#Step 5
#操作
# 在AC1上把acl策略从步骤2的终端识别表中删除，下发配置到AP1,终端STA1关联test1。
# AC1(config-wireless)#device-finger dhcp-option 55 starts-with 370d011c02790f  device-description tplink
# AC1(config-device-finger)#no access-control up 
# AC1#wireless ap profile apply 1
#
#预期
# STA1成功关联到AP1，并获取192.168.91.X网段的IP地址。
# Show wireless client summery可以看到STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
################################################################################
printStep(testname,'Step 5',\
        'delete acl from device-finger',\
        'sta connect network 1')
res1=res2=res3=res4=res5=1
#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'device-finger-policy os other')
SetCmd(switch1,'no access-control up')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#check
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='open',checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
#result
printCheckStep(testname, 'Step 5',res1,res2)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 6
    #操作
    #在STA1上ping PC1
    #
    #预期
    #可以ping通，PC1能收到STA1的ping包
    ################################################################################

    printStep(testname,'Step 6',\
              'STA1 ping pc1',\
              'ping successfully.')

    res1 = CheckPing(sta1,pc1_ipv4,mode='linux')

    printCheckStep(testname, 'Step 6',res1)
################################################################################
#Step 7
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 7',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

EnterNetworkMode(switch1,'1')
SetCmd(switch1,'no device-finger enable')
SetCmd(switch1,'no client-qos enable')
EnterWirelessMode(switch1)
SetCmd(switch1,'no device-finger-policy os other')
SetCmd(switch1,'no ap client-qos')
SetCmd(switch1,'no device-finger dhcp-option 55 starts-with 370d011c02790f')
EnterConfigMode(switch1)
SetCmd(switch1,'no access-list 100')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# end
printTimer(testname, 'End')