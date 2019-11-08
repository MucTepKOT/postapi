from aiohttp import web
import json
# import dbquery

async def handle(request):
    response_obj = {'status': 'success'}
    return web.Response(text=json.dumps(response_obj), status=200)


async def predict(request):
    try:
        user_predict = request.query['username', 'scores']
        response_obj = {'status': 'success', 'message': 'your predict accepted'}
        return web.Response(text=json.dumps(response_obj), status=200)
    except Exception as e:
        response_obj = {'status': 'failed', 'message': 'your have PAWS'}
        return web.Response(text=json.dumps(response_obj), status=500)


app = web.Application()
app.add_routes([web.get('/', handle),
                web.post('/predict', predict)])

web.run_app(app, host='localhost', port=9090)
