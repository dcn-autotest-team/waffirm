# -*- coding: UTF-8 -*-#
# *******************************************************************************
# waffirm_vars.py - variables defination for waffirm test script
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2008 Digital China Networks Co. Ltd
#
# Features: 存放变量信息
#
# 2012-12-4 10:23:59
#
# *******************************************************************************
# Change log:
#     - modified by zhangjxp 新增升级脚本5.3，添加参数If_vlan1_s3_ipv4，修改参数updateserver
#     - modified by yanwh 增加from waffirm_config_topu import *
#     - modified by yanwh 增加库函数导入，支持后面的函数运行
# *******************************************************************************

import re

Vlan1 = '1'

pc1_ipv4 = '192.168.10.'+EnvNo+'2'
Radius_server = '192.168.10.101'
Radius_server_windows = '192.168.10.104'

Netcard_sta1 = 'wls224'
Netcard_sta2 = 'wls224'
Netcard_pc = 'wls224'

Dhcp_pool1 = '192.168.'+EnvNo+'1.'

Ap1_ipv4 = '100.1.1.1'+EnvNo+'1'
Ap2_ipv4 = '100.1.1.1'+EnvNo+'2'

StaticIpv4_ac1 = '100.1.1.1'+EnvNo+'3'
StaticIpv4_ac2 = '100.1.1.1'+EnvNo+'4'

upgradeserver_ftp_username = 'upload'
upgradeserver_ftp_pwd = 'upload'

if 'bj' in Network_name1:
    updateserver = '100.1.1.1'
elif 'wh' in Network_name1:
    updateserver = '100.1.1.2'
elif 'sh' in Network_name1:
    updateserver = '100.1.1.3'
else:
    pass


# 确定AP版本号
ap1_current_buildnum = get_apversion_from_imagename(ap1_current_build)
ap1_standby_buildnum = get_apversion_from_imagename(ap1_standby_build)
ap2_current_buildnum = get_apversion_from_imagename(ap2_current_build)
ap2_standby_buildnum = get_apversion_from_imagename(ap2_standby_build)        

# AP升级路径
ap1_ftpupgrade_current_path = 'ftp://%s:%s@%s/%s' % (upgradeserver_ftp_username, upgradeserver_ftp_pwd, updateserver, ap1_current_build)
ap1_ftpupgrade_standby_path = 'ftp://%s:%s@%s/%s' % (upgradeserver_ftp_username, upgradeserver_ftp_pwd, updateserver, ap1_standby_build)
ap2_ftpupgrade_current_path = 'ftp://%s:%s@%s/%s' % (upgradeserver_ftp_username, upgradeserver_ftp_pwd, updateserver, ap2_current_build)
ap2_ftpupgrade_standby_path = 'ftp://%s:%s@%s/%s' % (upgradeserver_ftp_username, upgradeserver_ftp_pwd, updateserver, ap2_standby_build)
wrong_imagetype_ftpupgrade_path = 'ftp://%s:%s@%s/%s' % (upgradeserver_ftp_username, upgradeserver_ftp_pwd, updateserver, wrong_image_file)
ap1_ftpupgrade_current_path_6222 = 'flash:/%s' % (ap1_current_build)
ap1_ftpupgrade_standby_path_6222 = 'flash:/%s' % (ap1_standby_build)
ap2_ftpupgrade_current_path_6222 = 'flash:/%s' % (ap2_current_build)
ap2_ftpupgrade_standby_path_6222 = 'flash:/%s' % (ap2_standby_build)
ap1_tftpupgrade_current_path = 'tftp://%s/%s' % (updateserver, ap1_current_build)
ap1_tftpupgrade_standby_path = 'tftp://%s/%s' % (updateserver, ap1_standby_build)
# AP的image type
ap1_image_type = get_ap_image_type(switch1,hwtype1)
ap2_image_type = get_ap_image_type(switch1,hwtype2)


Vlan_Idle_time = 3
ftp_ap_upgrade_time = 300
tftp_ap_upgrade_time = 400
ap_reset_time = 80