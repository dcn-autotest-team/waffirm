#-*- coding: UTF-8 -*-#
#*******************************************************************************
# waffirm_run.py
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
#     - 
#*******************************************************************************

testName = 'waffirm'
priority = 10
runtimes = 1
testlist = []

fitap = True

if fitap == True:
    testlist.append(['waffirm_4.1.2.py',1])
    testlist.append(['waffirm_4.1.4.py',1])
    testlist.append(['waffirm_4.1.6.py',1])
    testlist.append(['waffirm_4.1.7.py',1])
    testlist.append(['waffirm_4.2.1.py',1])
    testlist.append(['waffirm_4.2.2.py',1])
    testlist.append(['waffirm_4.3.1.py',1])
    testlist.append(['waffirm_4.3.2.py',1])
    testlist.append(['waffirm_4.3.3.py',1])
    testlist.append(['waffirm_4.3.4.py',1])
    testlist.append(['waffirm_4.3.5.py',1])
    testlist.append(['waffirm_4.3.6.py',1])
    testlist.append(['waffirm_4.3.7.py',1])
    testlist.append(['waffirm_4.3.9.py',1])
    testlist.append(['waffirm_4.4.2.py',1])
    testlist.append(['waffirm_4.4.3.py',1])
    testlist.append(['waffirm_4.4.4.py',1])
    testlist.append(['waffirm_4.4.5.py',1])
    testlist.append(['waffirm_4.4.6.py',1])#已知问题
    testlist.append(['waffirm_4.4.7.py',1])# step fail 需定位
    testlist.append(['waffirm_4.5.2.py',1])
    testlist.append(['waffirm_4.5.3.py',1])
    testlist.append(['waffirm_4.5.4.py',1])
    testlist.append(['waffirm_4.5.6.py',1])
    testlist.append(['waffirm_4.6.3.py',1]) 
    testlist.append(['waffirm_4.6.4.py',1])
    testlist.append(['waffirm_4.6.5.py',1])
    testlist.append(['waffirm_4.7.py',1])
    testlist.append(['waffirm_4.11.1.py',1])
    testlist.append(['waffirm_4.11.2.py',1])
    testlist.append(['waffirm_4.11.3.py',1])
    testlist.append(['waffirm_4.13.py',1])#step6 7主备切换不成功
    testlist.append(['waffirm_4.14.1.py',1])
    testlist.append(['waffirm_4.14.2.py',1])
    testlist.append(['waffirm_4.14.3.py',1])
    testlist.append(['waffirm_4.14.4.py',1])
    testlist.append(['waffirm_4.15.1.py',1])
    testlist.append(['waffirm_4.15.2.py',1])
    testlist.append(['waffirm_4.20.py',1])
    testlist.append(['waffirm_5.2.py',1])
    testlist.append(['waffirm_5.7.py',1])