import asyncio

from core.ua import AsyncUaClient
from core.ua import SubHandler


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


# def sync_main():
#     ua = SyncUaClient()
#     uri = 'opc.tcp://0.0.0.0:4840/freeopcua/server/'
#     ua.connect(uri)
#     node = ua.get_node('ns=2;i=2')
#     print(node)
#     handler = SubHandler()
#     ua.subscribe_data_change(node, handler)
#
#     while True:
#         time.sleep(1)
#
#     # ua.unsubscribe_data_change(node)


if __name__ == '__main__':
    asyncio.run(main())
    # sync_main()
