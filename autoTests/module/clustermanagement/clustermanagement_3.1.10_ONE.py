#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# clustermanagement_3.1.10.py - test case 3.1.10 of clustermanagement
#
# Author:  humj
#
# Version 1.0.0
#
# Date:2018-1-2 08:58:00
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 3.1.10 AC通过vlan list列表进行主动发现AP
# 测试目的：测试AC通过vlan list列表进行主动发现功能是否正常
# 测试环境：同测试拓扑

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase clustermanagement_3.1.10'

avoiderror(testname)
printTimer(testname,'Start','Test AC active discovery AP through vlan list')

################################################################################
#Step 1
#
#操作
# 在没有任何配置的情况下,vlan list二层发现功能是开启的,且默认vlan 1是加入到vlan list中的
#预期
# 缺省情况下会向vlan 1发送二层发现报文,开启debug wireless discovery packet all
# 等待60s在AC1上检测会有如下提示报文:L2 discovery msg sent to vlanid:1
################################################################################

printStep(testname,'Step 1',
          'Check the wireless discovery packet with default config',
          'Check the result')

# operate	  
EnterEnableMode(switch1)
StartDebug(switch1)
SetCmd(switch1,'debug wireless discovery packet all')
IdleAfter(40)
data1 = StopDebug(switch1)
EnterEnableMode(switch1)
SetCmd(switch1,'no debug all')

#check
res1 = CheckLine(data1,'L2 discovery msg sent to vlanid:1',IC=True)
	
#result
printCheckStep(testname, 'Step 1', res1)

################################################################################
#Step 2
#
#操作
# 在vlan list中删除vlan 1
#
#预期
# 等待60s在AC1上不能检测到如下提示报文:L2 discovery msg sent to vlanid:1
################################################################################

printStep(testname,'Step 2',
          'Delete vlan 1 from discovery vlan list',
          'Check the result')

# operate	
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list 1')

EnterEnableMode(switch1)
StartDebug(switch1)
SetCmd(switch1,'debug wireless discovery packet all')
IdleAfter(40)
data1 = StopDebug(switch1)
EnterEnableMode(switch1)
SetCmd(switch1,'no debug all')
#check
res1 = CheckLine(data1,'L2 discovery msg sent to vlanid:1',IC=True)
res1 = 0 if res1 != 0 else 1
	
#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
# 在vlan list中添加一个在AC上不存在的vlan 2
#
#预期
# 等待60s在AC1上不能检测到如下提示报文:L2 discovery msg sent to vlanid:2
################################################################################

printStep(testname,'Step 3',
          'Add a new vlan in discovery vlan lis',
		  'Check the result')		  

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery vlan-list 2')

EnterEnableMode(switch1)
StartDebug(switch1)
SetCmd(switch1,'debug wireless discovery packet all')
IdleAfter(40)
data1 = StopDebug(switch1)
EnterEnableMode(switch1)
SetCmd(switch1,'no debug all')
#check
res1 = CheckLine(data1,'L2 discovery msg sent to vlanid:2',IC=True)
res1 = 0 if res1 != 0 else 1
	
#result
printCheckStep(testname, 'Step 3', res1)

################################################################################
#Step 4
#
#操作
# 在AC1上配置一个vlan 3,这个vlan没有绑定到某个端口,并把这个vlan添加在vlan list中
#
#预期
# 等待60s在AC1上不能检测到如下提示报文:L2 discovery msg sent to vlanid:3
################################################################################

printStep(testname,'Step 4',
          'Add a new vlan in discovery vlan list',
          'Check the result')

# operate
EnterConfigMode(switch1)
SetCmd(switch1,'vlan 3')

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery vlan-list 3')

EnterEnableMode(switch1)
StartDebug(switch1)
SetCmd(switch1,'debug wireless discovery packet all')
IdleAfter(40)
data1 = StopDebug(switch1)
EnterEnableMode(switch1)
SetCmd(switch1,'no debug all')
#check
res1 = CheckLine(data1,'L2 discovery msg sent to vlanid:3',IC=True)
res1 = 0 if res1 != 0 else 1
	
#result
printCheckStep(testname,'Step 4', res1)

################################################################################
#Step 5
#
#操作
#在AC1上把vlan 3绑定到端口
#
#预期
#等待60s在AC1上能检测到如下提示报文:L2 discovery msg sent to vlanid:3
################################################################################

printStep(testname,'Step 5',
          'Bind a new vlan to port on AC1',
          'Check the result')

# operate		
EnterConfigMode(switch1)
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'switchport trunk allowed vlan',Vlan70+';'+Vlan80+';'+'3')

EnterEnableMode(switch1)
StartDebug(switch1)
data1 = SetCmd(switch1,'debug wireless discovery packet all')
IdleAfter(40)
data1 = StopDebug(switch1)
EnterEnableMode(switch1)
SetCmd(switch1,'no debug all')
#check
res1 = CheckLine(data1,'L2 discovery msg sent to vlanid:3',IC=True)
	
#result
printCheckStep(testname,'Step 5', res1)

################################################################################
#Step 6
#
#操作
#在AC1上关闭ip list主动发现功能，将AP1的管理vlan加入到vlan list中
#
#预期
#等待60s,在AC1上能检测到如下提示报文:L2 discovery msg sent to vlanid:vlan70
#等待60s,show wireless ap status在AC1上可以检测到AP1被AC1成功管理AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 6',
          'Add AP1 management vlan to discovery vlan list',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery method ip-poll')
