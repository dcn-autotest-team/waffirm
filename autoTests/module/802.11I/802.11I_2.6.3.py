#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# 802.11I_2.6.3.py
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2020 Digital China Networks Co. Ltd
#
# Features:
# 2.6.3  非漫游关联成功后的处理:关联成功后,client和VAP对应关系正确
# 测试描述：在关联AP的管理UWS上查看VAP-Client Mapping表，该client和VAP的对应关系正确
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.2.7
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 802.11I_2.6.3'
avoiderror(testname)
printTimer(testname,'Start','Test VAP-Client Mapping')

################################################################################
#Step 1
#操作
#配置AC1的network1的安全接入方式为WPA-Personal，密码为abcd1234。
#Wireless
#Network 1
#Security mode wpa-personal
#Wpa key abcd1234
#Wpa versions wpa
#Exit
#配置成功。在AC1上面Show wireless network 1可以看到相关的配置。
################################################################################
printStep(testname,'Step 1',\
          'set network security mode wep-personal mode,',\
          'set wpa versions wpa.',\
          'show wireless network 1 and config success.')
#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'security mode wpa-personal')
SetCmd(switch1,'wpa key abcd1234')
SetCmd(switch1,'wpa versions wpa')
SetCmd(switch1,'wpa ciphers CCMP')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#check
data1 = SetCmd(switch1,'show wireless network 1')
res1 = CheckLine(data1,'Security Mode','WPA Personal')
res2 = CheckLine(data1,'WPA Versions','WPA')
res3 = CheckLine(data1,'WPA Versions','WPA2')
res4 = CheckLine(data1,'WPA Ciphers','CCMP')

printCheckStep(testname, 'Step 1',res1,res2,not res3,res4)

################################################################################
#Step 2
#操作
#设置STA1无线网卡的属性为WPA-PSK认证，正确输入密码，关联网络test1。
#预期
#成功关联，并获取192.168.91.X网段的IP地址。Show wireless client summery
#可以看到STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
################################################################################
printStep(testname,'Step 2',\
          'STA1 connect to network 1,',\
          'connect success.')
res1=1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='custom',
                                key_mgmt='WPA-PSK',proto='WPA', pairwise='CCMP',group='CCMP', psk='abcd1234',
                                checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)

printCheckStep(testname, 'Step 2',res1)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 3
    #操作
    #在AC上查看VAP-Client Mapping表项
    #sho wireless client status vap ap1_vap0_mac
    #预期
    #表项中存在sta1mac
    ################################################################################

    printStep(testname,'Step 3',\
              'show wireless client status vap ap1_vap0_mac on AC1',
              'sta1 is in list')

    res1 = CheckSutCmd(switch1,'show wireless client status vap '+ap1vapmac,
                        check=[(ap1vapmac,ap1mac,sta1mac)],retry=10,waitflag=False)

    printCheckStep(testname, 'Step 3',res1)

################################################################################
#Step 4
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 4',\
          'Recover initial config for switches.')

#operate
# sta1解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
CheckWirelessClientOnline(switch1,sta1mac,'offline',retry=20)

# 恢复network1配置
ClearNetworkConfig(switch1,1)
EnterNetworkMode(switch1,1)
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan ' + Vlan4091)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

#end
printTimer(testname, 'End')