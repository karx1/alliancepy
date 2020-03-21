from alliancepy import Team


class Client:
    """
    This is the main client class used for accessing the TOA API. Currently, it only serves up :class:`~.team.Team`
    objects but it will
    expand over time.

    :param api_key: Your TOA API key. This is required, otherwise you will not be able to access the database.
    :type api_key: str
    :param application_name: The name of the application that you are using to access the API. \
    This can just be the name of your script.
    :type application_name: str

    """

    def __init__(self, api_key: str, application_name: str):
        self.toa_key = api_key
        self.application_name = application_name
        self.headers = {
            "content-type": "application/json",
            "x-toa-key": self.toa_key,
            "x-application-origin": self.application_name,
        }

    def team(self, team_number: int):
        """Create a :class:`~.team.Team` object.

        :param team_number: The valid First Tech Challenge team number.
        :type team_number: int
        :return: The Team object
        :rtype: :class:`~.team.Team`
        """
        return Team(team_number=team_number, headers=self.headers)
