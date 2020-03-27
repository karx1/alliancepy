from .async_http import request
from alliancepy.season import Season
import asyncio
import nest_asyncio


class Team:
    """
    This is the Asynchronous version of the normal :class:`~alliancepy.team.Team` class. You should not create your own
    instances of this class - instead use your :class:`~.async_client.AsyncClient` object.

    region
        The key of the team's according region.
    league
        The key of the team's league.
    short_name
        The short team name.
    long_name
        The long team name.
    robot_name
        The name of the team's robot.
    location
        The team's location, in "City, State/Province, Country, Zipcode" format.
    rookie_year
        The year in which the team was a rookie team.
    last_active
        The season key of the season in which the team participated in their most recent match.
    website
        The URL of the team's website, if they have any

    """
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
        """
        The total amount of times the team has won a match.

        :return: The number of wins.
        :rtype: int
        """
        self._loop.run_until_complete(self._wlt())
        return self._wins

    @property
    def losses(self):
        """
        The total amount of times the team has lost a match.

        :return: The number of wins.
        :rtype: int
        """
        self._loop.run_until_complete(self._wlt())
        return self._losses

    @property
    def ties(self):
        """
        The total amount of times the team has tied in a match.

        :return: The number of wins.
        :rtype: int
        """
        self._loop.run_until_complete(self._wlt())
        return self._ties

    async def _rankings(self, season: Season):
        rankings = await request(f"/team/{self._team_number}/results/{season}", headers=self._headers)
        return rankings

    async def season_wins(self, season: Season):
        """
        The amount of times a team has won a match in a particular season.

        :param season: A valid TOA season key
        :type season: :class:`~alliancepy.season.Season`
        :return: The number of wins in the specified season
        :rtype: int
        """
        data = await self._rankings(season)
        x = []
        for item in data:
            raw = item["wins"]
            x.append(int(raw))

        return sum(x)

    async def season_losses(self, season: Season):
        """
        The amount of times a team has lost a match in a particular season.

        :param season: A valid TOA season key
        :type season: :class:`~alliancepy.season.Season`
        :return: The number of wins in the specified season
        :rtype: int
        """
        data = await self._rankings(season)
        x = []
        for item in data:
            raw = item["losses"]
            x.append(int(raw))

        return sum(x)

    async def season_ties(self, season: Season):
        """
        The amount of times a team has tied in a match in a particular season.

        :param season: A valid TOA season key
        :type season: :class:`~alliancepy.season.Season`
        :return: The number of wins in the specified season
        :rtype: int
        """
        data = await self._rankings(season)
        x = []
        for item in data:
            raw = item["ties"]
            x.append(int(raw))

        return sum(x)

    async def opr(self, season: Season):
        """
        OPR stands for Offensive Power Rating, which is a system to attempt to deduce the average point contribution of
        a team to an alliance. Penalties are also factored in.

        :param season: A valid TOA season key
        :type season: :class:`~alliancepy.season.Season`
        :return: The number of wins in the specified season
        :rtype: int
        """
        data = await self._rankings(season)
        x = []
        for item in data:
            raw = item["opr"]
            x.append(int(raw))

        return sum(x)

    async def np_opr(self, season: Season):
        """
        NP_OPR is just OPR, but penalties are not factored in.

        :param season: A valid TOA season key
        :type season: :class:`~alliancepy.season.Season`
        :return: The number of wins in the specified season
        :rtype: int
        """
        data = await self._rankings(season)
        x = []
        for item in data:
            raw = item["np_opr"]
            x.append(int(raw))

        return sum(x)

    async def tiebreaker_points(self, season: Season):
        """
        Tiebreaker points are the pre-penalty score of the losing alliance for each match. This function returns the
        total tiebreaker points of a team in one season.

        :param season: A valid TOA season key
        :type season: :class:`~alliancepy.season.Season`
        :return: The number of wins in the specified season
        :rtype: int
        """
        data = await self._rankings(season)
        x = []
        for item in data:
            raw = item["tie_breaker_points"]
            x.append(int(raw))

        return sum(x)

    async def ranking_points(self, season: Season):
        """
        Ranking points are the number of points scored by the losing alliance in a qualification match.
        If you win the match, then the RP awarded to you is the score of your opponent alliance (which lost).
        If you lose the match, then the RP awarded to you is your own alliance’s score.

        :param season: A valid TOA season key
        :type season: :class:`~alliancepy.season.Season`
        :return: The number of wins in the specified season
        :rtype: int
        """
        data = await self._rankings(season)
        x = []
        for item in data:
            raw = item["ranking_points"]
            x.append(int(raw))

        return sum(x)

    async def qualifying_points(self, season: Season):
        """
        Winning teams of a qualifying match eatch receive 2 QP. Losing teams receive 0. If a match ends in a tie, all
        four teams receive 1 QP.

        :param season: A valid TOA season key
        :type season: :class:`~alliancepy.season.Season`
        :return: The number of wins in the specified season
        :rtype: int
        """
        data = await self._rankings(season)
        x = []
        for item in data:
            raw = item["qualifying_points"]
            x.append(int(raw))

        return sum(x)
