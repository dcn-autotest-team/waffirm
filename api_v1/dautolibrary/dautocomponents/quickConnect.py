#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# quickConnect.py - 快速链接(历史连接)控制函数
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

from dautolibrary.dautoxmlconfig import cc_path

from .quickConnectDialog import *


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


def loadconfig():
    """
    加载配置文件中历史连接数据
    :return:None
    """
    channelType = ''
    channelTitle = ''
    channelHost = ''
    channelList = []
    channelPath = ''
    _file_path = cc_path
    xml_doc = minidom.parse(_file_path)
    for node in xml_doc.firstChild.childNodes:
        if node.nodeName == 'channel':
            channelName = node.getAttribute('id')
            for i in node.childNodes:
                if i.firstChild is not None:
                    data = i.firstChild.data
                else:
                    data = ''
                if i.nodeName == 'type':
                    channelType = data
                if i.nodeName == 'title':
                    channelTitle = data
                if i.nodeName == 'host':
                    channelHost = data
                if i.nodeName == 'path':
                    channelPath = data
            
            nodeList = [channelType, channelTitle, channelHost, channelName, channelPath]
            channelList.append(nodeList)
    dlg = QuickConnectDialog(None, "Quick connect", channelList)
    val = dlg.ShowModal()
    
    if val == wx.ID_OK:
        delete_list = dlg.deletelist
        delete_list.sort()
        deleteconfig(delete_list)
        for conn in dlg.connectlist:
            CreateNewConn(conn[0], conn[1], conn[2], conn[3])
    else:
        pass
    dlg.Destroy()


def add2config(con_type, con_title, con_host, con_path):
    """
    将新建连接的信息写入配置文件
    :param con_type: telnet serial
    :param con_title: s1 s2
    :param con_host: 172.17.100.14
    :param con_path: log path
    :return: None
    """
    path = cc_path
    xml_doc = minidom.parse(path)
    count = 1
    for node in xml_doc.firstChild.childNodes:
        if node.nodeName == 'channel':
            channelName = node.getAttribute('id')
            if int(channelName) != count:
                node.setAttribute('id', str(count))
            count += 1
    
    channel = xml_doc.createElement('channel')
    channel.setAttribute('id', str(count))
    root = xml_doc.childNodes[0]
    root.appendChild(channel)
    
    conn_type_node = xml_doc.createElement('type')
    channel.appendChild(conn_type_node)
    text = xml_doc.createTextNode(con_type)
    conn_type_node.appendChild(text)
    
    conn_title_node = xml_doc.createElement('title')
    channel.appendChild(conn_title_node)
    text = xml_doc.createTextNode(con_title)
    conn_title_node.appendChild(text)
    
    con_host_node = xml_doc.createElement('host')
    channel.appendChild(con_host_node)
    text = xml_doc.createTextNode(con_host)
    con_host_node.appendChild(text)
    
    con_path_node = xml_doc.createElement('path')
    channel.appendChild(con_path_node)
    text = xml_doc.createTextNode(con_path)
    con_path_node.appendChild(text)
    with open(path, 'wb') as f:
        writer = codecs.lookup('utf-8')[3](f)
        xml_doc.writexml(writer, encoding='utf-8')
        writer.close()


def deleteconfig(count_list):
    """
    删除历史连接数据
    :param count_list: count list
    :return: None
    """
    path = cc_path
    xml_doc = minidom.parse(path)
    
    root = xml_doc.firstChild
    nodes = root.childNodes
    flag = 0
    for i in count_list:
        node = nodes[int(i) - 1 - flag]
        flag += 1
        root.removeChild(node)
    
    count = 1
    for node in xml_doc.firstChild.childNodes:
        if node.nodeName == 'channel':
            channelName = node.getAttribute('id')
            if int(channelName) != count:
                node.setAttribute('id', str(count))
            count += 1
    with open(path, 'wb') as f:
        writer = codecs.lookup('utf-8')[3](f)
        xml_doc.writexml(writer, encoding='utf-8')
        writer.close()
