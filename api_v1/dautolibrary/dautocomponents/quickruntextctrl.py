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

import os

# from wx import wx
import wx
from dutils.dcnprint import printRes


class QuickRunTextCtrl(wx.TextCtrl):
    """
    快速运行窗口类
    """
    
    def __init__(self, parent, local_dir):
        """

        :param parent: parent frame
        :param local_dir: Dauto所在local dir路径
        """
        self.local_dir = local_dir
        wx.TextCtrl.__init__(self, parent, 551, '', wx.Point(0, 0), wx.Size(150, 90),
                             wx.NO_BORDER | wx.TE_MULTILINE, name='QuickRunTextCtrl')
        self.Bind(wx.EVT_CHAR, self.OnKeyPress)
    
    def OnKeyPress(self, evt):
        """
        :param evt: 窗口响应键盘鼠标事件句柄（ctrl+r 运行)
        :return: 调用TestRunAuto函数执行生成的default.py脚本
        """
        log_flag = 0  # 此处控制ctrl+r执行代码是否需要记录log, 默认不需要
        key_code = evt.GetKeyCode()
        if key_code == 18:  # Ctrl+R
            
            cmd = '\n'.join(['# -*- coding: UTF-8 -*-', 'from dcntestlibrary.dcnlibrary.dreceiver import *',
                             'from dcntestlibrary.dcnlibrary.lib_all import * ',
                             self.GetValue()])
            path = os.path.join(self.local_dir, 'default.py')
            with open(path, 'w+') as f:
                f.writelines(cmd)
            if self.Parent.thread and self.Parent.thread.isAlive():
                printRes('[One test is running,please stop it and then start a new one!]')
            else:
                self.Parent.TestRunAuto(path, log_flag)
        evt.Skip()  # 释放句柄 以方便后面的脚本执行
