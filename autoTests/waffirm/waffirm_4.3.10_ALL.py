#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.3.10.py - test case 4.3.10 of waffirm
#
# Author:  qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.3.10	基于流量的用户下线功能测试
# 测试目的：测试在线用户通过802.1x认证后，在一定的时间内网络访问流量低于一定的流量阈值时，用户被强制下线。
# 测试环境：同测试拓扑
# 测试描述：测试在线用户通过802.1x认证后，在一定的时间内网络访问流量低于一定的流量阈值时，用户被强制下线。
#          （STA1的MAC地址：STA1MAC）
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.3.10'
avoiderror(testname)
printTimer(testname,'Start','Test idle-timeout of radius attribute')
from time import *
################################################################################
#Step 1
#操作
#配置AC1的network1的安全接入方式为WPA-Enterprise，WPA version为WPA，认证服务器使用wlan：
#wireless
#security mode wpa-enterprise
#wpa versions wpa
#radius server-name acct wlan
#radius server-name auth wlan
#exit
#配置成功。在AC1上面show wireless network 1可以看到相关的配置。
################################################################################
printStep(testname,'Step 1',
          'set security mde of network 1 wpa-enterprise,',
          'set wpa versions wpa,',
          'set radius server-name acct wlan,',
          'set radius setver-name auth wlan,',
          'and u should config others and so on,',
          'check config success.')
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'radius source-ipv4 ' + StaticIpv4_ac1)
SetCmd(switch1,'radius-server key test')
SetCmd(switch1,'radius-server authentication host ' + Radius_server_windows)
SetCmd(switch1,'radius-server accounting host ' + Radius_server_windows)
SetCmd(switch1,'radius nas-ipv4 ' + StaticIpv4_ac1)
SetCmd(switch1,'aaa group server radius wlan')
SetCmd(switch1,'server ' + Radius_server_windows)
EnterConfigMode(switch1)
SetCmd(switch1,'aaa enable')
SetCmd(switch1,'aaa-accounting enable')
#配置wireless模式下的radius配置参数
EnterWirelessMode(switch1)
SetCmd(switch1,'radius server-name auth wlan')
SetCmd(switch1,'radius server-name acct wlan')
SetCmd(switch1,'radius accounting')
#配置network模式下的radius配置参数
EnterNetworkMode(switch1,1)
SetCmd(switch1,'radius server-name auth wlan')
SetCmd(switch1,'radius server-name acct wlan')
SetCmd(switch1,'radius accounting')
SetCmd(switch1,'security mode wpa-enterprise')
SetCmd(switch1,'wpa versions')

#check
data1 = SetCmd(switch1,'show run',timeout=15)
#printRes('data1='+ data1)
res1 = CheckLineList(data1,['radius source-ipv4 ' + StaticIpv4_ac1,'radius-server key 0 test','radius-server authentication host ' + Radius_server_windows,
                            'radius-server accounting host ' + Radius_server_windows,'aaa-accounting enable','aaa enable','radius nas-ipv4 ' + StaticIpv4_ac1,
                            'aaa group server radius wlan','server ' + Radius_server_windows])
data2 = SetCmd(switch1,'show wireless network 1',timeout=10)
res2 = CheckLine(data2,'Security Mode','WPA Enterprise')
res3 = CheckLine(data2,'RADIUS Authentication Server Name','wlan')
res4 = CheckLine(data2,'RADIUS Accounting Server Name','wlan')
res5 = CheckLine(data2,'WPA Versions','WPA/WPA2',IC=True)

#result
printCheckStep(testname, 'Step 1',res1,res2,res3,res4,res5)

################################################################################
#Step 2
# 在AC上通过offline-detect开启基于流量检测的功能，设定流量检测功能中的静默时间和流量阈值
# Wireless
# Network 1
# offline-detect
# offline-detect idle-timeout 60 threshold 102400
#预期
# 配置成功。在AC1上面show wireless network 1可以看到Offline-detect功能
# enable，Idle-timeout为60，Threshold为102400
################################################################################
printStep(testname,'Step 2',
          'enter network 1 then config offline-detect idle-timeout 60 threshold 102400,',
          'and show wireless network 1 to check configuration')
EnterWirelessMode(switch1)
SetCmd(switch1,'network 1')
# SetCmd(switch1,'offline-detect idle-timeout 60 threshold 102400')
SetCmd(switch1,'offline-detect idle-timeout 60 threshold 10240000')
data = SetCmd(switch1,'show wireless network 1',timeout=10)
res1 = CheckLine(data,'Offline-detect','Enable')
res2 = CheckLine(data,'Idle-timeout','60')
# res3 = CheckLine(data,'Threshold','102400')
res3 = CheckLine(data,'Threshold','10240000')
printCheckStep(testname, 'Step 2',res1,res2,res3)
################################################################################
#Step 3
# 将基于流量的用户下线功能相关参数下发到profile 1。
# Wireless ap profile apply 1
#预期
# 在AP上执行get vap vap0，可以看到offline_detect_enable开关为on，idle_timeout为60，
#offline_threshold为102400
################################################################################
printStep(testname,'Step 3',
          'wireless ap profile apply 1,',
          'and ap1 get vap vap0 to check configuration')
