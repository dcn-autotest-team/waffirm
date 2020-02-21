#-*- coding: UTF-8 -*
from dreceiver import *
from lib_all import *
import time
import re
import random
import wx

set_default = 1
upgrade_device = 0

execfile('waffirm_config_topu.py')
execfile('waffirm_config_vars.py')
execfile('waffirm_config_run.py')

#连接PC1,STA1,STA2,方式为 Telnet
CreateNewConn(pc1_type,pc1,pc1_host,None,'run')
TelnetLogin(pc1,Pc1_telnet_name,Pc1_telnet_password)
CreateNewConn(sta1_type,sta1,sta1_host,None,'run')
TelnetLogin(sta1,Pc1_telnet_name,Pc1_telnet_password)
CreateNewConn(sta2_type,sta2,sta2_host,None,'run')
TelnetLogin(sta2,Pc1_telnet_name,Pc1_telnet_password)

#连接 AC1,AC2,S3
CreateNewConn(switch1_type,switch1,switch1_host,None,'run')
Receiver(switch1,'\n\n')
TelnetLogin(switch1,Pc1_telnet_name,Pc1_telnet_password)
CreateNewConn(switch2_type,switch2,switch2_host,None,'run')
Receiver(switch2,'\n\n')
TelnetLogin(switch2,Pc1_telnet_name,Pc1_telnet_password)
CreateNewConn(switch3_type,switch3,switch3_host,None,'run')

Receiver(switch1,'\n\n')
SetCmd(switch1,'cd /home/dscc',timeout=5)
SetCmd(switch1,'./start.sh nos.img',promoteStop=30)
SetCmd(switch1,'./dcn_console',timeout=10)
Receiver(switch1,'\n\n')

SetCmd(switch2,'cd /home/dscc',timeout=5)
SetCmd(switch2,'./start.sh nos.img',promoteStop=30)
SetCmd(switch2,'./dcn_console',timeout=10)
Receiver(switch2,'\n\n')
		
#连接AP1,AP2
CreateNewConn(ap1_type,ap1,ap1_host,None,'run')
CreateNewConn(ap2_type,ap2,ap2_host,None,'run')
#登录AP1,AP2 (第一次连接AP需要登录)
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

if set_default == 1:#this defined in topo file
#S1-3恢复出厂设置
    SetDefault(switch3)
    EnterEnableMode(switch3)
    Receiver(switch3,'write')
    IdleAfter(1)
    Receiver(switch3,'y')
    ReloadMultiSwitch([switch3])
    if EnvNo == '4':#云AC环境S1-2恢复出厂设置
        ac1 = 'ac1'
        ac2 = 'ac2'
        		
        CreateNewConn('Telnet',ac1,switch1_host,None,'run')
        CreateNewConn('Telnet',ac2,switch2_host,None,'run')
        TelnetLogin(ac1,Pc1_telnet_name,Pc1_telnet_password)
        TelnetLogin(ac2,Pc1_telnet_name,Pc1_telnet_password)

        SetCmd(ac1,'pkill -9 dcn_console')
        SetCmd(ac1,'pkill -9 monitor.sh')
        SetCmd(ac1,'pkill -9 nos.img')
        SetCmd(ac1,'rm -rf /home/dscc/startup.cfg')

        SetCmd(ac2,'pkill -9 dcn_console')
        SetCmd(ac2,'pkill -9 monitor.sh')
        SetCmd(ac2,'pkill -9 nos.img')
        SetCmd(ac2,'rm -rf /home/dscc/startup.cfg')
        IdleAfter(10)
        Receiver(switch1,'\n\n')
        SetCmd(switch1,'cd /home/dscc',timeout=5)
        SetCmd(switch1,'./start.sh nos.img',promoteStop=30)
        SetCmd(switch1,'./dcn_console',timeout=20)
        Receiver(switch1,'\n\n')

        SetCmd(switch2,'cd /home/dscc',timeout=5)
        SetCmd(switch2,'./start.sh nos.img',promoteStop=30)
        SetCmd(switch2,'./dcn_console',timeout=20)
        Receiver(switch2,'\n\n')
        CloseChannels(ac1)
        CloseChannels(ac2)
    else:
        SetDefault(switch1)
        SetDefault(switch2)

        EnterEnableMode(switch1)
        EnterEnableMode(switch2)
        Receiver(switch1,'write')
        Receiver(switch2,'write')
        IdleAfter(1)
        Receiver(switch1,'y')
        Receiver(switch2,'y')
        IdleAfter(5)
        ReloadMultiSwitch([switch1,switch2])

