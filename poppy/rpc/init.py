# poppy/rpc/init.py

from aiohttp_apispec import (docs, setup_aiohttp_apispec)
from aiohttp import web

def __init__(hub):
    app = web.Application()

    # Hack - comment me out to see if pop decorator handling works
    hub.rpc.init.router.__apispec__ = router.__apispec__

    routes = [
        web.get('/', hub.rpc.init.router),
    ]

    app.add_routes(routes)

    setup_aiohttp_apispec(
        app=app,
        title='Poppy Documentation',
        version='v1',
        swagger_path='/docs',
        url='/docs/swagger.json'
    )

    web.run_app(app,
                host=hub.OPT['poppy']['addr'],
                port=hub.OPT['poppy']['port'])


@docs(
    tags=['router'],
    summary='Get things',
    description='Get things',
)
async def router(hub, request):
    try:
        data = await request.json()
    except:
        data = {}
    if 'ref' in data:
        result = {}
        result['ref'] = await getattr(hub.rpc, data['ref'])(**data.get('kwargs'))
        return web.json_response(result)
    default_text = """example: curl -X GET http://{0}:{1} -d '{{"ref": "math.fib", "kwargs": {{"num": "11"}}}}'\n""".format(
            hub.OPT['poppy']['addr'],
            hub.OPT['poppy']['port']
            )
    return web.Response(text=default_text)
