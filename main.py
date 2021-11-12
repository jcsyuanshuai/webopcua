import app
from app.hooks import *

if __name__ == '__main__':
    app.add_hook(
        init_env,
        init_config,
        init_logger,
        init_router,
        init_db,
        init_middleware,
        init_websocket,
    )
    app.start()
