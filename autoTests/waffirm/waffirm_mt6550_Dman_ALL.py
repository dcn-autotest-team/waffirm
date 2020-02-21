#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_mt6550_Dman.py
#
# Author:  (zhangjxp)
#
# Version 1.0.0
#
# Date:  2017-3-30 9:54:28
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 1.1.1	MT6550：Dman（apmgmt）进程异常挂掉AP重启测试
# 测试目的：测试AP主进程挂掉后是否有重启保护机制，重启后进程运行正常，AP上线运行OK，
# sta接入OK
# 测试环境：同测试拓扑
# 测试描述：dman挂掉后，软件狗（watchdog-software）进程会监测到，正常情况下，
# 软狗会先往/etc/watchdog_log写日志，然后重启AP。我们需要一个异常情况的保护机制，
# 当flash空间不足导致软狗写日志失败的时候，软狗依然正常运行（软狗停止运行是有问题的），
# 并且会重启AP让AP再次正常工作
#
#*******************************************************************************
# Change log:
#     - creadte by zhangjxp 2017.7.24
#     - modified by zhangjxp RDM50352,同步方案修改step3,killall -9 apmgmt后AP不重启
#     - modified by zhangjxp RDM50626,同步方案修改step3
#*******************************************************************************
#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase mt6550_Dman'
avoiderror(testname)
printTimer(testname,'Start')

################################################################################
#Step 1
#
#操作
# 登陆AP的命令行，进入AP的shell模式，ps –ef | grep dman和ps –ef | grep apmgmt进程正常工作
#
#预期
# 能查到正在运行的dman和apmgmt进程
#
################################################################################
printStep(testname,'Step 1',
          'check whether dman and apmgmt are running')
res1=1
res2=1
#operate
#AP1配置
SetCmd(ap1,'\n')
data1 = SetCmd(ap1,'ps | grep dman',timeout=5)
res1=CheckLine(data1,'/usr/sbin/dman',IC=True)
data2 = SetCmd(ap1,'ps | grep apmgmt',timeout=5)
res2=CheckLine(data2,'/sbin/apmgmt',IC=True)
#result
printCheckStep(testname, 'Step 1', res1,res2)

################################################################################
#Step 2
#操作
# cd /usr/sbin目录，df检查当前目录的磁盘空间，打印显示的/dev/root这一行Available
# 这一列的数字为X，然后敲dd if=/usr/sbin/dman of=/usr/sbin/testY.file bs=1K count=X，
# 即在当前目录下创建指定大小的文件填充flash，其中Y=1,2,3…，直到AP console口显示
# can't open '/usr/sbin/testY.file': No space left on device
#
#预期
# /usr/sbin目录被填充满，提示No space left on device
################################################################################
printStep(testname,'Step 2',
          'create files in /usr/sbin until there is no space')

res1=1
#operate
SetCmd(ap1,'\n')
SetCmd(ap1,'cd /usr/sbin')
data=SetCmd(ap1,'df',timeout=10)
tmpt=re.search('/dev/root+\s+\d+\s+\d+\s+(\d+)\s+',data)
if tmpt != None:
	availableroom=tmpt.group(1)
	print 'availableroom=',availableroom
	if availableroom=='0':
		print '1111111'
		res1=0
else:
	print 'Can\'t get availableroom,please check!'
	availableroom='100'

if res1 != 0:
	for i in range(1,50):
		StartDebug(ap1)
		Y=str(i)
		SetCmd(ap1,'dd if=/usr/sbin/dman of=/usr/sbin/test'+Y+'.file bs=1K count='+availableroom)
		data=StopDebug(ap1)
		res1=CheckLine(data,'No space left on device',IC=True)
		if res1 == 0:
			break
#result
printCheckStep(testname, 'Step 2', res1)

################################################################################
#Step 3
#
#操作
#在AP的shell模式下，用命令killall -9 apmgmt结束ap管理进程（root的子进程），等待三分钟，观察AP是否会重启
#
#预期
#AP的console口打印file: /tmp/watchdog/apmgmt timeout，并且在/etc/watchdog_log目录下产生一个基于linux系统时间生成的restartlog文件，
#文件内容为“Thu Jan 1 04:00:56 1970 [apmgmt] kill process apmgmt success“
################################################################################
printStep(testname,'Step 3',
          'kill apmgmt,and wait for 3 minites,'
          'Ap should reboot')

