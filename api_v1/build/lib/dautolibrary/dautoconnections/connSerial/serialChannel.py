#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# serialChannel.py - 串口连接方式实现
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

import serial

from ..connChannel.channel import *


class SerialChannel(Channel):
    def __init__(self, com):
        self.conn_type = 'Serial'
        try:
            self.com = com
            self.con = serial.Serial((com - 1), 9600, bytesize=8, parity='N', stopbits=1, timeout=0.01, xonxoff=0,
                                     rtscts=0)
            self.connected = True
        except BaseException as e:
            self.msg = 'Connect to port:' + str(com) + '[' + str(e) + ']'
            self.connected = False
    
    def reconnectChannel(self):
        
        com = self.com
        for times in range(0, 100):
            time.sleep(1)
            try:
                self.con.close()
                self.con = serial.Serial((com - 1), 9600, bytesize=8, parity='N', stopbits=1, timeout=0.01, xonxoff=0,
                                         rtscts=0)
                print("Connect successfully,sir!")
                return self.con
            except BaseException as e:
                print('try %d times:%s' % (times, e))
        return 0
    
    def disconnectChannel(self):
        self.con.close()
    
    def readChannel(self):
        time.sleep(0.01)
        try:
            buf = self.con.readline()
            return buf
        except BaseException as e:
            print(e)
            return ""
    
    def writeChannel(self, type_in):
        try:
            self.con.write(type_in.encode('ascii'))
            self.connected = True
        except BaseException as e:
            print('[SerialChannel]', e)
