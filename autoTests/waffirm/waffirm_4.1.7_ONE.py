#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.1.7.py - test case 4.1.1 of waffirm_new
#
# Author:  (jinpfb)
#
# Version 1.0.0
#
# Date:  2012-12-7 13:47:23
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 4.1.7	配置推送
# 测试目的：测试AC支持配置推送功能
# 测试环境：同测试拓扑
# 测试描述：把AC1的无线配置推送到AC2。
#（AC1的wireless地址是1.1.1.1；AC2的wireless地址是2.2.2.2；AP1的MAC地址：AP1MAC）
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

testname = 'TestCase 4.1.7'
avoiderror(testname)
printTimer(testname,'Start','test configuration push between AC1 and AC2')

suggestionList = []

################################################################################
#Step 1
#
#操作
# AC1使能全部配置推送功能
# AC1(config-wireless)#peer-switch configuration
#
#预期
# AC1上show显示全部enable
# AC1(config-wireless)#show wireless peer-switch configuration 
################################################################################
printStep(testname,"Step 1',\
          'Enable 'peer-switch configuration' on AC1',\
          'Check the result")

res1=1

#operate

#在AC2上开启对AP1的三层发现
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery ip-list',StaticIpv4_ac1)  

EnterEnableMode(switch1)
CheckSutCmd(switch1,'show wireless peer-switch',
            check=[(StaticIpv4_ac2,'IP Poll')],
            waittime=5,retry=20,interval=5,IC=True)

EnterWirelessMode(switch1)
SetCmd(switch1,'peer-switch configuration')  
IdleAfter(1)
#!!!!!!!!!现有版本对 'RADIUS Client' 推送还不支持，如果开启，那么整体推送失败，因此此处先no 掉这一选项
#!!!!!!!!!7.0一支持该功能的推送
# EnterWirelessMode(switch1)
# SetCmd(switch1,'no peer-switch configuration radius-client')

data1 = SetCmd(switch1,'show wireless peer-switch configuration')

#check
res1 = CheckLineList(data1,[('AP Database','Enable'),('AP Profile','Enable'),
                            ('Channel Power','Enable'),('Discovery','Enable'),
                            ('Global','Enable'),('Known Client','Enable'),
                            ('Captive Portal','Enable'),
                            #                            ('RADIUS Client','Disable'),\
                            ('RADIUS Client','Enable'),
                            ('WDS Group','Enable'),('QoS ACL','Enable'),
                            ('QoS DiffServ','Enable'),('Device Location','Enable')],IC=True)
                                
#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#操作
#在AC1上进行一系列配置
#
#预期
#配置成功
################################################################################
printStep(testname,'Step 2',
          'Execute a set of configuration on AC1')

res1=1

#operate
EnterConfigMode(switch1)
SetCmd(switch1,'radius-server authentication host 1.2.3.4')
SetCmd(switch1,'radius-server accounting host 1.2.3.4')
SetCmd(switch1,'radius-server key 0 test')
SetCmd(switch1,'aaa group server radius configuration_test_server')
SetCmd(switch1,'server 1.2.3.4')
SetCmd(switch1,'exit')

EnterWirelessMode(switch1)
SetCmd(switch1,'channel-plan bgn interval 777')
SetCmd(switch1,'power-plan interval 777')
SetCmd(switch1,'discovery ip-list 77.77.77.77')
SetCmd(switch1,'known-client 00-77-77-77-77-77 action deny name know777')

EnterWirelessMode(switch1)
SetCmd(switch1,'network 777')
SetCmd(switch1,'ssid configuration_test_ssid')
SetCmd(switch1,'security mode wpa-enterprise')
SetCmd(switch1,'radius server-name acct configuration_test_server')
SetCmd(switch1,'radius server-name auth configuration_test_server')
SetCmd(switch1,'exit')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 777')
SetCmd(switch1,'radio 1')
SetCmd(switch1,'vap 0')
SetCmd(switch1,'network 777')
SetCmd(switch1,'end')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap database 00-03-0f-77-77-70')
SetCmd(switch1,'profile 777')
SetCmd(switch1,'exit')

