#-*- coding: UTF-8 -*-#
#*******************************************************************************
# module_config_topu.py
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2008 Digital China Networks Co. Ltd
#
# Features:  存放变量信息
#
#*******************************************************************************
# Change log:
#     - 2017.12.7 created by zhangjxp
#*******************************************************************************
yourstring = 'exportal_test1'
set_default = 1
upgrade_device = 0
ap_new_versionfile = 'DCWL_79xx_R4_R5_2_3_1_29.tar'
ap_new_versionnum = '2.3.1.29'
ap_old_versionfile = 'DCWL_79xx_R4_R5_2_3_1_28.tar'
ap_old_versionnum = '2.3.1.28'
mainkeeponflag = False #用于判断脚本运行中如过客户端无法关联无线或无法获取IP时，是否继续执行后续步骤，True代表继续执行，False代表跳过后续步骤
radio5Gswitch = False #适配WAVE3项目，5G有两个radio，此参数为True时，可选择配置5G为radio2或radio3
radio5G = 2 #当radio5Gswitch=True时，此参数可以配置为2或3，表示5G为radio2或radio3


pc1 = 'pc1'
sta1 = 'sta1'
sta2 = 'sta2'
ap1 = 'ap1'
ap2 = 'ap2'
switch1 = 's1'
switch2 = 's2'
switch3 = 's3'

EnvName = 'bj'
EnvNo = '1'
# 定义ssid
Network_name1 = 'module_'+EnvName+'_'+EnvNo+'1'
Network_name2 = 'module_'+EnvName+'_'+EnvNo+'2'
Network_name3 = 'module_'+EnvName+'_'+EnvNo+'3'

#连接类型
pc1_type = 'Telnet'
pc1_host = '172.17.100.182'
sta1_type = 'Telnet'
sta1_host = '172.17.100.165'
sta2_type = 'Telnet'
sta2_host = '172.17.100.166'
switch1_type = 'TelnetCCM'
switch1_host = '172.17.100.242:10001'
switch2_type = 'TelnetCCM'
switch2_host = '172.17.100.242:10002'
switch3_type = 'TelnetCCM'
switch3_host = '172.17.100.242:10003'
ap1_type = 'TelnetCCM'
ap1_host = '172.17.100.242:10004'
ap2_type = 'TelnetCCM'
ap2_host = '172.17.100.242:10005'
 
testerip_sta1 = sta1_host
testerip_sta2 = sta2_host
testerp1_sta1 = '1'
testerp1_sta2 = '1'

testerip_wired = pc1_host
testerp1_wired = '1'

#设备端口定义
s1p1 = 'Ethernet1/0/1'
s2p1 = 'Ethernet1/0/1'

#S3连接AC1
s3p1 = 'Ethernet1/0/1'
#S3连接AC2
s3p2 = 'Ethernet1/0/3'
#S3连接AP1
s3p3 = 'Ethernet1/0/5'
#S3连接AP2
s3p4 = 'Ethernet1/0/7'
#连接 pc1 192.168.10网段
s3p5 = 'Ethernet1/0/15'
#连接80
s3p6 = 'Ethernet1/0/17'
#连接ap模拟器 暂时没用到
s3p7 = 'Ethernet1/0/12'

Pc1_telnet_name = 'root'
Pc1_telnet_password = '123456'
Ap_login_name = 'admin'
Ap_login_password = 'admin'
Ssh_login_name = 'admin'
Ssh_login_password = 'admin'