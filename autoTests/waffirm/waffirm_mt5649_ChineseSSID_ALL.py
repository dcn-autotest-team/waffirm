# -*- coding: UTF-8 -*-#
#
# *******************************************************************************
# waffirm_mt5649_ChineseSSID.py
#
# Author:  (zhangjxp)
#
# Version 1.0.0
#
# Date:  2017-4-28 9:54:28
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# mt5705  中文SSID测试
# 测试目的：当SSID设置成中文时，用户可以关联成功
# 测试环境：同测试拓扑
# 1.配置SSID为中文，用户可以关联成功。
# 2.AC重启后，配置的中文SSID不丢失,用户可以关联成功。
# 3.恢复默认配置
#
# *******************************************************************************
# Change log:
#     - creadte by zhangjxp 2017.4.28
# *******************************************************************************
# Package
# Global Definition

# Source files

# Procedure Definition

# Functional Code

testname = 'TestCase mt5649_ChineseSSID'
avoiderror(testname)
printTimer(testname, 'Start')


# 此函数仅适用于本用例，适配中文ssid
def WpaConnectWirelessNetworknew(sta, netcardName, ssid, connectType='open', dhcpFlag=True, **args):
    if ('' == sta) or ('' == netcardName) or ('' == ssid):
        printRes('Error: parameter input error')
        return 1
    res = 1
    CONFIGFLAG = 0
    # 清空IP
    SetCmd(sta, 'dhclient -r ' + netcardName)
    IdleAfter('2')
    # 启用网卡
    SetCmd(sta, 'ifconfig ' + netcardName + ' up')
    IdleAfter('2')
    #
    SetCmd(sta, 'dmesg -c | grep ppppppppppp')
    SetCmd(sta, 'wpa_cli -i ' + netcardName + ' remove_network 0')
    SetCmd(sta, 'wpa_cli -i ' + netcardName + ' add_network 0')
    SetCmd(sta, 'wpa_cli -i ' + netcardName + ' set_network 0 ssid ' + '\'"' + ssid + '"\'')
    if 'bssid' in args:
        SetCmd(sta, 'wpa_cli -i ' + netcardName + ' set_network 0 bssid ' + args['bssid'])

    if connectType.lower() == 'open':
        SetCmd(sta, 'wpa_cli -i ' + netcardName + ' set_network 0 key_mgmt NONE')

    if CONFIGFLAG == 0:
        SetCmd(sta, 'wpa_cli -i ' + netcardName + ' enable_network 0')

        # sta 关联 ap
        i_time = 1
        interval = 5
        while i_time < 16:
            data = SetCmd(sta, 'wpa_cli -i ' + netcardName + ' status')
            if 0 == CheckLineList(data, [('wpa_state', 'COMPLETED')], IC=True):
                printRes('Connect to AP succeed in ' + str(interval * (i_time - 1)) + ' sec')
                res = 0
                break
            else:
                i_time = i_time + 1
            if 15 == i_time:
                printRes('Failed: connet to ' + ssid + ' failed in ' + str(interval * i_time) + ' sec')
                try:
                    res = 2
                    # SetCmd(sta,'dhclient -r '+ netcardName)
                    # SetCmd(sta,'wpa_cli -i ' + netcardName + ' disable_network 0')
                    # SetCmd(sta,'wpa_cli -i ' + netcardName + ' remove_network 0')
                    SetCmd(sta, 'iwlist ' + netcardName + ' scan | grep ' + ssid)
                    SetCmd('ap1', 'admin')
                    SetCmd('ap1', 'admin')
                    SetCmd('ap1', 'iwconfig')

                    SetCmd('ap1', 'brctl show')

                    SetCmd('s1', 'show wireless ap status')
                    SetCmd('s1', 'show wireless ap fail status')
                    SetCmd('s1', 'show wireless client status')
                    SetCmd(sta, 'dmesg -c')
                    tempRe1 = SetCmd('ap1', 'iwconfig ' + ath)
                    if re.search('Bit Rate:0 kb', tempRe1) is not None:
                        res = 3
                except Exception:
                    print 'DEBUG ERROR'
                return 1
            IdleAfter(interval)

        # sta 网卡 dhcp 获取地址
        if dhcpFlag:
            SetCmd(sta, 'dhclient ' + netcardName)
            IdleAfter(2)
            i_time = 1
            if 'checkDhcpAddress' in args:
                tempNetworkIpRe = re.search('\d+\.\d+\.\d+\.', args['checkDhcpAddress'])
                tempNetworkIp = tempNetworkIpRe.group(0)
            while i_time < 4:
                data = SetCmd(sta, 'ifconfig -v ' + netcardName)
                if re.search('inet.*?((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)', data,
                             re.I) is not None:
                    if 'checkDhcpAddress' in args:
                        if re.search('inet.*?' + tempNetworkIp, data, re.I) is None:
                            printRes('Obatin ip via dhcp succeed but not match')
                            return 4
                    res = 0
                    printRes('Obatin ip via dhcp succeed')
                    break
                i_time = i_time + 1
                IdleAfter(10)
                if 3 == i_time:
                    printRes('Failed: Obtain ip via dhcp failed')
                    try:
                        SetCmd(sta, 'iwlist ' + netcardName + ' scan | grep ' + ssid)
                        SetCmd('ap1', 'admin')
                        SetCmd('ap1', 'admin')
                        SetCmd('ap1', 'iwconfig')
                        tempRe2 = SetCmd('ap1', 'brctl show')
                        if re.search(ath + '\.4091', tempRe2) is None:
                            if res == 0:
                                res = 5
                        SetCmd('s1', 'show wireless ap status')
                        SetCmd('s1', 'show wireless ap fail status')
                        SetCmd('s1', 'show wireless client status')
                    except Exception:
                        print 'DEBUG ERROR'
                    return 1

    return res


