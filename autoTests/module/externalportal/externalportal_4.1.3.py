#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# externalportal_4.1.3.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.3	free-resource功能验证(2.4GHz覆盖)
# 测试目的：验证AC的free-resource功能是否正常
# 测试描述：
# 1.	添加多个free-resource
# 2.	STA1连接SSID后没有通过认证，只能ping通free-resource 对应的地址，其他的无法ping通
# 3.	删除所有free-resource，STA1打开web页面访问任意地址无法推送出重定向页面
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.18
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase externalportal_4.1.3'
avoiderror(testname)
printTimer(testname,'Start','Test free-resource')

###############################################################################
#Step 1
#操作
# 添加多个free-resource（添加的free resources对应的ip地址必须是环境中真实存在的，另外free-resource 1在默认配置里是存在的）
# AC1(config-cp)#free-resource 2 destination  ipv4 BW_server/32 source  any
# （free-resource 2对应的ip地址是BW地址）
# AC1(config-cp)#free-resource 3 destination  ipv4 s3_ipv4/32 source  any
# （free-resource 3对应的ip地址是S3的ip地址，该ip地址为变量：s3_ipv4 = '192.168.10.'+EnvNo+'1'）
#预期
# 添加成功
# AC1上面通过命令show captive-portal  free-resource status可以看到free-resource表项：
# ID1对应的Destination IP Address为Portal_server（此处地址为portal服务器地址，是变量）
# ID2对应的Destination IP Address为BW_server（该地址为BW地址，是变量）
# ID3对应的Destination IP Address为s3_ipv4（该地址为S3的地址，是变量）
################################################################################
printStep(testname,'Step 1','add free-resource ip')
res1=res2=res3=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'free-resource 2 destination ipv4 ' + BW_server +'/32 source any')
SetCmd(switch1,'free-resource 3 destination ipv4 ' + If_vlan192_s3_ipv4 +'/32 source any')
data = SetCmd(switch1,'show captive-portal free-resource status')
res1 = CheckLine(data,'1\s+'+Radius_server+'\s+32')
res2 = CheckLine(data,'2\s+'+BW_server+'\s+32')
res3 = CheckLine(data,'3\s+'+If_vlan192_s3_ipv4+'\s+32')
#result
printCheckStep(testname, 'Step 1',res1,res2,res3)
################################################################################
#Step 2
#操作
# 将建立的free-resource绑定到实例下
# AC1(config)#captive-portal                                                                                                       
# AC1(config-cp)#configuration 1                                                                                                   
# AC1(config-cp-instance)#free-resource 2                                                                                          
# AC1(config-cp-instance)#free-resource 3
#预期
# 绑定成功
# AC1进入实例模式下，通过命令show running-config  current-mode可以看到三条free-resources规则：
# free-resource 1
# free-resource 2                                                                                                                   
# free-resource 3  
################################################################################
printStep(testname,'Step 2','bind free-resource to configuration 1')
res1=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'free-resource 2')
SetCmd(switch1,'free-resource 3')
data = SetCmd(switch1,'show run c')
res1 = CheckLine(data,'free-resource 1','free-resource 2','free-resource 3',ML=True)
#result
printCheckStep(testname, 'Step 2',res1)
################################################################################
#Step 3
#操作
#客户端STA1连接到网络Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端获取到192.168.X.X(Dhcp_pool1)网段的地址
################################################################################
printStep(testname,'Step 3','STA1 connect to test1')
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res1 == 0:
    res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
