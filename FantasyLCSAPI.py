import requests
from datetime import *
import re
# r = requests.get(format("http://na.lolesports.com:80/api/player/{0}", str(player_id)))
# print r.status_code
# json = r.json()
# print json
NALCS = 197
EULCS = 195
ADC = "AD Carry"
MID = "Mid Lane"
TOP = "Top Lane"
SUPPORT = "Support"
JUNGLER = "Jungler"

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
        try:
            player_stats = JSON["playerStats"]["game"+str(game_id)]["player"+str(player_id)]
        except KeyError:
            self.kills = 0
            self.assists = 0
            self.deaths = 0
            self.minion_kills = 0
            self.double_kills = 0
            self.triple_kills = 0
            self.quadra_kills = 0
            self.penta_kills = 0
            self.fantasy_points = 0
            return
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
        if self.kills > 10 or self.assists > 10:
            points += 2
        return points




class Player:
    def __init__(self, JSON, player_id):
        self.name = JSON["name"]
        self.first_name = JSON["firstname"]
        self.last_name = JSON["lastName"]
        self.role = JSON["role"]
        self.role_id = JSON["roleId"]
        self.player_id = player_id
        self.team_id = JSON["teamId"]


class Team_Player:
    def __init__(self, player):
        self.player_id = player["playerId"]
        self.name = player["name"]
        self.role = player["role"]
        self.isStarter = player["isStarter"]


class Team:
    def __init__(self, JSON, team_id):
        self.name = JSON["name"]
        self.roster = []
        for player in JSON["roster"]:
            self.roster.append(Team_Player(JSON["roster"][player]))

        self.acronym = JSON["acronym"]
        self.team_id = team_id


class Game:
    def __init__(self, JSON, game_id):
        self.game_id = game_id
        self.match_id = JSON["matchId"]
        self.winner_id = JSON["winnerId"]
        self.game_number = JSON["gameNumber"]
        self.max_games = JSON["maxGames"]
        self.game_length = JSON["gameLength"]
        self.contestants = []
        self.player_ids = []
        for player_id in JSON["players"]:
            self.player_ids.append(JSON["players"][player_id]["id"])
        for team in JSON["contestants"]:
            self.contestants.append(get_team(JSON["contestants"][team]["id"]))


class Contestant:
    def __init__(self, JSON, contestant):
        self.side = contestant
        self.team_id = JSON["id"]
        self.name = JSON["name"]


class MatchGame:
    def __init__(self, JSON):
        self.game_id = JSON["id"]
        self.winner_id = JSON["winnerId"]


class Match:
    def __init__(self, JSON, match_id):
        date_string = JSON["dateTime"]
        self.dateTime = date(int(date_string[:4]),int(date_string[5:7]), int(date_string[8:10]))
        self.match_id = match_id
        self.games = []
        self.winnerId = JSON["winnerId"]
        self.is_finished = int(JSON["isFinished"])
        self.is_live = int(JSON["isLive"])
        for game in JSON["games"]:
            self.games.append(MatchGame(JSON["games"][game]))
        self.name = JSON["name"]
        self.contestants = []
        for contestant in JSON["contestants"]:
            self.contestants.append(Contestant(JSON["contestants"][contestant], contestant))


#  /player/  #
def get_game(game_id):
    html = html_string.format("/game", "4544", "")
    r = requests.get(html)
    return Game(r.json(), game_id)

def get_player(player_id):
    # 11 = Dyrus
    html = html_string.format("/player", str(player_id), "")
    r = requests.get(html)
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


def get_players_in_tournament(tournament_id, role=False):
    players = []
    for team in get_teams_in_tournament(tournament_id):
        for player in team.roster:
            if role:
                if player.role == role:
                    players.append(player)
            else:
                players.append(player)

    return players
#  /Game/  #


def get_matches_for_week(tournament_id, start_date="", end_date="", team_id = ""):
    html = html_string.format("", "schedule", "?tournamentId=" + str(tournament_id) + "")
    r = requests.get(html)
    matches = []
    JSON = r.json()
    for match in JSON:
        cur_match = Match(JSON[match], JSON[match]["matchId"])
        if end_date >= cur_match.dateTime >= start_date:
            matches.append(cur_match)
    return matches

def get_player_stats_for_game(tournament_id, game_id, player_id):
    html = html_string.format("", "gameStatsFantasy", "?tournamentId=" + str(tournament_id))
    r = requests.get(html)
    return PlayerStats(r.json(), game_id, player_id)


def get_team_stats_for_game(tournament_id, game_id, team_id):
    html = html_string.format("", "gameStatsFantasy", "?tournamentId=" + str(tournament_id))
    r = requests.get(html)
    return TeamStats(r.json(), game_id, team_id)


#  /FANTASY/  #
def get_all_fantasy_points_for_week(tournament_id, start_date, end_date):
    players = {}
    for match in get_matches_for_week(tournament_id, start_date, end_date):
        if not match.is_live and not match.is_finished:
            continue
        print match.name
        for game in match.games:
            for contestant in match.contestants:
                for player in get_team(contestant.team_id).roster:
                    if player.isStarter:
                        try:
                            players[player.name] += get_player_stats_for_game(tournament_id, game.game_id, player.player_id).fantasy_points
                        except KeyError:
                            players[player.name] = get_player_stats_for_game(tournament_id, game.game_id, player.player_id).fantasy_points
    return players
#  /Tests/  #

# print get_team(get_player(11).team_id).name
#
# for player in get_team(1).roster:
#     print player.name
#     print '\t' + player.role
#     print '\t' + player.id
#     print '\t' + str(player.profile_url)
#
# for team in get_teams_in_tournament(197):
# #     print team.name
start_date = date(2015, 02, 11)
end_date = date(2015, 02, 15)
print get_all_fantasy_points_for_week(EULCS, start_date, end_date)
print get_all_fantasy_points_for_week(NALCS, start_date, end_date)
# game1 = get_team_stats_for_game(NALCS, 4544, 1)
# game2 = get_team_stats_for_game(NALCS, 4553, 1)
# print game1.fantasy_points
# print game2.fantasy_points


# for player in get_players_in_tournament(NALCS, TOP):
#     print player.name