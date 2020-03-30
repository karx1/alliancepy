from .async_http import request
from alliancepy.season import Season
import asyncio


class Event:
    def __init__(self, event_key: str, headers: dict):
        self._event_key = event_key
        self._headers = headers
        self._loop = asyncio.get_event_loop()
        info = self._loop.run_until_complete(request(f"/event/{self._event_key}", headers=self._headers))
        info = info[0]
        season_key = int(info["season_key"])
        self.season = Season(season_key).name
        self.region = info["region_key"]
        self.league = info["league_key"]
        self.name = info["event_name"]
        location = f"{info['city']} {info['state_prov']}, {info['country']}"
        self.location = location
        self.venue = info["venue"]

    def __str__(self):
        return f"<Event: {self.name}>"

    def __repr__(self):
        return f"<Event: {self.name} ({self._event_key})>"

    async def _rankings(self):
        resp = await request(f"/events/{self._event_key}/rankings", headers=self._headers)
        return resp

    async def rank(self, team_number: int):
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["rank"]
                return int(raw)

    async def rank_change(self, team_number: int):
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["rank_change"]
                return int(raw)

    async def wins(self, team_number: int):
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["wins"]
                return int(raw)

    async def losses(self, team_number: int):
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["losses"]
                return int(raw)

    async def ties(self, team_number: int):
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["ties"]
                return int(raw)

    async def opr(self, team_number: int):
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["opr"]
                return int(raw)

    async def np_opr(self, team_number: int):
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["np_opr"]
                return int(raw)

    async def highest_qualifier_score(self, team_number: int):
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["highest_qual_score"]
                return int(raw)

    async def ranking_points(self, team_number: int):
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["ranking_points"]
                return int(raw)

    async def qualifying_points(self, team_number: int):
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["qualifying_points"]
                return int(raw)

    async def tiebreaker_points(self, team_number: int):
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["tie_breaker_points"]
                return int(raw)
