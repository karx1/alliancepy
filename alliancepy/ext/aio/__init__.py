try:
    import aiohttp
except ImportError:
    raise ImportError("Package is not configured for async use. Please install with async support enabled.")

from .async_client import AsyncClient
