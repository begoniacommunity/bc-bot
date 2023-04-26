import aiohttp
from datetime import datetime, timedelta

from main import EXCHANGERATES_TOKEN

cache = {}

async def get_rates(base_currency):
    now = datetime.now()
    if base_currency in cache:
        rates, timestamp = cache[base_currency]
        if now - timestamp < timedelta(hours=24):
            return rates

    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATES_TOKEN}/latest/{base_currency}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data['result'] == 'success':
                    rates = data['conversion_rates']
                    cache[base_currency] = (rates, now)
                    return rates
            else:
                print(f'ERROR: Failed to get rates for {base_currency}. Status code: {response.status}')
    return None