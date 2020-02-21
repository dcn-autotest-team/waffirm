#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.1.6.py - test case 4.1.6 of waffirm_new
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
# 4.1.6	AP自动部署测试
# 测试目的：测试AP自动部署功能
# 测试环境：同测试拓扑
# 测试描述：AP1初始被AC1管理，通过自动部署，能够使AP1被指定的AC2管理。
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

testname = 'TestCase 4.1.6'
printTimer(testname,'Start','test automatic provision of AP feature of AC')

################################################################################
#Step 1,Step 2
#
#操作
# 在AC1上配置部署AP1的主交换机地址2.2.2.2
# AC1#wireless ap provision <AP1MAC> switch primary 2.2.2.2
# 在AC1上执行wireless ap provision start < AP1MAC >
# AC1#wireless ap provision start <AP1MAC>
#
#预期
#配置成功，AC1上show wireless ap provisioning status显示“AP1MAC”的“Primary”为“2.2.2.2”
#AC1上show wireless ap provisioning status显示“AP1MAC”的“Provisioning Status”为“Success”
################################################################################
printStep(testname,"Step1 step2',\
          'Conifg primary AC to be 2.2.2.2 of AP1 on AC1',\
          'Execute 'wireless ap provision start' on AC1")

res1=res2=1

#operate

#在AC2上开启对AC1,AP1的三层发现
EnterWirelessMode(switch2)
SetCmd(switch2,'discovery ip-list',StaticIpv4_ac1)  

i_times = 0
while i_times < 30:
    data0 = SetCmd(switch1,'show wireless peer-switch')
    if 0 == CheckLine(data0,StaticIpv4_ac2,'IP Poll',IC=True):
        break   
    i_times += 1
    IdleAfter(2)    

#开始部署
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap provision',ap1mac,'switch primary',StaticIpv4_ac2)
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap provision','start',ap1mac)
IdleAfter(30)

data1 = SetCmd(switch2,'show wireless discovery ip-list')
data2 = SetCmd(switch1,'sho wireless ap provisioning status')

#check
res1 = CheckLine(data1,StaticIpv4_ac1)
res2 = CheckLine(data2,ap1mac,StaticIpv4_ac2,'Success',IC=True)
                                
#result
printCheckStep(testname, 'Step1 Step2',res1,res2)

################################################################################
#Step 3
#操作
#重启AP1
#
#预期
# AP1重启后被AC2管理
# AC2上show wi ap status显示AP1的“Status”为“Managed”，“Configuration Status”为“Success”
################################################################################
printStep(testname,'Step 3',\
          'Reboot AP1',\
          'Check if managed by AC2')

res1=res2=1

#operate
RebootAp('AC',AC=switch1,MAC=ap1mac,AP=ap1)
EnterEnableMode(switch2)
for i in range(20):
	data1 = SetCmd(switch2,'show wireless ap status')

#check
	res1 = CheckLine(data1,ap1mac,'Managed','Success',IC=True)
	res2 = CheckNoLineList(data1,[('\*'+ap1mac,'Managed','Success')],IC=True)
	if res1 == 0 and res2 == 0:
		break
	IdleAfter(5)	


#result
printCheckStep(testname, 'Step 3', res1,res2)

################################################################################
#Step 4
#操作
#恢复默认配置
#
################################################################################
printStep(testname,'Step 4',\
          'Recover initial config')

#operate

#AC2关闭对AC1 的发现
EnterWirelessMode(switch2)
SetCmd(switch2,'no','discovery ip-list',StaticIpv4_ac1)

#AP1恢复出厂设置,清除自动部署配置
data0 = SetCmd(ap1,'factory-reset',timeout=2)
SetCmd(ap1,'y',timeout=1)
    
IdleAfter(Ap_reboot_time)

i_times = 0
while i_times < 10:
    data0 = SetCmd(ap1,'\n\n',promoteStop=False,timeout=1)
    if 0 == CheckLine(data0,'login',IC=True):
        SetCmd(ap1,Ap_login_name,promotePatten='Password',promoteTimeout=5)
        SetCmd(ap1,Ap_login_password,timeout=1)  
        break  
    IdleAfter(2)
    i_times += 1
    
#对AP1进行初始配置
SetCmd(ap1,'\n')
SetCmd(ap1,'set management dhcp-status down')
SetCmd(ap1,'set management dhcpv6-status down')
SetCmd(ap1,'set management static-ip',Ap1_ipv4)
SetCmd(ap1,'set management static-ipv6',Ap1_ipv6)
SetCmd(ap1,'set static-ip-route gateway',If_vlan20_s3_ipv4)
SetCmd(ap1,'set static-ipv6-route gateway',If_vlan20_s3_ipv6)
SetCmd(ap1,'set management static-ipv6-prefix-length','64')
SetCmd(ap1,'save-running')

#end
printTimer(testname, 'End')