import threading
import tkinter as tk
from config.config import Config
from config.page import Page
from control.style import Style
from control.widgetControl import WidgetController
from control.threadControl import ThreadController
from control.sourceControl import ImageController
from control.controller import Controller


class BaseFrame:
    def __init__(self, controller: Controller) -> None:
        self.__controller = controller  # 控制器

    def getConfig(self) -> Config:
        return self.__controller.getConfig()

    def getWidgetController(self) -> WidgetController:
        return self.__controller.getWidgetController()

    def getThreadController(self) -> ThreadController:
        return self.__controller.getThreadController()

    def getStyle(self) -> Style:
        return self.__controller.getStyle()

    def getPackCnf(self, key) -> dict:
        return self.getStyle().getPackCnf(key)

    def getCnf(self, key) -> dict:
        return self.getStyle().getCnf(key)

    def getPage(self) -> Page:
        return self.__controller.getPage()

    def getImageController(self) -> ImageController:
        return self.__controller.getImageController()

    def cacheImage(self, image: tk.PhotoImage, key: str, group: str):
        """缓存图片资源"""
        self.getImageController().cacheImage(image, key, group)

    def getImage(self, key: str, group: str) -> tk.PhotoImage:
        """获得图片"""
        return self.getImageController().getImage(key, group)

    def cacheWidget(self, widget: tk.Widget, parentKey: str, key: str) -> None:
        """缓存控件"""
        self.getWidgetController().cacheWidget(
            widget, parentKey, key, self.getPackCnf(key)
        )

    def getWidget(self, key: str) -> tk.Widget:
        """获取控件"""
        return self.getWidgetController().getWidget(key)

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
            width=self.getConfig().getContentPageWidth()
            + self.getPage().resizeWidthOffset(),
            window=contentFrame,
            anchor=tk.NW,
        )
        self.updateCanvas(scrollCanvas, contentFrame, pageWidgetKeys[2])  # 更新

    def scrollCanvas(self, event, pageKey: str = None):
        """滚动当前页面"""
        pageWidgetKeys = self.getPage().resizeKeys(pageKey)
        scrollCanvas = self.getWidget(pageWidgetKeys[0])
        scrollCanvas.yview_scroll(-2 * (event.delta), tk.UNITS)

    def cacheThread(self, func, key: str, args: tuple = ()):
        """缓存线程并执行"""
        self.getThreadController().cacheThread(
            threading.Thread(target=func, args=args, daemon=True), key
        )

    def destroyWidget(self,key:str):
        """清除该控件及子控件"""
        self.getWidgetController().destroyWidget(key)