#AP1-2恢复出厂设置
    FactoryResetMultiAp([ap1,ap2])

    Receiver(switch1,'\n\n\n')
    Receiver(switch2,'\n\n\n')
    Receiver(switch3,'\n\n\n')
    EnterEnableMode(switch1)
    EnterEnableMode(switch2)
    EnterEnableMode(switch3)
    Receiver(switch1,'terminal length 0')
    Receiver(switch2,'terminal length 0')
    Receiver(switch3,'terminal length 0')

#登录AP1,AP2 (第一次连接AP需要登录)
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

if upgrade_device == 1: #this defined in topo file
    upgrade_s1boot = 0
    upgrade_s1img = 0
    upgrade_s2boot = 0
    upgrade_s2img = 0
    upgrade_s3boot = 0
    upgrade_s3img = 0
    upgrade_ap1img = 0
    upgrade_ap2img = 0
    print '###########################################################'
    print "######### Now searching all devices's files ###############"
    IdleAfter(1)
    if os.path.isfile('c:\\version\\env' + EnvNo + '\\s1boot.rom'):
        upgrade_s1boot = 1
        print "######## AC1's boot file 's1boot.rom' founded #############"
    if os.path.isfile('c:\\version\\env' + EnvNo + '\\s1nos.img'):
        upgrade_s1img = 1
        print "######## AC1's img file 's1nos.img' founded   #############"
    if os.path.isfile('c:\\version\\env' + EnvNo + '\\s2boot.rom'):
        upgrade_s2boot = 1
        print "######## AC2's boot file 's2boot.rom' founded #############"
    if os.path.isfile('c:\\version\\env' + EnvNo + '\\s2nos.img'):
        upgrade_s2img = 1
        print "######## AC2's img file 's2nos.img' founded   #############"
    if os.path.isfile('c:\\version\\env' + EnvNo + '\\s3boot.rom'):
        upgrade_s3boot = 1
        print "######## S3's boot file 's3boot.rom' founded  #############"
    if os.path.isfile('c:\\version\\env' + EnvNo + '\\s3nos.img'):
        upgrade_s3img = 1
        print "######## S3's img file 's3nos.img' founded    #############"
    if os.path.isfile('c:\\version\\env' + EnvNo + '\\ap1.tar'):
        upgrade_ap1img = 1
        print "######## AP1's img file 'ap1.tar' founded     #############"
    if os.path.isfile('c:\\version\\env' + EnvNo + '\\ap2.tar'):
        upgrade_ap2img = 1
        print "######## AP2's img file 'ap2.tar' founded     #############"

    IdleAfter(5)
    print '###########################################################'
    execfile('waffirm_upgrade_device.py')
		
## 获取AC1和AP1的版本信息，并更新至testlink
EnterEnableMode(switch1)
data1 = SetCmd(switch1,'show version')
print data1
s1ver = re.search('Version ([^\n ]+)',data1)
EnterEnableMode(switch2)
print SetCmd(switch2,'show version')
data2 = SetCmd(ap1,'get system')
print data2
ap1ver = re.search('version\s+([^\n ]+)',data2)
print SetCmd(ap2,'get system')
if 'DCWS' in tl.__args__['testDevice'] or tl.__args__['testDevice'] == 'DSCC':
    if s1ver != None and tl.__args__['testBuild'] == 'Dynamic Create':
        #更新testBuild,交换机s1的版本
        tl.__args__['testBuild'] = str(s1ver.group(1))
        tl.__args__['notes'] = data1
        print 's1 version is:',str(s1ver.group(1))
else:
    if ap1ver != None and tl.__args__['testBuild'] == 'Dynamic Create':
        #更新testBuild,AP1的版本
        tl.__args__['testBuild'] = str(ap1ver.group(1))
        tl.__args__['notes'] = data2
        print 'ap1 version is:',str(ap1ver.group(1))    
