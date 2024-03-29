import os
import json


def isEmpty(value: str) -> bool:
    """判断字符串是否为空"""
    return value == None or value == "" or value == []


def isPhoto(fileName: str) -> bool:
    """判断当前文件为图片"""
    return (
        fileName.endswith(".png")
        or fileName.endswith(".PNG")
        or fileName.endswith(".jpg")
    )


def getFileName(file: str) -> str:
    """去掉文件后缀，获取文件名"""
    return file.split(".")[0]


def loadJsonByFile(filePath: str) -> None:
    """从文件中读取数据,基于项目根目录"""
    jsonData = None
    if filePath == None:
        raise Exception("文件路径不能为空")
    file = os.path.join(os.getcwd(), filePath)
    if os.path.exists(file):
        with open(file, encoding="utf-8") as f:
            jsonData = json.load(f)
    else:
        raise Exception("文件 %s 不存在" % file)
    if jsonData == None:
        raise Exception("文件 %s 没有数据" % file)
    return jsonData


def writeToJsonFile(filePath: str, data: any) -> None:
    """将当前数据写到文件"""
    if filePath == None:
        raise Exception("文件路径不能为空")
    if data == None:
        raise Exception("数据不能为空")
    file = os.path.join(os.getcwd(), filePath)
    if os.path.exists(file):
        with open(file, encoding="utf-8", mode="w") as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))
    else:
        raise Exception("文件 %s 不存在" % file)
