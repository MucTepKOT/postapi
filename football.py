import requests
import json
from datetime import datetime, timedelta, date

url = 'https://server1.api-football.com/'
token = '4d6eb732d555294aa9db01b0adfdc475'
headers = {'X-RapidAPI-Key': token, 'Accept': 'application/json'}

def next_match(date):
    endpoint = 'fixtures/team/596'
    now = datetime.now()
    matches = []
    try:
        r = requests.get(url+endpoint, headers=headers)
        response = json.loads(r.text)
    except requests.exceptions.ConnectionError as err:
        print(str(err))
        return 'Error'
    for i in response['api']['fixtures']:
        match_time = i['event_timestamp']
        time = datetime.fromtimestamp(match_time) + timedelta()  # timedelta(hours=3)
        read = time.strftime('%d-%m-%Y(%H:%M)')
        before_date = now + timedelta(days=7)
        if time > now and time < before_date:
            teams = i['homeTeam']['team_name'] + ' - ' + i['awayTeam']['team_name']
            one_match = str(read) + ' ' + teams
            matches.append(one_match)
    if matches:
        return matches
    else:
        return None

# def result(date):
#     # date = date.today()
#     # date = '2019-11-23'
#     endpoint = 'fixtures/league/511/' + date
#     r = requests.get(url+endpoint, headers=headers)
#     fixtures = r.json()['api']['fixtures']
#     # print(fixtures)
#     for games in fixtures:
#         if games['homeTeam']['team_id'] == 596 or games['awayTeam']['team_id'] == 596:
#             return games['score']['fulltime']
#         else:
#             continue
#     return None
    
def all_matches():
    endpoint = 'fixtures/team/596/511'
    try:
        r = requests.get(url+endpoint, headers=headers)
        response = json.loads(r.text)
        return response
    except requests.exceptions.ConnectionError as err:
        print(str(err))
        return 'Error'


        
 
    