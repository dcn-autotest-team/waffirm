#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# Software : PyCharm
#
# dcnprint.py - dcn打印模块
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
#       - 2018/3/28 15:34  add by yanwh
#
# *********************************************************************
# 打印到界面

import datetime
import time

try:
    from wx import wx
except ImportError:
    import wx

__all__ = ['printScr', 'printResInfo', 'printResInfo', 'printResError', 'printResWarn', 'printResDebug', 'printAll',
           'printStep', 'printRes', 'printFormat']


def printScr(sut, msg):
    """
    打印到屏幕
    :param sut: s1
    :param msg: msg
    :return: None
    """
    sut, msg = str(sut), str(msg)
    try:
        dev_window = wx.FindWindowByName(sut)
        if dev_window is None:
            printResWarn('[告警]无法找到sut对应的tab窗口', sut)
            return '[Error]:Can not find tab named', sut
        else:
            dev_window.WriteTextCtrl(msg + '\n')
    except (AttributeError, Exception) as e:
        printResError('[异常]打印到屏幕的时候遭遇异常，异常信息如下 {}'.format(e))


def printResInfo(msg):
    """
    打印到日志、调试窗口
    :param msg: msg
    :return: None
    """
    try:
        window = wx.FindWindowById(553)
        logger = wx.FindWindowById(10).logger
        msg = str(msg)
        if window and hasattr(window, 'WriteToText'):
            wx.CallAfter(window.WriteToText, msg + '\n')
        else:
            print(msg)
        if logger:
            for _msg in msg.split('\n'):
                logger.info(str(_msg, encoding='utf-8'))  # 此处是为了使得html日志回车换行
    except (AttributeError, Exception):
        print(msg)
    time.sleep(0.05)


printRes = printResInfo


def printResError(msg):
    """
    打印错误信息，如果有Dauto有logger（console log),则按照error级别记录log信息
    :param msg: msg
    :return: None
    """
    try:
        window = wx.FindWindowById(553)
        logger = wx.FindWindowById(10).logger
        msg = str(msg)
        if window and hasattr(window, 'WriteToText'):
            wx.CallAfter(window.WriteToText, msg + '\n')
        else:
            print(msg)
        if logger:
            for _msg in msg.split('\n'):
                logger.error(str(_msg, encoding='utf-8'))  # 此处是为了使得html日志回车换行
    except (AttributeError, Exception):
        print(msg)
    time.sleep(0.05)


def printResWarn(msg):
    """
    打印错误信息，如果有Dauto有logger（console log),则按照warning级别记录log信息
    :param msg: msg
    :return: None
    """
    try:
        window = wx.FindWindowById(553)
        logger = wx.FindWindowById(10).logger
        if window and hasattr(window, 'WriteToText'):
            wx.CallAfter(window.WriteToText, str(msg) + '\n')
        else:
            print(msg)
        if logger:
            for _msg in msg.split('\n'):
                logger.warning(str(_msg, encoding='utf-8'))  # 此处是为了使得html日志回车换行
    except (AttributeError, Exception):
        print(msg.encode('utf-8'))
    time.sleep(0.05)


def printResDebug(msg):
    """
    打印错误信息，如果有Dauto有logger（console log),则按照debug级别记录log信息
    :param msg: msg
    :return: None
    """
    try:
        window = wx.FindWindowById(553)
        logger = wx.FindWindowById(10).logger
        msg = str(msg)
        if window and hasattr(window, 'WriteToText'):
            wx.CallAfter(window.WriteToText, msg + '\n')
        else:
            print(msg)
        if logger:
            for _msg in msg.split('\n'):
                logger.debug(str(_msg, encoding='utf-8'))  # 此处是为了使得html日志回车换行
    except (AttributeError, Exception):
        print(msg)
    time.sleep(0.05)


def printAll(msg):
    """
    打印到界面、日志、调试窗口
    :param msg: msg
    :return: None
    """
    try:
        main_window = wx.FindWindowByName('Main')
        wx.CallAfter(main_window.PrintLogInfoAuto, msg)
    except (AttributeError, Exception) as e:
        printResError('[异常]打印到日志调试窗口和屏幕的时候遭遇异常，异常信息如下 {}'.format(e))


def printFormat(*msg):
    """
    格式化打印输出，打印形如如下信息
    ############################
    # msg info
    ############################
    :param msg:
    :return:
    """
    info = '\n' + '#' * 80
    line = '\n# '
    for j in msg:
        line += j
        info += line
        line = '\n# '
    info += '\n' + '#' * 80
    return info


def printStep(*msg):
    """
    打印格式化提示信息，到所有窗口和日志
    :param msg: msg
    :return: None
    """
    res = printFormat(*msg)
    printAll(res)
    time.sleep(0.5)


def printDebug(msg):
    """
    打印dauto系统调试信息
    :param msg: msg
    :return: None
    """
    if 1 == 2:
        this_time = datetime.datetime.now()
        print(str(this_time) + str(msg))
