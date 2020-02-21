#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# externalportal_4.1.7.1.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.7.1	portal逃生
# 测试目的：外置portal场景下，开启portal认证，当AC1与portal服务器的通信中断后，客户端连接网络后可以直接上网
# 测试描述：
# 1、	配置portal逃生功能。
# 2、	STA1连接网络进行portal认证
# 3、	中断AC1跟portal服务器的通信
# 4、	STA2连接无线网络，可以直接上网
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.21
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase externalportal_4.1.7.1'
avoiderror(testname)
printTimer(testname,'Start','Test extrnal portal escape function')
###############################################################################
#Step 1
#操作
# 开启portal逃生功能
# AC1(config-cp)# portal-server-detect server-name eportal interval 30 retry 3 action permit-all log  trap
#预期
# 配置成功。
# AC1上面通过命令show captive-portal  ext-portal-server server-name eportal status可以查看到Detect Mode为Enable
################################################################################
printStep(testname,'Step 1','Config portal-server-detect')
res1=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'enable')
SetCmd(switch1,'portal-server-detect server-name eportal interval 30 retry 3 action log permit-all trap')
# check
data=SetCmd(switch1,'show captive-portal ext-portal-server server-name eportal status')
res1=CheckLineList(data,[('Detect Mode','Enable')],IC=True)
#result
printCheckStep(testname, 'Step 1',res1)
################################################################################
#Step 2
#操作
#客户端STA1连接到网络Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端获取到192.168.X.X(Dhcp_pool1)网段的地址
################################################################################
printStep(testname,'Step 2','STA1 connect to test1')
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res1 == 0:
	res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
#result
printCheckStep(testname, 'Step 2',res1,res2)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 3
    #操作
    # 客户端STA1打开web页面访问1.1.1.1
    #
    #预期
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 3','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    #operate
    web = web_init(sta1_host)
    res1 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 3',res1)
    if res1 == 0:
        ################################################################################
        #Step 4
        #操作
        # 客户端STA1在推送出的重定向页面输入正确的用户名和密码进行认证
        # portal认证用户名：portal_username = 'aaa'
        # portal认证密码：portal_password = '111
        #预期
        # STA1认证成功
        # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）。
        # STA1ping PC1可以ping通
        ################################################################################
        printStep(testname,'Step 4',\
                            'input correct username and password',\
                            'login successully')
        res1=res2=res3=1
        # operate
        res1 = exportal_login_withcheck(web,portal_username,portal_password)
        res2 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        #result
        printCheckStep(testname, 'Step 4',res1,res2,res3)
    # 关闭网页
    res = web_close(web)
    if res['status'] != True:
        printRes(res)
        CMDKillFirefox(sta1)
    ################################################################################
    #Step 5
    #操作
    # 断开测试环境和portal 服务器的通信：
    # S3与portal服务器连接口：s3p5 
    # S3(config)#interface s3p5                                                                                    
    # S3(config-if- s3p5)#shutdown
    #预期
    # 90s后，AC1成功检测到portal服务器故障
    # AC1去ping portal服务器无法ping通
    # AC1上通过命令show captive-portal  ext-portal-server server-name eportal status显示Detect Operational Status为Down
    ################################################################################
    printStep(testname,'Step 5',\
                        'Shutdown s3p5',\
                        'trigger portal escape function')
    res1=1
    #operate
    EnterInterfaceMode(switch3,s3p5)
    SetCmd(switch3,'shutdown')
    # check
    IdleAfter(60)
    EnterEnableMode(switch1)
    res1 = CheckSutCmd(switch1,'show captive-portal ext-portal-server server-name eportal status', \
                check=[('Detect Operational Status','Down')], \
                retry=7,interval=5,waitflag=False,IC=True)
    #result
    printCheckStep(testname, 'Step 5',res1)
    ################################################################################
    #Step 6
    #操作
    #客户端STA2连接到网络Network_name1
    #预期
    # 关联成功。
    # 通过命令show wireless  client  summary可以查看客户端获取到192.168.X.X(Dhcp_pool1)网段的地址
    ################################################################################
    printStep(testname,'Step 6','STA2 connect to test1')
    res1=res2=1
    #operate
    #STA1关联 network1
    res1 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
    if res1 == 0:
        res2 = CheckWirelessClientOnline(switch1,sta2mac,'online')
    #result
    printCheckStep(testname, 'Step 6',res1,res2)
    ################################################################################
    #Step 7
    #操作
    # 检查客户端STA1是否可以上网
    # 检查客户端STA2是否可以上网
    #(此时由于s3p5已经shutdown,PC1与环境不通，改为pingAP的网关）
    #预期
    # STA1直接可以ping通网关
    # STA2直接可以ping通网关
    ################################################################################
    printStep(testname,'Step 7',\
                        'STA1 ping pc1 successfully',\
                        'STA2 ping pc1 successfully')
    res1=res2=1
    #operate
    res1 = CheckPing(sta1,If_vlan4091_s1_ipv4,mode='linux')
    res2 = CheckPing(sta2,If_vlan4091_s1_ipv4,mode='linux')
    #result
    printCheckStep(testname, 'Step 7',res1,res2)
    ################################################################################
    #Step 8
    #操作
    # 恢复测试环境跟portal服务器之间的通信
    # S3与portal服务器连接口：s3p5
    # S3(config)#interface s3p5                                                                                      
    # S3(config-if-s3p5)#no shutdown
    #预期
    # 90s后，AC1跟portal服务器通信正常
    # AC1可以ping通portal服务器
    # AC1上通过命令show captive-portal  ext-portal-server server-name eportal status显示Detect Operational Status为Up
    ################################################################################
    printStep(testname,'Step 8',\
                        'no shutdown s3p5',\
                        'portal server recover')
    res1=1
    #operate
    EnterInterfaceMode(switch3,s3p5)
    SetCmd(switch3,'no shutdown')
    # check
    IdleAfter(60)
    EnterEnableMode(switch1)
    res1 = CheckSutCmd(switch1,'show captive-portal ext-portal-server server-name eportal status', \
                check=[('Detect Operational Status','Up')], \
                retry=7,interval=5,waitflag=False,IC=True)                          
    #result
    printCheckStep(testname, 'Step 8',res1)
    ################################################################################
    #Step 9
    #操作
    # 重新检查客户端STA1是否可以上网
    # 重新检查客户端STA2是否可以上网
    #预期
    # STA1不能ping通PC1
    # STA2不能ping通PC1
    ################################################################################
    printStep(testname,'Step 9',\
                        'STA1 ping pc1 failed',\
                        'STA2 ping pc1 failed')
    res1=res2=0
    #operate
    res1 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res2 = CheckPing(sta2,pc1_ipv4,mode='linux')
    res1 = 0 if res1 != 0 else 1
    res2 = 0 if res2 != 0 else 1
    #result
    printCheckStep(testname, 'Step 9',res1,res2)
################################################################################
#Step 10
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 10',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)

EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'enable')
SetCmd(switch1,'no portal-server-detect server-name eportal')
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta2mac)],retry=10,waitflag=False)
#end
printTimer(testname, 'End')