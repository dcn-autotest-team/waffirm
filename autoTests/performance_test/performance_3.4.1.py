#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# performance_3.4.1.py
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2017 Digital China Networks Co. Ltd
#
# Features:
# 3.4.1	10台ap（包含I3R2/I2R2/WL2/I2/79五类机型）同时和ac建立连接，并通过ac下发配置文件
# (包含3个radio、15个vap，覆盖射频管理、用户隔离、广播抑制、ap逃生、portal功能等配置)，
# pc持续打入100pps的arp和dhcp广播报文，在ac上批量给ap升级（版本在本地ftp服务器上），
# 可以一次升级成功，反复执行1000次
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.13
#*******************************************************************************
# individualflag参数用于判断脚本执行入口，在performance_main.py文件中将会用到
individualflag = True

# multirunflag参数用于判断脚本执行入口，定义在performance_main.py文件中，如果不存在multirunflag参数，说明执行入口为当前文件
if 'multirunflag' not in vars():
    exec(compile(open('performance_main_oneap.py', "rb").read(), 'performance_main_oneap.py', 'exec'))
    
testname = 'Performance_test 3.4.1'
printTimer(testname,'Start','firmware-upgrade 1000 times and ap behave correctly')

#parameter（以下参数不需修改）
totaltime = 0    #脚本执行的总循环次数
upgrade_successtime=0    #脚本执行AP升级的成功次数
upgrade_failtime=0    #脚本执行AP升级的失败次数
sta_download_successtime=0    #AP升级成功后，客户端关联AP并成功下载文件的次数
sta_download_failtime=0    #AP升级成功后，客户端关联AP下载文件的失败次数
performance_stopflag = False    #用于判断sta2循环关联AP的操作何时终止
if total_cycle_time < 2:
    total_cycle_time = 2
    
exec(compile(open('performance_special_initial.py', "rb").read(), 'performance_special_initial.py', 'exec'))
#function   
def sta_connect_ssid_circularly(sta,netcard,ssid,connectType,bssidlist,**args):
    '''    
    函数：实现客户端循环关联AP，直至主程序停止
    输入：同函数WpaConnectWirelessNetwork
          可选参数printflag，建议执行此函数时增加关键字参数printflag=False，在执行过程中不会在Dauto平台console中输出打印，可以减少打印
    输出：无
    用法：sta_connect_ssid_circularly（sta2,Netcard_sta2,Network_name1,bssidlist=bssid_list,printflag=False)
    '''
    while not performance_stopflag:
        bssid = random.choice(bssidlist)
        res1 = WpaConnectWirelessNetwork(sta,netcard,ssid,connectType,retry=0,bssid=bssid,**args)
        if res1 == 0:
            sta_ipresult = GetStaIp(sta)
            sta_ipv4 = sta_ipresult['ip']
            res2 = CheckPing(sta,pc1_ipv4,mode='linux')
            if res2 == 0:
                SetCmd(sta,'downloadtest -u http://' + pc1_ipv4 + ':90/upgrade1.tar')
        IdleAfter(5,printflag=False)

