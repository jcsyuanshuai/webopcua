import aiohttp
from aiohttp import web
from asyncua import Client, Node

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
    try:
        req.app['wss'].append(ws)
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    WsSubscriber(ws)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())

        return ws
    finally:
        print('websocket connection closed')
        req.app['wss'].remove(ws)


class NodeSearcher:
    cli = None

    def __init__(self, url):
        self.cli = Client(url)

    def search_by_nid(self, nid):
        pass

    def search_by_chain(self, chain):
        pass


class WsSubscriber:
    url = 'opc.tcp://localhost:4840/freeopcua/server/'

    def __init__(self, ws: web.WebSocketResponse):
        self.ws = ws

    async def get_node(self) -> Node:
        client = Client(url=self.url)
        await client.connect()
        uri = 'http://examples.freeopcua.github.io'
        idx = await client.get_namespace_index(uri)
        node = await client.nodes.root.get_child(
            ["0:Objects", f"{idx}:MyObject", f"{idx}:MyVariable"])
        return node
        sub = await client.create_subscription(500, self)
        await sub.subscribe_data_change(node)

    async def datachange_notification(self, node, val, data):
        await self.ws.send_str(val)

    def event_notification(self, event):
        pass
