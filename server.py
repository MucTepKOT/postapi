import logging
from aiohttp import web
import json

async def handle(request):
    response_obj = {'status': 'success'}
    return web.Response(text=json.dumps(response_obj), status=200)

async def predict(request):
    try:
        user_predict = await request.json()  # get json-like body
        # print(user_predict['username'])
        # print(user_predict['scores'])
        if 'username' in user_predict and 'scores' in user_predict and len(user_predict) == 2:
            print(user_predict['username'], user_predict['scores'])
            response_obj = {'status': 'accepted', 'message': 'your predict accepted'}
            return web.Response(text=json.dumps(response_obj), status=202)
        else:
            response_obj = {'status': 'error', 'message': 'put it into your ass pls'}
            return web.Response(text=json.dumps(response_obj), status=400)
    except Exception as e:
        response_obj = {'status': 'failed', 'message': 'your have PAWS'}
        return web.Response(text=json.dumps(response_obj), status=500)

app = web.Application()
app.add_routes([web.get('/', handle),
                web.post('/predict', predict)])
logging.basicConfig(level=logging.DEBUG)
web.run_app(app, host='localhost', port=9090)
