from app.services import *
from service import node


def setup_routers(inst: web.Application):
    inst.router.add_get('/', index)
    inst.add_routes(node.routes)
