#-*- coding: UTF-8 -*-#
#*******************************************************************************
# module_vars.py - variables defination for waffirm test script
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features: 存放变量信息
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************
# 以下参数不需修改
# ssid
Network_name1 = 'module_'+EnvName+'_'+EnvNo+'1'
Network_name2 = 'module_'+EnvName+'_'+EnvNo+'2'
Network_name3 = 'module_'+EnvName+'_'+EnvNo+'3'
testerip_sta1 = sta1_host
testerip_sta2 = sta2_host
testerp1_sta1 = '1'
testerp1_sta2 = '1'
testerip_wired = pc1_host
testerp1_wired = '1'
Pc1_telnet_name = 'root'
Pc1_telnet_password = '123456'
Ap_login_name = 'admin'
Ap_login_password = 'admin'
Ssh_login_name = 'admin'
Ssh_login_password = 'admin'
pc1 = 'pc1'
sta1 = 'sta1'
sta2 = 'sta2'
ap1 = 'ap1'
ap2 = 'ap2'
switch1 = 's1'
switch2 = 's2'
switch3 = 's3'
                        
##################################################################################
## GetWhetherkeepon
## 
## function:
##     结合topo文件中的mainkeeponflag参数和脚本执行情况判断继续执行后续步骤
## args: 
##     keeponflag: 脚本上一步存在sta无法关联无线或无法获取IP地址的标志
##   
## examples:
##     GetWhetherkeepon（keeponflag）
################################################################################### 
def GetWhetherkeepon(flag):
    global mainkeeponflag
    if mainkeeponflag == True:
        return True
    else:
        if flag == 0:
            return True
        else:
            return False