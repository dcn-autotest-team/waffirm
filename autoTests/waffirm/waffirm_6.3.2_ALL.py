#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_6.3.2.py - test case 6.3.2 of waffirm
#
# Author:
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 6.3.2 management vlan 和untag vlan不相同情况下的内置Portal功能测试
# 测试目的：测试management vlan 和untag vlan不相同情况下的内置Portal测试
# 测试环境：同测试拓扑
# 测试描述：测试ap management vlan 和untag vlan不相同情况下客户端发起HTTP/HTTPS请求时，能够成功重定向到内置Portal的认证页面，客户端能够成功的上/下线
#          （STA1的MAC地址：STA1MAC）
#
#*******************************************************************************
# Change log:
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 6.3.2'
avoiderror(testname)
printTimer(testname,'Start','Test internal portal')

###############################################################################
#Step 1
#操作
#在AC1配置network1的SSID为test1，关联vlan4091，配置下发到AP1，
#配置Radius服务器
#配置内置Portal
#
#
#预期
#配置成功
################################################################################
printStep(testname,'Step 1',
          'set radius server-name acct wlan,',
          'set radius setver-name auth wlan,',
          'and u should config others and so on,',
          'check config success,'
          'config captive-portal,')
res1=1
# SetCmd(ap1,'set management vlan-id',Vlan20)
# SetCmd(ap1,'set untagged-vlan vlan-id 2')
# ApSetcmd(ap1,Ap1cmdtype,'set_management_vlanid',Vlan20)
# ApSetcmd(ap1,Ap1cmdtype,'set_untagged_vlanid','2',commitflag=True)

# AC修改management vlan和ethernet native-vlan配置，并下发profile
EnterWirelessMode(switch1)
EnterApProMode(switch1,'1')
SetCmd(switch1,'management vlan',Vlan20)
SetCmd(switch1,'ethernet native-vlan 2')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# 配置下发后，ap的management vlan和ethernet native-vlan已经修改，但是s3的端口配置没有修改，
# 导致AP和AC之间不通，AP会下线（注意：此处必须先等AP下线后再修改S3配置）
CheckSutCmd(switch1,'show wireless ap status',
            check=[(ap1mac,'Failed','Not Config')],
            waitflag=False,retry=10,interval=5,IC=True)
# 修改S3端口配置  
EnterConfigMode(switch3)
SetCmd(switch3,'vlan 2')
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan 2')
IdleAfter(20)
res1=CheckSutCmd(switch1,'show wireless ap status',
                 check=[(ap1mac,'Managed','Success')],
                 waittime=5,retry=20,interval=5,IC=True)
                
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
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'enable')
SetCmd(switch1,'authentication-type internal')
SetCmd(switch1,'configuration 1 ')
SetCmd(switch1,'enable')
SetCmd(switch1,'radius accounting ')
SetCmd(switch1,'protocol http')
SetCmd(switch1,'radius-acct-server wlan')
SetCmd(switch1,'radius-auth-server wlan')
SetCmd(switch1,'redirect attribute ssid enable ')
SetCmd(switch1,'redirect attribute nas-ip enable')
SetCmd(switch1,'interface ws-network 1')

if Ap1cmdtype == 'uci':
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'free-resource 1 destination ipv4 ' + StaticIpv4_ac1 +'/32 source any')
    SetCmd(switch1,'configuration 1 ')
    SetCmd(switch1,'free-resource 1')

#result
printCheckStep(testname, 'Step 1',res1)


################################################################################
#Step 2
#操作
#在STA1上连接test1
#
#预期
#连接成功
################################################################################

printStep(testname,'Step 2',
          'STA1connect to network 1,',
          'STA1dhcp and get 192.168.91.x ip')

sta1_ipv4 = ''

res1=res2=1

#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
IdleAfter(10)
#获取STA1的地址
sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
res2 = sta1_ipresult['res']

