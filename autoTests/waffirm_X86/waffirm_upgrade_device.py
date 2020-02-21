#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_upgrade_device_DSCC.py
#
# Author:  guomf@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

################################################################################
#Step 1 config all device ip address
################################################################################
print '###########################################################'
print "######### Now start set ip address and ping check #########"
print '###########################################################'

ac1 = 'ac1'
ac2 = 'ac2'
CreateNewConn('Telnet',ac1,switch1_host,None,'run')
CreateNewConn('Telnet',ac2,switch2_host,None,'run')
Receiver(ac1,'\n\n')
Receiver(ac2,'\n\n')
TelnetLogin(ac1,Pc1_telnet_name,Pc1_telnet_password)
TelnetLogin(ac2,Pc1_telnet_name,Pc1_telnet_password)

SetCmd(ac1,'cd /home/dscc/')
SetCmd(ac1,'pkill -9 dcn_console')
SetCmd(ac1,'pkill -9 monitor.sh')
SetCmd(ac1,'pkill -9 nos.img')

SetCmd(ac2,'cd /home/dscc/')
SetCmd(ac2,'pkill -9 dcn_console')
SetCmd(ac2,'pkill -9 monitor.sh')
SetCmd(ac2,'pkill -9 nos.img')

SetCmd(switch1,'\n\n')
SetCmd(switch2,'\n\n')

EnterConfigMode(switch3)
SetCmd(switch3,'no interface vlan 100')
SetCmd(switch3,'vlan 100')
SetCmd(switch3,'switchport interface '+s3p1+';'+s3p2+';'+s3p3+';'+s3p4+';'+s3p6)
EnterInterfaceMode(switch3,'vlan 100')
SetCmd(switch3,'ip address 100.1.1.13 255.255.255.0')

SetCmd(ap1,'\n')
SetCmd(ap1,'set management static-ip 100.1.1.14')
SetCmd(ap1,'save-running')

SetCmd(ap2,'\n')
SetCmd(ap2,'set management static-ip 100.1.1.15')
SetCmd(ap2,'save-running')

s1ping = CheckPing(switch1,'80.0.0.254',mode='linux')
s2ping = CheckPing(switch2,'80.0.0.254',mode='linux')
s3ping = CheckPing(switch3,'100.1.1.1')
ap1ping = CheckPing(ap1,'100.1.1.1',mode='linux')
ap2ping = CheckPing(ap2,'100.1.1.1',mode='linux')
if s1ping == 1:
	upgrade_s1img = 0
if s2ping == 1:
	upgrade_s2img = 0
if s3ping == 1:
	upgrade_s3boot = upgrade_s3img = 0
if ap1ping == 1:
	upgrade_ap1img = 0
if ap2ping == 1:
	upgrade_ap2img = 0

if s1ping == 0 and s2ping == 0 and s2ping == 0 and ap1ping == 0 and ap2ping == 0:
	step1 = 1
	print "######### all device ping tftp server pass ################"
else:
	step1 = 0
	print "#### some device ping Failed,please check console log #####"
print '###########################################################'

################################################################################
#Step 2 start write s3 boot file
################################################################################
print '###########################################################'
print "###### Start try upgrade s3's boot.rom if needed ########"
print '###########################################################'

s3bootstatus = 1
#如果找到s3boot.rom文件，开始升级s3 boot
if upgrade_s3boot == 1:
	EnterEnableMode(switch3)
	SetCmd(switch3,'copy tftp://100.1.1.1/env'+EnvNo+'/s3boot.rom boot.rom',promoteTimeout=5)
	time.sleep(1)
	data = SetCmd(switch3,'Y',promotePatten='close tftp client',promoteTimeout=60)
	if 0 == CheckLine(data,'Write ok'):
		s3bootstatus = 0
	else:
		s3bootstatus = -1
		print 'Error:Try upgrade S3 boot.rom failed!!!'
else:
	s3bootstatus = 0

if s3bootstatus == 0:
	step2 = 1
	print "####### s3's boot.rom write success or no need ##########"
else:
	step2 = 0
	print "#### boot.rom write failed, please check console log #####"
print '###########################################################'

################################################################################
#Step 3 start s1-3 and ap1-2 img file
################################################################################
print '###########################################################'
print "# Start try upgrade s1-3 and ap1-2's nos.img/tar if needed#"
print '###########################################################'

