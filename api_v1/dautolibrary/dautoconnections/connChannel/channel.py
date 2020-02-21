# -*- coding: UTF-8 -*-
# *********************************************************************
# channel.py - 各种连接方式接口
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


class Channel(object):
    def connectChannel(self):
        pass
    
    def disconnectChannel(self):
        pass
    
    def readChannel(self):
        pass
    
    def writeChannel(self, msg):
        pass
