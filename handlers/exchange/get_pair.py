import aiohttp
from bs4 import BeautifulSoup


async def get_pair(pair: str) -> str:
    url = f"https://www.investing.com/currencies/{pair}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as response:
            if response.status == 200:
                page = await response.text()
                soup = BeautifulSoup(page, "html.parser")
                rate = soup.select_one(
                    '[data-test="instrument-price-last"]'
                ).text

                return rate
