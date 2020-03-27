import aiohttp
import json


async def request(target: str, headers: dict):
    async with aiohttp.ClientSession(headers=headers) as session:
        url = f"https://theorangealliance.org/api{target}"
        async with session.get(url) as resp:
            data = json.loads(await resp.text())
            if resp.status != 200:
                raise WebException(data["_message"])

    return data


class WebException(Exception):
    pass
