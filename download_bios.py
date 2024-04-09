import json
import pickle
import requests
import sys

try:
    milb_bios = pickle.load(open("milb_bios.pickle", "rb"))
except (OSError, IOError) as e:
    milb_bios = {}

def pairs_from_stats_dict(stats_dict):
    # stats[0].splits[] | .team.name'
    pairs = []
    if not stats_dict['stats']:
        return []
    splits = stats_dict['stats'][0]['splits']
    for split in splits:
        if split.get('team'):
            pairs.append((split['season'], split['team']))
    return pairs

def pairs_from_roster_dict(roster_dict):
  pairs = []
  for person in roster_dict['roster']:
      pairs.append((person['person']['id'], person['person']['fullName']))
  return pairs

def get_all_year_pairs(player_id):
    mlb_urls = [
        f'https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=yearByYear&gameType=R&leagueListId=mlb_hist&group=hitting&language=en',
        f'https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=yearByYear&gameType=R&leagueListId=mlb_hist&group=pitching&language=en']
    milb_urls = [
        f'https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=yearByYear&gameType=R&leagueListId=milb_all&group=hitting&language=en',
        f'https://statsapi.mlb.com/api/v1/people/{player_id}/stats?stats=yearByYear&gameType=R&leagueListId=milb_all&group=pitching&language=en']
    mlb_pairs = sum([pairs_from_stats_dict(requests.get(mlb_url).json()) for mlb_url in mlb_urls], [])
    if not mlb_pairs:
        print("No MLB stats. He'll get there someday!")
    milb_pairs = sum([pairs_from_stats_dict(requests.get(milb_url).json()) for milb_url in milb_urls], [])
    if not milb_pairs:
        print(f'No MiLB stats for {player_id}? That seems wrong. Is today his first day ever?')
    return mlb_pairs + milb_pairs

def get_roster_url(teams_list, team_name):
#  "teams" : [ {
#    "allStarStatus" : "N",
#    "id" : 4104,
#    "name" : "Coastal Carolina Chanticleers",
#    "link" : "/api/v1/teams/4104",
#    "season" : 2019,
#    "venue" : {
#      "id" : 680,
#      "name" : "T-Mobile Park",
#      "link" : "/api/v1/venues/680"
#    },
  for team in teams_list:
    if team['name'] == team_name:
        team_url = team['link']
        return f'https://statsapi.mlb.com{team_url}/roster'
  print(f'Didn\'t find {team_name} in the list of teams. Things are going to break.')
  sys.exit(1)

def get_roster(teams_list, team_name):
  roster_url = get_roster_url(teams_list, team_name)
  return requests.get(roster_url).json()

#stats_dict = json.load(open('sample_data/stats_milb.json'))
#pairs = print(pairs_from_stats_dict(stats_dict))

teams_list = json.load(open(sys.argv[1]))["teams"]
current_team_name = sys.argv[2]
roster_dict = get_roster(teams_list, current_team_name)
player_pairs = pairs_from_roster_dict(roster_dict)
# fewer_pairs = player_pairs[0:2]

for player_id, player_name in player_pairs:
    if player_id in milb_bios:
        print(f'We already have the goods on {player_name}')
        continue
    else:
        pairs = get_all_year_pairs(player_id)
        milb_bios[player_id] = (player_name, pairs, current_team_name)
        print(f'Updated bio for {player_name}')

pickle.dump(milb_bios, open("milb_bios.pickle", "wb"))
