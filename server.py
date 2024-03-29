# -*- encoding: utf-8 -*-
import logging
from aiohttp import web
import json
import mongo
import postgresql
import keygen

async def main_page(request):
    header = request.headers
    if 'Name' in header:
        user = header['Name']
        token = keygen.hashText(header['Name'])
        postgresql.create_user(user, token)
        response_obj = {'your token': str(token)}
        return web.Response(text=json.dumps(response_obj), status=200)
    else:
        response_obj = {'status': 'message_error', 'message': 'give me your Name'}
        return web.Response(text=json.dumps(response_obj), status=400)

async def check(request):
    header = request.headers
    if 'Name' and 'Auth' in header:
        name = header['Name']
        token = header['Auth']
        db_token = postgresql.check_user(name)
        if token == db_token[0]:
            response_obj = {'predictions' : mongo.my_prediction(name)}
            return web.Response(text=json.dumps(response_obj), status=200)
        else:
            response_obj = {'status': 'auth_error', 'message': 'ti cho psina, kuda polez?'}
            return web.Response(text=json.dumps(response_obj), status=401)
    else:
        response_obj = {'status': 'message_error', 'message': 'incorrect parametres'}
        return web.Response(text=json.dumps(response_obj), status=400)

async def predict(request):
    try:
        user_predict = await request.json()  # get json-like body
        header = request.headers
        if 'Name' and 'Auth' in header:
            name = header['Name']
            token = header['Auth']
            db_token = postgresql.check_user(name)
            if db_token == None:
                response_obj = {'status': 'auth_error', 'message': 'ti cho psina, kuda polez?'}
                return web.Response(text=json.dumps(response_obj), status=401)
            else:
                if token == db_token[0]:
                    if 'username' and 'scores' in user_predict and len(user_predict) == 2:
                        data = user_predict
                        inserting = mongo.insert_db(name, data)
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
                web.get('/my_prediction', check),
                web.post('/do_predict', predict)])
logging.basicConfig(level=logging.DEBUG)
web.run_app(app, host='localhost', port=9090)
