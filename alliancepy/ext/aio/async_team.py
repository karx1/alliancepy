from .async_http import request
from .async_event import Event
from alliancepy.season import Season
import asyncio
from concurrent.futures import ThreadPoolExecutor
import re
import logging

# MIT License
#
# Copyright (c) 2020 Yash Karandikar
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

logger = logging.getLogger(__name__)


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
        team = self._loop.run_until_complete(
            request(target=f"/team/{team_number}", headers=headers)
        )
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
        logger.info(
            f"Initialized asynchronous 'Team' object with team number of {self._team_number}"
        )

    async def events(self, season: Season):
        """
        Every event the team has participated in, in a particular season.

        Args:
            season (:class:`~alliancepy.season.Season`): An alliancepy Season object
        Returns:
            dict: A dict containing the :class:`~alliancepy.event.Event` objects. The key names correspont to the name \
            of the event.
        """
        edict = {}
        events = await request(
            f"/team/{self._team_number}/events/{season}", headers=self._headers
        )

        def _parse_events(ev=events, ed=None):
            ed = ed or edict
            for event in ev:
                e = Event(event_key=event["event_key"], headers=self._headers)
                event_key = event["event_key"]
                raw_key = str(e.name)
                key = raw_key.replace(" ", "_")
                key = key.lower()
                if key in ed:
                    raw_key_right = re.sub(r"\d{4}-\w+-", "", event_key)
                    raw_key_right = raw_key_right.lower()
                    key = f"{key}_{raw_key_right}"
                ed[key] = e

            return ed

        loop = asyncio.get_event_loop_policy().new_event_loop()
        future = loop.run_in_executor(ThreadPoolExecutor(), _parse_events)
        return loop.run_until_complete(future)

    async def _wlt(self):
        logger.info("Fetching WLT data")
        data = await request(
            target=f"/team/{self._team_number}/wlt", headers=self._headers
        )
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
        logger.info("Getting ranking data")
        rankings = await request(
            f"/team/{self._team_number}/results/{season}", headers=self._headers
        )
        return rankings

    async def season_wins(self, season: Season):
        """
        The amount of times a team has won a match in a particular season.

        Args:
            season (:class:`~alliancepy.season.Season`): An alliancepy Season object
        Return:
            int: The number of wins in the specified season
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

        Args:
            season (:class:`~alliancepy.season.Season`): An alliancepy Season object
        Return:
            int: The number of losses in the specified season
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

        Args:
            season (:class:`~alliancepy.season.Season`): An alliancepy Season object
        Return:
            int: The number of ties in the specified season
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

        Args:
            season (:class:`~alliancepy.season.Season`): An alliancepy Season object
        Return:
            float: The team's OPR in the specified season
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

        Args:
            season (:class:`~alliancepy.season.Season`): An alliancepy Season object
        Return:
            float: The team's NP_OPR (OPR without penalties) in the specified season
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

        Args:
            season (:class:`~alliancepy.season.Season`): An alliancepy Season object
        Return:
            float: The team's tiebreaker points in the specified season
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

        Args:
            season (:class:`~alliancepy.season.Season`): An alliancepy Season object
        Return:
            float: The team's ranking points in the specified season
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

        Args:
            season (:class:`~alliancepy.season.Season`): An alliancepy Season object
        Return:
            int: The team's qualifying points in the specified season
        """
        data = await self._rankings(season)
        x = []
        for item in data:
            raw = item["qualifying_points"]
            x.append(int(raw))

        return sum(x)
