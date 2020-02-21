###-*- coding: UTF-8 -*-
# *********************************************************************
# wirelessDialog.py - 新建连接-对话框
# 
# Author:qidb(qidb@digitalchina.com)
#
# Version 2.0.0
#
# Copyright (c) 2004-2013 Digital China Networks Co. Ltd 
#
# 
# *********************************************************************
# Change log:
#     - 2013.8.20  
#
# *********************************************************************

import os
import sys

import wx

try:
    import wx.combo as _combo
    
    comboctrl = _combo.ComboCtrl
except ImportError:
    comboctrl = wx.ComboCtrl

from .messageBox import Alert

wildcard = "Python source (*.log)|*.log|" \
           "All files (*.*)|*.*"


class WirelessDialog(wx.Dialog):
    """
    无线专用Dialog窗口
    """
    
    def __init__(self, parent, ID, title):
        
        wx.Dialog.__init__(self, parent, ID, title, size=(500, 350), style=wx.DEFAULT_DIALOG_STYLE)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        label = wx.StaticText(self, -1, "                       无线自动确认测试选项:                       ")
        sizer.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        # --------------------------------------------------------------------
        box = wx.BoxSizer(wx.HORIZONTAL)
        
        label = wx.StaticText(self, -1, "操作人 IT CODE:")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        self.text1 = wx.TextCtrl(self, 2800)
        box.Add(self.text1, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        # --------------------------------------------------------------------
        # --------------------------------------------------------------------
        box = wx.BoxSizer(wx.HORIZONTAL)
        
        label = wx.StaticText(self, -1, "PASSWORD:      ")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        self.text0 = wx.TextCtrl(self, 2799)
        box.Add(self.text0, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        # --------------------------------------------------------------------
        box = wx.BoxSizer(wx.HORIZONTAL)
        
        label = wx.StaticText(self, -1, "AP Model:       ")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        sampleList = ['5-DCWL-7942AP-R4', '7-DCWL-7962AP-R4', '21-DCWL-7942AP-R5', '22-DCWL-7962AP-R5',
                      '26-DCWL-1000WAP-R1', '27-DCWL-2000WAP-R1', '28-DCWL-1000WAP-R1.1', '29-WL8200-I2-R1',
                      '30-WL8200-I3-R1', '31-DCWL-2000WAP-L-R1']
        self.choice1 = wx.Choice(self, 2801, (300, -1), choices=sampleList)
        box.Add(self.choice1, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        # --------------------------------------------------------------------
        box = wx.BoxSizer(wx.HORIZONTAL)
        
        label = wx.StaticText(self, -1, "AC Model:       ")
        box.Add(label, 0, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        sampleList = ['6028', '6222', '8504', '6002/6028P', 'DSCC']
        self.choice2 = wx.Choice(self, 2802, (300, -1), choices=sampleList)
        box.Add(self.choice2, 1, wx.ALIGN_CENTRE | wx.ALL, 5)
        
        sizer.Add(box, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        ##--------------------------------------------------------------------
        # --------------------------------------------------------------------
        ##        box = wx.BoxSizer(wx.HORIZONTAL)
        ##
        ##        label = wx.StaticText(self, -1, u"Comment: eg:建行测试版本等说明                              ")
        ##        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        ##
        ##        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        # --------------------------------------------------------------------
        # --------------------------------------------------------------------
        ##        box = wx.BoxSizer(wx.HORIZONTAL)
        ##
        ##        self.text2 = wx.TextCtrl(self, 2798)
        ##        box.Add(self.text2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        ##
        ##        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        # --------------------------------------------------------------------
        # box = wx.BoxSizer(wx.HORIZONTAL)
        
        # label = wx.StaticText(self, -1, u"AP确认测试用IMG: ")
        # box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        # self.combo1 = FileSelectorCombo(self,size=(200 , -1))
        # box.Add(self.combo1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        # sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        ##--------------------------------------------------------------------   
        # box = wx.BoxSizer(wx.HORIZONTAL)
        
        # label = wx.StaticText(self, -1, u"AP确认测试用UBOOT: ")
        # box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        # self.combo2 = FileSelectorCombo(self,size=(200 , -1))
        # box.Add(self.combo2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        # sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        ##--------------------------------------------------------------------
        # box = wx.BoxSizer(wx.HORIZONTAL)
        
        # label = wx.StaticText(self, -1, u"AP测试升级用IMG: ")
        # box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        # self.combo3 = FileSelectorCombo(self,size=(200 , -1))
        # box.Add(self.combo3, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        # sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        ##--------------------------------------------------------------------   
        # box = wx.BoxSizer(wx.HORIZONTAL)
        
        # label = wx.StaticText(self, -1, u"AP测试升级用UBOOT: ")
        # box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        # self.combo4 = FileSelectorCombo(self,size=(200 , -1))
        # box.Add(self.combo4, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        # sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        ##--------------------------------------------------------------------   
        
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
    
    def save(self, evt):
        ### zhaohj ###
        default_dir = sys.path[0]
        if os.path.isfile(default_dir):
            default_dir = os.path.split(default_dir)[0]
        ### zhaohj
        dlg2 = wx.FileDialog(
            # None, message="Save file as ...", defaultDir=os.getcwd(),
            None, message="Save file as ...", defaultDir=default_dir,
            defaultFile="", wildcard=wildcard, style=wx.SAVE
        )
        if dlg2.ShowModal() == wx.ID_OK:
            try:
                path = dlg2.GetPath()
                print(path)
                text = self.win.GetValue()
                fileBuffer = open(path, "w")
                fileBuffer.writelines(text)
                fileBuffer.close()
                Alert(self, 'Save done!')
            except BaseException as e:
                Alert(self, '[Failed:]' + str(e))
        
        dlg2.Destroy()


class FileSelectorCombo(comboctrl):
    def __init__(self, *args, **kw):
        wx.combo.ComboCtrl.__init__(self, *args, **kw)
        
        # make a custom bitmap showing "..."
        bw, bh = 14, 16
        bmp = wx.EmptyBitmap(bw, bh)
        dc = wx.MemoryDC(bmp)
        
        # clear to a specific background colour
        bgcolor = wx.Colour(255, 254, 255)
        dc.SetBackground(wx.Brush(bgcolor))
        dc.Clear()
        
        # draw the label onto the bitmap
        label = "..."
        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        tw, th = dc.GetTextExtent(label)
        dc.DrawText(label, (bw - tw) / 2, (bw - tw) / 2)
        del dc
        
        # now apply a mask using the bgcolor
        bmp.SetMaskColour(bgcolor)
        
        # and tell the ComboCtrl to use it
        self.SetButtonBitmaps(bmp, True)
    
    # Overridden from ComboCtrl, called when the combo button is clicked
    def OnButtonClick(self):
        path = ""
        name = ""
        if self.GetValue():
            path, name = os.path.split(self.GetValue())
        
        dlg = wx.FileDialog(self, "Choose File", 'c:\\version', name,
                            "All files (*.*)|*.*", wx.OPEN | wx.CHANGE_DIR)
        if dlg.ShowModal() == wx.ID_OK:
            self.SetValue(dlg.GetPath())
        dlg.Destroy()
        self.SetFocus()
    
    # Overridden from ComboCtrl to avoid assert since there is no ComboPopup
    def DoSetPopupControl(self, popup):
        pass
