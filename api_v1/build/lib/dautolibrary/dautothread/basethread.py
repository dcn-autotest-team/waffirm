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
import ctypes
import inspect
import os
import time
import traceback
from threading import Thread, Event, currentThread, settrace

# from wx import wx
import wx
from dautolibrary.dautoutils.dautoprint import printGlobal
from dautolibrary.dautoutils.dautotools import call_after


class ExThread(Thread):
    """
    Dauto平台线程基础类，继承Thread类，重写start以及run方法，增加kill pause ahead等方法实现线程控制
    """
    
    def __init__(self, thread_name, filename, window, print_flag=0, test_case_name='Test', event=Event(), *args, **kw):
        """
        初始化线程类实例
        :param thread_name:线程名称
        :param filename: 要执行的脚本名称
        :param window: parent frame
        :param print_flag: 是否打印输出
        :param test_case_name: case名称
        :param event: evt时间，用于控制线程状态同步
        :param args: 额外参数
        :param kw: 额外参数
        """
        Thread.__init__(self, name=thread_name, *args, **kw)
        self.testcasename = test_case_name
        self.printflag = print_flag
        self.filename = filename
        self.window = window
        self._killed = False
        self._willKill = False
        self._event = event
        self._event.set()
    
    def run_test_case(self):
        """
        运行指定测试用例（py脚本）
        :return:
        """
        exec(compile(open(self.filename, "rb").read(), self.filename, 'exec'))
    
    @staticmethod
    def globaltrace(frame, why, arg):
        """
        异常捕获跟踪
        :param frame:
        :param why:
        :param arg:
        :return:
        """
        try:
            return currentThread().localtrace if why == 'call' else None
        except AttributeError:
            pass
    
    def start(self):
        """
        start方法，线程实例调用run方法执行，会首选调用start方法，此处用于创建日志路径，根据需求打印输出信息到窗口
        :return:
        """
        settrace(self.globaltrace)
        if self.printflag:
            thispath = self.window.local_dir
            logpath = os.path.join(thispath, 'logs', 'run', self.testcasename)
            if not os.path.exists(logpath):
                os.makedirs(logpath)
            printGlobal('TestCase ' + str(self.testcasename), 'Start')
        Thread.start(self)
    
    def localtrace(self, frame, why, arg):
        """
        响应手动停止线程
        :param frame:
        :param why:
        :param arg:
        :return:
        """
        if self._willKill and why == 'line':
            # print('----[Warning] User Click Stop Button to Force Kill Running Thread----')
            raise SystemExit()
        elif not self._event.isSet() and why == 'line':  # 执行脚本的线程执行完毕，阻塞线程，线程进入等待状态直到set方法唤醒
            self._event.wait()
        return self.localtrace
    
    @call_after
    def kill(self):
        """
        线程退出
        :return:
        """
        if self._killed:
            return 0
        self._willKill = True
        if self.printflag:
            printGlobal('TestCase ' + str(self.testcasename), 'End')
        self._event.set()
        self._killed = True
        time.sleep(1)
    
    # 快速退出线程方法
    @call_after
    def quick_kill(self):
        def _async_raise(tid, exctype):
            tid = ctypes.c_long(tid)
            if not inspect.isclass(exctype):
                exctype = type(exctype)
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
            if not res:
                self.kill()
            elif res != 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                raise SystemError('PyThreadState_SetAsyncExc Error')
        
        _async_raise(self.ident, SystemExit)
    
    @call_after
    def pause(self):
        """
        想成暂停
        :return:
        """
        self._event.clear()
    
    @call_after
    def ahead(self):
        """
        线程继续
        :return:
        """
        self._event.set()
    
    def run(self):
        """
        运行脚本的线程，运行脚本结束之后调用AutoTestKill清理log等相关资源，最后线程kill，捕获详细异常输出
        :return:
        """
        self._killed = False
        try:
            exec(compile(open(self.filename, "r").read(), self.filename, 'exec'), {})
        except (Exception, BaseException) as e:
            print(('Thread Running Occur Exception {}'.format(e)))
            print((traceback.print_exc()))
        wx.CallAfter(self.window.AutoTestKill)
        self._killed = True
