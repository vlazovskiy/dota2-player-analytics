import dota2api

def get_api(WebKey):
	'''Takes developer's key and return an api object.'''
	return dota2api.Initialise(WebKey)

def extract_match_details(api_call, player_ID, match_ID, 
                         player_params = None, match_params = None):
    '''Get specified match details, check for leavers, and whether player won.'''
    match = api_call.get_match_details(match_id = match_ID)
    match_details = {} 
    match_details['leavers'] = check_leavers(match)
    match_details['won'] = check_win(player_ID, match)
    # Get player information
    for player in match['players']:
        if 'account_id' in player and player['account_id'] == player_ID:
            if player_params is not None:
                for param in player_params:
                    if param in player:
                        match_details[param] = player[param]
                    else:
                        match_details[param] = -1
            else:
                match_details.update({key : value for key, value in player.items() 
                                      if key != 'account_id'})
        else:
            continue
    # Get match information
    if match_params is not None:
        for param in match_params:
            if param in match_params:
                match_details[param] = match[param]
            else:
                match_details[param] = -1
    else:
        match_details.update({key : value for key, value in match.items() 
                              if key != 'players'})
        
    return match_details

def check_leavers(match):
    '''Leaver detector: check if there are any leavers in the game.
       In case no stats are recorded, returns -1.'''
    leaver_status = 0 
    for player in match['players']:
        if player.get('leaver_status', -1) > 1:
            leaver_status = 1
            break
        elif player.get('leaver_status', -1) == -1:
            leaver_status = -1
            break 
    return leaver_status

def get_index(player_list, player_ID):
    '''Helper function for the function to check player win/loss.'''
    player_index = -1
    for index_, dict_ in enumerate(player_list):
        if 'account_id' in dict_ and dict_['account_id'] == player_ID:
            player_index = index_
        else:
            continue
    return player_index

def check_win(player_ID, match):
    '''Find out if the player won the match'''
    player_index = get_index(match['players'], player_ID)
    if player_index >= 0:
        if player_index <= 4 and match['radiant_win'] == True:
            return 1
        elif player_index > 4 and match['radiant_win'] == False:
            return 1
        else:
            return 0
    return -1