import ctypes
import inspect
import _thread as thread
import threading
from robot.libraries.BuiltIn import BuiltIn
import time


class HangsafeLibrary:

    def with_timeout(self, kw, *args, timeout: float = 10, system_exit: bool = False):
        kw_tuple = (kw, *args)
        kw_thread = ThreadWithException(BuiltIn().run_keyword, *kw_tuple)
        kw_thread.name = 'kw running thread'
        kw_thread.start()
        kw_thread.join(timeout)
        
        if kw_thread.is_alive():
            exc = TimeoutError if not system_exit else SystemExit
            
            kw_thread.raise_exception(exc)
            #time for the main thread running robot to recover from thread exception
            time.sleep(5)
            raise TimeoutError('Keyword timeout exceeded!')
        
        return kw_thread.return_val



class ThreadWithException(threading.Thread):
    
    def __init__(self, func, *args):
        super().__init__()
        self.func = func
        self.args = args
        self.return_val = None



    def run(self):
        self.return_val = self.func(*self.args)
        

    
    def _get_own_tid(self):
        if not self.is_alive():
            raise threading.ThreadError("Thread is not active")
        
        if hasattr(self, "_thread_id"):
            return self._thread_id
        
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid
        
        raise AssertionError("Thread id not found!")
    

    def _async_raise(self, tid, exception_type):
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exception_type))
        if res == 0:
            raise ValueError("Invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
            raise SystemError("PyThreadState_SetAsyncExc failed")



    def raise_exception(self, exception_type):
        self._async_raise(self._get_own_tid(), exception_type)
    




