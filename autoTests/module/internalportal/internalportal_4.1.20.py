#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# internal_portal_4.1.20.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.20	客户端在开启portal认证的network(相同SSID)间切换网络
# 测试目的：验证客户端在开启了portal认证的网络间的切换功能
# 测试描述：
# 1、	STA1连接AP1 network1可以成功进行portal认证
# 2、	调低AP1 radio1的发射功率，关闭AP1和AP2的radio2，使STA1漫游到AP2 network1， 
# 3、	STA1不需要再次认证，就可以跟有线侧pc1通信
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.25
#*******************************************************************************
# 注意：原方案中采用调低ap1的功率，使客户端自动漫游到ap2上，但调低功率的方式在实际执行中
# 不好判断调低到何种程度才能使客户端漫游，脚本中采用客户端主动关联到network的方式

#Package

#Global Definition
ap1vapmac_network2 = incrmac(ap1vapmac,1)
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase internalportal_4.1.20'
avoiderror(testname)
printTimer(testname,'Start','Test sta switchover network that have same ssid')
################################################################################
#Step 1
#操作
# 新建1个network2（SSID与network1相同），将network2绑定到实例下
# AC1(config)#wireless
# AC1(config-wireless)#network 2
# AC1(config-network)#ssid Network_name1
# AC1(config-network)#vlan Vlan4091
# AC1(config)#captive-portal                                                                                                       
# AC1(config-cp)#configuration 1                                                                                                   
# AC1(config-cp-instance)#interface  ws-network  2  
#预期
# 绑定成功。
# AC1上通过命令show run可以查看到命令：
 # interface ws-network 1                                                                                                            
 # interface ws-network 2 
################################################################################
printStep(testname,'Step 1','Change network 2 ssid to test1',\
                            'Bind network2 to captive-portal configuration 1')
res1=res2=1
#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'network 2')
SetCmd(switch1,'ssid',Network_name1)
SetCmd(switch1,'vlan',Vlan4091)
res1 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1 ')
SetCmd(switch1,'interface ws-network 2 ')
# check
data=SetCmd(switch1,'show run c')
res2=CheckLineList(data,[('interface ws-network 1'),('interface ws-network 2')],IC=True)
#result
printCheckStep(testname, 'Step 1',res1,res2)
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
    # 客户端STA1打开web页面访问1.1.1.1（该地址为变量web_ip）
    #预期
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 3','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    # operate
    # sta1打开1.1.1.1，并检查是否重定向到外置portal认证页面
    web = web_init(sta1_host)
    res1 = inportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 3',res1)
    if res1 == 0:
        ################################################################################
        #Step 4
        #操作
        # 客户端STA1在推送出的重定向页面输入正确的用户名和密码进行认证
        # portal认证用户名：portal_username = ‘aaa’
        # portal认证密码：portal_password = ‘111
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
        res1 = inportal_login_withcheck(web,portal_username,portal_password)
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
###############################################################################
#Step 5
#操作
# 客户端STA1连接到Network2（SSID名称为Network_name1）  
# 查看AC1上的CP列表
# 检查STA1是否可以上网 
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端STA1获取到192.168.X.X(Dhcp_pool1)网段的地址。
# 通命令show wireless  client  status可查看到管理的SSID为 Network_name1，VAP MAC Address显示为(AP1MAC+1)   
# 通过命令show captive-portal  client  status
# 看到STA1的表项，其中mac=STA1MAC
# STA1可以ping通 PC1 
################################################################################
printStep(testname,'Step 5',\
                    'sta1 connect to network2')
res1=res2=res3=res4=1
#operate
#STA1关联 network2
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1_network2)
if res1 == 0:
    # 通过命令show wireless  client  summary可以查看客户端STA1获取到192.168.X.X(Dhcp_pool2)网段的地址
    res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
    # 通命令show wireless  client  status可查看到管理的SSID为 Network_name1，VAP MAC Address显示为(AP1MAC+1)  
    res3 = CheckSutCmd(switch1,'show wireless client status',\
                        check=[(sta1mac,ap1vapmac_network2,Network_name1)],retry=1,waitflag=False,IC=True)
    # 通过命令show captive-portal  client  status看到STA1的表项，其中mac=STA1MAC
    res4 = CheckSutCmd(switch1,'show captive-portal client status',\
                                check=[(sta1mac)],retry=5,waitflag=False)
    res5 = CheckPing(sta1,pc1_ipv4,mode='linux')
#result
printCheckStep(testname, 'Step 5',res1,res2,res3,res4,res5)

################################################################################
#Step 6(合并原方案step6,step7)
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 6',\
          'Recover initial config')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1 ')
SetCmd(switch1,'no interface ws-network 2 ')
EnterWirelessMode(switch1)
SetCmd(switch1,'network 2')
SetCmd(switch1,'ssid',Network_name2)
SetCmd(switch1,'vlan',Vlan4092)
res1 = WirelessApplyProfileWithCheck(switch1,['1'],[ap1mac])

CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)

#end
printTimer(testname, 'End')