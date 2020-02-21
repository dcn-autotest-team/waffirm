#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# telnetPCChannel.py - telnet连接方式实现
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
import time
from telnetlib import DO, DONT, ECHO, IAC, LFLOW, NAWS, NEW_ENVIRON, SB, SE, SGA, STATUS, TSPEED, TTYPE, Telnet, WILL, \
    WONT, XDISPLOC

from ..connChannel.channel import Channel

__all__ = ['TelnetPCChannel']


class TelnetPCChannel(Channel):
    """
    Telnet PC 主要是linux server的类，包含读写以及重连断开等动作
    """
    
    def __init__(self, host, port, timeout=300):
        """
        初始化telnet lib实例
        :param host: ip
        :param port: 端口
        :param timeout: 超时时间
        """
        self.conn_type = 'TelnetPC'
        self.host = host
        self.port = port
        try:
            self.telnet = Telnet(host, port, timeout)
            self.telnet.set_option_negotiation_callback(self.handle_negotiation)  # 设置回调函数处理跟终端的协商
            self.telnet.sock.sendall(IAC + DO + SGA + IAC + WONT + TTYPE)
            self.telnet.set_debuglevel(0)  # 调试开关 0 不开启调试
            self.connected = True
            self.msg = ''
        except Exception as e:
            print('Connect to host:' + host + '[' + str(e) + ']')
            self.msg = 'Connect to host:' + host + '[' + str(e) + ']'
            self.connected = False
    
    def handle_negotiation(self, socket, command, option):
        """
        回调函数，处理telnet服务器发送回来的协商报文
        :param socket: socket
        :param command: WILL DO and so on
        :param option: ECHO SGA and so on
        :return: none
        """
        if command == DO and option == ECHO:  # ECHO
            socket.sendall(IAC + WONT + ECHO)  # Wont Echo
        if command == WILL and option == ECHO:  # Will Echo
            socket.sendall(IAC + DO + ECHO)  # Do Echo
        if command == DO and option == TSPEED:  # Terminal Speed
            socket.sendall(IAC + WONT + TSPEED)  # Wont Terminal Speed
        if command == DO and option == XDISPLOC:  # X Display  Location
            socket.sendall(IAC + WONT + XDISPLOC)  # Wont X Display Location
        if command == DO and option == NEW_ENVIRON:  # New Environment Option
            socket.sendall(IAC + WONT + NEW_ENVIRON)  # Wont New Environment Option
        if command == DO and option == NAWS:  # Negotiate About Window Size
            # 回应WindowSize大小 Width=90 Height=32 和 Do not Status 仿照SecurityCRT
            socket.sendall(
                IAC + WILL + NAWS + IAC + SB + NAWS + chr(0).encode('ascii') + chr(90).encode('ascii') + chr(0).encode(
                    'ascii') + chr(32).encode('ascii') + IAC + SE + IAC +
                DONT + STATUS)
        if command == DO and option == LFLOW:  # Remote Flow Control
            socket.sendall(IAC + WILL + LFLOW)  # Will Remote Flow Control
        # if command == WILL and option == SGA:
        #     socket.send(IAC + DO + SGA)
        if command == DO and option == STATUS:  # Do Status
            socket.sendall(IAC + WONT + STATUS)  # Wont Status
        if command == DO and option == TTYPE:  # Terminal Type
            socket.sendall(IAC + WONT + TTYPE)  # Do not Terminal Type
        # -------------------------此处代码等待后续进行扩展，完全仿造CRT做-----------------------------------------------
        if self.telnet.read_sb_data() == TTYPE + chr(1).encode('ascii'):  # 匹配服务器发送的协商vty类型的消息
            # 回复vty的类型 'vt100'
            socket.send(
                IAC + SB + TTYPE + chr(0).encode('ascii') + chr(118).encode('ascii') + chr(116).encode('ascii') + chr(
                    49).encode('ascii') + chr(48).encode('ascii') + chr(48).encode('ascii') + IAC + SE)
    
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
                self.telnet = Telnet(self.host, self.port, 3)
                self.telnet.set_option_negotiation_callback(self.handle_negotiation)
                self.telnet.sock.sendall(IAC + DO + SGA + IAC + WONT + TTYPE)
                self.connected = True
                print("[通知]socket重连成功")
                return self.telnet
            except BaseException as e:
                self.connected = False
                print('try %d times:%s' % (times, e))
        return 0
    
    def disconnectChannel(self):
        """
        断开socket连接
        :return:
        """
        self.telnet.close()
    
    def readChannel(self):
        """
        读取远程服务器返回信息，如果为空，暂停0.01s， 断开连接触发重传
        :return:
        """
        if not self.is_exist_data():
            time.sleep(0.01)
        try:
            res = self.telnet.read_eager()  # 此处连接linux pc注意使用read_eager否则cat大文件的时候会假死
            return res if res else None
        except BaseException as e:
            print(e)
            self.reconnectChannel()
    
    def writeChannel(self, type_in):
        """
        往远端服务器写入信息
        :param type_in: 往远端服务器输入的信息
        :return: None
        """
        try:
            if type_in == '\003' or type_in == '\003\r':
                self.telnet.sock.sendall(IAC + WILL + ECHO)
                self.telnet.sock.sendall(IAC + WILL + SGA)
            self.telnet.write(type_in.encode('ascii'))
        except BaseException as e:
            print(e)
            self.reconnectChannel()
