#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# Software : PyCharm
#
# dcntestlinkutils.py -
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
#       - 2018/3/19 19:20  add by yanwh
#
# *********************************************************************


def recover_args(path=None):
    """
    修改参数，避免单跑调试脚本的结果回传到testlink
    :return: None
    """
    _temp = """#!/usr/bin/env python
# -*- coding: UTF-8 -*-
args = {
    'productLine': '无线产品线',
    'testSuite': '无线确认测试',
    'testPlan': 'auto',
    'testBuild': 'auto',
    'testDevice': 'auto',
    'notes': '',
    'user': 'auto',
    'aftersaleFlag': '0',
    'aftersaleVersion': 'auto',
    'scriptVersion': 'auto'
  }
        """
    if path is None:
        import os
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'args.py')
        del os
    _args_filename = path
    with open(_args_filename, str('w+')) as _fp:
        _fp.write(str(_temp))
