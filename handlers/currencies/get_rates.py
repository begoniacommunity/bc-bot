import requests
from datetime import datetime, timedelta

from main import EXCHANGERATES_TOKEN

cache = {}

def get_rates(base_currency):
    now = datetime.now()
    if base_currency in cache:
        rates, timestamp = cache[base_currency]
        if now - timestamp < timedelta(hours=24):
            return rates

    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGERATES_TOKEN}/latest/{base_currency}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['result'] == 'success':
            rates = data['conversion_rates']
            cache[base_currency] = (rates, now)
            return rates
    else:
        print(f'ERROR: Failed to get rates for {base_currency}. Status code: {response.status_code}')

    return None