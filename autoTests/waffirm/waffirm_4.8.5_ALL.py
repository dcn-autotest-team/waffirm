#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.8.5.py - test case 4.8.5 of waffirm
#
# Author: 
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 4.8.5	Captive-Portal url-filter白名单
# 测试目的：未通过Portal认证的用户可以访问白名单网址
# 测试环境：同测试拓扑
# 测试描述：AC1配置Portal方式认证，STA关联到SSID后不认证通过也能正常访问白名单网址
#
#*******************************************************************************
# Change log:
#     - - creadte by zhangjxp 2017.5.27
#     - zhangjxp 2017.12.4 RDM50486 适配WAVE3项目
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 4.8.5'
avoiderror(testname)
printTimer(testname,'Start','Test 4.8.5	Captive-Portal url-filter whilelist')
def Ap_check_whitelistip(ap,apcmdtype,cmd,ip,failflag=False):
    res = 1
    retry = 3 if failflag==False else 1
    for i in range(retry):
        data1 = ApSetcmd(ap,apcmdtype,cmd)
        if apcmdtype == 'set':
            data2 = SetCmd(ap,'dmesg -c',timeout=30)
            res = CheckLine(data2,
                            'on vap: '+vap+', whitelist ip address',
                            'rule number: 1.*ip:\s*'+ip,
                            ML=True,IC=True)
        elif apcmdtype == 'uci':
            res = CheckLine(data1,ip)
        else:
            pass
        if res == 0:
            break
    return res
                            
# 2.4G、5G差异化配置,test24gflag为True代表执行2.4G脚本，False代表执行5G脚本
if test24gflag:
    vap='0'
else:
    vap='16'
###############################################################################
#Step 1
#操作
#在AC1配置network1的SSID为test1，关联vlan4091，配置下发到AP1，
#配置Radius服务器
#配置外置Portal,配置下发到AP1
#
#
#预期
#配置成功
################################################################################
printStep(testname,'Step 1',
          'Config Extrnal portal Configuration on AC1')
res1=1
# operate
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
SetCmd(switch1,'authentication-type external')
SetCmd(switch1,'external portal-server server-name eportal ipv4 ' + Radius_server)
SetCmd(switch1,'free-resource 1 destination ipv4 ' + Radius_server +'/32 source any')
SetCmd(switch1,'configuration 1 ')
SetCmd(switch1,'enable')
SetCmd(switch1,'radius accounting ')
SetCmd(switch1,'protocol http')
SetCmd(switch1,'radius-acct-server wlan')
SetCmd(switch1,'radius-auth-server wlan')
SetCmd(switch1,'redirect attribute ssid enable ')
SetCmd(switch1,'redirect attribute nas-ip enable')
SetCmd(switch1,'redirect attribute url-after-login enable   ')
SetCmd(switch1,'redirect attribute apmac enable')
SetCmd(switch1,'redirect attribute usermac enable')
SetCmd(switch1,'ac-name 0100.0010.0'+EnvNo+'0.01')
SetCmd(switch1,'redirect url-head http://192.168.10.101/a79.htm')
SetCmd(switch1,'portal-server ipv4 eportal')
SetCmd(switch1,'free-resource 1')
SetCmd(switch1,'interface ws-network 1')

# check
IdleAfter(3)
SetCmd(ap1,'\n')
# SetCmd(ap1,'cp_debug vap_config')
ApSetcmd(ap1,Ap1cmdtype,'cp_debug vap_config')
data=SetCmd(ap1,'dmesg -c',timeout=25)
# print 'data=',data
# 不同型号AP打印有差异，不再对res1进行检测
# res1=CheckLine(data, \
				# 'Portal Enable\s+: Enabled', \
				# 'VAP free resource rule 1', \
				# 'source ip: 0.0.0.0', \
				# 'source mask: 0.0.0.0', \
				# 'destination ip: '+Radius_server , \
				# 'destination mask: 255.255.255.255', \
				# ML=True,IC=True)	
res1=0				
#result
printCheckStep(testname, 'Step 1',res1)
###############################################################################
#Step 2
#操作
#AC1上添加两条url-filter白名单资源，并将资源应用到Portal
#
#
#预期
#配置成功。在AC1上面show url-filter status可以看到Rule ID为1的资源与host
# 名称设置相同，并且action为permit
################################################################################
printStep(testname,'Step 2',
          'Add two url-filter whitelist on AC1 and apply to portal')
