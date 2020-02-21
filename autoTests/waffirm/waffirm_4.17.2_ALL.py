#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.17.2.py - test case 4.17.2 of waffirm
#
# Author:  qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2013 Digital China Networks Co. Ltd
#
# Features:
# 4.17.2 PPPoE Server-CHAP认证
# 测试目的：测试客户端通过pppoe的PAP模式接入无线网络。
# 测试环境：同测试拓扑
# 测试描述：测试客户端通过pppoe的PAP模式接入无线网络。
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
if ac1type != '508':
    testname = 'TestCase 4.17.2'
    avoiderror(testname)
    printTimer(testname,'Start','Test PPPoE server-CHAP')

    ################################################################################
    #Step 1
    #操作
    #配置AC的radius相关配置
    #radius source-ipv4 1.1.1.1
    #radius-server key 0 test
    #radius-server authentication host 192.168.10.2
    #radius-server accounting host 192.168.10.2
    #aaa-accounting enable
    #aaa enable
    #radius nas-ipv4 1.1.1.1
    #radius nas-ipv6 2001::1
    #aaa group server radius wlan
    #server 192.168.10.2
    #配置成功。在AC上面show running-config可以看到相关的配置。
    ################################################################################
    printStep(testname,'Step 1',
              'Config radius server')
    #operate
    EnterConfigMode(switch1)
    SetCmd(switch1,'radius source-ipv4 ' + StaticIpv4_ac1)
    SetCmd(switch1,'radius-server key test')
    SetCmd(switch1,'radius-server authentication host ' + Radius_server)
    SetCmd(switch1,'radius-server accounting host ' + Radius_server)
    SetCmd(switch1,'radius nas-ipv4 ' + StaticIpv4_ac1)
    SetCmd(switch1,'aaa group server radius wlan')
    SetCmd(switch1,'server ' + Radius_server)
    EnterConfigMode(switch1)
    SetCmd(switch1,'aaa enable')
    SetCmd(switch1,'aaa-accounting enable')

    # 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
    if testcentral:
        pass
    else:
        ###地址池原本在S3上，本测试例需要在AC1 以PPPoE方式的虚拟interface，需清除S3的dhcp配置
        EnterConfigMode(switch1)
        SetCmd(switch1,'service dhcp')

        SetCmd(switch1,'vlan',Vlan4091)
        EnterInterfaceMode(switch1,'vlan '+Vlan4091)
        IdleAfter(Vlan_Idle_time)
        SetCmd(switch1,'ip address ' + If_vlan4091_s1_ipv4 + ' 255.255.255.0')

        #配置s1p1为trunk口
        EnterInterfaceMode(switch1,s1p1)
        SetCmd(switch1,'switchport mode trunk') 
         
        #S3 清除dhcp server配置，配置ethernet 1/1、1/2为trunk口
        EnterConfigMode(switch3)
        SetCmd(switch3,'no service dhcp')
        EnterInterfaceMode(switch3,s3p1)
        SetCmd(switch3,'switchport mode trunk') 
        SetCmd(switch3,'switchport trunk native vlan','1')
        EnterConfigMode(switch3)
        SetCmd(switch3,'no interface vlan',Vlan4091) 
    #check
    # data1 = ShowRun(switch1)
    data1 = SetCmd(switch1,'show run',timeout=20)
    res1 = CheckLineList(data1,['radius source-ipv4 ' + StaticIpv4_ac1,'radius-server key 0 test','radius-server authentication host ' + Radius_server,
                                'radius-server accounting host ' + Radius_server,'aaa-accounting enable','aaa enable','radius nas-ipv4 ' + StaticIpv4_ac1,
                                'aaa group server radius wlan','server ' + Radius_server])

    #result
    printCheckStep(testname, 'Step 1',res1)

    ################################################################################
    #Step 2
    #配置AC的pppoe功能。认证模式为PAP。并no掉AC上给client分配地址的地址池
    #pppoe-server enable
    #pppoe-server bind radius-group wlan
    #ip pppoe pool poe 192.168.91.0 255.255.255.0
    #interface virtual-template 1
     #ip address 192.168.91.1 255.255.255.0
     #ppp authentication-mode pap
     #remote address pppoe-pool poe
     #ppp account-statistics enable
    #interface Vlan4091
    #pppoe-server bind virtual-template 1
    #配置成功。在AC上面Show running-config可以看到相关的配置。
    ################################################################################

    printStep(testname,'Step 2',
              'Config pppoe server')

    EnterConfigMode(switch1)
    SetCmd(switch1,'no','ip dhcp pool pool4091')
    SetCmd(switch1,'pppoe-server enable')
    SetCmd(switch1,'pppoe-server bind radius-group wlan')
    SetCmd(switch1,'ip pppoe pool poe ' + Dhcp_pool1 + '0 ' + '255.255.255.0')
    SetCmd(switch1,'interface virtual-template 1')
    SetCmd(switch1,'ip address ' + If_vlan4091_s1_ipv4 + ' 255.255.255.0')
    SetCmd(switch1,'ppp authentication-mode chap')
    SetCmd(switch1,'remote address pppoe-pool poe')
    SetCmd(switch1,'ppp account-statistics enable')
    EnterConfigMode(switch1)
    SetCmd(switch1,'interface vlan ' + Vlan4091)
    SetCmd(switch1,'pppoe-server bind virtual-template 1')

    data1 = SetCmd(switch1,'show run')

    res1 = CheckLine(data1,'pppoe-server enable')
    #result
    printCheckStep(testname, 'Step 2',res1)

    ################################################################################
    #Step 3
    #操作
    #将配置下发到AP1。
    #Wireless ap profile apply 1
    #
    #预期
    #配置下发成功。
    ################################################################################

    printStep(testname,'Step 3',
              'Wireless ap profile apply 1')
    res1 = 1		  
    res1 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

    printCheckStep(testname, 'Step 3',res1)

    ################################################################################
    #Step 4
    #操作
    #STA1关联到test1
    #
    #预期
    #成功关联，但获取不到地址
    ################################################################################

    printStep(testname,'Step 4',
              'STA1 associate with network1,',
              'but can not get ip address.')

    res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='open',checkDhcpAddress=Netcard_ipaddress_check,reconnectflag=0,bssid=ap1mac_lower)
    res1 = 0 if res1 != 0 else 1
    res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')

    printCheckStep(testname, 'Step 4',res1,res2)
    # 如果客户端无法关联network或获取到IP，则不执行后续步骤
    keeponflag = res1
    if GetWhetherkeepon(keeponflag):
        ################################################################################
        #Step 5
        #设输入正确的用户名和密码，连接
        #pppoe连接成功，能够获取到地址，且ping通AC
        ################################################################################

        printStep(testname,'Step 5',
                  'pppoe connect successfully')

        SetCmd(sta1,'ifup ppp0')
        data1 = SetCmd(sta1,'ifconfig ppp0')

        res1 = CheckLine(data1,Dhcp_pool1)

        res2 = CheckPing(sta1,If_vlan4091_s1_ipv4,mode='linux')

        #result
        printCheckStep(testname, 'Step 5',res1,res2)

    ################################################################################
    #Step 6
    #操作
    #恢复默认配置
    ################################################################################
    printStep(testname,'Step 6',
              'Recover initial config for switches.')

    #STA1解关联
    SetCmd(sta1,'ifdown ppp0')
    WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)          
    # AC1清除PPPOE配置
    EnterConfigMode(switch1)
    SetCmd(switch1,'interface vlan ' + Vlan4091)
    SetCmd(switch1,'no pppoe-server bind virtual-template 1')
    SetCmd(switch1,'exit')
    SetCmd(switch1,'no interface virtual-template 1')
    SetCmd(switch1,'no pppoe-server enable')
    SetCmd(switch1,'no pppoe-server bind radius-group')
    SetCmd(switch1,'no ip pppoe pool poe')
    # AC1清除Radius配置
    EnterConfigMode(switch1)
    SetCmd(switch1,'no radius source-ipv4')
    SetCmd(switch1,'no radius-server key')
    SetCmd(switch1,'no aaa group server radius wlan')
    SetCmd(switch1,'no radius nas-ipv4')
    SetCmd(switch1,'no aaa enable')
    SetCmd(switch1,'no aaa-accounting enable')
    SetCmd(switch1,'no radius-server authentication host ' + Radius_server)
    SetCmd(switch1,'no radius-server accounting host ' + Radius_server)
    # 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
    if testcentral:
        EnterConfigMode(switch1)
        SetCmd(switch1,'ip dhcp pool pool4091')
        SetCmd(switch1,'network-address ' + Dhcp_pool1 + '0 255.255.255.0')
        SetCmd(switch1,'default-router ' + If_vlan4091_s1_ipv4)
        SetCmd(switch1,'exit')
        SetCmd(switch1,'ip dhcp pool pool4092')
        SetCmd(switch1,'network-address ' + Dhcp_pool2 + '0 255.255.255.0')
        SetCmd(switch1,'default-router ' + If_vlan4092_s1_ipv4)
        SetCmd(switch1,'exit')
        SetCmd(switch1,'ip dhcp pool pool4093')
        SetCmd(switch1,'network-address ' + Dhcp_pool3 + '0 255.255.255.0')
        SetCmd(switch1,'default-router ' + If_vlan4093_s1_ipv4)
        SetCmd(switch1,'exit')
    else:
        #清除dhcp server，interface vlan配置
        EnterConfigMode(switch1)
        SetCmd(switch1,'no service dhcp')
        SetCmd(switch1,'no interface vlan',Vlan4091)
        SetCmd(switch1,'no','vlan',Vlan4091)

        #修改s1p1 为access 口，vlan40
        EnterInterfaceMode(switch1,s1p1)
        SetCmd(switch1,'no switchport mode')
        SetCmd(switch1,'switchport access vlan 40')

        #S3配置恢复
        #S3 清除dhcp server配置，恢复ethernet 1/1 为access 口，vlan40
        EnterConfigMode(switch3)
        SetCmd(switch3,'service dhcp')
        EnterInterfaceMode(switch3,s3p1)
        SetCmd(switch3,'no switchport mode')
        SetCmd(switch3,'switchport access vlan',Vlan40)

        EnterInterfaceMode(switch3,'vlan '+Vlan4091)
        IdleAfter(Vlan_Idle_time)
        SetCmd(switch3,'ip address ' + If_vlan4091_s1_ipv4 + ' 255.255.255.0')
        SetCmd(switch3,'ipv6 address',If_vlan4091_s1_ipv6+'/64')

    ##operate
    WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
    # WirelessApProfileApply(switch1,'1')
    # IdleAfter(Apply_profile_wait_time)
    #end
    printTimer(testname, 'End')