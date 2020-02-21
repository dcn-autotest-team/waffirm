#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_6.6.1.py - test case 6.6.1 of waffirm
#
# Author: ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 6.6.1 SSH访问稳定性
# 测试目的：测试可以通过ssh方式访问AC和AP
# 测试环境：同测试拓扑
# 测试描述：可以通过ssh方式访问AC（ip地址1.1.1.1）和AP（20.1.1.3）。
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

testname = 'TestCase 6.6.1'
avoiderror(testname)
printTimer(testname,'Start','Test SSH')

################################################################################
#Step 1
#操作
#S1上开启ssh：
#config 
#ssh-server enable
#
#预期
#s1上show ssh-server显示“ssh server is enabled”。
################################################################################

printStep(testname,'Step 1',
          'set ssh-server enable on s1,',
          'config success.')

EnterEnableMode(switch1)
SetCmd(switch1,'clear logging sdram')
EnterConfigMode(switch1)
SetCmd(switch1,'ssh-server enable')
#check
data = SetCmd(switch1,'show ssh-server',timeout=5)
res = CheckLine(data,'ssh server is enabled')
#result
printCheckStep(testname, 'Step 1',res)


################################################################################
#Step 2
#操作
#Pc1上ssh方式访问ac1（用户名密码都是admin），
#（ssh方式访问ac1后）在ac1上show wireless ap status。
#在ac1上show tech-support
#预期
#Pc1可以ssh访问ac1。show wireless ap status显示ap1为“Managed Success”状态。
################################################################################

printStep(testname,'Step 2',
          'pc1 ssh login ac1,',
          'pc1 ssh login ac1 success,',
          'show tech-support,',
          'show wireless ap status on pc1, ap1 is Managed Success.')
res=1
res1=0		  
SetCmd(pc1,'rm -f /root/.ssh/known_hosts')
SetCmd(pc1,'ssh '+Ssh_login_name+'@'+StaticIpv4_ac1,promoteTimeout=5,promotePatten='yes/no')
SetCmd(pc1,'yes',promoteTimeout=5,promotePatten='password:')
SetCmd(pc1,Ssh_login_password)
EnterEnableMode(pc1)
SetCmd(pc1,'terminal length 512')
data = SetCmd(pc1,'show wireless ap status')
res = CheckLine(data,ap1mac,IC=True)
data = SetCmd(pc1,'show wireless ap status')
res1 = CheckLine(data,'command not found',IC=True)
if res1 == 0:
	res1 = 1	
#result
printCheckStep(testname, 'Step 2',res)
loginflag = res1
if loginflag == 0:
    ################################################################################
    #Step 3
    #操作
    #PC1上连续30次对AC1进行show tech-support操作后在ac1上show wireless ap status。
    #
    #预期
    #show wireless ap status显示ap1为“Managed Success”状态。
    ################################################################################

    printStep(testname,'Step 3',
              'show tech-support,',
              'show wireless ap status on pc1, ap1 is Managed Success.')
    #check
    res=1
    res1=0
    data = SetCmd(pc1,'show tech-support',promoteTimeout=60,promotePatten='-More-')
    while(1):	
        if CheckLine(data,'-More-',IC=True) == 0:
            data = SetCmd(pc1,'\0x20',promoteTimeout=10,promotePatten='-More-')					
        elif CheckLine(data,'The End',IC=True)==0 or CheckLine(data,'#',IC=True)==0:
            break
    data = SetCmd(pc1,'show wireless ap status')
    res = CheckLine(data,ap1mac,'Managed','Success',IC=True)
    data = SetCmd(pc1,'show wireless ap status')
    res1 = CheckLine(data,'command not found',IC=True)
    if res1 == 0:
        res1 = 1
    else:
        res1 = 0	
    #result
    printCheckStep(testname, 'Step 3',res,res1)

################################################################################
#Step 4
#操作
#恢复初始配置
################################################################################
printStep(testname,'Step 4',
          'Recover initial config for switches.')

#operate
data = SetCmd(pc1,'show wireless ap status')
res = CheckLine(data,'command not found',IC=True)
if res != 0:
    SetCmd(pc1,'exit')
EnterConfigMode(switch1)	
SetCmd(switch1,'no ssh-server enable')

#end
printTimer(testname, 'End')





