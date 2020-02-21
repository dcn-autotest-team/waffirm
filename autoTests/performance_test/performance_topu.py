#-*- coding: UTF-8 -*-#
#*******************************************************************************
# performance_topu.py
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
#     - 2017.12.5 created by zhangjxp
#*******************************************************************************
mainkeeponflag = False
radio5Gswitch = False
radio5G = 2
set_default = 0
upgrade_device = 0
total_cycle_time = 1000

ap1_imagetype = '18'
ap1_now_versionfile = 'WL8200-WH2_3.3.4.2.tar'
ap1_old_versionfile = 'WL8200-WH2_3.3.4.2.tar'

EnvName='sh'
EnvNo = '1'
pc1_type = 'Telnet'
pc1_host = '172.17.100.115'
sta1_type = 'Telnet'
sta1_host = '172.17.100.114'
sta2_type = 'Telnet'
sta2_host = '172.17.100.113'
ap1_type = 'TelnetCCM'
ap1_host = '172.17.100.237:10005'

switch1_type = 'TelnetCCM'
switch1_host = '172.17.100.237:10001'
switch3_type = 'TelnetCCM'
switch3_host = '172.17.100.237:10002'

s1p1 = 'Ethernet1/0/1'
# s2p1 = 'Ethernet1/0/1'
s3p1 = 'Ethernet1/0/1'
# s3p2 = 'Ethernet1/0/3'
s3p3 = 'Ethernet1/0/13'
# s3p4 = 'Ethernet1/0/7'
s3p5 = 'Ethernet1/0/9'
s3p6 = 'Ethernet1/0/11'

# 可选参数(存放AP信息）
aplist = [
# # {'name':'ap2',
# # 'type':'TelnetCCM',
# # 'host':'172.17.100.237:10006',
# # 's3port':'Ethernet1/0/14',
# # 'mac':'',
# # 'hwtype':'',
# # 'imagetype':'14',
# # 'now_versionfile':'WL8200-T2-IT2_3.3.1.24.tar',
# # 'old_versionfile':'WL8200-T2-IT2_3.3.1.22.tar'
# # },
# {'name':'ap3',
# 'type':'TelnetCCM',
# 'host':'172.17.100.237:10007',
# 's3port':'Ethernet1/0/15',
# 'mac':'00:03:0f:20:d9:40',
# 'hwtype':'22',
# 'imagetype':'2',
# 'now_versionfile':'DCWL_79xx_R4_R5_2_3_1_31.tar',
# 'old_versionfile':'DCWL_79xx_R4_R5_2_3_1_29.tar'
# },
# {'name':'ap4',
# 'type':'TelnetCCM',
# 'host':'172.17.100.237:10008',
# 's3port':'Ethernet1/0/16',
# 'mac':'00:03:0f:3a:38:10',
# 'hwtype':'32',
# 'imagetype':'11',
# 'now_versionfile':'DCWL_EAP280L_WAP200L_2_3_1_31.tar',
# 'old_versionfile':'DCWL_EAP280L_WAP200L_2_3_1_30.tar'
# },
# {'name':'ap5',
# 'type':'TelnetCCM',
# 'host':'172.17.100.237:10009',
# 's3port':'Ethernet1/0/17',
# 'mac':'00:03:0f:4a:87:20',
# 'hwtype':'33',
# 'imagetype':'12',
# 'now_versionfile':'WL8200-W2_2_3_2_31.tar',
# 'old_versionfile':'WL8200-W2_2_3_2_31.tar'
# },
# {'name':'ap6',
# 'type':'TelnetCCM',
# 'host':'172.17.100.237:10010',
# 's3port':'Ethernet1/0/18',
# 'mac':'00:03:0f:35:5c:80',
# 'hwtype':'29',
# 'imagetype':'8',
# 'now_versionfile':'WL8200-I2_2_3_2_32.tar',
# 'old_versionfile':'WL8200-I2_2_3_2_32.tar'
# },
# {'name':'ap7',
# 'type':'TelnetCCM',
# 'host':'172.17.100.237:10011',
# 's3port':'Ethernet1/0/19',
# 'mac':'00:03:0f:67:26:e0',
# 'hwtype':'41',
# 'imagetype':'15',
# 'now_versionfile':'WL8200-WL2_3.3.1.24.tar',
# 'old_versionfile':'WL8200-WL2_3.3.1.23.tar'
# },
# {'name':'ap8',
# 'type':'TelnetCCM',
# 'host':'172.17.100.237:10012',
# 's3port':'Ethernet1/0/20',
# 'mac':'fc:ad:0f:06:26:a0',
# 'hwtype':'39',
# 'imagetype':'14',
# 'now_versionfile':'WL8200-T2-IT2_3.3.1.24.tar',
# 'old_versionfile':'WL8200-T2-IT2_3.3.1.22.tar'
# },
# {'name':'ap9',
# 'type':'TelnetCCM',
# 'host':'172.17.100.237:10013',
# 's3port':'Ethernet1/0/21',
# 'mac':'00:03:0f:07:00:00',
# 'hwtype':'59',
# 'imagetype':'16',
# 'now_versionfile':'WL8200-I2-R2_3_3_2_22.tar',
# 'old_versionfile':'WL8200-I2-R2_3_3_2_21.tar'
# },
# {'name':'ap10',
# 'type':'TelnetCCM',
# 'host':'172.17.100.237:10014',
# 's3port':'Ethernet1/0/22',
# 'mac':'00:03:0F:8E:1C:30',
# 'hwtype':'60',
# 'imagetype':'17',
# 'now_versionfile':'WL8200-I3-R2_3.5.1.13.tar',
# 'old_versionfile':'WL8200-I3-R2_3.5.1.13.tar'
# },
# {'name':'ap11',
# 'type':'TelnetCCM',
# 'host':'172.17.100.237:10015',
# 's3port':'Ethernet1/0/23',
# 'mac':'00:03:0f:35:76:00',
# 'hwtype':'30',
# 'imagetype':'9',
# 'now_versionfile':'WL8200-I3_2_3_2_32.tar',
# 'old_versionfile':'WL8200-I3_2_3_2_32.tar'
# },
]

# 以下参数不需要修改
ftpuser = 'upload'
ftppwd = 'upload'
Network_name1 = 'affirm_auto'+EnvName+'_'+EnvNo+'1'
Network_name2 = 'affirm_auto'+EnvName+'_'+EnvNo+'2'
Network_name3 = 'affirm_auto'+EnvName+'_'+EnvNo+'3'
pc1 = 'pc1'
sta1 = 'sta1'
sta2 = 'sta2'
ap1 = 'ap1'
ap2 = 'ap2'
switch1 = 's1'
switch2 = 's2'
switch3 = 's3'
testerip_sta1 = sta1_host
testerip_sta2 = sta2_host
testerp1_sta1 = '1'
testerp1_sta2 = '1'
testerip_wired = pc1_host
testerp1_wired = '1'
testerp1_wired_port = 11918
PortType_wlan = '0'
PortType_moni = '1'