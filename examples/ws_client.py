import asyncio

import aiohttp
from aiohttp import ClientSession


async def main():
    session = ClientSession()
    async with session.ws_connect('http://127.0.0.1:8080/ws') as ws:
        async for msg in ws:
            print(msg.data)
            # await asyncio.sleep(1)
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close cmd':
                    await ws.close()
                    break
                else:
                    await ws.send_str('msg from client\n')
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break


if __name__ == '__main__':
    asyncio.run(main())
