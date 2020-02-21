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
#       - 2018/4/13 12:51  add by yanwh
#
# *********************************************************************

import os
from pathlib import Path

__all__ = ['cc_path', 'dc_path', 'lc_path', 'sc_path']
# cc_path = os.path.join(os.path.dirname(__file__), 'channelConfig.xml')
cc_path = (Path(os.path.dirname(__file__)) / 'channelConfig.xml').as_posix()
# dc_path = os.path.join(os.path.dirname(__file__), 'debugConfig.xml')
dc_path = (Path(os.path.dirname(__file__)) / 'debugConfig.xml').as_posix()
# lc_path = os.path.join(os.path.dirname(__file__), 'logConfig.xml')
lc_path = (Path(os.path.dirname(__file__)) / 'logConfig.xml').as_posix()
# sc_path = os.path.join(os.path.dirname(__file__), 'styleConfig.xml')
sc_path = (Path(os.path.dirname(__file__)) / 'styleConfig.xml').as_posix()
del os
