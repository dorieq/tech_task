from django.core.cache import cache

CACHE_TRACKER_KEY = "tasks_cache_keys"

def add_cache_key(key):
    """
    Track cache keys by storing them in a list within the cache.
    """
    keys = cache.get(CACHE_TRACKER_KEY, set())
    keys.add(key)
    cache.set(CACHE_TRACKER_KEY, keys, timeout=None)  # Store indefinitely until cleared

def invalidate_task_cache():
    """
    Invalidate all cached task-related keys by iterating over the tracked keys.
    """
    keys = cache.get(CACHE_TRACKER_KEY, set())
    for key in keys:
        cache.delete(key)
    cache.delete(CACHE_TRACKER_KEY)  # Clear the tracker itself
