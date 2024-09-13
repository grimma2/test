import asyncio


users = []


async def saver_every_minute():
    while True:
        await asyncio.sleep(60)

