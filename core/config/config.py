import json
import os

dataFile = "src/config.json"  # 默认数据储存位置

"""配置文件相关，读取/写配置文件"""


class Config:
    def __init__(self) -> None:
        self.data = {}
        self.loadByFile()

    def loadByFile(self) -> None:
        """从文件中读取数据"""
        jsonData = None
        file = os.path.join(os.getcwd(), dataFile)
        if os.path.exists(file):
            with open(file, encoding="utf-8") as f:
                jsonData = json.load(f)
        if jsonData != None:
            self.data = jsonData

    def writeToFile(self) -> None:
        """将当前数据写到文件"""
        file = os.path.join(os.getcwd(), dataFile)
        if os.path.exists(file):
            with open(file, encoding="utf-8", mode="w") as f:
                f.write(json.dumps(self.data, ensure_ascii=False, indent=4))

    def getGeometry(self) -> str:
        """获取窗口大小/位置"""
        windowSize = self.data["windowSize"]
        windowPosition = self.data["windowPosition"]
        return "%dx%d+%d+%d" % (
            windowSize[0],
            windowSize[1],
            windowPosition[0],
            windowPosition[1],
        )

    def setGeometry(self, width: int, height: int, x: int, y: int) -> None:
        """记录窗口大小/位置"""
        self.data["windowSize"] = [width, height]
        self.data["windowPosition"] = [x, y]

    def getTitle(self) -> str:
        """获取窗口标题"""
        return str(self.data["windowTitle"])

    def getStylePath(self) -> str:
        """获取样式配置路径"""
        return str(self.data["stylePath"])

    def getPwdBook(self) -> str:
        """获取密码本路径"""
        return str(self.data["passwordBookPath"])

    def getContentPageWidth(self) -> str:
        """获取当前内容页显示的宽度"""
        return self.data["windowSize"][0] - self.data["sideBarWidth"]

    def hasWindowResize(self, width: int, height: int) -> int:
        """判断窗体是否已变化大小"""
        return (
            abs(self.data["windowSize"][0] - width) > 40
            or abs(self.data["windowSize"][1] - height) > 40
        )

    def getPagePath(self) -> str:
        """获取页面数据路径"""
        return self.data["pagePath"]

    def getNowPage(self) -> str:
        """获取当前页面"""
        return self.data["nowPage"]

    def setNowPage(self, nowPage: str) -> None:
        """记录当前页面"""
        self.data["nowPage"] = nowPage

    def getSideBarWidth(self) -> int:
        """返回SideBar的宽度"""
        return self.data["sideBarWidth"]

    def getPwdIconPath(self) -> int:
        """获取密码本图标路径"""
        return self.data["pwdIconPath"]

    def getpwdIconSize(self)->tuple:
        """获取密码本图片尺寸"""
        return tuple(self.data["pwdIconSize"])