###更新testSuite
tl.__args__['testSuite'] = 'waffirm'

##获得sta1的mac地址
data = SetCmd(sta1,'ifconfig -v',Netcard_sta1,promotePatten='#',timeout=3)
sta1mac_memory = re.search('\w\w:\w\w:\w\w:\w\w:\w\w:\w\w',data)
sta1mac_type1 = sta1mac_memory.group(0)
#mac 地址连接符可能为 ':' 或者 '-'
if None != re.search(':',sta1mac_type1):
    sta1mac_list = str(sta1mac_type1).split(':')
    sta1mac = '-'.join(sta1mac_list).lower()
else:
    sta1mac = sta1mac_type1.lower()   
     
##获得sta2的mac地址
data = SetCmd(sta2,'ifconfig -v',Netcard_sta2,promotePatten='#',timeout=3)
sta2mac_memory = re.search('\w\w:\w\w:\w\w:\w\w:\w\w:\w\w',data)
sta2mac_type1 = sta2mac_memory.group(0)
if None != re.search(':',sta2mac_type1):
    sta2mac_list = str(sta2mac_type1).split(':')
    sta2mac = '-'.join(sta2mac_list).lower()
else:
    sta2mac = sta2mac_type1.lower()

sta1mac_upcase = sta1mac.upper()
sta2mac_upcase = sta2mac.upper()
print sta1mac
print sta2mac

#开启sta1，sta2的wpa_supplicant
SetCmd(sta1,'ifconfig %s up' % Netcard_sta1)
IdleAfter(2)
data = SetCmd(sta1,'iwconfig')
if 0 != CheckLine(data,'%s' % Netcard_sta1):
    SetCmd(sta1,'rmmod iwldvm')
    SetCmd(sta1,'rmmod iwlwifi')
    IdleAfter(5)
    SetCmd(sta1,'modprobe iwlwifi')
#data = SetCmd(sta1,'ifconfig mon0')
if 0 != CheckLine(data,'mon0'):
    SetCmd(sta1,'airmon-ng start ' + Netcard_sta1)
IdleAfter(2)	
SetCmd(sta1,'pkill -9 wpa_supplicant')
IdleAfter(3)
SetCmd(sta1,'wpa_supplicant -B -i '+ Netcard_sta1 +' -c /etc/wpa_supplicant/wpa_supplicant.conf -f /tmp/wpa_log/%s.log' % Netcard_sta1)

SetCmd(sta2,'ifconfig %s up' % Netcard_sta2)
IdleAfter(2)
data = SetCmd(sta2,'iwconfig')
if 0 != CheckLine(data,'%s' % Netcard_sta2):
    SetCmd(sta2,'rmmod iwldvm')
    SetCmd(sta2,'rmmod iwlwifi')
    IdleAfter(5)
    SetCmd(sta2,'modprobe iwlwifi')
#data = SetCmd(sta2,'ifconfig mon0')
if 0 != CheckLine(data,'mon0'):
    SetCmd(sta2,'airmon-ng start ' + Netcard_sta2)
IdleAfter(2)
SetCmd(sta2,'pkill -9 wpa_supplicant')
IdleAfter(3)
SetCmd(sta2,'wpa_supplicant -B -i '+ Netcard_sta2 +' -c /etc/wpa_supplicant/wpa_supplicant.conf -f /tmp/wpa_log/%s.log' % Netcard_sta2)

#Get VLAN mac from AC1 (switch1)
EnterEnableMode(switch1)
SetCmd(switch1,'terminal length 0')
printRes('Get vlanmac of AC1...')
EnterInterfaceMode(switch1,'vlan 1')
s1vlanmac = GetVlanMac(switch1)
EnterConfigMode(switch1)
SetCmd(switch1,'no interface vlan 1')
SetWatchdogDisable(switch1)
SetExecTimeout(switch1)

#获取 Ap1,Ap2 的mac地址
SetCmd(ap1,'\n')
data1 = SetCmd(ap1,'get management')
ap1mac_type1 = str(GetValueBetweenTwoValuesInData (data1,'mac\s+','\n')).lstrip().rstrip()
ap1mac_list = str(ap1mac_type1).split(':')
ap1mac = '-'.join(ap1mac_list).lower()
ap1mac_lower = ap1mac_type1.lower()
ap1mac_lower_5g = incrmac(ap1mac_lower,16).lower()

