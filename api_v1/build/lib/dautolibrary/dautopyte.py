#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# Software : PyCharm
#
# dautopyte.py - 
#
# Author    :yanwh(yanwh@digitalchina.com)
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd 
#
#
# *********************************************************************
# Change log:
#       - 2018/4/3 15:38  add by yanwh
#
# *********************************************************************


from .dautotplibrary.pyte import DebugScreen, DebugEvent
from .dautotplibrary.pyte import Stream


class DcnPyte(DebugScreen):
    """
    通过pyte模块中的DebugScreen讲从服务器获取的报文解析成对应的动作和数据
    形如action=draw/linefeed data：要输出的信息
    """
    __slots__ = 'msg'
    
    def __init__(self):
        DebugScreen.__init__(self)
        self.msg = []
    
    def only_wrapper(self, attr):
        def wrapper(*args, **kwargs):
            self.msg.append(DebugEvent(attr, args, kwargs))
        
        return wrapper
    
    def __getattribute__(self, attr):
        if attr not in Stream.events:
            return super(DebugScreen, self).__getattribute__(attr)
        elif not self.only or attr in self.only:
            return self.only_wrapper(attr)
        else:
            return lambda *args, **kwargs: None
