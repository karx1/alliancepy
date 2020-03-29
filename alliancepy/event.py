from alliancepy.http import request
from alliancepy.season import Season


class Event:
    def __init__(self, event_key: str, headers: dict):
        self._event_key = event_key
        self._headers = headers
        info = request(f"/event/{self._event_key}", headers=self._headers)
        info = info[0]
        season_key = int(info["season_key"])
        self.season = Season(season_key).name
        self.region = info["region_key"]
        self.league = info["league_key"]
        self.name = info["event_name"]
        location = f"{info['city']} {info['state_prov']}, {info['country']}"
        self.location = location
