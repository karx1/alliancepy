import requests
import json


def request(target: str, headers: dict):
    with requests.Session() as session:
        session.headers.update(headers)
        url = f"https://theorangealliance.org/api{target}"
        with session.get(url) as resp:
            if resp.status_code != 200:
                try:
                    data = json.loads(resp.text)
                except json.decoder.JSONDecodeError:
                    raise WebException(resp.text)
                else:
                    raise WebException(data["_message"])
            data = json.loads(resp.text)

    return data


class WebException(Exception):
    pass
