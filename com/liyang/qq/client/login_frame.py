"""用户登录窗口"""
import json

from com.liyang.qq.client.my_frame import *
from com.liyang.qq.client.friends_frame import FriendsFrame


class LoginFrame(MyFrame):
    def __init__(self):
        super().__init__(title='QQ 登录', size=(340, 255))
        # 创建顶部图片
        topimage = wx.Bitmap('F:\\Python_project\\QQ2006\\resources\\images\\qq11.png', wx.BITMAP_TYPE_PNG)
        topimage_sb = wx.StaticBitmap(self.contentpanel, bitmap=topimage)

        # 创建界面控件
        middlepannel = wx.Panel(self.contentpanel, style=wx.BORDER_DOUBLE)

        accountid_st = wx.StaticText(middlepannel, label='QQ号码')
        password_st = wx.StaticText(middlepannel, label='QQ密码')
        self.accountid_txt = wx.TextCtrl(middlepannel)
        self.password_txt = wx.TextCtrl(middlepannel, style=wx.TE_PASSWORD)

        st = wx.StaticText(middlepannel, label='忘记密码')
        st.SetForegroundColour(wx.BLUE)

        # 创建flexgrid布局fgs对象
        fgs = wx.FlexGridSizer(3, 3, 8, 15)
        fgs.AddMany([
            (accountid_st, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE),
            (self.accountid_txt, 1, wx.CENTER | wx.EXPAND),
            wx.StaticText(middlepannel),
            (password_st, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE),
            (self.password_txt, 1, wx.CENTER | wx.EXPAND),
            (st, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE),
            wx.StaticText(middlepannel),
            (wx.CheckBox(middlepannel, -1, '自动登录'), 1, wx.CENTER | wx.EXPAND),
            (wx.CheckBox(middlepannel, -1, '隐身登录'), 1, wx.CENTER | wx.EXPAND)
        ])

        # 设置FlexGrid布局对象
        fgs.AddGrowableRow(0, 1)
        fgs.AddGrowableRow(1, 1)
        fgs.AddGrowableCol(0, 1)
        fgs.AddGrowableCol(1, 1)
        fgs.AddGrowableCol(2, 1)

        panelbox = wx.BoxSizer()
        panelbox.Add(fgs, 1, wx.CENTER | wx.ALL | wx.EXPAND, border=10)
        middlepannel.SetSizer(panelbox)

        # 创建按扭对象
        okb_btn = wx.Button(parent=self.contentpanel, label='确定')
        self.Bind(wx.EVT_BUTTON, self.okb_btn_onclick, okb_btn)

        cancel_btn = wx.Button(parent=self.contentpanel, label='取消')
        self.Bind(wx.EVT_BUTTON, self.cancel_btn_onclick, cancel_btn)

        # 创建水平的hbox对象
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(wx.Button(parent=self.contentpanel, label='申请号码'), 1, wx.CENTER | wx.ALL | wx.EXPAND, border=10)
        hbox.Add(okb_btn, 1, wx.CENTER | wx.ALL | wx.EXPAND, border=10)
        hbox.Add(cancel_btn, 1, wx.CENTER | wx.ALL | wx.EXPAND, border=10)
        # 创建垂直box将fgs和hbox添加到垂直box上
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(topimage_sb, -1, wx.CENTER | wx.EXPAND)
        vbox.Add(middlepannel, -1, wx.CENTER | wx.ALL | wx.EXPAND, border=5)
        vbox.Add(hbox, -1, wx.CENTER | wx.BOTTOM, border=1)
        self.contentpanel.SetSizer(vbox)

    def okb_btn_onclick(self, event):
        # 确定按钮事件处理
        account = self.accountid_txt.GetValue()
        password = self.password_txt.GetValue()
        user = self.login(account, password)
        # 加入线程后修改此处if语句
        if user is not None:
            logger.info('登录成功')
            next_frame = FriendsFrame(user)
            next_frame.Show()
            self.Hide()

        else:
            logger.info('登录失败')
            dlg = wx.MessageDialog(self, '您的QQ号或密码不正确', '登录失败', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

    def cancel_btn_onclick(self, event):
        # 取消按钮事件
        self.Destroy()
        sys.exit(0)

    def login(self, userid, password):
        """客户端向服务端发送登录请求"""
        # 登录处理
        json_obj = {}
        json_obj['command'] = COMMAND_LOGIN
        json_obj['user_id'] = userid
        json_obj['user_pwd'] = password
        # Json编码
        json_str = json.dumps(json_obj)
        # 给服务器发送数据
        client_socket.sendto(json_str.encode(), server_address)
        # 从服务器端接收数据
        json_data, _ = client_socket.recvfrom(1024)
        # json解码
        json_obj = json.loads(json_data.decode())
        logger.info('从服务端获接收数据：{0}'.format(json_obj))

        if json_obj['result'] == 0:
            #登录成功
            return json_obj
