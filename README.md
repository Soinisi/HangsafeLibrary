# HangsafeLibrary
Robot Framework keyword library for implementing timeout for a keyword if it hangs. This is particularly useful in Windows which have no signal solution.
Library works by running keyword in seperate thread and raising a `TimeoutError` or `SystemExit` in the thread to stop it. 
There could be some unseen problems with this so use is at your own risk. *Caution* `SystemExit` option will break the Robot log file.

## Usage
```
With Timeout    Example Keyword    
With Timeout    Example Keyword With Arguments    *kw_args    timeout=30
With Timeout    Example Keyword    system_exit=True
```


License
----

MIT
