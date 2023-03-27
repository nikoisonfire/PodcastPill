import aiohttp
import asyncio

url = ["https://google.de", "https://yahoo.de"]

async def get(url, session):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        print(e)

async def main():
    async with aiohttp.ClientSession() as session:
        html = await asyncio.gather(*[get(u, session) for u in url])
        print(html)

asyncio.run(main())