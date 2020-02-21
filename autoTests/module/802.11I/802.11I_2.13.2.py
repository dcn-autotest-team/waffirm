#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# 802.11I_2.13.2.py
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2020 Digital China Networks Co. Ltd
#
# Features:
# 为缩减脚本执行时间，将方案中2.13.8-9共2个用例合并为1个脚本
# 2.13.2 漫游关联成功后的处理:漫游成功：原关联AP认证client数目减一,新关联AP认证client数目加一(合并原方案中的测试例2.13.8，2.13.9）
# 测试描述: 漫游成功：如果此次漫游为本UWS内部的漫游，在AP的管理UWS上查看原关联AP的认证client数目减一,关联AP的认证client数目加一
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
def Get_apclient_num(switch,apmac):
    EnterEnableMode(switch)
    data = SetCmd(switch,'show wireless ap',apmac,'radio status')
    num_str = re.search('\s+'+radionum+'\s+(\d+\s+){3}(\d+)',data,re.I)
    if num_str:
        _clientnum = int(num_str.group(2))
    else:
        _clientnum = 0
    return _clientnum
    
testname = 'TestCase 802.11I_2.13.2'
avoiderror(testname)
printTimer(testname,'Start','Test client number when client roamed')

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
printCheckStep(testname, 'Step 1',res1)
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
    #查看AP1和AP2关联的客户端数量
    ################################################################################
    printStep(testname,'Step 4',\
              'Get ap1 and ap2 client number')
    # operate
    ap1_clientnum1 = Get_apclient_num(switch1,ap1mac)
    ap2_clientnum1 = Get_apclient_num(switch1,ap2mac)
    # result
    printCheckStep(testname, 'Step 4',0)
    ################################################################################
    #Step 5
    #操作
    #重启AP1
    #预期
    #sta1漫游到AP2上,AP2的客户端数量加1，AP1的客户端数量减1
    ################################################################################
    printStep(testname,'Step 5',\
              'Reboot Ap1',\
              'Sta1 roam to ap2',\
              'ap1 client number decrease 1',\
              'ap2 client number increase 1')
    res1=res2=1
    # operate
    RebootAp(AP=ap1,connectTime=1)
    ap2_clientnum2 = Get_apclient_num(switch1,ap2mac)
    CheckSutCmd(switch1,'show wireless ap status', 
                check=[(ap1mac,'Managed','Success')], 
                waittime=5,retry=20,interval=5,IC=True)
    ap1_clientnum2 = Get_apclient_num(switch1,ap1mac)

    res1 = 0 if  ap1_clientnum1 - ap1_clientnum2 == 1 else 1
    res2 = 0 if  ap2_clientnum2 - ap2_clientnum1 == 1 else 1
    printCheckStep(testname, 'Step 5',res1,res2)
################################################################################
#Step 6
#操作
##恢复默认配置
################################################################################
printStep(testname,'Step 6',\
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

EnterInterfaceMode(switch3,s3p4)
SetCmd(switch3,'shutdown')
IdleAfter(15)
CheckSutCmd(switch1,'show wireless ap status', 
                    check=[(ap1mac,'Managed','Success'),(ap2mac,'Failed','Not Config')], 
                    waittime=5,retry=20,interval=5,IC=True)
#end
printTimer(testname, 'End')