res1 = res2 =res3 = res4 = 1		  
EnterEnableMode(switch1)
res1 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
data = SetCmd(ap1,'get vap vap0')
res2 = CheckLine(data,'offline_detect_enable','on')
# res3 = CheckLine(data,'offline_threshold','102400')
res3 = CheckLine(data,'offline_threshold','10240000')
res4 = CheckLine(data,'idle_timeout','60')
printCheckStep(testname, 'Step 3',res1,res2,res3,res4)
################################################################################
#Step 4
# 设置STA1无线网卡的属性为WPA-Enterprise认证，关联网络test1，使用在Radius服务器配置
# 的用户名和密码，Radius服务器不下发RADIUS-ATTR-IDLE-TIMEOUT(28)属性。
# 预期
# 成功关联，并获取192.168.91.X网段的IP地址。Show wireless client summery
# 可以看到STA1（MAC Address显示STA1MAC），IP地址的网段正确
################################################################################
printStep(testname,'Step 4',
          'STA1 ping pc1',
          'ping success and the configuration is right.')
res1 = 1
EnterEnableMode(switch1)
StartDebug(switch1)
SetCmd(switch1,'debug aaa detail connection',timeout=1) 
# SetCmd(switch1,'debug aaa detail event',timeout=1)    
if CheckStaScanSSID([sta1],[Netcard_sta1]) == 0: 
	res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='wpa2_eap',identity=Dot1x_identity_no_idletimeout,password=Dot1x_password_no_idletimeout,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)

#result
printCheckStep(testname, 'Step 4',res1)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 5
    #操作
    #在STA1上ping PC1
    #
    #预期
    #能够ping通。在AP上执行get vap vap0，可以看到offline_detect_enable开关为on，
    # idle_timeout为60，offline_threshold为102400。在AP上执行get association 可以看
    # 到radius_idle_timeout值为0。
    ################################################################################
    printStep(testname,'Step 5',
              'STA1 ping pc1',
              'ping success and the configuration is right.')
    res1=res2=res3=res4=res5=1
    res1 = CheckPing(sta1,pc1_ipv4,mode='linux')
    data1 = SetCmd(ap1,'get vap vap0')
    res2 = CheckLine(data1,'offline_detect_enable','on')
    # res3 = CheckLine(data,'offline_threshold','102400')
    res3 = CheckLine(data,'offline_threshold','10240000')
    res4 = CheckLine(data1,'idle_timeout','60')
    data2 = SetCmd(ap1,'get association')
    res5 = CheckLine(data2,'radius_idle_timeout','0')
    printCheckStep(testname, 'Step 5',res1,res2,res3,res4,res5)
    ################################################################################
    #Step 6
    #操作
    #在60秒内，用户流量小于102400时，ap会强制用户下线。
    #
    #预期
    #用户被强制下线。等待130s后，debug显示计费开始到结束时间为60s。
    ################################################################################
    printStep(testname,'Step 6',
              'idleafter 70s,',
              'debug display accounting start to stop is 60s.')
    res1 = 1
    time1 = time2 = [0,0,0,0,0,0,0,0,0]
    #设备可能认证成功后没有发送start报文，等待idletimeout后重认证上线，再下线
    IdleAfter('130')
    SetCmd(switch1,'no debug all',timeout=1)
    SetCmd(switch1,'no debug all',timeout=1)
    data = StopDebug(switch1)
    time_start_stop = re.search('.*?\\s+(\\d\\d):(\\d\\d):(\\d\\d)\\s+\\d+\\s+radiusAccountingNamedStart.*?\\s+(\\d\\d):(\\d\\d):(\\d\\d)\\s+\\d+\\s+radiusAccountingNamedStop',data,re.S)
    # time_start_stop = re.search('.*?\\s+(\\d\\d):(\\d\\d):(\\d\\d)\\s+(\\d){4}\\s+radiusAccountingNamedStop',data)
    if time_start_stop != None:
        time1 = [0,0,0,int(time_start_stop.group(1)),int(time_start_stop.group(2)),int(time_start_stop.group(3)),0,0,0]
        time2 = [0,0,0,int(time_start_stop.group(4)),int(time_start_stop.group(5)),int(time_start_stop.group(6)),0,0,0]	
        print 'accounting start,the time is: '+str(time1[3])+':'+str(time1[4])+':'+str(time1[5])+'!'
        print 'accounting stop,the time is: '+str(time2[3])+':'+str(time2[4])+':'+str(time2[5])+'!'
    else:
        print 'can not get accounting time!'
    # if time_start_stop != None:
        # time2 = [0,0,0,int(time_start_stop.group(1)),int(time_start_stop.group(2)),int(time_start_stop.group(3)),0,0,0]
        # print 'accounting stop,the time is: '+str(time2[3])+':'+str(time2[4])+':'+str(time2[5])+'!'
    # else:
        # print 'can not get accounting stop time!'	
    time_account = int(mktime(time2)) - int(mktime(time1))
    if 50 <=time_account <= 66:
        res1 = 0
    WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
    printCheckStep(testname, 'Step 6',res1)

