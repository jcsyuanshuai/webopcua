from aiohttp import web
from asyncua import Node, Client

from core.ua import AsyncUaClient


class NodeSearcher:

    def __init__(self, cli):
        self.cli = cli

    async def search_by_nid(self, nid) -> Node:
        await self.cli.connect()
        node = self.cli.get_node(nid)
        return node

    async def search_by_chain(self, paths: [str]) -> Node:
        uri = 'http://examples.freeopcua.github.io'
        idx = await self.cli.get_namespace_index(uri)
        paths = ['0:Objects', '2:MyObject', '2:MyVariable']
        await self.cli.connect()
        node = await self.cli.nodes.root.get_child(paths)
        return node

    async def search(self):
        pass


class SubHandler:
    def datachange_notification(self, node, val, data):
        print(node, val, data)

    def event_notification(self, event):
        pass


class Subscriber:
    pass


class WsSubHandler(SubHandler):
    def __init__(self, ws: web.WebSocketResponse, cli: AsyncUaClient):
        self.ws = ws
        self.cli = cli

    async def datachange_notification(self, node, val, data):
        try:
            if not self.ws.closed:
                await self.ws.send_str(str(val))
            else:
                return
        except ConnectionResetError as e:
            print(e)


class WsSubscriber:

    def __init__(self, url, ws: web.WebSocketResponse):
        url = 'opc.tcp://localhost:4840/freeopcua/server/'
        self.url = url
        self.ws = ws
        self.client = Client(self.url)
        self.searcher = NodeSearcher(self.client)
        self.handler = WsSubHandler(ws)

    async def subscribe_by_nid(self, nid):
        sub = await self.client.create_subscription(500, self)
        node = await self.searcher.search_by_nid(nid)
        self.client.sub
        await sub.subscribe_data_change(node)

    async def subscribe_by_paths(self, paths):
        sub = await self.client.create_subscription(500, self)
        node = await self.searcher.search_by_chain(paths)
        await sub.subscribe_data_change(node)
