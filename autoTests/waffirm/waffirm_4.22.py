#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.22.py - test case 4.22 of waffirm
#
# Author:  fuzf@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.22 SAVI功能测试
# 测试目的：AP的SAVI功能。
# 测试环境：同测试拓扑
# 测试描述：开启SAVI功能，SAVI私设IP地址无法访问网络，DHCP获取地址可以创建SAVI表项并访问网络，
#          （STA1的MAC地址：STA1MAC）
#
#*******************************************************************************
# Change log:
#     - lupingc RDM49074 2017.5.17
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.22'
avoiderror(testname)
printTimer(testname,'Start',"SAVI test")


################################################################################
#Step 1
#操作
# STA1关联test1并设置静态IP地址，ping 网关
#
#预期
#STA1关联test1成功，可以ping通网关
################################################################################
printStep(testname,'Step 1',
          'STA1 connect test1',
          'STA1 config static-ip "Dhcp_pool1+100",'
          'STA1 ping gateway succeed')

res1=res2=res3=res4=1
#operate
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)


#手动配置STA1地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'ifconfig',Netcard_sta1,Dhcp_pool1+'100','netmask','255.255.255.0')


#获取已配置地址
data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)

#检查sta1的IP地址是否等于配置的静态IP地址
if None != SearchResult1:
    if SearchResult1.group(1).strip() == Dhcp_pool1+'100':
        res2=0
    else:
        res2=1
        printRes('Check sta1 IP address failed!')

res3=CheckPing(sta1,Dhcp_pool1+'1',mode='linux')

#result
printCheckStep(testname, 'Step 1',res1,res2,res3)

################################################################################
#Step 2
#操作
# 开启SAVI功能：
# enable
# config
#    wireless
#       ap profile 1
#          savi enable
#          savi ipv6-slaac enable
#          end
# wireless ap profile apply 1
#（sta1和sta2网络地址为Dhcp_pool1+'100'，网关为Var_dhcp_pool+'1'）
#
#预期
#
#配置成功，配置下发成功
################################################################################

printStep(testname,'Step 2',
          'add savi configuration on ap profile 1,',
          'wireless ap profile apply 1 success')

res1=res2=res3=res4=1

#operate
EnterApProMode(switch1,1)
SetCmd(switch1,"savi enable")
SetCmd(switch1,"savi ipv6-slaac enable")

#下发profile 1的配置到AP1
res1 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,1)

# IdleAfter(Ac_ap_syn_time)
# for i in xrange(10):
    # IdleAfter(10)
    # data1 = SetCmd(switch1,'show wireless ap status')
    # if re.search('1\s+Managed Success',data1) is not None:
        # break

#检查配置结果
EnterEnableMode(switch1)
# data1 = SetCmd(switch1,'show wireless ap status')
data2 = SetCmd(switch1,'show running-config')

# res1 = CheckLine(data1,ap1mac,'Managed','Success',IC=True)
res2 = CheckLine(data2,"savi enable")
res3 = CheckLine(data2,"savi ipv6-slaac enable")

#result
printCheckStep(testname, 'Step 2',res1,res2,res3)


################################################################################
#Step 3
#操作
# STA1关联test1并设置静态IP地址，ping 网关
#
#预期
#STA1关联test1成功，不可以ping通网关
################################################################################
printStep(testname,'Step 3',
          'STA1 connect test1',
          'STA1 config static-ip "Dhcp_pool1+100",'
          'STA1 ping gateway failed')

res1=res2=res3=res4=1
#operate
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,dhcpFlag=False,bssid=ap1mac_lower)


#手动配置STA1地址
SetCmd(sta1,'\x03')
SetCmd(sta1,'ifconfig',Netcard_sta1,Dhcp_pool1+'100','netmask','255.255.255.0')


#获取已配置地址
data1 = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data1,re.I)

#检查sta1的IP地址是否等于配置的静态IP地址
if None != SearchResult1:
    if SearchResult1.group(1).strip() == Dhcp_pool1+'100':
        res2=0
    else:
        res2=1
        printRes('Check sta1 IP address failed!')

res3=CheckPing(sta1,Dhcp_pool1+'1',mode='linux')
res3=0 if 0!=res3 else 1

#result
printCheckStep(testname, 'Step 3',res1,res2,res3)


################################################################################
#Step 4
#操作
#在AC1配置对应STA1的SAVI绑定，STA1 ping 网关
#
#预期
#能够 ping 通
################################################################################

printStep(testname,'Step 4',
          'config static savi bingding for sta1 on AC1',
          'sta1 ping gateway success')

res1=res2=1

#operate   
EnterWirelessMode(switch1)
SetCmd(switch1,"savi binding",sta1mac,"ipv4",Dhcp_pool1+"100") 

data=SetCmd(switch1,"show wireless savi binding")

res1=CheckLine(data,sta1mac,Dhcp_pool1+"100","STATIC",IC=True)

res2 = CheckPing(sta1,Dhcp_pool1+'1',mode='linux')

#check

#result
printCheckStep(testname,'Step 4',res1,res2)

################################################################################
#Step 5 
# 操作
# STA1重新关联test1，并通过DHCP获取IP；
# STA1 ping 网关
# 预期
# STA1获取IP地址成功，ping网关成功
################################################################################
printStep(testname,'Step 5',
          'STA1 connect to network 1',
          'STA1 get IP via DHCP',
          'STA1 ping gateway success')

res1=res2=res3=1

#operate
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
if 0==res1:
    data = SetCmd(sta1,'ifconfig -v',Netcard_sta1)
    SearchResult1 = re.search('inet.+?(\d+\.\d+\.\d+\.\d+)\s+',data,re.I)
    if None !=SearchResult1:
        sta1_tmp_ip = SearchResult1.group(1)


#check

res2 = CheckPing(sta1,Dhcp_pool1+'1',mode='linux')
if 0!=res3:
    printRes("sta1 ping gateway failed!")

#result
printCheckStep(testname, 'Step 5',res1,res2)

################################################################################
#Step 6
# 操作
# 在AC1上查看sta1的SAVI表项
#
# 预期
# 在Ac1上为sta1建立了dhcp类型的savi表项
################################################################################
printStep(testname,'Step 6',
          'Check AC1 savi bindings')

res1=1

#operate
data1 = SetCmd(switch1,"show wireless savi binding")
res1 = CheckLine(data1,sta1mac,sta1_tmp_ip,"DHCP",IC=True)

if 0!=res1:
    printRes("Check AC1 SAVI binding failed！")

#result
printCheckStep(testname, 'Step 6',res1)


################################################################################
#Step 7
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 7',
          'Recover initial config')

#operate
#删除SAVI配置
EnterApProMode(switch1,1)
SetCmd(switch1,"no savi enable")
SetCmd(switch1,"no savi ipv6-slaac enable")
EnterWirelessMode(switch1)
SetCmd(switch1,"no savi binding ipv4",Dhcp_pool1+"100")

WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# WirelessApProfileApply(switch1,1)
# for i in xrange(10):
    # IdleAfter(10)
    # data1 = SetCmd(switch1,'show wireless ap status')
    # if re.search('1\s+Managed Success',data1) is not None:
        # break

# IdleAfter(Ac_ap_syn_time)

#end
printTimer(testname, 'End')
