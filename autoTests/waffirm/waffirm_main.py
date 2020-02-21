# -*- coding: UTF-8 -*
# *********************************************************************
# waffirm_main.py - Main of Wireless Affirm
#
# Author:
#
# Version 1.0.0
#
# Copyright (c) 2004-9999 Digital China Networks Co. Ltd
#
#
# *********************************************************************
# Change log:
#     - 2017.12.21  modified by yanwh 修改了logger装饰器实现有序显示参数
#     - 2018.1.16 modified by yanwh 修复了上报ac版本的相关问题增加了json配置读写功能
# *********************************************************************
"""
main文件执行流程：
1、打开各设备串口
2、根据upgrade_device参数判断是否执行升级版本操作（upgrade_device定义在topu文件中）
3、动态获取设备版本、staMAC、ACvlanmac、APtype等信息
4、获取central24G、central5G、local24G、local5G参数，判断需要执行的测试用例
"""
import inspect
import os
import traceback
from collections import OrderedDict
from functools import wraps

from dcntestlibrary.dcnlibrary.lib_all import *
from dutils.dcnlogs.dcnuserlog import close_logger, DcnLog
try:
    from Dauto import log_base_path, log_config_file
except ImportError:
    pass
from .waffirm_config_run import *
from .waffirm_config_topu import *
from .waffirm_config_vars import *
from dautolibrary.dautoutils.dautoprint import printGlobal, printTimer, printCheckStep, printInitialTimer, \
    printUninitialTimer


