#定义窗口frame基类

import logging
import socket
import sys
import wx

logger = logging.getLogger(__name__)

#服务端IP
SERVER_IP='127.0.0.1'
#服务器端口号
SERVER_PORT=8888

#服务器地址
server_address=(SERVER_IP,SERVER_PORT)

#操作命令代码
COMMAND_LOGIN=1 #登录命令
COMMAND_LOGOUT=2 #下线命令
COMMAND_SENDNSG=3 #发消息命令
COMMAND_REFRESH=4 #刷新好友列表命令

client_socket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#设置超时1秒不再接收消息
client_socket.settimeout(1)

class MyFrame(wx.Frame):

    def __init__(self,title,size):
        super().__init__(parent=None,title=title,size=size,style=wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX)

        self.Center()
        self.contentpanel=wx.Panel(parent=self)
        icon=wx.Icon('F:\\Python_project\\QQ2006\\resources\\icon\\qq.jpg',wx.BITMAP_TYPE_JPEG)
        # 设置窗口图标
        self.SetIcon(icon)
        # 设置窗口的最大和最想尺寸
        self.SetSizeHints(size,size)
        self.Bind(wx.EVT_CLOSE,self.OnClose)
    def OnClose(self,evt):
        # 退出系统
        # 退出占有资源
        self.Destroy()
        client_socket.close()
        # 退出系统
        sys.exit(0)