s1imgstatus = s2imgstatus = s3imgstatus = ap1imgstatus = ap2imgstatus = 1
#如果找到s1nos.img/s2nos.img/s3nos.img文件，开始升级s1/s2/s3
if upgrade_s1img == 1:
	SetCmd(ac1,'rm -rf s1nos.img*')
	SetCmd(ac1,'mv -f nos.img nos_old.img')
	data = SetCmd(ac1,'wget ftp://upload:upload@80.0.0.254/env4/s1nos.img',promotePatten='dscc]#')
	if None != re.search('.*?s1nos.img.*?saved.*?',data):
		s1imgstatus = 0
		SetCmd(ac1,'mv -f s1nos.img nos.img')
	else:
		print 'Error:Try upgrade S1 nos.img failed!!!'
		s1imgstatus = -1

else:
	s1imgstatus = 0

if upgrade_s2img == 1:
	SetCmd(ac2,'rm -rf s2nos.img*')
	SetCmd(ac2,'mv -f nos.img nos_old.img')
	data = SetCmd(ac2,'wget ftp://upload:upload@80.0.0.254/env4/s2nos.img',promotePatten='dscc]#')
	if None != re.search('.*?s2nos.img.*?saved.*?',data):
		s2imgstatus = 0
		SetCmd(ac2,'mv -f s2nos.img nos.img')
	else:
		print 'Error:Try upgrade S2 nos.img failed!!!'
		s2imgstatus = -1
else:
	s2imgstatus = 0

if upgrade_s3img == 1:
	EnterEnableMode(switch3)
	SetCmd(switch3,'copy tftp://100.1.1.1/env'+EnvNo+'/s3nos.img nos.img',promoteTimeout=5)
	time.sleep(1)
	data = SetCmd(switch3,'Y',promotePatten='#',promoteTimeout=10)
	if 0 == CheckLine(data,'return error'):
		s3imgstatus = -1
		print 'Error:Try upgrade S3 nos.img failed!!!'
	StartDebug(switch3)
else:
	s3imgstatus = 0
	
#如果找到ap1.tar/ap2.tar文件，开始升级ap1和ap2
if upgrade_ap1img == 1:
	SetCmd(ap1,'\n\n',promoteTimeout=1)
	data4 = SetCmd(ap1,'firmware-upgrade tftp://100.1.1.1/env'+EnvNo+'/ap1.tar',promoteTimeout=5)
	if 0 != CheckLine(data4,'/ap1.tar','% |'):
		ap1imgstatus = -1
		print "ap1 img file ap1.tar incorrect!!! Please check this!!!"
	StartDebug(ap1)
else:
	ap1imgstatus = 0

if upgrade_ap2img == 1:
	SetCmd(ap2,'\n\n',promoteTimeout=1)
	data5 = SetCmd(ap2,'firmware-upgrade tftp://100.1.1.1/env'+EnvNo+'/ap2.tar',promoteTimeout=5)
	if 0 != CheckLine(data5,'/ap2.tar','% |'):
		ap2imgstatus = -1
		print "ap2 img file ap2.tar incorrect!!! Please check this!!!"
	StartDebug(ap2)
else:
	ap2imgstatus = 0

for tmpCounter in xrange(0,60):
	IdleAfter('10')
	data = StopDebug(switch3)
	StartDebug(switch3)
	if s3imgstatus == 1 and 0 == CheckLine(data,'Write ok'):
		s3imgstatus = 0
	if s3imgstatus == 1 and 0 == CheckLine(data,'close tftp client'):
		s3imgstatus = -1

	data1 = StopDebug(ap1)
	StartDebug(ap1)
	data2 = StopDebug(ap2)
	StartDebug(ap2)
	if ap1imgstatus == 1 and 0 == CheckLine(data1,'login:'):
		ap1imgstatus = 0
	if ap2imgstatus == 1 and 0 == CheckLine(data2,'login:'):
		ap2imgstatus = 0

	if s1imgstatus != 1 and s2imgstatus != 1 and s3imgstatus != 1 and ap1imgstatus != 1 and ap1imgstatus != 1:
		break

if upgrade_s3img == 1:
	StopDebug(switch3)
if upgrade_ap1img == 1:
	StopDebug(ap1)
