import unittest
import alliancepy
import alliancepy.team


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


class TestRequest(unittest.TestCase):
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
