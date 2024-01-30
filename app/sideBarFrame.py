import tkinter as tk
from frame.baseFrame import BaseFrame
from control.event import Event, WmEvent
from control.controller import Controller

"""侧边栏"""
class SideBarFrame(BaseFrame):

    def __init__(self,controller:Controller) -> None:
        super().__init__(controller)


    def loadSideBarFrame(self,sideBarFrameKey:str)->None:
        """加载侧边栏"""
        sideBarFrame = self.getWidget(sideBarFrameKey)
        passwordBookBtn = tk.Label(
            sideBarFrame,text="密码本",cnf=self.getStyle().getCnf("passwordBookBtn")
        )
        self.cacheWidget(passwordBookBtn, sideBarFrameKey, "passwordBookBtn")