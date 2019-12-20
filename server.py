# -*- encoding: utf-8 -*-
import logging
from aiohttp import web
import json
import mongo
import postgresql
import keygen
import requests
from datetime import datetime, timedelta
import yaml

try:
    with open(r'config.yaml') as cfg:
        config = yaml.load(cfg, Loader=yaml.FullLoader)
        logging.info('Config successfully loaded')
except yaml.error.YAMLError as err:
    logging.error(f'Yaml config error: {err}')

log_format = '%(asctime)s %(filename)s: %(message)s'
logging.basicConfig(filename="server.log", format=log_format, level=logging.DEBUG)

db = mongo.connect_mongo()

async def main_page(request):
    response_obj = 'Welcome to my API'
    return web.Response(text=response_obj, status=200)

async def get_prediction(request):
    header = request.headers
    if 'user' and 'access_token' in header:
        user_name = header['user'].lower()
        token = header['access_token']
        db_token = postgresql.get_token(user_name)
        if token == db_token and postgresql.token_alive(token) == True:
            collection = 'predictions'
            response_obj = {'predictions' : mongo.my_prediction(db, collection, user_name)}
            return web.Response(text=json.dumps(response_obj), status=200)
        else:
            response_obj = {'status': 'auth_error', 'message': "You aren't authorize or your token not alive"}
            return web.Response(text=json.dumps(response_obj), status=401)
    else:
        response_obj = {'status': 'message_error', 'message': 'incorrect parametres'}
        return web.Response(text=json.dumps(response_obj), status=400)

async def registration(request):
    user_registration = await request.json()
    if 'user' and 'password' in user_registration and len(user_registration) == 2:
        user_name = user_registration['user'].lower()
        password = user_registration['password']
        if postgresql.check_user(user_name):
            response_obj = {'Error': 'User already exist'}
            return web.Response(text=json.dumps(response_obj), status=406)
        else:
            user_password = keygen.hash(password)
            token = keygen.hash(f'{user_name}{password}')
            reg = postgresql.create_user(user_name, user_password, token)
            if reg == 'Error':
                response_obj = {'Error': 'Something went wrong, try again pls'}
                return web.Response(text=json.dumps(response_obj), status=400)
            else:
                response_obj = {'access_token': token}
                return web.Response(text=json.dumps(response_obj), status=200)
    else:
        response_obj = {'status': 'message_error', 'message': 'give me your Name and Password'}
        return web.Response(text=json.dumps(response_obj), status=400)

async def new_token(request):
    user_registration = await request.json()
    if 'user' and 'password' in user_registration and len(user_registration) == 2:
        user_name = user_registration['user'].lower()
        password = user_registration['password']
        if postgresql.check_user(user_name) == False:
            response_obj = {'Error': 'User not registered'}
            return web.Response(text=json.dumps(response_obj), status=401)
        else:
            db_password = postgresql.check_password(user_name)
            verify = keygen.verify_hash(password, db_password)
            if verify == True:
                token = keygen.hash(f'{user_name}{password}')
                new_token = postgresql.update_token(user_name, token)
                if new_token == 'Success':
                    response_obj = {'access_token': token}
                    return web.Response(text=json.dumps(response_obj), status=200)
                else:
                    response_obj = {'Error': 'Something went wrong, try again pls'}
                    return web.Response(text=json.dumps(response_obj), status=400)
            else:
                response_obj = {'auth_error': 'password invalid'}
                return web.Response(text=json.dumps(response_obj), status=401)        
    else:
        response_obj = {'status': 'message_error', 'message': 'give me your Name and Password'}
        return web.Response(text=json.dumps(response_obj), status=400)

