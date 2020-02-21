#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# Software : PyCharm
#
# dautoconst.py - Dauto Tools Const
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
#       - 2018/2/8 8:59  add by yanwh
#
# *********************************************************************


import platform

from .dautoabout import get_copyright, get_developers, get_description
from .dautoversion import get_version

# 自动测试平台的基础（Root）路径，其他模块建议均从此处统一获取

# Dauto平台窗口标题名称
# Main_WINDOW_TITLE = os.path.split(DAUTO_BASE_PATH)[1] if os.path.split(DAUTO_BASE_PATH)[1] else 'DC云科网络自动测试平台'
Main_WINDOW_TITLE = 'DC云科自动测试平台'
# 宿主机的操作系统类型，兼容linux
OS_TYPE = platform.platform()

# ------------------------------------------------------------------------------------
# Dauto工具打开文件的时候支持的文件类型(AutoTest-Run test cases-选择文件)
WILDCARD = """
           Python source (*.py)|*.py|
           Compiled Python (*.pyc)|*.pyc|
           SPAM files (*.spam)|*.spam|
           Egg file (*.egg)|*.egg|
           All files (*.*)|*.*
           """

# 打开串口保存Log的时候支持的log格式
WILDCARDLOG = """
              Log files (*.log)|*.log|
              All files (*.*)|*.*
              """
# --------------------------------Dauto平台常量信息----------------------------------------------------
# Dauto版本信息 严格遵守PEP 440-compliant规定
VERSION = (1, 0, 3, 'final', 0)

# Dauto 名称，版权信息 描述 网址 以及作者信息
NAME = 'Dauto'

WEBSITE = 'http://192.168.60.60/login.php'  # FAQ website 目前填写testlink网址，后续可以变更

COPYRIGHT = "(C) 2018 DCN"  # 会随着系统时间自动更新中间时间参数

DESCRIPTION = \
    """
DCN  Autotest tools For Wireless 
Powered By Python 2.7 
Copy right Digital China Networks Co.Ltd
"""

DEVELOPERS = 'caisy@digitalchina.com', 'zhaohj@digitalchina.com', 'yanwh@digitalchina.com'

# -------------------------------help->about窗口显示信息（Dauto.OnAbout函数使用的相关参数）--------------------------------
# 下述参数会呈现在Dauto平台Help->About中（Dauto 中的OnAbout函数使用），版本的迭代更新和版权信息作者和描述均在此修改
HELP_ABOUT_VERSION = get_version(VERSION)  # PEP 440-compliant version number from VERSION.

HELP_ABOUT_COPYRIGHT = get_copyright(COPYRIGHT)

HELP_ABOUT_DESCRIPTION = get_description(DESCRIPTION)

HELP_ABOUT_DEVELOPERS = get_developers(DEVELOPERS)

HELP_ABOUT_NAME = NAME

HELP_ABOUT_WEBSITE = WEBSITE
