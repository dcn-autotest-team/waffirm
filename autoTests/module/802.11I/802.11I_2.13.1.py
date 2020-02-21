#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# 802.11I_2.13.1.py
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2020 Digital China Networks Co. Ltd
#
# Features:
# 为缩减脚本执行时间，将方案中2.13.1-7共7个用例合并为1个脚本
# 2.13.1 漫游关联成功后的处理:漫游成功：client在associated client表（对应step5)
# 测试描述：无漫游成功：在AC上查看associated client表，该client在该UWS的associated client表中
# 2.13.2 漫游关联成功后的处理:漫游成功：STBC Capable和802.11n Capable正确（对应step6)
# 测试描述：漫游成功：在AC上查看associated client表，该client的STBC Capable和802.11n Capable正确
# 2.13.3 漫游关联成功后的处理:漫游成功：client在AP neighbor client表（对应step7)
# 测试描述:漫游成功：在AC上查看client关联AP的AP neighbor client表，该client被加入到该表中
# 2.13.4 漫游关联成功后的处理:漫游成功：Roam history记录漫游事件（对应step8)
# 测试描述:漫游成功：在AC上查看Roam history表，会添加此次漫游事件到该表
# 2.13.5 漫游关联成功后的处理:漫游成功：client和VAP对应关系更新（对应step9)
# 测试描述:漫游成功：在AC上查看VAP-Client Mapping表，该client和VAP的对应关系正确更新
# 2.13.6 漫游关联成功后的处理:漫游成功：client和SSID对应关系更新（对应step10)
# 测试描述:漫游成功：在AC上查看SSID-Client Mapping表，该client和SSID的对应关系正确更新
# 2.13.7 漫游关联成功后的处理:漫游成功：该client和UWS对应关系更新（对应step11)
# 测试描述: 漫游成功：在AC上查看UWS-Client Mapping表，该client和UWS的对应关系正确更新
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.2.11
#*******************************************************************************

#Package

#Global Definition
otherradio = radio2num if test24gflag == True else radio1num
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 802.11I_2.13.1'
avoiderror(testname)
printTimer(testname,'Start','Test client roamed')

################################################################################
#Step 1
#操作
#AC1的network1采用默认的安全接入方式none，即open方式。配置下发到AP1。
#wireless ap profile apply 1
#预期
#配置下发成功。
################################################################################
printStep(testname,'Step 1',\
          'set network1 access mode open as default,',\
          'apply ap profile1 to ap,',\
          'check config success.')

#operate
# step1配置与初始化配置相同，不需要单独下发配置
data = SetCmd(switch1,'show wireless network 1')
# 为防止sta在2.4G和5G之间漫游，测试2.4G时关闭5G，测试5G时关闭2.4G
EnterApProMode(switch1,1)
SetCmd(switch1,'radio',otherradio)
SetCmd(switch1,'no enable')
EnterApProMode(switch1,2)
SetCmd(switch1,'radio',otherradio)
SetCmd(switch1,'no enable')
res1 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
#result
printCheckStep(testname, 'Step 1',0)
################################################################################
#Step 2
#操作
#STA1关联test1。
#
#预期
#成功关联，并获取192.168.91.X网段的IP地址。
# Show wireless client summery可以看到sta1，IP地址的网段正确。
# 在STA1上ping Radius_server,能够ping通
################################################################################
printStep(testname,'Step 2',\
          'STA1 connect to test1',\
          'STA1 get a 192.168.91.X ipaddress'\
          'show client summery can see client',\
          'STA1 ping Radius_server successfully')
res1=res2=res3=1
# operate
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='open',checkDhcpAddress=Netcard_ipaddress_check)
if res1==0:
    res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
    res3 = CheckPing(sta1,Radius_server,mode='linux')

