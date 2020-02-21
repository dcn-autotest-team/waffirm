#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_5.3.py - test case 5.3 of waffirm_new
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2013 Digital China Networks Co. Ltd
#
# Features:
# 5.3     在AP上直接升级image测试
# 测试目的：测试在img下升级ap版本
# 测试环境：同测试拓扑
# 测试描述：在img下升级ap版本。TFP/TFTP服务器ip：tfp_tftp_ip。

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

testname = 'TestCase 5.3'
avoiderror(testname)
printTimer(testname,'Start','Directly upgrade image file from ap')

################################################################################
#Step 1
#操作
#telnet访问AP1
#WLAN-AP login: admin
#Password:admin
#
#预期
# 进入AP img模式，get system中“version”显示为“当前版本号”
################################################################################
printStep(testname,'Step 1',
          'Get ap version on ap1')

#operate
EnterWirelessMode(switch1)
SetCmd(switch1,'discovery ip-list ' + ap1backupip)
SetCmd(switch1,'discovery ip-list ' + ap2backupip)
SetCmd(ap1,'set management static-ip ' + ap1backupip)
SetCmd(ap2,'set management static-ip ' + ap2backupip)
IdleAfter(180)
#SetCmd(switch1,'wireless ap download image-type ' + imagetype + ' tftp://' + updateserver + '/' + aptestimg)
EnterConfigMode(switch3)
SetCmd(switch3,'vlan 777')
SetCmd(switch3,'interface vlan 777')
SetCmd(switch3,'ip address ' + updatel3ip + ' 255.255.255.0')
SetCmd(switch3,'exit')
SetCmd(switch3,'interface ' + s3p6)
SetCmd(switch3,'no shutdown')
SetCmd(switch3,'switchport access vlan 777')
SetCmd(switch3,'exit')

data2 = SetCmd(switch1,'show run')
data1 = SetCmd(ap1,'get system')
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
    
print '#############################'
print 'Now ap version is    ' + version1
print 'You selected version ' + version2
print 'Will update to version' + version5
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
#把AP升级tar文件：upgrade_new.tar放到TFP/TFTP服务器，在AP img下升级版本
#WLAN-AP# firmware-upgrade tftp://tfp_tftp_ip/upgrade_new.tar
#
#预期
#AP自动重启后进入img，使用命令get system确认“version”显示“新版本号”
################################################################################
printStep(testname,'Step 2',
          'Firmware upgrade')

SetCmd(ap1,'firmware-upgrade tftp://' + updateserver + '/' + aptestimg,timeout=1)
SetCmd(ap1,'y',timeout=1)
IdleAfter(370)
SetCmd(ap1,'admin',timeout=1)
SetCmd(ap1,'admin',timeout=1)
SetCmd(ap1,'admin',timeout=1)

data1 = SetCmd(ap1,'get system')
re1 = re.search('version           (\d+\.\d+\.\d+\.\d+)',data1)
if re1 is not None:
    version3 = re1.group(1)
else:
    version3 = 'error3'

print '#############################'
print 'Now ap1 version is ' + version3
print '#############################'

if version3 == version5:
    res1 = 0
else:
    res1 = 1

#result
printCheckStep(testname, 'Step 2',res1)

################################################################################
#Step 3
#操作
#等待AP被AC1管理
#AP被AC1管理上，show wireless ap version status查看“Software Version”显示“新版本号”
################################################################################
printStep(testname,'Step 3',
          'Show wireless ap version status.')

data7 = SetCmd(switch1,'show wireless ap version status')
res1 =CheckLine(data7,version5)

printCheckStep(testname, 'Step 3',res1)

################################################################################
#Step 4
#操作
#Return to initial config
################################################################################
printStep(testname,'Step 4',
          'Return to initial config.')
SetCmd(ap1,'firmware-upgrade tftp://' + updateserver + '/' + apnowimg,timeout=1)
SetCmd(ap1,'y',timeout=1)
IdleAfter('370')
SetCmd(switch1,'')
SetCmd(ap1,'',timeout=1)
SetCmd(ap2,'',timeout=1)
SetCmd(ap1,'admin',timeout=1)
SetCmd(ap1,'admin',timeout=1)
SetCmd(ap1,'admin',timeout=1)
SetCmd(ap2,'admin',timeout=1)
SetCmd(ap2,'admin',timeout=1)
SetCmd(ap2,'admin',timeout=1)

data1 = SetCmd(ap1,'get system')
re1 = re.search('version           (\d+\.\d+\.\d+\.\d+)',data1)
if re1 is not None:
    version3 = re1.group(1)
else:
    version3 = 'error3'
    
data1 = SetCmd(ap2,'get system')
re1 = re.search('version           (\d+\.\d+\.\d+\.\d+)',data1)
if re1 is not None:
    version4 = re1.group(1)
else:
    version4 = 'error4'

print '#############################'
print 'Now ap1 version is ' + version3
print 'Now ap2 version is ' + version4
print '#############################'

EnterConfigMode(switch3)
SetCmd(switch3,'no interface vlan 777')
SetCmd(switch3,'no vlan 777')

SetCmd(switch3,'interface ' + s3p6)
SetCmd(switch3,'shutdown')

EnterWirelessMode(switch1)
SetCmd(switch1,'no discovery ip-list ' + ap1backupip)
SetCmd(switch1,'no discovery ip-list ' + ap2backupip)
SetCmd(ap1,'set management static-ip ' + Ap1_ipv4)
SetCmd(ap1,'save-running')
SetCmd(ap2,'set management static-ip ' + Ap2_ipv4)
SetCmd(ap2,'save-running')
IdleAfter(180)
if (version3 == version1) and (version4 == version1):
    res1 = 0
else:
    res1 = 1

printCheckStep(testname, 'Step 4',res1)
#end
printTimer(testname, 'End')