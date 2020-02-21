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


import threading
import time

# from wx import wx
import wx


class PrintThread(threading.Thread):
    """
    向调试窗口打印信息的线程
    """
    
    def __init__(self, thread_name):
        """
        线程名称，用户标识线程
        :param thread_name:
        """
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_control = threading.Event()
        self.thread_control.clear()
        self._will_kill = False
        self._event = threading.Event()
        self._event.set()
    
    def localtrace(self, frame, why, arg):
        if self._will_kill and why == 'line':
            raise SystemExit()
        elif not self._event.isSet() and why == 'line':
            self._event.wait()
        return self.localtrace
    
    def stop(self):
        self.thread_control.set()
    
    def run(self):
        """
        while循环获取主窗口收到的msg，向打印窗口输出信息，并且记录log
        :return: None
        """
        pos = 0
        main_window = wx.FindWindowByName('Main')
        while 1:
            # 向调试窗口打印系统输出
            time.sleep(0.2)
            main_window.buff.flush()
            main_window.buff.seek(pos)
            stdout_msg = main_window.buff.read()
            pos += len(stdout_msg)
            if stdout_msg:
                window = wx.FindWindowById(553)
                if main_window.logger:
                    main_window.logger.info(stdout_msg)
                if window:
                    window.WriteToText(stdout_msg)
            if self.thread_control.isSet():
                break
