#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.26_5G.py - test case 4.26 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
# 
# Date 2017-11-22 14:37:33
#
# Features:
# 4.26	5G优先
# 测试目的：AP的RF-5G优先功能
# 测试描述：对于双频AP，开启5G优先功能后，可以引导双频client关联到5G
# 测试环境：见测试拓扑
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.6
#*******************************************************************************

#Package

#Global Definition
 
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.26'
avoiderror(testname)
printTimer(testname,'Start','test band-select')

################################################################################
#Step 1
#操作
# AC1的network1采用默认的安全接入方式none，即open方式，开启5G优先功能
# AP profile下配置#band-select enable
#band-select download下发
#预期
# 配置成功
################################################################################
printStep(testname,'Step 1',\
          'band-select enable in ap profile1')

res1=1
#operate
# 更改AP2的ssid，防止sta关联到AP2上
EnterWirelessMode(switch1)
SetCmd(switch1,'network 101')
SetCmd(switch1,'ssid whatever')
for i in [radio1num,radio2num]:
    EnterApProMode(switch1,2)
    SetCmd(switch1,'radio '+i)
    SetCmd(switch1,'vap 0')
    SetCmd(switch1,'network 101')
WirelessApplyProfileWithCheck(switch1,['2'],[ap2mac])
# 配置band-select enable并下发
EnterApProMode(switch1,1)
SetCmd(switch1,'band-select enable')
SetCmd(switch1,'band-select download')
# 检查配置成功
data = SetCmd(switch1,'show run c')
res1 = CheckLine(data,'band-select enable')
#result
printCheckStep(testname, 'Step 1', res1)
################################################################################
#Step 2
#操作
# 等待30s之后，使用双频client关联AP
#
#预期
# 可以关联成功，并ping通网关
################################################################################
printStep(testname,'Step 2',\
          'IdleAfter 30s',\
		  'STA1 connect to test1 successfully')

res1=res2=1
#operate
IdleAfter(30)
# AC主动断开所有关联的客户端，防止影响后续步骤
EnterEnableMode(switch1)
SetCmd(switch1,'wireless client  disassociate',timeout=1)
SetCmd(switch1,'y')
#check
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='open',checkDhcpAddress=Netcard_ipaddress_check)
res2 = CheckPing(sta1,pc1_ipv4,mode='linux')
#result
printCheckStep(testname, 'Step 2',res1,res2)

################################################################################
#Step 3
#操作
# 在AC上show wireless ap radio status查看client是否关联在5G
#预期
# 在5G radio下可以看到有客户端关联，2.4G没有
################################################################################

printStep(testname,'Step 3',\
          'AC1 show wireless ap radio status',\
          'check sta connected to 5G radio')

res1=res2=1
#operate
data = SetCmd(switch1,'show wireless ap '+ap1mac+' radio status')
res1 = CheckLine(data,'\s+1\s+(\d+\s+){3}0')
res2 = CheckLine(data,'\s+2\s+(\d+\s+){3}1')
#check
#result
printCheckStep(testname, 'Step 3',res1,res2)

# 备注：方案中step4、5、6无法实现自动化，因为要使sta连接上2.4G需要5G信号强度很低，实际上即使将5G功率降到最低，
# 但AP和sta网卡的距离不够远的情况下，sta仍能连接到5G，（实测将AP功率降到最低，AP距sta网卡约10米左右，5G信号才足够弱，sta才能连接到2.4G），
# 因此目前的自动化环境无法满足此要求
################################################################################
#Step 4
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 4',\
          'Recover initial config for switches.')

#operate
EnterApProMode(switch1,1)
SetCmd(switch1,'no band-select enable')
SetCmd(switch1,'band-select download')

for i in [radio1num,radio2num]:
    EnterApProMode(switch1,2)
    SetCmd(switch1,'radio '+i)
    SetCmd(switch1,'vap 0')
    SetCmd(switch1,'network 1')
    
ClearNetworkConfig(switch1,101)
SetCmd(switch1,'no network 101')
WirelessApplyProfileWithCheck(switch1,['2'],[ap2mac])
# end
printTimer(testname, 'End')