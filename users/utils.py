import functools
import time
import logging
from django.core.cache import cache
from .models import User  # Import the User model

def get_cache_key(prefix, identifier=None):
    """Generate consistent cache keys"""
    if identifier:
        return f"{prefix}_{identifier}"
    return prefix

logger = logging.getLogger(__name__)

def cache_performance(cache_name):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            logger.info(f"{cache_name}: {end_time - start_time:.4f}s")
            return result
        return wrapper
    return decorator

@cache_performance("br4_key")
def list(self, request, *args, **kwargs):
    users = cache.get('br4_key')
    if users is None:
        users = list(User.objects.all())
        cache.set('br4_key', users, 300)
    pass

def cache_with_tags(key, data, tags, timeout=300):
    cache.set(key, data, timeout)
    for tag in tags:
        tagged_keys = cache.get(f'tag_{tag}', set())
        tagged_keys.add(key)
        cache.set(f'tag_{tag}', tagged_keys, timeout)

def invalidate_by_tag(tag):
    tagged_keys = cache.get(f'tag_{tag}', set())
    for key in tagged_keys:
        cache.delete(key)
    cache.delete(f'tag_{tag}')
