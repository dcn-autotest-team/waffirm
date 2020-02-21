#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# Software : PyCharm
#
# dautoabout.py -
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
#       - 2018/3/11 11:24  add by yanwh
#
# *********************************************************************


from time import localtime


def get_copyright(copy_right=None):
    """
    获取copyright
    :param copy_right: copy_right
    :return: copy_right
    """
    if copy_right:
        _cr = str(copy_right).split()
        if _cr[1] == str(localtime().tm_year):
            return copy_right
        else:
            _cr[1] = str(localtime().tm_year)
            return ' '.join(_cr)
    else:
        from .dautoconst import COPYRIGHT as CR
        return CR


def get_description(description=None):
    """
    获取描述信息
    :param description: description
    :return: description
    """
    if description:
        _desc = str(description).split('\n')
        return '\n'.join(_d.strip() for _d in _desc)
    else:
        from .dautoconst import DESCRIPTION as DESC
        return DESC


def get_developers(developers=None):
    """
    获取开发者信息
    :param developers: developers
    :return: developers
    """
    if developers:
        return [dev for dev in developers]
    else:
        from .dautoconst import DEVELOPERS as DEV
        return DEV
