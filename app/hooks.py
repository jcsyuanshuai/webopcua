import logging
import os
from pathlib import Path

import aiosqlite
import yaml

import app
from app import inst
from app.routers import setup_routers


def init_env():
    name = os.getenv('NAME')
    print(f'app name: {name}')
    mode = os.getenv('MODE')
    print(f'app mode: {mode}')
    conf_dir = os.getenv('CONF_DIR')

    if mode not in {'dev', 'test', 'prod'}:
        raise ValueError(f'incorrect MODE value: {mode}')
    if conf_dir is not None and Path(conf_dir).exists():
        inst['conf_dir'] = conf_dir
        print(f'app conf dir: {conf_dir}')
    else:
        inst['conf_dir'] = app.base_dir / 'conf' / mode
        print(f"app conf dir: {inst['conf_dir']}")
    print()


def init_config():
    def get_config(path):
        with open(path) as f:
            config = yaml.safe_load(f)
        return config

    inst['config'] = get_config(inst['conf_dir'] / 'app.yaml')


def init_logger():
    logger = logging.getLogger(__name__)
    inst.logger = logger


def init_router():
    setup_routers(inst)


def init_db():
    cfg = inst['config']
    engine = aiosqlite.connect('test.db')
    inst['db'] = engine
