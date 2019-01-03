from get_matches import get_matches
from get_match_details import get_api, extract_match_details
import yaml
import json
import time
import random

with open('player_data.yaml', 'r') as yamlfile:
    config = yaml.load(yamlfile)

with open('players_matches.json', 'r') as read_file:
    players_matches_data = json.load(read_file)

for player_ID in config['player_IDs']:
    if str(player_ID) not in players_matches_data:
        player_matches = get_matches(player_ID)
        players_matches_data.update({player_ID : player_matches})
    else:
        players_matches_data[player_ID] = get_matches(player_ID)
      
with open('players_matches.json', 'w') as write_file:
    json.dump(players_matches_data, write_file)

with open('players_matches.json', 'r') as read_file:
	players_matches = json.load(read_file)


api = get_api('99EE52D56A138EA0FA0B2EC62432E2EB')
match_params = ['match_id', 'start_time', 'lobby_type', 'lobby_name', 'game_mode', 'duration']
player_params = ['kills', 'deaths', 'assists', 'last_hits', 'level', 'xp_per_min', 'gold_per_min', 'gold_spent',
                'gold', 'hero_id', 'item_0', 'item_1', 'item_2', 'item_3', 'item_4', 'item_5', 
                'backpack_0', 'backpack_1', 'backpack_2']
     
pause = 1 
errors = []
for player_ID in players_matches:
	with open('player_' + player_ID + '_match_details.json', 'a') as write_file:
		for match_ID in players_matches[player_ID]:
			try:
				json.dump({ match_ID : extract_match_details(api, player_ID, match_ID, 
														     player_params, match_params)}, write_file)
				time.sleep(pause)
			except:
				errors.append(match_ID)
				pass
