from alliancepy import Team


class Client:
    def __init__(self, api_key: str, application_name: str):
        self.toa_key = api_key
        self.application_name = application_name
        self.headers = {
            "content-type": "application/json",
            "x-toa-key": self.toa_key,
            "x-application-origin": self.application_name
        }

    def team(self, team_number: int):
        return Team(team_number=team_number, headers=self.headers)
