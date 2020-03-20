from alliancepy.http import request


class Team:
    """
    This is the class used to access an existing FTC team. Do not create instances of this class yourself. Instead use
    the "team" method provided by your client object.

    region
        The key of the team's according region.
    league
        The key of the team's league.
    short_name
        The short team name.
    long_name
        The long team name.
    robot_name
        The name of the team's robot.
    location
        The team's location, in "City, State/Province, Country, Zipcode" format.
    rookie_year
        The year in which the team was a rookie team.
    last_active
        The season key of the season in which the team participated in their most recent match.
    website
        The URL of the team's website, if they have any

    """
    def __init__(self, team_number: int, headers: dict):
        self.team_number = team_number
        self.headers = headers
        team_stats = request(target=f"/team/{team_number}", headers=headers)
        team_stats = team_stats[0]
        self.region = team_stats["region_key"]
        self.league = team_stats["league_key"]
        self.short_name = team_stats["team_name_short"]
        self.long_name = team_stats["team_name_long"]
        self.robot_name = team_stats["robot_name"]
        location = f"{team_stats['city']}, {team_stats['state_prov']}, {team_stats['country']}, {team_stats['zip_code']}"
        self.location = location
        self.rookie_year = team_stats["rookie_year"]
        self.last_active = team_stats["last_active"]
        self.website = team_stats["website"]

    def _wlt(self):
        data = request(target=f"/team/{self.team_number}/wlt", headers=self.headers)
        return data[0]

    @property
    def wins(self):
        """
        The total amount of times the team has won a match.
        """
        data = self._wlt()["wins"]
        return int(data)

    @property
    def losses(self):
        """
        The total amount of times the team has lost a match.
        """
        data = self._wlt()["losses"]
        return int(data)

    @property
    def ties(self):
        """The total amount of times the team has tied in a match."""
        data = self._wlt()["ties"]
        return int(data)

    def opr(self, season: int):
        """
        OPR stands for Offensive Power Rating, which is a system to attempt to deduce the average point contribution of
        a team to an alliance. Penalties are also factored in.

        :param season: A valid TOA season key.
        :type season: int
        """
        rankings = request(f"/team/{self.team_number}/results/{season}", headers=self.headers)
        return rankings[0]["opr"]

    def np_opr(self, season: int):
        """
        NP_OPR is just OPR, but penalties are not factored in.

        :param season: A valid TOA season key.
        :type season: int
        """
        rankings = request(f"/team/{self.team_number}/results/{season}", headers=self.headers)
        return rankings[0]["np_opr"]

    def tiebreaker_points(self, season: int):
        """Tiebreaker points are the pre-penalty score of the losing alliance for each match. This function returns the
        total tiebreaker points of a team in one season.

        :param season: A valid TOA season key.
        :type season: int
        """
        rankings = request(f"/team/{self.team_number}/results/{season}", headers=self.headers)
        return rankings[0]["tie_breaker_points"]

    def ranking_points(self, season: int):
        """Ranking points are the number of points scored by the losing alliance in a qualification match.
        If you win the match, then the RP awarded to you is the score of your opponent alliance (which lost).
        If you lose the match, then the RP awarded to you is your own alliance's score.

        :param season: A valid TOA season key.
        :type season: int
        """
        rankings = request(f"/team/{self.team_number}/results/{season}", headers=self.headers)
        return rankings[0]["ranking_points"]

    def qualifying_points(self, season: int):
        """
        Winning teams of a qualifying match eatch receive 2 QP. Losing teams receive 0. If a match ends in a tie, all
        four teams receive 1 QP.


        :param season: A valid TOA season key.
        :type season: int
        """
        rankings = request(f"/team/{self.team_number}/results/{season}", headers=self.headers)
        return rankings[0]["qualifying_points"]
