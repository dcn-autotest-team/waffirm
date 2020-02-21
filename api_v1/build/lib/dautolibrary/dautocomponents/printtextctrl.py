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


# 调试窗口
# from wx import wx
import wx
from dautolibrary.dautoutils.dautotools import call_after


class PrintTextCtrl(wx.TextCtrl):
    """
    输出窗口，该窗口输出用户输入或者系统反馈回来指定信息
    """
    
    def __init__(self, parent):
        """
        PrintTextCtrl实例
        :param parent: parent frame
        """
        wx.TextCtrl.__init__(self, parent, 553, '', wx.Point(0, 0), wx.Size(150, 90),
                             wx.NO_BORDER | wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2, name='ConsoleTextCtrl')
        font = wx.Font(9, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL)
        self.SetFont(font)
        self.SetDefaultStyle(wx.TextAttr(wx.BLUE))
    
    @call_after
    def WriteToText(self, msg):
        """
         # 向text ctrl打印信息，控制信息长度（如大于30000，清除前面6000）
        :param msg: 要打印的信息
        :return: None
        """
        if self.GetLastPosition() >= 30000:
            self.Remove(0, 6000)
            self.SetInsertionPointEnd()  # add by yanwh 删除6000之后将position设置到当前Text的末尾
        if msg:
            self.AppendText(msg)
