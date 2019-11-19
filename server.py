# -*- encoding: utf-8 -*-
import logging
from aiohttp import web
import json
import mongo
import postgresql
import keygen

async def main_page(request):
    response_obj = 'Welcome to my API'
    return web.Response(text=response_obj, status=200)

async def get_prediction(request):
    header = request.headers
    if 'user' and 'access_token' in header:
        user_name = header['user'].lower()
        token = header['access_token']
        db_token = postgresql.get_token(user_name)
        if keygen.verify_hash(token, db_token) == True:
            response_obj = {'predictions' : mongo.my_prediction(user_name)}
            return web.Response(text=json.dumps(response_obj), status=200)
        else:
            response_obj = {'status': 'auth_error', 'message': 'ti cho psina, kuda polez?'}
            return web.Response(text=json.dumps(response_obj), status=401)
    else:
        response_obj = {'status': 'message_error', 'message': 'incorrect parametres'}
        return web.Response(text=json.dumps(response_obj), status=400)

async def registration(request):
    user_registration = await request.json()
    if 'user' and 'password' in user_registration and len(user_registration) == 2:
        user_name = user_registration['user'].lower()
        password = user_registration['password']
        user_password = keygen.hash(user_name + password)
        token = keygen.hash(user_name + password)
        user_exist = postgresql.create_user(user_name, user_password, token)
        if user_exist == 'Error':
            response_obj = {'Error': 'User already exist'}
            return web.Response(text=json.dumps(response_obj), status=406)
        else:
            response_obj = {'your access_token': token}
            return web.Response(text=json.dumps(response_obj), status=200)
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
            if db_token == None:
                response_obj = {'status': 'auth_error', 'message': 'ti cho psina, kuda polez?'}
                return web.Response(text=json.dumps(response_obj), status=401)
            else:
                if keygen.verify_hash(token, db_token) == True:
                    if 'username' and 'scores' in user_predict and len(user_predict) == 2:
                        data = user_predict
                        inserting = mongo.insert_db(user_name, data)
                        if inserting == 'Success':
                            response_obj = {'status': 'accepted', 'message': 'your predict accepted'}
                            return web.Response(text=json.dumps(response_obj), status=202)
                        else:
                            response_obj = {'status': 'accepted', 'message': 'something went wrong, repeat pls'}
                            return web.Response(text=json.dumps(response_obj), status=400)
                    else:
                        response_obj = {'status': 'message_error', 'message': 'pls post it into your ass'}
                        return web.Response(text=json.dumps(response_obj), status=400)
                else:
                    response_obj = {'status': 'auth_error', 'message': 'ti cho psina, kuda polez?'}
                    return web.Response(text=json.dumps(response_obj), status=401)
        else:
            response_obj = {'status': 'auth_error', 'message': 'ti cho psina, kuda polez?'}
            return web.Response(text=json.dumps(response_obj), status=401)
    except Exception as e:
        print(e)
        response_obj = {'status': 'failed', 'message': 'you have PAWS'}
        return web.Response(text=json.dumps(response_obj), status=500)

app = web.Application()
app.add_routes([web.get('/', main_page),
                web.get('/get_prediction', get_prediction),
                web.post('/registration', registration),
                web.post('/post_prediction', post_prediction)])
logging.basicConfig(level=logging.DEBUG)
web.run_app(app, host='localhost', port=9090)
