import os
import json
import re
from copy import deepcopy
from utils import utils

"""控件相关个性配置"""


class Style:
    def __init__(self, filePath: str) -> None:
        self.filePath = filePath  # 本地配置文件路径
        self.cnfs = utils.loadJsonByFile(self.filePath)  # 样式数据集

    def getCnf(self, key: str) -> dict:
        """获取控件配置"""
        key = self.__cutSuffix(key)
        self.__checkKey(key, "cnf")
        return self.__getData(self.cnfs[key]["cnf"])

    def getPackCnf(self, key: str) -> dict:
        """获取控件布局配置"""
        # 若存在“_”,调用同种样式
        key = self.__cutSuffix(key)
        self.__checkKey(key, "packCnf")
        return self.__getData(self.cnfs[key]["packCnf"])

    def __getData(self, cnfData: any) -> dict:
        """获取Cnf内容，若存在[#key]这类型形式，则需要查找内容并替换"""
        # 存在标签则替换标签为实际数据
        if self.__isLabel(cnfData):
            if cnfData not in self.cnfs:
                raise Exception("不存在标签%s" % cnfData)
            cnfData = self.cnfs[cnfData]
            if isinstance(cnfData, str):
                raise Exception("%s存在多层嵌套或标签对应数据格式不符")
        if cnfData != None and isinstance(cnfData,dict):
            for cnfKey, cnfValue in cnfData.items():
                if self.__isLabel(cnfValue):
                    if cnfValue not in self.cnfs:
                        raise Exception("不存在标签%s" % cnfValue)
                    cnfData[cnfKey] = self.cnfs[cnfValue]
        return cnfData

    def __cutSuffix(self,key:str)->str:
        """去掉后缀"""
        if str(key).find("_") >= 0:
            return key.split("_")[0]
        return key

    def __checkKey(self, key: str, DataKey: str) -> None:
        """校验Key"""
        if key not in self.cnfs:
            raise Exception("键名%s不存在" % key)
        if DataKey not in self.cnfs[key]:
            raise Exception("%s对应数据中缺少%s字段" % (key, DataKey))

    def __isLabel(self, value: str) -> bool:
        """判断是否为标签"""
        return value != None and re.compile("\$[a-zA-Z]+").fullmatch(str(value))
