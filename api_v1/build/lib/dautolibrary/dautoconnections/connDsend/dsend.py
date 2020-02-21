# -*- coding: UTF-8 -*-
# *********************************************************************
# dsend.py - python调用发包工具底层接口
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
#     - 2011.12.2  modified by zhaohj 增加无线发包工具II期功能的相关函数：DrouteWireless,DrdpcapWireless
#     - 2011.11.4  modified by zhaohj 增加无线发包工具的相关函数：DsendWireless，DcaptureWireless，DassociateWireless
#     - 2011.8.31  modified by caisy
#
# *********************************************************************
import getopt
import sys
import time
from pickle import loads

import rpyc
import wx
from dautolibrary.dautocomponents.dstyle import LoadReceiverDebugConfig

__all__ = ['CONN', 'ControlWindowsPC', 'DassociateWireless', 'Dcapture', 'DcaptureWireless', 'Dconn', 'Ddisconn',
           'DrdpcapWireless', 'DrouteWireless', 'Dsend', 'DsendWireless', 'Dshow', 'LoadReceiverDebugConfig', 'Pause',
           'SERVER_IP', 'SERVER_PORT']

CONN = None
SERVER_IP = ''
SERVER_PORT = None


def Dconn(server_ip, server_portid):
    global CONN
    global SERVER_IP
    global SERVER_PORT
    SERVER_IP = server_ip
    SERVER_PORT = int(server_portid)
    try:
        CONN = rpyc.connect(server_ip, int(server_portid))
    except IOError as ex:
        print(ex)
        return 'Could not connect to server,please check host IP and PID.'
    return 0


def Ddisconn():
    global CONN
    try:
        CONN.close()
    except (IOError, AttributeError) as ex:
        return 'ERROR:Could not connect to server,please check host IP and PID,or run "Dconn" to init connection.'
    return 0


def Dsend(argstr):
    debug = LoadReceiverDebugConfig()
    if debug:
        Pause()
    global CONN
    global SERVER_IP
    global SERVER_PORT
    proc = ''
    port = ''
    buf = argstr.split()
    opts, args = getopt.getopt(buf, "h",
                               ["help", "proc=", "port=", "stream=", "rate=", "mode=", "streamMode=", "streamSize=",
                                "lastStreamFlag=", "count=", "countContinue=", "incrMac1=", "incrMac2=", "incrMac3=",
                                "incrIp1=", "incrIp2=", "incrIp3=", "incrIp4=", "incrIp5=", "incrIp6=", "incrIp7=",
                                "incrIp8=", "incrIp9=", "incrIp11=", "incrIp12=", "incrIp3=", "incrIpv61=",
                                "incrIpv62=", "incrIpv63=", "incrNum1=", "incrNum2=", "incrNum3=", "acl="])
    args = []
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("--proc"):
            proc = a
        elif o in ("-p", "--port"):
            port = a
        elif o in ("-s", "--stream"):
            args.append(['stream', a])
        elif o in ("-m", "--mode"):
            args.append(['mode', a])
        elif o in ("-r", "--rate"):
            args.append(['rate', a])
        elif o in ("-l", "--lastStreamFlag"):
            args.append(['lastStreamFlag', a])
        elif o in ("-c", "--count"):
            args.append(['count', a])
        elif o in "--countContinue":
            args.append(['countContinue', a])
        elif o in "--streamMode":
            args.append(['streamMode', '\'' + str(a) + '\''])
        elif o in "--streamSize":
            args.append(['streamSize', '\'' + str(a) + '\''])
        elif o in "--incrMac1":
            args.append(['incrMac1', '\'' + str(a) + '\''])
        elif o in "--incrMac2":
            args.append(['incrMac2', '\'' + str(a) + '\''])
        elif o in "--incrMac3":
            args.append(['incrMac3', '\'' + str(a) + '\''])
        elif o in "--incrIp1":
            args.append(['incrIp1', '\'' + str(a) + '\''])
        elif o in "--incrIp2":
            args.append(['incrIp2', '\'' + str(a) + '\''])
        elif o in "--incrIp3":
            args.append(['incrIp3', '\'' + str(a) + '\''])
        elif o in '--incrIpv61':
            args.append(['incrIpv61', '\'' + str(a) + '\''])
        elif o in '--incrIpv62':
            args.append(['incrIpv62', '\'' + str(a) + '\''])
        elif o in "--incrIpv63":
            args.append(['incrIpv63', '\'' + str(a) + '\''])
        elif o in "--incrNum1":
            args.append(['incrNum1', '\'' + str(a) + '\''])
        elif o in "--incrNum2":
            args.append(['incrNum2', '\'' + str(a) + '\''])
        elif o in "--incrNum3":
            args.append(['incrNum3', '\'' + str(a) + '\''])
        elif o in "--acl":
            args.append(['acl', a])
    
    intRetry = 0
    while intRetry < 100:
        try:
            if intRetry > 0:
                CONN = rpyc.connect(SERVER_IP, SERVER_PORT)
            result = loads(CONN.root.handle(proc, port, args))
            return result
        except Exception as e:
            # return 'ERROR:Could not connect to server,please check host IP and PID,or run "Dconn" to init connection.'
            if str(e) == "connection closed by peer":
                CONN.close()
                return 0
            print('Traffic Jam occur!!!!!  Reconnect  in 5s\n')
            print(str(e))
            # CONN.close()
            time.sleep(5)
            if intRetry >= 9:
                return 'Reconnect ' + str(intRetry) + ' times FAILED !!! This may due to physical link down.'
            intRetry += 1


