#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# Software : PyCharm
#
# performance_3.5.1.py.py - 
#
# Author    :zhangjxp(zhangjxp@digitalchina.com)
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd 
#
## Features:
# 3.5.1  依次将AP的radio 1,radio 2(或者radio 3)设置为不同的信道，检查sta是否能正常关联
# *********************************************************************
# Change log:
#       - 2018/3/26 15:21  add by zhangjxp
#
# *********************************************************************

from itertools import zip_longest

# individualflag参数用于判断脚本执行入口，在performance_main.py文件中将会用到
individualflag = True

# multirunflag参数用于判断脚本执行入口，定义在performance_main.py文件中，如果不存在multirunflag参数，说明执行入口为当前文件
if 'multirunflag' not in vars():
    exec(compile(open('performance_main.py', "rb").read(), 'performance_main.py', 'exec'))

testname = 'Performance_test 3.5.1'
printTimer(testname, 'Start',
           'change ap channel, and check whether sta connect network successfully')

# parameters
ap1mac_radio1 = ap1mac_type1
ap1mac_radio2 = incrmac(ap1mac_radio1,16).lower()
ap1mac_radio3 = incrmac(ap1mac_radio2,16).lower()
# function
def get_ap_support_channel(switch,profile,radio):
    channel_list = []
    _data = SetCmd(switch,'show wireless ap profile',profile,'radio',radio,'auto-eligible')
    _temp_str = re.search('Supported Channels.*?\d+.*?$',_data,re.DOTALL)
    if _temp_str:
        _temp_str = _temp_str.group()
        _temp_list = re.findall('\s\d+\**\s',_temp_str)
        for _channel in _temp_list:
            _channel = _channel.strip().rstrip('*')
            channel_list.append(_channel)
    return channel_list
    
################################################################################
# step1
# AP在AC上线,判断AP的radio数量n
# 配置n个network,各network的ssid不一致(规避5G优先问题)
# 配置profile,对AP的各radio配置不同的network
################################################################################
printStep(testname, 'Step 1',
          'count ap radio number',
          'config network and profile')

# operate
# 配置network
EnterNetworkMode(switch1,101)
SetCmd(switch1, 'ssid ssid_radio_1')
SetCmd(switch1,'vlan ' + Vlan4091)
# 配置profile
EnterApProMode(switch1,100)
SetCmd(switch1,'hwtype',hwtype1)
SetCmd(switch1,'radio 1')
SetCmd(switch1,'vap 0')
SetCmd(switch1,'enable')
SetCmd(switch1,'network 101')
channel_radio1_list = get_ap_support_channel(switch1,100,1)
# 判断AP是否有radio 2,radio 3
EnterApProMode(switch1,100)
data = SetCmd(switch1, 'show run c')
radio2_flag = CheckLine(data, 'radio\s+2', IC=True)
radio3_flag = CheckLine(data, 'radio\s+3', IC=True)
if radio2_flag == 0:
    EnterNetworkMode(switch1,102)
    SetCmd(switch1, 'ssid ssid_radio_2')
    SetCmd(switch1,'vlan ' + Vlan4091)
    EnterApProMode(switch1,100)
    SetCmd(switch1,'radio 2')
    SetCmd(switch1,'vap 0')
    SetCmd(switch1,'enable')
    SetCmd(switch1,'network 102')
    channel_radio2_list = get_ap_support_channel(switch1,100,2)
else:
    channel_radio2_list = []

if radio3_flag == 0:
    EnterNetworkMode(switch1,103)
    SetCmd(switch1, 'ssid ssid_radio_3')
    SetCmd(switch1,'vlan ' + Vlan4091)
    EnterApProMode(switch1,100)
    SetCmd(switch1,'radio 3')
    SetCmd(switch1,'vap 0')
    SetCmd(switch1,'enable')
    SetCmd(switch1,'network 103')
    channel_radio3_list = get_ap_support_channel(switch1,100,3)
else:
    channel_radio3_list = []
    
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'profile 100')  
  
channel_list = zip_longest(channel_radio1_list, channel_radio2_list, channel_radio3_list)

# result
printCheckStep(testname,'Step 1',0)
################################################################################
# step2
# 在AC1上循环修改AP各radio信道，重启AP
# 检查AP信道修改成功后，sta关联AP
################################################################################
printStep(testname, 'Step 2',
          'change ap channel and reboot ap',
          'check ap channel change successfully',
          'sta connect to ap')
          
