#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# createIxiaScriptDialog.py - python调用ixia脚本辅助生成界面
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
import time

# from wx import wx
import wx

from .python2tcl import IxiaProc, StartTclServerTh

__all__ = ['ConnIxiaFrame']

wildcard = "Tcl source (*.tcl)|*.tcl|" \
           "All files (*.*)|*.*"


class ConnIxiaFrame(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, None, -1, "Editor", size=(925, 600))
        pl = ConnIxiaPanel(self)


class ConnIxiaPanel(wx.ScrolledWindow):
    def __init__(self, parent, id=-1, size=wx.DefaultSize):
        wx.ScrolledWindow.__init__(self, parent, id, (0, 0), size=size, style=wx.SUNKEN_BORDER)
        self.SetScrollRate(20, 20)
        self.SetBackgroundColour(wx.WHITE)
        self.portlist = []
        self.portlistitem = []
        self.chassisid = 1
        self.portinfo = ''
        self.hostip = ''
        # 最外层
        sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        cardList = ['']
        portList = ['']
        for i in range(1, 21):
            if i < 9:
                portList.append(str(i))
            cardList.append(str(i))
        
        # 第一组
        box = wx.StaticBox(self, -1, "Port select:")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        sizer.Add(bsizer, 0, wx.ALL, 5)
        
        # Host IP
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Host IP:")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        text = wx.TextCtrl(self, 72, "", size=(100, -1), name='hostip')
        sizer1.Add(text, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        
        # ChassisID
        label = wx.StaticText(self, -1, "ChassisID:")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        choice = wx.Choice(self, -1, name='chassisid', choices=cardList, size=(50, -1))
        sizer1.Add(choice, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        bsizer.Add(sizer1, 1)
        
        # Testerp1
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "[Testerp1:]")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        label = wx.StaticText(self, -1, "Card:")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 1)
        choice = wx.Choice(self, -1, name='card1', choices=cardList, size=(50, -1))
        sizer1.Add(choice, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        label = wx.StaticText(self, -1, "Port:")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 1)
        choice = wx.Choice(self, -1, name='port1', choices=portList, size=(50, -1))
        sizer1.Add(choice, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        bsizer.Add(sizer1, 1, flag=wx.EXPAND)
        
        # Testerp2
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "[Testerp2:]")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        label = wx.StaticText(self, -1, "Card:")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 1)
        choice = wx.Choice(self, -1, name='card2', choices=cardList, size=(50, -1))
        sizer1.Add(choice, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        label = wx.StaticText(self, -1, "Port:")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 1)
        choice = wx.Choice(self, -1, name='port2', choices=portList, size=(50, -1))
        sizer1.Add(choice, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        bsizer.Add(sizer1, 1, flag=wx.EXPAND)
        
        # Testerp3
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "[Testerp3:]")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        label = wx.StaticText(self, -1, "Card:")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 1)
        choice = wx.Choice(self, -1, name='card3', choices=cardList, size=(50, -1))
        sizer1.Add(choice, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        label = wx.StaticText(self, -1, "Port:")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 1)
        choice = wx.Choice(self, -1, name='port3', choices=portList, size=(50, -1))
        sizer1.Add(choice, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        bsizer.Add(sizer1, 1, flag=wx.EXPAND)
        
        # Testerp4
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "[Testerp4:]")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        label = wx.StaticText(self, -1, "Card:")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 1)
        choice = wx.Choice(self, -1, name='card4', choices=cardList, size=(50, -1))
        sizer1.Add(choice, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        label = wx.StaticText(self, -1, "Port:")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 1)
        choice = wx.Choice(self, -1, name='port4', choices=portList, size=(50, -1))
        sizer1.Add(choice, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        bsizer.Add(sizer1, 1, flag=wx.EXPAND)
        
        # Testerp5
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "[Testerp5:]")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        label = wx.StaticText(self, -1, "Card:")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 1)
        choice = wx.Choice(self, -1, name='card5', choices=cardList, size=(50, -1))
        sizer1.Add(choice, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        label = wx.StaticText(self, -1, "Port:")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 1)
        choice = wx.Choice(self, -1, name='port5', choices=portList, size=(50, -1))
        sizer1.Add(choice, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        bsizer.Add(sizer1, 1, flag=wx.EXPAND)
        
        # Testerp6
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "[Testerp6:]")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        label = wx.StaticText(self, -1, "Card:")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 1)
        choice = wx.Choice(self, -1, name='card6', choices=cardList, size=(50, -1))
        sizer1.Add(choice, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        label = wx.StaticText(self, -1, "Port:")
        sizer1.Add(label, 0, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 1)
        choice = wx.Choice(self, -1, name='port6', choices=portList, size=(50, -1))
        sizer1.Add(choice, 1, wx.ALIGN_CENTRE_VERTICAL | wx.ALL, 5)
        bsizer.Add(sizer1, 1, flag=wx.EXPAND)
        
        # buttons
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        
        button = wx.Button(self, -1, u'Connect and Create')
        sizer1.Add(button, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.createPortlist, button)
        
        button = wx.Button(self, -1, u'Save')
        button.Disable()
        sizer1.Add(button, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        
        button = wx.Button(self, -1, u'Load')
        button.Disable()
        sizer1.Add(button, 0, wx.ALIGN_RIGHT | wx.ALL, 5)
        
        bsizer.Add(sizer1, 1, wx.ALIGN_RIGHT | wx.ALL)
        
        # 第二组
        box = wx.StaticBox(self, -1, "Script generate:")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        sizer.Add(bsizer, 0, wx.ALL, 5)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Portlist:", size=(70, -1))
        sizer1.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        choice = wx.Choice(self, 74, choices=self.portlist, size=(121, -1), name='portlist')
        choice.Enable(False)
        sizer1.Add(choice, 0, wx.ALIGN_CENTRE | wx.ALL, 1)
        bsizer.Add(sizer1, 1, flag=wx.EXPAND)
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        button = wx.Button(self, -1, u'Save Port Config', size=(150, -1))
        self.Bind(wx.EVT_BUTTON, self.savePortConfig, button)
        sizer1.Add(button, 0, wx.ALL, 5)
        
        button = wx.Button(self, -1, u'Load Port Config', size=(150, -1))
        self.Bind(wx.EVT_BUTTON, self.loadPortConfig, button)
        sizer1.Add(button, 0, wx.ALL, 5)
        bsizer.Add(sizer1, 1, wx.ALL)
        
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        button = wx.Button(self, -1, u'Start Transmit', size=(150, -1))
        self.Bind(wx.EVT_BUTTON, self.startTransmit, button)
        sizer1.Add(button, 0, wx.ALL, 5)
        
        button = wx.Button(self, -1, u'Stop Transmit', size=(150, -1))
        self.Bind(wx.EVT_BUTTON, self.stopTransmit, button)
        sizer1.Add(button, 0, wx.ALL, 5)
        bsizer.Add(sizer1, 1, wx.ALL)
        
        sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        button = wx.Button(self, -1, u'Start Capture', size=(150, -1))
        self.Bind(wx.EVT_BUTTON, self.startCapture, button)
        sizer1.Add(button, 0, wx.ALL, 5)
        
        button = wx.Button(self, -1, u'Stop Capture', size=(150, -1))
        self.Bind(wx.EVT_BUTTON, self.stopCapture, button)
        sizer1.Add(button, 0, wx.ALL, 5)
        bsizer.Add(sizer1, 1, wx.ALIGN_RIGHT | wx.ALL)
        
        sizer0.Add(sizer, 0, wx.EXPAND | wx.ALL)
        sizeright = wx.BoxSizer(wx.VERTICAL)
        textCtrl = wx.TextCtrl(self, 94, size=(550, 550), style=wx.TE_MULTILINE, name='resultwindow')
        sizeright.Add(textCtrl, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        sizer0.Add(sizeright, 0, wx.EXPAND | wx.ALL)
        
        self.SetSizer(sizer0)
        sizer0.Fit(self)
    
    def createPortlist(self, evt):
        hostip = self.FindWindowByName('hostip').GetValue()
        chassisid = self.FindWindowByName('chassisid').GetLabelText()
        ctrllist = []
        portlist = []
        portlistitem = []
        portliststr = ''
        
        for i in range(1, 7):
            card = self.FindWindowByName('card' + str(i)).GetLabelText()
            port = self.FindWindowByName('port' + str(i)).GetLabelText()
            if (card != '') and (port != ''):
                portlist.append(['portlist' + str(i), chassisid, card, port, hostip])
                portlistitem.append('portlist' + str(i))
        
        # print portlist
        self.portlist = portlist
        self.portlistitem = portlistitem
        choice = self.FindWindowByName('portlist')
        choice.SetItems(portlistitem)
        choice.Enable(True)
        choice.Refresh()
        self.hostip = self.FindWindowByName('hostip').GetValue()
        IxiaProc('InitIxia ' + self.hostip)
        
        for j in portlist:
            itemstr = "%s = \'[list [list %s %s %s ]]\'\n" % (j[0], j[1], j[2], j[3])
            portliststr += itemstr
        self.writeResult(portliststr)
    
    def startTclServer(self):
        StartTclServerTh()
    
    def setPortInfo(self):
        choice = self.FindWindowByName('portlist')
        select_id = choice.GetSelection()
        select = choice.GetString(select_id)
        for item in self.portlist:
            if item[0] == select:
                self.portinfo = ' [list [list ' + str(item[1]) + ' ' + str(item[2]) + ' ' + str(item[3]) + ' ]]'
                self.chassisid = str(item[1])
    
    def startTransmit(self, evt):
        self.setPortInfo()
        cmd = 'IxiaProc(' + '\'StartTransmit' + self.portinfo + '\')\n'
        self.writeResult(cmd)
    
    def stopTransmit(self, evt):
        self.setPortInfo()
        cmd = 'IxiaProc(' + '\'StopTransmit' + self.portinfo + '\')\n'
        self.writeResult(cmd)
    
    def startCapture(self, evt):
        self.setPortInfo()
        cmd = 'IxiaProc(' + '\'StartCapture' + self.portinfo + '\')\n'
        self.writeResult(cmd)
    
    def stopCapture(self, evt):
        self.setPortInfo()
        cmd = 'IxiaProc(' + '\'StopCapture' + self.portinfo + '\')\n'
        self.writeResult(cmd)
    
    def writeResult(self, res):
        textedit = self.FindWindowByName('resultwindow')
        wx.CallAfter(textedit.WriteText, res)
    
    def savePortConfig(self, evt):
        portconfig_dir = sys.path[0]
        if os.path.isfile(portconfig_dir):
            portconfig_dir = os.path.split(portconfig_dir)[0]
        dlg = wx.FileDialog(
            None, message="Save port config file as ...", defaultDir=portconfig_dir,
            defaultFile="", wildcard=wildcard, style=wx.SAVE
        )
        
        if dlg.ShowModal() == wx.ID_OK:
            try:
                res = ''
                time.sleep(5)
                path = dlg.GetPath()
                path = path.replace('\\', '/')
                print(path)
                self.setPortInfo()
                cmd = 'res = IxiaProc(' + '\'SaveIxiaPortConfig' + self.portinfo + ' ' + path + '\')'
                exec(cmd)
                print(res)
                cmd = '#' + cmd + '\n'
                self.writeResult(cmd)
                self.writeResult('#Save Ixia port ' + self.portinfo + ' config as file:' + path + '\n')
                # print('Save done!')
            except BaseException as e:
                print('[Failed:]' + str(e))
        dlg.Destroy()
    
    def loadPortConfig(self, evt):
        portconfig_dir = sys.path[0]
        if os.path.isfile(portconfig_dir):
            portconfig_dir = os.path.split(portconfig_dir)[0]
        dlg = wx.FileDialog(
            None, message="Choose a file",
            defaultDir=portconfig_dir,
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
        )
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            path = path.replace('\\', '/')
            self.setPortInfo()
            cmd = 'IxiaProc(' + '\'LoadIxiaPortConfig ' + path + '\')\n'
            self.writeResult(cmd)
        dlg.Destroy()


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = ConnIxiaFrame(parent=None)
    frame.Show()
    app.MainLoop()
