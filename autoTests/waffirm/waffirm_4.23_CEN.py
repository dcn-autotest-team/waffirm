#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.23.py - test case 4.23 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Date: 2013-09-23 10:41:12
#
# Copyright (c) 2004-2013 Digital China Networks Co. Ltd
#
# Features:
# 4.23	非抢占模式1+1备份功能测试（pantw）
# 测试目的：测试无线控制器1+1热备份的基本功能。
# 测试环境：同测试拓扑
# 测试描述：AC1与AC2构成备份组。当AC1出现故障，AC2可以代替AC1管理AP。
#         当AP1故障恢复后能够重新管理AP，而AC2恢复为备份设备。要求AC
#         之间发生切换时，数据基本上没有丢失
#
#*******************************************************************************
# Change log:
#     - zhaohj 2014-12-17 根据RDM33466修改
#     - lupingc RDM49074 2017.5.17
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.23'
avoiderror(testname)
printTimer(testname,'Start','1+1 backup,normal mode')

################################################################################
#Step 1
#操作
#ac1上s1p1划为vlan30 修改地址为30.1.1.10
#将无线地址改为30.1.1.10  增加30.1.1.12和30.1.1.11的发现地址
#s2上s2p1划为vlan30  地址30.1.1.12 并设置为无线地址
#增加30.1.1.10的发现列表
#s3上配置s3p1 s3p3为access vlan 30
#ap1地址配置为30.1.1.11
#分别在AC1和AC2配置冗备功能。AC1为master，AC2为backup：
#switch-redundancy master 30.1.1.10 backup 30.1.1.12
#重起ap1 ap2
#
#预期
#通过show wireless switch redundancy status查看冗备配置正确。
################################################################################
printStep(testname,'Step 1',
          'switch-redundancy master 1.1.1.1 backup 1.1.1.2,',
          'show wireless switch redundancy status')

res1=1
#operate
#s1
EnterConfigMode(switch1)
SetCmd(switch1,'vlan 30')
EnterInterfaceMode(switch1,'vlan 30')
SetCmd(switch1,'ip address 30.1.1.10 255.255.255.0')
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport access vlan 30')

EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip 30.1.1.10')
IdleAfter(50)
SetCmd(switch1,'switch-redundancy mode normal')
SetCmd(switch1,'switch-redundancy master 30.1.1.10 backup 30.1.1.12 interval 3000')
#SetCmd(switch1,'no switch-redundancy preempt')  #RDM46287【自动测试项目】【脚本问题】4.23.py非抢占模式功能测试脚本第一步初始化中配置非抢占命令错误
SetCmd(switch1,'discovery ip-list 30.1.1.12')
SetCmd(switch1,'discovery ip-list 30.1.1.11')

#s2
EnterConfigMode(switch2)
SetCmd(switch2,'vlan 30')
EnterInterfaceMode(switch2,'vlan 30')
SetCmd(switch2,'ip address 30.1.1.12 255.255.255.0')
EnterInterfaceMode(switch2,s2p1)
SetCmd(switch2,'switchport access vlan 30')
EnterWirelessMode(switch2)
SetCmd(switch2,'static-ip 30.1.1.12')
IdleAfter(50)
SetCmd(switch2,'switch-redundancy mode normal')
SetCmd(switch2,'switch-redundancy master 30.1.1.10 backup 30.1.1.12 interval 3000')
#SetCmd(switch2,'no switch-redundancy preempt')#RDM46287【自动测试项目】【脚本问题】4.23.py非抢占模式功能测试脚本第一步初始化中配置非抢占命令错误
SetCmd(switch2,'discovery ip-list 30.1.1.10')

#s3
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport access vlan 30')
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'switchport access vlan 30')

#ap1
SetCmd(ap1,'set management static-ip 30.1.1.11')
SetCmd(ap1,'save-running')

#wait for cluster created
# IdleAfter(120)
RebootMulitAp(AP=[ap1,ap2])
IdleAfter(60)
data1 = SetCmd(switch1,'show wireless switch redundancy status',timeout=3)
res1 = CheckLineList(data1,[('30.1.1.10\(Active\)')],IC=True)
data1 = SetCmd(switch2,'show wireless switch redundancy status',timeout=3)
res2 = CheckLineList(data1,[('30.1.1.10\(Active\)')],IC=True)
#config push
EnterEnableMode(switch1)
SetCmd(switch1,'write',timeout=1)
SetCmd(switch1,'y',timeout=1)

#check

#result
printCheckStep(testname, 'Step 1',res1,res2)

