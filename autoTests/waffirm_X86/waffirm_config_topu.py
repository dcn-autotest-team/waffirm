#-*- coding: UTF-8 -*-#
#*******************************************************************************
# bootrom_topu.py
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2008 Digital China Networks Co. Ltd
#
# Features:  ��ű�����Ϣ
#
#*******************************************************************************
# Change log:
#     - 
#*******************************************************************************

EnvNo = '4'
set_default = 1
upgrade_device = 0

pc1 = 'pc1'
sta1 = 'sta1'
sta2 = 'sta2'
ap1 = 'ap1'
ap2 = 'ap2'
switch1 = 's1'
switch2 = 's2'
switch3 = 's3'

#��������
pc1_type = 'Telnet'
pc1_host = '172.17.100.193'
sta1_type = 'Telnet'

sta1_host = '172.17.100.194'
sta2_type = 'Telnet'
sta2_host = '172.17.100.195'
switch1_type = 'Telnet'
switch1_host = '172.17.100.196'
switch2_type = 'Telnet'
switch2_host = '172.17.100.197'
switch3_type = 'TelnetCCM'
switch3_host = '172.17.100.242:10006'
ap1_type = 'TelnetCCM'
ap1_host = '172.17.100.242:10007'
ap2_type = 'TelnetCCM'
ap2_host = '172.17.100.242:10008'

testerip_sta1 = sta1_host
testerip_sta2 = sta2_host
testerp1_sta1 = '1'
testerp1_sta2 = '1'

testerip_wired = pc1_host
testerp1_wired = '1'

#�豸�˿ڶ���
s1p1 = 'Ethernet'
s2p1 = 'Ethernet'
#S3����AC1
s3p1 = 'Ethernet1/1'
#S3����AC2
s3p2 = 'Ethernet1/3'
#S3����AP1
s3p3 = 'Ethernet1/5'
#S3����AP2
s3p4 = 'Ethernet1/7'
#���� pc1 192.168.10����
s3p5 = 'Ethernet1/15'
#����80
s3p6 = 'Ethernet1/17'
#����apģ���� ��ʱû�õ�
s3p7 = 'Ethernet1/11'