class WmEvent:
    WindowClose = "WM_DELETE_WINDOW" #窗口关闭


class Event:
    MouseLeftClick = "<Button-1>" #鼠标左键
    MouseWheel = "<MouseWheel>"  # 滚轮滚动
    MouseRelease = "<ButtonRelease-1>" #鼠标左键释放

    WindowResize = "<Configure>" #窗口变化

def eventAdaptor(fun, **kwds):
    """
    fun:当前要绑定的方法
    kwds:要传入的额外参数，需带参数名(eg. sudoku=sudoku)
    """
    return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)