from core.utils import utils


class Page:
    def __init__(self, filePath: str, nowPage: str) -> None:
        self.filePath = filePath  # 本地配置文件路径
        self.data = utils.loadJsonByFile(self.filePath)  # 样式数据集
        self.nowPage = nowPage

    def resizeKeys(self, pageKey: str = None) -> list:
        """提供当前刷新页面用的keys"""
        if pageKey == None:
            return self.data[self.nowPage]["keys"]
        return self.data[pageKey]["keys"]

    def isNowPage(self, nowPage: str) -> None:
        """是否是当前页面"""
        return self.nowPage == nowPage
