from core.control.controller import Controller
from core.frame.baseFrame import BaseFrame
from core.utils import utils

class ComfirmDialog(BaseFrame):
    """确认弹窗"""

    def __init__(self, controller: Controller) -> None:
        super().__init__(controller)

    def loadDialog(self,parentKey:str,suffix:str):
        """加载弹窗"""
        #清理可能存在的缓存
        dialogKey = utils.createKey("cfmDlg")
        self.destroyWidget("pwdDialog_del")
        # mainWindow = self.getWidget("baseWindow")
        # pwdDialogKey = self.createWidget("baseWindow", "pwdDialog_del")
        # pwdFrameKey = self.createWidget(pwdDialogKey, "pwdDlgFrame_del")
        # self.createWidget(pwdFrameKey, "pwdDlgLabel", {"text": "请确认是否删除"},"del")
        # dlgYesBtnKey = self.createWidget(pwdFrameKey,"pwdDlgYesBtn", {"text": "确定"},"del")
        # dlgNoBtnKey = self.createWidget(pwdFrameKey, "pwdDlgNoBtn", {"text": "取消"},"del")

        # pwdDialog = self.getWidget(pwdDialogKey)
        # pwdDialog.title("")
        # self.packCenter(mainWindow,pwdDialog)

        # eventInfo["dialogKey"] = pwdDialogKey
        # self.getWidget(dlgYesBtnKey).bind(
        #     Event.MouseLeftClick,
        #     eventAdaptor(eventInfo["method"], eventInfo=eventInfo),
        # )
        # self.getWidget(dlgNoBtnKey).bind(
        #     Event.MouseLeftClick,
        #     eventAdaptor(self.closeDialog, dialogKey=pwdDialogKey),
        # )
        # # 禁用主窗口操作
        # self.packDialog(mainWindow,pwdDialog)