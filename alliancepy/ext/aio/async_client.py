from .async_team import Team


class AsyncClient:
    """
    This is the asynchronous version on the main client class. It has the same paramters and the team method, but async.
    This means that it must be called with `await`.

    :param api_key: Your TOA API key. This is required, otherwise you will not be able to access the database.
    :type api_key: str
    :param application_name: The name of the application that you are using to access the API. \
    This can just be the name of your script.
    :type application_name: str

    """
    def __init__(self, api_key: str, application_name: str):
        self._headers = {
            "content-type": "application/json",
            "x-toa-key": api_key,
            "x-application-origin": application_name
        }

    async def team(self, team_number: int):
        """
        Create an asynchronous :class:`~.async_team.Team` object.

        :param team_number: A valid First Tech Challenge team number.
        :type team_number: int
        :return: The Team object
        :rtype: :class:`~.async.Team`
        """
        return Team(team_number=team_number, headers=self._headers)
