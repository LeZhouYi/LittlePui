import os
import json
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
            self.data[groupKey] = {}

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