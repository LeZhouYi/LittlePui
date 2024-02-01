import os
import pyperclip
import webbrowser
import tkinter as tk
from time import sleep
from PIL import Image, ImageTk
from core.utils import utils
from app.data.pwdbook import PwdBook
from core.frame.baseFrame import BaseFrame
from core.control.event import Event, eventAdaptor
from core.control.controller import Controller

"""密码内容页"""


class PwdBookFrame(BaseFrame):
    def __init__(self, controller: Controller) -> None:
        super().__init__(controller)
        self.passwordBook = PwdBook(self.getConfig().getData("pwdBookPath"))
        self.loadIcon()
        self.checkPwdData()

    def loadIcon(self) -> None:
        """加载图片资源"""
        iconPaths = os.path.join(os.getcwd(), self.getConfig().getData("pwdIconPath"))
        # 遍历目标路径所有图片
        for fileName in os.listdir(iconPaths):
            if utils.isPhoto(fileName):
                # 加载图片并调整为适合尺寸
                iconfile = os.path.join(iconPaths, fileName)
                image = Image.open(iconfile).resize(
                    self.getConfig().getData("pwdIconSize")
                )
                image = ImageTk.PhotoImage(image)
                # 缓存
                self.cacheImage(image, utils.getFileName(fileName), "pwdbookIcon")

    def checkPwdData(self) -> None:
        """检查密码本数据，若无数据则加入默认数据"""
        if len(self.passwordBook.getGroupKeys()) == 0:
            self.passwordBook.addGroup("default")

    def updatePwdPage(self) -> None:
        """更新当前页面"""
        self.updateCanvas(
            self.getWidget("pwdScrollCanvas"),
            self.getWidget("pwdContentFrame"),
            "pwdDispalyFrame",
        )

    ###########控件事件################
    def clickComfirmEnv(self,event, groupKey:str, envKey:str)->None:
        """点击确认编辑Env"""
        entry = self.getWidget("pwdEditEnvEntry")
        entryText = entry.get()
        if utils.isEmpty(entryText) or envKey == entryText:
            self.closeDialog(event, "pwdEditEnvDialog")
        if self.passwordBook.existEnv(groupKey,entryText):
            self.getWidget("pwdEditEnvYesBtn").config(text="ENV已存在")
            self.cacheThread(
                self.replaceText, "pwdButton", ("pwdEditEnvYesBtn", "确定")
            )
        else:
            #编辑并保存
            self.passwordBook.editEnv(groupKey,envKey,entryText)
            self.passwordBook.writeToFile()
            #清理相关控件
            pwdEnvFrameKey = utils.createKey("pwdEnvFrame", groupKey, envKey)
            self.destroyWidget(pwdEnvFrameKey)
            # 加载新控件
            group = self.passwordBook.getGroup(groupKey)
            pwdList = group[entryText]
            self.loadSingleEnv(groupKey, entryText)
            for pwdData in pwdList:
                self.loadSingleData(groupKey, entryText, pwdData)
            # 关闭弹窗
            self.closeDialog(event, "pwdEditEnvDialog")

    def clickComfirmGroup(self, event, groupKey: str) -> None:
        """点击确认编辑组"""
        entry = self.getWidget("pwdEditGroupEntry")
        entryText = entry.get()
        if utils.isEmpty(entryText) or groupKey == entryText:
            self.closeDialog(event, "pwdEditGroupDialog")
        if self.passwordBook.existGroup(entryText):
            self.getWidget("pwdEditGroupYesBtn").config(text="组已存在")
            self.cacheThread(
                self.replaceText, "pwdButton", ("pwdEditGroupYesBtn", "确定")
            )
        else:
            # 编辑组并保存
            self.passwordBook.editGroup(groupKey, entryText)
            self.passwordBook.writeToFile()
            # 清理旧控件
            pwdSingleFrameKey = utils.createKey("pwdSingleFrame", groupKey)
            self.destroyWidget(pwdSingleFrameKey)
            # 加载新控件
            self.loadSingleGroup(entryText)
            group = self.passwordBook.getGroup(entryText)
            for envkey, pwdList in group.items():
                self.loadSingleEnv(entryText, envkey)
                for pwdData in pwdList:
                    self.loadSingleData(entryText, envkey, pwdData)
            # 关闭弹窗
            self.closeDialog(event, "pwdEditGroupDialog")

    def clickDeleteGroup(self, event, eventInfo: dict) -> None:
        """点击删除组事件"""
        self.passwordBook.deletetGroup(eventInfo["groupKey"])
        self.passwordBook.writeToFile()
        self.destroyWidget(eventInfo["widget"])
        self.closeDialog(event, eventInfo["dialogKey"])
        self.updatePwdPage()

    def clickDeleteEnv(self, event, eventInfo: dict) -> None:
        """点击删除环境事件"""
        self.passwordBook.deletetEnv(eventInfo["groupKey"], eventInfo["envKey"])
        self.passwordBook.writeToFile()
        self.destroyWidget(eventInfo["widget"])
        self.closeDialog(event, eventInfo["dialogKey"])
        self.updatePwdPage()

    def clickDeletePwdData(self, event, eventInfo: dict) -> None:
        """点击删除密码数据"""
        self.passwordBook.deleteData(
            eventInfo["groupKey"], eventInfo["envKey"], eventInfo["id"]
        )
        self.passwordBook.writeToFile()
        self.destroyWidget(eventInfo["widget"])
        self.closeDialog(event, eventInfo["dialogKey"])
        self.updatePwdPage()

    def closeDialog(self, event, dialogKey: str) -> None:
        """关闭提示框事件"""
        self.destroyWidget(dialogKey)

    def clickCopy(self, event, text: str, btnKey: str) -> None:
        """点击复制文本到剪切板"""
        pyperclip.copy(text)
        self.cacheThread(self.completeBtn, "pwdButton", args=(btnKey, "copy"))

    def clickBrowser(self, event, pwdData: dict) -> None:
        """点击访问链接"""
        pyperclip.copy(pwdData["account"])
        webbrowser.open(pwdData["website"])

    def clickPackGroup(self, event, groupKey: str) -> None:
        """点击收起组内容"""
        group = self.passwordBook.getGroup(groupKey)
        for envkey, pwdList in group.items():
            pwdEnvFrameKey = utils.createKey("pwdEnvFrame", groupKey, envkey)
            pwdEnvFrame = self.getWidget(pwdEnvFrameKey)
            pwdEnvFrame.pack_forget()

        packBtnKey = utils.createKey("pwdGroupBtn", groupKey, "pack")
        packBtn = self.getWidget(packBtnKey)
        packBtn.configure(image=self.getImage("display", "pwdbookIcon"))
        packBtn.unbind(Event.MouseLeftClick)
        packBtn.bind(
            Event.MouseLeftClick,
            eventAdaptor(self.clickDisplayGroup, groupKey=groupKey),
        )

    def clickDisplayGroup(self, event, groupKey: str) -> None:
        """点击展开组内容"""
        group = self.passwordBook.getGroup(groupKey)
        for envkey, pwdList in group.items():
            pwdEnvFrameKey = utils.createKey("pwdEnvFrame", groupKey, envkey)
            pwdEnvFrame = self.getWidget(pwdEnvFrameKey)
            pwdEnvFrame.pack(self.getPackCnf(pwdEnvFrameKey))

        packBtnKey = utils.createKey("pwdGroupBtn", groupKey, "pack")
        packBtn = self.getWidget(packBtnKey)
        packBtn.configure(image=self.getImage("pack", "pwdbookIcon"))
        packBtn.unbind(Event.MouseLeftClick)
        packBtn.bind(
            Event.MouseLeftClick,
            eventAdaptor(self.clickPackGroup, groupKey=groupKey),
        )

    def clickPackEnv(self, event, groupKey: str, envkey: str) -> None:
        """点击关闭Env内容"""
        group = self.passwordBook.getGroup(groupKey)
        for pwdData in group[envkey]:
            pwdDataId = pwdData["id"]
            pwdDataFrameKey = utils.createKey("pwdDataFrame", pwdDataId)
            pwdDataFrame = self.getWidget(pwdDataFrameKey)
            pwdDataFrame.pack_forget()

        packBtnKey = utils.createKey("pwdEnvBtn", groupKey, envkey, "pack")
        packBtn = self.getWidget(packBtnKey)
        packBtn.configure(image=self.getImage("pack", "pwdbookIcon"))
        packBtn.unbind(Event.MouseLeftClick)
        packBtn.bind(
            Event.MouseLeftClick,
            eventAdaptor(self.clickDisplayEnv, groupKey=groupKey, envkey=envkey),
        )

    def clickDisplayEnv(self, event, groupKey: str, envkey: str) -> None:
        """点击关闭Env内容"""
        group = self.passwordBook.getGroup(groupKey)
        for pwdData in group[envkey]:
            pwdDataId = pwdData["id"]
            pwdDataFrameKey = utils.createKey("pwdDataFrame", pwdDataId)
            pwdDataFrame = self.getWidget(pwdDataFrameKey)
            pwdDataFrame.pack(self.getPackCnf(pwdDataFrameKey))

        packBtnKey = utils.createKey("pwdEnvBtn", groupKey, envkey, "pack")
        packBtn = self.getWidget(packBtnKey)
        packBtn.configure(image=self.getImage("pack", "pwdbookIcon"))
        packBtn.unbind(Event.MouseLeftClick)
        packBtn.bind(
            Event.MouseLeftClick,
            eventAdaptor(self.clickPackEnv, groupKey=groupKey, envkey=envkey),
        )

    ###########渲染相关################
    def loadAddGroupDialog(self, event)->None:
        """加载添加组提示框"""
        if self.getWC().existWidget("pwdAddGroupDialog"):
            self.destroyWidget("pwdAddGroupDialog")

        mainWindow = self.getWidget("baseWindow")
        pwdEditGroupDialog = self.createDialog("baseWindow", "pwdAddGroupDialog")
        self.createFrame("pwdAddGroupDialog", "pwdAddGroupFrame")
        self.createLabel("pwdAddGroupFrame", "pwdAddGroupLabel", {"text": "请输入组名"})
        pwdAddGroupEntry = self.createEntry("pwdAddGroupFrame", "pwdAddGroupEntry")
        pwdAddGroupYesBtn = self.createLabel(
            "pwdAddGroupFrame", "pwdAddGroupYesBtn", {"text": "确定"}
        )
        pwdAddGroupNoBtn = self.createLabel(
            "pwdAddGroupFrame", "pwdAddGroupNoBtn", {"text": "取消"}
        )

        pwdEditGroupDialog.title("")
        # 计算并使提示框显示居中
        winX = (
            mainWindow.winfo_rootx()
            + (mainWindow.winfo_width() // 5)*2
        )
        winY = (
            mainWindow.winfo_rooty()
            + (mainWindow.winfo_height() // 5)*2
        )
        pwdEditGroupDialog.geometry("+{}+{}".format(winX, winY))

        pwdAddGroupNoBtn.bind(
            Event.MouseLeftClick,
            eventAdaptor(self.closeDialog, dialogKey="pwdEditGroupDialog"),
        )

        # 禁用主窗口操作
        mainWindow.update_idletasks()
        pwdEditGroupDialog.transient(mainWindow)
        pwdEditGroupDialog.grab_set()
        mainWindow.wait_window(pwdEditGroupDialog)

    def loadEditEnvDialog(self, event, groupKey: str, envKey: str) -> None:
        """加载编辑Env提示框"""
        #清理旧缓存的控件
        if self.getWC().existWidget("pwdEditEnvDialog"):
            self.destroyWidget("pwdEditEnvDialog")

        mainWindow = self.getWidget("baseWindow")
        pwdEditEnvDialog = self.createDialog("baseWindow", "pwdEditEnvDialog")

        self.createFrame("pwdEditEnvDialog", "pwdEditEnvFrame")
        self.createLabel("pwdEditEnvFrame", "pwdEditEnvLabel", {"text": "请输入Env名"})
        pwdEditEnvEntry = self.createEntry("pwdEditEnvFrame", "pwdEditEnvEntry")
        pwdEditEnvYesBtn = self.createLabel(
            "pwdEditEnvFrame", "pwdEditEnvYesBtn", {"text": "确定"}
        )
        pwdEditEnvNoBtn = self.createLabel(
            "pwdEditEnvFrame", "pwdEditEnvNoBtn", {"text": "取消"}
        )

        pwdEditEnvEntry.insert(tk.END, envKey)
        pwdEditEnvDialog.title("")
        # 计算并使提示框显示居中
        winX = (
            mainWindow.winfo_rootx()
            + (mainWindow.winfo_width() // 5)*2
        )
        winY = (
            mainWindow.winfo_rooty()
            + (mainWindow.winfo_height() // 5)*2
        )
        pwdEditEnvDialog.geometry("+{}+{}".format(winX, winY))
        pwdEditEnvYesBtn.bind(
            Event.MouseLeftClick,
            eventAdaptor(self.clickComfirmEnv,groupKey=groupKey,envKey=envKey)
        )
        pwdEditEnvNoBtn.bind(
            Event.MouseLeftClick,
            eventAdaptor(self.closeDialog, dialogKey="pwdEditEnvDialog"),
        )

        # 禁用主窗口操作
        mainWindow.update_idletasks()
        pwdEditEnvDialog.transient(mainWindow)
        pwdEditEnvDialog.grab_set()
        mainWindow.wait_window(pwdEditEnvDialog)

    def loadEditGroupDialog(self, event, groupKey: str) -> None:
        """加载编辑组提示框"""
        if self.getWC().existWidget("pwdEditGroupDialog"):
            self.destroyWidget("pwdEditGroupDialog")

        mainWindow = self.getWidget("baseWindow")
        pwdEditGroupDialog = self.createDialog("baseWindow", "pwdEditGroupDialog")
        self.createFrame("pwdEditGroupDialog", "pwdEditGroupFrame")
        self.createLabel("pwdEditGroupFrame", "pwdEditGroupLabel", {"text": "请输入组名"})
        pwdEditGroupEntry = self.createEntry("pwdEditGroupFrame", "pwdEditGroupEntry")
        pwdEditGroupYesBtn = self.createLabel(
            "pwdEditGroupFrame", "pwdEditGroupYesBtn", {"text": "确定"}
        )
        pwdEditGroupNoBtn = self.createLabel(
            "pwdEditGroupFrame", "pwdEditGroupNoBtn", {"text": "取消"}
        )

        pwdEditGroupEntry.insert(tk.END, groupKey)
        pwdEditGroupDialog.title("")
        # 计算并使提示框显示居中
        winX = (
            mainWindow.winfo_rootx()
            + (mainWindow.winfo_width() // 5)*2
        )
        winY = (
            mainWindow.winfo_rooty()
            + (mainWindow.winfo_height() // 5)*2
        )
        pwdEditGroupDialog.geometry("+{}+{}".format(winX, winY))

        pwdEditGroupNoBtn.bind(
            Event.MouseLeftClick,
            eventAdaptor(self.closeDialog, dialogKey="pwdEditGroupDialog"),
        )
        pwdEditGroupYesBtn.bind(
            Event.MouseLeftClick,
            eventAdaptor(self.clickComfirmGroup, groupKey=groupKey),
        )

        # 禁用主窗口操作
        mainWindow.update_idletasks()
        pwdEditGroupDialog.transient(mainWindow)
        pwdEditGroupDialog.grab_set()
        mainWindow.wait_window(pwdEditGroupDialog)

    def completeBtn(self, btnKey: str, controlKey: str) -> None:
        """点击按钮成功效果"""
        btn = self.getWidget(btnKey)
        btn.configure(image=self.getImage("complete", "pwdbookIcon"))
        sleep(0.8)
        btn.configure(image=self.getImage(controlKey, "pwdbookIcon"))

    def loadDeleteDialog(
        self,
        event,
        eventInfo: dict,
    ) -> None:
        """加载删除提示框"""
        if self.getWC().existWidget("pwdDeleteDialog"):
            self.destroyWidget("pwdDeleteDialog")

        mainWindow = self.getWidget("baseWindow")
        pwdDeleteDialog = self.createDialog("baseWindow", "pwdDeleteDialog")
        self.createFrame("pwdDeleteDialog", "pwdDelDlgFrame")
        self.createLabel("pwdDelDlgFrame", "pwdDelDlgLabel", {"text": "请确认是否删除"})
        pwdDelDlgYesBtn = self.createLabel(
            "pwdDelDlgFrame", "pwdDelDlgYesBtn", {"text": "确定"}
        )
        pwdDelDlgNoBtn = self.createLabel(
            "pwdDelDlgFrame", "pwdDelDlgNoBtn", {"text": "取消"}
        )

        pwdDeleteDialog.title("")
        # 计算并使提示框显示居中
        winX = (
            mainWindow.winfo_rootx()
            + (mainWindow.winfo_width() // 5)*2
        )
        winY = (
            mainWindow.winfo_rooty()
            + (mainWindow.winfo_height() // 5)*2
        )
        pwdDeleteDialog.geometry("+{}+{}".format(winX, winY))

        eventInfo["dialogKey"] = "pwdDeleteDialog"
        pwdDelDlgYesBtn.bind(
            Event.MouseLeftClick,
            eventAdaptor(eventInfo["method"], eventInfo=eventInfo),
        )
        pwdDelDlgNoBtn.bind(
            Event.MouseLeftClick,
            eventAdaptor(self.closeDialog, dialogKey="pwdDeleteDialog"),
        )
        # 禁用主窗口操作
        mainWindow.update_idletasks()
        pwdDeleteDialog.transient(mainWindow)
        pwdDeleteDialog.grab_set()
        mainWindow.wait_window(pwdDeleteDialog)

    def loadPasswordNote(self, contentFrameKey: str) -> None:
        """加载密码本页面"""
        # 构造基础框架
        self.createFrame(contentFrameKey, "pwdDispalyFrame")
        pwdScrollCanvas = self.createCanvas("pwdDispalyFrame", "pwdScrollCanvas")
        self.createFrame("pwdScrollCanvas", "pwdContentFrame")
        pwdScrollBar = self.createScrollBar("pwdDispalyFrame", "pwdScrollBar")

        # 绑定滚动事件
        pwdScrollCanvas.config(yscrollcommand=pwdScrollBar.set, yscrollincrement=5)
        pwdScrollBar.config(command=pwdScrollCanvas.yview)  # 绑定滚动

        # 加载密码内容
        for groupKey in self.passwordBook.getGroupKeys():
            self.loadSingleGroup(groupKey)
            group = self.passwordBook.getGroup(groupKey)
            for envkey, pwdList in group.items():
                self.loadSingleEnv(groupKey, envkey)
                for pwdData in pwdList:
                    self.loadSingleData(groupKey, envkey, pwdData)

        # 加载完成，刷新适应页面
        self.refreshCanvas()

    def loadSingleGroup(self, groupKey) -> None:
        """加载特定组"""
        pwdSingleFrameKey = utils.createKey("pwdSingleFrame", groupKey)
        pwdGroupLineKey = utils.createKey("pwdGroupLine", groupKey)
        pwdGroupLabelKey = utils.createKey("pwdGroupLabel", groupKey)
        pwdGroupPackBtnKey = utils.createKey("pwdGroupBtn", groupKey, "pack")
        pwdGroupAddBtnKey = utils.createKey("pwdGroupBtn", groupKey, "add")
        pwdGroupEditBtnKey = utils.createKey("pwdGroupBtn", groupKey, "edit")
        pwdGroupDelBtnKey = utils.createKey("pwdGroupBtn", groupKey, "del")

        self.createFrame("pwdContentFrame", pwdSingleFrameKey)
        self.createFrame(pwdSingleFrameKey, pwdGroupLineKey)
        pwdGroupPackBtn = self.createLabel(
            pwdGroupLineKey,
            pwdGroupPackBtnKey,
            {"image": self.getImage("pack", "pwdbookIcon")},
        )
        pwdGroupAddBtn = self.createLabel(
            pwdGroupLineKey,
            pwdGroupAddBtnKey,
            {"image": self.getImage("add", "pwdbookIcon")},
        )
        pwdGroupEditBtn = self.createLabel(
            pwdGroupLineKey,
            pwdGroupEditBtnKey,
            {"image": self.getImage("edit", "pwdbookIcon")},
        )
        pwdGroupDelBtn = self.createLabel(
            pwdGroupLineKey,
            pwdGroupDelBtnKey,
            {"image": self.getImage("delete", "pwdbookIcon")},
        )
        self.createLabel(pwdGroupLineKey, pwdGroupLabelKey, {"text": groupKey})

        pwdGroupDelBtn.bind(
            Event.MouseLeftClick,
            eventAdaptor(
                self.loadDeleteDialog,
                eventInfo={
                    "groupKey": groupKey,
                    "widget": pwdSingleFrameKey,
                    "method": self.clickDeleteGroup,
                },
            ),
        )
        pwdGroupPackBtn.bind(
            Event.MouseLeftClick,
            eventAdaptor(self.clickPackGroup, groupKey=groupKey),
        )
        pwdGroupEditBtn.bind(
            Event.MouseLeftClick,
            eventAdaptor(self.loadEditGroupDialog, groupKey=groupKey),
        )

    def loadSingleEnv(self, groupKey: str, envkey: str) -> None:
        """加载特定Env"""
        pwdSingleFrameKey = utils.createKey("pwdSingleFrame", groupKey)

        pwdEnvFrameKey = utils.createKey("pwdEnvFrame", groupKey, envkey)
        pwdEnvLineKey = utils.createKey("pwdEnvLineFrame", groupKey, envkey)
        pwdEmptyKey = utils.createKey("pwdEmptyLabel", groupKey, envkey)
        pwdEnvKey = utils.createKey("pwdEnvLabel", groupKey, envkey)
        pwdEnvPackKey = utils.createKey("pwdEnvBtn", groupKey, envkey, "pack")
        pwdEnvAddKey = utils.createKey("pwdEnvBtn", groupKey, envkey, "add")
        pwdEnvEditKey = utils.createKey("pwdEnvBtn", groupKey, envkey, "edit")
        pwdEnvDelKey = utils.createKey("pwdEnvBtn", groupKey, envkey, "del")

        self.createFrame(pwdSingleFrameKey, pwdEnvFrameKey)
        self.createLabel(pwdEnvFrameKey, pwdEmptyKey)
        self.createFrame(pwdEnvFrameKey, pwdEnvLineKey)
        pwdEnvPackBtn = self.createLabel(
            pwdEnvLineKey,
            pwdEnvPackKey,
            {"image": self.getImage("pack", "pwdbookIcon")},
        )
        pwdEnvAddBtn = self.createLabel(
            pwdEnvLineKey, pwdEnvAddKey, {"image": self.getImage("add", "pwdbookIcon")}
        )
        pwdEnvEditBtn = self.createLabel(
            pwdEnvLineKey,
            pwdEnvEditKey,
            {"image": self.getImage("edit", "pwdbookIcon")},
        )
        pwdEnvDelBtn = self.createLabel(
            pwdEnvLineKey,
            pwdEnvDelKey,
            {"image": self.getImage("delete", "pwdbookIcon")},
        )
        self.createLabel(pwdEnvLineKey, pwdEnvKey, {"text": envkey})

        pwdEnvEditBtn.bind(
            Event.MouseLeftClick,
            eventAdaptor(self.loadEditEnvDialog, groupKey=groupKey, envKey=envkey),
        )
        pwdEnvDelBtn.bind(
            Event.MouseLeftClick,
            eventAdaptor(
                self.loadDeleteDialog,
                eventInfo={
                    "groupKey": groupKey,
                    "envKey": envkey,
                    "widget": pwdEnvFrameKey,
                    "method": self.clickDeleteEnv,
                },
            ),
        )
        pwdEnvPackBtn.bind(
            Event.MouseLeftClick,
            eventAdaptor(self.clickPackEnv, groupKey=groupKey, envkey=envkey),
        )

    def loadSingleData(self, groupKey: str, envkey: str, pwdData: dict) -> None:
        """加载特定密码数据"""
        pwdEnvFrameKey = utils.createKey("pwdEnvFrame", groupKey, envkey)
        pwdDataId = pwdData["id"]
        pwdDataFrameKey = utils.createKey("pwdDataFrame", pwdDataId)
        self.createFrame(pwdEnvFrameKey, pwdDataFrameKey)

        for pwdKey, pwdValue in pwdData.items():
            if (not utils.isEmpty(pwdValue) and pwdKey != "id") or pwdKey == "labels":
                pwdItemFrameKey = utils.createKey(
                    "pwdItemFrame",
                    pwdDataId,
                    pwdKey,
                )
                pwdItemLabelKey = utils.createKey(
                    "pwdItemLabel",
                    pwdDataId,
                    pwdKey,
                )
                pwdItemValueKey = utils.createKey(
                    "pwdItemValue",
                    pwdDataId,
                    pwdKey,
                )
                pwdItemCopyKey = utils.createKey(
                    "pwdItemBtn", pwdDataId, pwdKey, "copy"
                )

                self.createFrame(pwdDataFrameKey, pwdItemFrameKey)
                self.createLabel(pwdItemFrameKey, pwdItemLabelKey, {"text": pwdKey})

                if pwdKey == "labels":
                    for pwdLabel in pwdValue:
                        pwdValueLabelKey = utils.createKey(
                            "pwdValueLabel",
                            pwdDataId,
                            pwdKey,
                            pwdLabel,
                        )
                        self.createLabel(
                            pwdItemFrameKey, pwdValueLabelKey, {"text": pwdLabel}
                        )
                    pwdValueEditKey = utils.createKey(
                        "pwdItemBtn", pwdDataId, pwdKey, "edit"
                    )
                    pwdValueDelKey = utils.createKey(
                        "pwdItemBtn", pwdDataId, pwdKey, "del"
                    )
                    pwdValueEditBtn = self.createLabel(
                        pwdItemFrameKey,
                        pwdValueEditKey,
                        {"image": self.getImage("edit", "pwdbookIcon")},
                    )
                    pwdValueDelBtn = self.createLabel(
                        pwdItemFrameKey,
                        pwdValueDelKey,
                        {"image": self.getImage("delete", "pwdbookIcon")},
                    )
                    pwdValueDelBtn.bind(
                        Event.MouseLeftClick,
                        eventAdaptor(
                            self.loadDeleteDialog,
                            eventInfo={
                                "groupKey": groupKey,
                                "envKey": envkey,
                                "widget": pwdDataFrameKey,
                                "id": pwdDataId,
                                "method": self.clickDeletePwdData,
                            },
                        ),
                    )
                elif pwdKey == "website":
                    pwdItemBrowserBtn = self.createLabel(
                        pwdItemFrameKey,
                        pwdItemCopyKey,
                        {"image": self.getImage("browser", "pwdbookIcon")},
                    )
                    pwdItemValue = self.createEntry(pwdItemFrameKey, pwdItemValueKey)

                    pwdItemValue.insert(tk.END, pwdValue)
                    pwdItemValue.config(state="readonly")
                    pwdItemBrowserBtn.bind(
                        Event.MouseLeftClick,
                        eventAdaptor(self.clickBrowser, pwdData=pwdData),
                    )
                else:
                    pwdItemCopyBtn = self.createLabel(
                        pwdItemFrameKey,
                        pwdItemCopyKey,
                        {"image": self.getImage("copy", "pwdbookIcon")},
                    )
                    pwdItemValue = self.createEntry(pwdItemFrameKey, pwdItemValueKey)

                    pwdItemValue.insert(tk.END, pwdValue)
                    pwdItemValue.config(state="readonly")
                    pwdItemCopyBtn.bind(
                        Event.MouseLeftClick,
                        eventAdaptor(
                            self.clickCopy,
                            text=pwdValue,
                            btnKey=pwdItemCopyKey,
                        ),
                    )