res1=res2=res3=res4=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'url-filter permit 1 web1.dcntest.com')
SetCmd(switch1,'url-filter permit 2 *.abc.com')
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'configuration 1 ')
SetCmd(switch1,'url-filter permit 1')
SetCmd(switch1,'url-filter permit 2')
# check
EnterEnableMode(switch1)
data = SetCmd(switch1,'show url-filter status',timeout=5)
# print 'data=',data
res1 = CheckLineList(data,[('1','web1.dcntest.com','permit')])
res2 = CheckLineList(data,[('2',r'\*.abc.com','permit')])

# SetCmd(ap1,'\n')
# data1=SetCmd(ap1,'iwconfig ath16',timeout=2)
# checkflag=CheckLine(data1,'No such',IC=True)
IdleAfter(20)
for i in range(3):
    # SetCmd(ap1,'cp_debug whitelist_hostname')
    data1 = ApSetcmd(ap1,Ap1cmdtype,'cp_debug whitelist_hostname')
    if Ap1cmdtype == 'set':
        data2 = SetCmd(ap1,'dmesg -c',timeout=30)
        res3=CheckLine(data2,
                       'on vap: '+vap+', whitelist hostname rule',
                       'rule number: 1, hostname: web1.dcntest.com',
                       r'rule number: 2, hostname: \*.abc.com',
                       ML=True,IC=True)
    elif  Ap1cmdtype == 'uci':
        res3 = CheckLineList(data1,[('web1.dcntest.com'),('\*.abc.com')])
    else:
        pass
    if res3 == 0:
        break

#result
printCheckStep(testname, 'Step 2',res1,res2,res3)
################################################################################
#Step 3
#操作
#客户端STA1连接到网络test1
#
#预期
#成功关联，并获取192.168.91.X网段的IP地址。Show wireless client summery可以看到
# STA1（“MAC Address”显示“STA1MAC”），IP地址的网段正确。
################################################################################

printStep(testname,'Step 3',
          'STA1 connect to test1')
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,checkDhcpAddress=Netcard_ipaddress_check,bssid=ap1mac_lower)
IdleAfter(10)

