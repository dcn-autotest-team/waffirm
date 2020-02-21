#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# quickCreatePy.py - 重复脚本快速生成控制函数
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

import re
import socket
import struct

import wx

wildcard = "Python source (*.py)|*.py|" \
           "All files (*.*)|*.*"


def setIncrMacList(args, maxnum):
    """
    创建mac递增列表
    :param args:
    :param maxnum:
    :return:
    """
    value = ''
    num = 0
    argslist = args.split(',')
    
    try:
        value = eval(argslist[0])
        num = argslist[1]
    except IndexError as e:
        pass
    num = int(num)
    maxnum = int(maxnum)
    valueTemp = value
    valueList = []
    for i in range(1, int(maxnum) + 1):
        valueList.append(value)
        valueInt = int(value.replace('-', ''), 16)
        valueInt += 1
        value = hex(valueInt)
        value = str(value).replace('0x', '')
        value = value.replace('L', '')
        for k in range(0, (12 - len(value))):
            value = '0' + str(value)
        value = value[0:2] + '-' + value[2:4] + '-' + value[4:6] + '-' + value[6:8] + '-' + value[8:10] + '-' + value[
                                                                                                                10:12]
        if i % num == 0:
            value = valueTemp
    return valueList


def setIncrIpList(args, maxnum, ):
    """
    创建ip递增列表
    :param args:
    :param maxnum:
    :return:
    """
    value = ''
    num = 0
    mode = 4
    step = 1
    argslist = args.split(',')
    try:
        value = argslist[0]
        num = argslist[1]
        mode = argslist[2]
        step = argslist[3]
    except IndexError as e:
        pass
    num = int(num)
    maxnum = int(maxnum)
    step = int(step)
    mode = int(mode)
    valueTemp = value
    valueList = []
    if mode == 4:
        mode = 0
    elif mode == 3:
        mode = 1
    elif mode == 2:
        mode = 2
    elif mode == 1:
        mode = 3
    for i in range(1, int(maxnum) + 1):
        valueList.append(value)
        valueInt = socket.ntohl(struct.unpack("I", socket.inet_aton(value))[0])
        valueInt += (256 ** mode) * step
        value = socket.inet_ntoa(struct.pack('I', socket.htonl(valueInt)))
        if i % num == 0:
            value = valueTemp
    return valueList


def setIncrIpv6List(args, maxnum):
    """
    创建ipv6递增列表
    :param args:
    :param maxnum:
    :return:
    """
    ipv6addr = ''
    num = 0
    network = 8
    step = 1
    argslist = args.split(',')
    try:
        ipv6addr = argslist[0]
        num = argslist[1]
        network = argslist[2]
        step = argslist[3]
    except IndexError as e:
        pass
    
    sep = ":"
    maxnum = int(maxnum)
    step = int(step)
    network = int(network)
    num = int(num) - 1
    a = ipv6addr.split(sep)
    num1 = len(a)
    num2 = a.count("")
    num3 = 8 - num1 + num2
    if num2 == 1:
        index = a.index("")
        i = 1
        while i < num3 + 1:
            a.insert(index + i, "0")
            i += 1
        del a[index]
    ipv6list = [sep.join(a)]
    temp1 = sep.join(a)
    duan = network - 1
    tmp = temp2 = int(a[duan], 16)
    j = 1
    while j < maxnum:
        tmp += step
        a[duan] = "%X" % tmp
        ipv6list.append(sep.join(a))
        if (j % num == 0) & (maxnum - j > 1):
            tmp = temp2
            ipv6list.append(temp1)
            maxnum = maxnum - 1
        j += 1
    return ipv6list


def setIncrNumList(args, maxnum):
    """
    创建整形递增列表
    :param args:
    :param maxnum:
    :return:
    """
    value = 0
    num = 0
    step = 1
    argslist = args.split(',')
    try:
        value = argslist[0]
        num = argslist[1]
        step = int(argslist[2])
    except IndexError as e:
        pass
    value = int(value)
    num = int(num)
    maxnum = int(maxnum)
    valueTemp = value
    valueList = []
    for i in range(1, int(maxnum) + 1):
        valueList.append(value)
        value += step
        if i % num == 0:
            value = valueTemp
    return valueList


def createPy(sut, repeat, data):
    """
    快速生成脚本主函数
    :param sut:
    :param repeat:
    :param data:
    :return:
    """
    newline = ''
    newdata = ''
    sep = ','
    count = 0
    maxIncrNum = 1
    res = ''
    incrPoint = []
    incrPointList = []
    buf = re.findall('<([0-9a-f.:,]+)>', data)
    # 找到maxNum，并用%s替换<.*>
    for i in buf:
        arglist = i.split(',')
        data = re.sub('<' + i + '>', '%s', data, 1)
        if maxIncrNum < int(arglist[1]):
            maxIncrNum = int(arglist[1])
            
            # 将每一个递增数组算出
    for j in range(0, len(buf)):
        temp_str = buf[j]
        temp_list = temp_str.split(',')
        if re.search('\.', temp_list[0]):
            incrPoint = setIncrIpList(temp_str, maxIncrNum)
        elif re.search(':', temp_list[0]):
            incrPoint = setIncrIpv6List(temp_str, maxIncrNum)
        elif re.search('-', temp_list[0]):
            incrPoint = setIncrMacList(temp_str, maxIncrNum)
        else:
            incrPoint = setIncrNumList(temp_str, maxIncrNum)
        
        incrPointList.append(incrPoint)
    res = 'from dreceiver import *\n'
    res += 'incrList=' + str(incrPointList) + '\n'
    res += 'for repeat in range(0,%s):\n' % str(repeat)
    # 按行遍历数据，将变量插入字符串
    subres = '    for count in range(0,' + str(maxIncrNum) + '):\n'
    res += subres
    datalist = data.split('\n')
    for k in range(0, len(datalist)):
        addline = []
        
        temp, times = re.subn('%s', '%s', datalist[k])
        if times == 0:
            newline = '\'' + datalist[k] + '\''
        else:
            for p in range(0, times):
                addline.append('incrList[' + str(count) + '][count]')
                addlinestr = sep.join(addline)
                newline = '\'' + datalist[k] + '\'' + '%(' + addlinestr + ')'
                count += 1
        # print '        Receiver('+'\''+sut+'\','+newline +',1)'
        subres = '        Receiver(' + '\'' + sut + '\',' + newline + ',1)\n'
        res += subres
    return res


# 对话框
def openCreateDialog():
    from .quickCreateDialog import QuickCreateDialog
    dlg = QuickCreateDialog(None, -1, "Create and Show a custom Dialog")
    val = dlg.ShowModal()
    
    if val == wx.ID_OK:
        print('OK!')
        dlg.Destroy()
