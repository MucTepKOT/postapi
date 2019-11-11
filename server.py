import logging
from aiohttp import web
import json

async def handle(request):
    response_obj = {'status': 'success'}
    return web.Response(text=json.dumps(response_obj), status=200)

async def predict(request):
    try:
        r_json = await request.json()  # get json-like body
        print(r_json['username'], r_json['scores'])

        headers = request.headers  # get headers from request
        print(headers['content_type'])

        response_obj = {'status': 'success', 'message': 'your predict accepted'}
        return web.Response(text=json.dumps(response_obj), status=200)
        # return web.Response(text=str(x), status=200)
    except Exception as e:
        response_obj = {'status': 'failed', 'message': 'your have PAWS'}
        return web.Response(text=json.dumps(response_obj), status=500)

app = web.Application()
app.add_routes([web.get('/', handle),
                web.post('/predict', predict)])
logging.basicConfig(level=logging.DEBUG)
web.run_app(app, host='localhost', port=9090)
