#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# internal_portal_4.1.25.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.25	CP用户最大输入（发送字节）和最大输出（接收字节）功能测试
# 测试目的：内置portal认证场景下，如果AC上面配置了CP用户最大输入/发送字节和最大输出/接收字节，那么客户端通过认证后的上传、下载流量超过限制后,客户端自动下线
# 测试描述：
# 1、	AC上配置CP用户最大输入/发送字节和最大输出/接收字节
# 2、	客户端连接无线网络，进行portal认证
# 3、	客户端从有线端PC上下载文件，下载文件的大于CP用户最大输入/发送字节，CP用户下线
# 4、	有线端PC从客户端上下载文件，下载文件的大于CP用户最大输出/接收字节，CP用户下线
# 5、	取消CP用户的出流量和入流量限制，客户端和有线端互相下载文件，下载文件正常，客户端正常在线
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.9
#*******************************************************************************

# ！！！注意：实际测试中，从AC检测到客户端流量超标到强制客户端下线生效需要一定的时间，
# 在这段时间内客户端可能已经完成了文件的下载，因此脚本中不对文件是否下载成功做检查

#Package

#Global Definition
download_flag = 1
#Source files

#Procedure Definition 

#Functional Code
def check_download(client,serverip,filename):
    data = SetCmd(client,'downloadtest -u http://' + serverip + '/'+filename)
    temp = re.search('speed is\s+:\s+(\d+\.\d+)\s+MB/s',data)
    if temp:
        return 0
    else:
        return 1
