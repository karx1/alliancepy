import requests
import json


def request(target: str, headers: dict):
    with requests.Session() as session:
        session.headers.update(headers)
        url = f"https://theorangealliance.org/api{target}"
        with session.get(url) as resp:
            data = json.loads(resp.text)
            if resp.status_code != 200:
                raise WebException(data["_message"])

    return data


class WebException(Exception):
    pass
