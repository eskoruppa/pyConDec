#!/bin/env python3

from functools import wraps


def conditional_decorator(decorator, condition, *dec_args, **dec_kwargs):
    """
    A decorator factory that conditionally applies an arbitrary decorator.

    If *condition* is truthy the supplied *decorator* is applied to the
    function; otherwise the original function is returned unchanged.

    Two calling conventions are supported:

    **Pre-configured decorator** (no extra arguments)
        Pass a decorator that already accepts a function directly::

            cond_dec(lru_cache(maxsize=128), condition)

    **Decorator factory with arguments** (extra positional/keyword args)
        Pass the factory followed by its arguments; the factory is called
        with those arguments first, and the result is applied to the
        function::

            cond_dec(lru_cache, condition, maxsize=128)
            # equivalent to: lru_cache(maxsize=128)(func)

    Parameters
    ----------
    decorator : callable
        Either a fully configured decorator (accepts a function, returns a
        function) or a decorator factory when *dec_args* / *dec_kwargs* are
        provided.
    condition : bool
        When truthy the decorator is applied; when falsy the function is
        returned as-is.
    *dec_args
        Positional arguments forwarded to *decorator* when it is used as a
        factory.
    **dec_kwargs
        Keyword arguments forwarded to *decorator* when it is used as a
        factory.

    Returns
    -------
    callable
        A decorator that conditionally wraps the target function.
    """
    def wrapper(func):
        if not condition:
            return func
        # If extra arguments were provided, treat decorator as a factory.
        if dec_args or dec_kwargs:
            configured = decorator(*dec_args, **dec_kwargs)
        else:
            configured = decorator
        decorated = configured(func)
        # Preserve the original function's metadata when the decorator
        # does not already do so (best-effort).
        if decorated is not func:
            try:
                wraps(func)(decorated)
            except (TypeError, AttributeError):
                pass
        return decorated
    return wrapper