if upgrade_ap2img == 1:
	StopDebug(ap2)

if s1imgstatus == 0 and s2imgstatus == 0 and s3imgstatus == 0 and ap1imgstatus == 0 and ap2imgstatus == 0:
	step3 = 1
	print "## all device's nos.img/tar file write success or no need##"
else:
	step3 = 0
	print "# nos.img/tar file write failed, please check console log #"
print '###########################################################'

################################################################################
#Step 4 reload s1-3 ap1-2 if needed
################################################################################
import wx,re
#operate
if upgrade_s1img == 1:
	if s1imgstatus != -1:
		Receiver(switch1,'\n\n')
		SetCmd(switch1,'cd /home/dscc',timeout=5)
		SetCmd(switch1,'chmod +x nos.img',timeout=5)
		SetCmd(switch1,'./start.sh nos.img',promoteStop=30)
		SetCmd(switch1,'./dcn_console',timeout=10)
		Receiver(switch1,'\n\n')
if upgrade_s2img == 1:
	if s2imgstatus != -1:
		SetCmd(switch2,'cd /home/dscc',timeout=5)
		SetCmd(switch2,'chmod +x nos.img',timeout=5)
		SetCmd(switch2,'./start.sh nos.img',promoteStop=30)
		SetCmd(switch2,'./dcn_console',timeout=10)
		Receiver(switch2,'\n\n')
if upgrade_s3img == 1 or upgrade_s3boot == 1:
	if s3bootstatus != -1 and s3imgstatus != -1:
		Receiver(switch3,'reload')
		time.sleep(1)
		Receiver(switch3,'y')
		time.sleep(200)

Receiver(switch1,'\n\n\n')
Receiver(switch2,'\n\n\n')
Receiver(switch3,'\n\n\n')
EnterEnableMode(switch1)
EnterEnableMode(switch2)
EnterEnableMode(switch3)
Receiver(switch1,'terminal length 0')
Receiver(switch2,'terminal length 0')
Receiver(switch3,'terminal length 0')
CloseChannels(ac1)
CloseChannels(ac2)
#登录AP1,AP2
SetCmd(ap1,'\n\n',timeout=5)
SetCmd(ap2,'\n\n',timeout=5)
data1 = SetCmd(ap1,'\n\n',timeout=1)
data2 = SetCmd(ap2,'\n\n',timeout=1)
if 0 == CheckLine(data1,'login'):
    SetCmd(ap1,Ap_login_name,promotePatten='Password',IC=True)
    SetCmd(ap1,Ap_login_password)
if 0 == CheckLine(data2,'login'):
    SetCmd(ap2,Ap_login_name,promotePatten='Password',IC=True)
    SetCmd(ap2,Ap_login_password)

SetCmd(ap1,'\n\n',promoteTimeout=1)
SetCmd(ap1,'set management static-ip 192.168.1.10')
SetCmd(ap1,'save-running')
SetCmd(ap2,'\n\n',promoteTimeout=1)
SetCmd(ap2,'set management static-ip 192.168.1.10')
SetCmd(ap2,'save-running')

s1v=s2v=s3v=ap1v=ap2v='get version error'
EnterEnableMode(switch1)
data = SetCmd(switch1,'show version')
s1v = re.search('Version ([^\n ]+)',data).group(1)
EnterEnableMode(switch2)
data = SetCmd(switch2,'show version')
s2v = re.search('Version ([^\n ]+)',data).group(1)
EnterEnableMode(switch3)
data = SetCmd(switch3,'show version')
s3v = re.search('Version ([^\n ]+)',data).group(1)
data = SetCmd(ap1,'get system')
ap1v = re.search('version\s+([^\n ]+)',data).group(1)
data = SetCmd(ap2,'get system')
ap2v = re.search('version\s+([^\n ]+)',data).group(1)
if step1 != 1 or step2  != 1 or step3  != 1:
	wx.MessageBox(u'某些文件写失败,请停止执行检查console日志')
	wx.FindWindowById(10).PauseTestAuto()
else:
	wx.MessageBox('AC1 version:'+s1v+'\nAC2 version:'+s2v+'\nS3 version:'+s3v+'\nAP1 version:'+ap1v+'\nAP2 version:'+ap2v+u'\n请确认设备是本次测试正确版本')