printCheckStep(testname, 'Step 2',res1,res2,res3)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 3
    #操作
    #在S3上将s3p4 no shutdown,等待AC1成功管理AP2
    #预期
    #AC1成功管理AP2
    ################################################################################
    printStep(testname,'Step 3',\
              'no shutdown s3p4',\
              'AC1 managed AP2 successfully')
    res1=1
    # operate
    EnterInterfaceMode(switch3,s3p4)
    SetCmd(switch3,'no shutdown')
    IdleAfter(15)
    res1 = CheckSutCmd(switch1,'show wireless ap status', 
                        check=[(ap2mac,'Managed','Success')], 
                        waittime=5,retry=20,interval=5,IC=True)
    WirelessApplyProfileWithCheck(switch1,['2'],[ap2mac])

    printCheckStep(testname, 'Step 3',res1)
    ################################################################################
    #Step 4
    #操作
    #在S3上将s3p3 shutdown,重启AP1
    #预期
    #AC1管理AP1失败
    ################################################################################
    printStep(testname,'Step 4',\
              'shutdown s3p3',\
              'Reboot Ap1')
    res1=1
    # operate
    EnterInterfaceMode(switch3,s3p3)
    SetCmd(switch3,'shutdown')
    RebootAp(AP=ap1,connectTime=1)
    res1 = CheckSutCmd(switch1,'show wireless ap status', 
                        check=[(ap1mac,'Failed','Not Config')], 
                        waittime=5,retry=20,interval=5,IC=True)

    printCheckStep(testname, 'Step 4',res1)
    ################################################################################
    #Step 5（对应测试例2.13.1）
    #操作
    #在AC1上show wireless client status
    #预期
    #sta1漫游到AP2上，能够ping通 Radius_server
    #在AC上查看associated client表，sta1在associated client表中
    ################################################################################
    printStep(testname,'Step 5',\
              'Sta1 roam to ap2 ',\
              'STA1 ping Radius_server successfully')

    # operate
    res1 = CheckSutCmd(switch1,'show wireless client status', 
                        check=[(sta1mac,ap2vapmac,'Auth')], 
                        retry=20,interval=5,waitflag=False,IC=True)
    res2 = CheckPing(sta1,Radius_server,mode='linux')

    printCheckStep(testname, 'Step 5',res1,res2)
    ################################################################################
    #Step 6（对应测试例2.13.2）
    #操作
    #在AC1上show wireless client sta1mac status
    #预期
    #sta1漫游到AP2上，并且sta1的802.11n Capable和STBC Capable状态正确
    ################################################################################
    printStep(testname,'Step 6',\
              'Sta1 roam to ap2 ',\
              'STA1 802.11n Capable status is yes',\
              'STA1 STBC Capable status is no')

    # operate
    res1 = CheckSutCmd(switch1,'show wireless client '+sta1mac+' status', 
                        check=[('AP MAC Address',ap2mac),('802.11n Capable','Yes'),('STBC Capable','No')], 
                        retry=1,interval=5,waitflag=False,IC=True)

    printCheckStep(testname, 'Step 6',res1)
    ################################################################################
    #Step 7（对应测试例2.13.3）
    #操作
    #在AC1上 show wireless ap ap2mac radio 1 neighbor client status
    #预期
    #sta1漫游到AP2上
    #在AC上查看client关联AP的AP neighbor client表，sta1被加入到该表中
    ################################################################################
    printStep(testname,'Step 7',\
              'Sta1 roam to ap2 ',\
              'STA1 is in ap2 neighbor client table')

    # operate
    res1 = CheckSutCmd(switch1,'show wireless ap '+ap2mac+' radio '+radionum+' neighbor client status', 
                        check=[(sta1mac,'Assoc this AP')],retry=1,interval=5,waitflag=False,IC=True)

    printCheckStep(testname, 'Step 7',res1)
    ################################################################################
    #Step 8（对应测试例2.13.4）
    #操作
    #在AC1上 show wireless client detected-client roam-history
    #预期
    #sta1漫游到AP2上，在AC上查看Roam history表，会添加此次漫游事件到该表
    ################################################################################
    printStep(testname,'Step 8',\
              'Sta1 roam to ap2 ',\
              'roam-history table recorded sta1 roamed')

    # operate
    res1 = CheckSutCmd(switch1,'show wireless client detected-client roam-history', 
                        waittime=10,check=[(sta1mac)],retry=1,interval=5,IC=True)

    printCheckStep(testname, 'Step 8',res1)
    ################################################################################
    #Step 9（对应测试例2.13.5）
    #操作
    #在AC1上 show wireless client status vap ap2mac
    #预期
    #sta1漫游到AP2上， AC1上查看sta1与vap的对应关系正确
    ################################################################################
    printStep(testname,'Step 9',\
              'Sta1 roam to ap2 ',\
              'show wireless client status vap ap2mac')

    # operate
    res1 = CheckSutCmd(switch1,'show wireless client status vap '+ap2vapmac, 
                        check=[(ap2vapmac,ap2mac,sta1mac)],retry=1,interval=5,waitflag=False,IC=True)

    printCheckStep(testname, 'Step 9',res1)
    ################################################################################
    #Step 10（对应测试例2.13.6）
    #操作
    #在AC1上 show wireless client status ssid network1
    #预期
    #sta1漫游到AP2上， AC1上查看sta1与ssid的对应关系正确
    ################################################################################
    printStep(testname,'Step 10',\
              'Sta1 roam to ap2 ',\
              'show wireless client status ssid network1',)

    # operate
    res1 = CheckSutCmd(switch1,'show wireless client status ssid '+Network_name1, 
                        check=[(Network_name1,sta1mac)],retry=1,interval=5,waitflag=False,IC=True)

    printCheckStep(testname, 'Step 10',res1)
    ################################################################################
    #Step 11（对应测试例2.13.6）
    #操作
    #在AC1上 show wireless client status switch StaticIpv4_ac1
    #预期
    #sta1漫游到AP2上， AC1上查看UWS-Client Mapping表,sta1与AC的对应关系正确
    ################################################################################
    printStep(testname,'Step 11',\
              'Sta1 roam to ap2 ',\
              'show wireless client status switch StaticIpv4_ac1')

    # operate
    res1 = CheckSutCmd(switch1,'show wireless client status switch '+StaticIpv4_ac1, 
                        check=[(StaticIpv4_ac1,sta1mac)],retry=1,interval=5,waitflag=False,IC=True)

    printCheckStep(testname, 'Step 11',res1)
