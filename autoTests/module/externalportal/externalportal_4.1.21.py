#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# external_portal_4.1.21.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.1.21	外置portal认证场景下的流量统计功能
# 测试目的：客户端通过外置portal认证成功后，通过AC查看客户端的流量统计正确
# 测试描述：
# 1.	客户端连接网络后成功进行portal认证。
# 2.	客户端从有线端PC上下载10M文件，通过AC查看对应的流量统计正常
# 3.	有线端PC从客户端上下载20M文件，通过AC查看对应的流量统计正常
# 测试环境：见测试环境拓扑图1
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.25
#*******************************************************************************

#Package

#Global Definition
download_flag = 1
#Source files

#Procedure Definition 

#Functional Code
def get_sta_statistics(switch,stamac,staip,type):
    data = SetCmd(switch,'show captive-portal client '+stamac+' ipv4 '+staip+' statistics')
    if type == 'Transmitted':
        temp = re.search('Bytes Transmitted.*?(\d+)\s',data)
    if type == 'Received':
        temp = re.search('Bytes Received.*?(\d+)\s',data)
    if temp:
        byte = int(temp.group(1))
        return byte
def check_download(client,serverip,filename):
    data = SetCmd(client,'downloadtest -u http://' + serverip + '/'+filename)
    temp = re.search('speed is\s+:\s+(\d+\.\d+)\s+MB/s',data)
    if temp:
        return 0
    else:
        return 1        
testname = 'TestCase externalportal_4.1.21'
avoiderror(testname)
printTimer(testname,'Start','Test traffic statistics')
################################################################################
#Step 1
#操作
#客户端STA1连接到网络Network_name1
#预期
# 关联成功。
# 通过命令show wireless  client  summary可以查看客户端获取到192.168.X.X(Dhcp_pool1)网段的地址
################################################################################
printStep(testname,'Step 1','STA1 connect to test1')
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_type1)
if res1 == 0:
    res2 = CheckWirelessClientOnline(switch1,sta1mac,'online')
sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
#result
printCheckStep(testname, 'Step 1',res1,res2)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 2
    #操作
    # 客户端STA1打开web页面访问1.1.1.1（该地址为变量web_ip）
    #预期
    # STA1上可以看到重定向页面，并且提示输入用户名和密码
    ################################################################################
    printStep(testname,'Step 2','sta1 open 1.1.1.1 and can redirect to portal auth page')
    res1=1
    # operate
    # sta1打开1.1.1.1，并检查是否重定向到外置portal认证页面
    web = web_init(sta1_host)
    res1 = exportal_redirect_success(web,web_ip)
    #result
    printCheckStep(testname, 'Step 2',res1)
    if res1 == 0:
        ################################################################################
        #Step 3
        #操作
        # 客户端STA1在推送出的重定向页面输入正确的用户名和密码进行认证
        # portal认证用户名：portal_username = ‘aaa’
        # portal认证密码：portal_password = ‘111
        #预期
        # STA1认证成功
        # 通过show captive-portal  client  status命令查看CP client列表，显示出STA1的信息（“MAC Address”显示“STA1MAC”）。
        # STA1ping PC1可以ping通
        ################################################################################
        printStep(testname,'Step 3',\
                            'input correct username and password',\
                            'login successully')
        res1=res2=res3=1
        # operate
        res1 = exportal_login_withcheck(web,portal_username,portal_password)
        res2 = CheckSutCmd(switch1,'show captive-portal client status',\
                                    check=[(sta1mac)],retry=5,waitflag=False)
        res3 = CheckPing(sta1,pc1_ipv4,mode='linux')
        download_flag = res3
        #result
        printCheckStep(testname, 'Step 3',res1,res2,res3)
    # 关闭网页
    res = web_close(web)
    if res['status'] != True:
        printRes(res)
        CMDKillFirefox(sta1)
    if download_flag == 0:
        ###############################################################################
        #Step 4
        #操作
        # 客户端STA1从有线端PC上下载10M文件，通过AC查看流量统计
        #预期
        # 下载成功，流量统计正确。
        # AC1上通过命令show captive-portal client STA1MAC STA1IP statistics可看到客户端的统计信息与实际相符
        # Bytes Transmitted大小为10M(误差为5%)
        ################################################################################
        printStep(testname,'Step 4','sta1 download file from pc1')
        res1=res2=1
        #operate
        res1 = check_download(sta1,pc1_ipv4+':90','upgrade.tar')
        IdleAfter(10)
        transmitted_bytes = get_sta_statistics(switch1,sta1mac,sta1_ipv4,type='Transmitted')
        if transmitted_bytes:
            # 脚本中误差控制在偏小不超过5%，偏大不超过10%，文件实际大小为14243840
            if 13531648 <= transmitted_bytes <= 15668224:
                res2 = 0
        #result
        printCheckStep(testname, 'Step 4',res1,res2)
        ###############################################################################
        #Step 5
        #操作
        # 有线端PC从客户端STA1上下载20M文件，通过AC查看流量统计
        #预期
        # 下载成功，流量统计正确。
        # AC1上通过命令show wireless client STA1MAC statistics查看无线流量统计正确
        # Bytes Transmitted大小为10M(误差为5%)
        # Bytes Received大小为20M(误差为5%)
        ################################################################################
        printStep(testname,'Step 5','pc1 download file from sta1')
        res1=res2=1
        #operate
        res1 = check_download(pc1,sta1_ipv4,'upgrade2.tar')
        IdleAfter(10)
        transmitted_bytes = get_sta_statistics(switch1,sta1mac,sta1_ipv4,type='Received')
        if transmitted_bytes:
            # 脚本中误差控制在偏小不超过5%，偏大不超过10%，文件实际大小为20072448
            if 19068826 <= transmitted_bytes <= 22079693:
                res2 = 0
        #result
        printCheckStep(testname, 'Step 5',res1,res2)

################################################################################
#Step 6
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 6',\
          'Recover initial config for switches.')

#operate
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

CheckSutCmdWithNoExpect(switch1,'show captive-portal client status',\
                        check=[(sta1mac)],retry=15,waitflag=False)
#end
printTimer(testname, 'End')