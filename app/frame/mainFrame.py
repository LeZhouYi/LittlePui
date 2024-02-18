import tkinter as tk
from app.frame.sideBarFrame import SideBarFrame
from app.frame.pwdBookFrame import PwdBookFrame
from core.frame.absFrame import BaseFrame
from core.control.event import Event, WmEvent
from core.control.controller import Controller

class MainFrame(BaseFrame):
    def __init__(self,configFile:str) -> None:
        super().__init__(Controller(configFile))
        #初始化控件数据
        self.__initBaseData()
        self.loadBaseFrame()
        self.loadPage()
        # 显示窗口
        self.mainWindow.mainloop()

    def __initBaseData(self) -> None:
        """初始化主窗口"""
        self.mainWindow = tk.Tk()
        #基础配置
        self.mainWindow.geometry(self.getGeometry())
        self.mainWindow.title(self.getCnfData("windowTitle"))
        #绑定相关事件
        self.mainWindow.protocol(WmEvent.WindowClose, self.onWindowClose)
        self.mainWindow.bind(Event.WindowResize,self.onWindowResize)
        self.mainWindow.bind(Event.MouseWheel,self.onMouseScroll)
        # 缓存控件
        self.cacheWidget(self.mainWindow, None, "baseWindow")

    def onWindowClose(self) -> None:
        """处理窗口关闭事件"""
        # 获取窗口的宽度和高度
        width = self.mainWindow.winfo_width()
        height = self.mainWindow.winfo_height()
        # 获取窗口左上角在屏幕上的位置
        x = self.mainWindow.winfo_rootx()
        y = self.mainWindow.winfo_rooty()
        # 备份窗口信息
        self.setGeometry(width, height, x, y)
        self.getConfig().writeToFile()
        # 关闭窗口
        self.mainWindow.destroy()

    #     #######渲染页面相关############
    def loadBaseFrame(self) -> None:
        """渲染基础框"""
        self.createWidget("baseWindow","sideBarFrame")
        self.createWidget("baseWindow","contentFrame")

    def loadPage(self)->None:
        """加载页面"""
        if self.getPage().isNowPage("passwordDisplay"):
            SideBarFrame(self.getController()).loadSideBarFrame("sideBarFrame")
            PwdBookFrame(self.getController()).loadPasswordNote("contentFrame")

    def onWindowResize(self,event) -> None:
        """处理窗口刷新事件"""

    def onMouseScroll(self,event):
        """滚动事件"""
        x, y = self.mainWindow.winfo_pointerxy()
        if x>self.mainWindow.winfo_rootx()+self.getCnfData("sideBarWidth"):
            self.scrollCanvas(event)