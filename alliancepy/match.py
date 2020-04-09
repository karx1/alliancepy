from alliancepy.http import request


class Match:
    def __init__(self, match_key: str, headers: dict):
        self._match_key = match_key
        self._headers = headers
        details = request(f"/match/{self._match_key}/details", headers=self._headers)
        self.randomization = int(details[0]["randomization"])
        self.red = Participant("red", self._match_key, details, self._headers)
        self.blue = Participant("blue", self._match_key, details, self._headers)

    def __str__(self):
        return f"<Match ({self._match_key})>"

    def __repr__(self):
        return str(self)

    @property
    def participants(self):
        participants = request(f"/match/{self._match_key}/participants", headers=self._headers)
        x = []
        for part in participants:
            raw = part["team_key"]
            x.append(int(raw))
        return x


class Participant:
    def __init__(self, alliance: str, match_key: str, details: list, headers: dict):
        self._alliance = alliance
        self._details = details[0]
        self._headers = headers
        self.robot_1 = Robot(self._alliance, 1, match_key, details, self._headers)
        self.robot_2 = Robot(self._alliance, 2, match_key, details, self._headers)

    @property
    def min_penalty(self):
        key = f"{self._alliance}_min_pen"
        return int(self._details[key])

    @property
    def maj_penalty(self):
        key = f"{self._alliance}_maj_pen"
        return int(self._details[key])

    @property
    def auto_stones(self):
        x = []
        for item in self._details[self._alliance]:
            if "auto_stone_" in item:
                x.append(self._details[self._alliance][item])
        return x

    @property
    def foundation(self):
        return self._details[self._alliance]["foundation_repositioned"]

    @property
    def teleop(self):
        delivered = self._details[self._alliance]["tele_delivered"]
        placed = self._details[self._alliance]["tele_placed"]
        returned = self._details[self._alliance]["tele_returned"]
        x = {
            "delivered": delivered,
            "returned": returned,
            "placed": placed
        }
        return x


class Robot:
    def __init__(self, alliance: str, robot_number: int, match_key: str, details: list, headers: dict):
        self._alliance = alliance
        self._robot_number = robot_number
        self._match_key = match_key
        self._details = details[0]
        self._headers = headers

    @property
    def parked_skybridge(self):
        key = f"robot_{self._robot_number}"
        value = self._details[self._alliance][key]["nav"]
        return bool(value)

    @property
    def parked_endgame(self):
        key = f"robot_{self._robot_number}"
        value = self._details[self._alliance][key]["parked"]
        return bool(value)

    @property
    def capstone_level(self):
        key = f"robot_{self._robot_number}"
        value = self._details[self._alliance][key]["parked"]
        return int(value)
    
    @property
    def owner(self):
        participants = request(f"/match/{self._match_key}/participants", headers=self._headers)
        for part in participants:
            station = str(part["station"])
            if int(station[1]) == self._robot_number:
                return int(part["team_key"])