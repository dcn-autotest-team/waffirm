#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.27.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.27	1+1场景下的portal认证
# 测试目的：开启1+1热备后，AP在主备AC之间切换过程中，客户端连接网络可以正常进行portal认证
# 测试描述：
# 1.	客户端STA1连接网络进行portal认证，客户端STA2连接到网络不进行portal认证
# 2.	AP从主AC切换到备AC后，客户端STA2进行portal认证能够成功，同时客户端STA1和STA2的表项都正常
# 3.	AP从备AC切换到主AC后，客户端STA1和STA2的表项仍然正常
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.2
#*******************************************************************************

#Package

#Global Definition
S1_vlan30_ipv4 = '30.1.'+EnvNo+'.10'
S2_vlan30_ipv4 = '30.1.'+EnvNo+'.12'
S3_vlan30_ipv4 = '30.1.'+EnvNo+'.1'
Ap1_new_ipv4 = '30.1.'+EnvNo+'.11'
#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase externalportal_4.1.27'
avoiderror(testname)
printTimer(testname,'Start','Test switch-redundancy')
###############################################################################
#Step 1
#操作
# 1+1初始化境配置：修改AC1、AC2和AP的接口ip，保证AC1和AC2能够ping通 
# AC1上配置
# AC1(config)#vlan 30                                                                                                                 
# AC1(config-vlan30)#interface  vlan  30                                                                                              
# AC1(config-if-vlan30)#ip address  30.1.1.10 255.255.255.0                                                                                                 
# AC1(config-if-vlan30)#interface  s1p1                                                                                    
# AC1(config-if-s1p1)#switchport  access  vlan  30                                                                                                                                                                                                                                                                                                                                                                                                                                                                
# AC1(config)#wireless    
# AC1(config-wireless)#static-ip 30.1.1.10                                                                                                            
# AC1(config-wireless)#switch-redundancy master 30.1.1.10 backup 30.1.1.12                                                                                  
# AC1(config-wireless)#discovery ip-list 30.1.1.12                                                                                  
# AC1(config-wireless)#discovery ip-list 30.1.1.11
# AC2上配置
# AC2(config)#vlan 30                                                                                                                 
# AC2(config-vlan30)#interface  vlan  30                                                                                              
# AC2(config-if-vlan30)#ip address  30.1.1.12 255.255.255.0                                                                                                 
# AC2(config-if-vlan30)#interface s2p1                                                                                    
# AC2(config-if-s2p1)#switchport  access  vlan  30                                                                                                                                                                                                                                                                                                                                                                                                                                                                
# AC2(config)#wireless   
# AC2(config-wireless)#static-ip 30.1.1.12                                                                                                             
# AC2(config-wireless)#switch-redundancy master 30.1.1.10 backup  30.1.1.12                                                                                  
# AC2(config-wireless)#discovery ip-list 30.1.1.10 
# S3配置    
# S3(config)#interface s3p1                                                                                                                                                                        
# S3(config-if-s3p1)#switchport  access  vlan  30
# S3(config)#interface s3p3                                                                                                                                                                        
# S3(config-if-s3p3)#switchport  access  vlan  30 
# AP1配置
# set management static-ip 30.1.1.11
# save-running  
# 重启AP1 
#预期
# 配置成功
# AC1上通过命令show wireless  ap status显示AP1在线
# AC1和AC2上通过命令show wireless switch redundancy status查看到
# Master显示为30.1.1.10 (Active)
################################################################################
printStep(testname,'Step 1','Config switch-redundancy')
res1=res2=res3=1
# operate
# 配置S1
# 配置端口
EnterConfigMode(switch1)
SetCmd(switch1,'vlan',Vlan30)
EnterInterfaceMode(switch1,'vlan '+Vlan30)
IdleAfter(Vlan_Idle_time)
SetCmd(switch1,'ip address',S1_vlan30_ipv4,'255.255.255.0')
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport mode access')
SetCmd(switch1,'switchport access vlan',Vlan30)
# 配置radius
EnterConfigMode(switch1)
SetCmd(switch1,'radius nas-ipv4',S1_vlan30_ipv4)
SetCmd(switch1,'radius source-ipv4',S1_vlan30_ipv4)
# 配置wireless
EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip',S1_vlan30_ipv4)
SetCmd(switch1,'discovery ip-list',S2_vlan30_ipv4)
SetCmd(switch1,'discovery ip-list',Ap1_new_ipv4)
IdleAfter(10)
SetCmd(switch1,'switch-redundancy master '+S1_vlan30_ipv4+' backup '+S2_vlan30_ipv4)
# 配置captive portal
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'ac-name ac1master')
# 配置S2
# 配置端口
EnterConfigMode(switch2)
SetCmd(switch2,'vlan',Vlan30)
EnterInterfaceMode(switch2,'vlan '+Vlan30)
IdleAfter(Vlan_Idle_time)
SetCmd(switch2,'no ip address')
SetCmd(switch2,'ip address',S2_vlan30_ipv4,'255.255.255.0')
# 配置radius
EnterConfigMode(switch2)
SetCmd(switch2,'radius nas-ipv4',S2_vlan30_ipv4)
SetCmd(switch2,'radius source-ipv4',S2_vlan30_ipv4)
# 配置wireless
EnterWirelessMode(switch2)
SetCmd(switch2,'static-ip',S2_vlan30_ipv4)
SetCmd(switch2,'discovery ip-list',S1_vlan30_ipv4)
SetCmd(switch2,'discovery ip-list',Ap1_new_ipv4)
SetCmd(switch2,'discovery ip-list',Ap2_ipv4)
IdleAfter(10)
SetCmd(switch2,'switch-redundancy master '+S1_vlan30_ipv4+' backup '+S2_vlan30_ipv4)
# 配置captive portal
EnterConfigMode(switch2)
SetCmd(switch2,'captive-portal')
SetCmd(switch2,'configuration 1')
SetCmd(switch2,'ac-name ac2backup')
# 配置S3
EnterConfigMode(switch3)
SetCmd(switch3,'vlan',Vlan30)
EnterInterfaceMode(switch3,'vlan '+Vlan30)
IdleAfter(Vlan_Idle_time)
SetCmd(switch3,'no ip address')
SetCmd(switch3,'ip address',S3_vlan30_ipv4,'255.255.255.0')
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport mode access')
SetCmd(switch3,'switchport access vlan',Vlan30)
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan30)

