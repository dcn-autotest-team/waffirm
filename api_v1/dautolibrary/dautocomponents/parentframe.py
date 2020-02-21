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


import codecs
import datetime
import os
import sys
import time
# 主框
from io import StringIO
from xml.dom import minidom

import wx
import wx.aui
from dautolibrary.dautocomponents.childframe import ChildFrame
from dautolibrary.dautoconnections.connIxia.createIxiaScriptDialog import ConnIxiaFrame
from dautolibrary.dautoconnections.connIxia.python2tcl import StartTclServerTh
from dautolibrary.dautoconnections.connSerial import DautoSerialFactory
from dautolibrary.dautoconnections.connTelnetCCM.dautoTelnetCCMFactory import DautoTelnetCCMFactory
from dautolibrary.dautoconnections.connTelnetPC.dautoTelnetPCFactory import DautoTelnetPCFactory
from dautolibrary.dautoconst import HELP_ABOUT_NAME, HELP_ABOUT_VERSION, HELP_ABOUT_COPYRIGHT, HELP_ABOUT_DESCRIPTION, \
    HELP_ABOUT_WEBSITE, HELP_ABOUT_DEVELOPERS, WILDCARD
from dautolibrary.dautoconst import Main_WINDOW_TITLE
from dautolibrary.dautothread.basethread import ExThread
from dautolibrary.dautothread.printthread import PrintThread
from dautolibrary.dautoutils.dautotools import call_after
from dtestlink.dcntestlink.dcntestlinkoperate import AffirmTestlinkOperate, DautoTestlinkOperate
from dutils.dcnlogs.dcnuserlog import close_logger, close_all_logger
from dutils.dcnprint import printResError, printResDebug, printScr, printRes, printAll
from wx.lib.wordwrap import wordwrap

from .connectDialog import TestDialog
from .debugframe import DebugFrame
from .dstyle import LoadReceiverDebugConfig, LoadErrorStopConfig, loadStyleConfig, dc_path, \
    ChangeColor
from .images import icon, autoTest, newConn, pause, ahead, stop, clear, ixos, quickConn, \
    autoCreate, pin, timelog, send, editScript, quickScript, debugpoint, debugpointon, printfront, printback, printUI, \
    quickShell, errorStop, errorPass
from .printtextctrl import PrintTextCtrl
from .quickConnect import loadconfig, add2config
from .quickCreatePy import openCreateDialog
from .quickruntextctrl import QuickRunTextCtrl
from .scriptEdit import EditDialog

if 'phoenix' in wx.version():  # 版本向后兼容新的wxpython平台
    import wx.adv
    
    wx.SAVE = wx.FC_SAVE
    wx.OPEN = wx.FD_OPEN
    wx.CHANGE_DIR = wx.FD_CHANGE_DIR
    wx.AboutDialogInfo = wx.adv.AboutDialogInfo
    wx.AboutBox = wx.adv.AboutBox