EnterWirelessMode(switch1)
SetCmd(switch1,'wds-group 1')
SetCmd(switch1,'ap 00-03-0f-77-77-70')
SetCmd(switch1,'exit')

EnterWirelessMode(switch1)
SetCmd(switch1,'device-location building 1')
SetCmd(switch1,'floor 1')
SetCmd(switch1,'ap 00-03-0f-77-77-70 xy-coordinate metres 777 777')
SetCmd(switch1,'end')

EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'enable')
SetCmd(switch1,'configuration 7')
SetCmd(switch1,'interface ws-network 777')

data1 = ShowRun(switch1)
#check
res1 = CheckLineInOrder(data1,[('radius-server authentication host 1.2.3.4'),
                               ('radius-server accounting host 1.2.3.4'),
                               ('aaa group server radius configuration_test_server'),
                               ('server 1.2.3.4'),
                               ('discovery ip-list 77.77.77.77'),
                               ('known-client 00-77-77-77-77-77 action deny name know777'),
                               ('channel-plan bgn interval 777'),
                               ('power-plan interval 777'),
                               ('network 777'),
                               ('radius server-name auth configuration_test_server'),
                               ('radius server-name acct configuration_test_server'),
                               ('security mode wpa-enterprise'),
                               ('ssid configuration_test_ssid'),
                               ('device-location building 1'),
                               ('description Building-1'),
                            ('floor 1'),
                               ('ap 00-03-0f-77-77-70 xy-coordinate metres 777 777'),
                               ('ap profile 777'),
                               ('network 777'),
                               ('ap database 00-03-0f-77-77-70'),
                               ('profile 777'),
                               ('wds-group 1'),
                               ('ap 00-03-0f-77-77-70'),
                               ('captive-portal'),
                               ('enable'),
                               ('configuration 7'),
                               ('interface ws-network 777')],IC=True)

#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#操作
#AC1上执行配置推送
#AC1#wireless peer-switch configure 2.2.2.2
#
#AC1上显示“Write configuration successfully!”后
#“show wireless peer-switch configure status”显示“Configuration Status”为“Success”
################################################################################
printStep(testname,'Step 3',
          'Execute configuration push on AC1')

res1=res2=1
#operate
StartDebug(switch1)
EnterEnableMode(switch1)
SetCmd(switch1,'wireless peer-switch configure',StaticIpv4_ac2)
IdleAfter(20)
data1 = StopDebug(switch1)
data2 = SetCmd(switch1,'show wireless peer-switch configure status')

#check
res1 = CheckLine(data1,'Write configuration successfully',IC=True)
res2 = CheckLine(data2,'Success',IC=True)

#result
printCheckStep(testname, 'Step 3', res1,res2)

################################################################################
#Step 4
#操作
#AC2上show run确认配置推送成功
#
#show run确认配置推送成功
################################################################################
printStep(testname,'Step 4',
          'Check if configuration push success on AC2')

res1=1
#operate

data1 = ShowRun(switch2)

#check
res1 = CheckLineInOrder(data1,[
    #                             ('radius-server authentication host','192.168.10.2'), \
#                             ('radius-server accounting host',pc1_ipv4), \
#                             ('aaa group server radius configuration_test_server'), \
#                             ('server',pc1_ipv4), \
                            ('discovery ip-list 77.77.77.77'),
    ('known-client 00-77-77-77-77-77 action deny name know777'),
    ('channel-plan bgn interval 777'),
    ('power-plan interval 777'),
    ('network 777'),
    ('radius server-name auth configuration_test_server'),
    ('radius server-name acct configuration_test_server'),
    ('security mode wpa-enterprise'),
    ('ssid configuration_test_ssid'),
    ('device-location building 1'),
    ('description Building-1'),
                            ('floor 1'),
    ('ap 00-03-0f-77-77-70 xy-coordinate metres 777 777'),
    ('ap profile 777'),
    ('network 777'),
    ('ap database 00-03-0f-77-77-70'),
    ('profile 777'),
    ('wds-group 1'),
    ('ap 00-03-0f-77-77-70'),
    ('captive-portal'),
    ('enable'),
    ('configuration 7'),
    ('interface ws-network 777')],IC=True)

