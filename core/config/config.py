from core.utils import utils

"""配置文件相关，读取/写配置文件"""


class Config:
    def __init__(self, filePath: str) -> None:
        self.filePath = filePath
        self.data = utils.loadJsonByFile(self.filePath)

    def writeToFile(self) -> None:
        """将当前数据写到文件"""
        utils.writeToJsonFile(self.filePath, self.data)

    def getData(self, key: str) -> any:
        """获取配置数据"""
        if key == None or key not in self.data:
            raise Exception("键名%s不存在" % key)
        return self.data[key]

    def setData(self, key: str, data: str) -> any:
        """设置配置数据"""
        if key == None or key not in self.data:
            raise Exception("键名%s不存在" % key)
        self.data[key] = data
