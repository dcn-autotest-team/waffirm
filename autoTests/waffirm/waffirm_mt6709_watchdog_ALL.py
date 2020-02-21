# -*- coding: UTF-8 -*-#
#
# *******************************************************************************
# waffirm_mt6709_watchdog.py
#
# Author:  (zhangjxp)
#
# Version 1.0.0
#
# Date:  2017-7-25 9:54:28
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# MT6709：AP的watchdog功能优化（mapd与mapqosd自动重启）测试
# 测试目的：mapd或者mapqosd进程在挂掉或者阻塞后会自动重新启动。Mapd重启后AP会重新上线，
# mapqod重启后，AP不会下线，client不会下线。Mapd和mapqosd的重启都会在/etc/watchdog_log
# 下面产生文件restartlog记录重启事件
# 测试环境：同测试拓扑
# 测试描述：问题最初的原因是，客户现场8200I2的AP发生了mapqosd的进程的重启，
# 但是watchdog、coredump、crashdump等目录下没有任何记录，只有watchdog_log下有
# mapqosd pending的记录，并且mapqosd的重启会导致AP也重启，影响用户体验。
# 优化后的watchdog功能实现了mapd和mapqosd进程的自动重启，不重启AP，降低对用户的影响
#
# *******************************************************************************
# Change log:
#     - creadte by zhangjxp 2017.7.25
#     - modified by zhangjxp 2017.11.8 RDM50323 
# *******************************************************************************
# Package

# Global Definition

# Source files

# Procedure Definition

# Functional Code

testname = 'TestCase mt6709_watchdog'
avoiderror(testname)
printTimer(testname, 'Start')

################################################################################
# Step 1
#
# 操作（合并方案的step1、2)
# 登陆AP1，敲killall -9 mapd，AP打印“dman: mapd exited .... dman: Starting mapd ....”之后，
# mapd进程重新启动，Mapd重启启动会引起AP下线，等待一段时间后，检查AP是否会重新上线
#
# 预期
# ps检查mapd进程重新启动OK，AP1重新上线成功，ps检查mapd进程在运行
################################################################################
printStep(testname, 'Step 1', 'killall -9 mapd, mapd restart and AP don\'t restart')
res1 = res2 = res3 = res4 = res5 = 1
# operate
# 设置AC和AP保活时间，使AP重启时尽快被发现
EnterWirelessMode(switch1)
SetCmd(switch1, 'keep-alive-interval 5000')
# AP1配置
# 检查AP1 mapd进程是否运行
SetCmd(ap1, '\n')
data1 = SetCmd(ap1, 'ps | grep mapd', timeout=5)
res1 = CheckLine(data1, '/usr/sbin/mapd', IC=True)
# kill mapd进程
StartDebug(ap1)
SetCmd(ap1, 'killall -9 mapd')
# 检查AP是否下线
IdleAfter(17)
EnterEnableMode(switch1)
data1 = SetCmd(switch1, 'show wireless ap status')
res = CheckLine(data1, ap1mac, Ap1_ipv4, '1', 'Failed', 'Not\s+Config', IC=True)
IdleAfter('60')
data = StopDebug(ap1)
# 检查mapd进程重启，AP不应重启
res2 = CheckLine(data, 'dman: mapd exited',
                 'dman: Starting mapd',
                 ML=True)
mapdflag = res2
res3 = CheckLine(data, 'Starting kernel')
# 如果mapd进程重启，检查AP是否重新上线
if res2 == 0:
    j = 0
    EnterEnableMode(switch1)
    while j < 20:
        data1 = SetCmd(switch1, 'show wireless ap status')
        res4 = CheckLine(data1, ap1mac, Ap1_ipv4, '1', 'Managed', 'Success', IC=True)
        if res4 == 0:
            break
        IdleAfter('5')
        j = j + 1
