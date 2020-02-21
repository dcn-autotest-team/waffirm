#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_6.6.2.py - test case 6.6.2 of waffirm
#
# Author: ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2012 Digital China Networks Co. Ltd
#
# Features:
# 6.6.2 测试控制终端登录测试
# 测试目的：测试控制终端登录功能
# 测试环境：同测试拓扑
# 测试描述：配置控制登录后ap能正常上线，满足条件终端能登录到AC.
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

testname = 'TestCase 6.6.2'
avoiderror(testname)
printTimer(testname,'Start','Test SSH')
# 定义函数CheckStaSshAC,用于检查sta是否成功ssh到AC
def CheckStaSshAC(sut,ip,loginname,loginpassword,check1='yes/no',check2=[(ap1mac)],failflag1=False):
    res = SshLogin(sut,ip,loginname,loginpassword,check=check1,failflag=failflag1)
    if failflag1:
        return res
    if res == 0:
        data1 = SetCmd(sut,'show wireless ap status')
        res = CheckLineList(data1,check2,IC=True)
        loginflag = CheckLine(data1,'command not found',IC=True)
        if loginflag != 0:
            data2 = SetCmd(sut,'exit')
            res2 = CheckLine(data2,'Connection to','closed',IC=True)
            if res2 != 0:
                SetCmd(sut,'exit')

    return res
################################################################################
#Step 1
#操作
#在AC1配置network1的SSID为test1，关联vlan4091，配置下发到AP1，
#配置network2的SSID为test2，关联vlan4092，配置下发到AP2
#在AC1上面将vlan4091和vlan4092加入到l2-tunnel vlan-list中
#
#(以上均包含在初始配置之中)
#
#
#预期
#通过show wireless l2-tunnel vlan-list可以看到vlan4091和vlan4092
################################################################################
printStep(testname,'Step 1',
          'set ssh-server enable on s1,',
          'config success.'
          'Show wireless l2tunnel vlan-list',
          'Check if contain vlan 4091,4092')

res1=1
#operate
EnterConfigMode(switch1)
SetCmd(switch1,'ssh-server enable')
data = SetCmd(switch1,'show ssh-server',timeout=5)

EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show wireless l2tunnel vlan-list')

#check
res = CheckLine(data,'ssh server is enabled')
res1 = CheckLineList(data1,[(Vlan4091),(Vlan4092)],IC=True)

#result
printCheckStep(testname, 'Step 1',res,res1)

################################################################################
#Step 2
#操作
#将STA1,STA2 分别关联到AP1的网络test1，AP2的 test2
#
#预期
#关联成功
#客户端STA1能够获取192.168.91.X网段的IP地址，STA2能够获取192.168.92.X网段的IP地址.
################################################################################

printStep(testname,'Step 2',
          'STA1 connect to test1, get 192.168.91.x ip via dhcp',
          'STA2 connect to test1, get 192.168.92.x ip via dhcp')

sta1_ipv4 = ''
sta2_ipv4 = ''

res1=res2=res3=res4=1

#operate
#STA1,STA2关联 network1
res1 = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_lower)
res2 = WpaConnectWirelessNetwork(sta2,Netcard_sta2,Network_name2,bssid=ap2mac_type1_network2)
IdleAfter(10)

#获取STA1,STA2的地址
sta1_ipresult = GetStaIp(sta1,checkippool=Dhcp_pool1)
sta1_ipv4 = sta1_ipresult['ip']
res3 = sta1_ipresult['res']

sta2_ipresult = GetStaIp(sta2,checkippool=Dhcp_pool2)
sta2_ipv4 = sta2_ipresult['ip']
res4 = sta2_ipresult['res']

#result
printCheckStep(testname, 'Step 2',res1,res2,res3,res4)