testname = 'TestCase internalportal_4.1.25'
avoiderror(testname)
printTimer(testname,'Start','Test max-input-octets and max-output-octets')
################################################################################
#Step 1
#操作
# AC1上配置CP用户最大输入/发送字节为30MB最大输出/接收字节为20MB
# AC1(config)#captive-portal                                                                                                          
# AC1(config-cp)#configuration 1                                                                                                      
# AC1(config-cp-instance)# max-input-octets 31457280                                                                       
# AC1(config-cp-instance)# max-output-octets 20971520
#预期
# 配置成功。
# AC1上通过命令show captive-portal  configuration  1 status  可以查看到
# Max Input Octets为31457280
# Max Output Octets为20971520
################################################################################
printStep(testname,'Step 1','Config max-input-octets and max-output-octets')
res1=1
#operate
# 文件过大会导致下载时间很长，脚本中调整了下载文件的大小，同时相应调整了最大发送和接受字节配置
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1')
# 配置最大输入字节为15M
SetCmd(switch1,'max-input-octets 15728640')
# 配置最大输出字节为10M
SetCmd(switch1,'max-output-octets 10485760')
# check
data=SetCmd(switch1,'show captive-portal configuration 1 status')
res1 = CheckLineList(data,[('Max Input Octets','15728640'),('Max Output Octets','10485760')])
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
#获取STA1的地址
sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
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
        download_flag = res3
        #result
        printCheckStep(testname, 'Step 4',res1,res2,res3)
    # 关闭网页
    web_close(web)
    if download_flag == 0:
        ###############################################################################
        #Step 5
        #操作
        # 客户端STA1从有线端PC上下载30M的文件，查看文件下载是否成功，STA1是否仍然处于认证状态  
        #预期
        # 文件下载失败，STA1处于非认证状态
        # AC上面通过命令show captive-portal  client  status查看不到任何表项
        ################################################################################
        printStep(testname,'Step 5',\
                            'sta1 download file(15M) from pc1 failed',\
                            'sta1 is not in captive-portal  client list')
        res1=res2=1
        #operate
        # 脚本中改为下载大于15M的文件
        check_download(sta1,pc1_ipv4+':90','upgrade2.tar')
        IdleAfter(10)
        res2 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                        check=[(sta1mac)],retry=10,waitflag=False)
        #result
        printCheckStep(testname, 'Step 5',res2)
    ################################################################################
    #Step 6
    #操作
    # 客户端STA1重新进行portal认证
    # 查看AC1上的CP列表
    # 检查STA1是否可以上网 
    #预期
    # STA1输入正确的用户名和密码后认证成功
    # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）
    # STA1ping PC1可以ping通
    ################################################################################
    printStep(testname,'Step 6','sta1 login again')
    res1=res2=res3=res4=download_flag=1
    # operate
    web = web_init(sta1_host)
    res1 = inportal_redirect_success(web,web_ip)
    if res1 == 0:
        res2 = inportal_login_withcheck(web,portal_username,portal_password)
        res3 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res4 = CheckPing(sta1,pc1_ipv4,mode='linux')
        download_flag = res4
    #result
    printCheckStep(testname, 'Step 6',res1,res2,res3,res4)
    if download_flag == 0:
        ###############################################################################
        #Step 7
        #操作
        # 有线端PC从客户端STA1上下载20M的文件，查看文件下载是否成功，STA1是否仍然出入认证状态 
        #预期
        # 文件下载失败，STA1处于非认证状态
        # AC上面通过命令show captive-portal  client  status查看不到任何表项
        ################################################################################
        printStep(testname,'Step 7',\
                            'pc1 download file(10M) from sta1 failed',\
                            'sta1 is not in captive-portal  client list')
        res1=res2=1
        #operate
        # 脚本中改为下载大于10M的文件
        check_download(pc1,sta1_ipv4,'upgrade2.tar')
        IdleAfter(10)
        res2 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                        check=[(sta1mac)],retry=10,waitflag=False)
        #result
        printCheckStep(testname, 'Step 7',res2)
    ################################################################################
    #Step 8
    #操作
    # AC1上取消配置的CP用户最大输入、输出字节限制
    # AC1(config)#captive-portal                                                                                                          
    # AC1(config-cp)#configuration  1                                                                                                     
    # AC1(config-cp-instance)#no max-input-octets                                                                                      
    # AC1(config-cp-instance)#no max-output-octets
    #预期
    # 取消成功
    # AC1上通过命令show captive-portal  configuration  1 status查看
    # Max Output Octets为0
    # Max Total Octets为0
    ################################################################################
    printStep(testname,'Step 8','Config max-input-octets and max-output-octets')
    res1=1
    #operate
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'configuration 1')
    SetCmd(switch1,'no max-input-octets')
    SetCmd(switch1,'no max-output-octets')
    # check
    data=SetCmd(switch1,'show captive-portal configuration 1 status')
    res1 = CheckLineList(data,[('Max Input Octets','\s0\s'),('Max Output Octets','\s0\s')])
    #result
    printCheckStep(testname, 'Step 8',res1)
    ################################################################################
    #Step 9
    #操作
    # 客户端STA1重新进行portal认证
    # 查看AC1上的CP列表
    # 检查STA1是否可以上网 
    #预期
    # STA1输入正确的用户名和密码后认证成功
    # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）
    # STA1ping PC1可以ping通
    ################################################################################
    printStep(testname,'Step 9','sta1 login again')
    res1=res2=res3=res4=1
    # operate
    web = web_init(sta1_host)
    res1 = inportal_redirect_success(web,web_ip)
    if res1 == 0:
        res2 = inportal_login_withcheck(web,portal_username,portal_password)
        res3 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res4 = CheckPing(sta1,pc1_ipv4,mode='linux')
        download_flag = res4
    #result
    printCheckStep(testname, 'Step 9',res1,res2,res3,res4)
    if download_flag == 0:
        ################################################################################
        #Step 10
        #操作
        # 客户端STA1从有线端PC上下载30M的文件，查看文件下载是否成功，STA1是否仍然处于认证状态
        #预期
        # 文件下载成功，STA1处于认证状态
        # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）
        # STA1ping PC1可以ping通
        ################################################################################
        printStep(testname,'Step 10',\
                            'sta1 download file(15M) from pc1 successully',\
                            'sta1 is still in captive-portal  client list')
        res1=res2=res3=1
        #operate
        res1 = check_download(sta1,pc1_ipv4+':90','upgrade2.tar')
        IdleAfter(10)
        res2 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        download_flag = res3
        #result
        printCheckStep(testname, 'Step 10',res1,res2,res3)
        if download_flag == 0:
            ###############################################################################
            #Step 11
            #操作
            # 有线端PC从客户端STA1上下载20M的文件，查看文件下载是否成功，STA1是否仍然出入认证状态 
            #预期
            # 文件下载成功，STA1处于认证状态
            # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）
            # STA1ping PC1可以ping通
            ################################################################################
            printStep(testname,'Step 11',\
                                'pc1 download file(10M) from sta1 successully',\
                                'sta1 is still in captive-portal  client list')
            res1=res2=res3=1
            #operate
            res1 = check_download(pc1,sta1_ipv4,'upgrade.tar')
            IdleAfter(10)
            res2 = CheckSutCmd(switch1,'show captive-portal client status',\
                                        check=[(sta1mac)],retry=5,waitflag=False)
            res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
            #result
            printCheckStep(testname, 'Step 11',res1,res2,res3)
else:
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'configuration 1')
    SetCmd(switch1,'no max-input-octets')
    SetCmd(switch1,'no max-output-octets')
################################################################################
#Step 12(合并原方案step12,step13)
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 12',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
CMDKillFirefox(sta1)
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)

#end
printTimer(testname, 'End')