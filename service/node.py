from aiohttp import web
from asyncua import Client

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