################################################################################
#Step 2
#操作
#STA1关联到网络test1。
#
#预期
#STA1关联成功，获取192.168.91.X网段的IP地址。
#s1\s2上分别show wireless l2tunnel tunnel-list获取状态分别为Active和Standby
################################################################################
printStep(testname,'Step 2',
          'STA1 connect to network 1,',
          'STA1 dhcp and get 192.168.91.X ip address.')

res1=res2=1
#operate
sta1_ipv4 = ''

#STA1 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
IdleAfter(10)

#获取STA1地址
sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
res2 = sta1_ipresult['res']

data3 = SetCmd(switch1,'show wireless l2tunnel tunnel-list')
data4 = SetCmd(switch2,'show wireless l2tunnel tunnel-list')
if re.search('Active',data3) is not None:
    res3 = 0
else:
    res3 = 1
if re.search('Standby',data4) is not None:
    res4 = 0
else:
    res4 = 1    
             
#result
printCheckStep(testname,'Step 2',res1,res2,res3,res4)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 3
    #操作
    #STA1 ping ac1网关
    #
    #预期
    #可以ping通
    ################################################################################
    printStep(testname,'Step 3',
              'Sta1 ping ac1 gateway')

    res1 = CheckPing(sta1,If_vlan4091_s1_ipv4,mode='linux')

    #result
    printCheckStep(testname, 'Step 3',res1)

    ################################################################################
    #Step 4
    #操作
    #断开AC1和S3的网络连接，
    #
    #预期
    #AC1和AC2之间发生主备切换。AC2成为master。通过show wireless switch redundancy status查看冗备状态正确。
    #sta1 ping ac1网关地址可以ping通
    ################################################################################
    printStep(testname,'Step 4',
              'Disconnect connection between ac1 and s3')
    res1=res2=1          
    EnterInterfaceMode(switch1,s1p1)
    SetCmd(switch1,'shutdown')
    #check
    IdleAfter(30)
    for i in range(14):
        data5 = SetCmd(switch2,'show wireless switch redundancy status')
        if re.search('30.1.1.12\(Active\)',data5) is not None:
            res2 = 0
        if res2 == 0:
            break
        else:
            IdleAfter(5)

    for i in range(14):		
        res1 = CheckPing(sta1,If_vlan4091_s2_ipv4,mode='linux')
        if res1 == 0:
            break
        else:
            IdleAfter(5)
    #result
    printCheckStep(testname, 'Step 4',res1,res2)
    ################################################################################
    #Step 5
    #操作
    #在S2上面查看AP和Client相关的信息。
    #
    #预期
    #AP1关联在AC2。STA1关联状态正常
    ################################################################################
    printStep(testname,'Step 5',
              'Check ap and client info on s2')
              
    #operate

    data1 = SetCmd(switch2,'show wireless ap status',timeout=5)
    res1 = CheckLineList(data1,[(re.sub(':','-',ap1mac),'Success')],IC=True)

    data1 = SetCmd(switch2,'show wireless client status',timeout=5)
    res2 = CheckLineList(data1,[(re.sub(':','-',sta1mac))],IC=True)

    #check

    #result
    printCheckStep(testname, 'Step 5',res1,res2)
    ################################################################################
    #Step 6
    #操作
    #AC1恢复和S3的网络连接，等待3分钟。
    #
    #预期
    #AC1和AC2没有发生主备切换。AC2仍然为master。通过show wireless switch redundancy status查看冗备配置正确。
    #STA 1 ping ac2网关可ping通
    ################################################################################
    printStep(testname,'Step 6',
              'Reconnect ac1 and s3')
    res1=res2=res3=1           
    EnterInterfaceMode(switch1,s1p1)
    SetCmd(switch1,'no shutdown',promotePatten='administratively',promoteTimeout=380)
    IdleAfter(30)
    for i in range(14):
        data5 = SetCmd(switch1,'show wireless switch redundancy status')
        if re.search('30.1.1.10\(Standby\)',data5) is not None:
            res2 = 0
        data6 = SetCmd(switch2,'show wireless switch redundancy status')
        if re.search('30.1.1.12\(Active\)',data6) is not None:
            res3 = 0
        if res2 == 0 and res3 == 0:
            break
        else:
            IdleAfter(5)

    for i in range(14):		
        res1 = CheckPing(sta1,If_vlan4091_s2_ipv4,mode='linux')
        if res1 == 0:
            break
        else:
            IdleAfter(5)
    #check

    #result
    printCheckStep(testname, 'Step 6',res1,res2,res3)
    ################################################################################
    #Step 7
    #操作
    #在AC2上面查看AP和Client相关的信息。
    #
    #预期
    #AP1关联在AC2。STA1关联状态正常
    ################################################################################
    printStep(testname,'Step 7',
              'Check client info on ac2')
              
    data1 = SetCmd(switch2,'show wireless ap status',timeout=5)
    res1 = CheckLineList(data1,[(re.sub(':','-',ap1mac),'Success')],IC=True)

    data1 = SetCmd(switch2,'show wireless client status',timeout=5)
    res2 = CheckLineList(data1,[(re.sub(':','-',sta1mac))],IC=True)

    #check

    #result
    printCheckStep(testname, 'Step 7',res1,res2)

    ################################################################################
    #Step 8
    #操作
    #断开AC2和S3的网络连接，
    #
    #预期
    #AC1和AC2之间发生主备切换。AC1成为master。通过show wireless switch redundancy status查看冗备状态正确。
    #STA 1 可以ping通ac1网关
    ################################################################################
    printStep(testname,'Step 8',
              'Disconnect connection between ac1 and s3')
    res1=res2=res3=1           
    EnterInterfaceMode(switch2,s2p1)
    SetCmd(switch2,'shutdown')
    IdleAfter(30)
    for i in range(14):
        data5 = SetCmd(switch1,'show wireless switch redundancy status')
        if re.search('30.1.1.10\(Active\)',data5) is not None:
            res2 = 0
        data3 = SetCmd(switch1,'show wireless l2tunnel tunnel-list')
        if re.search('Active',data3) is not None:
            res3 = 0
        if res2 == 0 and res3 == 0:
            break
        else:
            IdleAfter(5)
    for i in range(14):		
        res1 = CheckPing(sta1,pc1_ipv4,mode='linux')
        if res1 == 0:
            break
        else:
            IdleAfter(5)	
    #check

    #result
    printCheckStep(testname, 'Step 8',res1,res2,res3)

    ################################################################################
    #Step 9
    #操作
    #AC2恢复和S3的网络连接，等待3分钟。
    #
    #预期
    #AC1和AC2没有发生主备切换。AC1仍然为master。通过show wireless switch redundancy status查看冗备配置正确。
    #STA 1 可以ping通ac1网关
    ################################################################################
    printStep(testname,'Step 9',
              'Reconnect ac1 and s3')
    res1=res2=res3=1          
    EnterInterfaceMode(switch2,s2p1)
    SetCmd(switch2,'no shutdown',promotePatten='administratively',promoteTimeout=380)
    IdleAfter(120)
    for i in range(20):
        data5 = SetCmd(switch1,'show wireless switch redundancy status')
        if re.search('30.1.1.10\(Active\)',data5) is not None:
            res2 = 0
        data6 = SetCmd(switch2,'show wireless switch redundancy status')
        if re.search('30.1.1.12\(Standby\)',data6) is not None:
            res3 = 0
        if res2 == 0 and res3 == 0:
            break
        else:
            IdleAfter(5)
    for i in range(14):		
        res1 = CheckPing(sta1,If_vlan4091_s1_ipv4,mode='linux')
        if res1 == 0:
            break
        else:
            IdleAfter(5)
    #check

    #result
    printCheckStep(testname, 'Step 9',res1,res2,res3)
    ################################################################################
    #Step 10
    #操作
    #在AC1上面查看AP和Client相关的信息。
    #
    #预期
    #AP1关联在AC1。STA1关联状态正常
    ################################################################################
    printStep(testname,'Step 10',
              'Check client info on ac1')
              
    data1 = SetCmd(switch1,'show wireless ap status')
    res1 = CheckLineList(data1,[(re.sub(':','-',ap1mac),'Success')],IC=True)

    data1 = SetCmd(switch1,'show wireless client status')
    res2 = CheckLineList(data1,[(re.sub(':','-',sta1mac))],IC=True)

    #check

    #result
    printCheckStep(testname, 'Step 10',res1,res2)

