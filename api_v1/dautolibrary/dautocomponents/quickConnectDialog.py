#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# quickConnectDialog.py - 快速链接(历史连接)窗口
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


class QuickConnectDialog(wx.Dialog):
    def __init__(self, parent, title, data_list):
        """
        快速连接窗口（文件-快速连接)
        :param parent: parent frame
        :param title:快速连接
        :param data_list: data list
        """
        wx.Dialog.__init__(self, parent, -1, title, size=(300, 350), style=wx.DEFAULT_DIALOG_STYLE)
        self.connectlist = []
        self.deletelist = []
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.connlist = []
        box = wx.BoxSizer(wx.HORIZONTAL)
        checkbox = wx.CheckBox(self, -1, '')
        box.Add(checkbox, 0, wx.ALIGN_CENTRE | wx.ALL, 1)
        label = wx.StaticText(self, -1, 'Type:', size=(70, -1))
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 1)
        text = wx.StaticText(self, -1, 'Title:', size=(50, -1))
        box.Add(text, 0, wx.ALIGN_CENTRE | wx.ALL, 1)
        text = wx.StaticText(self, -1, 'Host:', size=(120, -1))
        box.Add(text, 0, wx.ALIGN_CENTRE | wx.ALL, 1)
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        
        for config_line in data_list:
            box = wx.BoxSizer(wx.HORIZONTAL)
            if 'phoenix' in wx.version():
                checkbox = wx.CheckBox(self, 200 + int(config_line[3]) * 5, '', name='channel' + config_line[3])
                checkbox.SetToolTip(config_line[4])
                box.Add(checkbox, 0, wx.ALIGN_CENTRE | wx.ALL, 1)
                self.Bind(wx.EVT_CHECKBOX, self.evtCheckBox, checkbox)
                
                label = wx.StaticText(self, 201 + int(config_line[3]) * 5, config_line[0], size=(70, -1))
                label.SetToolTip(config_line[4])
                box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 1)
                
                text = wx.TextCtrl(self, 202 + int(config_line[3]) * 5, config_line[1], size=(50, -1),
                                   style=wx.TE_READONLY)
                text.SetToolTip(config_line[4])
                box.Add(text, 0, wx.ALIGN_CENTRE | wx.ALL, 1)
                
                text = wx.TextCtrl(self, 203 + int(config_line[3]) * 5, config_line[2], size=(120, -1),
                                   style=wx.TE_READONLY)
                text.SetToolTip(config_line[4])
                box.Add(text, 0, wx.ALIGN_CENTRE | wx.ALL, 1)
                
                bmp = wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK, wx.ART_BUTTON, (10, 10))
                bmpbutton = wx.BitmapButton(self, 204 + int(config_line[3]) * 5, bmp)
                bmpbutton.SetToolTip("Click to delete!")
            else:
                checkbox = wx.CheckBox(self, 200 + int(config_line[3]) * 5, '', name='channel' + config_line[3])
                checkbox.SetToolTipString(config_line[4])
                box.Add(checkbox, 0, wx.ALIGN_CENTRE | wx.ALL, 1)
                self.Bind(wx.EVT_CHECKBOX, self.evtCheckBox, checkbox)
                
                label = wx.StaticText(self, 201 + int(config_line[3]) * 5, config_line[0], size=(70, -1))
                label.SetToolTipString(config_line[4])
                box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 1)
                
                text = wx.TextCtrl(self, 202 + int(config_line[3]) * 5, config_line[1], size=(50, -1),
                                   style=wx.TE_READONLY)
                text.SetToolTipString(config_line[4])
                box.Add(text, 0, wx.ALIGN_CENTRE | wx.ALL, 1)
                
                text = wx.TextCtrl(self, 203 + int(config_line[3]) * 5, config_line[2], size=(120, -1),
                                   style=wx.TE_READONLY)
                text.SetToolTipString(config_line[4])
                box.Add(text, 0, wx.ALIGN_CENTRE | wx.ALL, 1)
                
                bmp = wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK, wx.ART_BUTTON, (10, 10))
                bmpbutton = wx.BitmapButton(self, 204 + int(config_line[3]) * 5, bmp)
                bmpbutton.SetToolTipString("Click to delete!")
            box.Add(bmpbutton, 0, wx.ALIGN_CENTRE | wx.ALL, 1)
            self.Bind(wx.EVT_BUTTON, self.evtImgButton, bmpbutton)
            
            sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.TOP, 5)
        
        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        
        sizer.Add(btnsizer, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        
        self.SetSizer(sizer)
        sizer.Fit(self)
    
    def evtCheckBox(self, evt):
        """
        Check Box
        :param evt: Check Box 事件
        :return: None
        """
        startid = evt.GetId()
        conn_title_window = self.FindWindowById(startid + 2)
        conn_type = self.FindWindowById(startid + 1).Label
        conn_title = conn_title_window.Value
        conn_host = self.FindWindowById(startid + 3).Value
        conn_path = conn_title_window.GetToolTip().GetTip()
        if evt.IsChecked():
            self.connectlist.append([conn_type, conn_title, conn_host, conn_path])
        else:
            try:
                self.connectlist.remove([conn_type, conn_title, conn_host, conn_path])
            except ValueError as e:
                print('[evtCheckBox]', e)
    
    def evtImgButton(self, evt):
        """
        Img Button
        :param evt: Img Button 事件
        :return: None
        """
        button_id = evt.GetId()
        node_id = (button_id - 204) / 5
        for i in range(1, 5):
            tb = self.FindWindowById(button_id - i)
            tb.Enable(not tb.Enabled)
        if tb.Enabled:
            self.deletelist.remove(node_id)
        else:
            self.deletelist.append(node_id)
