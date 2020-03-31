import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor
import sys

if sys.platform == "win32" and hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    _BasePolicy = asyncio.WindowsSelectorEventLoopPolicy
else:
    _BasePolicy = asyncio.DefaultEventLoopPolicy


class ThreadEventLoopPolicy(_BasePolicy):
    def get_event_loop(self):
        try:
            return super().get_event_loop()
        except (RuntimeError, AssertionError):
            loop = self.new_event_loop()
            self.set_event_loop(loop)
            return loop