SetCmd(switch1,'discovery vlan-list',Vlan70)

EnterEnableMode(switch1)
StartDebug(switch1)
data1 = SetCmd(switch1,'debug wireless discovery packet all')
IdleAfter(40)
data1 = StopDebug(switch1)
EnterEnableMode(switch1)
SetCmd(switch1,'no debug all')

#check1
res1 = CheckLine(data1,'L2 discovery msg sent to vlanid:'+Vlan70,IC=True)
#check2
IdleAfter(20)
res2 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)
	
#result
printCheckStep(testname, 'Step 6', res1, res2)

################################################################################
#Step 7
#
#操作
#在AC1上关闭vlan list二层主动发现功能
#
#预期
#等待60s在AC1上不能检测到如下提示报文:L2 discovery msg sent to vlanid: vlan70
################################################################################

printStep(testname,'Step 7',
          'Close the method l2-multicast',
          'Check the result')

# operate		  
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery method l2-multicast')

EnterEnableMode(switch1)
StartDebug(switch1)
SetCmd(switch1,'debug wireless discovery packet all')
IdleAfter(40)
data1 = StopDebug(switch1)
EnterEnableMode(switch1)
SetCmd(switch1,'no debug all')
#check1
res1 = CheckLine(data1,'L2 discovery msg sent to vlanid:'+Vlan70,IC=True)
res1 = 0 if res1 != 0 else 1
		
#result
printCheckStep(testname, 'Step 7', res1)

################################################################################
#Step 8
#
#操作
#在AC1上重启无线功能
#
#预期
#重启后AP1无法被AC1管理。show wireless ap status显示No managed APs discovered
################################################################################

printStep(testname,'Step 8',
          'Roboot the wireless',
          'Check the result')

# operate		
EnterWirelessMode(switch1)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
IdleAfter(20)

#check1
res1 = CheckSutCmdWithNoExpect(switch1,'show wireless ap status',
                               check=[(ap1mac,'Managed','Success')],
                               retry=30,interval=5,waitflag=False,IC=True)

data2 = SetCmd(switch1,'show wireless ap status')
#check2
res2 = CheckLine(data2,'No managed APs discovered',IC=True)

#result
printCheckStep(testname, 'Step 8', res1, res2)

################################################################################
#Step 9
#
#操作
#在AC1上开启vlan list二层主动发现功能
#
#预期
#等待60s在AC1上能检测到如下提示报文:L2 discovery msg sent to vlanid: vlan70
#等待60s,show wireless ap status在AC1上可以检测到AP1被AC1成功管理,AP1_MAC的“Status”为“Managed Success”
################################################################################

printStep(testname,'Step 9',
          'Check the AP1 status on AC1 after Open the discovery l2-multicast method',
          'Check the result')

# operate		
EnterEnableMode(switch1)
StartDebug(switch1)
SetCmd(switch1,'debug wireless discovery packet all')

EnterWirelessMode(switch1)
SetCmd(switch1,'discovery method l2-multicast')
IdleAfter(60)
data1 = StopDebug(switch1)
EnterEnableMode(switch1)
SetCmd(switch1,'no debug all')

#check1
res1 = CheckLine(data1,'L2 discovery msg sent to vlanid:'+Vlan70,IC=True)
IdleAfter(20)
#check2
res2 = CheckSutCmd(switch1,'show wireless ap status',
				   check=[(ap1mac,'Managed','Success')],
				   retry=30,interval=5,waitflag=False,IC=True)

#result
printCheckStep(testname, 'Step 9', res1, res2)

################################################################################
#Step 10
#
#操作
#把AP1的管理vlan70从vlan list中删除
#
#预期
#重启后AP1无法被AC1管理。show wireless ap status显示No managed APs discovered
################################################################################

printStep(testname,'Step 10',
          'Delete AP1 management vlan from discovery ip list and reboot the wireless',
          'Check the result')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list',Vlan70)
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')
IdleAfter(60)

#check1
res1 = CheckSutCmdWithNoExpect(switch1,'show wireless ap status',
                               check=[(ap1mac,'Managed','Success')],
                               retry=30,interval=5,waitflag=False,IC=True)
data2 = SetCmd(switch1,'show wireless ap status')
#check2
res2 = CheckLine(data2,'No managed APs discovered',IC=True)

#result
printCheckStep(testname, 'Step 10', res1, res2)

################################################################################
#Step 11
#
#操作
#恢复默认配置
################################################################################

printStep(testname,'Step 11',
          'Recover initial config')

# operate		  
#恢复AC1的配置
EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery vlan-list')
SetCmd(switch1,'discovery vlan-list 1')
SetCmd(switch1,'discovery method l2-multicast')
SetCmd(switch1,'discovery method ip-poll')
SetCmd(switch1,'no enable')
IdleAfter(1)
SetCmd(switch1,'enable')

EnterConfigMode(switch1)
SetCmd(switch1,'no vlan 3')
SetCmd(switch1,'interface',s1p1)
SetCmd(switch1,'switchport trunk allowed vlan',Vlan70+';'+Vlan80)
		  
#end
printTimer(testname, 'End')