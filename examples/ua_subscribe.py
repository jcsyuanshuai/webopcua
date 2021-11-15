import asyncio

from core.core import SubHandler
from core.ua import AsyncUaClient


async def main():
    ua = AsyncUaClient()
    uri = 'opc.tcp://0.0.0.0:4840/freeopcua/server/'
    await ua.connect(uri)
    node = ua.get_node('ns=2;i=2')
    handler = SubHandler()
    await ua.subscribe_data_change(node, handler)
    i = 0
    while i < 10:
        await asyncio.sleep(1)
        i += 1

    await ua.unsubscribe_data_change(node)


if __name__ == '__main__':
    asyncio.run(main())
