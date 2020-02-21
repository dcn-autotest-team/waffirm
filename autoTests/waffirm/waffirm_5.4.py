#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_5.4.py - test case 5.4 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2013 Digital China Networks Co. Ltd
#
# Features:
# 5.4     AP uboot下升级测试（R4)
# 测试目的：测试在uboot下升级ap的uboot/image版本。
# 测试环境：同测试拓扑
# 测试描述：在uboot下升级ap的uboot/image版本，升级后AP能够正常启动。
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'TestCase 5.4'
avoiderror(testname)
printTimer(testname,'Start','Upgrade image file under uboot')

################################################################################
#Step 1
#操作
#AP1直连PC，PC上配置ip地址20.1.1.4，掩码255.255.255.0。PC上开启FTP/TFTP服务。
#
#预期
# PC可以ping通AP1
################################################################################
printStep(testname,'Step 1',
          'pc ping ap success ')

#operate
EnterConfigMode(switch3)
SetCmd(switch3,'interface ' + s3p6)
SetCmd(switch3,'no shutdown')
SetCmd(switch3,'switchport access vlan 20')
SetCmd(switch3,'exit')

data2 = SetCmd(switch1,'show run')
data1 = SetCmd(ap1,'get system')
data3 = SetCmd(ap1,'bootenv -p')
re1 = re.search('version           (\d+\.\d+\.\d+\.\d+)',data1)
if re1 is not None:
    version1 = re1.group(1)
else:
    version1 = 'error'

re1 = re.search('(\d+_\d+_\d+_\d+)',apnowimg)
if re1 is not None:
    version2 = re.sub('_','.',re1.group(1))
else:
    version2 = 'error'
re1 = re.search('(\d+_\d+_\d+_\d+)',aptestimg)
if re1 is not None:
    version5 = re.sub('_','.',re1.group(1))
else:
    version5 = 'error'

re1 = re.search('bootloader_version=(\d+\.\d+\.\d+)',data3)
if re1 is not None:
    version7 = re1.group(1)
else:
    version7 = 'error'

re1 = re.search('(\d+_\d+_\d+|\d+\.\d+\.\d+)',apnowuboot)
if re1 is not None:
    version8 = re.sub('_','.',re1.group(1))
else:
    version8 = 'error'

re1 = re.search('(\d+_\d+_\d+|\d+\.\d+\.\d+)',aptestuboot)
if re1 is not None:
    version9 = re.sub('_','.',re1.group(1))
else:
    version9 = 'error'
    
print '#############################'
print 'Now ap version is    ' + version1
print 'You selected version ' + version2
print 'Will update to image ' + version5
print '+++++++++++++++++++++++++++++'
print 'Now ap uboot is      ' + version7
print 'You selected uboot   ' + version8
print 'Will update to uboot ' + version9
print '#############################'

#EnterEnableMode(switch1)
#SetCmd(switch1,'copy tftp://' + updateserver + '/' + aptestimg + ' ' + aptestimg,timeout=180)

#data3 = SetCmd(switch1,'dir')

#res1 = CheckLine(data3,aptestimg)

if version1 == version2:
    res1 = 0
else:
    res1 = 1
#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#操作
#AP1重起，按ctrl+B进入uboot界面
#WLAN-AP# reboot
#
#预期
#进入APuboot界面
#Bootloader/>
################################################################################
printStep(testname,'Step 2',
          'Firmware upgrade')

SetCmd(ap1,'reboot',timeout=1)
SetCmd(ap1,'y',promotePatten= 'Hit any key')
SetCmd(ap1,'\x02')
SetCmd(ap1,'\x02')
IdleAfter('5')
data1 = SetCmd(ap1,'')

res1 = CheckLine(data1,'Boot')
printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#Uboot下配置ip地址和服务器地址
#Bootloader/> setenv ipaddr 20.1.1.3
#Bootloader/> setenv serverip 20.1.1.4
#配置成功，ping通20.1.1.4
################################################################################
printStep(testname,'Step 3',
          'Config server and ap address in bootloader.')

SetCmd(ap1,'setenv ipaddr ' + updatel3ip)
SetCmd(ap1,'setenv serverip ' + updateserver)
StartDebug(ap1)
SetCmd(ap1,'ping ' + updateserver,timeout=5)
data5 = StopDebug(ap1)
res1 = CheckLine(data5,'is alive')

printCheckStep(testname, 'Step 3',res1)

