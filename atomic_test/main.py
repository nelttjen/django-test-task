import asyncio
import aiohttp


count = 0
total = 200


async def send(session):
    global count
    try:
        async with session.get('http://127.0.0.1:8000/api/v1/chapters/1/') as response:
            result = await response.json()
            print(result)
    finally:
        count += 1


async def func():
    async with aiohttp.ClientSession() as session:
        for i in range(total):
            asyncio.create_task(send(session))
            # await asyncio.sleep(0.001)
        while count != total:
            await asyncio.sleep(1)


if __name__ == '__main__':
    event_loop = asyncio.new_event_loop()
    event_loop.create_task(func())
    asyncio.set_event_loop(event_loop)
    event_loop.run_until_complete(asyncio.gather(*asyncio.all_tasks(event_loop)))




