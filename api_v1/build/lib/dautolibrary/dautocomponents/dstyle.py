#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# dstyle.py - 样式设置
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

import codecs
from xml.dom import minidom

import wx
import wx.aui
from dautolibrary.dautoutils.dautotools import call_after
from dautolibrary.dautoxmlconfig import *


def loadLogConfig():
    """
    控制执行Receiver函数是否打印时间戳
    :return:
    """
    path = lc_path
    xmldoc = minidom.parse(path)
    root = xmldoc.firstChild
    nodes = root.childNodes
    logconfig = nodes[0].childNodes[0].firstChild.data
    try:
        logconfig = eval(logconfig)
    except BaseException as e:
        print('[loadLogConfig]{}'.format(e))
    return logconfig


load_log_config = loadLogConfig


def LoadReceiverDebugConfig(path=dc_path):
    """
    加载dauto平台debug样式，用户step by step debug显示样式
    :param path: 配置文件路径
    :return: 重新加载后配置文件
    """
    xmldoc = minidom.parse(path)
    root = xmldoc.firstChild
    nodes = root.childNodes
    reconfig = nodes[0].childNodes[0].firstChild.data
    try:
        reconfig = eval(reconfig)
    except BaseException as e:
        print('[loadLogConfig]', e)
    return reconfig


load_receiver_debug_config = LoadReceiverDebugConfig


def LoadErrorStopConfig(path=dc_path):
    """
    控制执行脚本时是否遇错暂停
    :param path: 配置文件路径
    :return: 重新加载后配置文件
    """
    xmldoc = minidom.parse(path)
    root = xmldoc.firstChild
    nodes = root.childNodes
    reconfig = nodes[0].childNodes[1].firstChild.data
    try:
        reconfig = eval(reconfig)
    except BaseException as e:
        print('[loadLogConfig]{}'.format(e))
    return reconfig


load_error_stop_config = LoadErrorStopConfig


def loadStyleConfig(flag=False, path=sc_path):
    """
    从配置文件加载样式
    :param flag: 控制标志位
    :param path: 配置文件路径
    :return: style_list
    """
    style_list = []
    xmldoc = minidom.parse(path)
    root = xmldoc.firstChild
    nodes = root.childNodes
    for node in nodes:
        for i in node.childNodes:
            if i.nodeName == 'enable':
                if i.firstChild.data == 'True' or flag:
                    style_name = node.childNodes[0].firstChild.data
                    style_enable = eval(node.childNodes[1].firstChild.data)
                    style_background_color = eval(node.childNodes[2].firstChild.data)
                    style_foreground_color = eval(node.childNodes[3].firstChild.data)
                    style = [style_name, style_enable, style_background_color, style_foreground_color]
                    style_list.append(style)
    
    return style_list


load_style_config = loadStyleConfig


def saveStyleConfig(style_id, path=sc_path):
    """
    保存样式配置
    :param path: 配置文件路径
    :param style_id: style id
    :return: None
    """
    xmldoc = minidom.parse(path)
    root = xmldoc.firstChild
    nodes = root.childNodes
    for node in nodes:
        for i in node.childNodes:
            if node.getAttribute('id') == str(style_id):
                node.childNodes[1].firstChild.data = 'True'
            else:
                node.childNodes[1].firstChild.data = 'False'
    
    with open(path, 'wb') as f:
        writer = codecs.lookup('utf-8')[3](f)
        xmldoc.writexml(writer, encoding='utf-8')
        writer.close()


save_style_config = saveStyleConfig


@call_after
def ChangeColor(mode):
    """
    更改串口背景窗口样式（颜色）
    :param mode:mode
    :return:None
    """
    saveStyleConfig(mode)
    window = wx.FindWindowByName('Main')
    windows_list = window.GetChildren()
    aui_client_list = windows_list[0].GetChildren()
    stylelist = loadStyleConfig()[0]
    color_background = stylelist[2]
    color_foreground = stylelist[3]
    for frame in aui_client_list:
        try:
            frame.page.SetBackgroundColour(color_background)
            frame.page.SetForegroundColour(color_foreground)
            wx.CallAfter(frame.page.Refresh)
        except AttributeError:
            pass


change_color = ChangeColor
