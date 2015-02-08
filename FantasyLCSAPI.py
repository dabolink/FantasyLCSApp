import requests

#r = requests.get(format("http://na.lolesports.com:80/api/player/{0}", str(player_id)))
#print r.status_code
#json = r.json()
#print json
html_string = "http://na.lolesports.com:80/api{0}/{1}.json{2}"


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

        self.acroynm = JSON["acronym"]
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
            print JSON["contestants"][team]["id"]
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


def get_teams_in_league(tournament_id):
    teams = []
    html = html_string.format("/tournament", tournament_id, "")
    print html
    r = requests.get(html)
    JSON = r.json()
    for team in JSON["contestants"]:
        teams.append(get_team((JSON["contestants"][team]["id"])))
    return teams

#  /Game/  #


def get_game(game_id):
    html = html_string.format("/game", str(game_id), "")
    r = requests.get(html)
    return Game(r.json(), game_id)


#  /Tests/  #

# print get_team(get_player(11).team_id).name
#
# for player in get_team(1).roster:
#     print player.name
#     print '\t' + player.role
#     print '\t' + player.id
#
# print get_game(4544)
# for team in get_teams_in_league(197):
#     print team.name