# 2.4G、5G差异化配置,test24gflag为True代表执行2.4G脚本，False代表执行5G脚本
if test24gflag:
    ath = 'ath0'
else:
    ath = 'ath16'
################################################################################
# Step 1
#
# 操作
# 配置AC1的network1的SSID为10个字中文”神州数码网络云科信息”。
#
# 预期
# 配置成功。在AC1上面Show wireless network 1可以看到相关的配置。
#
################################################################################
printStep(testname, 'Step 1',
          'Config Chinese ssid \'神州数码网络云科信息\'in network1')
res1 = 1
# operate
# AC1配置
EnterConfigMode(switch1)
SetCmd(switch1, 'ucs enable')
SetCmd(switch1, 'wireless')
SetCmd(switch1, 'network 1')
ssid1 = u'神州数码网络云科信息'
ssid2 = ssid1.encode('utf-8')
data = Receiver(switch1, 'ssid ' + ssid2)
data = Receiver(switch1, 'show run c', timeout=3)
res1 = CheckLine(data,
                 'network 1',
                 'ssid ' + ssid2,
                 ML=True)

# result
printCheckStep(testname, 'Step 1', res1)
################################################################################
# Step 2
# 操作
# 将配置下发到AP1
#
# 预期
# 配置下发成功
################################################################################
printStep(testname, 'Step 2',
          'Apply ap profile 1')

# operate
res1 = WirelessApplyProfileWithCheck(switch1, ['1'], [ap1mac])

# result
printCheckStep(testname, 'Step 2', res1)

################################################################################
# Step 3
# 操作
# STA1接入这个中文SSID。	
#
# #预期
# 成功关联，并获取192.168.91.X网段的IP地址。Show wireless client summery可以看到
# STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
################################################################################
printStep(testname, 'Step 3',
          'STA1 connect to test1')

res1 = 1
res2 = 1
res3 = 1
# operate
res1 = WpaConnectWirelessNetworknew(sta1, Netcard_sta1, '神州数码网络云科信息', checkDhcpAddress=Netcard_ipaddress_check,
                                    bssid=ap1mac_lower)
