#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# performance_3.2.2.py 
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2017 Digital China Networks Co. Ltd
#
# Features:
# 3.2.2	10台ap（包含I3R2/I2R2/WL2/I2/79五类机型），同时被ac管理，并通过ac下发配置文件
# (包含3个radio、15个vap，覆盖射频管理、用户隔离、广播抑制、ap逃生、portal功能等配置)，
# 持续打入100pps的arp和dhcp广播报文，操作ac反复重启ap1000次
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.12.13
#*******************************************************************************
import copy
# individualflag参数用于判断脚本执行入口，在performance_main.py文件中将会用到
individualflag = True

exec(compile(open('performance_main_oneap.py', "rb").read(), 'performance_main_oneap.py', 'exec'))

testname = 'Performance_test 3.2.2'
printTimer(testname,'Start','ac reboot ap for 1000 times')

#parameter（以下参数不需修改）
total_reboottime = 0    #脚本执行的总循环次数
reboot_successtime=0    #AP重启成功的次数
reboot_failtime=0    #脚本执行AP升级的失败次数
sta_download_successtime=0    #AP重启成功后，客户端关联AP并成功下载文件的次数
sta_download_failtime=0    #AP重启成功后，客户端关联AP下载文件的失败次数
performance_stopflag = False    #用于判断sta2循环关联AP的操作何时终止

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
    函数：通过POE交换机控制ap反复上下电重启，AP重启成功后，客户端关联AP并下载文件，循环执行上述过程
    输入：total_cycle_time，循环次数,此参数定义在performance_topu文件中，不需要再次定义
    输出：无
    用法：maintest(total_cycle_time)
    '''
    global total_reboottime
    global reboot_successtime
    global sta_download_successtime
    global performance_stopflag
    print('total_cycle_time=',total_cycle_time)
    for i in range(total_cycle_time):
        ################################################################################
        # step1:通过AC重启AP，检查AP是否重启成功，是否被AC管理
        ################################################################################
        printStep(testname,'Step 1','ac reboot ap')
        res1=res2=1
        total_reboottime += 1
        
        # 通过AC重启AP
        EnterEnableMode(switch1)
        SetCmd(switch1,'wireless ap reset',timeout=1)
        SetCmd(switch1,'y',timeout=1)
            
        # 在AC1上检测AP状态是否为failed
        temp_ap_mac_list = copy.deepcopy(ap_mac_list)
        for i in range(50):
            check_num = len(temp_ap_mac_list)
            for j in range(check_num):
                data = SetCmd(switch1,'show wireless ap status | include ' + temp_ap_mac_list[j],timeout=2)
                if CheckLine(data,'Failed', 'Not\s+Config',IC=True) == 0 or CheckLine(data,'Auth','In\s+Progress',IC=True) == 0:
                    temp_ap_mac_list.remove(temp_ap_mac_list[j])
                    break
            if len(temp_ap_mac_list) == 0:
                res1 = 0
                break
        else:
            if len(temp_ap_mac_list) != 0:
                print('some ap reboot failed,their mac is',temp_ap_mac_list)
            
        # 检查AP是否被AC成功管理
        temp_ap_mac_list = []
        for j in range(total_apnum):
            # ApLogin(ap_name_list[j],retry=20)
            res2a = CheckSutCmd(switch1,'show wireless ap status | include ' + ap_mac_list[j], \
                                check=[(ap_mac_list[j],'Managed','Success')], \
                                waittime=3,retry=30,interval=5,IC=True)
            if res2a == 0:
                temp_ap_mac_list.append(ap_mac_list[j])
        if len(temp_ap_mac_list) == len(ap_mac_list):
            res2 = 0
            reboot_successtime += 1
        else:
            print('some ap does not be managed by ac, please check !!!!!!')     
        printCheckStep(testname, 'Step 1',res1,res2)
        # if res1 == 0 and res2 == 0:
            # ################################################################################
            # # step2:AP重启成功并被AC管理后，sta关联AP并上传下载文件
            # ################################################################################
            # printStep(testname,'Step 2','STA1 connect to test1 and download file from pc1')
            # res3 = 1
            # res3_list = []
            # for j in range(total_apnum):
                # # res3a = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap_bssid_list[j]) 
                # res3a = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,connectType='wpa_psk',psk='12345678',bssid=ap_bssid_list[j]) 
                # if res3a == 0:
                    # res3b = CheckPing(sta1,pc1_ipv4,mode='linux')
                    # if res3b == 0:
                        # data = SetCmd(sta1,'downloadtest -u http://' + pc1_ipv4 + ':90/upgrade1.tar')
                        # res3c = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s',data)
                        # if res3c:
                            # res3_list.append(0)
                        # else:
                            # res3_list.append(1)
                            # print 'sta connect to',ap_name_list[j],'but can not download file from pc1,please check!!!!!!!!!!'
            # if len(res3_list) == len(ap_name_list):
                # res3 = 1 if 1 in res3_list else 0
            # if res3 == 0:
                # sta_download_successtime += 1
            # printCheckStep(testname, 'Step 2',res3)
        
        # 打印当前总循环次数、升级成功次数、客户端下载成功次数
        printAll('Total reboot time is '+ str(total_reboottime))
        printAll('Successful reboot time is '+ str(reboot_successtime))
        # printAll'Successful download time is '+sta_download_successtime)
            
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
    
# 执行程序 ，total_cycle_time定义在拓扑文件中                               
run(total_cycle_time)     

printTimer(testname, 'End')

