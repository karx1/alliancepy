import requests
import re
import json


def request(target: str, headers: dict):
    url = f"https://theorangealliance.org/api{target}"
    resp = requests.get(url, headers=headers)
    txt = re.sub(r"[\[\]]", "", resp.text)
    dec = json.JSONDecoder()
    jlist = []
    while True:
        try:
            j, n = dec.raw_decode(txt)
            jlist.append(j)
        except ValueError:
            break
        txt = txt[n:]

    return jlist
