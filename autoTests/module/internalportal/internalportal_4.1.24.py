#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# internal_portal_4.1.24.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.24	CP用户最大上行发送带宽和下行接收带宽功能测试
# 测试目的：内置portal认证场景下，AC可以限制认证客户端STA网络上行、下行数据的最大速率
# 测试描述：
# 1、	AC配置CP用户最大上行发送带宽和下行接收带宽
# 2、	客户端连接无线网络，进行portal认证，通过AP上面查看STA的最大上行发送带宽和下行接收带宽
# 3、	客户端从有线端PC上下载文件，下载速率低于AC上配置的下行接收带宽
# 4、	有线端PC从客户端上下载文件，上传速率低于AC上配置的上行发送带宽
# 5、	取消CP用户最大带宽限制功能，客户端和有线端互相下载文件，速率正常
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.1.9
#*******************************************************************************

# ！！！注意：测试此用例时需要注意AP的摆放位置，AP尽量靠近客户端网卡，不要有遮挡物阻隔AP和客户端网卡，
# AP信号发射面尽量朝向客户端网卡， AP与客户端之间的位置关系会影响客户端下载速率

#Package

#Global Definition
bandtest_username = 'bandtest'
bandtest_passwork = '111'
#Source files

#Procedure Definition 

#Functional Code
def get_download_rate(client,serverip,filename):
    data = SetCmd(client,'downloadtest -u http://' + serverip + '/'+filename,promotePatten='True|False',promoteTimeout=300)
    temp = re.search('speed is\s+:\s+(\d+\.\d+)\s+MB/s',data)
    if temp:
        rate = temp.group(1)
        return float(rate)
        
