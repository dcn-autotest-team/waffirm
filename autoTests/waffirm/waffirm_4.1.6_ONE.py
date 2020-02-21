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
#     - lupingc RDM49074 2017.5.17
#     - zhangjxp 2017.11.10 RDM50304 修改step3
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.1.6'
avoiderror(testname)
printTimer(testname,'Start','test automatic provision of AP feature of AC')

################################################################################
#Step 1,Step 2
#
#操作
# 在AC1上配置部署AP1的主交换机地址2.2.2.2
# AC1#wireless ap provision <AP1MAC> switch primary 2.2.2.2
# 在AC1上执行wireless ap provision start < AP1MAC >
# AC1#wireless ap provision start <AP1MAC>
# 等待30S
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
EnterEnableMode(switch1)
CheckSutCmd(switch1,'show wireless peer-switch',
            check=[(StaticIpv4_ac2,'IP Poll')],
            waittime=5,retry=20,interval=5,IC=True)
   
#开始部署
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap provision',ap1mac,'switch primary',StaticIpv4_ac2)
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap provision','start',ap1mac)
IdleAfter(30)

data1 = SetCmd(switch2,'show wireless discovery ip-list',timeout=5)
data2 = SetCmd(switch1,'sho wireless ap provisioning status',timeout=5)

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
printStep(testname,'Step 3',
          'Reboot AP1',
          'Check if managed by AC2')

res1=res2=1

#operate
SetCmd(switch1,'config')
SetCmd(switch1,'wireless ')
SetCmd(switch1,'no discovery ip-list ',Ap1_ipv4)  #RDM46881,删除掉命令“discovery ip-list AP1IP”
SetCmd(switch1,'end')
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap1,ap1mac,switch1,Ap1cmdtype)
IdleAfter(20)
EnterEnableMode(switch2)
res1=CheckSutCmd(switch2,'show wireless ap status',
                 check=[(ap1mac,'Managed','Success')],
                 waittime=5,retry=20,interval=5,IC=True)
            
data1 = SetCmd(switch2,'show wireless ap status')
res2 = CheckNoLineList(data1,[('\*'+ap1mac,'Managed','Success')],IC=True)

SetCmd(ap1,'get map-ap-provisioning')

#result
printCheckStep(testname, 'Step 3', res1,res2)

################################################################################
#Step 4
#操作
#恢复默认配置
#
################################################################################
printStep(testname,'Step 4',
          'Recover initial config')

#operate

#!!!!!!!!!!!!!!!!!!!!!!!!!!!
#注：此处必须对AP进行 factory reset 操作，不然自动部署的配置会保留在AP内，无法清除
#以后的发现方式都会采用自动部署，而不是二层三层发现

#修改primary
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap provision',ap1mac,'switch primary',StaticIpv4_ac1)
SetCmd(switch1,'wireless ap provision','start',ap1mac)

CheckSutCmd(switch1,'sho wireless ap provisioning status',
            check=[(ap1mac,StaticIpv4_ac1,'Success')],
            waittime=10,retry=10,interval=1,IC=True)
 
#重启AP1,使AC1成为AP1的primary AC 
SetCmd(switch1,'config')
SetCmd(switch1,'wireless')
SetCmd(switch1,'discovery ip-list ',Ap1_ipv4)

RebootAp('AP',AP=ap1)

#AC2关闭对AC1 的发现
EnterWirelessMode(switch2)
SetCmd(switch2,'no','discovery ip-list',StaticIpv4_ac1)

#AP1恢复出厂设置,清除自动部署配置

FactoryResetMultiAp([ap1])
ApLogin(ap1,retry=5)
# i_times = 0
# while i_times < 5:
    # data0 = SetCmd(ap1,'\n\n',promoteStop=False,timeout=1)
    # if 0 == CheckLine(data0,'login',IC=True):
        # SetCmd(ap1,Ap_login_name,promotePatten='Password',promoteTimeout=5)
        # SetCmd(ap1,Ap_login_password,timeout=1)  
        # break  
    # IdleAfter(2)
    # i_times += 1
    
#对AP1进行初始配置
SetCmd(ap1,'\n')
# SetCmd(ap1,'set management dhcp-status down')
# SetCmd(ap1,'set management dhcpv6-status down')
# SetCmd(ap1,'set management static-ip',Ap1_ipv4)
# SetCmd(ap1,'set management static-ipv6',Ap1_ipv6)
# SetCmd(ap1,'set static-ip-route gateway',If_vlan20_s3_ipv4)
# SetCmd(ap1,'set static-ipv6-route gateway',If_vlan20_s3_ipv6)
# SetCmd(ap1,'set management static-ipv6-prefix-length','64')
# SetCmd(ap1,'save-running')
ApSetcmd(ap1,Ap1cmdtype,'set_static_ip',Ap1_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6',Ap1_ipv6)
ApSetcmd(ap1,Ap1cmdtype,'set_dhcp_down')
ApSetcmd(ap1,Ap1cmdtype,'set_dhcpv6_down')
ApSetcmd(ap1,Ap1cmdtype,'set_ip_route',If_vlan20_s3_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'set_ipv6_route',If_vlan20_s3_ipv6)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ipv6_prefix_len','64')
ApSetcmd(ap1,Ap1cmdtype,'saverunning')

#end
printTimer(testname, 'End')