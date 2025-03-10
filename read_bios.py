import json
import pickle
import sys

milb_bios = pickle.load(open("milb_bios.pickle", "rb"))
teams_list = json.load(open(sys.argv[1]))["teams"]


def get_team_dict(teams_list, team_id):
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
    # Yeah this is O(T * P) deal with it for now
    for team in teams_list:
        if team["id"] == team_id:
            return team
        # else:
        #    print(f"I swear that {team['id']} is not {team_id}")
    # print(f'Didn\'t find {team_id} in the list of teams. Bailing out.')
    # sys.exit(1)


for player_id in milb_bios:
    (player_name, seasons, current_team_name) = milb_bios[player_id]
    #    if ("2022", "Syracuse Mets") not in seasons:
    #        continue

    output_teams = []
    for year, small_team_dict in sorted(seasons, key=lambda pair: pair[0]):
        full_team_dict = get_team_dict(teams_list, small_team_dict["id"])
        if not full_team_dict:
            team_name = f"{small_team_dict['name']} (team information unavailable)"
        else:
            parent_org_name = full_team_dict.get("parentOrgName")
            if parent_org_name and parent_org_name != "Office of the Commissioner":
                team_name = f"{small_team_dict['name']} (today the {full_team_dict['sport']['name']} affiliate of the {parent_org_name})"
            elif full_team_dict["sport"]["name"] == "Major League Baseball":
                team_name = f"{small_team_dict['name']} (MLB)"
            else:
                team_name = f"{small_team_dict['name']} (apparently a {full_team_dict['sport']['name']} team)"
        team_description = f"{year} {team_name}"
        output_teams.append(team_description)
    for output_team in sorted(set(output_teams)):
        print(
            f"{player_name}, currently with the {current_team_name}, was on the {output_team}"
        )
