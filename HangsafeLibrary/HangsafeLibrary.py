import ctypes
import inspect
import _thread as thread
import threading
from robot.libraries.BuiltIn import BuiltIn
import time
import sys
import functools


class HangsafeLibrary:

    def with_timeout(self, kw, *args, timeout: float = 10, system_exit: bool = False):
        kw_tuple = (kw, *args)
        kw_thread = ThreadWithException(BuiltIn().run_keyword, *kw_tuple)
        kw_thread.name = 'kw running thread'
        kw_thread.daemon = True
        kw_thread.start()
        kw_thread.join(timeout)
        
        if kw_thread.is_alive():
            exc = TimeoutError if not system_exit else SystemExit
            
            kw_thread.raise_exception(exc)
            #time for the main thread running robot to recover from thread exception
            time.sleep(5)
            raise TimeoutError('Keyword timeout exceeded!')
        
        return kw_thread.return_val



    def with_hang_detect(self, 
                         kw, 
                         *args, 
                         max_secs_hung: float = 15, 
                         interval: float = 1, 
                         system_exit: bool = False):
        
        exc = TimeoutError if not system_exit else SystemExit
        kw_tuple = (kw, *args)
        kw_thread = ThreadWithException(BuiltIn().run_keyword, *kw_tuple)
        kw_thread.name = 'kw running thread'
        kw_thread.daemon = True
        kw_thread.start()
        kw_thread.join(1)

        first_frame = kw_thread.get_own_current_frame()
        first_time = time.time()
        _loop_frame_hang_check(kw_thread, 
                               exc, 
                               max_secs_hung, 
                               interval, 
                               first_frame, 
                               first_time)

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
    


    def get_own_current_frame(self):
        try:
            tid = self._get_own_tid()
            return sys._current_frames()[int(tid)]
        except threading.ThreadError:
            return None


    def _async_raise(self, tid, exception_type):
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exception_type))
        if res == 0:
            raise ValueError("Invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
            raise SystemError("PyThreadState_SetAsyncExc failed")



    def raise_exception(self, exception_type):
        self._async_raise(self._get_own_tid(), exception_type)
    



def with_timeout_decorator(timeout: float = 10, system_exit: bool = False):
    def inner_deco(func):
        @functools.wraps(func)
        def wrapper(*args):
            kw_thread = ThreadWithException(func, *args)
            kw_thread.name = 'kw func running thread'
            kw_thread.daemon = True
            kw_thread.start()
            kw_thread.join(timeout)
            
            if kw_thread.is_alive():
                exc = TimeoutError if not system_exit else SystemExit
                
                kw_thread.raise_exception(exc)
                #time for the main thread running robot to recover from thread exception
                time.sleep(5)
                raise TimeoutError('Keyword timeout exceeded!')
            
            return kw_thread.return_val
        return wrapper
    return inner_deco



def with_hang_detect_decorator(max_secs_hung: float = 15, interval: float = 1, system_exit: bool = False):
    def inner_deco(func):
        @functools.wraps(func)
        def wrapper(*args):
            exc = TimeoutError if not system_exit else SystemExit
            kw_thread = ThreadWithException(func, *args)
            kw_thread.name = 'kw func running thread'
            kw_thread.daemon = True
            kw_thread.start()
            kw_thread.join(1)

            first_frame = kw_thread.get_own_current_frame()
            first_time = time.time()
            _loop_frame_hang_check(kw_thread, 
                                   exc, 
                                   max_secs_hung, 
                                   interval, 
                                   first_frame, 
                                   first_time)

            return kw_thread.return_val
        return wrapper
    return inner_deco
        



#HELPERS------------------------------------------------------------------------------
def _loop_frame_hang_check(kw_thread, exc, max_secs_hung, interval, first_frame, first_time):
    while kw_thread.is_alive():
        time.sleep(interval)
        
        second_frame = kw_thread.get_own_current_frame()
        if not second_frame: break
        second_time = time.time()
        
        if first_frame == second_frame:
            if (second_time - first_time) > max_secs_hung:
                kw_thread.raise_exception(exc)
                time.sleep(5)
                raise TimeoutError('Keyword hung time exceeded!')       
        else:
            first_frame = second_frame
            first_time = second_time 

