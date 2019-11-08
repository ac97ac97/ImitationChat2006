"""好友聊天创库"""
import datetime
import json
import threading

from com.liyang.qq.client.my_frame import *


class ChatFrame(MyFrame):
    def __init__(self, friendsframe, user, friend):
        super().__init__(title='', size=(450, 400))
        self.friendsframe = friendsframe
        self.user = user
        self.friend = friend

        title = '{0}与{1}聊天中...'.format(user['username'], friend['user_name'])
        self.SetTitle(title)
        # 创建查看消息文本输入控件
        self.seemsg_tc = wx.TextCtrl(self.contentpanel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.seemsg_tc.SetFont(
            wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName='微软雅黑'))
        # 底部发送面板消息
        bottompanel = wx.Panel(self.contentpanel, style=wx.DOUBLE_BORDER)
        bottombox = wx.BoxSizer()
        # 创建发送消息文本输入控件
        self.seemsg_tc.SetFocus()
        # 创建发送消息文本输入控件设置焦点
        self.seemsg_tc.SetFont(
            wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName='微软雅黑'))

        sendmsg_btn = wx.Button(bottompanel, label='发送')
        self.Bind(wx.EVT_BUTTON, self.on_click, sendmsg_btn)
        bottombox.Add(self.seemsg_tc, 5, wx.CENTER | wx.ALL | wx.EXPAND, border=5)
        bottombox.Add(sendmsg_btn, 1, wx.CENTER | wx.ALL | wx.EXPAND, border=5)

        # 创建整体box布局管理对象
        box=wx.BoxSizer(wx.VERTICAL)
        box.Add(self.seemsg_tc ,5, wx.CENTER | wx.ALL | wx.EXPAND, border=5)
        box.Add(bottompanel, 5, wx.CENTER | wx.ALL | wx.EXPAND, border=5)
        self.contentpanel.SetSizer(box)

        #消息日志
        self.msglog=''

    def on_click(self,event):
        #发送消息
        pass

#接收消息
    def OnClose(self,event):
        # 停止当前线程
        self.isrunning=False
        self.t1.join()
        self.Hide()

        #重启好友列表窗口子程序
        # self.friendsframe.resetthread()