################################################################################
#Step 11
#操作
#恢复默认配置
#两ap 恢复出厂设置
################################################################################
printStep(testname,'Step 11',
          'Recover initial config for switches.')

#operate
##解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

EnterWirelessMode(switch1)
SetCmd(switch1,'no switch-redundancy ')
SetCmd(switch1,'switch-redundancy mode preempt')
SetCmd(switch1,'static-ip',StaticIpv4_ac1)
EnterWirelessMode(switch2)
SetCmd(switch2,'no switch-redundancy ')
SetCmd(switch2,'switch-redundancy mode preempt')
SetCmd(switch2,'static-ip',StaticIpv4_ac2)

SetCmd(switch1,'no discovery ip-list ' + StaticIpv4_ac2)
SetCmd(switch2,'no discovery ip-list ' + StaticIpv4_ac1)
SetCmd(switch1,'no discovery ip-list 30.1.1.12')
SetCmd(switch1,'no discovery ip-list 30.1.1.11')

EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan 30')
SetCmd(switch1,'no vlan 30')
EnterInterfaceMode(switch1,'vlan 40')
IdleAfter(Vlan_Idle_time)
SetCmd(switch1,'ip address ' + If_vlan40_s1_ipv4 + ' 255.255.255.0')
SetCmd(switch1,'ipv6 address ' + If_vlan40_s1_ipv6 + '/64')

EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport access vlan 40')

EnterConfigMode(switch2)
SetCmd(switch2,'vlan ' + Vlan30 + ';' + Vlan4091 + '-' + Vlan4093)
EnterInterfaceMode(switch2,'vlan 30')
IdleAfter(Vlan_Idle_time)
SetCmd(switch2,'ip address ' + If_vlan30_s2_ipv4 + ' 255.255.255.0')
SetCmd(switch2,'ipv6 address ' + If_vlan30_s2_ipv6 + '/64')
#RDM37511
EnterWirelessMode(switch2)
SetCmd(switch2,'peer-group 2')
IdleAfter(5)
SetCmd(switch2,'peer-group 1')

#vlan20
EnterConfigMode(switch3)
SetCmd(switch3,'vlan',Vlan20)
SetCmd(switch3,'switchport interface',s3p3)
EnterInterfaceMode(switch3,'vlan '+Vlan20)
IdleAfter(Vlan_Idle_time)
SetIpAddress(switch3,If_vlan20_s3_ipv4,'255.255.255.0')
SetCmd(switch3,'ipv6 address',If_vlan20_s3_ipv6 + '/64')

#vlan30
EnterConfigMode(switch3)
SetCmd(switch3,'vlan',Vlan30)
SetCmd(switch3,'switchport interface',s3p2)
SetCmd(switch3,'switchport interface',s3p4)
EnterInterfaceMode(switch3,'vlan '+Vlan30)
IdleAfter(Vlan_Idle_time)
SetIpAddress(switch3,If_vlan30_s3_ipv4,'255.255.255.0')
SetCmd(switch3,'ipv6 address',If_vlan30_s3_ipv6 + '/64')

#vlan40
EnterConfigMode(switch3)
SetCmd(switch3,'vlan',Vlan40)
SetCmd(switch3,'switchport interface',s3p1)
EnterInterfaceMode(switch3,'vlan '+Vlan40)
IdleAfter(Vlan_Idle_time)
SetIpAddress(switch3,If_vlan40_s3_ipv4,'255.255.255.0')
SetCmd(switch3,'ipv6 address',If_vlan40_s3_ipv6 + '/64')

FactoryResetMultiAp([ap1,ap2])
ApLogin(ap1,retry=10)
ApLogin(ap2,retry=10)
#---------------------------  初始化AP1  ---------------------------------------
SetCmd(ap1,'\n')
SetCmd(ap1,'set management static-ip',Ap1_ipv4)
SetCmd(ap1,'set management static-ipv6',Ap1_ipv6)
SetCmd(ap1,'set management dhcp-status down')
SetCmd(ap1,'set management dhcpv6-status down')
SetCmd(ap1,'set static-ip-route gateway',If_vlan20_s3_ipv4)
SetCmd(ap1,'set static-ipv6-route gateway',If_vlan20_s3_ipv6)
SetCmd(ap1,'set management static-ipv6-prefix-length','64')
SetCmd(ap1,'save-running')

#---------------------------  初始化AP2  ---------------------------------------
SetCmd(ap2,'\n')
SetCmd(ap2,'set management static-ip',Ap2_ipv4)
SetCmd(ap2,'set management static-ipv6',Ap2_ipv6)
SetCmd(ap2,'set management dhcp-status down')
SetCmd(ap2,'set management dhcpv6-status down')
SetCmd(ap2,'set static-ip-route gateway',If_vlan30_s3_ipv4)
SetCmd(ap2,'set static-ipv6-route gateway',If_vlan30_s3_ipv6)
SetCmd(ap2,'set management static-ipv6-prefix-length','64')
SetCmd(ap2,'save-running')
EnterWirelessMode(switch2)
SetCmd(switch2,'peer-group 2')
IdleAfter(3)
SetCmd(switch2,'peer-group 1')
#下发配置
EnterEnableMode(switch1)
data0 = SetCmd(switch1,'wireless ap profile apply 1',timeout=1)
SetCmd(switch1,'y',timeout=1)
IdleAfter(Ac_ap_syn_time)
  
#end
printTimer(testname, 'End')