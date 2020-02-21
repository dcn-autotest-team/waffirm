#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# messageBox.py - 弹出窗口
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

import wx


def Alert(parent, msg, *arg):
    """
    Alert窗口
    :param parent: parent frame
    :param msg: 输入需要弹窗的内容信息
    :param arg: 额外指定参数
    :return: None
    """
    msgbox = wx.MessageDialog(parent, msg, 'DCN messageBox:', wx.OK | wx.ICON_INFORMATION)
    msgbox.ShowModal()
    msgbox.Destroy()
