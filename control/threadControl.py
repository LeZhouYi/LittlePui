import threading
import inspect
import ctypes
import threading

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you"re in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def stopThread(thread:threading.Thread):
    """停止线程"""
    if thread!=None and thread.is_alive():
        _async_raise(thread.ident, SystemExit)

"""
管理渲染线程
"""
class ThreadController:

    def __init__(self) -> None:
        self.threadPool = {} #线程池

    def cacheThread(self,thread:threading.Thread,key:str)->None:
        """缓存线程池并开始运行"""
        if key==None:
            thread.start()
            return
        if key in self.threadPool:
            threadNow = self.threadPool[key]
            if threadNow.is_alive():
                stopThread(threadNow)
        self.threadPool[key]=thread
        thread.start()