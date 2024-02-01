import re
import tkinter as tk
from copy import deepcopy
from core.utils import utils

"""控件相关个性配置"""

class TkinterMap:

    mapping = {
        "Button": tk.Button,
        "Dialog": tk.Toplevel,
        "Label": tk.Label,
        "Frame": tk.Frame
    }

    def getWidgetFunc(key:str):
        """返回对应的初始控件方法"""
        return TkinterMap.mapping[key]

class Style:

    def __init__(self, filePath: str) -> None:
        self.filePath = filePath  # 本地配置文件路径
        self.data = utils.loadJsonByFile(self.filePath)  # 样式数据集
        self.__loadImports()

    def getType(self, key: str):
        """获取该布局所属类型"""
        key = self.__cutSuffix(key)
        self.__checkKey(key, "type")
        return TkinterMap.getWidgetFunc(self.data[key]["type"])

    def getCnf(self, key: str) -> dict:
        """获取控件配置"""
        key = self.__cutSuffix(key)
        self.__checkKey(key, "cnf")
        return self.__getData(self.data[key]["cnf"])

    def getPackCnf(self, key: str) -> dict:
        """获取控件布局配置"""
        # 若存在“_”,调用同种样式
        key = self.__cutSuffix(key)
        self.__checkKey(key, "packCnf")
        return self.__getData(self.data[key]["packCnf"])

    def __loadImports(self) -> None:
        """引入其它配置文件"""
        if "imports" not in self.data:
            return
        importStack = deepcopy(self.data["imports"])
        importInfo = [self.filePath]
        while len(importStack) > 0:
            # 备份当前层级的导入信息
            tempStack = deepcopy(importStack)
            importStack = []
            for importFile in tempStack:
                # 存在已导入的配置文件则不再导入
                if importFile in importInfo:
                    continue
                importInfo.append(importFile)
                data = utils.loadJsonByFile(importFile)
                self.data.update(data)
                if "imports" in data:
                    importStack.extend(data["imports"])

    def __getData(self, cnfData: any) -> dict:
        """获取Cnf内容，若存在[#key]这类型形式，则需要查找内容并替换"""
        # 存在标签则替换标签为实际数据
        if self.__isLabel(cnfData):
            if cnfData not in self.data:
                raise Exception("不存在标签%s" % cnfData)
            cnfData = self.data[cnfData]
            if isinstance(cnfData, str):
                raise Exception("%s存在多层嵌套或标签对应数据格式不符")
        if cnfData != None and isinstance(cnfData, dict):
            if "$ref" in cnfData:
                label = cnfData["$ref"]
                if label not in self.data:
                    raise Exception("标签%s不存在" % label)
                cnfData.update(self.data[label])
            for cnfKey, cnfValue in cnfData.items():
                if self.__isLabel(cnfValue):
                    if cnfValue not in self.data:
                        raise Exception("标签%s不存在" % cnfValue)
                    cnfData[cnfKey] = self.data[cnfValue]
            if "$ref" in cnfData:
                cnfData.pop("$ref")
        return cnfData

    def __cutSuffix(self, key: str) -> str:
        """去掉后缀"""
        if str(key).find("_") >= 0:
            return key.split("_")[0]
        return key

    def __checkKey(self, key: str, DataKey: str) -> None:
        """校验Key"""
        if key not in self.data:
            raise Exception("键名%s不存在" % key)
        if DataKey not in self.data[key]:
            raise Exception("%s对应数据中缺少%s字段" % (key, DataKey))

    def __isLabel(self, value: str) -> bool:
        """判断是否为标签"""
        return value != None and re.compile("\$[a-zA-Z]+").fullmatch(str(value))
