#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# dautoTelnetCCM.py - telnetCCM连接方式产品类
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

from .telnetCCMChannel import TelnetCCMChannel


class DautoTelnetCCM:
    def __init__(self, host, port):
        self.channel = TelnetCCMChannel(host, port)
    
    def getChannelOP(self):
        return self.channel