################################################################################
#Step 12
#操作
##恢复默认配置
################################################################################
printStep(testname,'Step 12',\
          'Recover initial config for switches')

# operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
CheckWirelessClientOnline(switch1,sta1mac,'offline')
#配置Ap-profile1
EnterApProMode(switch1,1)
SetCmd(switch1,'radio '+radio1num)
SetCmd(switch1,'enable')
SetCmd(switch1,'vap 1')
SetCmd(switch1,'enable')
SetCmd(switch1,'vap 2')
SetCmd(switch1,'enable')
SetCmd(switch1,'exit')
SetCmd(switch1,'exit')
SetCmd(switch1,'radio '+radio2num)
SetCmd(switch1,'enable')
SetCmd(switch1,'vap 1')
SetCmd(switch1,'enable')
#配置Ap-profile2
EnterApProMode(switch1,2)
SetCmd(switch1,'radio '+radio1num)
SetCmd(switch1,'vap 1')
SetCmd(switch1,'enable')
SetCmd(switch1,'exit')
SetCmd(switch1,'exit')
SetCmd(switch1,'radio '+radio2num)
SetCmd(switch1,'vap 1')
SetCmd(switch1,'enable')

EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'no shutdown')
EnterInterfaceMode(switch3,s3p4)
SetCmd(switch3,'shutdown')
IdleAfter(15)
CheckSutCmd(switch1,'show wireless ap status', 
                    check=[(ap1mac,'Managed','Success'),(ap2mac,'Failed','Not Config')], 
                    waittime=5,retry=20,interval=5,IC=True)
#end
printTimer(testname, 'End')