# 配置AP1
SetCmd(ap1,'\n')
ApSetcmd(ap1,Ap1cmdtype,'set_static_ip',Ap1_new_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'set_ip_route',S3_vlan30_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'saverunning')
# check
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap1,ap1mac,switch1,Ap1cmdtype)
IdleAfter(20)
EnterEnableMode(switch1)
res1=CheckSutCmd(switch1,'show wireless ap status', \
                check=[(ap1mac,'Managed','Success')], \
                waittime=5,retry=20,interval=5,IC=True)
res2=CheckSutCmd(switch1,'show wireless switch redundancy status', \
                check=[('Master',S1_vlan30_ipv4+'\(Active\)')], \
                retry=1,waitflag=False,IC=True)   
res3=CheckSutCmd(switch2,'show wireless switch redundancy status', \
                check=[('Master',S1_vlan30_ipv4+'\(Active\)')], \
                retry=1,waitflag=False,IC=True)                 
# result
printCheckStep(testname, 'Step 1',res1,res2,res3)
###############################################################################
#Step 2
#操作
# 客户端STA1连接到网络Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端获取到192.168.X.X（Dhcp_pool1）网段的地址
# STA1无法ping通PC1
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
    ################################################################################
    #Step 4
    #操作
    # 重新输入正确的用户名和密码进行认证
    # portal认证用户名：portal_username = 'aaa'
    # portal认证密码：portal_password = '111' 
    # AC1上查看CP列表
    # 检查AC1是否放行STA1的流量
    #预期
    # 提示用户认证成功，通过show captive-portal  client  status命令查看CP client列表，
    # 显示出STA1的信息（“MAC Address”显示“STA1MAC”）
    # STA1可以ping通PC1
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
    # 客户端STA2连接到网络Network_name1
    #预期
    # 关联成功。
    # 通过命令show wireless  client  summary可以查看客户端STA2获取到192.168.X.X（Dhcp_pool1）网段的地址
    ################################################################################
    printStep(testname,'Step 5','STA2 connect to test1')
    res1=res2=1
    #operate
    #STA1关联 network1
    res1 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
    if res1 == 0:
        res2 = CheckWirelessClientOnline(switch1,sta2mac,'online')
    #result
    printCheckStep(testname, 'Step 5',res1,res2)
    sta2_login_flag = res1
    ###############################################################################
    #Step 6
    #操作
    # 断开AC1和S3的网络连接
    # AC1(config)#interface s1p1                                                                                            
    # AC1(config-if-s1p1)#shutdown
    #预期
    # AC1和AC2之间发生主备切换，AC2成为master
    # AC2上通过命令show wireless switch redundancy status查看到
    # Master显示为30.1.1.12 (Active)
    ################################################################################
    printStep(testname,'Step 6','Shutdown s1p1 and AC2 become master')
    res1=1
    #operate
    EnterConfigMode(switch1)
    SetCmd(switch1,'interface',s1p1)
    SetCmd(switch1,'shutdown')
    IdleAfter(10)
    res1 = CheckSutCmd(switch2,'show wireless switch redundancy status',\
                                check=[('Backup',S2_vlan30_ipv4+'\(Active\)')],retry=10,waitflag=False)
    # 等待AP将客户端上报给AC
    CheckSutCmd(switch2,'show wireless client status',\
                        check=[(sta1mac),(sta2mac)],retry=20,waitflag=False) 
    #result
    printCheckStep(testname, 'Step 6',res1)
    if sta2_login_flag == 0:
        ################################################################################
        #Step 7
        #操作
        # 客户端STA2打开web页面访问1.1.1.1（该地址为变量web_ip）
        #
        #预期
        # STA2上可以看到重定向页面，并且提示输入用户名和密码
        ################################################################################
        printStep(testname,'Step 7','sta2 open 1.1.1.1 and can redirect to portal auth page')
        res1=1
        #operate
        web = web_init(sta2_host)
        res1 = exportal_redirect_success(web,web_ip)
        #result
        printCheckStep(testname, 'Step 7',res1)
        ################################################################################
        #Step 8
        #操作
        # 输入正确的用户名和密码进行认证
        # portal认证用户名：portal_username = 'aaa'
        # portal认证密码：portal_password = '111' 
        # 查看AC2上的CP列表
        # 检查STA1、STA2是否可以上网 
        #预期
        # 提示用户认证成功，AC2通过show captive-portal  client  status命令查看CP client列表，显示出STA1和STA2的信息
        # STA1和STA2都可以ping通PC1
        ################################################################################
        printStep(testname,'Step 8',\
                            'sta2 input correct username and password',\
                            'login successully')
        res1=res2=res3=res4=1
        # operate
        res1 = exportal_login_withcheck(web,portal_username,portal_password)
        res2 = CheckSutCmd(switch2,'show captive-portal client status',\
                                    check=[(sta1mac),(sta2mac)],retry=5,waitflag=False)
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        res4 = CheckPing(sta2,pc1_ipv4,mode='linux')
        #result
        printCheckStep(testname, 'Step 8',res1,res2,res3,res4)
        # 关闭网页
        res = web_close(web)
        if res['status'] != True:
            printRes(res)
            CMDKillFirefox(sta2)
    ###############################################################################
    #Step 9
    #操作
    # AP从备AC2上切换到主AC1
    # 恢复AC1和S3的网络连接，断开AC2和S3的连接
    # AC1(config)#interface s1p1                                                                                            
    # AC1(config-if-s1p1)#no shutdown

    # AC2(config)#interface s2p1                                                                                            
    # AC2(config-if-s2p1)#shutdown
    #预期
    # AC1和AC2之间发生主备切换，AC1成为master
    # AC1上通过命令show wireless switch redundancy status查看到
    # Master显示为30.1.1.10 (Active)
    ################################################################################
    printStep(testname,'Step 9','No shutdown s1p1 and shutdown s2p1',\
                                'master and backup exchanged')
    res1=1
    #operate
    # 将s1p1 no shutdown后，需要先等待AC1的wireless up起来后，AC1和AC2之间的冗余备份才生效，ap和客户端表项才能正常切换，
    # 因此脚本中s1p1 no shutdown后，先等待AC1和AC2建立起冗余备份关系，再执行后续操作
    EnterConfigMode(switch1)
    SetCmd(switch1,'interface',s1p1)
    SetCmd(switch1,'no shutdown')
    IdleAfter(5)
    res1 = CheckSutCmd(switch1,'show wireless switch redundancy status',\
                        check=[('Master',S1_vlan30_ipv4+'\(Active\)')],retry=10,waitflag=False)
    IdleAfter(20)
    EnterConfigMode(switch2)
    SetCmd(switch2,'interface',s2p1)
    SetCmd(switch2,'shutdown')
    IdleAfter(2)
    #result
    printCheckStep(testname, 'Step 9',res1)
    ################################################################################
    #Step 10
    #操作
    # 检查客户端STA1和STA2的网络连接状态
    # 查看AC1上的CP列表
    # 检查STA1、STA2是否可以上网 
    #预期
    # 客户端STA1和STA2仍然在线
    # AC1上通过命令show captive-portal  client  status查看STA1和STA2的表项
    # STA1和STA2都可以ping通PC1
    ################################################################################
    printStep(testname,'Step 10','sta1 and sta2 are still in portal client list',\
                                'sta1 and sta2 ping pc1 successully')
    res1=res2=res3=1
    # operate
    res1 = CheckSutCmd(switch1,'show captive-portal client status',\
                                check=[(sta1mac),(sta2mac)],retry=10,waitflag=False)
    res2 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res3 = CheckPing(sta2,pc1_ipv4,mode='linux')
    #result
    printCheckStep(testname, 'Step 10',res1,res2,res3)