def Dshow(argstr):
    debug = LoadReceiverDebugConfig()
    if debug:
        Pause()
    global CONN
    port = ''
    datatype = ''
    buf = argstr.split()
    opts, args = getopt.getopt(buf, "h", ["help", "port=", "type=", "speed=", "mode="])
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-p", "--port"):
            port = a
        elif o in ("-t", "--type"):
            datatype = a
    intRetry = 0
    while intRetry < 100:
        try:
            if intRetry > 0:
                CONN = rpyc.connect(SERVER_IP, SERVER_PORT)
            
            async_function = rpyc.async_(CONN.root.getRate)
            speed = async_function(port, datatype)
            time.sleep(0.5)
            if speed.ready:
                return speed.value
            else:
                return 'I am so sorry!'
        except Exception as e:
            # return 'ERROR:Could not connect to server,please check host IP and PID,or run "Dconn" to init connection.'
            print('Traffic Jam occur!!!!!  Reconnect  in 5s\n')
            print(str(e))
            # CONN.close()
            time.sleep(5)
            if intRetry >= 9:
                return 'Reconnect ' + str(intRetry) + ' times FAILED !!! This may due to physical link down.'
            intRetry += 1


def Dcapture(argstr):
    debug = LoadReceiverDebugConfig()
    if debug:
        Pause()
    global CONN
    proc = ''
    port = ''
    buf = argstr.split()
    opts, args = getopt.getopt(buf, "h", ["help", "proc=", "port=", "fid=", "capFilter="])
    fid = '0'
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in "--proc":
            proc = str(a)
        elif o in ("-p", "--port"):
            port = str(a)
        elif o in ("-f", "--fid"):
            fid = str(a)
        elif o in "--capFilter":
            fid = str(a)
    
    intRetry = 0
    while intRetry < 100:
        try:
            if intRetry > 0:
                CONN = rpyc.connect(SERVER_IP, SERVER_PORT)
            result = loads(CONN.root.handle(proc, port, fid))
            return result
        except Exception as e:
            # return 'ERROR:Could not connect to server,please check host IP and PID,or run "Dconn" to init connection.'
            print('Traffic Jam occur!!!!!  Reconnect  in 5s\n')
            print(str(e))
            # CONN.close()
            time.sleep(5)
            if intRetry >= 9:
                return 'Reconnect ' + str(intRetry) + ' times FAILED !!! This may due to physical link down.'
            intRetry += 1


