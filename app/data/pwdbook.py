import os
import json

class PwdBook:

    def __init__(self,filePath:str) -> None:
        self.filePath = filePath #本地配置文件路径
        self.data = {} #样式数据集
        self.loadByFile()

    def loadByFile(self) -> None:
        """从文件中读取数据"""
        jsonData = None
        file = os.path.join(os.getcwd(), self.filePath)
        if os.path.exists(file):
            with open(file, encoding="utf-8") as f:
                jsonData = json.load(f)
        if jsonData != None:
            self.data = dict(jsonData)

    def writeToFile(self) -> None:
        """将当前数据写到文件"""
        file = os.path.join(os.getcwd(), self.filePath)
        if os.path.exists(file):
            with open(file, encoding="utf-8", mode="w") as f:
                f.write(json.dumps(self.data, ensure_ascii=False, indent=4))

    def getGroupKeys(self)->list:
        """获取组的键集"""
        return list(self.data.keys())

    def getGroup(self,groupKey:str)->dict:
        """获取组"""
        if groupKey in self.data:
            return self.data[groupKey]
        return {}

    def addGroup(self,groupKey:str)->None:
        """新增组"""
        if groupKey not in self.data:
            self.data[groupKey]={}

    def deletetGroup(self,groupKey:str)->None:
        """删除组及其数据"""
        if groupKey in self.data:
            self.data.pop(groupKey)

    def deletetEnv(self,groupKey:str,envKey:str)->None:
        """删除Env及其数据"""
        if groupKey in self.data and envKey in self.data[groupKey]:
            self.data[groupKey].pop(envKey)

    def deleteData(self,groupKey:str,envKey:str,id:str)->None:
        """删除密码数据"""
        if groupKey in self.data and envKey in self.data[groupKey]:
            for data in self.data[groupKey][envKey]:
                if data["id"]==id:
                    self.data[groupKey][envKey].remove(data)