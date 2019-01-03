import yaml
import json
import requests
import time
import random
from http import HTTPStatus
from bs4 import BeautifulSoup as bs

def get_url(page_url, retries = 3, retry_pause = 10, timeout = 10):
    '''Function to get url and check for errors.'''
    
    headers = { 'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) \
               AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36' }
    
    for retry in range(retries):
        try:
            response = requests.get(page_url, headers = headers, timeout = timeout)
            if response.status_code == HTTPStatus.OK:
                return response
            elif response.status_code in [HTTPStatus.FORBIDDEN]:
                continue
            else:
                break
        except requests.exceptions.Timeout:
            pass 
        time.sleep((1 + 0.3 * random.random()) * retry_pause)

def page_results(page_url):
    '''Function to get match id's from a single page.'''
    
    response = get_url(page_url)
    pages_matches = []
    next_page = None
    
    if response is not None:
        html = response.text
        soup = bs(html, 'html.parser')
        table = soup.find_all(class_= 'cell-large', attrs = {'href'})
        for row in table:
            match_id = row.find_all('a')[0]['href'][9:]
            pages_matches.append(int(match_id))
        if my_soup.find(class_ = 'next') is not None:
            next_page = my_soup.find(class_ = 'next')
            
    return pages_matches, next_page

def get_matches(player_id):
    '''Scrape match ID's from dotabuff.com for given players.'''

    # the general form of a page on dotabuff.com
    url = "https://www.dotabuff.com/players/{player_id}/matches?enhance=overview&page={page}"
    page = 1
    matches = []
    next_page = True
    
    while next_page is not None:
        page_url = url.format(player_id = player_id, page = page)
        results = page_results(page_url)
        matches = matches + results[0]
        page = page + 1
        next_page = results[1]
        
    return matches