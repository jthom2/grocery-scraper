import time


# simple time-based cache with fixed ttl
class TTLCache:
    def __init__(self, ttl_seconds):
        self.ttl = ttl_seconds
        self.cache = {}

    # returns value if exists and not expired
    def get(self, key):
        if key in self.cache:
            entry = self.cache[key]
            if entry['expires_at'] > time.time():
                return entry['value']
            del self.cache[key]
        return None

    # sets value with configured ttl
    def set(self, key, value):
        self.cache[key] = {
            'value': value,
            'expires_at': time.time() + self.ttl
        }

    # clears all cache entries
    def clear(self):
        self.cache.clear()
