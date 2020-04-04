import unittest
import alliancepy
import alliancepy.team
from alliancepy.ext import aio
import alliancepy.ext.aio.async_team as async_team
import asyncio


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
    client = aio.AsyncClient(api_key=headers["api-key"], application_name=headers["application-name"])
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
