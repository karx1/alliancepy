from .async_http import request
from alliancepy.season import Season
import asyncio
import nest_asyncio


class Team:
    def __init__(self, team_number, headers: dict):
        self._team_number = team_number
        self._headers = headers
        self._loop = asyncio.get_event_loop()
        nest_asyncio.apply(self._loop)
        team = self._loop.run_until_complete(request(target=f"/team/{team_number}", headers=headers))
        team = team[0]
        self.region = team["region_key"]
        self.league = team["league_key"]
        self.short_name = team["team_name_short"]
        self.long_name = team["team_name_long"]
        self.robot_name = team["robot_name"]
        location = f"{team['city']}, {team['state_prov']}, {team['country']}, {team['zip_code']}"
        self.location = location
        self.rookie_year = team["rookie_year"]
        self.last_active = team["last_active"]
        self.website = team["website"]

    async def _wlt(self):
        data = await request(target=f"/team/{self._team_number}/wlt", headers=self._headers)
        self._wins = data[0]["wins"]
        self._losses = data[0]["losses"]
        self._ties = data[0]["ties"]

    @property
    def wins(self):
        self._loop.run_until_complete(self._wlt())
        return self._wins

    @property
    def losses(self):
        self._loop.run_until_complete(self._wlt())
        return self._losses

    @property
    def ties(self):
        self._loop.run_until_complete(self._wlt())
        return self._ties

    async def _rankings(self, season: Season):
        rankings = await request(f"/team/{self._team_number}/results/{season}", headers=self._headers)
        return rankings

    async def season_wins(self, season: Season):
        data = await self._rankings(season)
        x = []
        for item in data:
            raw = item["wins"]
            x.append(int(raw))

        return sum(x)

    async def season_losses(self, season: Season):
        data = await self._rankings(season)
        x = []
        for item in data:
            raw = item["losses"]
            x.append(int(raw))

        return sum(x)

    async def season_ties(self, season: Season):
        data = await self._rankings(season)
        x = []
        for item in data:
            raw = item["ties"]
            x.append(int(raw))

        return sum(x)

    async def opr(self, season: Season):
        data = await self._rankings(season)
        x = []
        for item in data:
            raw = item["opr"]
            x.append(int(raw))

        return sum(x)

    async def np_opr(self, season: Season):
        data = await self._rankings(season)
        x = []
        for item in data:
            raw = item["np_opr"]
            x.append(int(raw))

        return sum(x)

    async def tiebreaker_points(self, season: Season):
        data = await self._rankings(season)
        x = []
        for item in data:
            raw = item["tie_breaker_points"]
            x.append(int(raw))

        return sum(x)

    async def ranking_points(self, season: Season):
        data = await self._rankings(season)
        x = []
        for item in data:
            raw = item["ranking_points"]
            x.append(int(raw))

        return sum(x)

    async def qualifying_points(self, season: Season):
        data = await self._rankings(season)
        x = []
        for item in data:
            raw = item["qualifying_points"]
            x.append(int(raw))

        return sum(x)
