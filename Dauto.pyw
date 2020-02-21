#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# Dauto.pyw - Dauto主框
# 
# Author:caisy(caisy@digitalchina.com)
#
# Version 2.10.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd 
#
# 
# *********************************************************************
# Change log:
#     - 2011.8.31  modified by caisy
#     - 2017.12.13 modified by zhangjxp RDM50596
# *********************************************************************
# from __future__ import print_function
# -------------------python内建模块(库)和第三方模块(库)---------------------------------------------------------------------
import getopt
import os
import sys
from pathlib import Path

import wx
# -------------------项目撰写核心模块(库)----------------------------------------------------------------------------------
# Dauto平台组件模块
from dautolibrary.dautocomponents.parentframe import ParentFrame
# ----------------------------------------------------------------------------------------------------------------------
# Dauto平台数据和网络通信相关模块
# from AffirmWireless.connDsend import *  # Dauto平台自研发包工具
# from dautolibrary.dautocomponents.wirelessDialog import *
# ----------------------------------------------------------------------------------------------------------------------
# Dauto平台辅助模块
# from dautolibrary.dautosyspath import optimize_syspath  # 初始化python的sys path（必须优先调用）
from dautolibrary.dautoutils.dautotools import dauto_catch_error  # Dauto装饰器函数，封装wx.CallAfter函数，简化代码逻辑
from dcntestlibrary.dcnlibrary.lib_all import *  # 导入一些基础的库

# ----------------------------------------------------------------------------------------------------------------------
# 其他辅助模块导入

# 优化syspath设置，减少无效的搜索路径
# optimize_syspath()

# 初始化变量
# ----------------------------------------------------------------------------------------------------------------------
_local_dir = Path(os.path.abspath(os.path.dirname(__file__)))

local_dir = _local_dir.as_posix()

log_base_path = f'{_local_dir}/logs'

if not os.path.isdir(log_base_path):
    os.mkdir(log_base_path)

log_config_file = f'{_local_dir}/config/logconfig.json'

ftp_config_file = f'{_local_dir}/config/ftpconfig.json'

ftp_server_ip = '192.168.60.60'


# ----------------------------------------------------------------------------------------------------------------------


class App(wx.App):
    def __init__(self):
        wx.App.__init__(self, False)
    
    def OnInit(self):
        frame = ParentFrame(parent=None, local_dir=local_dir, log_config_file=log_config_file,
                            ftp_config_file=ftp_config_file, log_base_path=log_base_path, ftp_server_ip=ftp_server_ip)
        frame.CenterOnScreen()
        frame.Show()
        return True


def main():
    # yappi.start()
    try:
        app = App()
        if len(sys.argv) > 1:
            mainpath = None
            opts, args = getopt.getopt(sys.argv[1:], 'l:m:e:')
            for op, values in opts:
                if op == '-l':
                    values = os.path.normpath(values).lstrip()
                    mainpath = values
                    pass
                elif op == '-m':
                    if mainpath:
                        runpath = os.path.join(mainpath, values)
                        wx.FindWindowById(10).TestRunAuto(runpath)
        # wx.FindWindowById(10).TestRunAuto(r'E:\DautoTest\autoTests\waffirm\waffirm_main.py')
        # wx.FindWindowById(10).CreateNewChannel('TelnetCCM', 's1', '172.17.100.14:10010')
        app.MainLoop()
        # yappi.stop()
        # stats = yappi.convert2pstats(yappi.get_func_stats())
        # stats.sort_stats("cumulative")
        # stats.print_stats()
        # stats.dump_stats('result1.pstat')
    except (Exception, BaseException) as e:
        print(e)
        dauto_catch_error()


if __name__ == '__main__':
    main()
