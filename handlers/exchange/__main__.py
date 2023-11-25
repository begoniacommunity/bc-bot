import aiohttp
from aiogram import html
from aiogram.types import Message
from aiogram.filters import CommandObject
from bs4 import BeautifulSoup

from .currency_emojis import *
from .default_pairs import *

async def exchange(message: Message, command: CommandObject):
    args = command.args
    if args:
        args = args.split()
        if len(args) == 2:
            currency1 = args[0].lower()
            currency2 = args[1].lower()
            url = f"https://www.investing.com/currencies/{currency1}-{currency2}"
            msg = await message.reply(html.bold('🚀 Получение данных...'))
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as response:
                    if response.status == 200:
                        page = await response.text()
                        soup = BeautifulSoup(page, "html.parser")
                        rate = soup.select_one('[data-test="instrument-price-last"]').text
                        rate = parse(rate)
                        await msg.edit_text(
                            html.bold(
                                f'{currency_emojis.get(currency1.upper(), "")} {currency1.upper()} / {currency_emojis.get(currency2.upper(), "")} {currency2.upper()}: {rate}'
                            )
                        )
                    else:
                        await msg.edit_text(
                            html.bold(
                                '⚠️ Не удалось получить данные. Попробуйте позже или проверьте правильность введенных валют.'
                            )
                        )
        else:
            await message.reply(
                html.bold('🚫 Укажите две валюты через пробел после команды.')
            )
    else:
        msg = await message.reply(
            html.bold(f'🚀 Получение данных... [0/{len(default_pairs)}]')
        )
        result = ''
        async with aiohttp.ClientSession() as session:
            for i, pair in enumerate(default_pairs):
                currency1, currency2 = pair.split('-')
                url = f"https://www.investing.com/currencies/{pair}"
                msg_pair = pair.upper().replace('-', '/')
                async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as response:
                    if response.status == 200:
                        page = await response.text()
                        soup = BeautifulSoup(page, "html.parser")
                        rate = soup.select_one('[data-test="instrument-price-last"]').text
                        rate = parse(rate)
                        result += html.bold(
                            f'{currency_emojis.get(currency1.upper(), "")} {currency1.upper()} / {currency_emojis.get(currency2.upper(), "")} {currency2.upper()}: {rate}\n'
                        )
                    else:
                        result += html.bold(
                            f'{currency_emojis.get(currency1.upper(), "")} {currency1.upper()} / {currency_emojis.get(currency2.upper(), "")} {currency2.upper()}: ⚠️\n'
                        )
                await msg.edit_text(
                    html.bold(f'🚀 Получение данных... [{i + 1}/{len(default_pairs)}]')
                )
        await msg.edit_text(result)

def parse(rate: str) -> str:
    # Strip to two decimal places
    rate = '{:.2f}'.format(float(rate))
    # Convert to russian formatting standard
    rate = rate.replace(',', ' ').replace('.', ',')

    return rate
