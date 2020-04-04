import aiohttp
import json


async def request(target: str, headers: dict):
    async with aiohttp.ClientSession(headers=headers) as session:
        url = f"https://theorangealliance.org/api{target}"
        async with session.get(url) as resp:
            if resp.status != 200:
                try:
                    data = json.loads(await resp.text())
                except json.decoder.JSONDecodeError:
                    raise WebException(await resp.text())
                else:
                    raise WebException(data["_message"])
            data = json.loads(await resp.text())

    return data


class WebException(Exception):
    pass
