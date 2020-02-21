#-*- coding: UTF-8 -*-#
#
#*******************************************************************************
# apconfiguration_2.2.2.6_ONE.py
#
# Author: zhangjxp
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
# Features: 
# 2.2.2.6	管理Ac可以按Ap组(Ip)触发升级
# 测试目的： 管理AC上可以wireless ap download start ap-group <word>触发手动独立升级此ap-group(以ip地址段分组)的所有ap，
#            ap重启后被AC管理，image版本已经更新成功。
#*******************************************************************************
# Change log:
#     - created by zhangjxp 2018.3.29
#*******************************************************************************

#Package

#Global Definition

#Source files

#Procedure Definition 

#Functional Code

testname = 'apconfiguration_2.2.2.6'
avoiderror(testname)
printTimer(testname,'Start','ac upgrade ap-group(classfied by ip)')

###############################################################################
#Step 1
#操作
# 在AC1上为AP1_image_type指定image文件为ap1_standby_build，
# 在AC1上为AP2_image_type指定image文件为ap2_standby_build，
# 将AP1和AP2的IP地址加入ap-group 111中，升级ap-group 111
# 预期
# AP1和AP2升级成功
################################################################################
printStep(testname,'Step 1',
          'config ap1_image_type upgrade to ap1_standby_build',
          'config ap2_image_type upgrade to ap2_standby_build',
          'add ap1_ip and ap2_ip to group 111',
          'upgrade group 111'
          'ap1 and ap2 upgrade successfully')

#operate
# 在AC1上为AP1和AP2指定image文件
# (脚本中先配置AP2再配置AP1，目的是如果AP2和AP1的image type相同时，AP2的配置会被AP1覆盖）
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap2_image_type, ap2_ftpupgrade_standby_path)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, ap1_ftpupgrade_standby_path)

# 创建group 111,将AP1和AP2的IP地址加入group 111
EnterWirelessMode(switch1)
SetCmd(switch1,'ap-group 111')
SetCmd(switch1,'permit-ap-network', Ap1_ipv4, '255.255.255.0')
SetCmd(switch1,'permit-ap-network', Ap2_ipv4, '255.255.255.0')

# 重启AP1和AP2
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap reset', promotePatten='Y/N', promoteTimeout=5)
SetCmd(switch1,'y')
IdleAfter(120)
# 等待AP认证上线
CheckSutCmd(switch1,'show wireless ap status', 
            check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
            retry=30,interval=5,waitflag=False,IC=True)
            
# 检查AP1和AP2是否加入ap grou111中
res1=CheckSutCmd(switch1,'show wireless ap-group 111', 
                 check=[(ap1mac),(ap2mac)],
                 retry=20,interval=5,waitflag=False,IC=True)
                 
# 升级group 111组内所有AP
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap download start ap-group 111')

# 等待升级完成
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)

# check
# 检查AC1是否重新管理AP1和AP2
res2=CheckSutCmd(switch1,'show wireless ap status', 
                 check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                 retry=20,interval=5,waitflag=False,IC=True)
                 
# 检查AP1和Ap2升级成功
ApLogin(ap1)
ApLogin(ap2) 
res3 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_standby_buildnum)
if ap1_image_type != ap2_image_type:
    res4 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_standby_buildnum)
else:
    res4 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap1_standby_buildnum)
#result
printCheckStep(testname, 'Step 1',res1,res2,res3,res4)
###############################################################################
#Step 2
#操作
# 在AC1上为AP1_image_type指定image文件为ap1_current_build，
# 在AC1上为AP2_image_type指定image文件为ap2_current_build，
# 升级ap-group 111
# 预期
# AP1和AP2升级成功
################################################################################
printStep(testname,'Step 2',
          'config ap1_image_type upgrade to ap1_standby_build',
          'config ap2_image_type upgrade to ap2_standby_build',
          'upgrade group 111'
          'ap1 and ap2 upgrade successfully')

#operate
EnterWirelessMode(switch1)
SetCmd(switch1, 'wireless ap download image-type',ap2_image_type, ap2_ftpupgrade_current_path)
SetCmd(switch1, 'wireless ap download image-type',ap1_image_type, ap1_ftpupgrade_current_path)

# 升级group 111组内所有AP
EnterEnableMode(switch1)
SetCmd(switch1,'wireless ap download start ap-group 111')

# 等待升级完成
IdleAfter(ftp_ap_upgrade_time)
ac_wait_download_finish(switch1)

# check
res1 = CheckSutCmd(switch1,'show wireless ap status', 
                   check=[(ap1mac,'Managed','Success'),(ap2mac,'Managed','Success')],
                   retry=20,interval=5,waitflag=False,IC=True)
                   
# 检查AP1和Ap2升级成功
ApLogin(ap1)
ApLogin(ap2) 
res2 = check_apversion_after_upgrade(ap1, Ap1cmdtype, ap1_current_buildnum)
if ap1_image_type != ap2_image_type:
    res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap2_current_buildnum)
else:
    res3 = check_apversion_after_upgrade(ap2, Ap2cmdtype, ap1_current_buildnum)
    
#result
printCheckStep(testname, 'Step 2',res1,res2,res3)
################################################################################
# Step 3
# 操作
# 恢复默认配置
################################################################################
printStep(testname, 'Step 3',
          'Recover initial config')
          
EnterWirelessMode(switch1)
SetCmd(switch1, 'no ap-group 111')
SetCmd(switch1, 'no wireless ap download image-type',ap1_image_type)
SetCmd(switch1, 'no wireless ap download image-type',ap2_image_type)
#end
printTimer(testname, 'End')