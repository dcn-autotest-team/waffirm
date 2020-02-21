#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_upgrade_device.py
#
# Author:  guomf@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 自动升级环境中的设备
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
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan 100')
SetCmd(switch1,'vlan 100')
SetCmd(switch1,'switchport interface '+s1p1)
EnterInterfaceMode(switch1,'vlan 100')
SetCmd(switch1,'ip address 100.1.1.11 255.255.255.0')

EnterConfigMode(switch2)
SetCmd(switch2,'no interface vlan 100')
SetCmd(switch2,'vlan 100')
SetCmd(switch2,'switchport interface '+s2p1)
EnterInterfaceMode(switch2,'vlan 100')
SetCmd(switch2,'ip address 100.1.1.12 255.255.255.0')

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

s1ping = CheckPing(switch1,'100.1.1.1')
s2ping = CheckPing(switch2,'100.1.1.1')
s3ping = CheckPing(switch3,'100.1.1.1')
ap1ping = CheckPing(ap1,'100.1.1.1',mode='linux')
ap2ping = CheckPing(ap2,'100.1.1.1',mode='linux')
if s1ping == 1:
	upgrade_s1boot = upgrade_s1img = 0
if s2ping == 1:
	upgrade_s2boot = upgrade_s2img = 0
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
#Step 2 start write s1-3 boot file
################################################################################
print '###########################################################'
print "###### Start try upgrade s1-3's boot.rom if needed ########"
print '###########################################################'
s1bootstatus = s2bootstatus = s3bootstatus = 1
#如果找到s1boot.rom/s2boot.rom/s3boot.rom文件，开始升级s1/s2/s3 boot
if upgrade_s1boot == 1:
	EnterEnableMode(switch1)
	SetCmd(switch1,'copy tftp://100.1.1.1/env'+EnvNo+'/s1boot.rom boot.rom',promoteTimeout=5)
	time.sleep(1)
	data = SetCmd(switch1,'Y',promotePatten='close tftp client',promoteTimeout=60)
	if 0 == CheckLine(data,'Write ok'):
		s1bootstatus = 0
	else:
		s1bootstatus = -1
		print "Try upgrade S1 boot.rom,device show this message:"
		print data
else:
	s1bootstatus = 0

if upgrade_s2boot == 1:
	EnterEnableMode(switch2)
	SetCmd(switch2,'copy tftp://100.1.1.1/env'+EnvNo+'/s2boot.rom boot.rom',promoteTimeout=5)
	time.sleep(1)
	data = SetCmd(switch2,'Y',promotePatten='close tftp client',promoteTimeout=60)
	if 0 == CheckLine(data,'Write ok'):
		s2bootstatus = 0
	else:
		s2bootstatus = -1
		print "Try upgrade S2 boot.rom,device show this message:"
		print data
else:
	s2bootstatus = 0

if upgrade_s3boot == 1:
	EnterEnableMode(switch3)
	SetCmd(switch3,'copy tftp://100.1.1.1/env'+EnvNo+'/s3boot.rom boot.rom',promoteTimeout=5)
	time.sleep(1)
	data = SetCmd(switch3,'Y',promotePatten='close tftp client',promoteTimeout=60)
	if 0 == CheckLine(data,'Write ok'):
		s3bootstatus = 0
	else:
		s3bootstatus = -1
		print "Try upgrade S3 boot.rom,device show this message:"
		print data
else:
	s3bootstatus = 0

if s1bootstatus == 0 and s2bootstatus == 0 and s3bootstatus == 0:
	step2 = 1
	print "####### s1-3's boot.rom write success or no need ##########"
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
	EnterEnableMode(switch1)
	SetCmd(switch1,'copy tftp://100.1.1.1/env'+EnvNo+'/s1nos.img nos.img',promoteTimeout=5)
	time.sleep(1)
	data = SetCmd(switch1,'Y',promotePatten='#',promoteTimeout=10)
	if 0 == CheckLine(data,'return error'):
		s1imgstatus = -1
		print "Try upgrade S1 nos.img,device show this message:"
		print data
	StartDebug(switch1)
else:
	s1imgstatus = 0

if upgrade_s2img == 1:
	EnterEnableMode(switch2)
	SetCmd(switch2,'copy tftp://100.1.1.1/env'+EnvNo+'/s2nos.img nos.img',promoteTimeout=5)
	time.sleep(1)
	data = SetCmd(switch2,'Y',promotePatten='#',promoteTimeout=10)
	if 0 == CheckLine(data,'return error'):
		s2imgstatus = -1
		print "Try upgrade S2 nos.img,device show this message:"
		print data
	StartDebug(switch2)
else:
	s2imgstatus = 0
if upgrade_s3img == 1:
	EnterEnableMode(switch3)
	SetCmd(switch3,'copy tftp://100.1.1.1/env'+EnvNo+'/s3nos.img nos.img',promoteTimeout=5)
	time.sleep(1)
	data = SetCmd(switch3,'Y',promotePatten='#',promoteTimeout=10)
	if 0 == CheckLine(data,'return error'):
		s3imgstatus = -1
		print "Try upgrade S3 nos.img,device show this message:"
		print date
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

for tmpCounter in xrange(0,120):
	IdleAfter('10')
	data = StopDebug(switch1)
	StartDebug(switch1)
	if s1imgstatus == 1 and 0 == CheckLine(data,'Write ok'):
		s1imgstatus = 0
	elif s1imgstatus == 1 and 0 == CheckLine(data,'close tftp client'):
		s1imgstatus = -1
	data = StopDebug(switch2)
	StartDebug(switch2)
	if s2imgstatus == 1 and 0 == CheckLine(data,'Write ok'):
		s2imgstatus = 0
	elif s2imgstatus == 1 and 0 == CheckLine(data,'close tftp client'):
		s2imgstatus = -1
	data = StopDebug(switch3)
	StartDebug(switch3)
	if s3imgstatus == 1 and 0 == CheckLine(data,'Write ok'):
		s3imgstatus = 0
	elif s3imgstatus == 1 and 0 == CheckLine(data,'close tftp client'):
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

if upgrade_s1img == 1:
	StopDebug(switch1)
if upgrade_s2img == 1:
	StopDebug(switch2)
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
if upgrade_s1img == 1 or upgrade_s1boot == 1:
	if s1bootstatus != -1 and s1imgstatus != -1:
		Receiver(switch1,'reload')
		time.sleep(1)
		Receiver(switch1,'y')
if upgrade_s2img == 1 or upgrade_s2boot == 1:
	if s2bootstatus != -1 and s2imgstatus != -1:
		Receiver(switch2,'reload')
		time.sleep(1)
		Receiver(switch2,'y')
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
	wx.MessageBox(u'某些文件写失败,请停止执行检console日志')
	wx.FindWindowById(10).PauseTestAuto()
else:
	wx.MessageBox('AC1 version:'+s1v+'\nAC2 version:'+s2v+'\nS3 version:'+s3v+'\nAP1 version:'+ap1v+'\nAP2 version:'+ap2v+u'\n请确认设备是本次测试正确版本')