from .async_team import Team
import asyncio


class AsyncClient:
    def __init__(self, api_key: str, application_name: str):
        self._headers = {
            "content-type": "application/json",
            "x-toa-key": api_key,
            "x-application-origin": application_name
        }

    async def team(self, team_number: int):
        return Team(team_number=team_number, headers=self._headers)
