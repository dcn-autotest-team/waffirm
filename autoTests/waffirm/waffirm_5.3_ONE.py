#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# waffirm_5.3_ONE.py
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2017 Digital China Networks Co. Ltd
#
# Features:
# 5.3	在AP上直接升级image测试（手工测试，部分可自动化）
# 测试目的：测试在img下升级ap版本
# 测试环境：同测试拓扑1。
# 测试描述：在img下升级ap版本。TFP/TFTP服务器ip：tfp_tftp_ip。对于epa280-l和2000-l这两种ap，
# 有无流量监控功能，若5分钟内没有流量，AP会重启。Ap升级传输版本时间约为30秒（具体时间视版本大小）
# ，写flash时间约为2分钟，我们设计了两种telnet升级场景，一种是版本传输未完成情况下，
# 传输中或版本校验过程中，用户敲ctrl+c强制退出，传输中断，ap升级失败；一种是版本传输完成后
# ，在写flash过程中，用户敲ctrl+c强制退出，ap依然可以升级成功（老系统的ap像79xx系列的ap，
# 版本传输完一旦开始写flash，telnet自动中断，而openWRT系统的新ap，写flash过程中telnet不会自动退出，
# 若用户强制ctrl+c，则telnet产生的session进程可以过继给其他进程，保证ap可以升级成功）。
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.4
#*******************************************************************************
import random

testname = 'TestCase 5.3'
avoiderror(testname)
printTimer(testname,'Start','firmware-upgrade ap version and quit by using ctrl+c')


################################################################################
#Step 1
#操作
# S3 telnet访问AP1
# WLAN-AP login: admin
# Password:admin
# AP1 ping 升级服务器
# 查看AP版本
#预期
# AP1可以ping通升级服务器
################################################################################
printStep(testname,'Step 1',\
          'Basic configuration', \
          'ap1 ping tftpserver successfully'
		  'S3 telnet ap1')

res1=1
#operate
# 修改S3配置
EnterConfigMode(switch3)
SetCmd(switch3,'vlan 1')
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'switchport mode access')
SetCmd(switch3,'switchport access vlan 1')
EnterInterfaceMode(switch3,'vlan 1')
IdleAfter(Vlan_Idle_time)
SetIpAddress(switch3,If_vlan1_s3_ipv4,'255.255.255.0')
# 修改AP1的IP
ap1_iptail = random.randint(101,250)
ap1_newip = '100.1.1.'+str(ap1_iptail)
ApSetcmd(ap1,Ap1cmdtype,'set_static_ip',ap1_newip)
ApSetcmd(ap1,Ap1cmdtype,'set_ip_route','100.1.1.254')
ApSetcmd(ap1,Ap1cmdtype,'saverunning')
res1 = CheckPing(ap1,updateserver,mode='linux')
if res1 != 0:
    print 'ap ping tftpserver failed,please check!!!!!!!!!!!'

