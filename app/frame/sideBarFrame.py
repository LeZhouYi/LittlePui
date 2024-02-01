import tkinter as tk
from core.frame.baseFrame import BaseFrame
from core.control.controller import Controller

"""侧边栏"""
class SideBarFrame(BaseFrame):

    def __init__(self,controller:Controller) -> None:
        super().__init__(controller)


    def loadSideBarFrame(self,sideBarFrameKey:str)->None:
        """加载侧边栏"""
        self.createWidget(sideBarFrameKey,"sideBarBtn",{"text":"密码本"},"pwdBook")