#result
printCheckStep(testname, 'Step 2',res1,res2)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 3
    #操作
    #客户端STA1访问1.1.1.1
    #
    #预期
    #STA1被重定向到Portal认证页面
    ################################################################################

    printStep(testname,'Step 3',
              'STA1 http connect 1.1.1.1,')

    web = web_init(sta1_host)
    if None != web:
        res1 = web_open(web,'http://1.1.1.1')
        if res1['status']:
            res2 = is_portal_page(web)
            if res2['status']:
                res3 = 0
            else:
                res3 = 1
                printRes('is_portal_page(web) status false')
        else:
            res3 = 1
            printRes('web_open(web,\'http://1.1.1.1\')')
    else:
        res3 =1
        printRes('web_init(sta1) status false')


    printCheckStep(testname, 'Step 3',res3)


    ################################################################################
    #Step 4
    #操作
    #输入用户名和密码
    #
    #预期
    #输入正确
    ################################################################################

    printStep(testname,'Step 4',
              'input username and password')


    #operate
    res1=res2=res3=1
    res1 = portal_login(web,'aaa','111')
    if res1['status']:
        res2 = 0
    else:
        printRes(res1)

    #result
    printCheckStep(testname, 'Step 4',res2)


    ################################################################################
    #Step 5
    #操作
    #客户端主动下线。
    #
    #预期
    #下线成功
    ################################################################################

    printStep(testname,'Step 5',
              'STA1 logout.')

    res1 = portal_logout(web)
    if res1 != None:
        if res1['status']:
            res2 = 0
        else:
            res2 =1
            printRes(res1)

    printCheckStep(testname, 'Step 5',res2)

    res1 = web_close(web)
    printRes(res1)
    if not res1['status']:
        CMDKillFirefox(sta1)
    ################################################################################
    #Step 6
    #操作
    #修改内置Portal协议为https
    #
    #预期
    #配置成功
    ################################################################################

    printStep(testname,'Step 6',
              'portal is https')

    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'configuration 1')
    SetCmd(switch1,'protocol https')



    printCheckStep(testname, 'Step 6',0)


    ################################################################################
    #Step 7
    #操作
    #客户端STA1访问1.1.1.1
    #
    #预期
    #STA1被重定向到Portal认证页面
    ################################################################################

    printStep(testname,'Step 7',
              'STA1 http connect 1.1.1.1,')

    web = newweb_init(sta1_host)
    if None != web:
        res1 = newweb_open(web,'http://1.1.1.1')
        if res1['status']:
            res2 = newis_innerportal_page(web)
            if res2['status']:
                res3 = 0
            else:
                res3 = 1
                printRes('is_portal_page(web) status false')
        else:
            res3 = 1
            printRes('web_open(web,\'http://1.1.1.1\')')
    else:
        res3 =1
        printRes('web_init(sta1) status false')

    if res3 !=0:
        printRes('if this step fail,please check this case manually!!!!!!!')
    printCheckStep(testname, 'Step 7',res3)


    ################################################################################
    #Step 8
    #操作
    #输入用户名和密码
    #
    #预期
    #输入正确
    ################################################################################

    printStep(testname,'Step 8',
              'input username and password')


    #operate
    res1=res2=res3=1
    res1 = newportal_login(web,'aaa','111')
    if res1['status']:
        res2 = 0
    else:
        printRes(res1)

    #result
    if res2 !=0:
        printRes('if this step fail,please check this case manually!!!!!!!')
    printCheckStep(testname, 'Step 8',res2)


    ################################################################################
    #Step 9
    #操作
    #客户端主动下线。
    #
    #预期
    #下线成功
    ################################################################################

    printStep(testname,'Step 9',
              'STA1 logout.')

    res1 = newportal_logout(web)
    if res1 != None:
        if res1['status']:
            res2 = 0
        else:
            res2 =1
            printRes(res1)
            
    WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
    if res2 !=0:
        printRes('if this step fail,please check this case manually!!!!!!!')
        
    printCheckStep(testname, 'Step 9',res2)


################################################################################
#Step 10
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 10',
          'Recover initial config for switches.')

#operate

WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'disable')
SetCmd(switch1,'no configuration 1')
SetCmd(switch1,'no authentication-type')
EnterConfigMode(switch1)
SetCmd(switch1,'no radius source-ipv4')
SetCmd(switch1,'no radius-server key')
SetCmd(switch1,'no aaa group server radius wlan')
SetCmd(switch1,'no radius nas-ipv4')
SetCmd(switch1,'no aaa enable')
SetCmd(switch1,'no aaa-accounting enable')
SetCmd(switch1,'no radius-server authentication host ' + Radius_server)
SetCmd(switch1,'no radius-server accounting host ' + Radius_server)

EnterWirelessMode(switch1)
EnterApProMode(switch1,'1')
SetCmd(switch1,'no','management vlan')
SetCmd(switch1,'ethernet native-vlan 1')
WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
# 配置下发后，ap的management vlan和ethernet native-vlan已经修改，但是s3的端口配置没有修改，
# 导致AP和AC之间不通，AP会下线（注意：此处必须先等AP下线后再修改S3配置）
CheckSutCmd(switch1,'show wireless ap status',
            check=[(ap1mac,'Failed','Not Config')],
            waitflag=False,retry=10,interval=5,IC=True)
# 修改S3端口配置 
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral:
    EnterConfigMode(switch3)
    SetCmd(switch3,'no vlan 2')
    SetCmd(switch3,'Interface ',s3p3)
    SetCmd(switch3,'switchport mode access ')
    SetCmd(switch3,'switchport access vlan ',Vlan20)
else:
    EnterConfigMode(switch3)
    SetCmd(switch3,'no vlan 2')
    SetCmd(switch3,'Interface ',s3p3)
    SetCmd(switch3,'switchport mode trunk')
    SetCmd(switch3,'switchport trunk allowed vlan all')
    SetCmd(switch3,'switchport trunk native vlan',Vlan20)

# SetCmd(ap1,'set management vlan-id',Vlan20)
# SetCmd(ap1,'set untagged-vlan vlan-id',Vlan20)
# ApSetcmd(ap1,Ap1cmdtype,'set_management_vlanid','1')
# ApSetcmd(ap1,Ap1cmdtype,'set_untagged_vlanid','1',commitflag=True)

# EnterWirelessMode(switch1)
# EnterApProMode(switch1,'1')
# SetCmd(switch1,'no','management vlan')
# SetCmd(switch1,'ethernet native-vlan 1')
IdleAfter(20)
res1=CheckSutCmd(switch1,'show wireless ap status',
                 check=[(ap1mac,'Managed','Success')],
                 waittime=5,retry=20,interval=5,IC=True)

if Ap1cmdtype == 'uci':
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'no free-resource 1')
#end
printTimer(testname, 'End')


