import pathlib

from aiohttp import web
from dotenv import load_dotenv

base_dir = pathlib.Path(__file__).parent.parent
conf_dir = base_dir / 'conf' / 'prod'
load_dotenv(verbose=True)

hook_arr = []

inst = web.Application()


def add_hook(*funcs) -> None:
    for func in funcs:
        hook_arr.append(func)


def start() -> None:
    for h in hook_arr:
        h()
    web.run_app(inst)


def get_logger():
    return inst.logger


async def context(apx: web.Application) -> None:
    cfg = inst['config']
