from alliancepy.team import Team

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
        self._headers = {
            "content-type": "application/json",
            "x-toa-key": api_key,
            "x-application-origin": application_name,
        }

    def team(self, team_number: int):
        """Create a :class:`~.team.Team` object.

        :param team_number: A valid First Tech Challenge team number.
        :type team_number: int
        :return: The Team object
        :rtype: :class:`~.team.Team`
        """
        return Team(team_number=team_number, headers=self._headers)
