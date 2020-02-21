#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# dautoSerialFactory.py - 串口连接方式工厂类
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
from .dautoSerial import DautoSerial
from ..connChannel.dautoChannelFactory import DautoChannelFactory


class DautoSerialFactory(DautoChannelFactory):
    def createDautoChannel(self, port):
        return DautoSerial(port)