################################################################################
#Step 7
#设置STA1无线网卡的属性为WPA-Enterprise认证，关联网络test1，使用Radius服务器上面配置好的用户名和密码。
# Radius服务器下发RADIUS-ATTR-IDLE-TIMEOUT(28)属性，属性值为100
#成功关联，并获取192.168.Env1.X网段的IP地址。Show wireless client summery
#可以看到STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
################################################################################
printStep(testname,'Step 7',
          'STA1 scanning network,',
          'and connect to affirm_auto_test1 using encrypt wpa')
res1=1
EnterEnableMode(switch1)
StartDebug(switch1)
SetCmd(switch1,'debug aaa detail connection',timeout=1)
# SetCmd(switch1,'debug aaa detail event',timeout=1)  
if CheckStaScanSSID([sta1],[Netcard_sta1]) == 0: 
	res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='wpa_eap',identity=Dot1x_identity_with_idletimeout,password=Dot1x_password_with_idletimeout,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)

#result
printCheckStep(testname, 'Step 7',res1)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 8
    #操作
    #在STA1上ping PC1
    #
    #预期
    #能够ping通。在AP上执行get association 可以看到radius_idle_timeout值为70。
    ################################################################################

    printStep(testname,'Step 8',
              'STA1 ping pc1',
              'ping success and the radius_idle_timeout is 70.')
    res1=res2=1		  
    res1 = CheckPing(sta1,pc1_ipv4,mode='linux')
    data2 = SetCmd(ap1,'get association')
    res2 = CheckLine(data2,'radius_idle_timeout','70')
    printCheckStep(testname, 'Step 8',res1,res2)

    ################################################################################
    #Step 9
    #操作
    #在100秒内，用户流量小于102400时，ap会强制用户下线。
    #
    #预期
    #用户被强制下线。等待150s后，在AP上执行Wlanconfig ath0 list看不到该用户。
    ################################################################################

    printStep(testname,'Step 9',
              'idleafter 110s,',
              'the user is offlined by ac, and ap1 can not show user.')
    res1 = 1
    #设备可能认证成功后没有发送start报文，等待idletimeout后重认证上线，再下线
    IdleAfter('150')
    SetCmd(switch1,'no debug all',timeout=1)
    SetCmd(switch1,'no debug all',timeout=1)
    data = StopDebug(switch1)
    time_start_stop = re.search('.*?\\s+(\\d\\d):(\\d\\d):(\\d\\d)\\s+\\d+\\s+radiusAccountingNamedStart.*?\\s+(\\d\\d):(\\d\\d):(\\d\\d)\\s+\\d+\\s+radiusAccountingNamedStop',data,re.S)
    if time_start_stop != None:
        time1 = [0,0,0,int(time_start_stop.group(1)),int(time_start_stop.group(2)),int(time_start_stop.group(3)),0,0,0]
        time2 = [0,0,0,int(time_start_stop.group(4)),int(time_start_stop.group(5)),int(time_start_stop.group(6)),0,0,0]	
        print 'accounting start,the time is: '+str(time1[3])+':'+str(time1[4])+':'+str(time1[5])+'!'
        print 'accounting stop,the time is: '+str(time2[3])+':'+str(time2[4])+':'+str(time2[5])+'!'
    else:
        print 'can not get accounting time!'		
    time_account = int(mktime(time2)) - int(mktime(time1))		
    if 63 <=time_account <= 77:
        res1 = 0

    printCheckStep(testname, 'Step 9',res1)
################################################################################
#Step 10
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 10',
          'Recover initial config for switches.')

#operate
EnterNetworkMode(switch1,1)
SetCmd(switch1,'no radius server-name auth')
SetCmd(switch1,'no radius server-name acct')
SetCmd(switch1,'no radius accounting')
SetCmd(switch1,'security mode none')
SetCmd(switch1,'no wpa versions')
#配置wireless模式下的radius配置参数
EnterWirelessMode(switch1)
SetCmd(switch1,'no radius server-name auth')
SetCmd(switch1,'no radius server-name acct')
SetCmd(switch1,'no radius accounting')

EnterConfigMode(switch1)
SetCmd(switch1,'no radius source-ipv4')
SetCmd(switch1,'no radius-server key')
SetCmd(switch1,'no aaa group server radius wlan')
SetCmd(switch1,'no radius nas-ipv4')
SetCmd(switch1,'no aaa enable')
SetCmd(switch1,'no aaa-accounting enable')
SetCmd(switch1,'no radius-server authentication host ' + Radius_server_windows)
SetCmd(switch1,'no radius-server accounting host ' + Radius_server_windows)
EnterWirelessMode(switch1)
SetCmd(switch1,'network 1')
SetCmd(switch1,'no offline-detect')
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#end
printTimer(testname, 'End')