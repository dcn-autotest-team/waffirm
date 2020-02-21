#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# performance_3.3.2.py 
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2017 Digital China Networks Co. Ltd
#
# Features:
# 3.3.2 ap通过串口登录，执行firmware-updata tftp进行ap直接升级，反复执行1000次，每次都能升级成功，
# 并能够被AC成功管理上，整个过程中终端反复连接，连接成功后上传下载文件
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
    
testname = 'Performance_test 3.3.2'
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
    函数：通过AP串口升级AP版本，升级成功后，客户端关联AP并下载文件，循环执行上述过程
    输入：total_cycle_time，循环次数,此参数定义在performance_topu文件中，不需要再次定义
    输出：无
    用法：maintest(total_cycle_time)
    '''
    global totaltime
    global upgrade_successtime
    global sta_download_successtime
    global performance_stopflag

    ap1version = Get_apversion_fromac(switch1,ap1mac)
    print('total_cycle_time=',total_cycle_time)
    for i in range(int(total_cycle_time/2)):
        for j in range(2):
            # 一个循环AP会升级两次版本，第一次升级为apnewversion，第二次降级为apoldversion
            apversionfile=ap1_old_versionfile if j==0 else ap1_now_versionfile
            apversionnum=ap1_old_versionnum if j==0 else ap1_now_versionnum
            ################################################################################
            # step1:检查AP是否可以ping通升级服务器
            ################################################################################
            printStep(testname,'Step 1','Basic configuration', 'ap1 ping tftpserver successfully')
            res1 = CheckPing(ap1,updateserver,mode='linux')
            if res1 != 0:
                print('ap ping tftpserver failed,please check!!!!!!!!!!!')

            printCheckStep(testname, 'Step 1',res1)
            ################################################################################
            # step2:升级AP，并检查是否升级成功
            ################################################################################
            printStep(testname,'Step 2','ap upgrade and check ap version on ac')
            res2 = 1
            totaltime += 1
            # data = SetCmd(ap1,'firmware-upgrade tftp://'+updateserver+'/'+apversionfile,promotePatten='(Starting kernel)|(Firmware upgrade failed)',promoteTimeout=360)
            # AP升级
            data = ApSetcmd(ap1,Ap1cmdtype,'firmware_upgrade',updateserver,'/',apversionfile,promotePatten='(Starting kernel)|(Firmware upgrade failed)',promoteTimeout=360)
            # 检查是否升级成功
            if CheckLine(data,'Firmware upgrade failed') == 0:
                print('AP download img file failed,please check!!!!!!!!!')
            elif CheckLine(data,'Starting kernel') == 0:
                IdleAfter(30)
                ApLogin(ap1,retry=20)
                # 检查AP是否被AC成功管理
                res2a = CheckSutCmd(switch1,'show wireless ap status', \
                                    check=[(ap1mac,'Managed','Success')], \
                                    waittime=5,retry=20,interval=5,IC=True)
                                    
                ap1version = Get_apversion_fromac(switch1,ap1mac)
                if res2a == 0:
                    # 检查升级后的AP版本和预期是否一致
                    if ap1version == apversionnum:
                        res2 = 0
                        upgrade_successtime += 1
                    else:
                        print('ap upgrade failed ,please check!!!!!!!')
            else:
                pass

            printCheckStep(testname, 'Step 2',res2)
            if res2 == 0:
                ################################################################################
                # step3:AP升级成功并被AC管理后，sta关联AP并上传下载文件
                ################################################################################
                printStep(testname,'Step 3','STA1 connect to test1 and download file from pc1')
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

                printCheckStep(testname, 'Step 3',res3)
            
            # 打印当前总循环次数、升级成功次数、客户端下载成功次数
            printAll('Total upgrade time is '+ str(totaltime))
            printAll('Successful upgrade time is ' + str(upgrade_successtime))
            printAll('Successful download time is '+ str(sta_download_successtime))
            
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

