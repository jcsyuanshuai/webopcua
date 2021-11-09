from app.services import *
from service.node import routes as node_routers


def setup_routers(inst: web.Application):
    inst.router.add_get('/', index)
    inst.add_routes(node_routers)
