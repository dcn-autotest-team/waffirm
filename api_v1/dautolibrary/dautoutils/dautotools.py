#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# Software : PyCharm
#
# dautotools.py -
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
#       - 2018/2/26 15:27  add by yanwh
#
# *********************************************************************


import sys
import traceback

import wx
from wx import CallAfter

__all__ = ['call_after']


def call_after(func):
    """
    call after装饰器
    :param func: 被调用函数
    :return:
    """
    
    def _wrapper(*args, **kwargs):
        return CallAfter(func, *args, **kwargs)
    
    return _wrapper


def dauto_catch_error():
    """Dauto平台报错的异常捕获，调试的时候通过python命令行的方式启动Dauto平台，捕获到异常之后会弹窗显示"""
    message = ''.join(traceback.format_exception(*sys.exc_info()))
    dialog = wx.MessageDialog(None, message, 'Error!', wx.OK | wx.ICON_ERROR)
    dialog.ShowModal()