# added by zhaohj,2011-11-4
def DsendWireless(argstr):
    debug = LoadReceiverDebugConfig()
    if debug:
        Pause()
    global CONN
    proc = ''
    port = ''
    buf = argstr.split()
    args = []
    opts, args = getopt.getopt(buf, "h", ["help", "proc=", "port=", "port1config=", "port2config=", "port3config=",
                                          "port4config=", "port5config=", "port6config=", "stream=", "rate=",
                                          "streamMode=", "streamSize=", "lastStreamFlag=", "count=", "countContinue=",
                                          "incrMac1=", "incrMac2=", "incrMac3=", "incrIp1=", "incrIp2=", "incrIp3=",
                                          "incrIpv61=", "incrIpv62=", "incrIpv63=", "incrNum1=", "incrNum2=",
                                          "incrNum3="])
    args = []
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in "--proc":
            proc = a
        elif o in ("-p", "--port"):
            port = a
        elif o in "--port1config":
            args.append(['port1config', a])
        elif o in "--port2config":
            args.append(['port2config', a])
        elif o in ("--port3config"):
            args.append(['port3config', a])
        elif o in ("--port4config"):
            args.append(['port4config', a])
        elif o in ("--port5config"):
            args.append(['port5config', a])
        elif o in ("--port6config"):
            args.append(['port6config', a])
        elif o in ("-s", "--stream"):
            args.append(['stream', a])
            # elif o in ("-m", "--mode"):
            # args.append(['mode',a])
        elif o in ("-r", "--rate"):
            args.append(['rate', a])
        elif o in ("-l", "--lastStreamFlag"):
            args.append(['lastStreamFlag', a])
        elif o in ("-c", "--count"):
            args.append(['count', a])
        elif o in ("--countContinue"):
            args.append(['countContinue', a])
        elif o in ("--streamMode"):
            args.append(['streamMode', '\'' + str(a) + '\''])
        elif o in ("--streamSize"):
            args.append(['streamSize', '\'' + str(a) + '\''])
        elif o in ("--incrMac1"):
            args.append(['incrMac1', '\'' + str(a) + '\''])
        elif o in ("--incrMac2"):
            args.append(['incrMac2', '\'' + str(a) + '\''])
        elif o in ("--incrMac3"):
            args.append(['incrMac3', '\'' + str(a) + '\''])
        elif o in ("--incrIp1"):
            args.append(['incrIp1', '\'' + str(a) + '\''])
        elif o in ("--incrIp2"):
            args.append(['incrIp2', '\'' + str(a) + '\''])
        elif o in ("--incrIp3"):
            args.append(['incrIp3', '\'' + str(a) + '\''])
        elif o in ("--incrIpv61"):
            args.append(['incrIpv61', '\'' + str(a) + '\''])
        elif o in ("--incrIpv62"):
            args.append(['incrIpv62', '\'' + str(a) + '\''])
        elif o in ("--incrIpv63"):
            args.append(['incrIpv63', '\'' + str(a) + '\''])
        elif o in ("--incrNum1"):
            args.append(['incrNum1', '\'' + str(a) + '\''])
        elif o in ("--incrNum2"):
            args.append(['incrNum2', '\'' + str(a) + '\''])
        elif o in ("--incrNum3"):
            args.append(['incrNum3', '\'' + str(a) + '\''])
    try:
        result = loads(CONN.root.handle(proc, port, args))
    except (IOError, AttributeError) as ex:
        print('ERROR: {err_msg}'.format(err_msg=ex))
        return 'ERROR:Could not connect to server,please check host IP and PID,or run "Dconn" to init connection.'
    return result


def DcaptureWireless(argstr):
    debug = LoadReceiverDebugConfig()
    if debug:
        Pause()
    global CONN
    proc = ''
    port = ''
    buf = argstr.split()
    opts, args = getopt.getopt(buf, "h", ["help", "proc=", "port=", "port1config=", "port2config=", "port3config=",
                                          "port4config=", "port5config=", "port6config=", "fid=", "filter=", ])
    args = []
    # fid='0'
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("--proc"):
            proc = str(a)
        elif o in ("-p", "--port"):
            port = str(a)
        elif o in ("--port1config"):
            args.append(['port1config', a])
        elif o in ("--port2config"):
            args.append(['port2config', a])
        elif o in ("--port3config"):
            args.append(['port3config', a])
        elif o in ("--port4config"):
            args.append(['port4config', a])
        elif o in ("--port5config"):
            args.append(['port5config', a])
        elif o in ("--port6config"):
            args.append(['port6config', a])
        elif o in ("--fid"):
            args.append(['fid', str(a)])
        elif o in ("--filter"):
            args.append(['filter', a])
            # args.append(['filter','\''+str(a)+'\''])
    try:
        result = loads(CONN.root.handle(proc, port, args))
    
    except (IOError, AttributeError) as ex:
        return 'ERROR:Could not connect to server,please check host IP and PID,or run "Dconn" to init connection.'
    return result


