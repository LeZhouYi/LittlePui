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

    def getPackCnf(self, key) -> dict:
        return self.getStyle().getPackCnf(key)

    def getCnf(self, key) -> dict:
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
        return self.getConfig().getData("windowSize")[0] - self.getConfig().getData(
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
        windowSize = self.getConfig().getData("windowSize")
        windowPosition = self.getConfig().getData("windowPosition")
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

    def createFrame(self, parentKey: str, key: str, extra: dict = None) -> tk.Frame:
        """创建Frame"""
        cnf = self.getCnf(key)
        if cnf != None and extra != None:
            cnf.update(extra)
        frame = tk.Frame(self.getWidget(parentKey), cnf=cnf)
        self.cacheWidget(frame, parentKey, key)
        return self.getWidget(key)

    def createLabel(self, parentKey: str, key: str, extra: dict = None) -> tk.Label:
        """创建Label"""
        cnf = self.getCnf(key)
        if cnf != None and extra != None:
            cnf.update(extra)
        label = tk.Label(self.getWidget(parentKey), cnf=cnf)
        self.cacheWidget(label, parentKey, key)
        return self.getWidget(key)

    def createCanvas(self, parentKey: str, key: str, extra: dict = None) -> tk.Canvas:
        """创建Canvas"""
        cnf = self.getCnf(key)
        if cnf != None and extra != None:
            cnf.update(extra)
        label = tk.Canvas(self.getWidget(parentKey), cnf=cnf)
        self.cacheWidget(label, parentKey, key)
        return self.getWidget(key)

    def createScrollBar(
        self, parentKey: str, key: str, extra: dict = None
    ) -> tk.Scrollbar:
        """创建Scrollbar"""
        cnf = self.getCnf(key)
        if cnf != None and extra != None:
            cnf.update(extra)
        label = tk.Scrollbar(self.getWidget(parentKey), cnf=cnf)
        self.cacheWidget(label, parentKey, key)
        return self.getWidget(key)

    def createEntry(self, parentKey: str, key: str, extra: dict = None) -> tk.Entry:
        """创建Entry"""
        cnf = self.getCnf(key)
        if cnf != None and extra != None:
            cnf.update(extra)
        label = tk.Entry(self.getWidget(parentKey), cnf=cnf)
        self.cacheWidget(label, parentKey, key)
        return self.getWidget(key)

    def createDialog(self, parentKey: str, key: str, extra: dict = None) -> tk.Toplevel:
        """创建Dialog"""
        cnf = self.getCnf(key)
        if cnf != None and extra != None:
            cnf.update(extra)
        label = tk.Toplevel(self.getWidget(parentKey), cnf=cnf)
        self.cacheWidget(label, parentKey, key)
        return self.getWidget(key)



    def replaceText(self, key: str, text: str):
        """替换按钮文本"""
        sleep(2)
        self.getWidget(key).config(text=text)

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
        print(widgetKey)
        return widgetKey