#result
printCheckStep(testname, 'Step 3',res1,res2)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 4
    #操作
    # STA1与PC1通信
    # STA1与free-resources 1对应的ip地址通信
    # STA1与free-resources 2对应的ip地址通信
    # STA1与free-resources 3对应的ip地址通信
    #预期
    # STA1无法ping通 PC1(PC1的ip地址是个变量：pc1_ipv4 = '192.168.10.'+EnvNo+'2')
    # STA1可以ping通free-resource 1对应的ip地址（该地址为portal服务器地址，是变量）
    # STA1可以ping通free-resource 2对应的ip地址（该地址为BW地址，是变量）
    # STA1可以ping通free-resource 3对应的ip地址（该地址为S3的地址，是变量）
    ################################################################################
    printStep(testname,'Step 4',\
                        'sta1 ping pc1 failed',\
                        'sta1 ping free-resource 1 successully',\
                        'sta1 ping free-resource 2 successully',\
                        'sta1 ping free-resource 3 successully')
    res1=res2=res3=1
    # operate
    IdleAfter(10)
    res1 = CheckPing(sta1,pc1_ipv4,mode='linux')
    res1 = 0 if res1 != 0 else 1
    res2 = CheckPing(sta1,Radius_server,mode='linux')
    res3 = CheckPing(sta1,BW_server,mode='linux')
    res4 = CheckPing(sta1,If_vlan192_s3_ipv4,mode='linux')
    #result
    printCheckStep(testname, 'Step 4',res1,res2,res3,res4)
    ################################################################################
    #Step 5
    #操作
    # 删除所有的free-resource 
    # AC1(config)#captive-portal                                                                                                       
    # AC1(config-cp)#configuration 1                                                                                                   
    # AC1(config-cp-instance)#no free-resource 1                                                                                    
    # AC1(config-cp-instance)#no free-resource 2                                                                                      
    # AC1(config-cp-instance)#no free-resource 3                                                                                      
    # AC1(config-cp-instance)#quit                                                                                                     
    # AC1(config-cp)#no free-resource  1                                                                                               
    # AC1(config-cp)#no free-resource  2                                                                                               
    # AC1(config-cp)#no free-resource  3 
    #预期
    # 删除成功
    # AC1上面通过命令show captive-portal  free-resource status查看提示：
    # No free resource rule configured! 
    ################################################################################
    printStep(testname,'Step 5','delete all free-resource and check')
    # opertate
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'configuration 1')
    SetCmd(switch1,'no free-resource 1')
    SetCmd(switch1,'no free-resource 2')
    SetCmd(switch1,'no free-resource 3')
    SetCmd(switch1,'exit')
    SetCmd(switch1,'no free-resource 1')
    SetCmd(switch1,'no free-resource 2')
    SetCmd(switch1,'no free-resource 3')

    data = SetCmd(switch1,'show captive-portal free-resource status')
    res1 = CheckLine(data,'No free resource rule configured')
    #result
    printCheckStep(testname, 'Step 5',res1)
    ################################################################################
    #Step 6
    #操作
    # STA1与portal服务器对应的ip地址通信
    # STA1与BW对应的ip地址通信
    # STA1与S3对应的ip地址通信
    #预期
    # STA1无法ping通portal服务器
    # STA1无法ping通BW
    # STA1无法ping通S3
    ################################################################################
    printStep(testname,'Step 6',\
                        'sta1 ping free-resource 1 failed',\
                        'sta1 ping free-resource 2 failed',\
                        'sta1 ping free-resource 3 failed')
    res1=res2=res3=1
    # operate
    IdleAfter(10)
    res1 = CheckPing(sta1,Radius_server,mode='linux')
    res2 = CheckPing(sta1,BW_server,mode='linux')
    res3 = CheckPing(sta1,If_vlan192_s3_ipv4,mode='linux')
    res1 = 0 if res1 != 0 else 1
    res2 = 0 if res2 != 0 else 1
    res3 = 0 if res3 != 0 else 1
    #result
    printCheckStep(testname, 'Step 6',res1,res2,res3)
else:
    # 清空step1配置
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'configuration 1')
    SetCmd(switch1,'no free-resource 1')
    SetCmd(switch1,'no free-resource 2')
    SetCmd(switch1,'no free-resource 3')
    SetCmd(switch1,'exit')
    SetCmd(switch1,'no free-resource 1')
    SetCmd(switch1,'no free-resource 2')
    SetCmd(switch1,'no free-resource 3')
################################################################################
#Step 7
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 7',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'free-resource 1 destination ipv4 ' + Radius_server +'/32 source any')
SetCmd(switch1,'configuration 1 ')
SetCmd(switch1,'free-resource 1')
#end
printTimer(testname, 'End')