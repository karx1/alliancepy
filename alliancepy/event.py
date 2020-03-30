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

    def _rankings(self):
        resp = request(f"/events/{self._event_key}/rankings", headers=self._headers)
        return resp

    def rank(self, team_number: int):
        rankings = self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["rank"]
                return int(raw)

    def rank_change(self, team_number: int):
        rankings = self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["rank_change"]
                return int(raw)

    def wins(self, team_number: int):
        rankings = self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["wins"]
                return int(raw)

    def losses(self, team_number: int):
        rankings = self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["losses"]
                return int(raw)

    def ties(self, team_number: int):
        rankings = self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["losses"]
                return int(raw)

    def opr(self, team_number: int):
        rankings = self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["opr"]
                return float(raw)

    def np_opr(self, team_number: int):
        rankings = self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["np_opr"]
                return float(raw)

    def highest_qualifier_score(self, team_number):
        rankings = self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["highest_qual_score"]
                return int(raw)

    def ranking_points(self, team_number: int):
        rankings = self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["ranking_points"]
                return float(raw)

    def qualifying_points(self, team_number: int):
        rankings = self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["qualifying_points"]
                return int(raw)

    def tiebreaker_points(self, team_number: int):
        rankings = self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["tie_breaker_points"]
                return float(raw)