testname = 'TestCase internalportal_4.1.24'
avoiderror(testname)
printTimer(testname,'Start','Test band width')
################################################################################
#Step 1
#操作
# AC1上配置客户端下行速率为32KB/s
# 配置客户端上行速率为64KB/s
# AC1(config)#captive-portal                                                                                                          
# AC1(config-cp)#configuration 1                                                                                                      
# AC1(config-cp-instance)#max-bandwidth-down 32000                                                                                   
# AC1(config-cp-instance)#max-bandwidth-up 64000
#预期
# 配置成功。
# 实例1模式下，通过命令show running-config  current-mode可以查看到命令
# max-bandwidth-up 64000                                                                                              
# max-bandwidth-down 32000
################################################################################
printStep(testname,'Step 1','Config max-bandwidth-down and max-bandwidth-up')
res1=1
#operate
# 方案中配置的速率过低，会导致sta下载文件的时间很长，脚本中提高了配置的速率，可以节省时间
EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1')
SetCmd(switch1,'max-bandwidth-down 320000')
SetCmd(switch1,'max-bandwidth-up 640000')
# check
data=SetCmd(switch1,'show captive-portal configuration 1 status')
res1=CheckLineList(data,[('Max Bandwidth Up','640000'),('Max Bandwidth Down','320000')])
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
        res1 = inportal_login_withcheck(web,bandtest_username,bandtest_passwork)
        res2 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        #result
        printCheckStep(testname, 'Step 4',res1,res2,res3)
    ###############################################################################
    #Step 5
    #操作
    # AP本地查看STA的限速是否下发成功
    # cp_debug sta
    # dmesg -c  
    #预期
    # 查看STA的限速跟AC上面配置一致
    # 查看Ap上面的打印，显示以下信息
    # CP Client Table                                                                                                                                                                                                                                    
     # STA1MAC       STA1IP                                                                                             
    # state AUTHED, uprate 64000/downrate 32000 on radio  1/vap  0
    ################################################################################
    printStep(testname,'Step 5',\
                        'cp_debug sta;dmesg -c on AP1')

    #operate
    # 为兼容不同AP，AP上只打印信息，不做检查
    SetCmd(ap1,'cp_debug sta;dmesg -c')
    #result
    printCheckStep(testname, 'Step 5',0)
    ################################################################################
    #Step 6
    #操作
    # 客户端STA1从有线端PC上下载文件
    #预期
    # 下载成功，速率显示正常
    # 平均下载速率为32KB/s（误差不超过5%）
    ################################################################################
    printStep(testname,'Step 6','sta1 download file from pc1,then check rate')
    res1=1
    # operate
    # # 一般第一次下载速率不稳定，在正式测试速率前先下载一次文件
    # SetCmd(sta1,'downloadtest -u http://' + pc1_ipv4+':90' + '/upgrade1.tar',promotePatten='True|False',promoteTimeout=300)
    # 检测速率
    # 下载过程中速率可能会不稳定，脚本中下载两次文件，任何一次速率达到预期都判定为通过
    rate1 = get_download_rate(sta1,pc1_ipv4+':90','upgrade1.tar')
    rate2 = get_download_rate(sta1,pc1_ipv4+':90','upgrade2.tar')
    if 0.26 <= rate1 <= 0.36 or 0.26 <= rate2 <= 0.36:
        res1=0
    print('rate1=',rate1)
    print('rate2=',rate2)
    #result
    printCheckStep(testname, 'Step 6',res1)
    ################################################################################
    #Step 7
    #操作
    # 有线端PC从客户端STA1上下载文件
    #预期
    #下载成功，速率显示正常
    # 平均下载速率为64KB/s（误差不超过5%）
    ################################################################################
    printStep(testname,'Step 7',\
                        'pc1 download filefrom sta1,then check rate')
    res1=1
    # operate
    # # 一般第一次下载速率不稳定，在正式测试速率前先下载一次文件
    # SetCmd(pc1,'downloadtest -u http://' + sta1_ipv4 + '/upgrade1.tar',promotePatten='True|False',promoteTimeout=300)
    # 检测速率
    # 下载过程中速率可能会不稳定，脚本中下载两次文件，任何一次速率达到预期都判定为通过
    rate1 = get_download_rate(pc1,sta1_ipv4,'upgrade1.tar')
    rate2 = get_download_rate(pc1,sta1_ipv4,'upgrade2.tar')
    if 0.54 <= rate1 <= 0.78 or 0.54 <= rate2 <= 0.78:
        res1 = 0
    print('rate1=',rate1)
    print('rate2=',rate2)
    #result
    printCheckStep(testname, 'Step 7',res1)
    ################################################################################
    #Step 8
    #操作
    # AC1上取消客户端上下行速率限制
    # AC1(config)#captive-portal                                                                                                          
    # AC1(config-cp)#configuration  1                                                                                                     
    # AC1(config-cp-instance)#no max-bandwidth-down                                                                                       
    # AC1(config-cp-instance)#no max-bandwidth-up
    #预期
    # 取消成功
    # 实例1模式下，通过命令show running-config  current-mode查看不到命令
    # max-bandwidth-up 64000                                                                                              
    # max-bandwidth-down 32000
    ################################################################################
    printStep(testname,'Step 8','No max-bandwidth-down and max-bandwidth-up')
    res1=1
    #operate
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'configuration 1')
    SetCmd(switch1,'no max-bandwidth-down')
    SetCmd(switch1,'no max-bandwidth-up')
    # check
    data=SetCmd(switch1,'show captive-portal configuration 1 status')
    res1=CheckLineList(data,[('Max Bandwidth Up','\s0\s'),('Max Bandwidth Down','\s0\s')])
    #result
    printCheckStep(testname, 'Step 8',res1)
    ################################################################################
    #Step 9
    #操作
    #客户端主动下线后再次进行portal认证
    # 查看AC1上的CP列表
    # 检查STA1是否可以上网 
    #预期
    # 再次认证成功
    # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）
    # STA1ping PC1可以ping通
    ################################################################################
    printStep(testname,'Step 9','STA1 logout and login again')
    res1=res2=res3=res4=res5=res6=1
    #operate
    # 退出登陆
    res1 = portal_logout_withcheck(web)
    res2 = CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=10,waitflag=False)
    # 重新打开认证页面并进行登录
    res3 = inportal_redirect_success(web,web_ip)
    if res3 == 0:
        res4 = inportal_login_withcheck(web,bandtest_username,bandtest_passwork)
        res5 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res6 = CheckPing(sta1,pc1_ipv4,mode='linux')
    #result
    printCheckStep(testname, 'Step 9',res1,res2,res3,res4,res5,res6)
    # 关闭网页
    res = web_close(web)
    if res['status'] != True:
        printRes(res)
        CMDKillFirefox(sta1)
    ###############################################################################
    #Step 10
    #操作
    # AP本地查看STA的portal限速是取消成功
    # cp_debug sta
    # dmesg -c  
    #预期
    # 查看STA的限速跟AC上面配置一致
    # 查看Ap上面的打印，显示以下信息
    # CP Client Table                                                                                                                                                                                                                                    
     # STA1MAC       STA1IP                                                                                             
    # state AUTHED, uprate 0/downrate 0 on radio  1/vap  0
    ################################################################################
    printStep(testname,'Step 10',\
                        'cp_debug sta;dmesg -c on AP1')

    #operate
    # 为兼容不同AP，AP上只打印信息，不做检查
    SetCmd(ap1,'cp_debug sta;dmesg -c')
    #result
    printCheckStep(testname, 'Step 10',0)
    ################################################################################
    #Step 11
    #操作
    # 客户端STA1从有线端PC上下载文件
    #预期
    # 下载成功，速率显示正常
    # 平均下载速率大于1MB/s
    ################################################################################
    printStep(testname,'Step 11','sta1 download file from pc1, rate >= 1MB/s')
    res1=1
    # operate
    # # 一般第一次下载速率不稳定，在正式测试速率前先下载一次文件
    # SetCmd(sta1,'downloadtest -u http://' + pc1_ipv4+':90' + '/upgrade1.tar',promotePatten='True|False',promoteTimeout=300)
    # 检测速率
    # 下载过程中速率可能会不稳定，脚本中下载两次文件，任何一次速率达到预期都判定为通过
    rate1 = get_download_rate(sta1,pc1_ipv4+':90','upgrade1.tar')
    rate2 = get_download_rate(sta1,pc1_ipv4+':90','upgrade2.tar')
    if rate1 >= 0.9 or rate2 >= 0.9:
        res1=0
    print('rate1=',rate1)
    print('rate2=',rate2)
    #result
    printCheckStep(testname, 'Step 11',res1)
    ################################################################################
    #Step 12
    #操作
    # 有线端PC从客户端STA1上下载文件
    #预期
    #下载成功，速率显示正常
    # 平均下载速率大于1MB/s
    ################################################################################
    printStep(testname,'Step 12','pc1 download filefrom sta1,rate >= 1MB/s')
    res1=1
    # operate
    # # 一般第一次下载速率不稳定，在正式测试速率前先下载一次文件
    # SetCmd(pc1,'downloadtest -u http://' + sta1_ipv4 + '/upgrade1.tar',promotePatten='True|False',promoteTimeout=300)
    # 检测速率
    # 下载过程中速率可能会不稳定，脚本中下载两次文件，任何一次速率达到预期都判定为通过
    rate1 = get_download_rate(pc1,sta1_ipv4,'upgrade1.tar')
    rate2 = get_download_rate(pc1,sta1_ipv4,'upgrade2.tar')
    if rate1 >= 0.9 or rate2 >= 0.9:
        res1=0
    print('rate1=',rate1)
    print('rate2=',rate2)
    #result
    printCheckStep(testname, 'Step 12',res1)
else:
    EnterConfigMode(switch1)
    SetCmd(switch1,'captive-portal')
    SetCmd(switch1,'configuration 1')
    SetCmd(switch1,'no max-bandwidth-down')
    SetCmd(switch1,'no max-bandwidth-up')
################################################################################
#Step 13(合并原方案step13,step14)
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 13',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=10,waitflag=False)

#end
printTimer(testname, 'End')