# 如果mapd进程重启使AP重启，则等待AP重启上线
if res3 == 0:
    IdleAfter(50)
    ApLogin(ap1, retry=20)
    IdleAfter(20)
    j = 0
    EnterEnableMode(switch1)
    while j < 20:
        data1 = SetCmd(switch1, 'show wireless ap status')
        res4 = CheckLine(data1, ap1mac, Ap1_ipv4, '1', 'Managed', 'Success', IC=True)
        if res4 == 0:
            break
        IdleAfter('5')
        j = j + 1
# 如果AP短时间内没有重启，mapd进程也没有重启，则自行重启AP
if res2 != 0 and res3 != 0:
    RebootAp(AP=ap1)
    j = 0
    EnterEnableMode(switch1)
    while j < 20:
        data1 = SetCmd(switch1, 'show wireless ap status')
        res4 = CheckLine(data1, ap1mac, Ap1_ipv4, '1', 'Managed', 'Success', IC=True)
        if res4 == 0:
            break
        IdleAfter('5')
        j = j + 1

SetCmd(ap1, '\n')
data1 = SetCmd(ap1, 'ps | grep mapd', timeout=5)
res5 = CheckLine(data1, '/usr/sbin/mapd', IC=True)
res3 = 0 if res3 != 0 else 1
# result
printCheckStep(testname, 'Step 1', res, res1, res2, res3, res4, res5)
################################################################################
# Step 2(对应方案step3)
# 操作
# 操作sta1接入AP1的network1,sta1 ping pc1对应环境的ip地址
#
# 预期
# client接入成功，获取了192.168.x.x的地址,sta1可以ping同pc1
################################################################################
printStep(testname, 'Step 2',
          'STA1 connect to network 1',
          'STA1 ping pc1',
          'STA1 dhcp and get ip address,'
          'sta1 ping pc1 success')
res1 = res2 = 1
# operate
# STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1, Netcard_sta1, Network_name1, bssid=ap1mac_lower, checkDhcpAddress=Dhcp_pool1)
res2 = CheckPing(sta1, pc1_ipv4, mode='linux', pingPara=' -c 10')
# result
printCheckStep(testname, 'Step 2', res1, res2)

################################################################################
# Step 3(合并方案step4,5)
# 操作
# 登陆AP1，敲killall -9 mapqosd，AP打印“dman: mapqosd exited .... 
# dman: Starting mapqosd ....”之后，mapqosd进程重新启动
# AC上show wireless client status检查client的状态
#
# 预期
# ps检查mapqosd进程重新启动OK，并且AP未下线,Client在线状态正常
################################################################################
printStep(testname, 'Step 3', 'killall -9 mapqosd, mapqosd restart and AP don\'t restart')

res1 = res2 = res3 = res4 = res5 = 1
# operate
# AP1配置
# 检查AP1 mapqosd进程是否运行
SetCmd(ap1, '\n')
data1 = SetCmd(ap1, 'ps | grep mapqosd', timeout=5)
res1 = CheckLine(data1, '/usr/sbin/mapqosd', IC=True)
# kill mapqosd进程
StartDebug(ap1)
SetCmd(ap1, 'killall -9 mapqosd')
# 检查AP是否下线
IdleAfter(17)
EnterEnableMode(switch1)
data1 = SetCmd(switch1, 'show wireless ap status')
res2 = CheckLine(data1, ap1mac, Ap1_ipv4, '1', 'Managed', 'Success', IC=True)
data2 = SetCmd(switch1, 'show wireless client status')
res3 = CheckLine(data2, sta1mac, ap1vapmac, IC=True)
data = StopDebug(ap1)
# 检查mapqosd进程重启，AP不应重启
res4 = CheckLine(data, 'dman: mapqosd exited',
                 'dman: Starting mapqosd',
                 ML=True)
