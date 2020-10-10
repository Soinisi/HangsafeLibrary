import pytest
from ..HangsafeLibrary import (with_timeout_decorator,
                               with_hang_detect_decorator)
import time





def test_with_timeout_decorator():
    with pytest.raises(TimeoutError):
        error_timeout_func('infiniteloop')
    
    assert success_timeout_func('success') == 'success'



def test_hang_detect_decorator():
    with pytest.raises(TimeoutError):
        error_hang_func('sleeploop')

    assert success_hang_func('success') == 'success'





#HELPERS-------------------------------------------------------
@with_timeout_decorator(timeout=0.1, system_exit=True)
def error_timeout_func(text):
    try: 
        while True: 
            print(text) 
    finally: 
        print('ended')



@with_timeout_decorator()
def success_timeout_func(text):
    return text



@with_hang_detect_decorator(max_secs_hung=0.1, system_exit=True)
def error_hang_func(text):
    print(text)
    time.sleep(5)
    print('ended')



@with_hang_detect_decorator(interval=0.1)
def success_hang_func(text):
    return text    