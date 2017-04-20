import itertools


def cached(func):
    def wrapper(*args, **kwargs):
        host = args[0]
        if not hasattr(host, 'cache'):
            setattr(host, 'cache', {})

        if func not in host.cache:
            host.cache[func] = func(*args, **kwargs)

        return host.cache[func]

    return wrapper


def cached_with_args(func):
    def wrapper(*args, **kwargs):
        host = args[0]
        if not hasattr(host, 'cache'):
            setattr(host, 'cache', {})

        if func not in host.cache:
            host.cache[func] = {}

        cached_args = tuple(itertools.chain(args, kwargs.values()))
        if cached_args not in host.cache[func]:
            host.cache[func][cached_args] = func(*args, **kwargs)

        return host.cache[func]

    return wrapper


def invalidate_cache(func):
    def wrapper(*args, **kwargs):
        host = args[0]
        if hasattr(host, 'cache'):
            host.cache = {}
        return func(*args, **kwargs)

    return wrapper
