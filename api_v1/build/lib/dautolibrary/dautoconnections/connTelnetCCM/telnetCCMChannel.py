#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# telnetCCMChannel.py - telnetCCM连接方式实现
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
#     - 2017.11.3  RDM50307 modified by zhangjxp
#
# *********************************************************************
import time
from telnetlib import Telnet, IAC, WILL, ECHO, SGA, DO

from ..connChannel.channel import Channel

__all__ = ['TelnetCCMChannel']


class TelnetCCMChannel(Channel):
    """
    Telnet CCM 类，主要用户跟telnet ccm服务器交互（发送返回msg，处理协商，判断socket是否存在)
    """
    
    def __init__(self, host, port, timeout=3):
        self.conn_type = 'TelnetCCM'
        self.host = host
        self.port = port
        self.timeout = timeout
        self.telnet = None
        self.msg = None
        self.connected = False
        try:
            self.telnet = Telnet(host, port, self.timeout)
            self.telnet.set_option_negotiation_callback(self.handle_negotiation)  # 设置回调函数处理跟终端的协商
            self.connected = True
        except BaseException as e:
            self.msg = 'Connect to host:' + host + '[' + str(e) + ']'
            self.connected = False
            print((self.msg))
    
    @staticmethod
    def handle_negotiation(socket, command, option):
        """
        回调函数，处理telnet服务器发送回来的协商报文
        :param socket: socket
        :param command: WILL DO and so on
        :param option: ECHO SGA and so on
        :return: none
        """
        if command == WILL and option == ECHO:  # Will Echo
            socket.send(IAC + DO + ECHO)  # Do Echo
        if command == WILL and option == SGA:
            socket.send(IAC + DO + SGA)
    
    def reconnectChannel(self, reconnect_times=100, sleep_interval=1):
        """
        telnet重连
        :param reconnect_times: 重连次数，默认100
        :type reconnect_times: int
        :param sleep_interval: 每次重连时间，默认1s
        :type sleep_interval: int
        :return: None
        :rtype: None
        """
        for times in range(reconnect_times):
            time.sleep(sleep_interval)
            try:
                self.telnet.close()
                self.telnet = Telnet(self.host, self.port, self.timeout)
                self.connected = True
                print("[通知]socket重连成功")
                return self.telnet
            except BaseException as e:
                self.connected = False
                print('[通知]第%d次尝试重连，重连失败原因:%s' % (times, e))
    
    def disconnectChannel(self):
        """
        断开连接
        :return:None
        """
        self.telnet.close()
    
    def readChannel(self):
        """
        读取ccm发回来的数据信息（如果数据为空不存在暂停0.01s），socket连接断开触发重连
        :return:
        """
        if not self.is_exist_data():
            time.sleep(0.01)
        try:
            res = self.telnet.read_eager()
            return res
        except BaseException as e:
            print(e)
            self.reconnectChannel()
    
    def writeChannel(self, type_in):
        """
        往ccm服务器发送数据信息，socket断开触发重连
        :param type_in:
        :return:
        """
        try:
            self.telnet.write(type_in.encode('ascii'))
        except BaseException as e:
            print(e)
            self.reconnectChannel()
    
    def is_alive(self):
        """
        判断连接状态
        :return: True：成功 False:失败
        """
        return self.connected
    
    def is_exist_data(self):
        """
        判断socket上面是否存在数据
        :return: True：存在数据，False：不存在数据
        :rtype: bool
        """
        return self.telnet.sock_avail()