mapqosdflag = res4
res5 = CheckLine(data, 'Restarting system')
# 如果mapqosd进程重启使AP重启，则等待AP重启上线
if res5 == 0:
    IdleAfter(50)
    ApLogin(ap1, retry=20)
    # i=1
    # while i<20:
    # data1 = SetCmd(ap1,'\n\n',timeout=1)
    # if 0 == CheckLine(data1,'login'):
    # break
    # IdleAfter('5')
    # i = i + 1
    # SetCmd(ap1,Ap_login_name,promotePatten='Password',IC=True)
    # data = SetCmd(ap1,Ap_login_password,timeout=2)
    # if CheckLine(data,'#')!=0 or CheckLine(data,'Login incorrect')==0:
    # SetCmd(ap1,Ap_login_name,promotePatten='Password',IC=True)
    # SetCmd(ap1,Ap_login_password,timeout=2)
    IdleAfter(20)
    j = 0
    EnterEnableMode(switch1)
    while j < 20:
        data1 = SetCmd(switch1, 'show wireless ap status')
        resa = CheckLine(data1, ap1mac, Ap1_ipv4, '1', 'Managed', 'Success', IC=True)
        if resa == 0:
            break
        IdleAfter('5')
        j = j + 1
# 如果AP短时间内没有重启，mapqosd进程也没有重启，则自行重启AP
if res4 != 0 and res5 != 0:
    RebootAp(AP=ap1)
    j = 0
    EnterEnableMode(switch1)
    while j < 20:
        data1 = SetCmd(switch1, 'show wireless ap status')
        resa = CheckLine(data1, ap1mac, Ap1_ipv4, '1', 'Managed', 'Success', IC=True)
        if resa == 0:
            break
        IdleAfter('5')
        j = j + 1

SetCmd(ap1, '\n')
data1 = SetCmd(ap1, 'ps | grep mapqosd', timeout=5)
res6 = CheckLine(data1, '/usr/sbin/mapqosd', IC=True)
res5 = 0 if res5 != 0 else 1
# result
printCheckStep(testname, 'Step 3', res1, res2, res3, res4, res5, res6)

################################################################################
# Step 4
# 操作
# STA1下线
#
# 预期
# Client下线成功
################################################################################
printStep(testname, 'Step 4', 'STA1 disconnect to network 1')

# res1 = 1
# operate
# sta1下线
WpaDisconnectWirelessNetwork(sta1, Netcard_sta1)
EnterEnableMode(switch1)
# i = 0
# while i < 20:
#     data = SetCmd(switch1, 'show wireless client status')
#     res1 = CheckLine(data, sta1mac, ap1vapmac, IC=True)
#     if res1 != 0:
#         break
#     IdleAfter(5)
#     i = i + 1
for _tick in xrange(60):  # 最多等待300s 防止误判
    _res = CheckLine(SetCmd(switch1, 'show wireless client status'), sta1mac, ap1vapmac, IC=True)
    if _res != 0:
        _res = 0
        break  # 如果CheckLine检测不到client用户信息，认为下线成功，将_res设置成0，退出循环
    IdleAfter(5, msg='Show Wireless Client Status')
else:
    _res = 1  # 如果上面CheckLine连续20次检测到client信息，那么认为用户下线失败，将_res设置为1
# res1 = 0 if _res != 0 else 1
# result
printCheckStep(testname, 'Step 4', _res)
################################################################################
# Step 5
# 操作
# 重启AP1，等待AP重新上线
#
# 预期
# AP1重启成功，再次上线成功
################################################################################
printStep(testname, 'Step 5', 'Reboot Ap1')

res1 = 1
# operate
RebootAp(AP=ap1)
EnterEnableMode(switch1)
i = 0
while i < 20:
    data = SetCmd(switch1, 'show wireless ap status')
    res1 = CheckLine(data, ap1mac, Ap1_ipv4, '1', 'Managed', 'Success', IC=True)
    if res1 == 0:
        break
    IdleAfter('5')
    i = i + 1
