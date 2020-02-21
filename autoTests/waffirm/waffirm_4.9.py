#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_4.9.py - test case 4.9 of waffirm
#
# Author:  qidb@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2011 Digital China Networks Co. Ltd
#
# Features:
# 4.9 License Control基本功能测试（手工测试）
# 测试目的：测试通过License文件控制AC所能够管理的AP数量是否生效。
# 测试环境：同测试拓扑1
# 测试描述：通过向AC导入一定数量的License文件，测试其管理的AP数量能否达到预期数值。
#           执行本测试例之前，要先确认被测AC的型号以及所支持的AP最大数量、License
#           文件中AP数量以及增加的步长等参数。
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

testname = 'TestCase 4.9'
avoiderror(testname)
printTimer(testname,'Start','License control test')

################################################################################
#Step 1
#操作
#在AC1上通过show license命令查看AC1内存放的缺省license文件。
#AC1的flash中存在缺省的license文件，限制AC1最多能管理x个AP。
################################################################################
printStep(testname,'Step 1',
          'Show license')
#operate
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless switch local status')
re1 = re.search('Maximum Managed Access Points.................. (\d+)',data1)
if re1 is not None:
    maxap = int(re1.group(1).strip())
    res1 = 0
else:
    maxap = 2
    res1 = 1
#check

#IdleAfter(Pc_client_login_wait_time)
#result
printCheckStep(testname, 'Step 1',res1)

################################################################################
#Step 2
#操作
#通过license文件生成工具生成2个license文件，每个文件限制AC管理AP数量为y个并导入AC1。
#
#预期
#在AC1上show license可以查看到两个新导入的license文件。此时共存在3个license文件，AC1最多可以管理x+2*y个AP。
################################################################################

printStep(testname,'Step 2',
          'Create license files.')

res = 0
printCheckStep(testname, 'Step 2',res1)


################################################################################
#Step 3
#操作
#在PC2启动AP模拟器模拟大于x+2*y个AP，在AC1上面配置相应的AP database。
#
#预期
#只有x+2*y-1个可以被AC1管理（AC1本身管理AP1）。
################################################################################

printStep(testname,'Step 3',
          'simulate ap')

if maxap > maxapcount:
    apcount = maxapcount
else:
    apcount = maxap
EnterConfigMode(switch1)
SetCmd(switch1,'wireless')
SetCmd(switch1,'ap profile 1')
SetCmd(switch1,'hwtype 1')
SetCmd(switch1,'exit')
startmac = apsimstartmac
#for itemp in range(apcount):
for itemp in range(270): 
    SetCmd(switch1,'ap database ' + startmac)
    startmac = incrmac(startmac,step=16)
    SetCmd(switch1,'exit')
EnterConfigMode(switch3)
SetCmd(switch3,'interface vlan 20')
SetCmd(switch3,'ip address ' + apsimtempip + ' 255.255.0.0')
SetCmd(switch3,'interface ' + s3p7)
SetCmd(switch3,'no shutdown')
SetCmd(switch3,'switchport access vlan 20')
IdleAfter(apcount * 10)
EnterEnableMode(switch1)
data2 = SetCmd(switch1,'show wireless ap status')
re2 = re.search('Total Access Points............................ (\d+)',data2)
if re2 is not None:
    onlineap = int(re2.group(1))
else:
    onlineap = -1
if onlineap == apcount:
    res1 = 0
else:
    res1 = 1


printCheckStep(testname, 'Step 3',res1)



################################################################################
#Step 4
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 4',
          'Recover initial config for switches.')

#operate
EnterConfigMode(switch1)
SetCmd(switch1,'wireless')
SetCmd(switch1,'ap profile 1')
SetCmd(switch1,'hwtype ' + hwtype1)
SetCmd(switch1,'exit')
startmac = apsimstartmac
#for itemp in range(apcount):
for itemp in range(270):    
    SetCmd(switch1,'no ap database ' + startmac)
    startmac = incrmac(startmac,step=16)
    #SetCmd(switch1,'exit')
EnterConfigMode(switch3)
SetCmd(switch3,'interface vlan 20')
SetCmd(switch3,'ip address ' + If_vlan20_s3_ipv4 + ' 255.255.255.0')
SetCmd(switch3,'interface ' + s3p7)
SetCmd(switch3,'shutdown')
IdleAfter(120)
EnterEnableMode(switch1)
SetCmd(switch1,'clear wireless ap failed',timeout=1)
SetCmd(switch1,'y',timeout=1)

#end
printTimer(testname, 'End')