# 如果客户端无法关联network或无法获取IP，则不执行后续步骤
keeponflag = res1 + res2 + res3 + res4
if GetWhetherkeepon(keeponflag):
    ################################################################################
    #Step 3 Step 4
    #操作
    #sta1,sta2上ssh方式访问ac1（用户名密码都是admin），
    #（ssh方式访问ac1后）在ac1上show wireless ap status.
    #
    #预期
    #sta1,sta2可以ssh访问ac1.show wireless ap status显示ap1为“Managed Success”状态.
    ################################################################################

    printStep(testname,'Step 3,Step 4',
              'sta1 ssh login ac1,',
              'sta2 ssh login ac1,',
              'sta1 ssh login ac1 success,',
              'sta2 ssh login ac1 success,',
              'show wireless ap status on sta1,sta2 ap1 is Managed Success.')
    res = res1 = res2 = res3 = 1
    #check
    SetCmd(sta1,'rm -f /root/.ssh/known_hosts',timeout=2)
    res = CheckStaSshAC(sta1,StaticIpv4_ac1,Ssh_login_name,Ssh_login_password)

    SetCmd(sta2,'rm -f /root/.ssh/known_hosts',timeout=5)
    res1 = CheckStaSshAC(sta2,StaticIpv4_ac1,Ssh_login_name,Ssh_login_password)

    # result
    printCheckStep(testname, 'Step 3 Step 4',res,res1)
    ################################################################################
    #Step 5
    #操作
    #sta1,sta2上ssh方式访问ac1（用户名密码都是admin），
    #（ssh方式访问ac1后）在ac1上show wireless ap status.
    #
    #预期
    #sta1不可以ssh访问ac1
    #sta2可以ssh访问ac1.show wireless ap status显示ap1为“Managed Success”状态.
    ################################################################################

    printStep(testname,'Step 5',
              'sta1 ssh login ac1,',
              'sta2 ssh login ac1,',
              'sta1 ssh login ac1 failed,',
              'sta2 ssh login ac1 success,',
              'show wireless ap status on sta2 ap1 is Managed Success.')
    res1=res2=1
    logflag3=logflag4=1
    #check
    EnterConfigMode(switch1)
    SetCmd(switch1,'access-list 1 permit ' + sta2_ipv4 + ' 0.0.0.255')
    SetCmd(switch1,'access-list 1 permit ' + Ap1_ipv4 + ' 0.0.0.255')
    SetCmd(switch1,'access-list 1 permit ' + Ap2_ipv4 + ' 0.0.0.255')
    SetCmd(switch1,'authentication ip access-class 1 in')
    IdleAfter(40)
    SetCmd(sta1,'rm -f /root/.ssh/known_hosts',timeout=2)
    res1 = SshLogin(sta1,StaticIpv4_ac1,Ssh_login_name,Ssh_login_password,options='-o ConnectTimeout=30',check='timed out',timeout1=35,failflag=True)
    res1 = 0 if res1 == 2 else 1

    SetCmd(sta2,'rm -f /root/.ssh/known_hosts',timeout=2)
    res2 = CheckStaSshAC(sta2,StaticIpv4_ac1,Ssh_login_name,Ssh_login_password)

    printCheckStep(testname, 'Step 5',res1,res2)

################################################################################
#Step 6
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 6',
          'Recover initial config')

#operate
#解关联
WpaDisconnectWirelessNetwork(sta1,Netcard_sta1)
WpaDisconnectWirelessNetwork(sta2,Netcard_sta2)


#删除step4的配置
EnterConfigMode(switch1)
SetCmd(switch1,'no authentication ip access-class')
SetCmd(switch1,'no access-list 1')
SetCmd(switch1,'no ssh-server enable')
EnterWirelessMode(switch1)
SetCmd(switch1,'ap profile 1')
SetCmd(switch1,'no management vlan')
SetCmd(switch1,'no ethernet native-vlan')
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap eth-parameter apply profile 1',timeout=1)
SetCmd(switch1,'y',timeout=1)


#end
printTimer(testname, 'End')