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


# 从各种Channel读取信息线程
import threading

from dutils.dcnprint import printResError


class ReadThread(threading.Thread):
    """
    读取远程服务器发送过来的信息的线程，通过协程实现
    """
    
    def __init__(self, thread_name, window, channel, c):  # 协程实现部分代码
        """
        初始化线程实例
        :param thread_name: 线程名称
        :param window: parent frame
        :param channel: 远程连接服务器的channel实例，用于远程会话交互
        :param c: 协程，chlidframe模块中通过consumer协程函数生成的协程对象，将thread read到的信息，
        传给chlidframe.WriteTextCtrl函数显示到窗口
        """
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.window = window
        self.thread_control = threading.Event()
        self.thread_control.clear()
        self._will_kill = False
        self._event = threading.Event()
        self._event.set()
        self.channel = channel
        self.c = c  # 协程实现部分代码
    
    def localtrace(self, frame, why, arg):
        """
        异常捕获
        :param frame:
        :param why:
        :param arg:
        :return:None
        """
        if self._will_kill and why == 'line':
            raise SystemExit()
        elif not self._event.isSet() and why == 'line':
            self._event.wait()
        return self.localtrace
    
    def stop(self):
        """
        线程暂停
        :return:
        """
        self.thread_control.set()
    
    # 读取远端串口发来的信息
    def run(self):
        """
        读取远程服务器发送回来的信息，并且通过协程传递给chlidframe.WriteTextCtrl函数显示到窗口
        :return:
        """
        self.c.send(None)  # 协程实现部分代码
        while 1:
            if self.thread_control.isSet():
                self.channel.disconnectChannel()
                break
            try:
                msg = self.channel.readChannel()
            except BaseException as e:
                printResError('[异常]线程读取远端服务器发送回来的信息异常，异常如下:{}'.format(e))
            if msg:
                self.c.send(msg)  # 协程实现部分代码
            else:
                self.thread_control.wait(0.1)
