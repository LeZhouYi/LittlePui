import os
import json

def createKey(key:str,*args)->str:
    """创建Key"""
    for value in args:
        key=key+"_"+str(value)
    return key

def isEmpty(value:str)->bool:
    """判断字符串是否为空"""
    return value==None or value=="" or value==[]

def isPhoto(fileName:str)->bool:
    """判断当前文件为图片"""
    return fileName.endswith(".png") or fileName.endswith(".PNG") or fileName.endswith(".jpg")

def getFileName(file:str)->str:
    """去掉文件后缀，获取文件名"""
    return file.split(".")[0]

def eventAdaptor(fun, **kwds):
    """
    fun:当前要绑定的方法
    kwds:要传入的额外参数，需带参数名(eg. sudoku=sudoku)
    """
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

def loadJsonByFile(filePath) -> None:
    """从文件中读取数据,基于"""
    jsonData = None
    file = os.path.join(os.getcwd(), filePath)
    if os.path.exists(file):
        with open(file, encoding="utf-8") as f:
            jsonData = json.load(f)
    else:
        raise Exception("文件 %s 不存在"%file)
    if jsonData == None:
        raise Exception("文件 %s 没有数据"%file)
    return jsonData