# result
printCheckStep(testname, 'Step 5', res1)
if mapdflag == 0:
    ################################################################################
    # Step 6
    # 操作
    # rm /etc/watchdog_log/restartlog ，然后1200s内连续三次kill掉mapd进程，
    # 在第四次kill的时候，AP打印“dman: mapd process restart more then 3 times in 1200 seconds, reboot ap ”之后重启
    #
    # 预期
    # AP重启后上线成功，ps检查mapd进程在运行，cat /etc/watchdog_log/restartlog显示mapd有四次重启记录，前三次为
    ################################################################################
    printStep(testname, 'Step 6', 'kill mapd three times in five minites,',
              'Ap1 will reboot when kill mapd the fourth time,',
              'cat /etc/watchdog_log/restartlog,there should be:',
              '\[mapd\] restart',
              '\[mapd\] restart',
              '\[mapd\] restart',
              '\[mapd\] process restart more then 3 times in 1200 seconds, reboot ap')

    res1 = 1
    # operate
    SetCmd(ap1, '\n')
    SetCmd(ap1, 'rm /etc/watchdog_log/restartlog')
    i = 0
    while i < 3:
        SetCmd(ap1, '\n')
        SetCmd(ap1, 'killall -9 mapd')
        IdleAfter(15)
        i = i + 1
    StartDebug(ap1)
    SetCmd(ap1, '\n')
    SetCmd(ap1, 'killall -9 mapd')
    IdleAfter(20)
    data = StopDebug(ap1)
    res1 = CheckLine(data, 'dman: mapd process restart more then 3 times in 1200 seconds, reboot ap')
    # 等待AP重启
    IdleAfter(60)
    ApLogin(ap1, retry=20)
    # i=1
    # while i<20:
    # data1 = SetCmd(ap1,'\n\n',timeout=1)
    # if 0 == CheckLine(data1,'login'):
    # break
    # IdleAfter('5')
    # i = i + 1
    # SetCmd(ap1,Ap_login_name,promotePatten='Password',IC=True)
    # data = SetCmd(ap1,Ap_login_password,timeout=2)
    # if CheckLine(data,'#')!=0 or CheckLine(data,'Login incorrect')==0:
    # SetCmd(ap1,Ap_login_name,promotePatten='Password',IC=True)
    # SetCmd(ap1,Ap_login_password,timeout=2)

    # 检查AP上线
    IdleAfter(30)
    EnterEnableMode(switch1)
    while i < 30:
        data = SetCmd(switch1, 'show wireless ap status')
        res2 = CheckLine(data, ap1mac, Ap1_ipv4, '1', 'Managed', 'Success', IC=True)
        if res2 == 0:
            break
        IdleAfter('5')
        i = i + 1

    SetCmd(ap1, '\n')
    data1 = SetCmd(ap1, 'ps | grep mapd')
    res3 = CheckLine(data1, '/usr/sbin/mapd', IC=True)
    SetCmd(ap1, '\n')
    data = SetCmd(ap1, 'cat /etc/watchdog_log/restartlog')
    print 'data=', data
    res4 = CheckLine(data, '\[mapd\] restart',
                     '\[mapd\] restart',
                     '\[mapd\] restart',
                     '\[mapd\] process restart more then 3 times in 1200 seconds, reboot ap',
                     ML=True)
    # result
    printCheckStep(testname, 'Step 6', res1, res2, res3, res4)
