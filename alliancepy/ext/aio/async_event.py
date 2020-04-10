from .async_http import request
from .async_match import Match
from alliancepy.season import Season
from alliancepy.match_type import MatchType
import asyncio
import re

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


class Event:
    """
    This is the asynchronous version of the normal :class:`~alliancepy.event.Event` class.
    Instances of this class should not be created directly; instead use your :class:`~.team.Team` object.

    season
        The season in which the event occurred.
    region
        The key of the region in which the event occured.
    league
        The key of the league the event occured in, if any.
    name
        The name of the event
    location
        The location of the event, in City, State/Province, Country form.
    venue
        The venue of the event.
    """

    def __init__(self, event_key: str, headers: dict):
        self._event_key = event_key
        self._headers = headers
        self._loop = asyncio.get_event_loop()
        info = self._loop.run_until_complete(
            request(f"/event/{self._event_key}", headers=self._headers)
        )
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

    async def match(self, match_type: MatchType, match_number: int):
        """
        Get one of the matches for the event.

        :param match_type: The type of the match. See :ref:`match_type` for more information.
        :type match_type: :class:`~alliancepy.match_type.MatchType`
        :param match_number: The number of the match.
        :type match_number: int
        :return: A :class:`~.async_match.Match` object containing details about the specific match.
        :rtype: :class:`.async_match.Match`
        """
        if len(str(match_number)) == 1:
            match_name = f"{match_type.value}00{match_number}"
        elif len(str(match_number)) == 2:
            match_name = f"{match_type.value}0{match_number}"
        else:
            match_name = f"{match_type.value}{match_number}"
        loop = asyncio.get_event_loop()
        matches = loop.run_until_complete(request(f"/event/{self._event_key}/matches", headers=self._headers))
        mdict = {}
        for match in matches:
            key = match["match_key"]
            key_right_strip = re.sub(r"\d{4}-\w+-\w+-", "", key)
            value = re.sub(r"-\d+", "", key_right_strip)
            mdict[key] = value
        try:
            match_key = list(mdict.keys())[list(mdict.values()).index(match_name.upper())]
        except ValueError:
            raise ValueError("This match does not exist")
        else:
            return Match(match_key, headers=self._headers)

    async def _rankings(self):
        resp = await request(
            f"/event/{self._event_key}/rankings", headers=self._headers
        )
        return resp

    async def rank(self, team_number: int):
        """
        The specified team's rank at the end of the match.

        :param team_number: A valid FTC team number.
        :type team_number: int
        :return: The rank as an integer
        :rtype: int
        """
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["rank"]
                return int(raw)

    async def rank_change(self, team_number: int):
        """
        The amount of times the team's rank changed during the event.

        :param team_number: A valid FTC team number.
        :type team_number: int
        :return: The rank change as an integer
        :rtype: int
        """
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["rank_change"]
                return int(raw)

    async def wins(self, team_number: int):
        """
        The amount of times within the event that the specified team won a match.

        :param team_number: A valid FTC team number.
        :type team_number: int
        :return: The amount of wins as an integer
        :rtype: int
        """
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["wins"]
                return int(raw)

    async def losses(self, team_number: int):
        """
        The amount of times within the event that the specified team lost a match.

        :param team_number: A valid FTC team number.
        :type team_number: int
        :return: The amount of losses as an integer
        :rtype: int
        """
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["losses"]
                return int(raw)

    async def ties(self, team_number: int):
        """
        The amount of times within the event that the specified team tied in a match.

        :param team_number: A valid FTC team number.
        :type team_number: int
        :return: The amount of ties as an integer
        :rtype: int
        """
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["ties"]
                return int(raw)

    async def opr(self, team_number: int):
        """
        The specified team's OPR for this event only. Penalties are factored in.

        :param team_number: A valid FTC team number.
        :type team_number: int
        :return: The OPR as a floating point number.
        :rtype: float
        """
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["opr"]
                return int(raw)

    async def np_opr(self, team_number: int):
        """
        The specified team's OPR for this event only. Penaltied are not factored in.

        :param team_number: A valid FTC team number.
        :type team_number: int
        :return: The NP_OPR as a floating point number.
        :rtype: float
        """
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["np_opr"]
                return int(raw)

    async def highest_qualifier_score(self, team_number: int):
        """
        The specified team's highest score in a qualifier.

        :param team_number: A valid FTC team number.
        :type team_number: int
        :return: The score as an integer
        :rtype: int
        """
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["highest_qual_score"]
                return int(raw)

    async def ranking_points(self, team_number: int):
        """
        The specified team's ranking points for this event only.

        :param team_number: A valid FTC team number.
        :type team_number: int
        :return: The amount of ranking points as a floating point number
        :rtype: float
        """
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["ranking_points"]
                return int(raw)

    async def qualifying_points(self, team_number: int):
        """
        The specified team's qualifying points for this event only.

        :param team_number: A valid FTC team number.
        :type team_number: int
        :return: The amount of qualifying points as an integer
        :rtype: int
        """
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["qualifying_points"]
                return int(raw)

    async def tiebreaker_points(self, team_number: int):
        """
        The specified team's tiebreaker points for this event only.

        :param team_number: A valid FTC team number.
        :type team_number: int
        :return: The amount of tiebreaker points as a floating point number
        :rtype: int
        """
        rankings = await self._rankings()
        for rank in rankings:
            if rank["team"]["team_number"] == team_number:
                raw = rank["tie_breaker_points"]
                return int(raw)