# Function
def logger(flag=False):
    """
    :param flag:日志打印开关，默认为False,开启日志打印
    :return: 打印执行函数调用的参数内容，格式如下
    ----------Log Print Start----------
    param a  {'testSuite': 'waffirm', 'productLine'}
    param b 7.0.5.0(R0102.0026)
    param c 2.3.2.21
    param d 2017-12-12 17:58:57
    ...
    """
    if flag:
        def _logger(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                printRes('\n' + '-' * 25 + 'Log Print Start' + '-' * 25)
                _args_info = inspect.getcallargs(func, *args, **kwargs)
                _args_info = OrderedDict(sorted(_args_info.items(), key=lambda t: (t[0])))
                # 如果参数不为空，遍历参数
                if _args_info:
                    for names, values in _args_info.items():
                        para = values
                        # 如果参数是字典，表明函数通过**kwargs方式调用
                        if isinstance(para, dict):
                            # 更新原来的字典key为统一kwargs
                            _args_info['kwargs'] = _args_info.pop(names)
                            # 字典非空输出结果
                            if _args_info['kwargs']:
                                # 显示信息按照参数名字符大小进行排序（such as 'aa , ab, bc ,bd '）
                                para = OrderedDict(sorted(para.items(), key=lambda t: (t[0])))
                                for k, v in para.items():
                                    printRes('{0:10}'.format('').join(['{0:<5}'.format('param'),
                                                                       '{0:<15}'.format(str(k)),
                                                                       '{0:<50}'.format(v)]))
                                # 删除该键避免后面重复打印
                                _args_info.pop('kwargs')
                                continue
                            else:
                                # 字典为空，删除
                                _args_info.pop('kwargs')
                                continue
                        # 如果参数是tuple，表明函数通过*args方式调用
                        elif isinstance(para, tuple):
                            _args_info['args'] = _args_info.pop(names)
                            if _args_info['args']:
                                # 排序
                                para = sorted(para, key=lambda t: t[0])
                                for v in para:
                                    printRes('{0:10}'.format('').join(['{0:<5}'.format('param'),
                                                                       '{0:<15}'.format('args'),
                                                                       '{0:<50}'.format(v)]))
                                # 删除该键避免后面重复打印
                                _args_info.pop('args')
                                continue
                            else:
                                # tuple为空，删除
                                _args_info.pop('args')
                                continue
                        # 普通参数，判断强制转换成str类型输出
                        elif not isinstance(values, str):
                            # 额外处理testlink tl参数
                            if hasattr(values, '__args__'):
                                para = str(values.__args__) if isinstance(values.__args__, dict) else values.__args__
                            # 额外处理正则表达式
                            elif hasattr(values, 'group'):
                                para = values.group(1)
                            else:
                                try:
                                    para = str(values)
                                except TypeError:
                                    pass
                        printRes('{0:10}'.format('').join(['{0:<5}'.format('param'),
                                                           '{0:<15}'.format(str(names)),
                                                           '{0:<50}'.format(para)]))
                else:
                    printRes('Param Is None')
                printRes('-' * 25 + 'Log Print Ended' + '-' * 25)
                return func(*args, **kwargs)

            return wrapper
    else:
        def _logger(func):
            return func
    return _logger


def get_testcase_byuser(*args, **kargs):
    '''
    函数：根据用户输入的testcentral_24g=True等信息返回按照用户指定优先级排序的要执行模块字符串
    输入：testcentral_24g=True,testcentral_5g=False
    输出：函数返回一个列表，包含了用户选择为True的模块，并且该模块根据run文件中的xxx_Pri进行从小到大的排序
    用法：默认只需要调用函数get_testcase_byuser()即可返回对应列表，用户也可指定参数
    '''

    if not kargs:
        kargs = {'central24G': central24G,
                 'central5G': central5G,
                 'local24G': local24G,
                 'local5G': local5G
                 }
    l = [k for (k, v) in kargs.items() if v]
    kargs = {}
    for i in l:
        kargs.update({i: eval(i + '_pri')})
    return [k for (k, v) in sorted(kargs.items(), key=lambda x: x[1])]


def classify_testcase(Tlist):
    '''
    功能：根据用例名称对用例进行分类：
    名称后缀带_ALL代表集中转发、本地转发、2.4G、5G都需要执行；
    名称后缀带_ONE代表与集中转发、本地转发、2.4G、5G无关，此类用例在整个执行过程中只会执行一遍
    名称后缀带_CEN代表集中转发（包括2.4G和5G）需要执行；
    名称后缀带_LOC代表本地转发（包括2.4G和5G）需要执行；
    名称后缀带_24G代表2.4G需要执行（包括集中转发和本地转发）；
    名称后缀带_5G代表5G需要执行（包括集中转发和本地转发）；
    参数：Tlist，由所有测试例名称构成的测试列表，由run文件自动生成
    返回值：分类后的测试用例字典，key为类别，如ALL、ONE等，值为属于该类的测试用例列表   
    '''
    ret = {'ALL': [],
           'ONE': [],
           'CEN': [],
           'LOC': [],
           '24G': [],
           '5G': [],
           'C24G': [],
           'C5G': [],
           'L24G': [],
           'L5G': []}
    for testcase in Tlist:
        if '_ALL' in testcase[0]:
            ret['ALL'].append(testcase)
        elif '_ONE' in testcase[0]:
            ret['ONE'].append(testcase)
        elif '_CEN' in testcase[0]:
            ret['CEN'].append(testcase)
        elif '_LOC' in testcase[0]:
            ret['LOC'].append(testcase)
        elif '_24G' in testcase[0]:
            ret['24G'].append(testcase)
        elif '_5G' in testcase[0]:
            ret['5G'].append(testcase)
        elif '_C24G' in testcase[0]:
            ret['C24G'].append(testcase)
        elif '_C5G' in testcase[0]:
            ret['C5G'].append(testcase)
        elif '_L24G' in testcase[0]:
            ret['L24G'].append(testcase)
        elif '_L5G' in testcase[0]:
            ret['L5G'].append(testcase)
        else:
            ret['ALL'].append(testcase)
    return ret


def get_testlist(testcategory, order, Tdic):
    '''
    功能：根据当前执行的测试类别获取testlist列表，如当前执行集中转发2.4G测试，
    则会返回由名称带_ALL、_CEN、_24G、_C24G的所有测试例组成的列表
    参数：testcategory：代表当前测试类别的字符串
    order：当前测试类别的执行顺序，值为0、1、2、3
    Tdic：由classify_testcase函数获得的返回值
    返回值：该测试类别需要执行的所有测试用例组成的列表
    '''
    finaltestlist = []
    finaltestlist.extend(Tdic['ALL'])
    if order == 0:
        finaltestlist.extend(Tdic['ONE'])
    if 'central' in testcategory:
        finaltestlist.extend(Tdic['CEN'])
        if '24G' in testcategory:
            finaltestlist.extend(Tdic['24G'])
            finaltestlist.extend(Tdic['C24G'])
        if '5G' in testcategory:
            finaltestlist.extend(Tdic['5G'])
            finaltestlist.extend(Tdic['C5G'])
    if 'local' in testcategory:
        finaltestlist.extend(Tdic['LOC'])
        if '24G' in testcategory:
            finaltestlist.extend(Tdic['24G'])
            finaltestlist.extend(Tdic['L24G'])
        if '5G' in testcategory:
            finaltestlist.extend(Tdic['5G'])
            finaltestlist.extend(Tdic['L5G'])
    return finaltestlist


def create_mulconn(sutlist, prefix=''):
    for sut in sutlist:
        if sut == pc1:
            CreateNewConn(pc1_type, pc1, pc1_host, None, 'run', logprefix=prefix)
            TelnetLogin(pc1, Pc1_telnet_name, Pc1_telnet_password)
        elif sut == sta1:
            CreateNewConn(sta1_type, sta1, sta1_host, None, 'run', logprefix=prefix)
            TelnetLogin(sta1, Pc1_telnet_name, Pc1_telnet_password)
        elif sut == sta2:
            CreateNewConn(sta2_type, sta2, sta2_host, None, 'run', logprefix=prefix)
            TelnetLogin(sta2, Pc1_telnet_name, Pc1_telnet_password)
        elif sut == switch1:
            CreateNewConn(switch1_type, switch1, switch1_host, None, 'run', logprefix=prefix)
            SetTerminalLength(switch1)
        elif sut == switch2:
            CreateNewConn(switch2_type, switch2, switch2_host, None, 'run', logprefix=prefix)
            SetTerminalLength(switch2)
        elif sut == switch3:
            CreateNewConn(switch3_type, switch3, switch3_host, None, 'run', logprefix=prefix)
            SetTerminalLength(switch3)
        elif sut == ap1:
            CreateNewConn(ap1_type, ap1, ap1_host, None, 'run', logprefix=prefix)
            ApLogin(ap1)
        elif sut == ap2:
            CreateNewConn(ap2_type, ap2, ap2_host, None, 'run', logprefix=prefix)
            ApLogin(ap2)


def create_muliti_device_logs(sutlist, test_name, prefix=''):
    """
    给sutlist里面的设备根据指定test_name创建指定路径的日志
    :param sutlist: 设备列表
    :type sutlist: list
    :param test_name: test_case名称
    :type test_name: string
    :param log_list: 记录logger句柄的list，用户全局管理创建的日志
    :param prefix: 日志前缀
    :type prefix: string
    :return: None
    :rtype:
    """

    var = {pc1: pc1_host, sta1: sta1_host, sta2: sta2_host, switch1: switch1_host, switch2: switch2_host,
           switch3: switch3_host,
           ap1: ap1_host, ap2: ap2_host}

    for sut in sutlist:
        if sut in var.keys():
            dev = wx.FindWindowByName(sut)
            if dev.logger:
                dev.logger = close_logger(dev.logger)
                time.sleep(0.1)
            dev.logger = DcnLog(log_base_path=log_base_path, log_define_type='run', page_name=var[sut], title_name=sut,
                                prefix_log_name=prefix, test_name=test_name).create_log(log_config_file)


def update_device(flag):
    """
    :param flag: testlink上面是否执行升级的参数，如果为1执行升级否则不会升级设备，此处数值通过testlink页面传递给dcnrdc
                  dcndrc写入waffirm_config_topu.py然后waffrim_mian文件读取upgrade_device，默认值为0
    :return:
    """
    if flag:
        upgrade_s1boot = upgrade_s1img = upgrade_s2boot = upgrade_s2img = \
            upgrade_s3boot = upgrade_s3img = \
            upgrade_ap1img = upgrade_ap2img = 0
        print('\n' + '#' * 65 + '\n' + ' '.join(['#' * 15, 'Now searching all devices\'s files', '#' * 15]))
        IdleAfter(1)
        if os.path.isfile('c:\\version\\env' + EnvNo + '\\s1boot.rom'):
            upgrade_s1boot = 1
            print("############## AC1's boot file 's1boot.rom' founded #############")
        if os.path.isfile('c:\\version\\env' + EnvNo + '\\s1nos.img'):
            upgrade_s1img = 1
            print("############## AC1's img file 's1nos.img' founded ###############")
        if os.path.isfile('c:\\version\\env' + EnvNo + '\\s2boot.rom'):
            upgrade_s2boot = 1
            print("############## AC2's boot file 's2boot.rom' founded #############")
        if os.path.isfile('c:\\version\\env' + EnvNo + '\\s2nos.img'):
            upgrade_s2img = 1
            print("############## AC2's img file 's2nos.img' founded   #############")
        if os.path.isfile('c:\\version\\env' + EnvNo + '\\s3boot.rom'):
            upgrade_s3boot = 1
            print("############## S3's boot file 's3boot.rom' founded  #############")
        if os.path.isfile('c:\\version\\env' + EnvNo + '\\s3nos.img'):
            upgrade_s3img = 1
            print("############# S3's img file 's3nos.img' founded    #############")
        if os.path.isfile('c:\\version\\env' + EnvNo + '\\ap1.tar'):
            upgrade_ap1img = 1
            print("############# AP1's img file 'ap1.tar' founded     #############")
        if os.path.isfile('c:\\version\\env' + EnvNo + '\\ap2.tar'):
            upgrade_ap2img = 1
            print("############# AP2's img file 'ap2.tar' founded     #############")
        IdleAfter(5)
        print('#' * 65)
        execfile('waffirm_upgrade_device.py')


def login_device():
    """
    函数用来打开串口以及对PC STA 和AP进行登录
    :return: 登录成功返回1，失败0，同时记录调试log
    """
    # 连接PC1,STA1,STA2,方式为 Telnet
    CreateNewConn(pc1_type, pc1, pc1_host, None, 'default')
    pc_login_res = 0 if TelnetLogin(pc1, Pc1_telnet_name, Pc1_telnet_password) else 1
    CreateNewConn(sta1_type, sta1, sta1_host, None, 'default')
    sta1_login_res = 0 if TelnetLogin(sta1, Pc1_telnet_name, Pc1_telnet_password) else 1
    CreateNewConn(sta2_type, sta2, sta2_host, None, 'default')
    sta2_login_res = 0 if TelnetLogin(sta2, Pc1_telnet_name, Pc1_telnet_password) else 1
    # 连接 AC1,AC2,S3
    CreateNewConn(switch1_type, switch1, switch1_host, None, 'default')
    SetTerminalLength(switch1)
    CreateNewConn(switch2_type, switch2, switch2_host, None, 'default')
    SetTerminalLength(switch2)
    CreateNewConn(switch3_type, switch3, switch3_host, None, 'default')
    SetTerminalLength(switch3)
    # 连接AP1,AP2
    CreateNewConn(ap1_type, ap1, ap1_host, None, 'default')
    CreateNewConn(ap2_type, ap2, ap2_host, None, 'default')
    # 登录AP1,AP2 (第一次连接AP需要登录)
    ap1_login_res = 0 if ApLogin(ap1) else 1
    time.sleep(0.5)
    ap2_login_res = 0 if ApLogin(ap2) else 1

    @logger(True)
    def get_login_res(pc_res, sta1_res, sta2_res, ap1_res, ap2_res):
        """
        函数用来记录log，并且返回登录结果
        :param pc_res: 0 or 1
        :param sta1_res: 0 or 1
        :param sta2_res: 0 or 1
        :param ap1_res: 0 or 1
        :param ap2_res: 0 or 1
        :return: 0 or 1
        """
        if pc_res and sta1_res and sta2_res and ap1_res and ap2_res:
            printResDebug('[通知]所有设备全部登录成功')
            return 1
        else:
            printResWarn('[告警]有设备登录失败，请检查测试环境')
            return 0

    return get_login_res(pc_login_res, sta1_login_res, sta2_login_res, ap1_login_res, ap2_login_res)


def get_device_info(dut):
    """
    :param dut: 输入设备的标签名称
    :return: 根据标签名称返回对应的namedtuple类型，该tuple包含设备的版本信息，编译时间，type值，mac值等相关信息
    """
    from collections import namedtuple
    from re import search

    def _get_vlan_mac():
        EnterEnableMode(dut)
        EnterInterfaceMode(dut, 'vlan 1')
        _vlan_mac = GetVlanMac(dut)
        EnterConfigMode(dut)
        SetCmd(dut, 'no interface vlan 1')
        SetWatchdogDisable(dut)
        SetExecTimeout(dut)
        printRes('{device} vlan mac is {vlan_mac}'.format(device=dut, vlan_mac=_vlan_mac))
        return _vlan_mac if _vlan_mac else 'get vlan_mac failed by function GetVlanMac'

    if str(dut).startswith(('s1', 's2', 's3', 's4')):
        ac = namedtuple('ac', ['version', 'compile_time', 'type', 'vlan_mac', 'ac_notes'])
        EnterEnableMode(dut)
        ac_notes = SetCmd(dut, 'show version')
        _regular_res = search('Version ([^\n ]+)', ac_notes)
        version = _regular_res.group(1) if _regular_res else 'get version failed by function SetCmd'
        _regular_res = search(r'(?i)compile.*\s+on\s+(.*)', ac_notes)
        compile_time = _regular_res.group(1) if _regular_res else 'get compile time failed by regular'
        device_type = GetAcType(dut)
        vlan_mac = _get_vlan_mac()
        printRes('{device} version is {version}'.format(device=dut, version=version))
        printRes('{device} compile time is {compile_time}'.format(device=dut, compile_time=compile_time))
        return ac(version=version, compile_time=compile_time, type=device_type, vlan_mac=vlan_mac, ac_notes=ac_notes)
    elif str(dut).startswith('ap'):
        ap = namedtuple('ap', ['cmd_type', 'version', 'compile_time', 'type', 'ap_mac', 'ap_notes'])
        # 获取AP的命令类型，'set' or 'uci set
        cmd_type = Get_ap_cmdtype(dut)
        ap_notes = ApSetcmd(dut, cmd_type, 'getsystem', 'detail')
        _regular_res = search('version\s+([^\n ]+)', ap_notes)
        version = _regular_res.group(1) if _regular_res else 'get version failed by function ApSetcmd'
        _regular_res = search(r'#\d+\s+(.*)', SetCmd(dut, 'cat /proc/version'))
        compile_time = _regular_res.group(1) if _regular_res else 'get compile time failed by regular'
        _regular_res = search('(\d+)', ApSetcmd(dut, cmd_type, 'getsystem', 'device-type'))
        device_type = _regular_res.group(1) if _regular_res else 'get device type failed by regular'
        ap_mac = GetApMac(dut, cmd_type)
        printRes('{device} cmd type is {cmd_type}'.format(device=dut, cmd_type=cmd_type))
        printRes('{device} version is {version}'.format(device=dut, version=version))
        printRes('{device} compile time is {compile_time}'.format(device=dut, compile_time=compile_time))
        printRes('{device} mac is {ap_mac}'.format(device=dut, ap_mac=ap_mac))
        printRes('{device} type is {device_type}'.format(device=dut, device_type=device_type))
        return ap(cmd_type=cmd_type, version=version, compile_time=compile_time, type=device_type, ap_mac=ap_mac,
                  ap_notes=ap_notes)
    elif str(dut).startswith('sta'):
        # 构造sta的namedtuple，返回内容为mac三种格式[xx-xx-xx..,xx:xx:xx..,XX-XX-XX..]
        sta = namedtuple('sta', ['mac_with_colon', 'mac_with_dash', 'mac_with_dash_upper'])
        mac_with_dash = GetStaMac(dut)
        mac_with_colon = GetStaMac(dut, connectflag=':')
        mac_with_dash_upper = mac_with_dash.upper()
        printRes('{device} mac is {mac_with_dash}'.format(device=dut, mac_with_dash=mac_with_dash))
        return sta(mac_with_colon=mac_with_colon, mac_with_dash=mac_with_dash, mac_with_dash_upper=mac_with_dash_upper)


# --------------------------------此处添加需要打印的参数信息-------------------------------------------------------
def display_info():
    """要打印的参数信息"""
    _src_data_for_display = dict(
        zip(['script_start_time', 'ac1_version', 'ac1_type', 'ac1_vlan_mac', 'ac1_compile_time',
             'ac2_version', 'ac2_type', 'ac2_vlan_mac', 'ac2_compile_time', 'ap1_version',
             'ap1_type', 'ap1_mac', 'ap1_compile_time', 'ap1_command_type', 'ap2_version',
             'ap2_type', 'ap2_mac', 'ap2_compile_time', 'ap2_command_type', 'sta1_mac', 'sta2_mac',
             'testlink_info'],
            [run_time, ac1_info.version, ac1_info.type, ac1_info.vlan_mac, ac1_info.compile_time,
             ac2_info.version,
             ac2_info.type, ac2_info.vlan_mac, ac2_info.compile_time, ap1_info.version,
             ap1_info.type,
             ap1_info.ap_mac, ap1_info.compile_time, ap1_info.cmd_type, ap2_info.version,
             ap2_info.type,
             ap2_info.ap_mac, ap2_info.compile_time, ap2_info.cmd_type, sta1_info.mac_with_dash,
             sta2_info.mac_with_dash, affirm_tl_operate.tl]))

    @logger(flag=True)
    def display(**kwargs):
        if not kwargs:
            printResError('Argument is None')
        pass

    return display(**_src_data_for_display)


# ---------------------------------------------------------------------------------------
# -------------------------------------脚本执行入口---------------------------------------
# 跟testlink服务器交互句柄
affirm_tl_operate = wx.FindWindowById(10).tl
#  脚本开始执行时间

run_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

# 获取用户自定义的日志字符串，添加在log的文件名中
prefix_log = '' if not prefix_log.strip() else '[' + prefix_log + ']'
# ------------------------------------设备登录---------------------------------------------------
# 打开设备串口，进行设备登录，记录log， 登录成功返回1失败0
printResDebug('[通知]设备登录中，请耐心等待')
login_device()
# ------------------------------------初始化被测设备参数信息---------------------------------------------------
# 获取ac1 ac2 ap1 ap2参数
# ac = namedtuple('ac', ['version', 'compile_time', 'type', 'vlan_mac'])
# ap = namedtuple('ap', ['cmd_type', 'version', 'compile_time', 'type', 'ap_mac'])
# sta = namedtuple('sta', ['mac_with_colon','mac_with_dash','mac_with_colon_upper'])
printResDebug('[通知]获取测试设备(AC AP STA...)参数中，请耐心等待')
ac1_info = get_device_info(switch1)
ac2_info = get_device_info(switch2)
ap1_info = get_device_info(ap1)
ap2_info = get_device_info(ap2)
sta1_info = get_device_info(sta1)
sta2_info = get_device_info(sta2)
# ---------------------------------------------------------------------------------------
# 初始化确认测试用例执行运行参数（兼容之前命名的变量）
# 获取AP的命令类型，'set' or 'uci set'
# ---------------------------------------------------------------------------------------

s1vlanmac = ac1_info.vlan_mac
ac1type = ac1_info.type
ac2type = ac2_info.type
Ap1cmdtype = ap1_info.cmd_type
Ap2cmdtype = ap2_info.cmd_type
# 获取AP1参数
# ap1的type值,mac
hwtype1 = ap1_info.type
ap1maclist = ap1_info.ap_mac
ap1mac = ap1maclist['-']
# 获取AP2参数
# ap2的type值,mac
hwtype2 = ap2_info.type
ap2maclist = ap2_info.ap_mac
ap2mac = ap2maclist['-']
# 获得sta1 sta2的mac地址
# staxmac = xx-xx-xx-xx-xx-xx
# staxmac_type1 = xx:xx:xx:xx:xx:xx
# staxmac_upcase = XX-XX-XX-XX-XX-XX
sta1mac = sta1_info.mac_with_dash
sta1mac_type1 = sta1_info.mac_with_colon
sta1mac_upcase = sta1_info.mac_with_dash_upper
sta2mac = sta2_info.mac_with_dash
sta2mac_type1 = sta2_info.mac_with_colon
sta2mac_upcase = sta2_info.mac_with_dash_upper
# ---------------------------------------------------------------------------------------
# 根据upgrade_device判断是否进行升级操作
# ---------------------------------------------------------------------------------------
update_device(upgrade_device)
# ---------------------------------------------------------------------------------------
# 更新ap ac 版本 编译时间 脚本运行时间以及测试用例集参数至tl.__args__参数
# 用于后面testlink上面更新相关信息
# ---------------------------------------------------------------------------------------
printResDebug('[通知]更新设备信息到Testlink服务器')
affirm_tl_operate.update_waffirm_args(ac1_info.version, ac1_info.ac_notes, ap1_info.version, ap1_info.compile_time,
                                      ap1_info.ap_notes,
                                      run_time)
# ---------------------------------------------------------------------------------------
# 显示要执行的测试环境的信息，例如运行时间,ap的命令行类型，ac和ap的版本信息,testlink信息等
# ---------------------------------------------------------------------------------------
printResDebug('[通知]显示许多重要的环境变量参数')
display_info()
# -------------------------------判断需要执行的测试项目--------------------------------------
# 初始化测试用例执行的时候不同测试拓扑和环境下面生产不同的运行参数
# -----------------------------------------------------------------------------------------
printResDebug('[通知]初始化测试用例参数')
testcategory_list = get_testcase_byuser()
testdic = classify_testcase(testlist)
radio1num = '1'
macincrease, radio2num = (radio5G - 1) * 16, str(radio5G)

# 执行用例脚本   
passinitial, passunintial, newlog = False, False, False
temp_setdefault = set_default

# ----------------------------------用例执行-------------------------------------------------------

# def run_testcase():
for i in range(len(testcategory_list)):
    try:
        if 'local24G' in testcategory_list[i]:
            affirm_tl_operate.tl.__args__['wireless_tp'] = 1
        elif 'local5G' in testcategory_list[i]:
            affirm_tl_operate.tl.__args__['wireless_tp'] = 2
        elif 'central24G' in testcategory_list[i]:
            affirm_tl_operate.tl.__args__['wireless_tp'] = 3
        elif 'central5G' in testcategory_list[i]:
            affirm_tl_operate.tl.__args__['wireless_tp'] = 4
        else:
            pass
    except Exception, e:
        printResError('error %s' % e)
    # 获取当前测试类别中需要执行的测试例
    finaltestlist = get_testlist(testcategory_list[i], i, testdic)
    # 判断是否需要执行initial和unintial（基本逻辑是如果上一次执行的是本地转发,当前执行的也是本地转发，
    # 则不需要执行initial和unintial，如果上次执行集中转发，当前执行本地转发，则需要执行initial和unintial）
    if i != 0:
        newlog = True
        add_onlyonce_testlist = False
        if testcategory_list[i][0:5] == testcategory_list[i - 1][0:5]:
            passinitial = True
        else:
            passinitial = False
    if i != len(testcategory_list) - 1:
        if testcategory_list[i][0:5] == testcategory_list[i + 1][0:5]:
            passunintial = True
        else:
            passunintial = False
    # 获取参数testcentral、testlocal，将在initial文件中用到
    testcentral = True if 'central' in testcategory_list[i] else False
    testlocal = True if 'local' in testcategory_list[i] else False
    # 获取ApMAC
    ap1vapmac = ap1mac
    ap1mac_lower = ap1maclist[':']
    ap1mac_type1_network2 = incrmac(ap1mac_lower, 1).lower()
    ap2vapmac = ap2mac
    ap2mac_lower = ap2maclist[':']
    ap2mac_type1_network2 = incrmac(ap2mac_lower, 1).lower()
    if '24G' in testcategory_list[i]:
        # 参数test24glist、test5glist
        test24gflag = True
        test5gflag = False
        radionum = '1'
        wlan = 'wlan0'
    if '5G' in testcategory_list[i]:
        # 获取ApMAC（5g）
        ap1vapmac = incrmac(ap1vapmac, macincrease).lower()
        ap1mac_lower = incrmac(ap1mac_lower, macincrease).lower()
        ap1mac_type1_network2 = incrmac(ap1mac_lower, 1).lower()
        ap2vapmac = incrmac(ap2vapmac, macincrease).lower()
        ap2mac_lower = incrmac(ap2mac_lower, macincrease).lower()
        ap2mac_type1_network2 = incrmac(ap2mac_lower, 1).lower()
        # 参数test24gflag、test5gflag
        test24gflag = False
        test5gflag = True
        radionum = str(radio5G)
        wlan = 'wlan1'
    # 根据测试类别确定测试名称testName
    testName = 'waffirm'
    testName = testName + '_' + testcategory_list[i]
    # if vars():
    #     JsonHandle(vars()).save_data_to_file(WAFFIRM_ENV_ARGUMENT_JSON_PATH)
    #     printRes('Save All Arguments At {}'.format(WAFFIRM_ENV_ARGUMENT_JSON_PATH))
    printResDebug(
        '[通知]无线确认测试类型为{}（参数说明1:本地2.4G,2:本地5G,3:集中2,.4G,4:集中5G）'.format(affirm_tl_operate.tl.__args__['wireless_tp']))
    printResDebug('[通知]测试名称为 {}'.format(testName))
    # 重新根据testName创建按照文件夹分类的日志
    create_muliti_device_logs([pc1, sta1, sta2, switch1, switch2, switch3, ap1, ap2], prefix=prefix_log,
                              test_name='TestCase_' + testName)  # 根据24G和5G重新创建日志
    printGlobal('TestCase_' + testName, 'Start', logprefix=prefix_log)
    IdleAfter(0.5, msg='创建设备测试串口日志')
    if len(finaltestlist) > 0:
        for runtime in range(runtimes):
            printResDebug('[通知]|当前执行次数:|' + str(runtime + 1))
            if not passinitial:
                execfile('waffirm_initial.py')
            wx.FindWindowById(10).nowrunning = ''
            wx.FindWindowById(10).faillist = []
            for test in finaltestlist:
                if test[1] <= priority:
                    try:
                        wx.FindWindowById(10).nowrunning = test[0]
                        print(test[0])
                        execfile(test[0])
                    except Exception as e:
                        printTimer(test[0], 'Start')
                        printCheckStep(test[0], 'Step 0', 1)
                        traceback.print_exc()
                        printTimer(test[0], 'End', suggestion=['Python解释器捕获到脚本语法错误'])
                        set_default = 1
                        execfile('waffirm_initial.py')
                        set_default = temp_setdefault
                    printResWarn('[通知]当前失败用例为{}'.format(wx.FindWindowById(10).faillist))
        printGlobal('TestCase_' + testName, 'End')
        IdleAfter(10)
        faillister = wx.FindWindowById(10).faillist[:]
        if len(faillister) > 0:
            # 打开PC1,STA1,STA2,AC1,AC2,S3,AP1,AP2设备串口
            # 重新创建rerun的日志
            create_muliti_device_logs([pc1, sta1, sta2, switch1, switch2, switch3, ap1, ap2],
                                      prefix=prefix_log + '[ReRun]',
                                      test_name='TestCase_' + testName)  # 根据24G和5G重新创建日志
            # create_mulconn([pc1, sta1, sta2, switch1, switch2, switch3, ap1, ap2], prefix=prefix_log + '[ReRun]')
            printGlobal('TestCase_' + testName, 'RerunStart', logprefix=prefix_log)
            for fileTemp in faillister:
                try:
                    execfile(fileTemp)
                except Exception, e:
                    printTimer(fileTemp, 'Start')
                    printCheckStep(fileTemp, 'Step 0', 1)
                    traceback.print_exc()
                    printTimer(fileTemp, 'End', suggestion=['Python解释器捕获到脚本语法错误'])
                    set_default = 1
                    execfile('waffirm_initial.py')
                    set_default = temp_setdefault
            printGlobal('TestCase_' + testName, 'RerunEnd')
        if not passunintial:
            execfile('waffirm_uninitial.py')
testName = 'waffirm'
printGlobal('TestCase_' + testName, 'TlEnd')

if __name__ == '__main__':
    pass