if mapqosdflag == 0:
    ################################################################################
    # Step 7
    # 操作
    # rm /etc/watchdog_log/restartlog ，然后1200s内连续三次kill掉mapqosd进程，
    # 在第四次kill的时候，AP打印“dman: mapqosd process restart more then 3 times in 1200 seconds, reboot ap ”之后重启
    #
    # 预期
    # AP重启后上线成功，ps检查mapqosd进程在运行，cat /etc/watchdog_log/restartlog显示mapqosd有四次重启记录，前三次为
    ################################################################################
    printStep(testname, 'Step 7', 'kill mapqosd three times in five minites,',
              'Ap1 will reboot when kill mapqosd the fourth time,',
              'cat /etc/watchdog_log/restartlog,there should be:',
              '\[mapqosd\] restart',
              '\[mapqosd\] restart',
              '\[mapqosd\] restart',
              '\[mapqosd\] process restart more then 3 times in 1200 seconds, reboot ap')

    res1 = 1
    # operate
    SetCmd(ap1, '\n')
    SetCmd(ap1, 'rm /etc/watchdog_log/restartlog')
    i = 0
    while i < 3:
        SetCmd(ap1, '\n')
        SetCmd(ap1, 'killall -9 mapqosd')
        IdleAfter(15)
        i = i + 1
    StartDebug(ap1)
    SetCmd(ap1, '\n')
    SetCmd(ap1, 'killall -9 mapqosd')
    IdleAfter(20)
    data = StopDebug(ap1)
    res1 = CheckLine(data, 'dman: mapqosd process restart more then 3 times in 1200 seconds, reboot ap')
    # 等待AP重启
    IdleAfter(60)
    ApLogin(ap1, retry=20)
    # i=1
    # while i<20:
    # data1 = SetCmd(ap1,'\n\n',timeout=1)
    # if 0 == CheckLine(data1,'login'):
    # break
    # IdleAfter('5')
    # i = i + 1
    # SetCmd(ap1,Ap_login_name,promotePatten='Password',IC=True)
    # data = SetCmd(ap1,Ap_login_password,timeout=2)
    # if CheckLine(data,'#')!=0 or CheckLine(data,'Login incorrect')==0:
    # SetCmd(ap1,Ap_login_name,promotePatten='Password',IC=True)
    # SetCmd(ap1,Ap_login_password,timeout=2)

    # 检查AP上线
    IdleAfter(30)
    EnterEnableMode(switch1)
    while i < 30:
        data = SetCmd(switch1, 'show wireless ap status')
        res2 = CheckLine(data, ap1mac, Ap1_ipv4, '1', 'Managed', 'Success', IC=True)
        if res2 == 0:
            break
        IdleAfter('5')
        i = i + 1

    SetCmd(ap1, '\n')
    data1 = SetCmd(ap1, 'ps | grep mapqosd')
    res3 = CheckLine(data1, '/usr/sbin/mapqosd', IC=True)
    SetCmd(ap1, '\n')
    data = SetCmd(ap1, 'cat /etc/watchdog_log/restartlog')
    print 'data=', data
    res4 = CheckLine(data, '\[mapqosd\] restart',
                     '\[mapqosd\] restart',
                     '\[mapqosd\] restart',
                     '\[mapqosd\] process restart more then 3 times in 1200 seconds, reboot ap',
                     ML=True)
    # result
    printCheckStep(testname, 'Step 7', res1, res2, res3, res4)
################################################################################
# Step 8
# 操作
# sta1接入AP1的network1
#
# 预期
# client接入成功，获取了192.168.x.x的地址,sta1 ping PC1，可以ping通
################################################################################
printStep(testname, 'Step 8',
          'STA1 connect to network 1',
          'STA1 ping pc1',
          'STA1 dhcp and get ip address,'
          'sta1 ping pc1 success')
res1 = res2 = 1
# operate
# STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1, Netcard_sta1, Network_name1, bssid=ap1mac_lower, checkDhcpAddress=Dhcp_pool1)
res2 = CheckPing(sta1, pc1_ipv4, mode='linux', pingPara=' -c 10')
# result
printCheckStep(testname, 'Step 8', res1, res2)

################################################################################
# Step 9
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 9',
          'Recover initial config')

# operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'keep-alive-interval 10000')
# sta1下线
WpaDisconnectWirelessNetwork(sta1, Netcard_sta1)
# end
printTimer(testname, 'End')
