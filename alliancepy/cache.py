cache = {}


class Cache:
    def __init__(self):
        self._cache = cache

    def keys(self):
        return self._cache.keys()

    def add(self, key, value):
        self._cache[key] = value

    def get(self, key):
        return self._cache[key]

    def remove(self, key):
        self._cache.pop(key, None)

    def clear(self):
        map(self.remove, self._cache.keys())
