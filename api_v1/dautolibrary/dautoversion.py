#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# Software : PyCharm
#
# dautoversion.py -
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
#       - 2018/3/11 10:51  add by yanwh
#
# *********************************************************************


def get_version(version=None):
    """
    Returns a PEP 440-compliant version number from VERSION.
    :param version:
    :return:
    """
    version = get_complete_version(version)
    
    # Now build the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN - for pre-alpha releases
    #     | {a|b|rc}N - for alpha, beta, and rc releases
    
    main = get_main_version(version)
    
    sub = ''
    if version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'rc'}
        sub = mapping[version[3]] + str(version[4])
    
    return str(main + sub)


def get_main_version(version=None):
    "Returns main version (X.Y[.Z]) from VERSION."
    version = get_complete_version(version)
    parts = 2 if version[2] == 0 else 3
    return '.'.join(str(x) for x in version[:parts])


def get_complete_version(version=None):
    """Returns a tuple of the django version. If version argument is non-empty,
    then checks for correctness of the tuple provided.
    """
    if version is None:
        from .dautoconst import VERSION as version
    else:
        assert len(version) == 5
        assert version[3] in ('alpha', 'beta', 'rc', 'final')
    
    return version


def get_docs_version(version=None):
    version = get_complete_version(version)
    if version[3] != 'final':
        return 'dev'
    else:
        return '%d.%d' % version[:2]
