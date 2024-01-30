import os
import json

class Page:

    def __init__(self,filePath:str,nowPage:str) -> None:
        self.filePath = filePath #本地配置文件路径
        self.data = {} #样式数据集
        self.nowPage = nowPage
        self.loadByFile()

    def loadByFile(self) -> None:
        """从文件中读取数据"""
        jsonData = None
        file = os.path.join(os.getcwd(), self.filePath)
        if os.path.exists(file):
            with open(file, encoding="utf-8") as f:
                jsonData = json.load(f)
        if jsonData != None:
            self.data = jsonData

    def resizeKeys(self,pageKey:str=None)->list:
        """提供当前刷新页面用的keys"""
        if pageKey==None:
            return self.data[self.nowPage]["keys"]
        return self.data[pageKey]["keys"]

    def resizeWidthOffset(self,pageKey:str=None)->int:
        """获取当前刷新页面宽度调整值"""
        if pageKey==None:
            return self.data[self.nowPage]["widthOffset"]
        return self.data[pageKey]["widthOffset"]

    def setNowPage(self,nowPage:str)->None:
        """设置当前页面"""
        self.nowPage = nowPage

    def isNowPage(self,nowPage:str)->None:
        """是否是当前页面"""
        return self.nowPage==nowPage