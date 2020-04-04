import unittest
import alliancepy
import alliancepy.team
from alliancepy.ext import aio
import alliancepy.ext.aio.async_team as async_team
import asyncio

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


def create_team(team_number: int):
    headers = {
        "api-key": "1e48fa3b34a8ab86cbec44735c5b6055a141f245455faac878bfa204e35c1a7e",
        "application-name": "alliancepy-test",
    }
    client = alliancepy.Client(
        api_key=headers["api-key"], application_name=headers["application-name"]
    )
    team = client.team(team_number)
    return team


async def create_team_async(team_number: int):
    headers = {
        "api-key": "1e48fa3b34a8ab86cbec44735c5b6055a141f245455faac878bfa204e35c1a7e",
        "application-name": "alliancepy-test",
    }
    client = aio.AsyncClient(
        api_key=headers["api-key"], application_name=headers["application-name"]
    )
    team = await client.team(team_number)
    return team


class TestRequest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop = asyncio.get_event_loop()

    def test_instance(self):
        team = create_team(16405)
        self.assertIsInstance(team, alliancepy.team.Team)

    def test_response(self):
        team = create_team(16405)
        self.assertEqual(team.rookie_year, 2019)

    def test_interaction(self):
        team1 = create_team(16405)
        team2 = create_team(16405)
        self.assertEqual(team1.rookie_year, team2.rookie_year)

    def test_instance_async(self):
        team = self.loop.run_until_complete(create_team_async(16405))
        self.assertIsInstance(team, async_team.Team)

    def test_response_async(self):
        team = self.loop.run_until_complete(create_team_async(16405))
        self.assertEqual(team.rookie_year, 2019)

    def test_interaction_async(self):
        team1 = self.loop.run_until_complete(create_team_async(16405))
        team2 = self.loop.run_until_complete(create_team_async(16405))
        self.assertEqual(team1.rookie_year, team2.rookie_year)

    def test_compat(self):
        team1 = create_team(16405)
        team2 = self.loop.run_until_complete(create_team_async(16405))
        self.assertEqual(team1.rookie_year, team2.rookie_year)