res1=res2=res3=res4=1
#operate
StartDebug(ap1)
SetCmd(ap1,'\n')
SetCmd(ap1,'killall -9 apmgmt')
# 等待3分钟会有file: /tmp/watchdog/apmgmt timeout打印，实际AP重启需要5分钟左右
IdleAfter(200)
CheckSutCmd(switch1,'show wireless ap status',
            check=[(ap1mac,'Managed','Success')],
            waittime=5,retry=20,interval=5,IC=True)
data=StopDebug(ap1)
res1=CheckLine(data,'file: /tmp/watchdog/apmgmt timeout')
data1 = SetCmd(ap1,'ps | grep apmgmt')
res2=CheckLine(data1,'/sbin/apmgmt',IC=True)
# RDM50626删除对res3的检查
# SetCmd(ap1,'cd /etc/watchdog_log')
# SetCmd(ap1,'ls')
# data2=SetCmd(ap1,'cat restartlog')
# res3 = CheckLine(data2,'[apmgmt]\s+kill\s+process\s+apmgmt\s+success')

# 根据几款AP的实际表现，如果检测不到apmgmt进程重启，则认为Ap会自动重启或者卡死
# 下面代码防止部分AP存在bug会异常重启，导致后面用例fail
flag = res2
rebootflag = 1
if flag != 0:
    IdleAfter(180)
    for i in range(12):
        data1 = SetCmd(ap1,'\n\n',timeout=1)
        if 0 == CheckLine(data1,'login'):
            rebootflag = 0
            break
        IdleAfter(5)
    # 如果软件狗没有重启AP，则自行重启AP
    if rebootflag != 0:
        RebootAp(AP=ap1)
    else:
        ApLogin(ap1)
#result
printCheckStep(testname, 'Step 3',res1,res2)
################################################################################
#Step 4
#操作
# 等待AP上线。然后登陆AP，ps aux | grep dman检查dman进程在工作，
# ps aux| grep apmgmt进程在工作
#
#预期
#AP重新上线成功，dman和apmgmt进程运行OK
################################################################################
printStep(testname,'Step 4',
          'After Ap reboot,check whether dman and apmgmt are running')

res1=res2=res3=1
#operate
# 检查AP上线
IdleAfter(20)
EnterEnableMode(switch1)
while i<20:
    data = SetCmd(switch1,'show wireless ap status')
    res1 = CheckLine(data,ap1mac,Ap1_ipv4,'1','Managed','Success',IC=True)
    if res1 == 0:
        break
    IdleAfter('5')
    i = i + 1
	
SetCmd(ap1,'\n')
data1 = SetCmd(ap1,'ps | grep dman',timeout=5)
res2=CheckLine(data1,'/usr/sbin/dman',IC=True)
data2 = SetCmd(ap1,'ps | grep apmgmt',timeout=5)
res3=CheckLine(data2,'/sbin/apmgmt',IC=True)
#result
printCheckStep(testname, 'Step 4', res1,res2,res3)

################################################################################
#Step 5
#操作
# sta1接入AP1的network1
#
#预期
#client接入成功，获取了192.168.x.x的地址,sta1 ping PC1，可以ping通
################################################################################
printStep(testname,'Step 5',
          'STA1 connect to network 1',
          'STA1 ping pc1',
          'STA1 dhcp and get ip address,'
          'sta1 ping pc1 success')
res1=res2=1
#operate
#STA1关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower,checkDhcpAddress=Dhcp_pool1)
res2 = CheckPing(sta1,pc1_ipv4,mode='linux',pingPara=' -c 10')
#result
printCheckStep(testname, 'Step 5', res1,res2)

################################################################################
#Step 6
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 6',
          'Recover initial config')

#operate
# 进入AP的shell模式，cd /usr/sbin进入到指定目录，rm –f *.file强制移除第2步添加的所有文件并退出shell
SetCmd(ap1,'\n')
SetCmd(ap1,'cd /usr/sbin')
SetCmd(ap1,'rm -f *.file')
# sta1下线
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
#end
printTimer(testname, 'End')
