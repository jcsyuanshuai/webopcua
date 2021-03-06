import os
from pathlib import Path

import aiosqlite
import yaml

from app import inst, base_dir
from app.routers import setup_routers


def init_env():
    name = os.getenv('NAME')
    mode = os.getenv('MODE')
    conf_dir = os.getenv('CONF_DIR')

    if name is not None:
        inst['name'] = name

    if mode is not None and mode in {'dev', 'test', 'prod'}:
        inst['mode'] = mode

    if conf_dir is not None and Path(conf_dir).exists():
        inst['conf_dir'] = conf_dir
    else:
        inst['conf_dir'] = base_dir / 'conf' / inst['mode']

    print(f'app name: {inst["name"]}')
    print(f'app mode: {inst["mode"]}')
    print(f"app conf dir: {inst['conf_dir']}")
    print()


def init_config():
    def get_config(path):
        with open(path) as f:
            config = yaml.safe_load(f)
        return config

    inst['config'] = get_config(inst['conf_dir'] / 'app.yaml')


def init_logger():
    # logging.basicConfig(level=logging.DEBUG)
    pass


def init_router():
    setup_routers(inst)


def init_db():
    cfg = inst['config']
    engine = aiosqlite.connect('test.db')
    inst['db'] = engine


def init_middleware():
    async def close_sockets(ap):
        for ws in ap['wss']:
            await ws.close()

    inst.on_shutdown.append(close_sockets)


def init_websocket():
    inst['wss'] = []
