import tkinter as tk

class ImageController:

    def __init__(self) -> None:
        """资源缓存"""
        self.imagePool = {}

    def cacheImage(self,image:tk.PhotoImage,key:str,group:str):
        """缓存图片"""
        if group not in self.imagePool:
            self.imagePool[group] = {}
        if key not in self.imagePool[group]:
            self.imagePool[group][key] = image

    def isInImagePool(self,key:str,group:str):
        """是否存在该缓存"""
        if group in self.imagePool:
            return key in self.imagePool[group]
        return False

    def getImage(self,key:str,group:str)->tk.PhotoImage:
        """获取缓存的图片"""
        return self.imagePool[group][key]

    def clearImage(self,group:str):
        """清理图片"""
        if group in self.imagePool:
            self.imagePool[group]={}
            self.imagePool.pop(group)