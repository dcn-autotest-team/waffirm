#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# performance_func.py
#
# Author:  zhangjxp@digitalchina.com
#
# Version 1.0.0
#
# Copyright (c) 2004-2017 Digital China Networks Co. Ltd
#
# Features:
# 定义性能测试需要用到的函数
#
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2017.11.27
#*******************************************************************************
from globalpara import *
from dreceiver import *
from lib_all import *

from .performance_vars import *
#function   
def sta_connect_ssid_circularly(sta,netcard,ssid,**args):
    '''    
    函数：实现客户端循环关联AP，直至主程序停止
    输入：同函数WpaConnectWirelessNetwork
          可选参数printflag，建议执行此函数时增加关键字参数printflag=False，在执行过程中不会在Dauto平台console中输出打印，可以减少打印
    输出：无
    用法：sta_connect_ssid_circularly（sta2,Netcard_sta2,Network_name1,bssid=ap1mac_type1,printflag=False)
    '''
    # if 'event' in args:
        # myevent = args['event']
        # del args['event']
    # else:
        # myevent = MYEVENT
    # global performance_stopflag
    # performance_stopflag = False
    while not performance_stopflag:
        res1 = WpaConnectWirelessNetwork(sta,netcard,ssid,retry=0,**args) 
        if res1 == 0:
            sta_ipresult = GetStaIp(sta)
            sta_ipv4 = sta_ipresult['ip']
            res2 = CheckPing(sta,pc1_ipv4,mode='linux')
            if res2 == 0:
                SetCmd(sta,'downloadtest -u http://' + pc1_ipv4 + ':90/upgrade1.tar')
        IdleAfter(5,printflag=False)



