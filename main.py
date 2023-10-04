import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

from static.tokens import *
from handlers import *

async def main():
    bot = Bot(TELEGRAM_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    bcID = -1001474397357
    bcMessageFilter = F.chat.id == bcID
    bcCallbackFilter = F.message.chat.id == bcID

    dp.message.register(alo, Command("alo"))
    dp.message.register(cum, Command("cum"))
    dp.message.register(exchange, Command("exchange"), bcMessageFilter)
    dp.message.register(stats, Command("stats"))
    dp.callback_query.register(delete_currency_message, bcCallbackFilter)

    @dp.message(bcMessageFilter)
    async def non_command(message: Message):
        await log_message(message)
        await convert_currency(message)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
