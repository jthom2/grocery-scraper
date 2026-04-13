import time


class TTLCache:
    """A simple time-based cache for storing values with a fixed TTL."""
    def __init__(self, ttl_seconds):
        self.ttl = ttl_seconds
        self.cache = {}

    def get(self, key):
        """Returns the value if it exists and hasn't expired, else None."""
        if key in self.cache:
            entry = self.cache[key]
            if entry['expires_at'] > time.time():
                return entry['value']
            del self.cache[key]
        return None

    def set(self, key, value):
        """Sets a value with the configured TTL."""
        self.cache[key] = {
            'value': value,
            'expires_at': time.time() + self.ttl
        }

    def clear(self):
        """Clears all entries from the cache."""
        self.cache.clear()

