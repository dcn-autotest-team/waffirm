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


import os
# ----------------------------------------------------------------------
# 子框架：在打开连接时创建
# from wx.lib.pubsub import setuparg1
# from wx.lib.pubsub import pub as Publisher
import re
import time

# from wx import wx
import wx
import wx.aui
from dautolibrary.dautocomponents.dstyle import loadStyleConfig
from dautolibrary.dautoconst import OS_TYPE as os_type
from dautolibrary.dautopyte import DcnPyte
from dautolibrary.dautothread.readthread import ReadThread
from dautolibrary.dautotplibrary.pyte import ByteStream
from dautolibrary.dautoutils.dautotools import call_after
from dtestlink.dcntestlink.dcntestlinkoperate import DautoTestlinkOperate
from dutils.dcnlogs.dcnuserlog import DcnLog, close_logger
from dutils.dcnprint import printResError, printResWarn

"""
命令不符合PEP8规范，后续需要处理使其符合PEP8规范
需要整改的地方为此处的file_path没有实际使用意义，后续需要合理处理该处内容
"""


class ChildFrame(wx.aui.AuiMDIChildFrame):
    """
    创建Dauto平台子窗口，继承自wx.aui.AuiMDIChildFrame
    主要作用：
    远程连接serial telnet ssh（后续支持）服务器的时候生成子窗口用于会话交互输入输出
    """
    __slots__ = ('title', 'sendMessageFlag', 'pagename', 'namelist', 'conn', 'insertPoint', 'childid', 'parent'
                                                                                                       'fontsize',
                 'cut_line_times', 'res', 'resflag', 'debugres', 'debugflag', 'log_buffer', 'log_type'
                                                                                            'last_enter_pos',
                 'logprefix', 'logger', 'file_path', 'thread1',
                 'onKeyUpCode', 'onKeyDownCode', 'onCtrlDownFlag', 'showPositionFlag', 'page', 'lock')
    
    def __init__(self, parent, child_id, child_title, child_name, conn, path=None, log_type='default', log_prefix=''):
        """
        初始化子窗口
        :param parent:ParentFrame ，Dauto平台ParentFrame
        :param child_id: 窗口ID 用户查找定位该窗口
        :param child_title: 连接的时候输入host 例如 172.17.100.100
        :param child_name: 设备的名称 例如s1 s2
        :param conn: 远程连接服务实例，例如telnet_lib,用于跟远程串口服务器进行输入和输出交互，判断远程连接状态等
        :param path: log日志路径
        :param log_type: 日志类型 run or default
        :param log_prefix: 日志前缀名称
        """
        super().__init__(parent, child_id,
                         title='(' + str(child_id) + ')' + child_title + '(' + child_name + ')',
                         name=child_name, style=wx.DEFAULT_FRAME_STYLE | wx.WANTS_CHARS)
        
        self.title = child_title
        self.parent = parent
        self.sendMessageFlag = True
        self.pagename = child_name
        self.namelist = []
        self.conn = conn
        self.insertPoint = 0
        self.childid = child_id
        self.fontsize = 10
        self.cut_line_times = 0
        self.res = ''
        self.resflag = 1
        self.debugres = ''
        self.debugflag = 0  # debug打开记录日志
        self.log_buffer = ''
        self.log_type = log_type
        self.last_enter_pos = 0
        self.logprefix = log_prefix
        self.log_final_path = path
        self.dp = DcnPyte()
        self.bs = ByteStream(self.dp)
        self.patten_rule = re.compile('(.*?)([->!\#:/_@\w \,\.\,\(\)\[\]]+)', re.S)
        # 编码处理(oh)
        self.ascii_temp = ''
        self.codetype = 'ascii'
        """
        脚本打开窗口默认运行最后分支
        手工打开窗口如果没有填写日志路径不记录日志，如果指定日志路径，按照指定的日志路径记录日志
        """
        if self.log_final_path and self.log_final_path != 'None':
            self.logger = DcnLog(log_final_path=self.log_final_path).create_log(self.parent.log_config_file)
        elif self.log_type == 'default' and self.log_final_path == 'None' and self.logprefix == '':
            self.logger = None
        else:
            self.logger = DcnLog(log_base_path=self.parent.log_base_path, log_define_type=self.log_type,
                                 prefix_log_name=self.logprefix,
                                 page_name=self.pagename,
                                 title_name=self.title).create_log(self.parent.log_config_file)
        self.onKeyUpCode = ''
        self.onKeyDownCode = ''
        self.onCtrlDownFlag = False
        self.showPositionFlag = True
        
        self.page = wx.TextCtrl(self, int(child_id) + 100, "",
                                style=wx.TE_MULTILINE | wx.TE_NOHIDESEL | wx.TE_PROCESS_TAB | wx.TE_READONLY |
                                      wx.TE_RICH2)
        # 修复新版本wxpython tab的时候 focus到串口窗口的标题栏（例如（1）172.17.100.20（1）
        self.page.GetParent().SetWindowStyle(wx.DEFAULT_FRAME_STYLE ^ wx.TE_PROCESS_TAB)
        self.page.GetGrandParent().SetWindowStyle(wx.DEFAULT_FRAME_STYLE ^ wx.TE_PROCESS_TAB)
        
        font = wx.Font(self.fontsize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.page.SetFont(font)
        font = wx.SystemSettings.GetFont(wx.SYS_SYSTEM_FONT)  # 获取操作系统字体
        stylelist = loadStyleConfig()[0]
        self.page.SetForegroundColour(stylelist[3])
        self.page.SetBackgroundColour(stylelist[2])
        
        self.page.Bind(wx.EVT_CHAR, self.KeyPress)
        self.page.Bind(wx.EVT_LEFT_UP, self.LeftMouseUp)
        self.page.Bind(wx.EVT_LEFT_DOWN, self.LeftMouseClick)
        self.page.Bind(wx.EVT_MIDDLE_UP, self.MiddleMouseDclick)
        self.page.Bind(wx.EVT_MIDDLE_DOWN, self.MiddleMouseDown)
        self.page.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.page.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        # self.page.popupmenu = wx.Menu()
        # for text in "copy paste SelectAll".split():
        #     item = self.page.popupmenu.Append(-1, text)
        #     self.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)
        # self.page.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)
        
        wx.CallAfter(self.page.SetFocus)
        sizer = wx.BoxSizer()
        sizer.Add(self.page, 1, wx.EXPAND)
        self.SetSizer(sizer)
        wx.CallAfter(self.Layout)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        self.thread1 = ReadThread(self.title, self, self.conn, self.consumer())  # 协程实现部分代码
        wx.CallAfter(self.thread1.start)
    
    def set_log_path(self):
        """
        设置log日志路径以及log格式
        :return: 生成日志的路径
        """
        _current_time = time.strftime('[%Y-%m-%d][%H-%M-%S]', time.localtime())
        _path = os.path.join(self.parent.local_dir, 'logs', self.log_type)
        _filename = self.logprefix + self.pagename + '[' + self.title + ']' + _current_time + '.log'
        if not os.path.exists(_path):
            os.mkdir(_path)
        return os.path.join(_path, _filename)
    
    def onKeyDown(self, evt):
        """
        用于控制ctrl-c\ctrl-v\ctrl-a等系统有定义的组合键
        :param evt: 键盘按下的时候产生的系统事件
        :return: None
        """
        self.onKeyDownCode = evt.GetKeyCode()
        if self.onKeyDownCode == 308:
            self.onCtrlDownFlag = True
        if self.onKeyDownCode == 13:
            self.WriteChannel('\x0D')
        elif self.onKeyDownCode == 393:  # 过滤掉Windows Key键
            pass
        elif self.onKeyDownCode == 8:
            self.WriteChannel('\x08')
        elif self.onCtrlDownFlag:
            if self.onKeyDownCode == 67:
                self.OnPressCtrlC(evt)
            elif self.onKeyDownCode == 86:
                self.OnPressCtrlV(evt)
            elif self.onKeyDownCode == 88:
                self.WriteChannel('\x18')
            elif self.onKeyDownCode == 65:
                self.OnPressCtrlA(evt)
            elif self.onKeyDownCode == 54:
                self.WriteChannel('\x1E')
            else:
                evt.Skip()
        else:
            evt.Skip()
    
    def onKeyUp(self, evt):
        """
        用于控制ctrl-c\ctrl-v\ctrl-a等系统有定义的组合键
        :param evt: 键盘弹起的时候产生的系统事件
        :return: None
        """
        self.onKeyUpCode = evt.GetKeyCode()
        if self.onKeyUpCode == 308:
            self.onCtrlDownFlag = False
        evt.Skip()
    
    def OnShowPopup(self, evt):
        """
        右键弹出窗口
        :param evt: 鼠标右键产生的系统事件
        :return: None
        """
        pos = evt.GetPosition()
        pos = self.page.ScreenToClient(pos)
        self.page.PopupMenu(self.page.popupmenu, pos)
    
    def OnPopupItemSelected(self, evt):
        """
        右键弹出窗口选定，兼容linux平台
        :param evt: 鼠标右键选定产生的系统事件
        :return: None
        """
        item = self.page.popupmenu.FindItemById(evt.GetId())
        text = item.GetText()
        if text == 'SelectAll':
            self.page.SelectAll()
        elif text == 'copy':
            selection = self.page.GetSelection()
            if selection[1] == selection[0]:
                pass
            else:
                selection_data = self.page.GetRange(selection[0], selection[1])
                selection_data = wx.TextDataObject(selection_data)
                if wx.TheClipboard.Open():
                    wx.TheClipboard.SetData(selection_data)
                    wx.TheClipboard.Close()
        elif text == 'paste':
            if os_type.find('Linux') >= 0:
                pass
            elif os_type.find('Windows') >= 0:
                text_data = wx.TextDataObject()
                if wx.TheClipboard.Open():
                    wx.TheClipboard.GetData(text_data)
                    wx.TheClipboard.Close()
                    ChildFrame.WriteChannel(self, text_data.GetText())
    
    def OnPressCtrlC(self, evt):
        """
        控制ctrl-c
        :param evt: ctrl-c事件
        :return: None
        """
        selection = self.page.GetSelection()
        if selection[1] == selection[0]:
            ChildFrame.WriteChannel(self, '\x03')
        else:
            selection_data = self.page.GetRange(selection[0], selection[1])
            selection_data = wx.TextDataObject(selection_data)
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(selection_data)
                wx.TheClipboard.Close()
    
    def OnPressCtrlV(self, evt):
        """
        控制ctrl-v
        :param evt: ctrl-v 事件
        :return: None
        """
        if os_type.find('Linux') >= 0:
            pass
        elif os_type.find('Windows') >= 0:
            text_data = wx.TextDataObject()
            if wx.TheClipboard.Open():
                wx.TheClipboard.GetData(text_data)
                wx.TheClipboard.Close()
                ChildFrame.WriteChannel(self, text_data.GetText())
    
    def OnPressCtrlA(self, evt):
        """
        控制ctrl-a
        :param evt: ctrl-a事件
        :return: None
        """
        ChildFrame.WriteChannel(self, '\x01')
    
    def WriteChannel(self, input_str):
        """
        程序通过SetCmd命令往终端发送命令
        :param input_str: 输入命令内容
        :return: 0 表示终止发送消息 1 成功发送消息 2 读取远程终端信息线程重启失败 3 远程终端连接失败
        """
        try:
            if not self.sendMessageFlag:
                return 0  # 表明停止串口输入对应toolbar中的Stop Send Message
            if self.thread1.isAlive():
                if self.thread1.channel.connected:
                    self.thread1.channel.writeChannel(input_str)  # 窗口线程存在，并且远端串口连接成功执行写入操作
                    return 1
                else:
                    printResWarn('[告警]进入自动重连模式...')
                    if self.thread1.channel.reconnectChannel() and self.thread1.channel.connected:
                        self.thread1.channel.writeChannel(input_str)
                        return 1
                    else:
                        printResWarn('[告警]重连失败')
                        return 3
            else:
                printResWarn('[告警]远程连接线程不是alive状态!')  # 读取远程终端信息线程is not alive时候重启线程
                if self.thread1.channel.reconnectChannel() and self.thread1.channel.connected:
                    self.thread1.stop()
                    self.thread1 = ReadThread(self.title, self, self.conn, self.consumer())  # 协程实现
                    self.thread1.start()
                    if self.thread1.isAlive():
                        self.thread1.channel.writeChannel(input_str)
                        return 1
                    else:
                        printResWarn('[告警]远程连接线程重启失败!')
                        return 2
                else:
                    printResWarn('[告警]重连失败')
                    return 3
        except BaseException as e:
            printResError('[异常]往远程终端服务器命发送命令异常: {}'.format(e))
    
    def WriteTextCtrl(self, raw_msg):
        """
        1 记录log信息，并且返回self.res记录remote返回信息
        2 处理remote发送回来的raw_msg（回显，响应回车空格换行等）
        说明 后续支持其他特性在此处扩展即可（Core）
        :param raw_msg:(linux)服务器传输过来的原始字符串
        :return:None
        """
        if self.page.GetLastPosition() >= 300000:
            self.SetInsertPoint()
            self.page.Remove(0, 60000)
            self.insertPoint = self.insertPoint - 60000
        try:
            # 写入log
            print2debug = re.sub('\r', '', raw_msg.decode('utf-8'))
            self.res = f'{self.res}{print2debug}'
            if self.debugflag == 1:
                self.debugres = f'{self.debugres}{print2debug}'
            self.SetInsertionPointLocal(self.insertPoint)
            self.bs.feed(raw_msg)
            msg = self.dp.msg
            if msg:
                for _msg in msg:
                    data, cmd = _msg.args, _msg.name
                    if 'carriage_return' == cmd:  # 归位
                        self.page.SetInsertionPointEnd()
                        self.insertPoint = self.page.GetInsertionPoint()
                        self.SetInsertionPointLocal(
                            self.insertPoint - self.page.GetLineLength(self.page.GetNumberOfLines()))
                    elif 'linefeed' == cmd:  # 换行
                        self.page.SetInsertionPointEnd()
                        linetemp = self.page.GetRange(self.last_enter_pos, self.page.GetInsertionPoint())
                        self.last_enter_pos = self.page.GetInsertionPoint() + 1
                        self.page.AppendText('\n')
                        if self.logger:
                            self.logger.info(linetemp)
                    elif 'backspace' == cmd:  # 回格
                        self.SetInsertionPointLocal(self.insertPoint - 1)
                    elif 'erase_in_display' == cmd and data:  # 擦除回显：
                        data = int(data[0])
                        if data == 0:  # -- Erases from cursor to end of screen, including cursor position.
                            erase_length = self.page.GetLineLength(self.page.GetNumberOfLines()) - self.insertPoint
                            self.page.Replace(self.insertPoint, erase_length, '')
                        elif data == 1:  # `1`` -- Erases from beginning of screen to cursor
                            pass  # 目前暂不实现
                        elif data == 2 or 3:  # 2 or 3 --- Erases complete display
                            pass  # 目前暂不实现
                    elif 'bell' == cmd:
                        wx.Bell()  # 响铃，发声
                    elif 'draw' == cmd and data:  # 回显字符串
                        try:
                            data = data[0]
                        except Exception:
                            pass
                        else:
                            self.page.Replace(self.insertPoint, self.insertPoint + len(data), data)
                    self.insertPoint = self.page.GetInsertionPoint()
        except Exception as e:
            printResError('[异常]将远端服务器返回信息解析并写入打开的窗口异常，异常信息如下:{}'.format(e))
    
    def SetInsertionPointLocal(self, pos):
        """
        可控制的设置光标位置，如果showPositionFlag为真，不执行操作
        :param pos: 光标位置
        :return: None
        """
        if self.showPositionFlag:
            self.page.SetInsertionPoint(pos)
    
    def ReturnRes(self):
        """
        返回屏幕打印信息：如Receiver
        :return: 屏幕打印信息
        """
        return self.res
    
    # 关闭标签
    @call_after
    def OnCloseWindow(self, evt):
        """
        关闭窗口，同时后续扩展响应关闭窗口的事件，同时跟testlink服务器联动
        :param evt: 关闭串口
        :return: None
        """
        DautoTestlinkOperate().tl_on_close_window()
        
        close_logger(self.logger)
        self.logger = None
        self.thread1.stop()
        self.parent.childnamelist.remove(self.pagename)
        if self.childid < 10:
            self.parent.countlist.append(self.childid)
            self.parent.countlist.sort()
        time.sleep(0.5)
        self.Destroy()
    
    # 脚本关闭标签
    def OnCloseWindowAuto(self):
        """
        关闭窗口，同时跟testlink服务器联动
        :return: None
        """
        close_logger(self.logger)
        self.logger = None
        self.thread1.stop()
        self.parent.childnamelist.remove(self.pagename)
        if self.childid < 10:
            self.parent.countlist.append(self.childid)
            self.parent.countlist.sort()
        time.sleep(0.5)
        self.Destroy()
    
    def BackspaceEve(self):
        """
        处理退格
        :return: None
        """
        self.SetInsertPoint()
        if self.insertPoint > 0:
            self.insertPoint = self.insertPoint - 1
        self.page.SetInsertionPoint(self.insertPoint)
    
    def RightMouseClick(self, evt):
        """
        处理鼠标右键点击
        :param evt: 鼠标右键事件
        :return: None
        """
        pass
    
    def LeftMouseClick(self, evt):
        """
        处理鼠标左键点击
        :param evt: 鼠标左键点击事件
        :return: None
        """
        if not self.showPositionFlag:
            pass
        else:
            evt.Skip()
    
    def LeftMouseUp(self, evt):
        """
        处理鼠标左键弹起
        :param evt: 鼠标左键弹起事件
        :return: None
        """
        selection = self.page.GetSelection()
        if selection[1] == selection[0]:
            pass
        else:
            selection_data = self.page.GetRange(selection[0], selection[1])
            selection_data = wx.TextDataObject(selection_data)
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(selection_data)
                wx.TheClipboard.Close()
        evt.Skip()
    
    def MiddleMouseDclick(self, evt):
        """
        处理鼠标中键双击点击
        :param evt: 中键双击点击事件
        :return: None
        """
        text_data = wx.TextDataObject()
        if wx.TheClipboard.Open():
            wx.TheClipboard.GetData(text_data)
            wx.TheClipboard.Close()
            ChildFrame.WriteChannel(self, text_data.GetText())
        evt.Skip()
    
    def MiddleMouseDown(self, evt):
        """
        处理鼠标中键按下点击
        :param evt: 中键按下事件
        :return: None
        """
        pass
    
    def SetInsertPoint(self):
        """
        设置光标位置-插入
        :return: None
        """
        insert_point = self.page.GetInsertionPoint()
        if insert_point > self.insertPoint:
            self.insertPoint = insert_point
    
    def KeyPress(self, evt):
        """
        处理键盘事件支持特殊字符如下
        alt-1 2 3 4...切换到对应子窗口
        alt-t 打印时间
        shift+v 复制
        上下左右
        page up和page down
        :param evt: 键盘按下事件
        :return:
        """
        key_code = evt.GetKeyCode()
        uni_chr = ''
        if "unicode" in wx.PlatformInfo:
            uni_chr = chr(key_code)
        if evt.AltDown():
            if 49 <= key_code <= 57:
                tab_focus = wx.FindWindowById(key_code + 52)
                if tab_focus:
                    tab_focus.SetFocus()
                    # 打印时间->"Alt-t"
            elif key_code == 116:
                self.parent.PrintLogInfo()
        elif evt.ShiftDown() and key_code == 322:
            self.OnPressCtrlV(evt)
        # 处理上下左右
        elif key_code == wx.WXK_UP:
            ChildFrame.WriteChannel(self, '\x1B\x5B\x41')
        elif key_code == wx.WXK_DOWN:
            ChildFrame.WriteChannel(self, '\x1B\x5B\x42')
        elif key_code == wx.WXK_LEFT:
            ChildFrame.WriteChannel(self, '\x1B\x5B\x44')
        elif key_code == wx.WXK_RIGHT:
            ChildFrame.WriteChannel(self, '\x1B\x5B\x43')
        elif key_code == wx.WXK_PAGEUP:
            self.page.ScrollPages(-1)
        elif key_code == wx.WXK_PAGEDOWN:
            self.page.ScrollPages(1)
        else:
            ChildFrame.WriteChannel(self, uni_chr)
    
    def consumer(self):
        """
        # 协程实现部分代码
        :return:msg
        :rtype:str
        """
        while 1:
            msg = yield
            if not msg:
                return
            self.dp.msg = []
            self.WriteTextCtrl(msg)
