from aiohttp import web
from asyncua import Client


async def index(req: web.Request) -> web.Response:
    return web.Response(text='hello')


async def discover(req: web.Request) -> web.Response:
    
    return web.Response(text='')


async def subscribe():
    async with Client(url='opc.tcp://localhost:4840/freeopcua/server/') as cli:
        # logger.info("children of root: %r", await cli.nodes.root.get_children())
        while True:
            uri = 'http://examples.freeopcua.github.io'
            idx = await cli.get_namespace_index(uri)
            var = await cli.nodes.root.get_child(
                ['0:Objects', f'{idx}:MyObject', f'{idx}:MyVariable'],
            )
            print(var)
