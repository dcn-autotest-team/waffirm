#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# Software : PyCharm
#
# dcntools.py - 
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
#       - 2018/3/16 13:31  add by yanwh
#
# *********************************************************************

import re
import subprocess
import time
from functools import wraps

from .dcnprint import printResWarn


def ping_server(ip):
    """
    ping server
    :param ip: ping server 的ip地址
    :return: 1 成功 0 失败
    """
    lifeline = re.compile(r'bytes=\d+ time.*TTL=\d+')
    res = 0
    p = subprocess.Popen('ping ' + ip + ' -n 2 -w 100', shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.wait()
    p.stdout.flush()
    line = p.stdout.read()
    if re.findall(lifeline, line):
        res = 1
    return res


def idle(idle_time=0):
    """
    暂停装饰器
    :param idle_time:
    :return:
    """
    if idle_time and int(idle_time) > 0:
        time.sleep(idle_time)
        
        def _idle(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            
            return wrapper
        
        return _idle
    else:
        printResWarn('等待时间必须大于0')
