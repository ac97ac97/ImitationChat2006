""""客户端启动模块"""
import logging
import wx
from com.liyang.qq.client.login_frame import LoginFrame

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(threadName)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
logger=logging.getLogger(__name__)

class App(wx.App):
    def OnInit(self):
        # 创建窗口对象
        loginFrame = LoginFrame()
        loginFrame.Show()
        return True


if __name__ == '__main__':
    app = App()
    app.MainLoop()  # 进入主事件循环