#result
if res1 != 0:
    suggestionList.append('Suggestions: Step 4 failed reason MAYBE RDM27674')
printCheckStep(testname, 'Step 4', res1)

################################################################################
#Step 5
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 5',
          'Recover initial config')

#operate

#缺省配置,默认配置推送项都是打开的，除了discovery一项,此处将其关闭
EnterWirelessMode(switch1)
SetCmd(switch1,'no peer-switch configuration discovery')

#在AC2上关闭对AP1的三层发现
EnterWirelessMode(switch2)
#SetCmd(switch2,'no cluster-priority')
SetCmd(switch2,'no discovery ip-list',StaticIpv4_ac1) 

#推送过程已经在AC1,AC2上都执行了save 动作，因此重启AC 不起作用，必须逐条清除配置
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'disable')
SetCmd(switch1,'no configuration 7')

EnterWirelessMode(switch1)
SetCmd(switch1,'no device-location building 1')

EnterWirelessMode(switch1)
SetCmd(switch1,'no wds-group 1')

EnterWirelessMode(switch1)
SetCmd(switch1,'no ap database 00-03-0f-77-77-70')

EnterWirelessMode(switch1)
SetCmd(switch1,'no ap profile 777')
SetCmd(switch1,'no network 777')

EnterWirelessMode(switch1)
SetCmd(switch1,'no channel-plan bgn interval')
SetCmd(switch1,'no power-plan interval')
SetCmd(switch1,'no discovery ip-list 77.77.77.77')
SetCmd(switch1,'no known-client 00-77-77-77-77-77')

EnterConfigMode(switch1)
SetCmd(switch1,'no aaa group server radius configuration_test_server')
SetCmd(switch1,'no radius-server authentication host 1.2.3.4')
SetCmd(switch1,'no radius-server accounting host 1.2.3.4')
SetCmd(switch1,'no radius-server key')

EnterEnableMode(switch1)
data = SetCmd(switch1,'write',timeout=1)
#if 0==CheckLine(data,'Y/N'):
SetCmd(switch1,'y',timeout=1)
    
#清空AC2上的配置
EnterConfigMode(switch2)
SetCmd(switch2,'captive-portal')
SetCmd(switch2,'disable')
SetCmd(switch2,'no configuration 7')

EnterWirelessMode(switch2)
SetCmd(switch2,'no device-location building 1')

EnterWirelessMode(switch2)
SetCmd(switch2,'no wds-group 1')

EnterWirelessMode(switch2)
SetCmd(switch2,'no ap database 00-03-0f-77-77-70')

EnterWirelessMode(switch2)
SetCmd(switch2,'no ap profile 777')
SetCmd(switch2,'no network 777')

EnterWirelessMode(switch2)
SetCmd(switch2,'no channel-plan bgn interval')
SetCmd(switch2,'no power-plan interval')
SetCmd(switch2,'no discovery ip-list 77.77.77.77')
SetCmd(switch2,'no known-client 00-77-77-77-77-77')

EnterConfigMode(switch2)
SetCmd(switch2,'no aaa group server radius configuration_test_server')
SetCmd(switch2,'no radius-server authentication host',pc1_ipv4)
SetCmd(switch2,'no radius-server accounting host',pc1_ipv4)

#AC1上其他无关配置也会推送到AC2,此处 no 掉
EnterWirelessMode(switch2)
SetCmd(switch2,'no discovery ip-list',Ap1_ipv4)                      
SetCmd(switch2,'no discovery ipv6-list',Ap1_ipv6)
SetCmd(switch2,'no discovery ip-list',Ap2_ipv4)
SetCmd(switch2,'no discovery ipv6-list',Ap2_ipv6)

EnterEnableMode(switch2)
data = SetCmd(switch2,'write',timeout=1)
#if 0==CheckLine(data,'Y/N'):
SetCmd(switch2,'y',timeout=1)

#end
printTimer(testname, 'End',suggestion = suggestionList)