from aiohttp import web
from asyncua import Node, Client


class AsyncUaClient:
    client = None
    connected = False
    sub = None
    sub_res = {}

    def get_node(self, nid) -> Node:
        if not self.client:
            raise "not init client"
        return self.client.get_node(nid)

    async def connect(self, uri):
        self.client = Client(uri)
        try:
            await self.client.connect()
            self.connected = True
        except Exception as e:
            print(e)
        return self

    async def subscribe_data_change(self, node, handler):
        if self.sub is None:
            self.sub = await self.client.create_subscription(500, handler)
        handle = await self.sub.subscribe_data_change(node)
        self.sub_res[node.nodeid] = handle

    async def unsubscribe_data_change(self, node):
        handler = self.sub_res[node.nodeid]
        await self.sub.unsubscribe(handler)


class SubHandler:
    def datachange_notification(self, node, val, data):
        print(node, val, data)

    def event_notification(self, event):
        pass


class WsSubHandler(SubHandler):
    def __init__(self, ws: web.WebSocketResponse, cli: AsyncUaClient):
        self.ws = ws
        self.cli = cli

    async def datachange_notification(self, node: Node, val, data):
        print(node, val, data)
        try:
            if not self.ws.closed:
                await self.ws.send_str(str(val))
            else:
                return
        except ConnectionResetError as e:
            print(e)
