#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# performance_3.2.1.py 
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2017 Digital China Networks Co. Ltd
#
# Features:
# 3.2.1 通过POE交换机控制ap反复上下电重启，反复执行1000次，每一次都能重启成功，
# 并能够被ac成功管理上，整个过程中终端反复连接，连接成功后下载上传文件
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.11.27
#*******************************************************************************
# individualflag参数用于判断脚本执行入口，在performance_main.py文件中将会用到
individualflag = True

# multirunflag参数用于判断脚本执行入口，定义在performance_main.py文件中，如果不存在multirunflag参数，说明执行入口为当前文件
if 'multirunflag' not in vars():
    exec(compile(open('performance_main.py', "rb").read(), 'performance_main.py', 'exec'))
    
testname = 'Performance_test 3.2.1'
printTimer(testname,'Start','no power inline enable on POE switch(s3), ap reboot because poweroff.Repeat that 1000 times')

#parameter（以下参数不需修改）
total_reboottime = 0    #脚本执行的总循环次数
reboot_successtime=0    #AP重启成功的次数
reboot_failtime=0    #脚本执行AP升级的失败次数
sta_download_successtime=0    #AP重启成功后，客户端关联AP并成功下载文件的次数
sta_download_failtime=0    #AP重启成功后，客户端关联AP下载文件的失败次数
performance_stopflag = False    #用于判断sta2循环关联AP的操作何时终止

#function   
def sta_connect_ssid_circularly(sta,netcard,ssid,**args):
    '''    
    函数：实现客户端循环关联AP，直至主程序停止
    输入：同函数WpaConnectWirelessNetwork
          可选参数printflag，建议执行此函数时增加关键字参数printflag=False，在执行过程中不会在Dauto平台console中输出打印，可以减少打印
    输出：无
    用法：sta_connect_ssid_circularly（sta2,Netcard_sta2,Network_name1,bssid=ap1mac_type1,printflag=False)
    '''
    while not performance_stopflag:
        res1 = WpaConnectWirelessNetwork(sta,netcard,ssid,retry=0,**args) 
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
            # step1:通过POE交换机控制ap上下电重启，检查AP是否重启成功，是否被AC管理
            ################################################################################
            printStep(testname,'Step 1','no power inline enable on POE switch(s3), ap reboot because poweroff,then check')
            res1=res2=1
            total_reboottime += 1
            SetCmd(ap1,'\n')
            # POE交换机端口停止供电，再恢复供电
            StartDebug(ap1)
            EnterConfigMode(switch3)
            SetCmd(switch3,'interface',s3p3)
            SetCmd(switch3,'no power inline enable')
            IdleAfter(5)
            SetCmd(switch3,'power inline enable')
            IdleAfter(40)
            data = StopDebug(ap1)
            # 检查AP是否重启
            if CheckLine(data,'Starting kernel') == 0:
                res1 = 0
                reboot_successtime = 1
            ApLogin(ap1,retry=20)
            # 检查AP是否被AC成功管理
            res2 = CheckSutCmd(switch1,'show wireless ap status', \
                                check=[(ap1mac,'Managed','Success')], \
                                waittime=5,retry=20,interval=5,IC=True)

            printCheckStep(testname, 'Step 1',res1,res2)
            if res1 == 0 and res2 == 0:
                ################################################################################
                # step2:AP升级成功并被AC管理后，sta关联AP并上传下载文件
                ################################################################################
                printStep(testname,'Step 2','STA1 connect to test1 and download file from pc1')
                res3 = 1
                res3a = WpaConnectWirelessNetwork(sta1,Netcard_sta1,Network_name1,bssid=ap1mac_type1) 
                if res3a == 0:
                    sta1_ipresult = GetStaIp(sta1)
                    sta1_ipv4 = sta1_ipresult['ip']
                    res3b = CheckPing(sta1,pc1_ipv4,mode='linux')
                    if res3b == 0:
                        data = SetCmd(sta1,'downloadtest -u http://' + pc1_ipv4 + ':90/upgrade1.tar')
                        res3c = re.search('speed is      :\s+(\d+\.\d+)\s+MB/s',data)
                        if res3c:
                            res3 = 0
                            sta_download_successtime += 1
                        else:
                            print('sta can not download file from pc1,please check!!!!!!!!!!')

            printCheckStep(testname, 'Step 2',res3)
            
            # 打印当前总循环次数、升级成功次数、客户端下载成功次数
            print('Total reboot time is',total_reboottime)
            print('Successful reboot time is',reboot_successtime)
            print('Successful download time is',sta_download_successtime)
            
        # performance_stopflag为全局变量，用于判断sta2循环关联AP的操作何时终止
    performance_stopflag = True
    print('performance.stopflagmain =',performance_stopflag)
                   
def run(total_cycle_time):
    threadslist = []
    t1 = CallThread(maintest,total_cycle_time)
    threadslist.append(t1)
    t2 = CallThread(sta_connect_ssid_circularly,sta2,Netcard_sta2,Network_name1,bssid=ap1mac_type1,printflag=False)
    threadslist.append(t2)
    for t in threadslist:
        t.start()
    for t in threadslist:
        t.join()   
    print('performance_stopflagrun =',performance_stopflag)   
    
# 执行程序 ，total_cycle_time定义在拓扑文件中                               
run(total_cycle_time)     

printTimer(testname, 'End')

