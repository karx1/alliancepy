import requests
import json


def request(target: str, headers: dict):
    url = f"https://theorangealliance.org/api{target}"
    resp = requests.get(url, headers=headers)
    data = json.loads(resp.text)
    if resp.status_code != 200:
        raise WebException(data["_message"])
    return data


class WebException(Exception):
    pass
