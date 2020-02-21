#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_5.6.py - test case 5.6 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 5.6	AP指示灯测试
# 测试目的：Client QoS基本功能测试-限速
# 测试环境：同测试拓扑
# 测试描述：测试AP上面能够通过bandwidth limit对每个无线用户的的带宽限制，
#           可以分别对上行和下行的流量进行限制。
#
#*******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
#*******************************************************************************

#Package
import wx
s1vlanmac = GetVlanMac(switch1)

Var_bandwidth_limit_500 = '20000'
Var_bandwidth_limit_700 = '3008'

testname = 'TestCase 5.6'
avoiderror(testname)
printTimer(testname,'Start','AP LED light test')

################################################################################
#Step 1
#操作
#在UWS1配置network1的SSID为test1，关联vlan4092
#
#预期
#配置成功。
################################################################################
printStep(testname,'Step 1',
          'set network 1 ssid test1 and vlan 4092,',
          'config success.')
          
res1=res2=1
#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap client-qos')
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'ssid ' + Network_name1)
SetCmd(switch1,'vlan '+ Vlan4092)

data1 = SetCmd(switch1,'show wireless network','1')

#check
res1 = CheckLine(data1,'Default VLAN',Vlan4092,IC=True)
res2 = CheckLine(data1,'SSID',Network_name1,IC=True)

#result
printCheckStep(testname, 'Step 1',res1,res2)

################################################################################
#Step 2
#操作
#开启network1的Client Qos功能，并且设置下行带宽为20000kbps。配置下发到AP1。
#
#预期
#配置成功。
################################################################################
printStep(testname,'Step 2',
          'enable client-qos and set down speed 20000kbps,',
          'Check config success.')
          
res1=1
#operate
EnterNetworkMode(switch1,'1')
SetCmd(switch1,'client-qos enable')
SetCmd(switch1,'client-qos bandwidth-limit down',Var_bandwidth_limit_500)
res1 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')
# IdleAfter(Ac_ap_syn_time)      
EnterEnableMode(switch1)
# data1 = SetCmd(switch1,'show wireless network','1')
# data2 = SetCmd(switch1,'show wireless ap status')

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
printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#STA1连接网络test1，在STA1上启动ixchariot向PC1发包，速率为1Mbps。
#
#预期
#上行转发速率为448kbps（5%偏差）
################################################################################
printStep(testname,'Step 3',
          '2.4G LED test.')

res1=res2=res3=1
sta1_ipv4 = ''

wx.MessageBox(u'按下按钮后的一分钟内请观察2.4G指示灯与LAN灯是否间歇性快速闪烁，\n之后的一分钟5G指示灯与LAN灯是否间歇性快速闪烁')

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
    sta1_ipv4 = '7.7.7.7'
    printRes('Failed: Get ipv4 address of STA1 failed') 
  
#清除AC1上端口s1p1的数据信息

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
for itemp in xrange(10):
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
    IdleAfter(5)
    
#result
printCheckStep(testname, 'Step 3',0)

################################################################################
#Step 4
#操作
#STA1连接网络test1，在STA1上启动ixchariot向PC1发包，速率1Mbps。
#
#预期
#上行转发速率为640kbps。
################################################################################
printStep(testname,'Step 4',
          '5G LED testing.')

res1=1

#operate

#清除AC1上端口s1p1的数据信息
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
mac5g = incrmac(ap1mac_lower,step=16)
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=mac5g) 

data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)
if None != SearchResult1:
    sta1_ipv4 = SearchResult1.group(1)
    if None != re.search(Dhcp_pool2,sta1_ipv4):
        printRes('STA1 ip address: ' + sta1_ipv4)
        res2 = 0  
else:
    res2 = 1
    sta1_ipv4 = '7.7.7.7'
    printRes('Failed: Get ipv4 address of STA1 failed') 

for itemp in xrange(10):
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
    IdleAfter(5)
    
dlg = wx.MessageDialog(wx.FindWindowById(10), '2.4G and 5G LED work well?',
                               'Affirm',
                               wx.ICON_INFORMATION | wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION
                               )
if dlg.ShowModal() == wx.ID_YES:
    wx.MessageBox(u'已经通过LED指示灯测试和基本拓扑检查，你可以离开让脚本自动运行了')
    res7 = 0
else:
    wx.MessageBox(u'如果没有看见指示灯快速闪烁请检查sta1刚才的下载过程是否正常\n如果下载未进行请检查环境，如果下载进行了但速度未超过500KBps,请察看是否有环境干扰')
    res7 = 1

dlg.Destroy()


#result
printCheckStep(testname, 'Step 4',res7)

################################################################################
#Step 5
#操作
#关闭Client Qos功能。
#
#预期
#配置成功。
################################################################################
printStep(testname,'Step 5',
          'close client-qos,',
          'Check config success.')

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
printCheckStep(testname, 'Step 5',res1)

################################################################################
#Step 6
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 6',
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
SetCmd(switch1,'no','client-qos bandwidth-limit up')
SetCmd(switch1,'no','client-qos bandwidth-limit down')
SetCmd(switch1,'vlan ' + Vlan4091)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,'1')
# IdleAfter(Ac_ap_syn_time) 

#end
printTimer(testname, 'End')