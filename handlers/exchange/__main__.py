import aiohttp
from aiogram import html
from aiogram.types import Message
from aiogram.filters import CommandObject
from bs4 import BeautifulSoup

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
                        rate = rate.replace(',', ' ').replace('.', ',')
                        await msg.edit_text(html.bold(f'💸 {currency1.upper()}/{currency2.upper()}: {rate}'))
                    else:
                        await msg.edit_text(html.bold('⚠️ Не удалось получить данные. Попробуйте позже или проверьте правильность введенных валют.'))
        else:
            await message.reply(html.bold('🚫 Укажите две валюты через пробел после команды.'))
    else:
        await message.reply(html.bold('🚫 Не указаны валюты.'))
