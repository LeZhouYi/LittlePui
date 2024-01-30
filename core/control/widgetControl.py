import tkinter as tk
from copy import deepcopy

"""
缓存/提取控件，管理控件的层级关系，方便重新布局
"""

class WidgetController:
    def __init__(self) -> None:
        self.widgetPool = {}  # 缓存控件池，键名：控件
        self.relations = {}  # 缓存控件的层级，键名：「子控件列表，布局」

    def repackWidget(self, keys: list) -> None:
        """重新安排布局"""
        for key in keys:
            self.getWidget(key).pack_forget()
        for key in keys:
            cnf = self.getCnf(key)
            if cnf != None:
                self.getWidget(key).pack(cnf=cnf)

    def getCnf(self, key: str) -> dict:
        """获取cnf"""
        if key not in self.relations:
            raise Exception("键名%s不存在" % key)
        return self.relations[key]["packInfo"]

    def cacheWidget(
        self, widget: tk.Widget, parentKey: str, key: str, cnf: dict
    ) -> None:
        """缓存控件"""
        if cnf != None:
            widget.pack_configure(cnf)
        self.__cacheWidget(widget, key)
        self.__cacheRelation(parentKey, key, cnf)

    def cacheWidgetByGrid(
        self, widget: tk.Widget, parentKey: str, key: str, cnf: dict
    ) -> None:
        """缓存控件"""
        if cnf != None:
            widget.grid(cnf)
        self.__cacheWidget(widget, key)
        self.__cacheRelation(parentKey, key, cnf)

    def getWidget(self, key: str) -> tk.Widget:
        """获取控件"""
        if key not in self.widgetPool:
            raise Exception("键名%s不存在" % key)
        return self.widgetPool[key]

    def clearWidget(self, key: str) -> None:
        """清理该控件的子控件"""
        if key not in self.widgetPool or key not in self.relations:
            return  # 已清除
        keyStack = self.__popChilds(key)  # 关键字栈
        while len(keyStack) > 0:
            keyItem = keyStack.pop()
            keyStack.extend(self.__popChilds(keyItem))
            self.__destroyWidget(keyItem)  # 销毁当前控件

    def destroyWidget(self, key: str) -> None:
        """清理该控件及其子控件"""
        if key not in self.widgetPool or key not in self.relations:
            return  # 已清除
        keyStack = self.__popChilds(key)  # 关键字栈
        while len(keyStack) > 0:
            keyItem = keyStack.pop()
            keyStack.extend(self.__popChilds(keyItem))
            self.__destroyWidget(keyItem)  # 销毁当前控件
        self.__destroyWidget(key)

    def __destroyWidget(self, key: str) -> None:
        """执行控件destory"""
        if key not in self.relations:
            return
            # raise Exception("键名%s不存在" % key)
        self.widgetPool.pop(key).destroy()
        self.relations.pop(key)

    def __popChilds(self, key: str) -> list:
        """获取子控件关键字"""
        if key not in self.relations:
            return []
            # raise Exception("键名%s不存在" % key)
        childs = deepcopy(self.relations[key]["childs"])
        self.relations[key]["childs"] = []
        return childs

    def __cacheRelation(self, parentKey: str, key: str, cnf) -> None:
        """缓存控件层级和布局"""
        if parentKey != None:
            if parentKey not in self.relations:
                raise Exception("父级键名%s不存在" % parentKey)
            self.relations[parentKey]["childs"].append(key)  # 记录子控件
        if key in self.relations:
            raise Exception("键名%s已存在" % key)
        self.relations[key] = {"childs": [], "packInfo": cnf}  # 初始化结构

    def __cacheWidget(self, widget: tk.Widget, key: str) -> None:
        """将控件添加进缓存池"""
        if key in self.widgetPool:
            raise Exception("键名%s已存在" % key)
        self.widgetPool[key] = widget