# operate
change_channel_faillist = []
sta_connect_faillist = []
# 修改AP信道并重启AP，检查信道是否修改成功
for (radio1_channel,radio2_channel,radio3_channel) in channel_list:
    res1=res2=res3=0
    # 总共尝试修改信道2次，2次都失败后会报错
    for i in range(2):
        if radio1_channel:
            EnterWirelessMode(switch1)
            SetCmd(switch1,'ap database',ap1mac)
            SetCmd(switch1,'radio 1 channel',radio1_channel)
        if radio2_channel:
            EnterWirelessMode(switch1)
            SetCmd(switch1,'ap database',ap1mac)
            SetCmd(switch1,'radio 2 channel',radio2_channel)   
        if radio3_channel:
            EnterWirelessMode(switch1)
            SetCmd(switch1,'ap database',ap1mac)
            SetCmd(switch1,'radio 3 channel',radio3_channel)
        RebootAp('AC',AC=switch1,MAC=ap1mac,AP=ap1,connectTime=50)
        CheckSutCmd(switch1,'show wireless ap status',
                    check=[(ap1mac,'Managed','Success')],
                    retry=20,interval=5,waitflag=False,IC=True)
        for i in range(5):
            IdleAfter(5)
            data = SetCmd(switch1,'show wireless ap ', ap1mac ,' radio status')
            res1 = CheckLine(data,'\s1\s+'+radio1_channel)
            if radio2_channel:
                res2 = CheckLine(data,'\s2\s+'+radio2_channel)
            if radio3_channel:
                res3 = CheckLine(data,'\s3\s+'+radio3_channel)
            if res1==0 and res2==0 and res3==0:
                break
        if res1==0 and res2==0 and res3==0:
            break
    else:
        # AP信道修改失败后的报错信息 
        notice1 = 'change ap channel failed!!!!!!it should be changed to: radio1:'+radio1_channel
        if radio2_channel:
            notice1 = '%s%s%s' % (notice1,';radio2:',radio2_channel)
        if radio3_channel:
            notice1 = '%s%s%s' % (notice1,';radio3:',radio3_channel)
        notice1 = '%s\n%s\n%s\n%s\n%s' % ('#'*20,notice1,'but infact the channel is:',data,'#'*20)
        print(notice1)
        change_channel_faillist.append(notice1)
        printCheckStep(testname,'Step 2', res1)
    # 信道修改成功后，sta关联AP
    if res1 == 0:
        temp_list = []
        if radio1_channel:
            temp_list.append(('ssid_radio_1',ap1mac_radio1,radio1_channel))
        if radio2_channel:
            temp_list.append(('ssid_radio_2',ap1mac_radio2,radio2_channel))
        if radio3_channel:
            temp_list.append(('ssid_radio_3',ap1mac_radio3,radio3_channel))
        for (ssid,mac,channel) in temp_list:
            notice2 = ''
            resa = resb = 1
            resa = WpaConnectWirelessNetwork(sta1,Netcard_sta1,ssid,checkDhcpAddress=Netcard_ipaddress_check,bssid=mac)
            if resa == 0:
                resb = CheckPing(sta1,pc1_ipv4,mode='linux')
                if resb != 0:
                    notice2 = 'sta connect to %s successfully, but ping pc1 failed, the channel is %s' % (ssid, channel)
            else:
                notice2 = 'sta connect to %s failed, the channel is %s' % (ssid, channel)
            if resa!=0 or resb!=0:
                print(notice2)  
                sta_connect_faillist.append(notice2)
            printCheckStep(testname,'Step 2', resa ,resb)
print(change_channel_faillist)
print(sta_connect_faillist)
################################################################################
# Step 3
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 3',
          'Recover initial config')

# operate
WpaDisconnectWirelessNetwork(sta1, Netcard_sta1)
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'profile 1')  
SetCmd(switch1,'radio 1 channel 0')
SetCmd(switch1,'radio 2 channel 0')
SetCmd(switch1,'radio 3 channel 0')
EnterWirelessMode(switch1)
SetCmd(switch1,'no ap profile 100')
SetCmd(switch1,'no network 101')
SetCmd(switch1,'no network 102')
SetCmd(switch1,'no network 103')

RebootAp('AC',AC=switch1,MAC=ap1mac,AP=ap1,connectTime=50)
CheckSutCmd(switch1,'show wireless ap status',
            check=[(ap1mac,'Managed','Success')],
            retry=20,interval=5,waitflag=False,IC=True)
# end
printTimer(testname, 'End')
        
                
                
        
    