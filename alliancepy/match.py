from alliancepy.http import request
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


class Match:
    """
    An object containing the details of an FTC match. Instances of this class should not be created directly. Instead,
    use your :class:`~alliancepy.event.Event` object.

    randomization
        The randomization of the stones and skystones at the beginning of the match.
    red
        An :class:`Alliance` object containing the details of the red alliance of the match.
    blue
        An :class:`Alliance` object containing the details of the blue alliance of the match.
    """

    def __init__(self, match_key: str, headers: dict):
        self._match_key = match_key
        self._headers = headers
        details = request(f"/match/{self._match_key}/details", headers=self._headers)
        self.randomization = int(details[0]["randomization"])
        self.red = Alliance("red", self._match_key, details, self._headers)
        self.blue = Alliance("blue", self._match_key, details, self._headers)
        logger.info(f"Initialized Match object with match key of {self._match_key}")

    def __str__(self):
        return f"<Match ({self._match_key})>"

    def __repr__(self):
        return str(self)

    @property
    def participants(self):
        """
        The participants of the match.

        :return: The team numbers in a list
        :rtype: List[int]
        """
        participants = request(
            f"/match/{self._match_key}/participants", headers=self._headers
        )
        x = []
        for part in participants:
            raw = part["team_key"]
            x.append(int(raw))
        return x


class Alliance:
    """
    An object representing a match alliance. Instances of this class should not be created directly. Instead,
    use your :class:`Match` object.

    robot_1
        A :class:`Robot` object that represents the first team's robot.
    robot_2
        A :class:`Robot` object that represents the second team's robot.
    """

    def __init__(self, alliance: str, match_key: str, details: list, headers: dict):
        self._alliance = alliance
        self._details = details[0]
        self._headers = headers
        self.robot_1 = Robot(self._alliance, 1, match_key, details, self._headers)
        self.robot_2 = Robot(self._alliance, 2, match_key, details, self._headers)
        logger.info(
            f"Initialized Alliance object with alliance name of {self._alliance}"
        )

    def __str__(self):
        return f"<Alliance ({self._alliance})>"

    def __repr__(self):
        return str(self)

    @property
    def min_penalty(self):
        """
        The amount of minor penalties an alliance earned.

        :rtype: int
        """
        key = f"{self._alliance}_min_pen"
        return int(self._details[key])

    @property
    def maj_penalty(self):
        """
        The amount of major penalites an alliance earned.

        :rtype: int
        """
        key = f"{self._alliance}_maj_pen"
        return int(self._details[key])

    @property
    def auto_stones(self):
        """A list of the stones the alliance stacked in autonomous.

        :rtype: List[str]
        """
        x = []
        for item in self._details[self._alliance]:
            if "auto_stone_" in item:
                x.append(self._details[self._alliance][item])
        return x

    @property
    def foundation(self):
        """
        Whether the alliance repositioned the foundation suring autonomous or not.

        :rtype: bool
        """
        return self._details[self._alliance]["foundation_repositioned"]

    @property
    def teleop(self):
        """
        Returns a dict containing integer values.
        Contains "delivered", "placed", and "returned".

        :rtype: dict[str: int]
        """
        delivered = self._details[self._alliance]["tele_delivered"]
        placed = self._details[self._alliance]["tele_placed"]
        returned = self._details[self._alliance]["tele_returned"]
        x = {"delivered": delivered, "returned": returned, "placed": placed}
        return x


class Robot:
    """
    An object containing details about a robot. Instances of this class should not be created directly. Instead,
    use your :class:`Alliance` object.
    """

    def __init__(
        self,
        alliance: str,
        robot_number: int,
        match_key: str,
        details: list,
        headers: dict,
    ):
        self._alliance = alliance
        self._robot_number = robot_number
        self._match_key = match_key
        self._details = details[0]
        self._headers = headers
        logger.info(
            f"Initialized Robot object with alliance {self._alliance} and robot number of {self._robot_number}"
        )

    @property
    def parked_skybridge(self):
        """Whether the robot parked under the skybridge or not

        :rtype: bool
        """
        key = f"robot_{self._robot_number}"
        value = self._details[self._alliance][key]["nav"]
        return bool(value)

    @property
    def parked_endgame(self):
        """
        Whether the robot parked at the end of the match or not.

        :rtype: bool
        """
        key = f"robot_{self._robot_number}"
        value = self._details[self._alliance][key]["parked"]
        return bool(value)

    @property
    def capstone_level(self):
        """
        The level of the capstone at the end of the match.

        :rtype: int
        """
        key = f"robot_{self._robot_number}"
        value = self._details[self._alliance][key]["parked"]
        return int(value)

    @property
    def owner(self):
        """The team that owns the bot.

        :return: The team's team number as an integer
        :rtype: int
        """
        match = request(f"/match/{self._match_key}", headers=self._headers)
        participants = list(
            filter(lambda p: p["station_status"] == 1, match[0]["participants"])
        )
        if self._alliance == "red" and self._robot_number == 1:
            raw = participants[0]["team_key"]
        elif self._alliance == "red" and self._robot_number == 2:
            raw = participants[1]["team_key"]
        elif self._alliance == "blue" and self._robot_number == 1:
            raw = participants[2]["team_key"]
        elif self._alliance == "blue" and self._robot_number == 2:
            raw = participants[3]["team_key"]
        else:
            raise ValueError("Something went wrong, please try again")
        return int(raw)
