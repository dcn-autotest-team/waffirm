#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# Software : PyCharm
#
# __init__.py - 
#
# Author    :yanwh(yanwh@digitalchina.com)
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd 
#
#
# *********************************************************************
# Change log:
#       - 2018/4/1 9:19  add by yanwh
#
# *********************************************************************
import time
from waffirm_config_vars import *
from dcntestlibrary.dcnlibrary.BasicConfiguration import *

# CreateNewConn(ap1_type, ap1, ap1_host, None, 'run', logprefix='test')
# CreateNewConn('TelnetCCM', 's1', '172.17.100.243:10001', None, 'run', logprefix='test')

def run():
    CreateNewConn('Telnet', 'sta1', '172.17.100.167', None, 'run', logprefix='test')
    time.sleep(0.1)
    TelnetLogin('sta1', 'root', '123456')
    # SetCmd('sta1', 'cat /var/log/messages')
def run1():
    CreateNewConn('TelnetCCM', 's1', '172.17.100.243:10001', None, 'run', logprefix='test')
    EnterEnableMode('s1')
    SetTerminalLength('s1')
    for x in xrange(20):
        SetCmd('s1', 'show run', promoteStop=False)

# run()
run1()

if __name__ == '__main__':
    run()