#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# dautoTelnetPCFactory.py - telnet连接方式工厂类
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
from .dautoTelnetPC import DautoTelnetPC
from ..connChannel.dautoChannelFactory import DautoChannelFactory


class DautoTelnetPCFactory(DautoChannelFactory):
    def createDautoChannel(self, host, port):
        return DautoTelnetPC(host, port)
