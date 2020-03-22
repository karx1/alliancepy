import requests
import json


def request(target: str, headers: dict):
    url = f"https://theorangealliance.org/api{target}"
    resp = requests.get(url, headers=headers)
    data = json.loads(resp.text)
    return data