printCheckStep(testname, 'Step 1',res1)
# 如果AP1 ping不通升级服务器，则后续升级步骤都不执行
if res1 == 0:
    ################################################################################
    #Step 2
    #操作
    # 把AP1升级tar文件：upgrade_new.tar放到TFP/TFTP服务器，在AP img下升级版本
    # WLAN-AP# firmware-upgrade tftp://tfp_tftp_ip/upgrade_new.tar
    # 等待20s，手工敲ctrl+c
    #预期
    # telnet退出(部分交换机设备不会退出telnet登录)，AP升级失败，get system version显示版本号为“旧版本号”
    ################################################################################
    printStep(testname,'Step 2','S3 telnet ap,and upgrade ap version,quit by using ctrl+c after 20s')
    res1=1
    # S3 telnet登录AP1
    EnterEnableMode(switch3)
    data = SetCmd(switch3,'telnet '+ap1_newip,promotePatten='login|Unable to connect',promoteTimeout=15)
    if CheckLine(data,'login') != 0:
        print 'AC can not telnet AP,please check!!!!!!!!!!!!'
    else:
        res1a = TelnetLogin(switch3,'admin','admin')
        if res1a == 0:
            # 登录成功后对AP1升级，并等待20s
            SetCmd(switch3,'firmware-upgrade tftp://'+updateserver+'/'+standby_build,promotePatten='Connection closed|(Firmware upgrade failed)',promoteTimeout=20)
            # 键入ctrl+C
            data1 = SetCmd(switch3,'\x03',promotePatten='Connection closed|(Firmware upgrade failed)',promoteTimeout=10)
            # 检查S3是否退出telnet登录，如果没有退出则手工输入exit退出
            if CheckLine(data1,'Connection closed') != 0:
				SetCmd(switch3,'exit')
            # 检查AP1升级失败，仍为旧版本
            data2 = ApSetcmd(ap1,Ap1cmdtype,'getsystem')
            res1 = re.search('^version\s+'+current_buildnum,data2,re.M)
            res1 = 0 if res1 else 1
        else:
            print 'S3 telnet login ap1 failed,please check!!!!!'
    # result
    printCheckStep(testname, 'Step 2',res1)        
    ################################################################################
    #Step 3
    #操作
    # 再次fireware-upgrade，等待telnet自动断开
    #预期
    #不同ap有不同表现：
    # （1）	Eap_V_patch流AP（主要是下述四款AP：79xx、2000-l，epa280-l，2000）和eap-X_V_patch流ap
    # （主要是8200I2\I3\W2三款AP），版本文件传输完成一旦开始写flash，不等敲ctrl+c，telnet自行退出。
    # （2）	T2/IT2/2000WAP2.0/I2-R2/I3R2这些ap，在开始写flash后，telnet进程会卡住几秒再退出（进程过继）
    # 共同表现：AP升级成功。系统起来后，登陆AP，查看版本get system version为“新版本号”
    ################################################################################
    printStep(testname,'Step 3','S3 telnet ap,and upgrade ap version,waiting for telnet disconnected automatically')
    res1=res2= 1  
    # S3 telnet登录AP1
    EnterEnableMode(switch3)
    data = SetCmd(switch3,'telnet '+ap1_newip,promotePatten='login|Unable to connect',promoteTimeout=15)
    if CheckLine(data,'login') != 0:
        print 'AC can not telnet AP,please check!!!!!!!!!!!!'
    else:
        res1a = TelnetLogin(switch3,'admin','admin')
        if res1a == 0:
            # 登录成功后对AP1升级，并等待telnet自动断开
            data1 = SetCmd(switch3,'firmware-upgrade tftp://'+updateserver+'/'+standby_build,promotePatten='Connection closed|(Firmware upgrade failed)',promoteTimeout=300)
            # 等待telnet连接自动断开
            if CheckLine(data1,'Firmware upgrade failed') == 0:
                print 'AP download img file failed,please check!!!!!!!!!'
            elif CheckLine(data1,'Connection closed') == 0:
                res1 = 0
                # 等待AP重启
                SetCmd(ap1,'\n',promotePatten='(Starting kernel)|(Firmware upgrade failed)',promoteTimeout=300)
                SetCmd(switch3,'\x03')
                IdleAfter(30)
                ApLogin(ap1,retry=20)
            # 检查AP1升级为新版本(AP升级版本重启后不会立马显示为新版本，需要等待几秒)
            for i in range(3):
                IdleAfter(3)
                data2 = ApSetcmd(ap1,Ap1cmdtype,'getsystem')
                res2 = re.search('^version\s+'+standby_buildnum,data2,re.M)
                res2 = 0 if res2 else 1
                if res2 == 0:
                    break       
        else:
            print 'S3 telnet login ap1 failed,please check!!!!!'
    # result
    printCheckStep(testname, 'Step 3',res1,res2)    
    ################################################################################
    #Step 4
    #操作
    # 打开无流量监控，并配置L3（poe sw）无流量监控时间为3分钟（新poe设备默认是150s，
    # 老的poe设备默认是30s，时间都短了，为避免写flash失败把ap搞坏，我们改为180s）,配置下电时长为5s：
    # S3(config)#power inline enable
    # S3(config)#power inline monitor interval 180
    # S3(config)#power inline reset
    # S3(config)#power inline reset interval 5
    # S3(config)#interface Ethernet s3p3
    # S3(config-if-s3p3)# power inline enable
    # 在S3上telnet AP1，fireware-upgrade升级方式，将版本从upgrade_new.tar升级到upgrade_old.tar
    #预期
    # AP升级成功。待AP系统起来后，get system version显示版本号为“旧版本号”
    ################################################################################
    printStep(testname,'Step 4','Config power inline monitor on S3', \
                        'S3 telnet ap,upgrade ap version,waiting for telnet disconnected automatically',\
                        'check ap upgrade successully')
    res1=res2=1
    # operate
    EnterConfigMode(switch3)
    SetCmd(switch3,'power inline enable')
    SetCmd(switch3,'power inline monitor interval 180')
    # SetCmd(switch3,'power inline reset')
    SetCmd(switch3,'power inline reset interval 5')
    EnterInterfaceMode(switch3,s3p3)
    SetCmd(switch3,'power inline enable')
    SetCmd(switch3,'power inline monitor on')
    # S3 telnet登录AP1
    EnterEnableMode(switch3)
    data = SetCmd(switch3,'telnet '+ap1_newip,promotePatten='login|Unable to connect',promoteTimeout=15)
    if CheckLine(data,'login') != 0:
        print 'AC can not telnet AP,please check!!!!!!!!!!!!'
    else:
        res1a = TelnetLogin(switch3,'admin','admin')
        if res1a == 0:
            # 登录成功后对AP1升级
            data1 = SetCmd(switch3,'firmware-upgrade tftp://'+updateserver+'/'+current_build,promotePatten='Connection closed|(Firmware upgrade failed)',promoteTimeout=300)
            # 等待telnet连接自动断开
            if CheckLine(data1,'Firmware upgrade failed') == 0:
                print 'AP download img file failed,please check!!!!!!!!!'
            elif CheckLine(data1,'Connection closed') == 0:
                res1 = 0
                # 等待AP重启
                SetCmd(ap1,'\n',promotePatten='(Starting kernel)|(Firmware upgrade failed)',promoteTimeout=300)
                SetCmd(switch3,'\x03')
                IdleAfter(30)
                ApLogin(ap1,retry=20)
            # 检查AP1升级为新版本(AP升级版本重启后不会立马显示为新版本，需要等待几秒)
            for i in range(3):
                IdleAfter(3)
                data1 = ApSetcmd(ap1,Ap1cmdtype,'getsystem')
                res2 = re.search('^version\s+'+current_buildnum,data1,re.M)
                res2 = 0 if res2 else 1
                if res2 == 0:
                    break
        else:
            print 'S3 telnet login ap1 failed,please check!!!!!'
            
    # result
    printCheckStep(testname, 'Step 4',res1,res2)
    # 如果AP升级失败，单独升级AP到测试版本        
    if res2 != 0:
        data = ApSetcmd(ap1,Ap1cmdtype,'firmware_upgrade',updateserver,'/',current_build,promotePatten='(Starting kernel)|(Firmware upgrade failed)',promoteTimeout=360)
        # 检查是否升级成功
        if CheckLine(data,'Firmware upgrade failed') == 0:
            print 'AP download img file failed,please check!!!!!!!!!'
        elif CheckLine(data,'Starting kernel') == 0:
            IdleAfter(30)
            ApLogin(ap1,retry=20)
        else:
            pass