EnterEnableMode(switch1)
data=SetCmd(switch1,'show wireless client summary')
res2=CheckLine(data,sta1mac)
#result
printCheckStep(testname, 'Step 3',res1,res2)
# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 4
    #操作
    #STA1未认证通过，使用浏览器访问web1.test.com。
    #
    #预期
    #web1.test.com可以打开。
    # 在AP上使用以下两个命令查询：
    # cp_debug whitelist_ip
    # dmesg –c
    # 可以看到
    # on vap: 0, whitelist ip address:
    # rule number: 1, ip: 200.1.1.102

    ################################################################################

    printStep(testname,'Step 4',
              'sta1 doesn\'t auth',
              'sta1 can open whitelist: web1.dcntest.com')
    res1=res2=res3=res4=1
    #operate
    title='Apache HTTP Server Test Page powered by CentOS'
    web = web_init(sta1_host)
    if None != web:
        res1 = web_open(web,'http://web1.dcntest.com:90')
        if res1['status']:
            res2=checktitle(web,title)
            if res2['status']:
                res3 = 0
            else:
                res3 = 1
                printRes('fail to get title')
    else:
        res3 =1
        printRes('web_init(sta1) status false')

    # i=0
    # while i<5:
        # IdleAfter(20)
        # SetCmd(ap1,'\n')
        # # SetCmd(ap1,'cp_debug whitelist_ip')
        # ApSetcmd(ap1,Ap1cmdtype,'cp_debug whitelist_ip')
        # data=SetCmd(ap1,'dmesg -c',timeout=30)
        # # print 'data=',data
        # if Ap1cmdtype == 'set':
            # res4=CheckLine(data, \
                            # 'on vap: '+vap+', whitelist ip address', \
                            # 'rule number: 1.*ip: 192.168.10.12', \
                            # ML=True,IC=True)
        # elif Ap1cmdtype == 'uci':
            # res4 = CheckLine(data,'192.168.10.12')
        # else:
            # pass
        # if res4==0:
            # break
        # i=i+1
    # 为适配不同型号AP的不同命令行，将检查whitelist ip封装为函数：
    res4 = Ap_check_whitelistip(ap1,Ap1cmdtype,'cp_debug whitelist_ip','192.168.10.12')
    #result			
    printCheckStep(testname, 'Step 4',res3,res4)

    res1 = web_close(web)
    printRes(res1)
    if not res1['status']:
        CMDKillFirefox(sta1)
    ################################################################################
    #Step 5
    #操作
    #STA1再使用浏览器访问web2.test.com
    #
    #预期
    #web2.test.com无法打开。
    # 在AP上使用以下两个命令查询：
    # cp_debug whitelist_ip
    # dmesg –c
    # vap 0上看不到web2的IP记录。
    ################################################################################

    printStep(testname,'Step 5',
              'sta1 doesn\'t auth',
              'sta1 can not open url that is not in whitelis')
    res1=res2=res3=res4=1
    #operate
    web = web_init(sta1_host)
    if None != web:
        res1 = web_open(web,'http://web2.dcntest.com:90')
        if not res1['status']:
            res2=checktitle(web,title)
            if res2['status']:
                res3 = 1
            else:
                res3 = 0
                printRes('fail to open web2.dcntest.com:')
        else:
            res3=0
    else:
        res3 =1
        printRes('web_init(sta1) status false')

    IdleAfter(30)
    SetCmd(ap1,'\n')
    # SetCmd(ap1,'cp_debug whitelist_ip')
    # data=SetCmd(ap1,'dmesg -c',timeout=30)
    # # print 'data=',data
    # res4=CheckLine(data, \
                    # 'on vap: '+vap+', whitelist ip address', \
                    # 'rule number: 1.*ip: 192.168.10.22', \
                    # ML=True,IC=True)
                    
    res4 = Ap_check_whitelistip(ap1,Ap1cmdtype,'cp_debug whitelist_ip','192.168.10.22',failflag=True)
    res4 = 0 if res4 != 0 else 1
    printCheckStep(testname, 'Step 5',res3,res4)

    res1 = web_close(web)
    printRes(res1)
    if not res1['status']:
        CMDKillFirefox(sta1)
    ################################################################################
    #Step 6
    #操作
    #STA1再使用浏览器访问web3.abc.com。
    #
    #预期
    #web3.abc.com可以打开。
    # 在AP上使用以下两个命令查询：
    # cp_debug whitelist_ip
    # dmesg –c
    # 可以看到
    # on vap: 0, whitelist ip address:
    # rule number: 1, ip: 200.1.1.103

    ################################################################################

    printStep(testname,'Step 6',
              'sta1 doesn\'t auth',
              'sta1 can open whitelist: web3.abc.com')
    res1=res2=res3=res4=1
    #operate
    web = web_init(sta1_host)
    if None != web:
        res1 = web_open(web,'http://web3.abc.com:90')
        if res1['status']:
            res2=checktitle(web,title)
            if res2['status']:
                res3 = 0
            else:
                res3 = 1
                printRes('fail to get title')
    else:
        res3 =1
        printRes('web_init(sta1) status false')

    # i=0
    # while i<3:
        # IdleAfter(20)
        # SetCmd(ap1,'\n')
        # SetCmd(ap1,'cp_debug whitelist_ip')
        # data=SetCmd(ap1,'dmesg -c',timeout=30)
        # # print 'data=',data
        # res4=CheckLine(data, \
                        # 'on vap: '+vap+', whitelist ip address', \
                        # 'rule number: 1.*ip: 192.168.10.32', \
                        # ML=True,IC=True)
        # if res4==0:
            # break
        # i=i+1
    res4 = Ap_check_whitelistip(ap1,Ap1cmdtype,'cp_debug whitelist_ip','192.168.10.32')
    # result
    printCheckStep(testname, 'Step 6',res3,res4)
    # 关闭firefox窗口
    res1 = web_close(web)
    printRes(res1)
    if not res1['status']:
        CMDKillFirefox(sta1)
# ################################################################################
# #Step 7
# #操作
# #恢复默认配置
################################################################################
printStep(testname,'Step 7',
          'Recover initial config for switches.')

#operate

WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)

EnterConfigMode(switch1)
SetCmd(switch1,'captive-portal')
SetCmd(switch1,'disable')
SetCmd(switch1,'no configuration 1')
SetCmd(switch1,'no external portal-server ipv4 server-name eportal')
SetCmd(switch1,'no free-resource 1')
EnterConfigMode(switch1)
SetCmd(switch1,'no url-filter permit all',promotePatten='Y/N',promoteTimeout=10)
IdleAfter(1)
Receiver(switch1,'y')
SetCmd(switch1,'no radius source-ipv4')
SetCmd(switch1,'no radius-server key')
SetCmd(switch1,'no aaa group server radius wlan')
SetCmd(switch1,'no radius nas-ipv4')
SetCmd(switch1,'no aaa enable')
SetCmd(switch1,'no aaa-accounting enable')
SetCmd(switch1,'no radius-server authentication host ' + Radius_server)
SetCmd(switch1,'no radius-server accounting host ' + Radius_server)

#end
printTimer(testname, 'End')