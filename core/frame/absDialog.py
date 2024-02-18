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
        yesBtnKey = utils.createKey("cfmYesBtn",self.suffix)
        self.getWidget(yesBtnKey).bind(Event.MouseLeftClick,eventAdaptor(func,**kwargs))

    def loadDialog(self,text:str):
        """加载弹窗"""
        #清理可能存在的缓存
        dialogKey = utils.createKey("cfmDlg",self.suffix)
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

        self.getWidget(noBtnKey).bind(
            Event.MouseLeftClick,
            self.closeDialog
        )

    def packDialog(self) -> None:
        """禁用主窗口操作"""
        mainWindow = self.getWidget(self.parentKey)
        dialogKey = utils.createKey("cfmDlg",self.suffix)
        dialog = self.getWidget(dialogKey)
        return super().packDialog(mainWindow, dialog)

    def closeDialog(self,event):
        """清理窗口"""
        dialogKey = utils.createKey("cfmDlg",self.suffix)
        self.destroyWidget(dialogKey)

class InputDialog(ComfirmDialog):
    """输入数据弹窗"""

    def __init__(self, controller: Controller, parentKey: str, suffix: str) -> None:
        super().__init__(controller, parentKey, suffix)

    def loadDialog(self, text: str)->None:
        """加载弹窗"""
        #清理可能存在的缓存
        dialogKey = utils.createKey("cfmDlg",self.suffix)
        self.destroyWidget(dialogKey)
        mainWindow = self.getWidget(self.parentKey)
        self.createWidget(self.parentKey, dialogKey)
        frameKey = self.createWidget(dialogKey, "cfmFrame",None,self.suffix)
        self.createWidget(frameKey,"cfmContent",None,self.suffix) #用于InputDialog的内容
        self.createWidget(frameKey, "cfmInfo", {"text": text},self.suffix)
        self.createWidget(frameKey,"cfmYesBtn", {"text": "确定"},self.suffix)
        noBtnKey = self.createWidget(frameKey, "cfmNoBtn", {"text": "取消"},self.suffix)

        pwdDialog = self.getWidget(dialogKey)
        pwdDialog.title("")
        self.packCenter(mainWindow,pwdDialog)

        self.getWidget(noBtnKey).bind(
            Event.MouseLeftClick,
            self.closeDialog
        )