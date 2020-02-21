#-*- coding: UTF-8 -*-#
#*******************************************************************************
# module_config_run.py
#
# Author:  ()
#
# Version 1.0.0
#
# Copyright (c) 2004-2008 Digital China Networks Co. Ltd
#
# Features: 控制测试例运行
#
#*******************************************************************************
# Change log:
#     - 2017.12.7 created by zhangjxp
#*******************************************************************************

testName = 'module'
priority = 10
runtimes = 1

central24G = False  #是否执行集中转发2.4G
central5G = False #是否执行集中转发5G
local24G = False  #是否执行本地转发2.4G
local5G = True #是否执行本地转发5G

# 下列参数用于判断脚本执行顺序，优先级小的先执行，如对执行顺序无特别要求则不需修改
central24G_pri = 3 #集中转发2.4G优先级
central5G_pri = 4 #集中转发5G优先级
local24G_pri = 1 #本地转发2.4G优先级
local5G_pri = 2 #本地转发5G优先级

module_list = [
'externalportal',
'internalportal',
'apwds',
'802.11I'
]