################################################################################
#Step 11
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 11',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)
# 配置S2
# 配置端口
EnterConfigMode(switch2)
SetCmd(switch2,'interface',s2p1)
SetCmd(switch2,'no shutdown')
EnterConfigMode(switch2)
SetCmd(switch2,'vlan',Vlan30)
EnterInterfaceMode(switch2,'vlan '+Vlan30)
IdleAfter(Vlan_Idle_time)
SetCmd(switch2,'no ip address')
SetCmd(switch2,'ip address',If_vlan30_s2_ipv4,'255.255.255.0')
# 配置radius
EnterConfigMode(switch2)
SetCmd(switch2,'radius nas-ipv4',StaticIpv4_ac2)
SetCmd(switch2,'radius source-ipv4',StaticIpv4_ac2)
# 配置wireless
EnterWirelessMode(switch2)
SetCmd(switch2,'static-ip',StaticIpv4_ac2)
CheckSutCmd(switch2,'show wireless', \
                check=[('WS IP Address',StaticIpv4_ac2)], \
                retry=20,waitflag=False,IC=True) 
SetCmd(switch2,'no discovery ip-list',S1_vlan30_ipv4)
SetCmd(switch2,'no discovery ip-list',Ap1_new_ipv4)
SetCmd(switch2,'no discovery ip-list',Ap2_ipv4)
SetCmd(switch2,'no switch-redundancy')
# 配置captive portal
EnterConfigMode(switch2)
SetCmd(switch2,'captive-portal')
SetCmd(switch2,'configuration 1')
SetCmd(switch2,'ac-name 0100.0010.0'+EnvNo+'0.02')

