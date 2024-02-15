import platform
import sys
from datetime import datetime, timedelta
import aiohttp
import asyncio


class HttpError(Exception):
    pass


async def request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result
                else:
                    raise HttpError(f"Error status: {resp.status} for {url}")
        except (aiohttp.ClientConnectorError, aiohttp.InvalidURL) as err:
            raise HttpError(f'Connection error: {url}', str(err))


async def main(num_days):

    if num_days > 10:
        num_days = 10
        print('You can see only 10 days')

    results = []
    for i in range(1, num_days + 1):
        d = datetime.now() - timedelta(days=i)
        shift = d.strftime("%d.%m.%Y")
        try:
            response = await request('https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=5')
            responce_data = {}
            for data in response:
                ccy = data.get('ccy')
                sale = float(data.get('sale', 0))
                purchase = float(data.get('buy', 0))
                responce_data[ccy] = {'sale': sale, 'purchase': purchase}
            results.append({shift: responce_data})
        except HttpError as err:
            print(err)
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: py .\main.py <number_of_days>")
    else:
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        # print(sys.argv)
        r = asyncio.run(main(int(sys.argv[1])))
        print(r)






























# async def main():
#
#     async with aiohttp.ClientSession() as session:
#         async with session.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5') as response:
#
#             print("Status:", response.status)
#             print("Content-type:", response.headers['content-type'])
#             print('Cookies: ', response.cookies)
#             print(response.ok)
#             result = await response.json()
#             return result
#
#
# if __name__ == "__main__":
#     if platform.system() == 'Windows':
#         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#     r = asyncio.run(main())
#     print(r)
