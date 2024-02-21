import tkinter as tk
from core.control.controller import Controller
from core.frame.absFrame import BaseFrame
from core.utils import utils
from core.control.event import Event,eventAdaptor

class ComfirmDialog(BaseFrame):
    """确认弹窗"""

    def __init__(self, controller: Controller,parentKey:str,suffix:str) -> None:
        super().__init__(controller)
        self.suffix = suffix
        self.parentKey = parentKey

    def getSuffix(self)->str:
        return self.suffix

    def bindYesMethod(self,func, **kwargs):
        """绑定确认控件点击方法"""
        self.bindClickMethod(self.getYesBtnKey(),func,**kwargs)

    def loadDialog(self,text:str):
        """加载弹窗"""
        #清理可能存在的缓存
        dialogKey = self.createKey("cfmDlg",self.suffix)
        self.destroyWidget(dialogKey)
        mainWindow = self.getWidget(self.parentKey)
        self.createWidget(self.parentKey, dialogKey)
        frameKey = self.createWidget(dialogKey, "cfmFrame",None,self.suffix)
        self.createWidget(frameKey, "cfmLabel", {"text": text},self.suffix)
        self.createWidget(frameKey,"cfmYesBtn", {"text": "确定"},self.suffix)
        noBtnKey = self.createWidget(frameKey, "cfmNoBtn", {"text": "取消"},self.suffix)

        pwdDialog = self.getWidget(dialogKey)
        pwdDialog.title("")
        self.packCenter(mainWindow,pwdDialog)
        self.bindClickMethod(noBtnKey,self.closeDialog)

    def getYesBtnKey(self)->str:
        """获取确认控件的Key"""
        return self.createKey("cfmYesBtn",self.suffix)

    def packDialog(self) -> None:
        """禁用主窗口操作"""
        mainWindow = self.getWidget(self.parentKey)
        dialogKey = self.createKey("cfmDlg",self.suffix)
        dialog = self.getWidget(dialogKey)
        return super().packDialog(mainWindow, dialog)

    def closeDialog(self,event):
        """清理窗口"""
        dialogKey = self.createKey("cfmDlg",self.suffix)
        self.destroyWidget(dialogKey)

class InputDialog(ComfirmDialog):
    """输入数据弹窗"""

    def __init__(self, controller: Controller, parentKey: str, suffix: str) -> None:
        super().__init__(controller, parentKey, suffix)
        self.keySet = {}

    def loadDialog(self, text: str)->None:
        """加载弹窗"""
        #清理可能存在的缓存
        dialogKey = self.createKey("cfmDlg",self.suffix)
        self.destroyWidget(dialogKey)
        mainWindow = self.getWidget(self.parentKey)
        self.createWidget(self.parentKey, dialogKey)
        frameKey = self.createWidget(dialogKey, "cfmFrame",None,self.suffix)
        self.createWidget(frameKey, "cfmInfo", {"text": text},self.suffix)
        self.createWidget(frameKey,"cfmContent",None,self.suffix) #用于InputDialog的内容
        self.createWidget(frameKey,"cfmYesBtn", {"text": "确定"},self.suffix)
        noBtnKey = self.createWidget(frameKey, "cfmNoBtn", {"text": "取消"},self.suffix)

        pwdDialog = self.getWidget(dialogKey)
        pwdDialog.title("")
        self.packCenter(mainWindow,pwdDialog)
        self.bindClickMethod(noBtnKey,self.closeDialog)

    def addEntry(self, key:str,labelText:str,value:str="")->None:
        """添加输入框及标签"""
        #构建Key
        ctntFrameKey = self.createKey("cfmContent",self.suffix)
        suffixKey = self.suffix+key
        #初始化控件
        lineFrameKey = self.createWidget(ctntFrameKey,"cfmLineFrame",None,suffixKey)
        if labelText!=None:
            self.createWidget(lineFrameKey,"cfmEntryLabel",{"text":labelText},suffixKey)
        entryKey = self.createWidget(lineFrameKey,"cfmEntry",None,suffixKey)
        if value!=None:
            self.getWidget(entryKey).insert(tk.END,value)
        #备份Key
        self.addKey(key,entryKey)

    def addKey(self,key:str,widgetKey:str)->None:
        """添加键"""
        if key not in self.keySet:
            self.keySet[key]=widgetKey

    def getEntryValue(self,key:str)->str:
        """获取输入框的值"""
        if key not in self.keySet:
            raise Exception("键名%s不存在" % key)
        return self.getWidget(self.keySet[key]).get()

    def focusEntry(self,key:str=None)->None:
        """使输入框获得焦点，若Key为None则默认为第一个，若不存在输入框则不处理"""
        if len(self.keySet)>0:
            if key == None:
                for dictKey, dictValue in self.keySet.items():
                    key = dictKey
                    break
            if key in self.keySet:
                self.getWidget(self.keySet[key]).focus_set()