data2 = SetCmd(ap2,'get management')
ap2mac_type1 = str(GetValueBetweenTwoValuesInData (data2,'mac\s+','\n')).lstrip().rstrip()

ap2mac_list = str(ap2mac_type1).split(':')
ap2mac = '-'.join(ap2mac_list).lower()
ap2mac_lower = ap2mac_type1.lower()
ap2mac_lower_5g = incrmac(ap2mac_lower,16).lower()

ap2mac_type1_network2 = incrmac(ap2mac_lower)
ap2mac_type1_network2_5g = incrmac(ap2mac_lower_5g)

probe_request_replace_value = ' '.join(sta2mac_type1.lower().split(':'))
deauth_replace_value1 = ' '.join(ap1mac_type1.lower().split(':'))
deauth_replace_value2 = ' '.join(sta2mac_type1.lower().split(':'))
deauth_replace_value3 = ' '.join(ap1mac_type1.lower().split(':'))
deauth_replace_value = deauth_replace_value1 + ' ' + deauth_replace_value2 + ' ' +deauth_replace_value3
auth_replace_value1 = ' '.join(ap1mac_type1.lower().split(':'))
auth_replace_value2 = ' '.join(sta2mac_type1.lower().split(':'))
auth_replace_value3 = ' '.join(ap1mac_type1.lower().split(':'))
auth_replace_value = auth_replace_value1 + ' ' + auth_replace_value2 + ' ' + auth_replace_value3
 
#获取AP的 device-type (id)
tempdata1 = SetCmd(ap1,'get system device-type')
tempdata2 = SetCmd(ap2,'get system device-type')
hwtype1 = re.search('(\d+)',tempdata1).group(1)
hwtype2 = re.search('(\d+)',tempdata2).group(1)
SetCmd(sta1,'ifconfig ' + Netcard_sta1 + ' up')
SetCmd(sta1,'rm -rf /tmp/capture/*.cap')
SetCmd(sta1,'rm -rf /tmp/wpa_log/*.log')
SetCmd(sta1,'rm -rf /root/nohup.out')
SetCmd(sta2,'ifconfig ' + Netcard_sta2 + ' up')
SetCmd(sta1,'rm -rf /tmp/capture/*.cap')
SetCmd(sta1,'rm -rf /tmp/wpa_log/*.log')
SetCmd(sta1,'rm -rf /root/nohup.out')
if len(testlist) > 0:
    for runtime in range(runtimes):
        printRes('|runtime:|'+str(runtime+1))
        execfile('waffirm_initial.py')
        wx.FindWindowById(10).nowrunning = ''
        wx.FindWindowById(10).faillist = []
        for test in testlist:
            if test[1] <= priority:
                wx.FindWindowById(10).nowrunning = test[0]
                execfile(test[0])
                print wx.FindWindowById(10).faillist
        execfile('waffirm_uninitial.py')
    printGlobal('TestCase '+str('waffirm'),'End')
    faillister = wx.FindWindowById(10).faillist[:]
    if len(faillister) > 0:
        IdleAfter(5)
        CreateNewConn(pc1_type,pc1,pc1_host,None,'run')
        CreateNewConn(sta1_type,sta1,sta1_host,None,'run')
        CreateNewConn(sta2_type,sta2,sta2_host,None,'run')

        #连接 AC1,AC2,S3
        CreateNewConn(switch1_type,switch1,switch1_host,None,'run')
        CreateNewConn(switch2_type,switch2,switch2_host,None,'run')
        CreateNewConn(switch3_type,switch3,switch3_host,None,'run')

        #连接AP1,AP2
        CreateNewConn(ap1_type,ap1,ap1_host,None,'run')
        CreateNewConn(ap2_type,ap2,ap2_host,None,'run')
        printGlobal('TestCase '+str('waffirm'),'Start')
        for fileTemp in faillister:
            execfile(fileTemp)
        printGlobal('TestCase '+str('waffirm'),'End')
    printGlobal('TestCase '+str('waffirm'),'TlEnd')