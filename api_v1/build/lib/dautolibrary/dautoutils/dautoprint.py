#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# *********************************************************************
# Software : PyCharm
#
# __init__.py - 
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
#       - 2018/4/13 12:51  add by yanwh
#
# *********************************************************************


import datetime
import json
import time

# from wx import wx
import wx
from dautolibrary.dautocomponents.dstyle import LoadErrorStopConfig
from dtestlink.dcntestlink.dcntestlinkutils import recover_args
from dutils.dcnftp import DcnCommonFtp, DcnTestlinkFtp
from dutils.dcnlogs.dcnuserlog import close_logger, DcnLog
from dutils.dcnprint import printFormat, printAll, printRes, printResWarn, printResDebug, printResError

TESTNAME = ''
FAILLIT = []
TOTALFAILLIST = []
TIMERLIST = []
LOGGER = None
STARTTIME = None
TOTALSTARTTIME = datetime.datetime.now()
RERUNSTARTTEME = None
ENDTIME = None
TOTALENDTIME = None
RERUNENDTIME = None
TESTNUM = 0
tempTESTNUM = 0
TOTALTESTNUM = 0
RERUNTESTNUM = 0
tempTOTALTESTNUM = 0
FILEDSTEPLIST = []
TESTID = ''


def printGlobal(title, switch, msg='', logprefix=''):
    """
    方案脚本控制-开始计时/结束计时，统计执行信息
    说明：此处的函数实现不合理，但是为了兼容原有的实现方式不得已保留，后续可对此进行重构
    :param title: s1 s2
    :param switch:控制start stop end tlend
    :param msg: 打印的信息
    :param logprefix: 日志前缀
    :return: None
    """
    global TESTNAME
    global TESTNUM
    global tempTESTNUM
    global TOTALTESTNUM
    global tempTOTALTESTNUM
    global RERUNTESTNUM
    global FAILLIST
    global TOTALFAILLIST
    global STARTTIME
    global TOTALSTARTTIME
    global RERUNSTARTTEME
    global ENDTIME
    global TOTALENDTIME
    global RERUNENDTIME
    global TESTID
    
    TESTNAME = title
    thistime = datetime.datetime.now()
    mainWin = wx.FindWindowById(10)
    affirm_tl_operate = mainWin.tl  # 获取跟testlink服务器交互句柄
    if (switch == 'start') or (switch == 'Start'):
        TESTID = time.strftime("%Y%m%d", time.localtime()) + str(int(time.time()))
        mainWin.dbInfo['id'] = TESTID
        STARTTIME = thistime
        TESTNUM = 0
        FAILLIST = []
        res = printFormat(title + ' ' + switch + ' ' + str(thistime), msg)
        # 开始记录console的log
        if mainWin.logger:
            mainWin.logger = close_logger(mainWin.logger)
        mainWin.logger = DcnLog(log_base_path=mainWin.log_base_path,
                                log_define_type='run',
                                prefix_log_name=logprefix,
                                console_name='console',
                                test_name=TESTNAME).create_log()
        printAll(res)
    elif (switch == 'Rerunstart') or (switch == 'RerunStart'):
        TESTID = time.strftime("%Y%m%d", time.localtime()) + str(int(time.time()))
        mainWin.dbInfo['id'] = TESTID
        RERUNSTARTTEME = thistime
        RERUNTESTNUM = 0
        tempTESTNUM = TESTNUM
        tempTOTALTESTNUM = TOTALTESTNUM
        FAILLIST = []
        res = printFormat(title + ' ' + switch + ' ' + str(thistime), msg)
        printAll(res)
        if mainWin.logger:
            mainWin.logger = close_logger(mainWin.logger)
        mainWin.logger = DcnLog(log_base_path=mainWin.log_base_path,
                                log_define_type='run',
                                prefix_log_name=logprefix + '[ReRun]',
                                console_name='console',
                                test_name=TESTNAME).create_log()
    elif (switch == 'end') or (switch == 'End'):
        ENDTIME = thistime
        duration = timediff(STARTTIME, ENDTIME)
        res = printFormat(title + ' ' + switch + ' ' + str(thistime), 'TestCase Duration Time:' + duration)
        printAll(res)
        res_str = 'AutoTest Name :' + TESTNAME + '\n' + 'Start Time :' + str(STARTTIME) + '\n' + 'End Time   :' + str(
            ENDTIME) + '\n' + 'Duration Time :' + str(duration)
        failnum = len(FAILLIST)
        printAll(res_str)
        printAll('TestCase : Total ' + str(TESTNUM) + '\n           Pass  ' + str(
            TESTNUM - failnum) + '\n           Fail  ' + str(failnum))
        if failnum > 0:
            printstr = ''
            printAll('Failed TestCase :')
            for j in FAILLIST:
                printstr += str(j) + '\n'
            printAll(printstr)
        
        printAll('')
        mainWin.dbInfo['totalcases'] = str(TESTNUM)
        mainWin.dbInfo['passed'] = str(TESTNUM - failnum)
        mainWin.dbInfo['failed'] = str(failnum)
        mainWin.dbInfo['knownbugs'] = 'Not available'
        mainWin.dbInfo['unknowbugs'] = 'Not available'
        mainWin.dbInfo['failsummary'] = str(FAILLIST)
        mainWin.dbInfo['suggestions'] = 'Not available'
        mainWin.dbInfo['starttime'] = str(STARTTIME)
        mainWin.dbInfo['stoptime'] = str(ENDTIME)
        mainWin.dbInfo['totaltime'] = str(duration)
        
        time.sleep(3)
        printRes(res_str)
        printRes('TestCase : Total ' + str(TESTNUM) + '\n           Pass  ' + str(
            TESTNUM - failnum) + '\n           Fail  ' + str(failnum))
        if failnum > 0:
            printstr = ''
            printResWarn('Failed TestCase :')
            for j in FAILLIST:
                printstr += str(j) + '\n'
            printResWarn(printstr)
    elif (switch == 'Rerunend') or (switch == 'RerunEnd'):
        TESTNUM = tempTESTNUM
        TOTALTESTNUM = tempTOTALTESTNUM
        RERUNENDTIME = thistime
        TOTALFAILLIST.extend(FAILLIST)
        printRes('TOTALFAILLIST={}'.format(TOTALFAILLIST))
        duration = timediff(RERUNSTARTTEME, RERUNENDTIME)
        res = printFormat(title + ' ' + switch + ' ' + str(thistime), 'TestCase Duration Time:' + duration)
        printAll(res)
        res_str = 'AutoTest Name :' + TESTNAME + '\n' + 'Start Time :' + str(
            RERUNSTARTTEME) + '\n' + 'End Time   :' + str(RERUNENDTIME) + '\n' + 'Duration Time :' + str(duration)
        failnum = len(FAILLIST)
        printAll(res_str)
        printAll('TestCase : Total ' + str(RERUNTESTNUM) + '\n           Pass  ' + str(
            RERUNTESTNUM - failnum) + '\n           Fail  ' + str(failnum))
        if failnum > 0:
            printstr = ''
            printAll('Failed TestCase :')
            for j in FAILLIST:
                printstr += str(j) + '\n'
            printAll(printstr)
        duration = timediff(STARTTIME, RERUNENDTIME)
        res = printFormat(title + ' ' + switch + ' ' + str(thistime), 'TestCase Duration Time:' + duration)
        printAll(res)
        res_str = 'AutoTest Name :' + TESTNAME + '\n' + 'Start Time :' + str(STARTTIME) + '\n' + 'End Time   :' + str(
            RERUNENDTIME) + '\n' + 'Duration Time :' + str(duration)
        printAll(res_str)
        printAll('TestCase : Total ' + str(TESTNUM) + '\n           Pass  ' + str(
            TESTNUM - failnum) + '\n           Fail  ' + str(failnum))
        if failnum > 0:
            printstr = ''
            printAll('Failed TestCase :')
            for j in FAILLIST:
                printstr += str(j) + '\n'
            printAll(printstr)
        printAll('')
        mainWin.dbInfo['totalcases'] = str(TESTNUM)
        mainWin.dbInfo['passed'] = str(TESTNUM - failnum)
        mainWin.dbInfo['failed'] = str(failnum)
        mainWin.dbInfo['knownbugs'] = 'Not available'
        mainWin.dbInfo['unknowbugs'] = 'Not available'
        mainWin.dbInfo['failsummary'] = str(FAILLIST)
        mainWin.dbInfo['suggestions'] = 'Not available'
        mainWin.dbInfo['starttime'] = str(STARTTIME)
        mainWin.dbInfo['stoptime'] = str(ENDTIME)
        mainWin.dbInfo['totaltime'] = str(duration)
        time.sleep(3)
        printRes(res_str)
        printRes('TestCase : Total ' + str(TESTNUM) + '\n           Pass  ' + str(
            TESTNUM - failnum) + '\n           Fail  ' + str(failnum))
        if failnum > 0:
            printstr = ''
            printResWarn('Failed TestCase :')
            for j in FAILLIST:
                printstr += str(j) + '\n'
            printResWarn(printstr)
    elif switch == 'TlEnd':
        if mainWin.logger:
            mainWin.logger = close_logger(mainWin.logger)
        mainWin.logger = DcnLog(log_base_path=mainWin.log_base_path,
                                log_define_type='run',
                                prefix_log_name=logprefix,
                                console_name='summary',
                                test_name=TESTNAME).create_log()  # 创建一个汇总结果的日志文件summary
        printRes('TOTALFAILLIST{}'.format(TOTALFAILLIST))
        TOTALENDTIME = thistime
        duration = timediff(TOTALSTARTTIME, TOTALENDTIME)
        res = printFormat(title + ' ' + switch + ' ' + str(thistime), 'TestCase Duration Time:' + duration)
        printAll(res)
        res_str = 'AutoTest Name :' + TESTNAME + '\n' + 'Start Time :' + str(
            TOTALSTARTTIME) + '\n' + 'End Time   :' + str(TOTALENDTIME) + '\n' + 'Duration Time :' + str(duration)
        failnum = len(TOTALFAILLIST)
        printAll(res_str)
        printAll('TestCase : Total ' + str(TOTALTESTNUM) + '\n           Pass  ' + str(
            TOTALTESTNUM - failnum) + '\n           Fail  ' + str(failnum))
        if failnum > 0:
            printstr = ''
            printAll('Failed TestCase :')
            for j in TOTALFAILLIST:
                printstr += str(j) + '\n'
            printAll(printstr)
        DcnCommonFtp(ftp_config=mainWin.ftp_config_file).upload(
            mainWin.logfiles)  # 日志上传到用户指定服务器，指定服务器配置在config/ftpconfig.json
        try:
            if 'job_id' in affirm_tl_operate.tl.__args__ and mainWin.logger and mainWin.logfiles:
                printResDebug('\ntestlink args are:\n{arg}'.format(
                    arg=json.dumps(affirm_tl_operate.tl.__args__, ensure_ascii=False,
                                   indent=4, sort_keys=True)))
                DcnTestlinkFtp(affirm_tl_operate.tl.__args__, ip=mainWin.ftp_server_ip).upload(
                    mainWin.logfiles)  # 日志上传到testlink ftp服务器
                recover_args()  # testlink/args.py文件恢复初始状态
                affirm_tl_operate.set_waffirm_end()  # 关闭确认测试平台窗口
        except Exception as ex:
            printResError('error %s' % ex)
        TOTALTESTNUM = 0
        TOTALFAILLIST = []