################################################################################
#Step 4
#操作
# 
#4	下载新版本u-boot.bin
#Bootloader/>tftp 0x80060000 u-boot.bin	下载成功	   
#5	升级uboot
#Bootloader/>run lu	升级成功	   
#6	下载新版本image文件upgrade_new.tar
#tftp 0x80060000 upgrade_new.tar	下载成功	   
#7	升级分区1
#tar_img_update	升级成功	 
################################################################################
printStep(testname,'Step 4',
          'Update image and uboot')

data7 = SetCmd(ap1,'tftp 0x80060000 ' + aptestuboot,timeout=10)
res1 =CheckLine(data7,'done')

if re.search('tar',aptestuboot) is not None:
    data7 = SetCmd(ap1,'tar_bootloader_update',timeout=10)
    res2 =CheckLine(data7,'done')
else:
    data7 = SetCmd(ap1,'run lu',timeout=10)
    res2 =CheckLine(data7,'done')

data7 = SetCmd(ap1,'tftp 0x80060000 ' + aptestimg,timeout=30)
res3 =CheckLine(data7,'done')

data7 = SetCmd(ap1,'tar_img_update',timeout=180)
res4 =CheckLine(data7,'done')

printCheckStep(testname, 'Step 4',res1,res2,res3,res4)

################################################################################
#Step 5
#操作
#重启后自动进入img
#Reset
#AP image下get system的“version”显示“新版本号”
################################################################################
printStep(testname,'Step 5',
          'Show wireless ap version status.')

SetCmd(ap1,'reset')
IdleAfter('80')
SetCmd(ap1,'admin',timeout=1)
SetCmd(ap1,'admin',timeout=1)
SetCmd(ap1,'admin',timeout=1)
data7 = SetCmd(ap1,'get system')
res1 =CheckLine(data7,version5)

data3 = SetCmd(ap1,'bootenv -p')
re1 = re.search('bootloader_version=(\d+\.\d+\.\d+)',data3)
if re1 is not None:
    version10 = re1.group(1)
else:
    version10 = 'error10'
if version10 == version9:
    res2 = 0
else:
    res2 = 1

printCheckStep(testname, 'Step 5',res1,res2)

################################################################################
#Step 6
#Return initial config
################################################################################
printStep(testname,'Step 6',
          'Return initial config.')

SetCmd(ap1,'reboot',timeout=1)
SetCmd(ap1,'y',promotePatten= 'Hit any key')
SetCmd(ap1,'\x02')
SetCmd(ap1,'\x02')
IdleAfter('5')
data1 = SetCmd(ap1,'')
SetCmd(ap1,'setenv ipaddr ' + updatel3ip)
SetCmd(ap1,'setenv serverip ' + updateserver)
StartDebug(ap1)
SetCmd(ap1,'ping ' + updateserver,timeout=5)
data5 = StopDebug(ap1)
res1 = CheckLine(data5,'is alive')
data7 = SetCmd(ap1,'tftp 0x80060000 ' + apnowuboot,timeout=10)
res5 =CheckLine(data7,'done')

if re.search('tar',aptestuboot) is not None:
    data7 = SetCmd(ap1,'tar_bootloader_update',timeout=10)
    res2 =CheckLine(data7,'done')
else:
    data7 = SetCmd(ap1,'run lu',timeout=10)
    res2 =CheckLine(data7,'done')

data7 = SetCmd(ap1,'tftp 0x80060000 ' + apnowimg,timeout=30)
res3 =CheckLine(data7,'done')

data7 = SetCmd(ap1,'tar_img_update',timeout=180)
res4 =CheckLine(data7,'done')

SetCmd(ap1,'reset')
IdleAfter('80')
SetCmd(ap1,'admin',timeout=1)
SetCmd(ap1,'admin',timeout=1)
SetCmd(ap1,'admin',timeout=1)
data7 = SetCmd(ap1,'get system')
res5 =CheckLine(data7,version1)

data3 = SetCmd(ap1,'bootenv -p')
re1 = re.search('bootloader_version=(\d+\.\d+\.\d+)',data3)
if re1 is not None:
    version10 = re1.group(1)
else:
    version10 = 'error10'
if version10 == version7:
    res6 = 0
else:
    res6 = 1

EnterConfigMode(switch3)
SetCmd(switch3,'interface ' + s3p6)
SetCmd(switch3,'shutdown')
SetCmd(switch3,'switchport access vlan 1')
SetCmd(switch3,'exit')

printCheckStep(testname, 'Step 6',res1,res2,res3,res4,res5,res6)