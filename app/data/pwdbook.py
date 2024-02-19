import datetime
from copy import deepcopy
from core.utils import utils


class PwdBook:
    def __init__(self, filePath: str) -> None:
        self.filePath = filePath  # 本地配置文件路径
        self.data = utils.loadJsonByFile(self.filePath)  # 样式数据集

    def writeToFile(self) -> None:
        """将当前数据写到文件"""
        utils.writeToJsonFile(self.filePath,self.data)

    def getGroupKeys(self) -> list:
        """获取组的键集"""
        return list(self.data.keys())

    def getGroup(self, groupKey: str) -> dict:
        """获取组"""
        if groupKey in self.data:
            return self.data[groupKey]
        return {}

    def addGroup(self, groupKey: str) -> None:
        """新增组"""
        if groupKey not in self.data:
            self.data[groupKey] = {"default":[{"id":self.getTimeStamp(),"labels":[]}]}
        else:
            raise Exception("组 %s 已存在"%groupKey)

    def deletetGroup(self, groupKey: str) -> None:
        """删除组及其数据"""
        if groupKey in self.data:
            self.data.pop(groupKey)

    def deletetEnv(self, groupKey: str, envKey: str) -> None:
        """删除Env及其数据"""
        if groupKey in self.data and envKey in self.data[groupKey]:
            self.data[groupKey].pop(envKey)

    def deleteData(self, groupKey: str, envKey: str, id: str) -> None:
        """删除密码数据"""
        if groupKey in self.data and envKey in self.data[groupKey]:
            for data in self.data[groupKey][envKey]:
                if data["id"] == id:
                    self.data[groupKey][envKey].remove(data)

    def existGroup(self, groupKey: str) -> bool:
        """是否存在组"""
        return groupKey in self.data

    def editGroup(self, groupKey: str, value: str) -> None:
        """编辑组"""
        if not self.existGroup(groupKey):
            raise Exception("组 %s 不存在" % groupKey)
        self.data[value]= deepcopy(self.data.pop(groupKey))

    def existEnv(self, groupKey:str, envKey:str)->bool:
        """是否存在Env"""
        if self.existGroup(groupKey):
            return envKey in self.data[groupKey]
        return False

    def editEnv(self,groupKey: str, envKey:str, value:str)->None:
        """编辑ENV"""
        if not self.existEnv(groupKey,envKey):
            raise Exception("Env %s 不存在"%envKey)
        self.data[groupKey][value] = deepcopy(self.data[groupKey].pop(envKey))

    def addEnv(self,groupKey:str, value:str)->None:
        """新增Env"""
        if not self.existGroup(groupKey):
            raise Exception("组 %s 不存在"%groupKey)
        self.data[groupKey][value] = [{"id":self.getTimeStamp(),"labels":[]}]

    def getTimeStamp(self)->str:
        """获取时间戳"""
        now = datetime.datetime.now()
        return str(int(datetime.datetime.timestamp(now)))

    def addData(self,groupKey:str,envKey:str,data:dict)->None:
        """新增密码数据"""
        if not self.existGroup(groupKey):
            raise Exception("组 %s 不存在"%groupKey)
        if not self.existEnv(groupKey,envKey):
            raise Exception("Env %s 不存在"%envKey)
        data["id"]=self.getTimeStamp()
        self.data[groupKey][envKey].append(data)