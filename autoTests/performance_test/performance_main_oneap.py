#-*- coding: UTF-8 -*

import time
import re
import random
import wx
import traceback

from dreceiver import *
from lib_all import *
from globalpara import *
from log import *
# from performance_func import *

multirunflag = True

def getWaffirmTestCaseByUser(*args,**kargs):
    '''
    函数：根据用户输入的testcentral_24g=True等信息返回按照用户指定优先级排序的要执行模块字符串
    输入：testcentral_24g=True,testcentral_5g=False
    输出：函数返回一个列表，包含了用户选择为True的模块，并且该模块根据run文件中的xxx_Pri进行从小到大的排序
    用法：默认只需要调用函数getWaffirmTestCaseByUser()即可返回对应列表，用户也可指定参数
    '''

    if not kargs:
        kargs={'central24G':central24G,
               'central5G':central5G,
               'local24G':local24G,
               'local5G':local5G
               }
    l=[k for (k,v) in list(kargs.items()) if v]
    kargs={}
    for i in l:
        kargs.update({i:eval(i+'_pri')})
    return [k for (k,v) in sorted(list(kargs.items()),key=lambda x:x[1])]
    
def ClassifyTestCase(Tlist):
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
    ret = {'ALL':[],
            'ONE':[],
            'CEN':[],
            'LOC':[],
            '24G':[],
            '5G':[],
            'C24G':[],
            'C5G':[],
            'L24G':[],
            'L5G':[]}
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