def printTimer(title, switch, *msglist, **args):
    """
    测试例开始/结束计时
    :param title:s1 s2
    :param switch: start end流程控制
    :param msglist: msg
    :param args: other args
    :return:
    """
    global FILEDSTEPLIST
    global TIMERLIST
    global TESTNUM
    global FAILLIST
    global TOTALTESTNUM
    global TOTALFAILLIST
    global RERUNTESTNUM
    mainWin = wx.FindWindowById(10)
    affirm_tl_operate = mainWin.tl  # 获取跟testlink服务器交互句柄
    # result表示脚本执行的结果，默认是p(pass)，也可以取f(fail),无效测试例x(N/A)
    result = 'p'
    if 'suggestion' in args:
        suggestion = args['suggestion']
    else:
        suggestion = ''
    thistime = datetime.datetime.now()
    lasttime = None
    if (switch == 'start') or (switch == 'Start'):
        TIMERLIST.append([title, thistime])
        FILEDSTEPLIST = [TESTNAME[9:], title]
        res = printFormat(title + ' ' + switch + ' ' + str(thistime), *msglist)
        printAll(res)
    elif (switch == 'end') or (switch == 'End'):
        TESTNUM += 1
        TOTALTESTNUM += 1
        RERUNTESTNUM += 1
        if len(FILEDSTEPLIST) > 2:
            if len(suggestion) > 0:
                FILEDSTEPLIST.append(suggestion)
            FAILLIST.append(FILEDSTEPLIST)
            result = 'f'
        
        for i in TIMERLIST:
            for j in i:
                if j == title:
                    lasttime = i[1]
                    TIMERLIST.remove(i)
        duration = timediff(lasttime, thistime)
        res = printFormat(title + ' ' + switch + ' ' + str(thistime), 'TestCase Duration Time:' + duration)
        printAll(res)
        affirm_tl_operate.set_test_build()
        affirm_tl_operate.set_testcase_name_by_title(title)
        fail_step = '' if FILEDSTEPLIST[2:] == [] else str(FILEDSTEPLIST[2:]).replace('[', '').replace(']', '')
        affirm_tl_operate.update_testcase_result(result, fail_step)  # 如果测试用例有执行错误的步骤，传入错误的测试用例的错误步骤
    time.sleep(0.5)


