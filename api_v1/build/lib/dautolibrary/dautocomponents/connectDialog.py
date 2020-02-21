# -*- coding: UTF-8 -*-
# *********************************************************************
# connectDialog.py - 新建连接-对话框
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

import wx

from .messageBox import Alert

wildcard = "Python source (*.log)|*.log|" \
           "All files (*.*)|*.*"


class TestDialog(wx.Dialog):
    """
    供parentframe模块中的ConfigNewChannel函数使用
    Dauto平台-文件-连接窗口（快捷键Ctrl+N)
    type:目前支持Telnet TelnetCCM  Serial
    title:设备名称例如s1 s2
    host:设备连接ip地址端口号 例如172.17.100.14：10007
    说明：手动打开窗口之后会让选择日志存放路径
    """
    
    def __init__(self, parent, id, title):
        """
        初始化Dialog实例
        :param parent: 父窗口ParentFrame
        :param id: 窗口唯一标识
        :param title: 对话框名称默认为Create a connection
        """
        
        wx.Dialog.__init__(self, parent, id, title, size=(500, 350), style=wx.DEFAULT_DIALOG_STYLE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        label = wx.StaticText(self, 70, "Create a connection:")
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        # --------------------------------------------------------------------
        box = wx.BoxSizer(wx.HORIZONTAL)
        
        label = wx.StaticText(self, 71, "Type:", size=(30, -1))
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        choice = wx.Choice(self, 72, (150, -1), choices=['Telnet', 'TelnetCCM', 'Serial'])
        
        self.Bind(wx.EVT_CHOICE, self.choice_change, choice)
        
        box.Add(choice, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        sizer.Add(box, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        # --------------------------------------------------------------------
        box = wx.BoxSizer(wx.HORIZONTAL)
        
        label = wx.StaticText(self, 73, "Title: ", size=(30, -1))
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        text = wx.TextCtrl(self, 74, "", size=(150, -1))
        box.Add(text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        sizer.Add(box, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        # --------------------------------------------------------------------
        box = wx.BoxSizer(wx.HORIZONTAL)
        
        label = wx.StaticText(self, 75, "Host: ", size=(30, -1))
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        text = wx.TextCtrl(self, 76, "", size=(150, -1))
        box.Add(text, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        label = wx.StaticText(self, 78, "Port: ")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        text = wx.TextCtrl(self, 79, "", size=(50, -1))
        box.Add(text, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        # --------------------------------------------------------------------
        box = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, 80, "Baud Rate :", size=(70, -1))
        box.Add(label, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        baudrate_choice = wx.Choice(self, 88, (50, -1),
                                    choices=['110', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200',
                                             '38400', '57600',
                                             '115200', '230400', '380200', '460800', '921600'])
        baudrate_choice.SetSelection(6)
        box.Add(baudrate_choice, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        
        sizer.Add(box, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 5)
        btnsizer = wx.StdDialogButtonSizer()
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btn.Disable = True
        
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        
        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        self.SetSizer(sizer)
        sizer.Fit(self)
    
    def save(self):
        """
        弹出选择日志路径的对话框，日志类型默认log
        :return: 返回用户选择的日志路径
        """
        save_dir = sys.path[0]
        if os.path.isfile(save_dir):
            save_dir = os.path.split(save_dir)[0]
        dlg2 = wx.FileDialog(
            None, message="文件另存为 ...", defaultDir=save_dir,
            defaultFile="", wildcard=wildcard, style=wx.SAVE
        )
        if dlg2.ShowModal() == wx.ID_OK:
            try:
                path = dlg2.GetPath()
                Alert(self, '保存成功!')
                return path
            except BaseException as e:
                Alert(self, '[Failed:]' + str(e))
        
        dlg2.Destroy()
    
    def choice_change(self, evt):
        if wx.FindWindowById(72).GetSelection() == 1:
            wx.FindWindowById(88).Enable(False)
            wx.FindWindowById(79).Enable(True)
            wx.FindWindowById(76).Enable(True)
        elif wx.FindWindowById(72).GetSelection() == 2:
            wx.FindWindowById(88).Enable(True)
            wx.FindWindowById(79).Enable(True)
            wx.FindWindowById(76).Enable(False)
        elif wx.FindWindowById(72).GetSelection() == 0:
            wx.FindWindowById(88).Enable(False)
            wx.FindWindowById(79).Enable(False)
            wx.FindWindowById(76).Enable(True)
        else:
            wx.FindWindowById(88).Enable(False)
            wx.FindWindowById(79).Enable(True)
            wx.FindWindowById(76).Enable(True)
