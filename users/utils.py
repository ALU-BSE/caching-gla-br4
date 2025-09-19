def get_cache_key(user_id):
    """
    Returns a cache key string for a given user ID.
    """
    return f"user_cache_{user_id}"