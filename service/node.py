import aiohttp
from aiohttp import web
from asyncua import Client

from core.ua import AsyncUaClient
from core.ua import WsSubHandler
from service import Ok

routes = web.RouteTableDef()


@routes.get('/node/all')
async def all_nodes(req: web.Request) -> web.Response:
    """

    :param req:
    :return: Ok
    ---
    description: This is todo
    tags:
    - Health check
    produces:
    - application/json
    """
    # url = req.match_info.get("url")
    # log = app.get_logger()
    # log.info('>>>>>>>>>>>>>>>>>>>>>' + url)
    cli = Client(url='opc.tcp://localhost:4840/freeopcua/server/')
    # uri = 'http://examples.freeopcua.github.io'
    # idx = await cli.get_namespace_index(uri)
    nodes = cli.get_root_node()
    return web.json_response(Ok("this is test").to_json())


@routes.get('/node/{id}')
async def all_nodes(req: web.Request) -> web.Response:
    return web.json_response(Ok())


@routes.get('/ws')
async def subscribe(req: web.Request) -> web.WebSocketResponse:
    ws = web.WebSocketResponse()
    await ws.prepare(req)
    await ws.send_str('connect success')
    ua = AsyncUaClient()
    uri = 'opc.tcp://0.0.0.0:4840/freeopcua/server/'
    await ua.connect(uri)
    node = ua.get_node('ns=2;i=2')
    handler = WsSubHandler(ws, ua)
    await ua.subscribe_data_change(node, handler)

    try:
        req.app['wss'].append(ws)

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    await ws.ping()
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())
        return ws
    finally:
        print('websocket connection closed')
        await ua.unsubscribe_data_change(node)
        req.app['wss'].remove(ws)