def printInitialTimer(title, switch, msg=''):
    """
    初始化开始/结束计时
    :param title: s1 s2
    :param switch: start end
    :param msg: msg
    :return: None
    """
    global TIMERLIST
    thistime = datetime.datetime.now()
    if (switch == 'start') or (switch == 'Start'):
        TIMERLIST = [[title, thistime]]
        res = printFormat(title + ' ' + switch + ' ' + str(thistime), msg)
        printAll(res)
    
    elif (switch == 'end') or (switch == 'End'):
        for i in TIMERLIST:
            for j in i:
                if j == title:
                    TIMERLIST.remove(i)
        res = printFormat(title + ' ' + switch + ' ' + str(thistime))
        printAll(res)
    time.sleep(0.5)


def printUninitialTimer(title, switch, msg=''):
    """
    Uninitial开始/结束计时
    :param title: s1 s2
    :param switch: start end
    :param msg: msg
    :return: None
    """
    global TIMERLIST
    this_time = datetime.datetime.now()
    if (switch == 'start') or (switch == 'Start'):
        TIMERLIST.append([title, this_time])
        res = printFormat(title + ' ' + switch + ' ' + str(this_time), msg)
        printAll(res)
    elif (switch == 'end') or (switch == 'End'):
        for i in TIMERLIST:
            for j in i:
                if j == title:
                    TIMERLIST.remove(i)
        res = printFormat(title + ' ' + switch + ' ' + str(this_time))
        printAll(res)
    time.sleep(0.5)


