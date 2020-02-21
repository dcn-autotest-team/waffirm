#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.21.py - test case 3.1.21 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-9 17:35:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.21 AP Pass-Phrase认证功能
# 测试目的：测试AP Pass-Phrase认证功能是否正确
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.21'

avoiderror(testname)
printTimer(testname,'Start','Test Pass-Phrase authentication of AP')

################################################################################
#Step 1
#
#操作
#在AC1的vlan-list发现列表中加入AP1的管理vlan vlan70
#在AC1上把AP反制功能关掉
#
#预期
#show wi ap status在AC1上可以检测到AP1和AP2被AC1成功管理
#AP1_MAC的“Status”为“Managed Success”
#AP2_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 1',
          'Add management vlan to discovery vlan list on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery vlan-list',Vlan70)
SetCmd(switch1,'no wireless ap anti-flood')

IdleAfter(20)
#check1
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success'),
				   (ap2mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
#在AC1上把AP1的MAC从ap database中删除，修改认证方式为pass-phrase，本地认证
#
#预期
#由于本地ap database表中没有AP1 MAC对应的表项，AP1在AC1上认证失败
#在AC1上show wireless ap failure status能看到:
#MAC地址为AP1_MAC,“Last Failure Type”显示为”No Database Entry”
################################################################################

printStep(testname,'Step 2',
          'Change ap authentication pass-phrase'
          'and validation local after delete AP1 mac',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no ap database',ap1mac)
SetCmd(switch1,'ap authentication pass-phrase')
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
	
IdleAfter(20)	
#check
res1 = CheckSutCmd(switch1,'show wireless ap failure status',
				   check=[(ap1mac,'No Database Entry')],
				   retry=30,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
#在AC1上添加AP1的MAC到ap database表项中,AP1和AC1的密码都为空
#在AC1上AP认证debug
#在AC1上重启无线功能
#
#预期
#AP1能成功被AC管理，show wi ap status在AC1上可以检测到AP1被AC1成功管理
#AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 3',
          'Add AP1 MAC to ap database',
		  'Check the result')		  

# operate	
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'exit')
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(20)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
				   
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
#在AP1上设置AP1的密码并保存配置，AC1上不设置密码
#在AC1上重启无线功能
#
#预期
#AP1在AC1上认证失败,在AC1上show wireless ap failure status能看到:
#MAC地址为AP1_MAC, “Last Failure Type”显示为” Local Authentication”
################################################################################

printStep(testname,'Step 4',
          'Set password on AP1',
          'Check the result')

# operate
SetCmd(ap1,'set managed-ap mode down')
SetCmd(ap1,'set managed-ap pass-phrase 123456789')
SetCmd(ap1,'set managed-ap mode up')
ApSetcmd(ap1,Ap1cmdtype,'saverunning')  
  
EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
	
IdleAfter(20)
#check
res1 = CheckSutCmd(switch1,'show wireless ap failure status',
				   check=[(ap1mac,'Local Authentication')],
				   retry=30,interval=5,waitflag=False,IC=True)	
				   
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#在AC1上设置密码和AP1上一致
#在AC1上重启无线功能
#
#预期
#AP1能成功被AC管理,show wi ap status在AC1上可以检测到AP1被AC1成功管理
#AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 5',
          'Set password the same as AP1 on AC1',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'password plain 123456789')

EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(20)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)	
	
#result
printCheckStep(testname,'Step 5', res1)

################################################################################
#Step 6
#
#操作
#在AC1上设置密码和AP1上不一致
#在AC1上重启无线功能
#
#预期
#AP1在AC1上认证失败,在AC1上show wireless ap failure status能看到:
#MAC地址为AP1_MAC, “Last Failure Type”显示为” Local Authentication”
################################################################################

printStep(testname,'Step 6',
          'Set password different from AP1 on AC1',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'password plain 12345678')

EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(20)
#check
res1 = CheckSutCmd(switch1,'show wireless ap failure status',
				   check=[(ap1mac,'Local Authentication')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 6', res1)

################################################################################
#Step 7
#
#操作
#在S3上配置用户vlan80和管理VLAN 70对应的IP地址
#在AC1上修改认证方式为pass-phrase，radius认证
#在AC1上配置radius相关配置
#在AC1上创建network 111绑定到ap profile 11的radio 1中,其中radius给AP下发的配置profile id为11
#
#预期
#AP1在AC1上认证失败,在AC1上show wireless ap failure status能看到:
#MAC地址为AP1_MAC, “Last Failure Type”显示为” RADIUS Authentication”
################################################################################

printStep(testname,'Step 7',
          'Change ap authentication pass-phrase and validation'
		  'radius after set AP1 password different from radius',
          'Check the result')

# operate		  
EnterConfigMode(switch3)
SetCmd(switch3,'interface vlan',Vlan80)
SetCmd(switch3,'ip address',If_vlan80_s3_ipv4)
EnterConfigMode(switch3)
SetCmd(switch3,'interface vlan',Vlan70)
SetCmd(switch3,'ip address',If_vlan70_s3_ipv4)

EnterWirelessMode(switch1)
SetCmd(switch1,'ap validation radius')
SetCmd(switch1,'radius server-name auth',radius_server_name)

EnterConfigMode(switch1)
SetCmd(switch1,'aaa group server radius',radius_server_name)
SetCmd(switch1,'server',radius_server_ipv4)

EnterConfigMode(switch1)
SetCmd(switch1,'radius-server key 0',radius_password)
SetCmd(switch1,'radius-server authentication host',radius_server_ipv4)
SetCmd(switch1,'radius-server accounting host',radius_server_ipv4)
SetCmd(switch1,'aaa-accounting enable')
SetCmd(switch1,'aaa enable')
SetCmd(switch1,'radius nas-ipv4',If_vlan70_s1_ipv4_s)
SetCmd(switch1,'radius source-ipv4',If_vlan70_s1_ipv4_s)

EnterWirelessMode(switch1)
SetCmd(switch1,'network 111')
SetCmd(switch1,'ssid 111')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 11')
SetCmd(switch1,'radio 1')
IdleAfter(1)
SetCmd(switch1,'enable')
SetCmd(switch1,'vap 0')
SetCmd(switch1,'network 111')
IdleAfter(1)
SetCmd(switch1,'enable')

SetCmd(ap1,'set managed-ap mode down')
SetCmd(ap1,'set managed-ap pass-phrase 12345678')
SetCmd(ap1,'set managed-ap mode up')
ApSetcmd(ap1,Ap1cmdtype,'saverunning')  

EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(20)
#check
res1 = CheckSutCmd(switch1,'show wireless ap failure status',
				   check=[(ap1mac,'RADIUS Authentication')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 7', res1)

################################################################################
#Step 8
#
#操作
#在AP1上配置密码和radius服务器上相同
#在AC1上重启无线功能
#
#预期
#AP1能成功被AC管理,show wi ap status在AC1上可以检测到AP1被AC1成功管理
#AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 8',
          'Set AP1 password same as radius',
          'Check the result')

# operate		  
SetCmd(ap1,'set managed-ap mode down')
SetCmd(ap1,'set managed-ap pass-phrase 123456789')
SetCmd(ap1,'set managed-ap mode up')
ApSetcmd(ap1,Ap1cmdtype,'saverunning')  

EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(20)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   waittime=5,retry=15,interval=5,IC=True)	

#result
printCheckStep(testname,'Step 8', res1)

################################################################################
#Step 9
#
#操作
#在AP1上配置密码为空
#
#预期
#AP1在AC1上认证失败,在AC1上show wireless ap failure status能看到:
#MAC地址为AP1_MAC, “Last Failure Type”显示为” RADIUS Authentication”
################################################################################

printStep(testname,'Step 9',
          'Delete the AP1 password',
          'Check the result')

# operate
RebootAp(setdefaut=True, AP=ap1,connectTime=1)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ip',Ap1_ipv4) 
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6',Ap1_ipv6) 
ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_down') 
ApSetcmd(ap1,Ap1cmdtype,'set_dhcpv6_down') 
ApSetcmd(ap1,Ap1cmdtype,'set_ip_route',If_vlan70_s3_ipv4_s) 
ApSetcmd(ap1,Ap1cmdtype,'set_ipv6_route',If_vlan70_s3_ipv6_s) 
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6_prefix_len','64') 
ApSetcmd(ap1,Ap1cmdtype,'saverunning') 

IdleAfter(30)
#check
res1 = CheckSutCmd(switch1,'show wireless ap failure status',
				   check=[(ap1mac,'Invalid Profile ID')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 9', res1)

################################################################################
#Step 10
#
#操作
#在AP1上配置密码和radius服务器上相同
#在AC1上删除profile 11
#在AC1上重启无线功能
#
#预期
#AP1在AC1上认证失败,在AC1上show wireless ap failure status能看到:
#MAC地址为AP1_MAC,“Last Failure Type”显示为” Invalid Profile ID”
################################################################################

printStep(testname,'Step 10',
          'Set password same as radius on AP1'
		  'and delete the profile id on AC1',
          'Check the result')

# operate
SetCmd(ap1,'set managed-ap mode down')
SetCmd(ap1,'set managed-ap pass-phrase 123456789')
SetCmd(ap1,'set managed-ap mode up')
ApSetcmd(ap1,Ap1cmdtype,'saverunning')  

EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(20)
#check
res1 = CheckSutCmd(switch1,'show wireless ap failure status',
				   check=[(ap1mac,'Invalid Profile ID')],
				   retry=30,interval=5,waitflag=False,IC=True)	

#result
printCheckStep(testname,'Step 10', res1)

################################################################################
#Step 11
#
#操作
#在AC1上添加profile 11
#在AC1上重启无线功能
#
#预期
#AP1能成功被AC管理,show wi ap status在AC1上可以检测到AP1被AC1成功管理
#AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 11',
          'Add the profile id on AC1',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 11')
SetCmd(switch1,'radio 1')
IdleAfter(1)
SetCmd(switch1,'enable')
SetCmd(switch1,'vap 0')
SetCmd(switch1,'network 111')
SetCmd(switch1,'enable')	  
		  
EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

IdleAfter(20)
#check
res1 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   waittime=5,retry=15,interval=5,IC=True)	

#result
printCheckStep(testname,'Step 11', res1)

################################################################################
#Step 12
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 12',
          'Recover initial config')

# operate		  
#恢复AC1的配置
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list',Vlan70)
SetCmd(switch1,'wireless ap anti-flood')
SetCmd(switch1,'no radius server-name auth')
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap authentication none')
SetCmd(switch1,'ap validation local')
SetCmd(switch1,'no ap profile 11')
SetCmd(switch1,'no network 111')

EnterConfigMode(switch1)
SetCmd(switch1,'no aaa group server radius',radius_server_name)
SetCmd(switch1,'no radius nas-ipv4')
SetCmd(switch1,'no aaa enable')
SetCmd(switch1,'no aaa-accounting enable')
SetCmd(switch1,'no radius source-ipv4')

EnterConfigMode(switch1)
SetCmd(switch1,'no radius-server authentication host',radius_server_ipv4)
SetCmd(switch1,'no radius-server accounting host',radius_server_ipv4)
SetCmd(switch1,'no radius-server key')

#恢复AP1的配置
RebootAp(setdefaut=True, AP=ap1,connectTime=1)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ip',Ap1_ipv4) 
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6',Ap1_ipv6) 
ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_down') 
ApSetcmd(ap1,Ap1cmdtype,'set_dhcpv6_down') 
ApSetcmd(ap1,Ap1cmdtype,'set_ip_route',If_vlan70_s3_ipv4_s) 
ApSetcmd(ap1,Ap1cmdtype,'set_ipv6_route',If_vlan70_s3_ipv6_s) 
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6_prefix_len','64') 
ApSetcmd(ap1,Ap1cmdtype,'saverunning') 

#配置AC1的database
EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap1mac)
SetCmd(switch1,'no passsword')
SetCmd(switch1,'profile 1')

EnterWirelessMode(switch1)
SetCmd(switch1,'ap database',ap2mac)
SetCmd(switch1,'profile 2')

#恢复S3的配置
EnterConfigMode(switch3)
SetCmd(switch3,'no interface vlan',Vlan80)
SetCmd(switch3,'no interface vlan',Vlan70)

#end
printTimer(testname, 'End')