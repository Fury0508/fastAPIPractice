import time
_cache: dict[str, dict] = {}

def get_cache(key: str) -> dict | None:
    """Retrieve a cached value by key."""
    if key not in _cache:
        return None
    entry = _cache[key]
    if time.time()  - entry["timestamp"] > entry["ttl"]:
        del _cache[key]
        return None
    return entry["data"]

def set_cache(key: str, data: dict, ttl: int = 3600) -> None:
    """Store a value in the cache with a time-to-live (TTL)."""
    _cache[key] = {
        "data": data,
        "timestamp": time.time(),
        "ttl": ttl
    }

def clear_cache() -> None:
    """Clear the entire cache."""
    _cache.clear()