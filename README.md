# HangsafeLibrary
Robot Framework keyword library for implementing timeout for a keyword if it hangs. This is particularly useful in Windows which have no signal solution.
Library works by running keyword in seperate thread and raising a `TimeoutError` or `SystemExit` in the thread to stop it. 
There could be some unseen problems with this so use is at your own risk. *Caution* `SystemExit` option will break the Robot output.xml file.
In general the output.xml can break in some circumstances anyway.

## Usage
```
With Timeout    Example Keyword    
With Timeout    Example Keyword With Arguments    *kw_args    timeout=30
With Timeout    Example Keyword    system_exit=True
${return value}=    With Timeout    Example Keyword With Return Value
```

Same with `With Hang Detect`:
```
With Hang Detect    Example Keyword
With Hang Detect    Example Keyword With Arguments    *kw_args    max_secs_hung=10    interval=2    system_exit=True

```
When running Python code directly inside Robot Framework you can use `decorator` versions. They have the same arguments as the keyword versions. Because the decorators are based on the keywords, they can only pass `*args` and not `**kwargs` as Robot Framework does.
```python
@with_timeout_decorator(timeout=0.1, system_exit=True)
def example_function(arg1, arg2):
    return arg1, arg2

@with_hang_detect_decorator(interval=0.1)
def example_function(arg1, arg2):
    return arg1, arg2
```
etc.


License
----

MIT
