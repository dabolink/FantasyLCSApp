import requests

#r = requests.get(format("http://na.lolesports.com:80/api/player/{0}", str(player_id)))
#print r.status_code
#json = r.json()
#print json
html_string = "http://na.lolesports.com:80/api/{0}/{1}.json"


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
    def __init__(self, JSON, team_id):
        self.name = JSON["name"]
        self.roster = []
        for player in JSON["roster"]:
            self.roster.append(Team_Player(JSON["roster"][player]))

        self.acroynm = JSON["acronym"]
        self.team_id = team_id






#  /player/  #


def get_player(player_id):
    # 11 = Dyrus
    html = html_string.format("player", str(player_id))
    r = requests.get(html)
    #print r.status_code
    return Player(r.json(), player_id)

#  /league/  #



#  /Team/  #
def get_team(team_id):
    # 1 = Team SoloMid
    html = html_string.format("team", str(team_id))
    r = requests.get(html)
    return Team(r.json(), team_id)
#  /Tests/  #

print get_team(get_player(11).team_id).name

for player in get_team(1).roster:
    print player.name
    print '\t' + player.role
    print '\t' + player.id