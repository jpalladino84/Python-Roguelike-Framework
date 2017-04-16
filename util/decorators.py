import itertools
import logging


logger = logging.getLogger()


def cached(func):
    def wrapper(*args, **kwargs):
        host = args[0]
        if not hasattr(host, 'cache'):
            setattr(host, 'cache', {})

        if func not in host.cache:
            logger.debug("Setting new cache for function {}".format(func))
            host.cache[func] = func(*args, **kwargs)
        else:
            logger.debug("Retrieving from cache for function {}".format(func))

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
            logger.debug("Setting new argument cache for function {}".format(func))
            host.cache[func][cached_args] = func(*args, **kwargs)
        else:
            logger.debug("Retrieving from cache for function {}".format(func))

        return host.cache[func]

    return wrapper


def invalidate_cache(func):
    def wrapper(*args, **kwargs):
        host = args[0]
        if hasattr(host, 'cache'):
            logger.debug("Invalidating cache for {}".format(func))
            host.cache = {}
        return func(*args, **kwargs)

    return wrapper
