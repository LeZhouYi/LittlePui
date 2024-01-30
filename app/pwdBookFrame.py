import os
import pyperclip
import webbrowser
import tkinter as tk
from time import sleep
from PIL import Image, ImageTk
from utils import utils
from config.pwdbook import PwdBook
from frame.baseFrame import BaseFrame
from control.event import Event, WmEvent
from control.controller import Controller

"""密码内容页"""


class PwdBookFrame(BaseFrame):
    def __init__(self, controller: Controller) -> None:
        super().__init__(controller)
        self.passwordBook = PwdBook(self.getConfig().getPwdBook())
        self.loadIcon()
        self.checkPwdData()

    def loadIcon(self) -> None:
        """加载图片资源"""
        iconPaths = os.path.join(os.getcwd(), self.getConfig().getPwdIconPath())
        # 遍历目标路径所有图片
        for fileName in os.listdir(iconPaths):
            if utils.isPhoto(fileName):
                # 加载图片并调整为适合尺寸
                iconfile = os.path.join(iconPaths, fileName)
                image = Image.open(iconfile).resize(self.getConfig().getpwdIconSize())
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
            utils.eventAdaptor(self.clickDisplayGroup, groupKey=groupKey),
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
            utils.eventAdaptor(self.clickPackGroup, groupKey=groupKey),
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
            utils.eventAdaptor(self.clickDisplayEnv, groupKey=groupKey, envkey=envkey),
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
            utils.eventAdaptor(self.clickPackEnv, groupKey=groupKey, envkey=envkey),
        )

    ###########渲染相关################
    def loadEditGroupDialog(self, groupKey:str)->None:
        """加载编辑组提示框"""
        mainWindow = self.getWidget("baseWindow")
        pwdDeleteDialog = tk.Toplevel(mainWindow, cnf=self.getCnf("pwdEditGroupDialog"))
        pwdDeleteDialog.title("")
        # 禁用主窗口操作
        mainWindow.update_idletasks()
        pwdDeleteDialog.transient(mainWindow)
        pwdDeleteDialog.grab_set()

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
        mainWindow = self.getWidget("baseWindow")
        pwdDeleteDialog = tk.Toplevel(mainWindow, cnf=self.getCnf("pwdDeleteDialog"))
        pwdDeleteDialog.title("")
        # 禁用主窗口操作
        mainWindow.update_idletasks()
        pwdDeleteDialog.transient(mainWindow)
        pwdDeleteDialog.grab_set()
        # 计算并使提示框显示居中
        winX = (
            mainWindow.winfo_rootx()
            + (mainWindow.winfo_width() // 2)
            - (pwdDeleteDialog.winfo_width() // 2)
        )
        winY = (
            mainWindow.winfo_rooty()
            + (mainWindow.winfo_height() // 2)
            - (pwdDeleteDialog.winfo_height() // 2)
        )
        pwdDeleteDialog.geometry("+{}+{}".format(winX, winY))
        pwdDeleteDialog.bind(
            WmEvent.WindowClose,
            utils.eventAdaptor(self.closeDialog, dialogKey="pwdDeleteDialog"),
        )

        pwdDelDlgFrame = tk.Frame(pwdDeleteDialog, cnf=self.getCnf("pwdDelDlgFrame"))
        pwdDelDlgLabel = tk.Label(
            pwdDelDlgFrame, text="请确认是否删除", cnf=self.getCnf("pwdDelDlgLabel")
        )
        pwdDelDlgYesBtn = tk.Label(
            pwdDelDlgFrame, text="确定", cnf=self.getCnf("pwdDelDlgYesBtn")
        )
        pwdDelDlgNoBtn = tk.Label(
            pwdDelDlgFrame, text="取消", cnf=self.getCnf("pwdDelDlgNoBtn")
        )

        eventInfo["dialogKey"] = "pwdDeleteDialog"

        pwdDelDlgYesBtn.bind(
            Event.MouseLeftClick,
            utils.eventAdaptor(eventInfo["method"], eventInfo=eventInfo),
        )
        pwdDelDlgNoBtn.bind(
            Event.MouseLeftClick,
            utils.eventAdaptor(self.closeDialog, dialogKey="pwdDeleteDialog"),
        )

        self.cacheWidget(pwdDeleteDialog, "baseWindow", "pwdDeleteDialog")
        self.cacheWidget(pwdDelDlgFrame, "pwdDeleteDialog", "pwdDelDlgFrame")
        self.cacheWidget(pwdDelDlgLabel, "pwdDelDlgFrame", "pwdDelDlgLabel")
        self.cacheWidget(pwdDelDlgYesBtn, "pwdDelDlgFrame", "pwdDelDlgYesBtn")
        self.cacheWidget(pwdDelDlgNoBtn, "pwdDelDlgFrame", "pwdDelDlgNoBtn")

        mainWindow.wait_window(pwdDeleteDialog)

    def loadPasswordNote(self, contentFrameKey: str) -> None:
        """加载密码本页面"""
        contentFrame = self.getWidget(contentFrameKey)
        # 构造基础框架
        pwdDispalyFrame = tk.Frame(contentFrame, cnf=self.getCnf("pwdDispalyFrame"))
        pwdScrollCanvas = tk.Canvas(pwdDispalyFrame, cnf=self.getCnf("pwdScrollCanvas"))
        pwdContentFrame = tk.Frame(pwdScrollCanvas, cnf=self.getCnf("pwdContentFrame"))
        pwdScrollBar = tk.Scrollbar(pwdDispalyFrame, self.getCnf("pwdScrollBar"))

        # 绑定滚动事件
        pwdScrollCanvas.config(yscrollcommand=pwdScrollBar.set, yscrollincrement=5)
        pwdScrollBar.config(command=pwdScrollCanvas.yview)  # 绑定滚动

        # 缓存并Pack
        self.cacheWidget(pwdDispalyFrame, contentFrameKey, "pwdDispalyFrame")
        self.cacheWidget(pwdScrollCanvas, "pwdDispalyFrame", "pwdScrollCanvas")
        self.cacheWidget(pwdContentFrame, "pwdScrollCanvas", "pwdContentFrame")
        self.cacheWidget(pwdScrollBar, "pwdDispalyFrame", "pwdScrollBar")

        # 加载密码内容
        for groupKey in self.passwordBook.getGroupKeys():
            self.loadSingleGroup(groupKey)
            group = self.passwordBook.getGroup(groupKey)
            for envkey, pwdList in group.items():
                self.loadSingleEnv(groupKey,envkey)
                for pwdData in pwdList:
                    self.loadSingleData(groupKey,envkey,pwdData)

        # 加载完成，刷新适应页面
        self.refreshCanvas()

    def loadSingleGroup(self,groupKey)->None:
        """加载特定组"""
        pwdContentFrame = self.getWidget("pwdContentFrame")

        pwdSingleFrameKey = utils.createKey("pwdSingleFrame", groupKey)
        pwdGroupLineKey = utils.createKey("pwdGroupLine", groupKey)
        pwdGroupLabelKey = utils.createKey("pwdGroupLabel", groupKey)
        pwdGroupPackBtnKey = utils.createKey("pwdGroupBtn", groupKey, "pack")
        pwdGroupAddBtnKey = utils.createKey("pwdGroupBtn", groupKey, "add")
        pwdGroupEditBtnKey = utils.createKey("pwdGroupBtn", groupKey, "edit")
        pwdGroupDelBtnKey = utils.createKey("pwdGroupBtn", groupKey, "del")

        pwdSingleFrame = tk.Frame(
            pwdContentFrame, cnf=self.getCnf(pwdSingleFrameKey)
        )
        pwdGroupLineFrame = tk.Frame(
            pwdSingleFrame, cnf=self.getCnf(pwdGroupLineKey)
        )
        pwdGroupLabel = tk.Label(
            pwdGroupLineFrame, text=groupKey, cnf=self.getCnf(pwdGroupLabelKey)
        )
        pwdGroupAddBtn = tk.Label(
            pwdGroupLineFrame,
            image=self.getImage("add", "pwdbookIcon"),
            cnf=self.getCnf(pwdGroupAddBtnKey),
        )
        pwdGroupPackBtn = tk.Label(
            pwdGroupLineFrame,
            image=self.getImage("pack", "pwdbookIcon"),
            cnf=self.getCnf(pwdGroupPackBtnKey),
        )
        pwdGroupEditBtn = tk.Label(
            pwdGroupLineFrame,
            image=self.getImage("edit", "pwdbookIcon"),
            cnf=self.getCnf(pwdGroupEditBtnKey),
        )
        pwdGroupDelBtn = tk.Label(
            pwdGroupLineFrame,
            image=self.getImage("delete", "pwdbookIcon"),
            cnf=self.getCnf(pwdGroupDelBtnKey),
        )

        pwdGroupDelBtn.bind(
            Event.MouseLeftClick,
            utils.eventAdaptor(
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
            utils.eventAdaptor(self.clickPackGroup, groupKey=groupKey),
        )
        pwdGroupEditBtn.bind(
            Event.MouseLeftClick,
            utils.eventAdaptor(self.loadEditGroupDialog, groupKey=groupKey)
        )

        self.cacheWidget(pwdSingleFrame, "pwdContentFrame", pwdSingleFrameKey)
        self.cacheWidget(pwdGroupLineFrame, pwdSingleFrameKey, pwdGroupLineKey)
        self.cacheWidget(pwdGroupPackBtn, pwdGroupLineKey, pwdGroupPackBtnKey)
        self.cacheWidget(pwdGroupAddBtn, pwdGroupLineKey, pwdGroupAddBtnKey)
        self.cacheWidget(pwdGroupEditBtn, pwdGroupLineKey, pwdGroupEditBtnKey)
        self.cacheWidget(pwdGroupDelBtn, pwdGroupLineKey, pwdGroupDelBtnKey)
        self.cacheWidget(pwdGroupLabel, pwdGroupLineKey, pwdGroupLabelKey)

    def loadSingleEnv(self,groupKey:str,envkey:str)->None:
        """加载特定Env"""
        pwdSingleFrameKey = utils.createKey("pwdSingleFrame", groupKey)
        pwdSingleFrame = self.getWidget(pwdSingleFrameKey)

        pwdEnvFrameKey = utils.createKey("pwdEnvFrame", groupKey, envkey)
        pwdEnvLineKey = utils.createKey("pwdEnvLineFrame", groupKey, envkey)
        pwdEmptyKey = utils.createKey("pwdEmptyLabel", groupKey, envkey)
        pwdEnvKey = utils.createKey("pwdEnvLabel", groupKey, envkey)
        pwdEnvPackKey = utils.createKey("pwdEnvBtn", groupKey, envkey, "pack")
        pwdEnvAddKey = utils.createKey("pwdEnvBtn", groupKey, envkey, "add")
        pwdEnvEditKey = utils.createKey("pwdEnvBtn", groupKey, envkey, "edit")
        pwdEnvDelKey = utils.createKey("pwdEnvBtn", groupKey, envkey, "del")

        pwdEnvFrame = tk.Frame(pwdSingleFrame, cnf=self.getCnf(pwdEnvFrameKey))
        pwdEnvLineFrame = tk.Frame(pwdEnvFrame, cnf=self.getCnf(pwdEnvLineKey))
        pwdEmptyLabel = tk.Label(pwdEnvFrame, cnf=self.getCnf(pwdEmptyKey))
        pwdEnvLabel = tk.Label(
            pwdEnvLineFrame, text=envkey, cnf=self.getCnf(pwdEnvKey)
        )
        pwdEnvPackBtn = tk.Label(
            pwdEnvLineFrame,
            image=self.getImage("pack", "pwdbookIcon"),
            cnf=self.getCnf(pwdEnvPackKey),
        )
        pwdEnvAddBtn = tk.Label(
            pwdEnvLineFrame,
            image=self.getImage("add", "pwdbookIcon"),
            cnf=self.getCnf(pwdEnvAddKey),
        )
        pwdEnvEditBtn = tk.Label(
            pwdEnvLineFrame,
            image=self.getImage("edit", "pwdbookIcon"),
            cnf=self.getCnf(pwdEnvEditKey),
        )
        pwdEnvDelBtn = tk.Label(
            pwdEnvLineFrame,
            image=self.getImage("delete", "pwdbookIcon"),
            cnf=self.getCnf(pwdEnvDelKey),
        )

        pwdEnvDelBtn.bind(
            Event.MouseLeftClick,
            utils.eventAdaptor(
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
            utils.eventAdaptor(
                self.clickPackEnv, groupKey=groupKey, envkey=envkey
            ),
        )

        self.cacheWidget(pwdEnvFrame, pwdSingleFrameKey, pwdEnvFrameKey)
        self.cacheWidget(pwdEmptyLabel, pwdEnvFrameKey, pwdEmptyKey)
        self.cacheWidget(pwdEnvLineFrame, pwdEnvFrameKey, pwdEnvLineKey)
        self.cacheWidget(pwdEnvPackBtn, pwdEnvLineKey, pwdEnvPackKey)
        self.cacheWidget(pwdEnvAddBtn, pwdEnvLineKey, pwdEnvAddKey)
        self.cacheWidget(pwdEnvEditBtn, pwdEnvLineKey, pwdEnvEditKey)
        self.cacheWidget(pwdEnvDelBtn, pwdEnvLineKey, pwdEnvDelKey)
        self.cacheWidget(pwdEnvLabel, pwdEnvLineKey, pwdEnvKey)

    def loadSingleData(self,groupKey:str, envkey:str,pwdData:dict)->None:
        """加载特定密码数据"""
        pwdEnvFrameKey = utils.createKey("pwdEnvFrame", groupKey, envkey)
        pwdEnvFrame = self.getWidget(pwdEnvFrameKey)
        pwdDataId = pwdData["id"]
        pwdDataFrameKey = utils.createKey("pwdDataFrame", pwdDataId)
        pwdDataFrame = tk.Frame(
            pwdEnvFrame, cnf=self.getCnf(pwdDataFrameKey)
        )
        self.cacheWidget(pwdDataFrame, pwdEnvFrameKey, pwdDataFrameKey)

        for pwdKey, pwdValue in pwdData.items():
            if (
                not utils.isEmpty(pwdValue) and pwdKey != "id"
            ) or pwdKey == "labels":
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

                pwdItemFrame = tk.Frame(
                    pwdDataFrame, cnf=self.getCnf(pwdItemFrameKey)
                )
                pwdItemLabel = tk.Label(
                    pwdItemFrame,
                    text=pwdKey,
                    cnf=self.getCnf(pwdItemLabelKey),
                )

                self.cacheWidget(
                    pwdItemFrame, pwdDataFrameKey, pwdItemFrameKey
                )
                self.cacheWidget(
                    pwdItemLabel, pwdItemFrameKey, pwdItemLabelKey
                )

                if pwdKey == "labels":
                    for pwdLabel in pwdValue:
                        pwdValueLabelKey = utils.createKey(
                            "pwdValueLabel",
                            pwdDataId,
                            pwdKey,
                            pwdLabel,
                        )
                        pwdValueLabel = tk.Label(
                            pwdItemFrame,
                            text=pwdLabel,
                            cnf=self.getCnf(pwdValueLabelKey),
                        )
                        self.cacheWidget(
                            pwdValueLabel, pwdItemFrameKey, pwdValueLabelKey
                        )
                    pwdValueEditKey = utils.createKey(
                        "pwdItemBtn", pwdDataId, pwdKey, "edit"
                    )
                    pwdValueDelKey = utils.createKey(
                        "pwdItemBtn", pwdDataId, pwdKey, "del"
                    )
                    pwdValueEditBtn = tk.Label(
                        pwdItemFrame,
                        image=self.getImage("edit", "pwdbookIcon"),
                        cnf=self.getCnf(pwdValueEditKey),
                    )
                    pwdValueDelBtn = tk.Label(
                        pwdItemFrame,
                        image=self.getImage("delete", "pwdbookIcon"),
                        cnf=self.getCnf(pwdValueDelKey),
                    )
                    pwdValueDelBtn.bind(
                        Event.MouseLeftClick,
                        utils.eventAdaptor(
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
                    self.cacheWidget(
                        pwdValueEditBtn, pwdItemFrameKey, pwdValueEditKey
                    )
                    self.cacheWidget(
                        pwdValueDelBtn, pwdItemFrameKey, pwdValueDelKey
                    )
                elif pwdKey == "website":
                    pwdItemValue = tk.Entry(
                        pwdItemFrame, cnf=self.getCnf(pwdItemValueKey)
                    )
                    pwdItemValue.insert(tk.END, pwdValue)
                    pwdItemValue.config(state="readonly")
                    pwdItemBrowserBtn = tk.Label(
                        pwdItemFrame,
                        image=self.getImage("browser", "pwdbookIcon"),
                        cnf=self.getCnf(pwdItemCopyKey),
                    )

                    pwdItemBrowserBtn.bind(
                        Event.MouseLeftClick,
                        utils.eventAdaptor(
                            self.clickBrowser, pwdData=pwdData
                        ),
                    )

                    self.cacheWidget(
                        pwdItemBrowserBtn, pwdItemFrameKey, pwdItemCopyKey
                    )
                    self.cacheWidget(
                        pwdItemValue, pwdItemFrameKey, pwdItemValueKey
                    )
                else:
                    pwdItemValue = tk.Entry(
                        pwdItemFrame, cnf=self.getCnf(pwdItemValueKey)
                    )
                    pwdItemValue.insert(tk.END, pwdValue)
                    pwdItemValue.config(state="readonly")
                    pwdItemCopyBtn = tk.Label(
                        pwdItemFrame,
                        image=self.getImage("copy", "pwdbookIcon"),
                        cnf=self.getCnf(pwdItemCopyKey),
                    )

                    pwdItemCopyBtn.bind(
                        Event.MouseLeftClick,
                        utils.eventAdaptor(
                            self.clickCopy,
                            text=pwdValue,
                            btnKey=pwdItemCopyKey,
                        ),
                    )

                    self.cacheWidget(
                        pwdItemCopyBtn, pwdItemFrameKey, pwdItemCopyKey
                    )
                    self.cacheWidget(
                        pwdItemValue, pwdItemFrameKey, pwdItemValueKey
                    )