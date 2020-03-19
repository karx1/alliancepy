from alliancepy.http import request


class Team:
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
        self.location = f"{team_stats['city']}, {team_stats['state_prov']}, {team_stats['country']}, {team_stats['zip_code']}"
        self.rookie_year = team_stats["rookie_year"]
        self.last_active = team_stats["last_active"]
        self.website = team_stats["website"]

    def _wlt(self):
        data = request(target=f"/team/{self.team_number}/wlt", headers=self.headers)
        return data[0]

    @property
    def wins(self):
        data = self._wlt()["wins"]
        return int(data)

    @property
    def losses(self):
        data = self._wlt()["losses"]
        return int(data)

    @property
    def ties(self):
        data = self._wlt()["ties"]
        return int(data)

    def opr(self, season: int):
        rankings = request(f"/team/{self.team_number}/results/{season}", headers=self.headers)
        return rankings[0]["opr"]

    def np_opr(self, season: int):
        rankings = request(f"/team/{self.team_number}/results/{season}", headers=self.headers)
        return rankings[0]["np_opr"]

    def tiebreaker_points(self, season: int):
        rankings = request(f"/team/{self.team_number}/results/{season}", headers=self.headers)
        return rankings[0]["tie_breaker_points"]

    def ranking_points(self, season: int):
        rankings = request(f"/team/{self.team_number}/results/{season}", headers=self.headers)
        return rankings[0]["ranking_points"]

    def qualifying_points(self, season: int):
        rankings = request(f"/team/{self.team_number}/results/{season}", headers=self.headers)
        return rankings[0]["qualifying_points"]