def GetTestlist(testcategory,order,Tdic):
    '''
    功能：根据当前执行的测试类别获取testlist列表，如当前执行集中转发2.4G测试，
    则会返回由名称带_ALL、_CEN、_24G、_C24G的所有测试例组成的列表
    参数：testcategory：代表当前测试类别的字符串
    order：当前测试类别的执行顺序，值为0、1、2、3
    Tdic：由ClassifyTestCase函数获得的返回值
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

def create_mulconn(sutlist,prefix=''):
    for sut in sutlist:
        if sut == pc1:
            try:
                CreateNewConn(pc1_type,pc1,pc1_host,None,'run',logprefix=prefix)
                TelnetLogin(pc1,Pc1_telnet_name,Pc1_telnet_password)
            except Exception as e:
                pass
        elif sut == sta1:
            try:
                CreateNewConn(sta1_type,sta1,sta1_host,None,'run',logprefix=prefix)
                TelnetLogin(sta1,Pc1_telnet_name,Pc1_telnet_password)
            except Exception as e:
                pass
        elif sut == sta2:
            try:
                CreateNewConn(sta2_type,sta2,sta2_host,None,'run',logprefix=prefix)
                TelnetLogin(sta2,Pc1_telnet_name,Pc1_telnet_password)
            except Exception as e:
                pass
        elif sut == switch1:
            try:
                CreateNewConn(switch1_type,switch1,switch1_host,None,'run',logprefix=prefix)
                SetTerminalLength(switch1)
            except Exception as e:
                pass
        # elif sut == switch2:
            # try:
                # CreateNewConn(switch2_type,switch2,switch2_host,None,'run',logprefix=prefix)
                # SetTerminalLength(switch2)
            # except Exception,e:
                # pass
        elif sut == switch3:
            try:
                CreateNewConn(switch3_type,switch3,switch3_host,None,'run',logprefix=prefix)
                SetTerminalLength(switch3)
            except Exception as e:
                pass
        elif sut == ap1:
            try:
                CreateNewConn(ap1_type,ap1,ap1_host,None,'run',logprefix=prefix)
                ApLogin(ap1)
            except Exception as e:
                pass

def create_mulapconn(aplist,prefix=''):
    for ap in aplist:
        try:
            CreateNewConn(ap['type'],ap['name'],ap['host'],None,'run',logprefix=prefix)
            ApLogin(ap['name'])
        except Exception as e:
            pass
            
def error_fix(casename):
    '''
    功能：遇到脚本错误后，自动重启设备，执行初始化操作
    参数：testcategory：代表当前测试类别的字符串
    order：当前测试类别的执行顺序，值为0、1、2、3
    Tdic：由classify_testcase函数获得的返回值
    返回值：该测试类别需要执行的所有测试用例组成的列表
    '''
    printTimer(casename,'Start')
    printCheckStep(casename, 'Step 0', 1)
    traceback.print_exc()
    printTimer(casename, 'End',suggestion = ['There is something wrong in this script'])
    set_default = 1
    exec(compile(open(module + '\\' + module + '_initial.py', "rb").read(), module + '\\' + module + '_initial.py', 'exec'))
    set_default = temp_setdefault
# 导入参数                  
exec(compile(open('performance_topu.py', "rb").read(), 'performance_topu.py', 'exec'))
exec(compile(open('performance_vars.py', "rb").read(), 'performance_vars.py', 'exec'))
exec(compile(open('performance_run.py', "rb").read(), 'performance_run.py', 'exec'))

# 获取用户自定义的字符串，添加在log的文件名中
if 'yourstring' in vars():
    if yourstring == '':
        pass
    else:
        yourstring='['+yourstring+']'
else:
    yourstring = ''

# 打开PC1,STA1,STA2,AC1,AC2,S3,AP1,AP2设备串口
create_mulconn([pc1,sta1,sta2,switch1,switch3,ap1])

# 获取switch1参数
switch1version = Get_switch_version(switch1)
ac1type=GetAcType(switch1)
EnterInterfaceMode(switch1,'vlan 1')
s1vlanmac = GetVlanMac(switch1)
   
# 获取AP1参数
# 获取AP的命令类型，'set' or 'uci set'
Ap1cmdtype = Get_ap_cmdtype(ap1)
ap1ver = Get_ap_version(ap1,Ap1cmdtype)
hwtype1 = Get_ap_hwtype(ap1,Ap1cmdtype)
ap1maclist = GetApMac(ap1,Ap1cmdtype)
ap1mac = ap1maclist['-']
ap1vapmac = ap1mac
ap1mac_type1 = ap1maclist[':']
ap1mac_type1_network2=incrmac(ap1mac_type1,1).lower()
##获得sta1的mac地址
sta1mac=GetStaMac(sta1)
sta1mac_type1=GetStaMac(sta1,connectflag=':')
sta1mac_upcase = sta1mac.upper()
print('sta1mac=',sta1mac)
##获得sta2的mac地址
sta2mac=GetStaMac(sta2)
sta2mac_type1=GetStaMac(sta2,connectflag=':')
sta2mac_upcase = sta2mac.upper()
print('sta2mac=',sta2mac)
pc1mac='00:0E:C6:CE:96:44'
# 判断是否打开多个ap的串口
if len(aplist) > 0:
    mulapflag = True
    # create_mulapconn(aplist)
    for ap in aplist:
        # ap['cmdtype'] = Get_ap_cmdtype(ap['name'])
        # ap['version'] = Get_ap_version(ap['name'],ap['cmdtype'])
        # ap['hwtype'] = Get_ap_hwtype(ap['name'],ap['cmdtype'])
        # ap['maclist'] = GetApMac(ap['name'],ap['cmdtype'])
        # ap['mac'] = ap['maclist']['-']
        ap['mac_type1'] = ap['mac'].lower()
        ap['mac'] = re.sub(':','-',ap['mac_type1'])
        ap['vapmac'] = ap['mac']
        # ap['mac_type1'] = ap['maclist'][':']
        # ap['mac_type1'] = re.sub('-',':',ap['mac'])
        ap['mac_type1_network2'] = incrmac(ap['mac_type1'] ,1)
else:
    mulapflag = False
    
ap_name_list = [ap1]
ap_s3port_list = [s3p3]
ap_mac_list = [ap1mac]
ap_bssid_list = [ap1mac_type1]
ap_imagetype_list = [ap1_imagetype]
ap_nowversionfile_list = [ap1_now_versionfile]
ap_oldversionfile_list = [ap1_old_versionfile]
ap_nowversionnum_list = [ap1_now_versionnum]
ap_oldversionnum_list = [ap1_old_versionnum]
ap_hwtype_list = [hwtype1]
ap_ipv4_list = [Ap1_ipv4]
ap_cmdtype_list = [Ap1cmdtype]
if mulapflag == True:
    for ap in aplist:
        ap_name_list.append(ap['name'])
        ap_s3port_list.append(ap['s3port'])
        ap_mac_list.append(ap['mac'])
        ap_bssid_list.append(ap['mac_type1'])
        ap_imagetype_list.append(ap['imagetype'])
        ap_nowversionfile_list.append(ap['now_versionfile'])
        ap_oldversionfile_list.append(ap['old_versionfile'])
        ap_nowversionnum_list.append(ap['now_versionnum'])
        ap_oldversionnum_list.append(ap['old_versionnum'])
        ap_hwtype_list.append(ap['hwtype'])
        # ap_ipv4_list.append(ap['ipv4'])
        # ap_cmdtype_list.append(ap['cmdtype'])
total_apnum = len(ap_name_list)
    
# # 判断需要执行的测试项目
testcategory_list = getWaffirmTestCaseByUser()
testdic = ClassifyTestCase(testlist)
if 'radio5Gswitch' in vars():
    radio1num = '1'
    if radio5Gswitch == True:
        macincrease = (radio5G-1)*16
        radio2num = str(radio5G)
    else:
        macincrease = 16
        radio2num = '2'
else:
    radio1num = '1'
    radio2num = '2'
    macincrease = 16
# 执行用例脚本   
passinitial = False
passunintial = False
newlog = False
for i in range(len(testcategory_list)):
    finaltestlist = GetTestlist(testcategory_list[i],i,testdic)
    if i != 0:
        newlog = True
        add_onlyonce_testlist = False
        if testcategory_list[i][0:5] == testcategory_list[i-1][0:5]:
            passinitial = True
        else:
            # set_default = 1
            passinitial = False
    if i != len(testcategory_list)-1:
        if testcategory_list[i][0:5] == testcategory_list[i+1][0:5]:
            passunintial = True
        else:
            passunintial = False

    # 参数testcentral、testlocal将在initial和run文件中用到
    testcentral = True if 'central' in testcategory_list[i] else False
    testlocal = True if 'local' in testcategory_list[i] else False
    if '24G' in testcategory_list[i]:
        # 参数test24glist、test5glist将在run文件中用到
        test24gflag = True
        test5gflag = False
        radionum = '1'
        wlan = 'wlan0'
    if '5G' in testcategory_list[i]:
        # 获取ApMAC（5g）
        # 参数test24gflag、test5gflag将在run文件中用到
        test24gflag = False
        test5gflag = True
        radionum = str(radio5G)
        wlan = 'wlan1'
        ap1vapmac = incrmac(ap1vapmac,macincrease).lower()
        ap1mac_type1 = incrmac(ap1mac_type1,macincrease).lower()
        ap1mac_type1_network2=incrmac(ap1mac_type1,1).lower()
        if mulapflag == True:
            ap['vapmac'] = incrmac(ap['vapmac'],macincrease).lower()
            ap['mac_type1'] = incrmac(ap['mac_type1'],macincrease).lower()
            ap['mac_type1_network2'] = incrmac(ap['mac_type1'],1).lower()
    # 确定测试名称testName
    testName = 'performance'
    printGlobal('TestCase_'+testName,'Nothing')
    # 打开PC1,STA1,STA2,AC1,AC2,S3,AP1,AP2设备串口
    create_mulconn([pc1,sta1,sta2,switch1,switch3,ap1])
    # if mulapflag == True:
        # create_mulapconn(aplist)
    printGlobal('TestCase_'+testName,'Start')

    if len(finaltestlist) > 0:
        for runtime in range(runtimes):
            printRes('|runtime:|'+str(runtime+1))
            if passinitial == False:
                exec(compile(open('performance_initial_oneap.py', "rb").read(), 'performance_initial_oneap.py', 'exec'))
            wx.FindWindowById(10).nowrunning = ''
            wx.FindWindowById(10).faillist = []
            if 'individualflag' not in vars():
                for test in finaltestlist:
                    if test[1] <= priority:
                        try:
                            wx.FindWindowById(10).nowrunning = test[0]
                            exec(compile(open(test[0], "rb").read(), test[0], 'exec'))
                        except Exception as e:
                            error_fix(test[0])
                        print(wx.FindWindowById(10).faillist)
                # if passunintial == False:
                    # execfile('waffirm_uninitial.py')
                printGlobal('TestCase_'+testName,'End')

# testName = 'performance'
# printGlobal('TestCase_'+testName,'TlEnd')