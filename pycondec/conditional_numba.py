#!/bin/env python3

try:
    from numba import jit
except ImportError:
    jit = None
    
try:
    from numba.experimental import jitclass
except ImportError:
    jitclass = None

def conditional_numba(*jit_args, **jit_kwargs):
    """
    A decorator factory that conditionally applies numba.jit with the
    given arguments. If numba is not installed, it returns the original
    function unchanged.
    
    Usage:
        @conditional_numba(nopython=True, cache=True)
        def f(...):
            ...

        @conditional_numba
        def g(...):
            ...
    """
    def decorator(func):
        if jit is None:
            return func
        return jit(*jit_args, **jit_kwargs)(func)
    return decorator
    
def conditional_jitclass(*jit_args, **jit_kwargs):
    def wrapper(cls):
        if jitclass is None:
            return cls
        return jitclass(*jit_args, **jit_kwargs)(cls)
    return wrapper