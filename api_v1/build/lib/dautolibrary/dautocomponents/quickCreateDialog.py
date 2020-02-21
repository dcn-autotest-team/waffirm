#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# quickCreateDialog.py - 重复脚本快速生成-对话框
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
import sys

from .messageBox import Alert
from .quickCreatePy import *


class QuickCreateDialog(wx.Dialog):
    """
    快速创建窗口
    """
    
    def __init__(self, parent, ID, title):
        
        self.main = wx.FindWindowByName('Main')
        wx.Dialog.__init__(self, self.main, ID, title, size=(824, 450), style=wx.DEFAULT_DIALOG_STYLE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # --------------------------------------------------------------------
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, 300, "Repeat Times:", size=(100, 20))
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        self.win1 = wx.TextCtrl(self, 301, "", size=(50, 20))
        box.Add(self.win1, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        label = wx.StaticText(self, 302, "             Sut title:", size=(100, 20))
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        self.win2 = wx.TextCtrl(self, 303, "", size=(50, 20))
        box.Add(self.win2, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        
        # --------------------------------------------------------------------
        box = wx.BoxSizer(wx.HORIZONTAL)
        self.win3 = wx.TextCtrl(self, 305, "", style=wx.TE_MULTILINE, size=(400, 500))
        box.Add(self.win3, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        self.win = wx.TextCtrl(self, 306, "", style=wx.TE_MULTILINE | wx.TE_DONTWRAP, size=(400, 500))
        box.Add(self.win, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 5)
        
        box = wx.BoxSizer(wx.HORIZONTAL)
        button = wx.Button(self, -1, 'Create')
        self.Bind(wx.EVT_BUTTON, self.create, button)
        box.Add(button, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        button = wx.Button(self, -1, 'Save')
        self.Bind(wx.EVT_BUTTON, self.save, button)
        box.Add(button, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        btnsizer = wx.StdDialogButtonSizer()
        
        btn = wx.Button(self, wx.ID_OK, 'Close')
        btnsizer.AddButton(btn)
        
        btnsizer.Realize()
        box.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        sizer.Add(box, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        
        self.SetSizer(sizer)
        sizer.Fit(self)
    
    def create(self, evt):
        
        self.Refresh()
        win1 = self.win1
        win2 = self.win2
        win3 = self.win3
        try:
            repeat_times = int(win1.GetValue())
        except ValueError as e:
            msg = wx.MessageDialog(self, '[Repeat times:]Please input a int type!',
                                   'Warning!',
                                   wx.OK | wx.ICON_INFORMATION)
            msg.ShowModal()
            msg.Destroy()
            return -1
        sut = win2.GetValue()
        data = win3.GetValue()
        res = createPy(sut, repeat_times, data)
        # print '------------'
        # print res
        self.win.WriteText(res)
    
    def save(self, evt):
        save_dir = sys.path[0]
        if os.path.isfile(save_dir):
            save_dir = os.path.split(save_dir)[0]
        dlg2 = wx.FileDialog(
            None, message="Save file as ...", defaultDir=save_dir,
            defaultFile="", wildcard=wildcard, style=wx.SAVE
        )
        if dlg2.ShowModal() == wx.ID_OK:
            try:
                path = dlg2.GetPath()
                text = self.win.GetValue()
                fileBuffer = open(path, "w")
                fileBuffer.writelines(text)
                fileBuffer.close()
                Alert(self, 'Save done!')
            except BaseException as e:
                Alert(self, '[Failed:]' + str(e))
        
        dlg2.Destroy()
