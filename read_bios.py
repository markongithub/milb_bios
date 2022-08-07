import pickle

milb_bios = pickle.load(open("milb_bios.pickle", "rb"))

for player_id in milb_bios:
    (player_name, seasons, current_team_name) = milb_bios[player_id]
#    if ("2022", "Syracuse Mets") not in seasons:
#        continue
    for (year, team) in sorted(seasons):
        print(f'{player_name}, currently with the {current_team_name}, was on the {year} {team}')
