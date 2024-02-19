import os
import pyperclip
import webbrowser
import tkinter as tk
from time import sleep
from PIL import Image, ImageTk
from core.utils import utils
from app.data.pwdbook import PwdBook
from core.frame.absFrame import BaseFrame
from core.frame.absDialog import ComfirmDialog,InputDialog
from core.control.event import Event, eventAdaptor
from core.control.controller import Controller

"""密码内容页"""


class PwdBookFrame(BaseFrame):
    def __init__(self, controller: Controller) -> None:
        super().__init__(controller)
        self.passwordBook = PwdBook(self.getCnfData("pwdBookPath"))
        self.dialog = None #删除弹窗
        self.loadIcon()
        self.checkPwdData()

    def loadIcon(self) -> None:
        """加载图片资源"""
        iconPaths = os.path.join(os.getcwd(), self.getCnfData("pwdIconPath"))
        # 遍历目标路径所有图片
        for fileName in os.listdir(iconPaths):
            if utils.isPhoto(fileName):
                # 加载图片并调整为适合尺寸
                iconfile = os.path.join(iconPaths, fileName)
                image = Image.open(iconfile).resize(
                    self.getCnfData("pwdIconSize")
                )
                image = ImageTk.PhotoImage(image)
                # 缓存
                self.cacheImage(image, utils.getFileName(fileName), "pwdbookIcon")

    def checkPwdData(self) -> None:
        """检查密码本数据，若无数据则加入默认数据"""
        if len(self.passwordBook.getGroupKeys()) == 0:
            self.passwordBook.addGroup("default")

    def getImgInfo(self,key:str)->dict:
        """构建图片按钮的构建信息"""
        return {"image": self.getImage(key, "pwdbookIcon")}

    ###########控件事件################
    def clickAddData(self,event,groupKey:str,envKey:str)->None:
        """点击确认添加数据"""
        labelText = self.dialog.getEntryValue("labels")
        if utils.isEmpty(labelText):
            labelText = []
        else:
            labelText = labelText.split("、")
        data = {
            "account": self.dialog.getEntryValue("account"),
            "password": self.dialog.getEntryValue("password"),
            "website": self.dialog.getEntryValue("website"),
            "labels": labelText
        }
        self.passwordBook.addData(groupKey,envKey,data)
        self.passwordBook.writeToFile()
        self.loadSingleData(groupKey,envKey,data)
        self.dialog.closeDialog(event)
        self.updatePwdPage()

    def clickAddEnv(self,event,groupKey:str)->None:
        """点击确认添加Env"""
        entryText = self.dialog.getEntryValue("env")
        if self.checkEnvEntry(self.dialog.getYesBtnKey(),groupKey,entryText):
            #新增Env并保存
            self.passwordBook.addEnv(groupKey,entryText)
            self.passwordBook.writeToFile()
            # 加载新控件
            self.loadFullEnv(groupKey,entryText)
            # 关闭弹窗
            self.dialog.closeDialog(event)
            self.updatePwdPage()

    def clickAddGroup(self,event)->None:
        """点击确认添加Group"""
        entryText = self.dialog.getEntryValue("group")
        if self.checkGroupEntry(self.dialog.getYesBtnKey(),entryText):
            # 新增组并保存
            self.passwordBook.addGroup(entryText)
            self.passwordBook.writeToFile()
            # 加载新控件
            self.loadFullGroup(entryText)
            # 关闭弹窗
            self.dialog.closeDialog(event)
            self.updatePwdPage()

    def clickComfirmEnv(self,event, groupKey:str, envKey:str)->None:
        """点击确认编辑Env"""
        entryText = self.dialog.getEntryValue("env")
        if self.checkEnvEntry(self.dialog.getYesBtnKey(),groupKey,entryText):
            if envKey == entryText:
                self.dialog.closeDialog(event)
            else:
                #编辑并保存
                self.passwordBook.editEnv(groupKey,envKey,entryText)
                self.passwordBook.writeToFile()
                #清理相关控件
                pwdEnvFrameKey = self.createKey("pwdEnvFrame", groupKey, envKey)
                self.destroyWidget(pwdEnvFrameKey)
                # 加载新控件
                self.loadFullEnv(groupKey,entryText)
                # 关闭弹窗
                self.dialog.closeDialog(event)

    def clickComfirmGroup(self, event, groupKey: str) -> None:
        """点击确认编辑组"""
        entryText = self.dialog.getEntryValue("group")
        if self.checkGroupEntry(self.dialog.getYesBtnKey(),entryText):
            if groupKey == entryText:
                self.dialog.closeDialog(event)
            else:
                # 编辑组并保存
                self.passwordBook.editGroup(groupKey, entryText)
                self.passwordBook.writeToFile()
                # 清理旧控件
                pwdSingleFrameKey = self.createKey("pwdSingleFrame", groupKey)
                self.destroyWidget(pwdSingleFrameKey)
                # 加载新控件
                self.loadFullGroup(entryText)
                # 关闭弹窗
                self.dialog.closeDialog(event)

    def clickDeleteGroup(self, event, eventInfo: dict) -> None:
        """点击删除组事件"""
        self.passwordBook.deletetGroup(eventInfo["groupKey"])
        self.passwordBook.writeToFile()
        self.destroyWidget(eventInfo["widget"])
        self.dialog.closeDialog(event)
        self.updatePwdPage()

    def clickDeleteEnv(self, event, eventInfo: dict) -> None:
        """点击删除环境事件"""
        self.passwordBook.deletetEnv(eventInfo["groupKey"], eventInfo["envKey"])
        self.passwordBook.writeToFile()
        self.destroyWidget(eventInfo["widget"])
        self.dialog.closeDialog(event)
        self.updatePwdPage()

    def clickDeletePwdData(self, event, eventInfo: dict) -> None:
        """点击删除密码数据"""
        self.passwordBook.deleteData(
            eventInfo["groupKey"], eventInfo["envKey"], eventInfo["id"]
        )
        self.passwordBook.writeToFile()
        self.destroyWidget(eventInfo["widget"])
        self.dialog.closeDialog(event)
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
            pwdEnvFrameKey = self.createKey("pwdEnvFrame", groupKey, envkey)
            pwdEnvFrame = self.getWidget(pwdEnvFrameKey)
            pwdEnvFrame.pack_forget()

        packBtnKey = self.createKey("pwdBtn", groupKey, "pack")
        packBtn = self.getWidget(packBtnKey)
        packBtn.configure(image=self.getImage("display", "pwdbookIcon"))
        packBtn.unbind(Event.MouseLeftClick)
        self.bindClickMethod(packBtnKey,self.clickDisplayGroup,groupKey=groupKey)

    def clickDisplayGroup(self, event, groupKey: str) -> None:
        """点击展开组内容"""
        group = self.passwordBook.getGroup(groupKey)
        for envkey, pwdList in group.items():
            pwdEnvFrameKey = self.createKey("pwdEnvFrame", groupKey, envkey)
            pwdEnvFrame = self.getWidget(pwdEnvFrameKey)
            pwdEnvFrame.pack(self.getPackCnf(pwdEnvFrameKey))

        packBtnKey = self.createKey("pwdBtn", groupKey, "pack")
        packBtn = self.getWidget(packBtnKey)
        packBtn.configure(image=self.getImage("pack", "pwdbookIcon"))
        packBtn.unbind(Event.MouseLeftClick)
        self.bindClickMethod(packBtn,self.clickPackGroup, groupKey=groupKey)

    def clickPackEnv(self, event, groupKey: str, envkey: str) -> None:
        """点击关闭Env内容"""
        group = self.passwordBook.getGroup(groupKey)
        for pwdData in group[envkey]:
            pwdDataId = pwdData["id"]
            pwdDataFrameKey = self.createKey("pwdDataFrame", pwdDataId)
            pwdDataFrame = self.getWidget(pwdDataFrameKey)
            pwdDataFrame.pack_forget()

        packBtnKey = self.createKey("pwdEnvBtn", groupKey, envkey, "pack")
        packBtn = self.getWidget(packBtnKey)
        packBtn.configure(image=self.getImage("pack", "pwdbookIcon"))
        packBtn.unbind(Event.MouseLeftClick)
        self.bindClickMethod(packBtnKey,self.clickDisplayEnv, groupKey=groupKey, envkey=envkey)

    def clickDisplayEnv(self, event, groupKey: str, envkey: str) -> None:
        """点击关闭Env内容"""
        group = self.passwordBook.getGroup(groupKey)
        for pwdData in group[envkey]:
            pwdDataId = pwdData["id"]
            pwdDataFrameKey = self.createKey("pwdDataFrame", pwdDataId)
            pwdDataFrame = self.getWidget(pwdDataFrameKey)
            pwdDataFrame.pack(self.getPackCnf(pwdDataFrameKey))

        packBtnKey = self.createKey("pwdEnvBtn", groupKey, envkey, "pack")
        packBtn = self.getWidget(packBtnKey)
        packBtn.configure(image=self.getImage("pack", "pwdbookIcon"))
        packBtn.unbind(Event.MouseLeftClick)
        self.bindClickMethod(packBtnKey,self.clickPackEnv, groupKey=groupKey, envkey=envkey)

    ###########渲染相关################
    def loadAddDataDialog(self,event,groupKey:str,envKey:str)->None:
        """加载添加密码数据提示框"""
        self.dialog = InputDialog(self.getController(),"baseWindow","adddata")
        self.dialog.loadDialog("请输入数据")
        self.dialog.addEntry("account","account")
        self.dialog.addEntry("password","password")
        self.dialog.addEntry("website", "website")
        self.dialog.addEntry("labels", "labels")
        self.dialog.bindYesMethod(self.clickAddData,groupKey=groupKey,envKey=envKey)
        self.dialog.packDialog()

    def loadAddEnvDialog(self, event,groupKey:str)->None:
        """加载添加Env提示框"""
        self.dialog = InputDialog(self.getController(),"baseWindow","addenv")
        self.dialog.loadDialog("请输入Env")
        self.dialog.addEntry("env",None)
        self.dialog.bindYesMethod(self.clickAddEnv,groupKey=groupKey)
        self.dialog.packDialog()

    def loadAddGroupDialog(self, event)->None:
        """加载添加组提示框"""
        self.dialog = InputDialog(self.getController(),"baseWindow","addgroup")
        self.dialog.loadDialog("请输入组名")
        self.dialog.addEntry("group",None)
        self.dialog.bindYesMethod(self.clickAddGroup)
        self.dialog.packDialog()

    def loadEditEnvDialog(self, event, groupKey: str, envKey: str) -> None:
        """加载编辑Env提示框"""
        self.dialog = InputDialog(self.getController(),"baseWindow","editenv")
        self.dialog.loadDialog("请输入Env名")
        self.dialog.addEntry("env",None,envKey)
        self.dialog.bindYesMethod(self.clickComfirmEnv,groupKey=groupKey,envKey=envKey)
        self.dialog.packDialog()

    def loadEditGroupDialog(self, event, groupKey: str) -> None:
        """加载编辑组提示框"""
        self.dialog = InputDialog(self.getController(),"baseWindow","editgroup")
        self.dialog.loadDialog("请输入组名")
        self.dialog.addEntry("group",None,groupKey)
        self.dialog.bindYesMethod(self.clickComfirmGroup, groupKey=groupKey)
        self.dialog.packDialog()

    def completeBtn(self, btnKey: str, controlKey: str) -> None:
        """点击按钮成功效果"""
        btn = self.getWidget(btnKey)
        btn.configure(image=self.getImage("complete", "pwdbookIcon"))
        sleep(0.8)
        btn.configure(image=self.getImage(controlKey, "pwdbookIcon"))

    def loadDeleteDialog(self,event,eventInfo: dict,) -> None:
        """加载删除提示框"""
        self.dialog = ComfirmDialog(self.getController(),"baseWindow","del")
        self.dialog.loadDialog(text="请确认是否删除")
        self.dialog.bindYesMethod(eventInfo["method"], eventInfo=eventInfo)
        self.dialog.packDialog()

    def loadPasswordNote(self, contentFrameKey: str) -> None:
        """加载密码本页面"""
        # 构造基础框架
        frameKey = self.createWidget(contentFrameKey, "pwdDispalyFrame")
        canvasKey = self.createWidget(frameKey, "pwdScrollCanvas")
        self.createWidget("pwdScrollCanvas", "pwdContentFrame")
        scrollBarKey = self.createWidget("pwdDispalyFrame", "pwdScrollBar")
        # 绑定滚动事件
        self.bindScroll(canvasKey,scrollBarKey)
        # 加载密码内容
        for groupKey in self.passwordBook.getGroupKeys():
            self.loadFullGroup(groupKey)
        # 加载完成，刷新适应页面
        self.refreshCanvas()

    def loadFullGroup(self, groupKey)->None:
        """加载特定组完整内容"""
        self.loadSingleGroup(groupKey)
        group = self.passwordBook.getGroup(groupKey)
        for envKey in group.keys():
            self.loadFullEnv(groupKey,envKey)

    def loadFullEnv(self,groupKey:str,envKey:str)->None:
        """加载特定Env完整内容"""
        group = self.passwordBook.getGroup(groupKey)
        self.loadSingleEnv(groupKey, envKey)
        for pwdData in group[envKey]:
            self.loadSingleData(groupKey, envKey, pwdData)

    def loadSingleGroup(self, groupKey) -> None:
        """加载特定组"""
        frameKey = self.createWidget("pwdContentFrame","pwdSingleFrame",None,groupKey)
        lineFrameKey = self.createWidget(frameKey,"pwdLine",None,groupKey)
        packBtnKey = self.createWidget(lineFrameKey,"pwdBtn",self.getImgInfo("pack"),groupKey,"pack")
        addBtnKey = self.createWidget(lineFrameKey,"pwdBtn",self.getImgInfo("add"),groupKey,"add")
        editBtnKey = self.createWidget(lineFrameKey,"pwdBtn",self.getImgInfo("edit"),groupKey,"edit")
        delBtnKey = self.createWidget(lineFrameKey,"pwdBtn",self.getImgInfo("delete"),groupKey,"del")
        self.createWidget(lineFrameKey, "pwdGroupLabel", {"text": groupKey},groupKey)
        #绑定事件
        self.bindClickMethod(delBtnKey,self.loadDeleteDialog,
                eventInfo={
                    "groupKey": groupKey,
                    "widget": frameKey,
                    "method": self.clickDeleteGroup,
                })
        self.bindClickMethod(packBtnKey,self.clickPackGroup, groupKey=groupKey)
        self.bindClickMethod(editBtnKey,self.loadEditGroupDialog, groupKey=groupKey)
        self.bindClickMethod(addBtnKey,self.loadAddGroupDialog)

    def loadSingleEnv(self, groupKey: str, envkey: str) -> None:
        """加载特定Env"""
        pwdSingleFrameKey = self.createKey("pwdSingleFrame", groupKey)
        envSuffix = self.createKey(groupKey, envkey)

        frameKey = self.createWidget(pwdSingleFrameKey,"pwdEnvFrame",None,envSuffix)
        self.createWidget(frameKey, "pwdEmptyLabel",None, envSuffix)
        lineFrameKey = self.createWidget(frameKey, "pwdEnvLineFrame",None, envSuffix)
        packBtnKey = self.createWidget(lineFrameKey, "pwdEnvBtn",self.getImgInfo("pack"),envSuffix, "pack")
        addBtnKey = self.createWidget(lineFrameKey, "pwdEnvBtn",self.getImgInfo("add"),envSuffix, "add")
        editBtnKey = self.createWidget(lineFrameKey, "pwdEnvBtn",self.getImgInfo("edit"),envSuffix, "edit")
        delBtnKey = self.createWidget(lineFrameKey, "pwdEnvBtn",self.getImgInfo("delete"),envSuffix, "del")
        self.createWidget(lineFrameKey, "pwdEnvLabel", {"text": envkey},envSuffix)

        self.bindClickMethod(editBtnKey,self.loadEditEnvDialog, groupKey=groupKey, envKey=envkey)
        self.bindClickMethod(delBtnKey,self.loadDeleteDialog,
                eventInfo={
                    "groupKey": groupKey,
                    "envKey": envkey,
                    "widget": frameKey,
                    "method": self.clickDeleteEnv,
                })
        self.bindClickMethod(packBtnKey,self.clickPackEnv, groupKey=groupKey, envkey=envkey)
        self.bindClickMethod(addBtnKey,self.loadAddEnvDialog, groupKey=groupKey)

    def loadSingleData(self, groupKey: str, envkey: str, pwdData: dict) -> None:
        """加载特定密码数据"""
        pwdEnvFrameKey = self.createKey("pwdEnvFrame", groupKey, envkey)
        pwdDataId = pwdData["id"]
        dataFrameKey = self.createWidget(pwdEnvFrameKey, "pwdDataFrame",None,pwdDataId)

        for pwdKey, pwdValue in pwdData.items():
            pwdDataSuffix = self.createKey(pwdDataId,pwdKey)
            if (not utils.isEmpty(pwdValue) and pwdKey != "id") or pwdKey == "labels":
                frameKey = self.createWidget(dataFrameKey, "pwdItemFrame",None,pwdDataSuffix)
                self.createWidget(frameKey, "pwdItemLabel", {"text": pwdKey},pwdDataSuffix)

                if pwdKey == "labels":
                    for pwdLabel in pwdValue:
                        self.createWidget(frameKey,"pwdValueLabel",{"text": pwdLabel},pwdDataSuffix,pwdLabel)
                    addBtnKey = self.createWidget(frameKey,"pwdItemBtn",self.getImgInfo("add"),pwdDataSuffix, "add")
                    editBtnKey = self.createWidget(frameKey,"pwdItemBtn",self.getImgInfo("edit"),pwdDataSuffix, "edit")
                    delBtnKey = self.createWidget(frameKey,"pwdItemBtn",self.getImgInfo("delete"),pwdDataSuffix, "del")
                    self.bindClickMethod(addBtnKey,self.loadAddDataDialog,groupKey=groupKey,envKey=envkey)
                    self.bindClickMethod(delBtnKey,self.loadDeleteDialog,
                            eventInfo={
                                "groupKey": groupKey,
                                "envKey": envkey,
                                "widget": dataFrameKey,
                                "id": pwdDataId,
                                "method": self.clickDeletePwdData,
                            })
                elif pwdKey == "website":
                    browerBtnKey = self.createWidget(frameKey,"pwdItemBtn",self.getImgInfo("browser"),pwdDataSuffix, "browser")
                    valueEntryKey = self.createWidget(frameKey,"pwdItemValue",None,pwdDataSuffix)

                    pwdItemValue = self.getWidget(valueEntryKey)
                    pwdItemValue.insert(tk.END, pwdValue)
                    pwdItemValue.config(state="readonly")
                    self.bindClickMethod(browerBtnKey,self.clickBrowser, pwdData=pwdData)
                else:
                    copyBtnKey = self.createWidget(frameKey,"pwdItemBtn",self.getImgInfo("copy"),pwdDataSuffix, "copy")
                    valueEntryKey = self.createWidget(frameKey,"pwdItemValue",None,pwdDataSuffix)

                    pwdItemValue = self.getWidget(valueEntryKey)
                    pwdItemValue.insert(tk.END, pwdValue)
                    pwdItemValue.config(state="readonly")
                    self.bindClickMethod(copyBtnKey,self.clickCopy,text=pwdValue,btnKey=copyBtnKey)

    def updatePwdPage(self) -> None:
        """更新当前页面"""
        self.updateCanvas(
            self.getWidget("pwdScrollCanvas"),
            self.getWidget("pwdContentFrame"),
            "pwdDispalyFrame",
        )

    def checkGroupEntry(self,btnKey:str,entryText:str)->bool:
        """检查组输入栏内容,False表示内容不符并做了处理，True表示内容满足约束不做处理"""
        if utils.isEmpty(entryText):
            self.cacheThread(
                self.replaceText, "pwdButton", ("不能为空",btnKey, "确定")
            )
            return False
        elif self.passwordBook.existGroup(entryText):
            self.cacheThread(
                self.replaceText, "pwdButton", ("组已存在",btnKey, "确定")
            )
            return False
        return True

    def checkEnvEntry(self,btnKey:str,groupKey:str,entryText:str)->bool:
        """检查Env输入栏内容,False表示内容不符并做了处理，True表示内容满足约束不做处理"""
        if utils.isEmpty(entryText):
            self.cacheThread(
                self.replaceText, "pwdButton", ("不能为空",btnKey, "确定")
            )
            return False
        elif self.passwordBook.existEnv(groupKey,entryText):
            self.cacheThread(
                self.replaceText, "pwdButton", ("ENV已存在",btnKey, "确定")
            )
            return False
        return True