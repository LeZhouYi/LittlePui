from core.config.config import Config
from core.control.page import Page
from core.control.style import Style
from core.control.widgetControl import WidgetController
from core.control.threadControl import ThreadController
from core.control.sourceControl import ImageController


class Controller:
    """控制模块集"""

    def __init__(self, configFile: str) -> None:
        # 初始化所有控制类
        self.config = Config(configFile)
        self.style = Style(self.config.getData("stylePath"))  # 样式配置
        self.page = Page(
            self.config.getData("pagePath"), self.config.getData("nowPage")
        )
        self.widgetController = WidgetController()
        self.threadController = ThreadController()  # 线程池
        self.imageController = ImageController()

    def getConfig(self) -> Config:
        """获取配置"""
        return self.config

    def getWC(self) -> WidgetController:
        """获取控件池"""
        return self.widgetController

    def getStyle(self) -> Style:
        """获取布局"""
        return self.style

    def getPage(self) -> Page:
        """获取分页"""
        return self.page

    def getTC(self) -> ThreadController:
        """获取线程管理器"""
        return self.threadController

    def getIC(self) -> ImageController:
        """获取图像池"""
        return self.imageController
