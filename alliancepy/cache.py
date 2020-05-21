import pickle


class Cache:
    def __init__(self):
        self._filename = "alliancepy.txt"
        self._cache = {}

    def __enter__(self):
        try:
            with open(self._filename, "rb") as file:
                d = pickle.load(file)
                for key, value in d.items():
                    self._cache[key] = value
        except (FileNotFoundError, EOFError):
            self._cache = {}
        finally:
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        with open(self._filename, "wb+") as file:
            d = {}
            for key, value in self._cache.items():
                d[key] = value
            pickle.dump(d, file)

    def keys(self):
        return self._cache.keys()

    def add(self, key, value):
        self._cache[key] = value

    def get(self, key):
        return self._cache[key]

    def remove(self, key):
        self._cache.pop(key, None)

    def clear(self):
        map(self.remove, self.keys())
