#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# Software : PyCharm
#
# dautolazyimport.py -
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
#       - 2018/3/30 13:25  add by yanwh
#
# *********************************************************************

import imp
import sys

_lazy_modules = {}


class LazyModule(object):
    def __init__(self, name):
        self.name = name
    
    def __getattr__(self, attr):
        
        try:
            path = _lazy_modules[self.name]
            f, pathname, desc = imp.find_module(self.name, path)
            
            lf = sys.meta_path.pop()
            imp.load_module(self.name, f, pathname, desc)
            sys.meta_path.append(lf)
            
            self.__dict__ = sys.modules[self.name].__dict__
            return self.__dict__[attr]
        except (ImportError, Exception):
            pass
            # return self.__dict__[attr]


class LazyFinder(object):
    def find_module(self, name, path):
        _lazy_modules[name] = path
        return self
    
    @staticmethod
    def load_module(name):
        return LazyModule(name)


sys.meta_path.append(LazyFinder())
