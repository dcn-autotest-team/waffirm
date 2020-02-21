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
import wx.py
from dutils.dcnprint import printRes


class DebugFrame(wx.py.shell.Shell):
    """
    从wx库中继承python shell解释器，shell启动之后执行脚本default.py
    默认default脚本会导入dreceiver和基础库函数，便于调试
    """
    
    def __init__(self, parent, local_dir):
        """
        初始化python shell实例，parent为parentframe, local_dir指定shell解释器默认生成的脚本路径
        :param parent: parentframe
        :param local_dir: shell解释器会自动生成一个名为local_dir/default.py的脚本
        """
        self.local_dir = local_dir
        _cmd = '\n'.join(['# -*- coding: UTF-8 -*-', 'from dcntestlibrary.dcnlibrary.dreceiver import *',
                          'from dcntestlibrary.dcnlibrary.lib_all import * ', ])
        _path = os.path.join(local_dir, 'default.py')
        with open(_path, 'w+') as f:
            f.writelines(_cmd)
        wx.py.shell.Shell.__init__(self, parent, 552, startupScript=_path)
        self.setDisplayLineNumbers(1)
        self.Bind(wx.EVT_CHAR, self.OnKeyPress)
    
    def OnKeyPress(self, evt):
        """
        shell解释器模式下面按住ctrl+r自定执行输入的命令
        :param evt: 窗口响应键盘鼠标事件句柄
        :return: 调用TestRunAuto函数执行生成的default.py脚本
        """
        log_flag = 0  # 此处控制ctrl+r执行代码是否需要记录log, 默认不需要
        keycode = evt.GetKeyCode()
        if keycode == 18:  # Ctrl+R
            cmd = '\n'.join(['# -*- coding: UTF-8 -*-', 'from dcntestlibrary.dcnlibrary.dreceiver import *',
                             'from dcntestlibrary.dcnlibrary.lib_all import * ',
                             self.getCommand()])
            path = os.path.join(self.local_dir, 'default.py')
            with open(path, 'w+') as f:
                f.writelines(cmd)
            if self.Parent.thread and self.Parent.thread.isAlive():
                printRes('[One test is running,please stop it and then start a new one!]')
            else:
                self.Parent.TestRunAuto(path, log_flag)
        evt.Skip()  # 释放句柄 以方便后面的脚本执行
