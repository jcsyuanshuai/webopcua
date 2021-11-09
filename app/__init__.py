import pathlib

from aiohttp import web
from aiohttp_swagger import *
from dotenv import load_dotenv

base_dir = pathlib.Path(__file__).parent.parent
load_dotenv(verbose=True)

hook_arr = []

inst = web.Application()
inst['mode'] = 'prod'
inst['name'] = __name__
inst['conf_dir'] = base_dir / 'conf' / inst['mode']


def add_hook(*funcs) -> None:
    for func in funcs:
        hook_arr.append(func)


def start() -> None:
    for h in hook_arr:
        h()
    setup_swagger(inst)
    web.run_app(inst)


def get_logger():
    return inst.logger


async def context(apx: web.Application) -> None:
    cfg = inst['config']
