from get_matches import get_matches
from get_match_details import get_api, extract_match_details
import yaml
import json
import time
import os
import random

with open('config.yaml', 'r') as yamlfile:
	config = yaml.load(yamlfile)

#Check if the file with players' matches exists and create/update it.
dir_name = 'data'
dir_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))

players_matches = 'players_matches.json'
players_matches_path = os.path.join(dir_path, players_matches)

if not os.path.isdir(dir_path):
	os.mkdir(dir_path)

if not os.path.exists(players_matches_path):
	with open(players_matches_path, 'w') as write_file:
		json.dump({}, write_file)

with open(players_matches_path, 'r') as read_file:
	players_matches_data = json.load(read_file)	

for player_ID in config['player_IDs']:
	if str(player_ID) not in players_matches_data:
		player_matches = get_matches(player_ID)
		players_matches_data.update({player_ID : player_matches})
	else:
		players_matches_data[str(player_ID)] = get_matches(player_ID)
		  
with open(players_matches_path, 'w') as write_file:
	json.dump(players_matches_data, write_file)

with open(players_matches_path, 'r') as read_file:
	players_matches = json.load(read_file)

api = get_api(config['dev_key'])
match_params = config['match_params']
player_params = config['player_params']

pause = 1
counter = 1
for player_ID in players_matches:
	player_match_details = 'player_' + player_ID + '_match_details.json'
	player_match_details_path = os.path.join(dir_path, player_match_details)

	matches_details = {}
	for match_ID in players_matches[player_ID]:
		print(counter)
		try:
			matches_details[match_ID] = extract_match_details(api, int(player_ID),
									    match_ID, player_params, match_params)
			time.sleep(pause)
		except:
			pass
		counter = counter + 1

	with open(player_match_details_path, 'a') as write_file:
		json.dump(matches_details, write_file)