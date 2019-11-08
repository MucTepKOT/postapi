from aiohttp import web

async def hello(request):
    data = {'response': 'Hi, this is my first api'}
    return web.json_response(data)
async def post(request):
    data = {'Status': 'Success'}
    return web.json_response(data)

app = web.Application()
app.add_routes([web.get('/', hello),
                web.post('/post', post)]
                )
web.run_app(app)
