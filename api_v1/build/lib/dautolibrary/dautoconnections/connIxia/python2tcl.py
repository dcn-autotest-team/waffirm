#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# python2tcl.py - python调用tcl
# 
# Author:caisy(caisy@digitalchina.com)
#
# Version 2.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd 
#
# 
# *********************************************************************
# Change log:
#     - 2011.8.31  modified by caisy
#
# *********************************************************************
import os
import threading

import wx
from dautolibrary.dautocomponents.dstyle import LoadReceiverDebugConfig

path = os.path.dirname(__file__)


def StartTclServer():
    ixia_server = os.path.join(path, 'ixiaServer.tcl')
    os.system('tclsh ' + ixia_server + ' 9927')


def IxiaProc(command, flag=1):
    debug = LoadReceiverDebugConfig()
    if debug and (command.find('InitIxia') < 0) and (command.find('SaveIxiaPortConfig') < 0):
        Pause()
    res = 0
    if flag == 0:
        os.system('tclsh ' + command)
    elif flag == 1:
        ixia_client = os.path.join(path, 'ixiaServer.tcl')
        res = os.popen('tclsh ' + ixia_client + ' ' + command).read()
        res = res.rstrip()
    return res


def StartTclServerTh():
    th = threading.Thread(target=StartTclServer, args=())
    th.start()


def Pause():
    window = wx.FindWindowByName('Main')
    window.PauseTestAuto()
