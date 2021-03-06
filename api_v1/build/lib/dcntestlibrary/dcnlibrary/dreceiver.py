#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# dreceiver.py - 脚本运行所需函数
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
#     - 2017.12.13 modified by zhangjxp RDM50596
# *********************************************************************
import time
from re import compile, M, I

import wx
from dutils.dcnprint import printResWarn


# 开始记录信息
def StartDebug(sut):
    window = wx.FindWindowByName(str(sut))
    if window is None:
        printResWarn('[告警]无法找到{}对应的tab窗口'.format(sut))
        return '[Error]:Can not find tab named', sut
    window.debugres = ''
    window.debugflag = 1


# 停止记录信息并返回
def StopDebug(sut):
    window = wx.FindWindowByName(str(sut))
    if window is None:
        printResWarn('[告警]无法找到sut对应的tab窗口', sut)
        return '[Error]:Can not find tab named', sut
    window.debugflag = 0
    res = window.debugres
    window.debugres = ''
    return res


# 新建连接并打开标签页
def CreateNewConn(conn_type, conn_name, conn_host, conn_path=None, log_type='default', logprefix=''):
    """
    :param conn_type: 连接类型 Telnet 或者TelnetCCM或者Serial
    :type conn_type: basestring
    :param conn_name: 创建窗口的名称
    :type conn_name: basestring
    :param conn_host: 要连接终端的地址和端口信息
    :type conn_host: basestring
    :param conn_path: 窗口对应的日志路径
    :type conn_path: basestring
    :param log_type: 执行类型 default或者run
    :type log_type: basestring
    :param logprefix: 日志前缀
    :type logprefix: basestring
    :return: None
    :rtype: None
    """
    window = wx.FindWindowByName('Main')
    conn_host = str(conn_host)
    window.CreateNewChannel(conn_type, conn_name, conn_host, conn_path, log_type, logprefix)


# 关闭连接并关闭标签页
def CloseChannels(title):
    window = wx.FindWindowByLabel(title)
    if window:
        window.OnCloseWindowAuto()


# 执行中脚本暂停
def Pause():
    window = wx.FindWindowByName('Main')
    window.PauseTestAuto()


# tuple类型转换
def GetData(**arg):
    return arg


################################################################################
##
# Receiver:
#
# args:
#     sut:
#     command:
#     timeout:
#     **args: 可变长度参数 promoteStop, promotePatten, promoteTimeout
##
# return:  buf:
##
# addition:
#
# examples:
##
# 输入信息并获取输出
##
# 获取表项：show in e 1/0/1
# data = Receiver('s1','show in e 1/0/1',3)
##
# 输入字符但不回车
# Receiver('s1','\x03',0.1,newLine = False)
##
# 等到表项打印完毕后以字符串格式返回
# data = Receiver('s1','show run',1,promoteStop = True)
#
################################################################################

def Receiver(sut, command, timeout=0, **args):
    """
    CLI跟终端交互函数
    :param sut: 设备名称
    :param command: 命令行
    :param timeout: 超时时间
    :param args: 可选参数
    :return: 终端返回buffer
    """
    
    def auto_input_cmd_by_include_or_not(_window, flag):
        """
        根据传递参数中includeCmd不同值执行不同的操作
        :param flag: includeCmd：True or False
        :return:
        """
        if flag:  # 默认情况直接将命令发送给终端
            _res = _window.WriteChannel(command + '\r')
        else:  # 如果includeCmd=False 表示命令行中带有|include命令
            _window.WriteChannel(command)
            time.sleep(0.1)
            _window.res = ''  # 清空回显
            _res = _window.WriteChannel('\r')
        return _res
    
    def judge_status_muliti(_res, try_times=10):
        """
        :param _res: window.WriteChannel返回值
        :param try_times: 尝试次数
        :return:
        """
        for _time in range(try_times):
            if _res == 1:  # 写入信息成功跳出循环
                break
            elif _res == 2:  # 线程重启失败，等待10s，重新执行写入操作
                time.sleep(10)
                _res = auto_input_cmd_by_include_or_not(include_cmd)
            elif _res == 3:
                time.sleep(5)  # 远程终端连接失败，重连，重新执行写入操作
                _res = auto_input_cmd_by_include_or_not(include_cmd)
            else:
                break
    
    # 如果可变长度参数 promotePatten 没有被赋值，则进行常规匹配
    promote_patten = args['promotePatten'] if 'promotePatten' in args else \
        '([#>])|(\[Boot\]:)|(BCM\.[0-9]>)|(->)|(Bootloader/>)'
    promote_timeout = args['promoteTimeout'] if 'promoteTimeout' in args else 300
    promote_stop = args['promoteStop'] if 'promoteStop' in args else False
    new_line = args['newLine'] if 'newLine' in args else True
    include_cmd = args['includeCmd'] if 'includeCmd' in args else True
    # 找到标签页,并且判断窗口实例对象是否全部初始化成功
    window = wx.FindWindowByName(str(sut))
    assert window, '没法找到窗口标签'
    if not window.sendMessageFlag:
        return ''
    # 存放获取到的数据
    window.res = ''
    if new_line:  # 输入信息后是否带'\r'
        res = auto_input_cmd_by_include_or_not(window, include_cmd)
        judge_status_muliti(res)
    else:
        res = window.WriteChannel(command)
        judge_status_muliti(res)
    # 发送信息后等待timeout时间
    time.sleep(int(timeout))
    # 如果promoteStop = True，在获取的信息中匹配promotePatten，如果匹配 成功，返回
    _time_tick = 0
    _compile = compile(promote_patten, M | I)
    if promote_stop and timeout == 0:
        while 1:
            buf = window.res
            if _compile.search(buf):
                time.sleep(0.08)
                break
            time.sleep(0.01)
            if _time_tick >= promote_timeout:
                break
            _time_tick += 0.01
    buf = window.res
    return buf
