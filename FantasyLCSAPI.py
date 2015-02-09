import requests
from datetime import *
#r = requests.get(format("http://na.lolesports.com:80/api/player/{0}", str(player_id)))
#print r.status_code
#json = r.json()
#print json

NALCS = 197
EULCS = 195

cur_date = date.today()
one_week = date.today() + timedelta(weeks=1)
html_string = "http://na.lolesports.com:80/api{0}/{1}.json{2}"

class TeamStats:
    def __init__(self, JSON, game_id, team_id):
        self.team_id = team_id
        self.game_id = game_id
        team_stats = JSON["teamStats"]["game"+str(game_id)]["team"+str(team_id)]
        self.first_blood = team_stats["firstBlood"]
        self.towers = team_stats["towersKilled"]
        self.barons = team_stats["baronsKilled"]
        self.dragons = team_stats["dragonsKilled"]
        self.victory = team_stats["matchVictory"]
        self.game_length = JSON["teamStats"]["game"+str(game_id)]["timePlayed"]
        self.fantasy_points = self.calc_points()

    def calc_points(self):
        points = self.first_blood * 2 + self.towers * 1 + self.barons * 2 + self.dragons * 1 + self.victory * 2
        if self.game_length < 1800:
            points += 2
        return points



class PlayerStats:
    def __init__(self, JSON, game_id, player_id):
        self.player_id = player_id
        self.game_id = game_id
        player_stats = JSON["playerStats"]["game"+str(game_id)]["player"+str(player_id)]
        self.kills = player_stats["kills"]
        self.deaths = player_stats["deaths"]
        self.assists = player_stats["assists"]
        self.minion_kills = player_stats["minionKills"]
        self.double_kills = player_stats["doubleKills"]
        self.triple_kills = player_stats["tripleKills"]
        self.quadra_kills = player_stats["quadraKills"]
        self.penta_kills = player_stats["pentaKills"]
        self.fantasy_points = self.calc_points()

    def calc_points(self):
        points = (self.kills * 2) + (self.deaths * (-.5)) + self.assists * 1.5 + (self.minion_kills * 0.01)\
            + (self.triple_kills * 2) + (self.quadra_kills * 5)\
            + (self.penta_kills * 10)
        if (self.kills + self.assists) > 10:
            points += 2
        return points




class Player:
    def __init__(self, JSON, player_id):
        self.first_name = JSON["firstname"]
        self.last_name = JSON["lastName"]
        self.role = JSON["role"]
        self.role_id = JSON["roleId"]
        self.player_id = player_id
        self.team_id = JSON["teamId"]


class Team_Player:
    def __init__(self, player):
        self.id = player["playerId"]
        self.name = player["name"]
        self.role = player["role"]
        self.isStarter = player["isStarter"]


class Team:
    def __init__(self, JSON, team_id=0):
        self.name = JSON["name"]
        self.roster = []
        for player in JSON["roster"]:
            self.roster.append(Team_Player(JSON["roster"][player]))

        self.acronym = JSON["acronym"]
        self.team_id = team_id


class Game:
    def __init__(self, JSON, game_id):
        self.game_id = game_id
        self.winner_id = JSON["winnerId"]
        self.game_number = JSON["gameNumber"]
        self.max_games = JSON["maxGames"]
        self.game_length = JSON["gameLength"]
        self.contestants = []
        for team in JSON["contestants"]:
            self.contestants.append(get_team(JSON["contestants"][team]["id"]))






#  /player/  #


def get_player(player_id):
    # 11 = Dyrus
    html = html_string.format("/player", str(player_id), "")
    r = requests.get(html)
    #print r.status_code
    return Player(r.json(), player_id)


#  /league/  #



#  /Team/  #


def get_team(team_id):
    # 1 = Team SoloMid
    html = html_string.format("/team", str(team_id), "")
    r = requests.get(html)
    return Team(r.json(), team_id)


def get_teams_in_tournament(tournament_id):
    teams = []
    html = html_string.format("/tournament", tournament_id, "")
    r = requests.get(html)
    JSON = r.json()
    for team in JSON["contestants"]:
        teams.append(get_team((JSON["contestants"][team]["id"])))
    return teams

#  /Game/  #


def get_game(game_id, cur_date, one_week):
    html = html_string.format("/game", str(game_id), "")
    r = requests.get(html)
    return Game(r.json(), game_id)


def get_player_stats_for_game(tournament_id, game_id, player_id):
    html = html_string.format("", "gameStatsFantasy", "?tournamentId=" + str(tournament_id))
    r = requests.get(html)
    return PlayerStats(r.json(), game_id, player_id)

def get_team_stats_for_game(tournament_id, game_id, team_id):
    html = html_string.format("", "gameStatsFantasy", "?tournamentId=" + str(tournament_id))
    r = requests.get(html)
    return TeamStats(r.json(), game_id, team_id)


#  /FANTASY/  #

#  /Tests/  #

# print get_team(get_player(11).team_id).name
#
# for player in get_team(1).roster:
#     print player.name
#     print '\t' + player.role
#     print '\t' + player.id
#     print '\t' + str(player.profile_url)
#
# print get_game(4544).contestants
# for team in get_teams_in_tournament(197):
#     print team.name
game1 = get_team_stats_for_game(NALCS, 4544, 1)
game2 = get_team_stats_for_game(NALCS, 4553, 1)
print game1.fantasy_points + game2.fantasy_points
