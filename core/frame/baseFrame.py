import threading
import tkinter as tk
from time import sleep
from core.config.config import Config
from core.control.page import Page
from core.control.style import Style
from core.control.widget import WidgetController
from core.control.thread import ThreadController
from core.control.source import ImageController
from core.control.controller import Controller
from core.utils import utils


class BaseFrame:
    def __init__(self, controller: Controller) -> None:
        self.__controller = controller  # 控制器

    def getConfig(self) -> Config:
        return self.__controller.getConfig()

    def getWC(self) -> WidgetController:
        return self.__controller.getWC()

    def getTC(self) -> ThreadController:
        return self.__controller.getTC()

    def getStyle(self) -> Style:
        return self.__controller.getStyle()

    def getCnfData(self,key:str)->any:
        """获取配置数据"""
        return self.getConfig().getData(key)

    def getPackCnf(self, key:str) -> dict:
        """获取控件布局信息"""
        return self.getStyle().getPackCnf(key)

    def getCnf(self, key) -> dict:
        """获取控件初始化信息"""
        return self.getStyle().getCnf(key)

    def getPage(self) -> Page:
        return self.__controller.getPage()

    def getIC(self) -> ImageController:
        return self.__controller.getIC()

    def cacheImage(self, image: tk.PhotoImage, key: str, group: str):
        """缓存图片资源"""
        self.getIC().cacheImage(image, key, group)

    def getImage(self, key: str, group: str) -> tk.PhotoImage:
        """获得图片"""
        return self.getIC().getImage(key, group)

    def cacheWidget(self, widget: tk.Widget, parentKey: str, key: str) -> None:
        """缓存控件"""
        cnf=self.getPackCnf(key)
        if cnf!=None:
            widget.pack_configure(cnf=cnf)
        self.getWC().cacheWidget(widget, parentKey, key)

    def getWidget(self, key: str) -> tk.Widget:
        """获取控件"""
        return self.getWC().getWidget(key)

    def getController(self) -> Controller:
        return self.__controller

    def updateCanvas(self, canvas: tk.Canvas, frame: tk.Frame, parentKey: str):
        """更新滚动画布控件"""
        self.getWidget(parentKey).update()
        canvas.config(
            scrollregion=(0, 0, frame.winfo_width(), frame.winfo_height()),
            width=frame.winfo_width(),
            height=frame.winfo_height(),
        )

    def refreshCanvas(self, pageKey: str = None):
        """刷新当前页面"""
        pageWidgetKeys = self.getPage().resizeKeys(pageKey)
        scrollCanvas = self.getWidget(pageWidgetKeys[0])
        contentFrame = self.getWidget(pageWidgetKeys[1])
        scrollCanvas.create_window(
            0,
            0,
            width=self.getContentWidth(),
            window=contentFrame,
            anchor=tk.NW,
        )
        self.updateCanvas(scrollCanvas, contentFrame, pageWidgetKeys[2])  # 更新

    def getContentWidth(self) -> int:
        """获取内容页宽度"""
        return self.getCnfData("windowSize")[0] - self.getCnfData(
            "sideBarWidth"
        )

    def scrollCanvas(self, event, pageKey: str = None):
        """滚动当前页面"""
        pageWidgetKeys = self.getPage().resizeKeys(pageKey)
        scrollCanvas = self.getWidget(pageWidgetKeys[0])
        scrollCanvas.yview_scroll(-2 * (event.delta), tk.UNITS)

    def cacheThread(self, func, key: str, args: tuple = ()):
        """缓存线程并执行"""
        self.getTC().cacheThread(
            threading.Thread(target=func, args=args, daemon=True), key
        )

    def destroyWidget(self, key: str):
        """清除该控件及子控件"""
        self.getWC().destroyWidget(key)

    def getGeometry(self) -> str:
        """获取窗口大小/位置"""
        windowSize = self.getCnfData("windowSize")
        windowPosition = self.getCnfData("windowPosition")
        return "%dx%d+%d+%d" % (
            windowSize[0],
            windowSize[1],
            windowPosition[0],
            windowPosition[1],
        )

    def setGeometry(self, width: int, height: int, x: int, y: int) -> None:
        """记录窗口大小/位置"""
        self.getConfig().setData("windowSize", [width, height])
        self.getConfig().setData("windowPosition", [x, y])

    def replaceText(self, before:str ,key: str, after: str):
        """替换按钮文本,用于提示错误信息并2秒后替换回原文"""
        self.getWidget(key).config(text=before)
        sleep(2)
        self.getWidget(key).config(text=after)

    def createWidget(self, parentKey: str, key: str, extra: dict = None, *args) -> str:
        """创建控件并返回该控件名"""
        #获取配置数据并合并
        cnf = self.getCnf(key)
        if cnf != None and extra != None:
            cnf.update(extra)
        #获取构造方法并构造
        widgetFunc = self.getStyle().getType(key)
        widget = widgetFunc(self.getWidget(parentKey), cnf=cnf)
        #创建唯一键名并缓存
        widgetKey = utils.createKey(key, *args)
        self.cacheWidget(widget, parentKey, widgetKey)
        return widgetKey

    def packCenter(self,mainWindow:tk.Widget,dialog:tk.Widget)->None:
        """计算并使弹窗显示在主窗口中心"""
        winX = (
            mainWindow.winfo_rootx()
            + (mainWindow.winfo_width() // 5)*2
        )
        winY = (
            mainWindow.winfo_rooty()
            + (mainWindow.winfo_height() // 5)*2
        )
        dialog.geometry("+{}+{}".format(winX, winY))

    def packDialog(self,mainWindow:tk.Widget,dialog:tk.Widget)->None:
        """禁用主窗口等待弹窗"""
        mainWindow.update_idletasks()
        dialog.transient(mainWindow)
        dialog.grab_set()
        mainWindow.wait_window(dialog)

    def bindScroll(self,canvasKey:str,scrollKey:str,isVertical:bool=True,crement:int=5)->None:
        """绑定滚动条"""
        canvas = self.getWidget(canvasKey)
        scrollBar = self.getWidget(scrollKey)
        if isVertical:
            canvas.config(yscrollcommand=scrollBar.set, yscrollincrement=crement)
            scrollBar.config(command=canvas.yview)
        else:
            canvas.config(xscrollcommand=scrollBar.set, xscrollincrement=crement)
            scrollBar.config(command=canvas.xview)