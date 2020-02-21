#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# Software : PyCharm
#
# waffirmdevice.py - 
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
#       - 2018/3/31 9:46  add by yanwh
#
# *********************************************************************
from AffirmWireless.utils.dcnlogs.dcnuserlog import DcnLog
from AffirmWireless.log import LOGGERLIST

class DcnDevice(object):
    def __init__(self, name, link_method, host, port=None):
        self.name = name
        self.link_method = link_method
        self.host = host
        self.port = port

    def create_running_log(self, logprefix, testname):
        _hl = str(self.host).split(':')
        if len(_hl) > 1:
            self.port = _hl[1]
        return DcnLog(log_define_type='run', page_name=self.host, title_name=self.name, prefix_log_name=logprefix,
                      test_name=testname).create_log(LOGGERLIST)

    def create_default_log(self):
        pass
