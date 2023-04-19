from aiohttp import web

async def handle(request):
    text = ""
    return web.Response(text=text)

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])