# 配置S1
# 配置端口
EnterInterfaceMode(switch1,s1p1)
SetCmd(switch1,'switchport mode access')
SetCmd(switch1,'switchport access vlan',Vlan40)
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan',Vlan30)
SetCmd(switch1,'no vlan',Vlan30)
# 配置radius
EnterConfigMode(switch1)
SetCmd(switch1,'radius nas-ipv4',StaticIpv4_ac1)
SetCmd(switch1,'radius source-ipv4',StaticIpv4_ac1)
# 配置wireless
EnterWirelessMode(switch1)
SetCmd(switch1,'static-ip',StaticIpv4_ac1)
SetCmd(switch1,'no discovery ip-list',S2_vlan30_ipv4)
SetCmd(switch1,'no discovery ip-list',Ap1_new_ipv4)
SetCmd(switch1,'no switch-redundancy')
# 配置captive portal
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'ac-name 0100.0010.0'+EnvNo+'0.01')

# 配置S3
EnterInterfaceMode(switch3,s3p1)
SetCmd(switch3,'switchport mode access')
SetCmd(switch3,'switchport access vlan',Vlan40)
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'switchport mode trunk')
SetCmd(switch3,'switchport trunk native vlan',Vlan20)
EnterInterfaceMode(switch3,'vlan '+Vlan30)
IdleAfter(Vlan_Idle_time)
SetCmd(switch3,'no ip address')
SetCmd(switch3,'ip address',If_vlan30_s3_ipv4,'255.255.255.0')

# 配置AP1
SetCmd(ap1,'\n')
ApSetcmd(ap1,Ap1cmdtype,'set_static_ip',Ap1_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'set_ip_route',If_vlan20_s3_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'saverunning')
# check
# set managed-ap mode为ap的隐藏命令，可以使Ap重新被AC认证（代替重启AP操作）
ChangeAPMode(ap1,ap1mac,switch1,Ap1cmdtype)
IdleAfter(20)
EnterEnableMode(switch1)
res1=CheckSutCmd(switch1,'show wireless ap status', \
                check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')], \
                waittime=5,retry=20,interval=5,IC=True)

#end
printTimer(testname, 'End')