async def post_prediction(request):
    try:
        user_predict = await request.json()  # get json-like body
        header = request.headers
        if 'user' and 'access_token' in header:
            user_name = header['user'].lower()
            token = header['access_token']
            db_token = postgresql.get_token(user_name)
            if token == db_token and postgresql.token_alive(token) == True:
                if 'scores' in user_predict and len(user_predict) == 1 and len(user_predict['scores']) == 3:
                    collection = 'results'
                    timestamp = datetime.timestamp(datetime.now())
                    time_check = mongo.check_time_prediction(db, collection, timestamp)
                    if time_check == 'Error':
                        response_obj = {'status': 'time_error', 'message': 'you can post predictions not early than 24 hours and no later than 10 minutes before the match'}
                        return web.Response(text=json.dumps(response_obj), status=400)
                    else:
                        user_predict['fixture_id'] = time_check
                        user_predict['user_name'] = user_name
                        user_predict['timestamp'] = int(timestamp)
                        collection = 'predictions'
                        inserting = mongo.update_db(db, collection, **user_predict)
                        if inserting == None:
                            response_obj = {'status': 'accepted', 'message': 'your predict accepted'}
                            return web.Response(text=json.dumps(response_obj), status=202)
                        else:
                            response_obj = {'status': 'error', 'message': 'something went wrong, try again pls'}
                            return web.Response(text=json.dumps(response_obj), status=400)
                else:
                    response_obj = {'status': 'message_error', 'message': 'incorrect data'}
                    return web.Response(text=json.dumps(response_obj), status=400)
            else:
                response_obj = {'status': 'auth_error', 'message': "You aren't authorize or your token not alive"}
                return web.Response(text=json.dumps(response_obj), status=401)
        else:
            response_obj = {'status': 'auth_error', 'message': "You aren't authorize or your token not alive"}
            return web.Response(text=json.dumps(response_obj), status=401)
    except Exception as err:
        logging.error(f'Error: {str(err)}')
        response_obj = {'status': 'failed', 'message': 'you have PAWS'}
        return web.Response(text=json.dumps(response_obj), status=500)

async def get_points(request):
    header = request.headers
    if 'user' and 'access_token' in header:
        user_name = header['user'].lower()
        token = header['access_token']
        db_token = postgresql.get_token(user_name)
        if token == db_token and postgresql.token_alive(token) == True:
            collection = 'users_scores'
            response_obj = {'your_points': mongo.find_all(db, collection)}
            return web.Response(text=json.dumps(response_obj), status=200)
        else:
            response_obj = {'status': 'auth_error', 'message': "You aren't authorize or your token not alive"}
            return web.Response(text=json.dumps(response_obj), status=401)
    else:
        response_obj = {'status': 'message_error', 'message': 'incorrect parametres'}
        return web.Response(text=json.dumps(response_obj), status=400)

async def next_match(request):
    url = config['api_url']
    token = config['api_token']
    headers = {'X-RapidAPI-Key': token, 'Accept': 'application/json'}
    endpoint = 'fixtures/team/596'
    now = datetime.now()
    matches = []
    try:
        r = requests.get(f'{url}{endpoint}', headers=headers)
        response = json.loads(r.text)
    except requests.exceptions.ConnectionError as err:
        logging.error(f'Error: {str(err)}')
        response_obj = {'status': 'error', 'message': str(err)}
        return web.Response(text=json.dumps(response_obj), status=400)
    for i in response['api']['fixtures']:
        match_time = i['event_timestamp']
        time = datetime.fromtimestamp(match_time) + timedelta()  # timedelta(hours=3)
        read = time.strftime('%d-%m-%Y(%H:%M)')
        before_date = now + timedelta(days=7)
        if time > now and time < before_date:
            teams = f"{i['homeTeam']['team_name']} - {i['awayTeam']['team_name']}"
            one_match = f'{str(read)} {teams}'
            matches.append(one_match)
    if matches:
        response_obj = {'next_match': matches}
        return web.Response(text=json.dumps(response_obj), status=200)
    else:
        response_obj = {'empty': 'there are no matches in the next 7 days'}
        return web.Response(text=json.dumps(response_obj), status=200)

app = web.Application()
app.add_routes([web.get('/', main_page),
                web.get('/get_prediction', get_prediction),
                web.post('/registration', registration),
                web.post('/new_token', new_token),
                web.post('/post_prediction', post_prediction),
                web.get('/get_points', get_points),
                web.get('/next_match', next_match)])

web.run_app(app, host=config['web_host'], port=config['web_port'])