class ParentFrame(wx.aui.AuiMDIParentFrame):
    """
    Dauto平台的主窗口，为程序入口的主Frame，后面创建的输入输出以及shell还有打开的窗口基于此Frame而创建
    """
    
    def __init__(self, parent, local_dir, log_base_path, log_config_file, ftp_config_file, ftp_server_ip):
        """
        主窗口初始化
        :param parent: AuiMDIParentFrame
        :param local_dir: Dauto程序所在的dir路径
        :param log_base_path: 日志前缀路径
        :param log_config_file: 日志配置文件路径
        :param ftp_config_file: ftp配置文件路径
        :param ftp_server_ip: ftp server ip地址
        """
        super().__init__(parent, 10,
                         title=Main_WINDOW_TITLE,
                         size=(800, 600),
                         name='Main',
                         style=wx.DEFAULT_FRAME_STYLE ^ wx.WANTS_CHARS)
        self.local_dir = local_dir
        self.log_base_path = log_base_path
        self.log_config_file = log_config_file
        self.ftp_config_file = ftp_config_file
        self.ftp_server_ip = ftp_server_ip
        self._mgr = wx.aui.AuiManager(self)
        self.consoleWindow = None
        self.buff = StringIO()
        self.temp = sys.stdout  # 保留原始的输出环境
        sys.stdout = self.buff
        sys.stderr = self.buff
        self.thread = None
        self.print2window = False
        self.count = 0
        self.countlist = list(range(1, 10))
        self.stylelist = []
        self.childnamelist = []
        self.childqueue = []
        self.logger = None  # 主窗口日志操作句柄，用于后面记录console日志
        self.nowrunning = ''
        self.faillist = []
        self.ac = ''
        self.ap = ''
        self.apimg1 = ''
        self.apuboot1 = ''
        self.apimg2 = ''
        self.apuboot2 = ''
        self.dbInfo = {
            'id': '', 'username': '', 'env': '', 'totalcases': '', 'logs': '', 'passed': '', 'failed': '',
            'knownbugs': '',
            'unknowbugs': '', 'failsummary': '', 'suggestions': '', 'starttime': '', 'stoptime': '',
            'totaltime': '', 'versioninfo': '', 'comment': '', 'statistics1': '', 'statistics2': '',
            'statistics3': '', 'reserved1': '', 'reserved2': '', 'reserved3': ''
        }
        self.logfiles = []
        self.env = '1'
        self.SetIcon(icon.Icon)
        # 图标
        auto_test_bmp = autoTest.GetBitmap()
        new_bmp = newConn.GetBitmap()
        pause_bmp = pause.GetBitmap()
        ahead_bmp = ahead.GetBitmap()
        stop_bmp = stop.GetBitmap()
        clear_bmp = clear.GetBitmap()
        ixia_bmp = ixos.GetBitmap()
        quick_conn_bmp = quickConn.GetBitmap()
        auto_create_bmp = autoCreate.GetBitmap()
        pin_bmp = pin.GetBitmap()
        timelog_bmp = timelog.GetBitmap()
        send_img = send.GetBitmap()
        edit_script_img = editScript.GetBitmap()
        quick_script_bmp = quickScript.GetBitmap()
        self.debugpoint_bmp = debugpoint.GetBitmap()
        self.debugpointon_bmp = debugpointon.GetBitmap()
        self.printfront_bmp = printfront.GetBitmap()
        self.printback_bmp = printback.GetBitmap()
        self.printUI_bmp = printUI.GetBitmap()
        quick_shell_bmp = quickShell.GetBitmap()
        self.errorStop = errorStop.GetBitmap()
        self.errorPass = errorPass.GetBitmap()
        if 'phoenix' in wx.version():
            toolbar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
            toolbar.AddTool(58, '', quick_conn_bmp, "快速连接")
            toolbar.AddSeparator()
            
            toolbar.AddTool(59, '', auto_create_bmp, "自动创建测试脚本")
            toolbar.AddTool(504, '', edit_script_img, "编辑脚本")
            toolbar.AddTool(505, '', ixia_bmp, "自动创建Ixia脚本.")
            toolbar.AddSeparator()
            
            toolbar.AddTool(501, '', pin_bmp, "控制滚屏")
            toolbar.AddTool(503, '', send_img, "Stop/Continue 发送消息")
            toolbar.AddTool(502, '', timelog_bmp, "短消息留言")
            toolbar.AddTool(57, '', clear_bmp, "清屏")
            toolbar.AddSeparator()
            
            toolbar.AddTool(506, '', quick_script_bmp, "快速运行脚本")
            toolbar.AddTool(510, '', quick_shell_bmp, "快速连接Shell")
            toolbar.AddTool(509, '', self.printUI_bmp, "系统输出")
            toolbar.AddSeparator()
            
            toolbar.AddTool(51, '', auto_test_bmp, "运行测试用例")
            toolbar.AddTool(54, '', pause_bmp, "暂停")
            toolbar.AddTool(55, '', ahead_bmp, "前进")
            toolbar.AddTool(56, '', stop_bmp, "停止")
            debug_flag = LoadReceiverDebugConfig()
            if debug_flag:
                debugpoint_bmp = self.debugpointon_bmp
            else:
                debugpoint_bmp = self.debugpoint_bmp
            
            toolbar.AddTool(507, '', debugpoint_bmp, "调试: step by step")
            
            errorstop_flag = LoadErrorStopConfig()
            if errorstop_flag:
                errorstop_bmp = self.errorStop
            else:
                errorstop_bmp = self.errorPass
            toolbar.AddTool(511, '', errorstop_bmp, "遇错就停")
        else:
            toolbar = self.CreateToolBar(wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT | wx.TB_TEXT)
            toolbar.AddSimpleTool(58, quick_conn_bmp, "快速连接", "快速连接")
            toolbar.AddSeparator()
            
            toolbar.AddSimpleTool(59, auto_create_bmp, "自动创建测试脚本.", "自动创建测试脚本")
            toolbar.AddSimpleTool(504, edit_script_img, "编辑脚本", "编辑脚本")
            toolbar.AddSimpleTool(505, ixia_bmp, "自动创建Ixia脚本.", "自动创建Ixia脚本")
            toolbar.AddSeparator()
            
            toolbar.AddSimpleTool(501, pin_bmp, "控制滚屏", "控制滚屏")
            toolbar.AddSimpleTool(503, send_img, "Stop/Continue 发送消息", "Stop/Continue 发送消息")
            toolbar.AddSimpleTool(502, timelog_bmp, "短消息留言", "短消息留言")
            toolbar.AddSimpleTool(57, clear_bmp, "清屏", "清屏")
            toolbar.AddSeparator()
            
            toolbar.AddSimpleTool(506, quick_script_bmp, "快速运行脚本", "快速运行脚本")
            toolbar.AddSimpleTool(510, quick_shell_bmp, "快速连接Shell", "快速连接Shell")
            toolbar.AddSimpleTool(509, self.printUI_bmp, "系统输出", "系统输出")
            toolbar.AddSeparator()
            
            toolbar.AddSimpleTool(51, auto_test_bmp, "运行测试用例", "运行测试用例")
            toolbar.AddSimpleTool(54, pause_bmp, "暂停", "暂停")
            toolbar.AddSimpleTool(55, ahead_bmp, "前进", "前进")
            toolbar.AddSimpleTool(56, stop_bmp, "停止", "停止")
            debug_flag = LoadReceiverDebugConfig()
            if debug_flag:
                debugpoint_bmp = self.debugpointon_bmp
            else:
                debugpoint_bmp = self.debugpoint_bmp
            
            toolbar.AddSimpleTool(507, debugpoint_bmp, "调试: step by step", "调试: step by step")
            
            errorstop_flag = LoadErrorStopConfig()
            if errorstop_flag:
                errorstop_bmp = self.errorStop
            else:
                errorstop_bmp = self.errorPass
            toolbar.AddSimpleTool(511, errorstop_bmp, "遇错就停", "遇错就停")
        
        toolbar.EnableTool(54, False)
        toolbar.EnableTool(55, False)
        toolbar.EnableTool(56, False)
        
        toolbar.Realize()
        self.toolbar = toolbar
        
        # 事件绑定
        self.Bind(wx.EVT_TOOL, self.TestRun, id=51)
        self.Bind(wx.EVT_TOOL, self.ConfigNewChannel, id=52)
        self.Bind(wx.EVT_TOOL, self.ConfigNewChannel, id=53)
        self.Bind(wx.EVT_TOOL, self.PauseTestManual, id=54)
        self.Bind(wx.EVT_TOOL, self.AheadTest, id=55)
        self.Bind(wx.EVT_TOOL, self.TestKill, id=56)
        self.Bind(wx.EVT_TOOL, self.ClearFocus, id=57)
        self.Bind(wx.EVT_TOOL, self._LoadChannelConfig, id=58)
        self.Bind(wx.EVT_TOOL, self.OnOpenCreateDialog, id=59)
        self.Bind(wx.EVT_TOOL, self.ControlSroll, id=501)
        self.Bind(wx.EVT_TOOL, self.OnPrintLogInfo, id=502)
        self.Bind(wx.EVT_TOOL, self.OnStopSendMessage, id=503)
        self.Bind(wx.EVT_TOOL, self.OnScriptEdit, id=504)
        self.Bind(wx.EVT_TOOL, self.OnCreateIxiaScript, id=505)
        self.Bind(wx.EVT_TOOL, self.OnQuickScriptWindow, id=506)
        self.Bind(wx.EVT_TOOL, self.OnQuickShell, id=510)
        self.Bind(wx.EVT_TOOL, self.OnSetStepDebug, id=507)
        self.Bind(wx.EVT_TOOL, self.OnErrorStop, id=511)
        self.Bind(wx.EVT_TOOL, self.OnSystemStdoutWindow, id=509)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        # 菜单
        menuBar = self.MakeMenuBar()
        self.menuBar = menuBar
        menu3 = wx.Menu()
        stylelist = loadStyleConfig(True)
        style_count = 31
        for style_i in stylelist:
            menu3.Append(style_count, style_i[0], "选择切换一种样式.", wx.ITEM_RADIO)
            if style_i[1]:
                menu3.Check(style_count, True)
            style_count += 1
        # menuBar.Append(menu3, "&View")
        menuBar.Append(menu3, "&视图")
        menu = wx.Menu()
        # item = menu.Append(-1, "Run test cases")
        item = menu.Append(-1, "运行测试用例")
        self.Bind(wx.EVT_MENU, self.TestRun, item)
        # menuBar.Append(menu, "&Autotest")
        menuBar.Append(menu, "&自动测试")
        menu = wx.Menu()
        # item = menu.Append(-1, "Quick run windows")
        item = menu.Append(-1, "快速运行窗口")
        self.Bind(wx.EVT_MENU, self.OnQuickScriptWindow, item)
        # item = menu.Append(-1, "Shell window")
        item = menu.Append(-1, "Shell窗口")
        self.Bind(wx.EVT_MENU, self.OnQuickShell, item)
        # item = menu.Append(-1, "Stdout/Stderr window")
        item = menu.Append(-1, "输出/错误信息窗口")
        self.Bind(wx.EVT_MENU, self.OnSystemStdoutWindow, item)
        # item = menu.Append(-1, "Start Tcl Server")
        item = menu.Append(-1, "开启Tcl Server")
        self.Bind(wx.EVT_MENU, self.OnStartTclServer, item)
        menuBar.Append(menu, "&工具")
        menu = wx.Menu()
        item = menu.Append(-1, "关于")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)
        menuBar.Append(menu, "&帮助")
        for i in range(31, style_count):
            self.Bind(wx.EVT_MENU, self._ChangeColor, id=i)
        self.SetMenuBar(menuBar)
        self.CreateStatusBar()
        # 向调试窗口打印信息的线程
        self.printTh = PrintThread('print')
        self.printTh.start()
        self.OnSystemStdoutWindow1()
        # 连接testlink服务器
        self.tl = AffirmTestlinkOperate(tl_args_flag=1, tl_overwrite_flag=1)
        # 在testlink服务器上面校验参数是否正确，校验成功：testlink服务器执行或者/testlink/args.py撰写正确的参数，校验失败：本地执行，或者testlink服务器参数异常
        self.tl.check_testlink_args()
    
    @staticmethod
    def OnOpenCreateDialog(evt):
        """
        重复脚本快速生成窗口
        :param evt:
        :return:
        """
        openCreateDialog()
    
    def OnAbout(self, evt):
        """
        About窗口
        :param evt: 用户点击About事件
        :return: None
        """
        info = wx.AboutDialogInfo()
        info.Name = HELP_ABOUT_NAME
        info.Version = HELP_ABOUT_VERSION
        info.Copyright = HELP_ABOUT_COPYRIGHT
        info.Description = wordwrap(HELP_ABOUT_DESCRIPTION, 600, wx.ClientDC(self))
        info.WebSite = (HELP_ABOUT_WEBSITE, "FAQ<--Click")
        info.Developers = HELP_ABOUT_DEVELOPERS
        wx.AboutBox(info)
    
    @staticmethod
    def OnStartTclServer(evt):
        """
        运行tcl中转服务
        :param evt: 用户点击start tcl server事件
        :return: None
        """
        StartTclServerTh()
    
    def OnSetStepDebug(self, evt):
        """
        单步调试
        :param evt: 单步调试事件
        :return: None
        """
        _path = dc_path
        xmldoc = minidom.parse(_path)
        root = xmldoc.firstChild
        nodes = root.childNodes
        flag = nodes[0].childNodes[0].firstChild.data
        if flag == 'False':
            self.toolbar.SetToolNormalBitmap(507, self.debugpointon_bmp)
        else:
            self.toolbar.SetToolNormalBitmap(507, self.debugpoint_bmp)
        nodes[0].childNodes[0].firstChild.data = str(not eval(flag))
        with open(path, 'wb') as f:
            writer = codecs.lookup('utf-8')[3](f)
            xmldoc.writexml(writer, encoding='utf-8')
            writer.close()
    
    def OnErrorStop(self, evt):
        """
        遇错就停
        :param evt: 遇错就停事件
        :return: None
        """
        path = dc_path
        xmldoc = minidom.parse(path)
        root = xmldoc.firstChild
        nodes = root.childNodes
        flag = nodes[0].childNodes[1].firstChild.data
        if flag == 'False':
            self.toolbar.SetToolNormalBitmap(511, self.errorStop)
        else:
            self.toolbar.SetToolNormalBitmap(511, self.errorPass)
        nodes[0].childNodes[1].firstChild.data = str(not eval(flag))
        with open(path, 'wb') as f:
            writer = codecs.lookup('utf-8')[3](f)
            xmldoc.writexml(writer, encoding='utf-8')
            writer.close()
    
    def OnSystemStdoutWindow1(self):
        """
        调试信息窗口
        :return: None
        """
        
        if self.FindWindowById(553):
            return 1
        self._mgr.AddPane(self.CreateConsoleTextCtrl(), wx.aui.AuiPaneInfo().
                          Caption("输出窗口:").
                          Bottom().Layer(1).Position(1).
                          CloseButton(False).MaximizeButton(True).MinimizeButton(True).DestroyOnClose(False).MinSize(
            wx.Size(200, 240)))
        self._mgr.Update()
    
    def OnSystemStdoutWindow(self, evt):
        """
        调试信息窗口
        :param evt: 调试信息窗口事件
        :return: None
        """
        if self.FindWindowById(553):
            return 1
        self._mgr.AddPane(self.CreateConsoleTextCtrl(), wx.aui.AuiPaneInfo().
                          Caption("输出窗口:").
                          Bottom().Layer(1).Position(1).
                          CloseButton(True).MaximizeButton(True).DestroyOnClose(True))
        self._mgr.Update()
    
    @call_after
    def OnQuickScriptWindow(self, evt):
        """
        快速运行脚本窗口（篮球）
        :param evt: 快速运行脚本窗口事件
        :return: None
        """
        if self.FindWindowById(551):
            return 1
        self._mgr.AddPane(self.CreateQuickScriptTextCtrl(), wx.aui.AuiPaneInfo().
                          Caption("脚本运行窗口:").
                          Bottom().Layer(1).Position(1).
                          CloseButton(True).MaximizeButton(True).DestroyOnClose(True))
        self._mgr.Update()
    
    @call_after
    def OnQuickShell(self, evt):
        """
        快速调试发包工具窗口（棒球）
        :param evt: 快速调试发包工具窗口事件
        :return: None
        """
        if self.FindWindowById(552):
            return 1
        self._mgr.AddPane(self.CreateShell(), wx.aui.AuiPaneInfo().
                          Caption("Shell窗口:").
                          Bottom().Layer(1).Position(1).
                          CloseButton(True).MaximizeButton(True).DestroyOnClose(True))
        self._mgr.Update()
    
    def CreateConsoleTextCtrl(self):
        """
        调试信息打印窗口(足球)
        :return: PrintTextCtrl实例
        """
        console_window = PrintTextCtrl(self)
        return console_window
    
    def CreateShell(self):
        """
        创建并返回特定的textctrl
        :return: DebugFrame实例
        """
        return DebugFrame(self, self.local_dir)
    
    # 创建并返回特定的textctrl
    def CreateQuickScriptTextCtrl(self):
        
        tc = QuickRunTextCtrl(self, self.local_dir)
        return tc
    
    @staticmethod
    def OnCreateIxiaScript(evt):
        """
        ixia命令生成指导窗口
        :param evt:ixia命令生成指导窗口事件
        :return:None
        """
        
        a = ConnIxiaFrame(parent=None)
        a.ShowModal()
        a.Destroy()
    
    @staticmethod
    def _LoadChannelConfig(evt):
        """
        加载样式
        :param evt:加载样式事件
        :return:None
        """
        loadconfig()
    
    @staticmethod
    def _ChangeColor(evt):
        """
        改变样式
        :param evt:改变样式事件
        :return:None
        """
        
        menu_id = evt.GetId()
        ChangeColor(menu_id - 30)
    
    def ReturnFilePath(self, evt):
        """
        返回所选要执行python文件的文件路径
        :param evt: evt事件
        :return:返回所选要执行python文件的文件路径
        """
        
        save1_dir = sys.path[0]
        if os.path.isfile(save1_dir):
            save1_dir = os.path.split(save1_dir)[0]
        dlg = wx.FileDialog(
            self,
            message="选择一个python文件",
            defaultDir=save1_dir,
            defaultFile="",
            wildcard=WILDCARD,
            style=wx.OPEN | wx.CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPaths()
            return path
        else:
            return None
    
    def ErrorReport(self, msg):
        """
        底部状态栏-出错提示
        :param msg: 出错信息
        :return: None
        """
        self.StatusBar.SetStatusText(str(msg))
    
    def ConfigNewChannel(self, evt):
        """
        新建连接（标签页获取各参数)
        :param evt: 用户点击文件-连接按钮输入参数信息点击ok之后事件
        :return: None
        """
        
        dlg = TestDialog(self, -1, "Connect Dialog")
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            # -----------------------get select and input-------------------
            op_type = dlg.FindWindowById(72)
            con_type_id = op_type.GetSelection()
            con_type = op_type.GetString(con_type_id)
            con_title = dlg.FindWindowById(74).GetValue()
            con_host = dlg.FindWindowById(76).GetValue()
            # 打开选择日志路径对话框，返回用户选择的日志路径
            path = str(dlg.save())
            self.CreateNewChannel(con_type, con_title, con_host, path)
            add2config(con_type, con_title, con_host, path)
        dlg.Destroy()
    
    @call_after
    def CreateNewChannel(self, con_type, con_title, con_host, path=None, log_type='default', logprefix=''):
        """
        新建连接（标签页建立连接并打开标签)
        :param con_type: TelnetCCM Telnet Serial
        :param con_title: s1 s2
        :param con_host: 172.17.100.1
        :param path: 日志路径
        :param log_type: 日志类型
        :param logprefix: 日志前缀
        :return: None
        """
        try:
            
            self.childnamelist.append(con_title)
            if len(self.countlist):
                self.count = self.countlist[0]
                self.countlist.remove(self.count)
            else:
                self.count += 1
            con_port = 23
            conn = ''
            # -----------------------Telnet PC----------------------------
            if con_type == 'Telnet':
                con_port = 23
                pcConn = DautoTelnetPCFactory().createDautoChannel(con_host, int(con_port))
                conn = pcConn.getChannelOP()
            
            # -----------------------Telnet CCM----------------------------
            elif con_type == 'TelnetCCM':
                con_host_list = con_host.split(':')
                if len(con_host_list) == 2:
                    con_host = con_host_list[0]
                    con_port = con_host_list[1]
                try:
                    con_port = int(con_port)
                except BaseException as e:
                    printResError('[CreateNewChannel] {}'.format(e))
                ccmConn = DautoTelnetCCMFactory().createDautoChannel(con_host, con_port)
                conn = ccmConn.getChannelOP()
            
            # -----------------------Connect Serial----------------------------
            elif con_type == 'Serial':
                con_port = con_host
                try:
                    con_port = int(con_port)
                except BaseException as e:
                    printResError('[CreateNewChannel] {}'.format(e))
                serialConn = DautoSerialFactory().createDautoChannel(con_port)
                conn = serialConn.getChannelOP()
            elif con_type == 'Shell':
                childpage = DebugFrame(self)
                childpage.Show()
                return 0
            if conn.connected:
                child = ChildFrame(self, self.count, str(con_host), str(con_title), conn, path, log_type, logprefix)
                self.childqueue.append(child)
                child.Activate()
            else:
                ParentFrame.ErrorReport(self, conn.msg)
                self.childnamelist.remove(con_title)
                self.countlist.append(self.count)
        except BaseException as e:
            printResError('Occur Exception: {}'.format(e))
    
    def ClearFocus(self, evt):
        """
        清除焦点所在屏幕的信息
        :param evt: 清除焦点所在屏幕的信息事件
        :return: None
        """
        page_focus = self.FindFocus()
        if page_focus.ClassName == 'wxTextCtrl':
            page_focus.Clear()
            page_focus.Parent.insertPoint = 0
    
    def TestRunAuto(self, path, printflag=1):
        """
        测试例运行脚本调用接口
        :param path: 脚本所在路径
        :param printflag: 是否打印显示
        :return: None
        """
        
        if path:
            namelist = os.path.split(path)
            if namelist[0] not in sys.path:
                sys.path.append(namelist[0])
            os.chdir(namelist[0])
            self.thread = ExThread('th1918', path, self, printflag, namelist[1].split('_')[0])
            self.thread.start()
            self.toolbar.EnableTool(54, True)
            self.toolbar.EnableTool(56, True)
            self.toolbar.EnableTool(51, False)
    
    def TestRun(self, evt):
        """
        测试例运行界面手工调用接口
        :param evt: 测试例运行界面手工调用接口事件
        :return: None
        """
        path = self.ReturnFilePath(evt)
        if path:
            namelist = os.path.split(path[0])
            # 获取路径
            sys.path.append(namelist[0])
            self.thread = ExThread('th1918', path[0], self, 1, namelist[1].split('_')[0])
            self.thread.start()
            self.toolbar.EnableTool(54, True)
            self.toolbar.EnableTool(56, True)
            self.toolbar.EnableTool(51, False)
    
    def PauseTestManual(self, evt):
        """
        测试例暂停界面手工控制接口, 同时将暂停结果反馈给testlink服务器
        :param evt: 测试例暂停界面手工控制接口事件
        :return: None
        """
        DautoTestlinkOperate().tl_pause_test_manual()
        self.toolbar.EnableTool(54, False)
        self.toolbar.EnableTool(55, True)
        if self.thread:
            self.thread.pause()
    
    def PauseTestAuto(self):
        """
        测试例暂停止脚本控制接口
        :return: None
        """
        self.toolbar.EnableTool(54, False)
        self.toolbar.EnableTool(55, True)
        if self.thread:
            self.thread.pause()
    
    def AheadTest(self, evt):
        """
        暂停的测试例继续运行,结果反馈给testlink服务器
        :param evt: 暂停的测试例继续运行事件
        :return: None
        """
        DautoTestlinkOperate().tl_ahead_test()
        self.toolbar.EnableTool(54, True)
        self.toolbar.EnableTool(55, False)
        if self.thread:
            self.thread.ahead()
    
    def AutoTestKill(self):
        """
        测试例停止运行脚本调用接口
        :return: None
        """
        wx.CallAfter(self.toolbar.EnableTool, 54, False)
        wx.CallAfter(self.toolbar.EnableTool, 55, False)
        wx.CallAfter(self.toolbar.EnableTool, 56, False)
        wx.CallAfter(self.toolbar.EnableTool, 51, True)
    
    def TestKill(self, evt):
        """
        测试例停止运行界面手工控制接口
        :param evt: 测试例停止运行界面手工控制接口事件
        :return: None
        """
        wx.CallAfter(self.toolbar.EnableTool, 54, False)
        wx.CallAfter(self.toolbar.EnableTool, 55, False)
        wx.CallAfter(self.toolbar.EnableTool, 56, False)
        wx.CallAfter(self.toolbar.EnableTool, 51, True)
        if self.thread:
            self.thread.kill()
    
    def GetPages(self, return_type='name'):
        """
        获取当前打开的标签页信息
        :param return_type: 通过name（s1 s2）获取页面信息
        :return: page list
        """
        windows_list = self.GetChildren()
        aui_client_list = windows_list[0].GetChildren()
        page_list = []
        
        for frame in aui_client_list:
            try:
                page_name = frame.pagename
                if return_type == 'name':
                    page_list.append(page_name)
                elif return_type == 'page':
                    page_list.append(frame)
            except AttributeError:
                pass
        return page_list
    
    def ControlSroll(self, evt):
        """
        控制滚屏
        :param evt: 控制滚屏事件
        :return:
        """
        page_list = self.GetPages('page')
        showPositionFlag = True
        for i in page_list:
            i.showPositionFlag = not i.showPositionFlag
            showPositionFlag = i.showPositionFlag
            if showPositionFlag:
                if 'phoenix' in wx.version():
                    i.page.Thaw()
                else:
                    i.page.SetWindowStyle(wx.TE_NOHIDESEL)
            else:
                try:
                    i.page.SetWindowStyle(wx.TE_AUTO_SCROLL)
                except Exception as e:  # 兼容新版本的phoenix
                    i.page.Freeze()
        if not showPositionFlag:
            self.SetFocus()
    
    def OnCloseWindowAuto(self):
        """
        调试使用
        :return:None
        """
        windows_list = self.GetChildren()
        aui_client_list = windows_list[0].GetChildren()
        if self.thread and isinstance(self.thread, ExThread):
            if self.thread.is_alive():
                self.thread.kill()
        for frame in aui_client_list:
            try:
                printResDebug('[OnCloseWindowAuto] 1')
                frame.OnCloseWindowAuto()
                time.sleep(0.5)
                printResDebug('[OnCloseWindowAuto] 2')
            except:
                printResDebug('[OnCloseWindowAuto] 3')
        self.printTh.stop()
        printResDebug('[OnCloseWindowAuto]')
    
    def OnCloseWindow(self, event):
        """
        手动点击右上角关闭按钮，关闭主窗口,清理buffer，关闭run线程，print线程，读取串口信息线程，logger信息
        :param event: 手工关闭窗口的时候wxpython调用绑定事件的时候带上event参数，可以对event进行处理
        :return: None
        """
        
        wx.TheClipboard.Flush()
        dlg = wx.MessageDialog(self, '确定要关闭吗?', '拜拜:', wx.YES_NO | wx.ICON_INFORMATION | wx.CENTRE | wx.NO_DEFAULT)
        _res = dlg.ShowModal()
        dlg.Destroy()
        if _res == wx.ID_NO:
            event.Veto()
            return
        windows_list = self.GetChildren()
        aui_client_list = windows_list[0].GetChildren()
        if self.thread and isinstance(self.thread, ExThread):
            if self.thread.is_alive():
                self.thread.kill()
        for frame in aui_client_list:
            if isinstance(frame, ChildFrame):
                frame.OnCloseWindowAuto()
        if self.printTh.is_alive():
            self.printTh.stop()
        time.sleep(0.5)
        self._mgr.UnInit()
        self.Destroy()
    
    def OnAutoCloseWindow(self):
        """
        关闭主窗口，打开的标签页，log日志以及相关收尾工作--脚本控制
        :return: None
        """
        wx.TheClipboard.Flush()
        windows_list = self.GetChildren()
        aui_client_list = windows_list[0].GetChildren()
        if self.thread and isinstance(self.thread, ExThread):
            if self.thread.is_alive():
                self.thread.kill()
        for frame in aui_client_list:
            if isinstance(frame, ChildFrame):
                frame.OnCloseWindowAuto()
        if self.printTh.is_alive():
            self.printTh.stop()
        time.sleep(0.5)
        self._mgr.UnInit()
        self.Destroy()
    
    def MakeMenuBar(self):
        """
        设置Menu
        :return: None
        """
        mb = wx.MenuBar()
        menu = wx.Menu()
        # item = menu.Append(-1, "Connect\tCtrl-N")
        item = menu.Append(-1, "连接\tCtrl-N")
        self.Bind(wx.EVT_MENU, self.ConfigNewChannel, item)
        # item = menu.Append(-1, "Quick Connect")
        item = menu.Append(-1, "快速连接")
        self.Bind(wx.EVT_MENU, self._LoadChannelConfig, item)
        # item = menu.Append(-1, "Close Parent")
        item = menu.Append(-1, "关闭父窗口")
        self.Bind(wx.EVT_MENU, self.OnDoClose, item)
        # mb.Append(menu, "&File")  # 英文
        mb.Append(menu, "&文件")  # 中文
        
        menu = wx.Menu()
        # item = menu.Append(-1, "Clear Screen")
        item = menu.Append(-1, "清屏")
        self.Bind(wx.EVT_MENU, self.ClearFocus, item)
        # mb.Append(menu, "&Edit")  # 英文
        mb.Append(menu, "&编辑")  # 中文
        return mb
    
    @staticmethod
    def CloseLogger(logger):
        """
        关闭日志
        :param logger: 日志logger
        :return: None
        """
        close_logger(logger)
    
    @staticmethod
    def CloseAllLogger(logger_list):
        """
        关闭所有日志
        :param logger_list: 日志logger list
        :return: None
        """
        close_all_logger(logger_list)
    
    def OnPrintLogInfo(self, evt):
        """
        时间信息窗口（Leave your message below: Message 然后在当前时间)
        :param evt: 时间信息窗口事件
        :return: None
        """
        dlg = wx.TextEntryDialog(
            self, 'Leave your message below:', 'Message', '')
        if dlg.ShowModal() == wx.ID_OK:
            msg = dlg.GetValue()
        else:
            return 0
        dlg.Destroy()
        self.PrintLogInfo(msg)
    
    def PrintLogInfoAuto(self, msg=''):
        """
        alt+t 打印时间
        :param msg: 要打印到屏幕的信息
        :return:
        """
        page_list = self.GetPages()
        for page in page_list:
            sut = str(page)
            printScr(sut, msg)
        printRes(msg)
    
    def PrintLogInfo(self, msg=''):
        """
        "时间信息"窗口 打印时间
        :param msg: 要打印到屏幕的信息
        :return: None
        """
        print_str = '|[Message:' + msg + '] time:' + str(datetime.datetime.now()) + '|'
        print_separator = '+'
        
        for k in range(0, 42 + len(msg)):
            print_separator += '-'
            print_separator += '+'
        print_str = '\n' + print_separator + '\n' + print_str + '\n' + print_separator
        printAll(print_str)
    
    def OnStopSendMessage(self, evt):
        """
        停止向remote发送消息
        :param evt: 停止向remote发送消息事件
        :return: None
        """
        page_list = self.GetPages('page')
        for i in page_list:
            i.sendMessageFlag = not i.sendMessageFlag
    
    def OnScriptEdit(self, evt):
        """
        脚本编辑器窗口
        :param evt: 脚本编辑器窗口事件
        :return: None
        """
        dlg = EditDialog(self)
        dlg.CenterOnScreen()
        dlg.ShowModal()
        dlg.Destroy()
    
    def OnDoClose(self, evt):
        """
        关闭主窗口
        :param evt: 关闭主窗口事件
        :return: None
        """
        self.Close()