def maintest(total_cycle_time,**args):
    '''    
    函数：通过AP串口升级AP版本，升级成功后，客户端关联AP并下载文件，循环执行上述过程
    输入：total_cycle_time，循环次数,此参数定义在performance_topu文件中，不需要再次定义
    输出：无
    用法：maintest(total_cycle_time)
    '''
    global totaltime
    global upgrade_successtime
    global sta_download_successtime
    global performance_stopflag
    # ###############################################################################
    # # step1:检查AP是否可以ping通升级服务器
    # ###############################################################################
    # printStep(testname,'Step 1','Basic configuration', 'ap1 ping tftpserver successfully')
    # res1 = 1
    # res1_list = []
    # for k in range(total_apnum):
        # res = CheckPing(ap_name_list[k],updateserver,mode='linux')
        # if res != 0:
            # print ap_name_list[k]+' ping tftpserver failed,please check!!!!!!!!!!!'
        # res1_list.append(res)
    # if len(res1_list) == total_apnum:
        # res1 = 1 if 1 in res1_list else 0
    # printCheckStep(testname, 'Step 1',0)
    for i in range(int(total_cycle_time/2)):
        for j in range(2):
            # 一个循环AP会升级两次版本，第一次升级为apnewversion，第二次降级为apoldversion
            ap_versionfile_list=ap_oldversionfile_list if j==0 else ap_nowversionfile_list
            ap_versionnum_list=ap_oldversionnum_list if j==0 else ap_nowversionnum_list
            ################################################################################
            # step2:升级AP，并检查是否升级成功
            ################################################################################
            printStep(testname,'Step 2','ap upgrade and check ap version on ac')
            res2 = res3 = 1
            totaltime += 1
            EnterWirelessMode(switch1)
            for k in range(total_apnum):
                # ftp升级
                SetCmd(switch1,'wireless ap download image-type '+ap_imagetype_list[k]+' ftp://'+ftpuser+':'+ftppwd+'@'+updateserver+'/'+ap_versionfile_list[k])
                # tftp升级
                # SetCmd(switch1,'wireless ap download image-type '+ap_imagetype_list[k]+' tftp://'+updateserver+'/'+ap_versionfile_list[k])
            EnterEnableMode(switch1)
            SetCmd(switch1,'wireless ap download start')
            IdleAfter(330)
            for k in range(12):
                data = SetCmd(switch1,'show wireless ap download')
                temp1 = re.search('Success Count.*?(\d+)\s',data)
                if temp1:
                    successnum = int(temp1.group(1))
                    print('successnum',successnum)
                    print('total_apnum',total_apnum)
                    if successnum == total_apnum:
                        res2 = 0
                        upgrade_successtime += 1
                        break
                    else:
                        IdleAfter(5)
                else:
                    pass
            for k in range(total_apnum):
                # ApLogin(ap_name_list[k],retry=5)
                
                CheckSutCmd(switch1,'show wireless ap status | include ' + ap_mac_list[k], \
                                    check=[(ap_mac_list[k],'Managed','Success')], \
                                    waittime=5,retry=5,interval=5,IC=True)
            if res2 != 0:
                data = SetCmd(switch1,'show wireless ap download')
                for k in range(total_apnum):
                    if ap_mac_list[k] in data:
                        print(ap_name_list[k],'version should be',ap_versionnum_list[k])
                        print(ap_name_list[k],'upgrade failed ,please check!!!!!!!')
            printCheckStep(testname, 'Step 2',res2)
            printAll('Total upgrade time is '+ str(totaltime))
            printAll('Successful upgrade time is '+ str(upgrade_successtime))
            ################################################################################
            # step3:AP升级成功并被AC管理后，sta关联AP并上传下载文件
            ################################################################################
            # printStep(testname,'Step 3','STA1 connect to test1 and download file from pc1')
            # res4 = 1
            # res4_list = []
            # for k in range(total_apnum):
                # res4a = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='wpa_psk',psk='12345678',bssid=ap_bssid_list[k]) 
                # if res4a == 0:
                    # res4b = CheckPing(sta1,pc1_ipv4,mode='linux')
                    # if res4b == 0:
                        # data = SetCmd(sta1,'downloadtest -u http://' + pc1_ipv4 + ':90/upgrade1.tar')
                        # res4c = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s',data)
                        # if res4c:
                            # res4_list.append(0)
                        # else:
                            # res4_list.append(1)
                            # print 'sta connect to',ap_name_list[k],'but can not download file from pc1,please check!!!!!!!!!!'
                # else:
                    # print 'sta can not connect to',ap_name_list[k],'please check!!!!!'
            # if len(res4_list) == len(ap_name_list):
                # res4 = 1 if 1 in res4_list else 0
            # if res4 == 0:
                # sta_download_successtime += 1
            # printCheckStep(testname, 'Step 3',res4)
            
            # 打印当前总循环次数、升级成功次数、客户端下载成功次数
            # print 'Total upgrade time is',totaltime
            # print 'Successful upgrade time is',upgrade_successtime
            # print 'Successful download time is',sta_download_successtime
            
        # performance_stopflag为全局变量，用于判断sta2循环关联AP的操作何时终止
    performance_stopflag = True
    print('performance.stopflagmain =',performance_stopflag)
                   
def run(total_cycle_time):
    threadslist = []
    t1 = CallThread(maintest,total_cycle_time)
    threadslist.append(t1)
    # t2 = CallThread(sta_connect_ssid_circularly,sta2,Netcard_sta2,Network_name1,bssidlist=ap_bssid_list,printflag=False)
    t2 = CallThread(sta_connect_ssid_circularly,sta2,Netcard_sta2,Network_name1,connectType='wpa_psk',psk='12345678',bssidlist=ap_bssid_list,printflag=False)
    threadslist.append(t2)
    for t in threadslist:
        t.start()
    for t in threadslist:
        t.join()   
    print('performance_stopflagrun =',performance_stopflag)
    
# 开启背景流量
try:
    res = ConnectDsendWireless(testerip_wired)
    SetDsendStreamWireless(Port=testerp1_wired,PortTypeConfig='0',StreamMode='2',StreamRateMode='pps',StreamRate='100',NumFrames='1', \
                       SouMac = pc1mac,DesMac='ff-ff-ff-ff-ff-ff',\
                       Protocl='arp',ArpOperation='2',\
                       TargetIp=StaticIpv4_ac1,\
                       StreamNum='1',LastStreamFlag= 'false')
    SetDsendStreamWireless(Port=testerp1_wired,PortTypeConfig='0',StreamMode='2',StreamRateMode='pps',StreamRate='100',NumFrames='1', \
                       SouMac = pc1mac,DesMac='ff-ff-ff-ff-ff-ff',\
                       StreamNum='2',LastStreamFlag= 'true')                   
    StartTransmitWireless(testerp1_wired)
except Exception as e:
    traceback.print_exc()    
# 执行程序 ，total_cycle_time定义在拓扑文件中                               
run(total_cycle_time)     

# 停止背景流量
try:
    StopTransmitWireless(testerp1_wired)
    DisconnectDsendWireless()
except Exception as e:
    traceback.print_exc()
printTimer(testname, 'End')