IdleAfter(10)
# check
res2 = CheckWirelessClientOnline(switch1, sta1mac, 'online')
res3 = CheckPing(sta1, pc1_ipv4, mode='linux', pingPara=' -c 10')
# result
printCheckStep(testname, 'Step 3', res1, res2, res3)

################################################################################
# Step 4
# 保存AC配置，重启AC.AC重启后，在AC1上面Show wireless network 1可以看到AC重启后配置没有丢失。
################################################################################
printStep(testname, 'Step 4',
          'Write and reload AC1',
          'The Chinese ssid configuration is not lost')
res1 = 1
# operate
EnterEnableMode(switch1)
Receiver(switch1, 'write', timeout=1)
IdleAfter(1)
Receiver(switch1, 'y')
IdleAfter(5)
# ReloadMultiSwitch([switch1])
reload_multi_switch([switch1])
EnterWirelessMode(switch1)
SetCmd(switch1, 'network 1')
data = Receiver(switch1, 'show run c', timeout=3)
res1 = CheckLine(data,
                 'network 1',
                 'ssid ' + ssid2,
                 ML=True)
# res1=CheckLine(data, \
# 'network 1', \
# 'ssid 神州数码网络云科信息', \
# ML = True)
# result
printCheckStep(testname, 'Step 4', res1)
################################################################################
# Step 5
# 操作
# AP被管理后，STA1接入这个中文SSID。
# 预期	
# 成功关联，并获取192.168.91.X网段的IP地址。
# Show wireless client summery可以看到STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
################################################################################
printStep(testname, 'Step 5',
          'STA1 connect to test1')

res1 = 1
res2 = 1
res3 = 1
# operate
i = 1
while i < 30:
    EnterEnableMode(switch1)
    data1 = SetCmd(switch1, 'show wireless ap status')
    res = CheckLine(data1, ap1mac, Ap1_ipv4, '1', 'Managed', 'Success', IC=True)
    if res == 0:
        break
    IdleAfter('5')
    i = i + 1

res1 = WpaConnectWirelessNetworknew(sta1, Netcard_sta1, '神州数码网络云科信息', checkDhcpAddress=Netcard_ipaddress_check,
                                    bssid=ap1mac_lower)
IdleAfter(10)
# check
res2 = CheckWirelessClientOnline(switch1, sta1mac, 'online')
res3 = CheckPing(sta1, pc1_ipv4, mode='linux', pingPara=' -c 10')
# result
printCheckStep(testname, 'Step 5', res1, res2, res3)
################################################################################
# Step 6
#
# 操作
# 配置AC1的network1的SSID为11个字中文”神州数码网络云科信息技”。
#
# 预期
# 配置失败，提示错误信息
#
################################################################################
printStep(testname, 'Step 6',
          'AC can not config Chinese ssid with 11 character')
res1 = 1
# operate
# AC1配置
EnterConfigMode(switch1)
SetCmd(switch1, 'wireless')
SetCmd(switch1, 'network 1')
ssid1 = u'神州数码网络云科信息技'
ssid2 = ssid1.encode('gbk')
data = Receiver(switch1, 'ssid ' + ssid2, timeout=3)
res1 = CheckLine(data, 'Invalid')
# result
printCheckStep(testname, 'Step 6', res1)
################################################################################
# Step 7
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 7',
          'Recover initial config')

# operate
# AC1恢复
EnterConfigMode(switch1)
SetCmd(switch1, 'wireless')
SetCmd(switch1, 'network 1')
SetCmd(switch1, 'ssid ' + Network_name1)
EnterEnableMode(switch1)
WirelessApplyProfileWithCheck(switch1, ['1'], [ap1mac])
EnterConfigMode(switch1)
SetCmd(switch1, 'ucs disable')

# end
printTimer(testname, 'End')
