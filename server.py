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
    if 'Auth' in header:
        response_obj = {'status': 'OK'}
        return web.Response(text=json.dumps(response_obj), status=200)
    else:
        response_obj = {'status': 'auth_error', 'message': 'ti cho psina, kuda polez?'}
        return web.Response(text=json.dumps(response_obj), status=401)

async def predict(request):
    try:
        user_predict = await request.json()  # get json-like body
        header = request.headers
        if 'Auth' in header:
            if 'username' and 'scores' in user_predict and len(user_predict) == 2:
                response_obj = {'status': 'accepted', 'message': 'your predict accepted'}
                return web.Response(text=json.dumps(response_obj), status=202)
            else:
                response_obj = {'status': 'message_error', 'message': 'pls post it into your ass'}
                return web.Response(text=json.dumps(response_obj), status=400)
        else:
            response_obj = {'status': 'auth_error', 'message': 'ti cho psina, kuda polez?'}
            return web.Response(text=json.dumps(response_obj), status=401)
    except Exception as e:
        print(e)
        response_obj = {'status': 'failed', 'message': 'you have PAWS'}
        return web.Response(text=json.dumps(response_obj), status=500)

app = web.Application()
app.add_routes([web.get('/', main_page),
                web.get('/my', check),
                web.post('/predict', predict)])
logging.basicConfig(level=logging.DEBUG)
web.run_app(app, host='localhost', port=9090)