def DassociateWireless(argstr):
    debug = LoadReceiverDebugConfig()
    if debug:
        Pause()
    global CONN
    proc = ''
    port = ''
    buf = argstr.split()
    opts, args = getopt.getopt(buf, "h", ["help", "proc=", "port=", "essid="])
    args = []
    essid = '0'
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("--proc"):
            proc = str(a)
        elif o in ("-p", "--port"):
            port = str(a)
        elif o in ("-e", "--essid"):
            essid = str(a)
    try:
        result = loads(CONN.root.handle(proc, port, essid))
    
    except (IOError, AttributeError) as ex:
        return 'ERROR:Could not connect to server,please check host IP and PID,or run "Dconn" to init connection.'
    return result


# added by zhaohj end

# added by zhaohj,2011-11-23
def DrouteWireless(argstr):
    debug = LoadReceiverDebugConfig()
    if debug:
        Pause()
    global CONN
    proc = ''
    port = ''
    buf = argstr.split()
    opts, args = getopt.getopt(buf, "h", ["help", "proc=", "port=", "net=", "gateway=", ])
    args = []
    # fid='0'
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("--proc"):
            proc = str(a)
        elif o in ("-p", "--port"):
            port = str(a)
        elif o in ("--net"):
            args.append(['net', str(a)])
        elif o in ("--gateway"):
            args.append(['gateway', str(a)])
    try:
        result = loads(CONN.root.handle(proc, port, args))
    except (IOError, AttributeError) as ex:
        return 'ERROR:Could not connect to server,please check host IP and PID,or run "Dconn" to init connection.'
    return result


# added by zhaohj,2011-11-25
def DrdpcapWireless(argstr):
    debug = LoadReceiverDebugConfig()
    if debug:
        Pause()
    global CONN
    proc = ''
    port = ''
    buf = argstr.split()
    opts, args = getopt.getopt(buf, "h",
                               ["help", "proc=", "filename=", "pktnum=", "initnum1=", "finalnum1=", "replacevalue1=",
                                "initnum2=", "finalnum2=", "replacevalue2=", ])
    args = []
    # fid='0'
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("--proc"):
            proc = str(a)
        elif o in ("--filename"):
            port = str(a)
        elif o in ("--pktnum"):
            args.append(['pktnum', str(a)])
        elif o in ("--initnum1"):
            args.append(['initnum1', str(a)])
        elif o in ("--finalnum1"):
            args.append(['finalnum1', str(a)])
        elif o in ("--replacevalue1"):
            args.append(['replacevalue1', str(a)])
        elif o in ("--initnum2"):
            args.append(['initnum2', str(a)])
        elif o in ("--finalnum2"):
            args.append(['finalnum2', str(a)])
        elif o in ("--replacevalue2"):
            args.append(['replacevalue2', str(a)])
    try:
        result = loads(CONN.root.handlepcap(proc, port, args))
    except (IOError, AttributeError) as ex:
        return 'ERROR:Could not connect to server,please check host IP and PID,or run "Dconn" to init connection.'
    return result


def Pause():
    window = wx.FindWindowByName('Main')
    window.PauseTestAuto()


def ControlWindowsPC(ip, command):
    try:
        # print command
        c = rpyc.classic.connect(ip)
        result = c.modules.os.popen(command).read()
        c.close()
        return result
    except IOError as ex:
        print('ERROR:', ex)
        return 'Could not connect to server,please check host IP.'
