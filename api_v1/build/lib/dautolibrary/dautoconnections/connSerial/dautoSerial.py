#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# dautoSerial.py - 串口连接方式产品类
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

from .serialChannel import SerialChannel


class DautoSerial:
    def __init__(self, port):
        self.channel = SerialChannel(port)
    
    def getChannelOP(self):
        return self.channel