def returnFailure():
    """
    返回错误测试例列表
    :return: None
    """
    global FAILLIST
    return FAILLIST


def printFailure():
    """
    打印错误测试例列表
    :return:None
    """
    global FAILLIST


# 计算时间差
def timediff(time_start, time_stop):
    """
    辅助函数，用于计算时间差
    :param timestart: start time
    :param timestop: stop time
    :return: 时间差值
    """
    t = (time_stop - time_start)
    time_day = t.days
    s_time = t.seconds
    ms_time = t.microseconds / 1000000
    used_time = int(s_time + ms_time)
    time_hour = used_time / 60 / 60
    time_minute = (used_time - time_hour * 3600) / 60
    time_second = used_time - time_hour * 3600 - time_minute * 60
    return "%dDay,%d:%d:%d(Hour:Min:Sec)" % (time_day, time_hour, time_minute, time_second)


def printCheckStep(test_name, step, *res_1):
    """
    检查测试例step对错，打印并记录
    :param test_name: test name
    :param step: 步骤 step 1 2
    :param res_1: other args
    :return: 0 or 1 success or fail
    """
    time.sleep(0.5)
    _res = 0
    global FILEDSTEPLIST
    for i in res_1:
        if i == 0:
            printRes('[res = ' + str(i) + ']Check res = 0,OK!')
        else:
            printResError('[res = ' + str(i) + ']Check res = 0,Failed!')
            _res = 1
    
    if _res == 1:
        FILEDSTEPLIST.append(step)
        if wx.FindWindowById(10).nowrunning not in wx.FindWindowById(10).faillist:
            if wx.FindWindowById(10).nowrunning != '':
                wx.FindWindowById(10).faillist.append(wx.FindWindowById(10).nowrunning)
        printResError(test_name + ' ' + step + ' is FAILED!')
        if LoadErrorStopConfig():
            def errorPause():
                """
                遇错暂停
                :return:
                """
                window = wx.FindWindowByName('Main')
                window.PauseTestAuto()
            
            errorPause()
    else:
        printRes(test_name + ' ' + step + ' is PASSED!')
    time.sleep(0.5)
    return _res


def printCheckStepDebug(test_name, step, *res_1):
    """
    # 检查测试例step对错，打印 如果fail则暂停脚本
    :param test_name: test name
    :param step: step 1 2
    :param res_1: other args
    :return: 0 or 1
    """
    time.sleep(0.5)
    _res = 0
    global FILEDSTEPLIST
    for i in res_1:
        if i == 0:
            printRes('[res = ' + str(i) + ']Check res = 0,OK!')
        else:
            printResError('[res = ' + str(i) + ']Check res = 0,Failed!')
            _res = 1
    
    if _res == 1:
        FILEDSTEPLIST.append(step)
        if wx.FindWindowById(10).nowrunning not in wx.FindWindowById(10).faillist:
            if wx.FindWindowById(10).nowrunning != '':
                wx.FindWindowById(10).faillist.append(wx.FindWindowById(10).nowrunning)
        printResError(test_name + ' ' + step + ' is FAILED!')
        wx.MessageBox('该Step不通过，已停止脚本保留现场')
        wx.FindWindowById(10).PauseTestAuto()
    else:
        printRes(test_name + ' ' + step + ' is PASSED!')
    time.sleep(0.5)
    return _res
