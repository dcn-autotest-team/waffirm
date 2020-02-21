#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.25.py - test case 3.1.25 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-10 16:42:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.25 配置推送功能
# 测试目的：测试配置推送功能是否正常
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.25'

avoiderror(testname)
printTimer(testname,'Start','Test configuration push function')

################################################################################
#Step 1
#
#操作
#把AC2的IP地址加入到AC1的三层发现ip list中
#
#预期
#在AC1上show wireless peer-switch显示有“IP Address”为“IF_VLAN70_S2_IPV4”
################################################################################

printStep(testname,'Step 1',
          'Add AC2 ip to discovery ip list on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch2)
SetCmd(switch2,'no discovery vlan-list 1')

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list',If_vlan70_s2_ipv4_s)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
IdleAfter(20)

#check
res1 = CheckSutCmd(switch1,'show wireless peer-switch',
				   check=[(If_vlan70_s2_ipv4_s,'IP Poll')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
#在AC1上进行配置
#
#预期
#配置成功
################################################################################

printStep(testname,'Step 2',
          'config on AC1',
          'Check the result')

# operate
EnterConfigMode(switch1)
SetCmd(switch1,'access-list 1 deny host-source 80.1.1.5')
SetCmd(switch1,'access-list 102 permit ip any-source host-destination 80.1.1.3')
SetCmd(switch1,'access-list 1103 permit host-source-mac 00-0d-a3-13-30-98 any-destination-mac cos 4')
SetCmd(switch1,'access-list 701 permit host-source-mac 00-0d-a3-13-30-98')

EnterConfigMode(switch1)
SetCmd(switch1,'ipv6 access-list standard abc')
SetCmd(switch1,'permit host-source 1:1::1:1')

EnterConfigMode(switch1)
SetCmd(switch1,'ipv6 access-list extended aaa')
SetCmd(switch1,'permit icmp host-source 1:1::1:1 host-destination 1:1::1:2')

EnterConfigMode(switch1)
SetCmd(switch1,'class-map class1')
SetCmd(switch1,'match access-group 102')

EnterConfigMode(switch1)
SetCmd(switch1,'policy-map policy1')
SetCmd(switch1,'class class1')
SetCmd(switch1,'policy 1000 1000 conform-action set-dscp-transmit 18 exceed-action drop')

EnterWirelessMode(switch1)
SetCmd(switch1,'network 777')
SetCmd(switch1,'ssid configuration_test_ssid')
SetCmd(switch1,'security mode wpa-enterprise')
SetCmd(switch1,'radius server-name acct configuration_test_server')
SetCmd(switch1,'radius server-name auth configuration_test_server')
SetCmd(switch1,'client-qos enable')
SetCmd(switch1,'client-qos diffserv-policy down policy1')
SetCmd(switch1,'client-qos diffserv-policy up policy1')

EnterWirelessMode(switch1)
SetCmd(switch1,'network 777')
SetCmd(switch1,'client-qos access-control down ip 1')
SetCmd(switch1,'client-qos access-control up ip 102')
SetCmd(switch1,'client-qos bandwidth-limit down 1024')
SetCmd(switch1,'client-qos bandwidth-limit up 1024')

EnterWirelessMode(switch1)
SetCmd(switch1,'network 778')
SetCmd(switch1,'ssid configuration_test_ssid1')
SetCmd(switch1,'client-qos access-control down ip 1')
SetCmd(switch1,'client-qos access-control up ip 102')

EnterWirelessMode(switch1)
SetCmd(switch1,'network 779')
SetCmd(switch1,'ssid configuration_test_ssid2')
SetCmd(switch1,'client-qos access-control down ipv6 abc')
SetCmd(switch1,'client-qos access-control up ipv6 aaa')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 777')
SetCmd(switch1,'radio 1')
SetCmd(switch1,'vap 0')
SetCmd(switch1,'network 777')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap database 00-03-0f-77-77-70')
SetCmd(switch1,'profile 777')

EnterWirelessMode(switch1)
SetCmd(switch1,'channel-plan bgn interval 777')
SetCmd(switch1,'power-plan interval 777')
SetCmd(switch1,'discovery ip-list 77.77.77.77')
SetCmd(switch1,'known-client 00-77-77-77-77-77 action deny name know777')
SetCmd(switch1,'ap client-qos')

EnterWirelessMode(switch1)
SetCmd(switch1,'wds-group 1')
SetCmd(switch1,'ap 00-03-0f-77-77-70')

EnterWirelessMode(switch1)
SetCmd(switch1,'device-location building 1')
SetCmd(switch1,'floor 1')
SetCmd(switch1,'ap 00-03-0f-77-77-70 xy-coordinate metres 777 777')

EnterConfigMode(switch1)
SetCmd(switch1,'radius-server authentication host 1.2.3.4')
SetCmd(switch1,'radius-server accounting host 1.2.3.4')
SetCmd(switch1,'aaa group server radius configuration_test_server')
SetCmd(switch1,'server 1.2.3.4')

EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
IdleAfter(1)
SetCmd(switch1,'enable')
SetCmd(switch1,'configuration 7')
SetCmd(switch1,'interface ws-network 777')

#result
printCheckStep(testname, 'Step 2', 0)

################################################################################
#Step 3
#
#操作
#在AC1上查看初始状态时关键配置开关
#
#预期
#在AC1上显示Discovery为Disable
#其他关键配置即“AP Database” “AP Profile” “Channel Power ” “Global” “Known Client”“ Captive Portal”
#“RADIUS Client” “WDS Group”“ QoS ACL” “QoS DiffServ” “Device Location” “WAPI”开关都为Enable
################################################################################

printStep(testname,'Step 3',
          'Check peer-switch configuration on AC1 1',
		  'Check the result')		  

# operate
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless peer-switch configuration')

checklist1 = []
checklist1.append(('AP Database','Enable'))
checklist1.append(('AP Profile','Enable'))
checklist1.append(('Channel Power','Enable'))
checklist1.append(('Global','Enable'))
checklist1.append(('Known Client','Enable'))
checklist1.append(('Captive Portal','Enable'))
checklist1.append(('RADIUS Client','Enable'))
checklist1.append(('QoS ACL','Enable'))
checklist1.append(('QoS DiffServ','Enable'))
checklist1.append(('Device Location','Enable'))
checklist1.append(('WAPI','Enable'))
#check
res1 = CheckLineList(data1,checklist1,IC=True)
				   
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
#在AC1上关闭所有关键配置的推送
#在AC1上发出配置推送到AC2
#
#预期
#推送不成功,在AC1上检查会出现如下打印:Error! Failed to start the configuration push
################################################################################

printStep(testname,'Step 4',
          'Close all peer-switch configuration',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no peer-switch configuration')	
	
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'wireless peer-switch configure',timeout=5)
#check
res1 = CheckLine(data1,'Error! Failed to start the configuration push',IC=True)
				   
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#在AC1上开启ap-database的配置推送开关
#
#预期
#在AC1上检查AP Database显示为：Enable
################################################################################

printStep(testname,'Step 5',
          'Open peer-switch configuration ap-database',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'peer-switch configuration ap-database')
  
data1 = SetCmd(switch1,'show wireless peer-switch configuration')
#check
res1 = CheckLine(data1,'AP Database','Enable',IC=True)
	
#result
printCheckStep(testname,'Step 5', res1)

################################################################################
#Step 6
#
#操作
#在AC1上发出配置推送到AC2
#
#预期
#AC1上显示“Write configuration successfully!”
#在AC2上检查显示“Config Push Validation Failed”
################################################################################

printStep(testname,'Step 6',
          'Config AC2 wireless peer-switch configure',
          'Check the result')

# operate
EnterEnableMode(switch1)
StartDebug(switch2)
data1 = SetCmd(switch1,'wireless peer-switch configure',timeout=10)
#check1	
res1 = CheckLine(data1,'Write configuration successfully!',IC=True)
IdleAfter(60)
data2 = StopDebug(switch2)
#check2
res2 = CheckLine(data2,'Config Push Validation Failed',IC=True)

#result
printCheckStep(testname,'Step 6', res1, res2)

################################################################################
#Step 7
#
#操作
#在AC1上开启ap-profile, QoS ACL, QoS DiffServ的配置推送开关
#在AC1上发出配置推送到AC2
#
#预期
#推送成功,AC1上显示“Write configuration successfully!”
#“show wireless peer-switch configure status”显示“Configuration Status”为“Success”
################################################################################

printStep(testname,'Step 7',
          'Open peer-switch configuration ap-profile, QoS ACL, QoS DiffServ',
          'Check the result')	  

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'peer-switch configuration ap-profile')
SetCmd(switch1,'peer-switch configuration qos-acl')
SetCmd(switch1,'peer-switch configuration qos-diffserv')

EnterEnableMode(switch1)		  
data1 = SetCmd(switch1,'wireless peer-switch configure',timeout=10)
#check1	
res1 = CheckLine(data1,'Write configuration successfully!',IC=True)
#check2
res2 = CheckSutCmd(switch1,'show wireless peer-switch configure status',
				   check=[(If_vlan70_s2_ipv4_s,'Success')],
				   retry=30,interval=5,waitflag=False,IC=True)		
	
#result
printCheckStep(testname,'Step 7', res1, res2)

################################################################################
#Step 8
#
#操作
#在AC1上关闭ap-database的配置推送开关
#
#预期
#在AC1上show wireless peer-switch configuration检查AP Database显示为:Disable
################################################################################

printStep(testname,'Step 8',
          'Close peer-switch configuration ap-database',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no peer-switch configuration ap-database')

data1 = SetCmd(switch1,'show wireless peer-switch configuration')
#check
res1 = CheckLine(data1,'AP Database','Disable',IC=True)

#result
printCheckStep(testname,'Step 8', res1)

################################################################################
#Step 9
#
#操作
#在AC1上开启所有关键配置的推送
#
#预期
#在AC1上显示所有的关键配置开关都为Enable
################################################################################

printStep(testname,'Step 9',
          'Open all peer-switch configuration',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'peer-switch configuration')	  
		  
data1 = SetCmd(switch1,'show wireless peer-switch configuration')
checklist1 = []
checklist1.append(('AP Database','Enable'))
checklist1.append(('AP Profile','Enable'))
checklist1.append(('Discovery','Enable'))
checklist1.append(('Channel Power','Enable'))
checklist1.append(('Global','Enable'))
checklist1.append(('Captive Portal','Enable'))
checklist1.append(('RADIUS Client','Enable'))
checklist1.append(('WDS Group','Enable'))
checklist1.append(('QoS ACL','Enable'))
checklist1.append(('QoS DiffServ','Enable'))
checklist1.append(('Device Location','Enable'))
checklist1.append(('WAPI','Enable'))

#check
res1 = CheckLineList(data1,checklist1,IC=True)

#result
printCheckStep(testname,'Step 9', res1)

################################################################################
#Step 10
#
#操作
#在AC1上发出配置推送到AC2
#
#预期
#推送成功,AC1上显示“Write configuration successfully!”
#“show wireless peer-switch configure status”显示“Configuration Status”为“Success”
################################################################################

printStep(testname,'Step 10',
          'Config AC2 wireless peer-switch configure',
          'Check the result') 

# operate
EnterEnableMode(switch1)		  
data1 = SetCmd(switch1,'wireless peer-switch configure',timeout=10)
#check1	
res1 = CheckLine(data1,'Write configuration successfully!',IC=True)				   
IdleAfter(10)
#check2
res2 = CheckSutCmd(switch1,'show wireless peer-switch configure status',
				   check=[(If_vlan70_s2_ipv4_s,'Success')],
				   retry=30,interval=5,waitflag=False,IC=True)		

#result
printCheckStep(testname,'Step 10', res1, res2)

################################################################################
#Step 11
#
#操作
#AC2上show run确认配置推送成功
#
#预期
#show run确认配置推送成功
################################################################################

printStep(testname,'Step 11',
          'Check show run on AC2',
          'Check the result')

# operate
EnterEnableMode(switch2)
data1 = SetCmd(switch2,'show run')
#check
res1 = CheckLineList(data1,['access-list 1 deny host-source 80.1.1.5',
                     'access-list 102 permit ip any-source host-destination 80.1.1.3',
					 'ipv6 access-list standard abc','permit host-source 1:1::1:1',
					 'ipv6 access-list extended aaa','permit icmp host-source 1:1::1:1 host-destination 1:1::1:2',
					 'class-map class1','match access-group 102','policy-map policy1','class class1',
					 'policy 1000 1000 conform-action set-dscp-transmit 18 exceed-action drop',
					 'radius-server authentication host 1.2.3.4','radius-server accounting host 1.2.3.4',
					 'aaa group server radius configuration_test_server','server 1.2.3.4',
					 'discovery ip-list 77.77.77.77','known-client 00-77-77-77-77-77 action deny name know777',
					 'ap client-qos','channel-plan bgn interval 777','power-plan interval 777',
					 'network 777','client-qos enable','client-qos access-control down ip 1',
					 'client-qos access-control up ip 102','client-qos bandwidth-limit down 1024',
					 'client-qos bandwidth-limit up 1024','client-qos diffserv-policy down policy1',
					 'client-qos diffserv-policy up policy1','radius server-name auth configuration_test_server',
					 'radius server-name acct configuration_test_server','security mode wpa-enterprise',
					 'ssid configuration_test_ssid','network 778','client-qos access-control down ip 1',
					 'client-qos access-control up ip 102','ssid configuration_test_ssid1',
					 'network 779','client-qos access-control down ipv6 abc',
					 'client-qos access-control up ipv6 aaa','ssid configuration_test_ssid2',
					 'device-location building 1','description Building-1','floor 1',
					 'description None','ap 00-03-0f-77-77-70 xy-coordinate metres 777 777',
					 'ap profile 777','network 777','ap database 00-03-0f-77-77-70','profile 777',
					 'wds-group 1','ap 00-03-0f-77-77-70','captive-portal','enable',
					 'configuration 7','interface ws-network 777'],IC=True)
				   
#result
printCheckStep(testname,'Step 11', res1)

################################################################################
#Step 12
#
#操作
#在AC1上增加配置
#
#预期
#推送成功，AC1上显示“Write configuration successfully!”
#“show wireless peer-switch configure status”显示“Configuration Status”为“Success”
################################################################################

printStep(testname,'Step 12',
          'config on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'igmp snooping')

EnterWirelessMode(switch1)
SetCmd(switch1,'network 777')
SetCmd(switch1,'igmp snooping m2u')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 777')
SetCmd(switch1,'radio 1')
SetCmd(switch1,'time-limit from 1:30 to 2:30 weekday Tuesday')
SetCmd(switch1,'time-limit-UTC from 2017-02-02 2:30 to 2017-02-02 3:30 off')

EnterWirelessMode(switch1)
SetCmd(switch1,'network 777')
SetCmd(switch1,'time-limit from 1:30 to 2:30 weekday Tuesday')
SetCmd(switch1,'time-limit-UTC from 2017-02-02 2:30 to 2017-02-02 3:30 off')

EnterEnableMode(switch1)
#check1
res1 = CheckSutCmd(switch1,'wireless peer-switch configure',
				   check=[('Write configuration successfully!')],
				   retry=30,interval=5,waitflag=False,IC=True)	
				   
IdleAfter(10)
#check2
res2 = CheckSutCmd(switch1,'show wireless peer-switch configure status',
				   check=[(If_vlan70_s2_ipv4_s,'Success')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 12', res1, res2)

################################################################################
#Step 13
#
#操作
#AC2上show run确认配置推送成功
#
#预期
#show run确认配置推送成功
################################################################################

printStep(testname,'Step 13',
          'Check show run on AC2',
          'Check the result')

# operate
EnterEnableMode(switch2)
data1 = SetCmd(switch2,'show run')
#check
res1 = CheckLineList(data1,['igmp snooping','igmp snooping m2u',
                     'time-limit from 01:30 to 02:30 weekday tuesday',
					 'time-limit-UTC from 2017-02-02 02:30 to 2017-02-02 03:30 off',
					 'ap profile 777','time-limit from 01:30 to 02:30 weekday tuesday',
					 'time-limit-UTC from 2017-02-02 02:30 to 2017-02-02 03:30 off'],IC=True)

#result
printCheckStep(testname,'Step 13', res1)

################################################################################
#Step 14
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 14',
          'Recover initial config')

# operate		  
#恢复AC1的配置
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery ip-list',If_vlan70_s2_ipv4_s)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
SetCmd(switch1,'peer-switch configuration')
SetCmd(switch1,'no peer-switch configuration Discovery')
SetCmd(switch1,'no device-location building 1')
SetCmd(switch1,'no known-client 00-77-77-77-77-77')

EnterWirelessMode(switch1)
SetCmd(switch1,'network 777')
SetCmd(switch1,'no igmp snooping m2u')
SetCmd(switch1,'no client-qos access-control down')
SetCmd(switch1,'no client-qos access-control up')
SetCmd(switch1,'no client-qos bandwidth-limit down')
SetCmd(switch1,'no client-qos bandwidth-limit up')
SetCmd(switch1,'no client-qos diffserv-policy down')
SetCmd(switch1,'no client-qos diffserv-policy up')
SetCmd(switch1,'no client-qos enable')

EnterWirelessMode(switch1)
SetCmd(switch1,'network 777')
SetCmd(switch1,'no radius server-name auth')
SetCmd(switch1,'no radius server-name acct')
SetCmd(switch1,'no security mode')
SetCmd(switch1,'no time-limit from 01:30 to 02:30 weekday tuesday')
SetCmd(switch1,'no time-limit-UTC from 2017-02-02 02:30 to 2017-02-02 03:30')

EnterWirelessMode(switch1)
SetCmd(switch1,'network 778')
SetCmd(switch1,'no client-qos access-control down')
SetCmd(switch1,'no client-qos access-control up')

EnterWirelessMode(switch1)
SetCmd(switch1,'network 779')
SetCmd(switch1,'no client-qos access-control down')
SetCmd(switch1,'no client-qos access-control up')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 777')
SetCmd(switch1,'radio 1')
SetCmd(switch1,'no time-limit from 01:30 to 02:30 weekday tuesday')
SetCmd(switch1,'no time-limit-UTC from 2017-02-02 02:30 to 2017-02-02 03:30')

EnterWirelessMode(switch1)
SetCmd(switch1,'no ap database 00-03-0f-77-77-70')
SetCmd(switch1,'no ap profile 777')
SetCmd(switch1,'no wds-group 1')
SetCmd(switch1,'no network 777')
SetCmd(switch1,'no network 778')
SetCmd(switch1,'no network 779')

EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery ip-list 77.77.77.77')
SetCmd(switch1,'no ap client-qos')
SetCmd(switch1,'no igmp snooping')
SetCmd(switch1,'no channel-plan bgn interval')
SetCmd(switch1,'no power-plan interval')

EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'disable')
SetCmd(switch1,'no configuration 7')

EnterConfigMode(switch1)
SetCmd(switch1,'no access-list 1')
SetCmd(switch1,'no access-list 102')
SetCmd(switch1,'no access-list 1103')
SetCmd(switch1,'no access-list 701')

EnterConfigMode(switch1)
SetCmd(switch1,'no ipv6 access-list standard abc')
SetCmd(switch1,'no ipv6 access-list extended aaa')
SetCmd(switch1,'no policy-map policy1')
SetCmd(switch1,'no class-map class1')
SetCmd(switch1,'no aaa group server radius configuration_test_server')
SetCmd(switch1,'no radius-server authentication host 1.2.3.4')
SetCmd(switch1,'no radius-server accounting host 1.2.3.4')

#恢复AC2的配置
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery vlan-list 1')
SetCmd(switch2,'no enable')
IdleAfter(1)
SetCmd(switch2,'enable')
SetCmd(switch2,'no device-location building 1')

EnterWirelessMode(switch2)
SetCmd(switch2,'network 777')
SetCmd(switch2,'no igmp snooping m2u')
SetCmd(switch2,'no client-qos access-control down')
SetCmd(switch2,'no client-qos access-control up')
SetCmd(switch2,'no client-qos bandwidth-limit down')
SetCmd(switch2,'no client-qos bandwidth-limit up')
SetCmd(switch2,'no client-qos diffserv-policy down')
SetCmd(switch2,'no client-qos diffserv-policy up')
SetCmd(switch2,'no client-qos enable')

EnterWirelessMode(switch2)
SetCmd(switch2,'network 777')
SetCmd(switch2,'no radius server-name auth')
SetCmd(switch2,'no radius server-name acct')
SetCmd(switch2,'no security mode')
SetCmd(switch2,'no time-limit from 01:30 to 02:30 weekday tuesday')
SetCmd(switch2,'no time-limit-UTC from 2017-02-02 02:30 to 2017-02-02 03:30')

EnterWirelessMode(switch2)
SetCmd(switch2,'network 778')
SetCmd(switch2,'no client-qos access-control down')
SetCmd(switch2,'no client-qos access-control up')

EnterWirelessMode(switch2)
SetCmd(switch2,'network 779')
SetCmd(switch2,'no client-qos access-control down')
SetCmd(switch2,'no client-qos access-control up')

EnterWirelessMode(switch2)
SetCmd(switch2,'ap profile 777')
SetCmd(switch2,'radio 1')
SetCmd(switch2,'no time-limit from 01:30 to 02:30 weekday tuesday')
SetCmd(switch2,'no time-limit-UTC from 2017-02-02 02:30 to 2017-02-02 03:30')

EnterConfigMode(switch2)
SetCmd(switch2,'no access-list 1')
SetCmd(switch2,'no access-list 102')
SetCmd(switch2,'no access-list 1103')
SetCmd(switch2,'no access-list 701')

EnterWirelessMode(switch2)
SetCmd(switch2,'no ap database 00-03-0f-77-77-70')
SetCmd(switch2,'no ap profile 777')
SetCmd(switch2,'no wds-group 1')
SetCmd(switch2,'no network 777')
SetCmd(switch2,'no network 778')
SetCmd(switch2,'no network 779')

EnterWirelessMode(switch2)
SetCmd(switch2,'no discovery ip-list 77.77.77.77')
SetCmd(switch2,'no ap client-qos')
SetCmd(switch2,'no igmp snooping')
SetCmd(switch2,'no channel-plan bgn interval')
SetCmd(switch2,'no power-plan interval')

EnterConfigMode(switch2)
SetCmd(switch2,'captive-portal')
SetCmd(switch2,'disable')
SetCmd(switch2,'no configuration 7')

EnterWirelessMode(switch2)
SetCmd(switch2,'no discovery ipv6-list 2001:11::100')
SetCmd(switch2,'no discovery ip-list 70.1.11.100')
SetCmd(switch2,'no known-client 00-77-77-77-77-77')

EnterConfigMode(switch2)
SetCmd(switch2,'no ipv6 access-list standard abc')
SetCmd(switch2,'no ipv6 access-list extended aaa')
SetCmd(switch2,'no policy-map policy1')
SetCmd(switch2,'no class-map class1')
SetCmd(switch2,'no aaa group server radius configuration_test_server')
SetCmd(switch2,'no radius-server authentication host 1.2.3.4')
SetCmd(switch2,'no radius-server accounting host 1.2.3.4')

#end
printTimer(testname, 'End')