################################################################################
#Step 5
#操作
# 等待AP重新上线。
#预期
# AP被AC1管理成功，show wireless ap version status查看“Software Version”显示“旧版本号”
################################################################################
printStep(testname,'Step 5','Check if AC1 managed AP1')
res1=res2=1 
# operate
# 修改S3配置
# 集中转发、本地转发差异化配置，testcentral为True代表集中转发配置，False代表本地转发配置
if testcentral == True:
    EnterConfigMode(switch3)
    SetCmd(switch3,'vlan',Vlan20)
    SetCmd(switch3,'switchport interface',s3p3)
else:
    EnterConfigMode(switch3)
    SetCmd(switch3,'interface',s3p3)
    SetCmd(switch3,'switchport mode trunk')
    SetCmd(switch3,'switchport trunk native vlan',Vlan20)
    
EnterInterfaceMode(switch3,'vlan 1')
IdleAfter(Vlan_Idle_time)
SetCmd(switch3,'no ip address')
# 修改AP1的IP
ApSetcmd(ap1,Ap1cmdtype,'set_static_ip',Ap1_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'set_ip_route',If_vlan20_s3_ipv4)
ApSetcmd(ap1,Ap1cmdtype,'saverunning')

res1=CheckSutCmd(switch1,'show wireless ap status', \
                check=[(ap1mac,'Managed','Success')], \
                waittime=5,retry=20,interval=5,IC=True)
                
ap1_now_versionnum = Get_apversion_fromac(switch1,ap1mac)
if current_buildnum ==  ap1_now_versionnum:
    res2 = 0
# result
printCheckStep(testname, 'Step 5',res1,res2)
################################################################################
#Step 6
#操作
#恢复默认配置
################################################################################
printStep(testname,'Step 6',\
          'Recover initial config.')

EnterConfigMode(switch3)
SetCmd(switch3,'power inline monitor interval 150')       
EnterInterfaceMode(switch3,s3p3)
SetCmd(switch3,'power inline monitor off')
# end
printTimer(testname, 'End')

