import re, asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command, Text, ChatTypeFilter, IDFilter
from aiogram.dispatcher import FSMContext
from aiogram.types.chat import ChatType
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ContentTypes
from aiogram.utils import executor

from static.tokens import *
from handlers import *

# A blank http page via aiohttp
HTTP_SERVER=False

if HTTP_SERVER:
    from keepalive import *

async def main():
    bot = Bot(token=TELEGRAM_TOKEN)
    dp = Dispatcher(bot)

    dp.message_handlers.once = False
    dp.register_message_handler(alo, Command("alo"))
    dp.register_message_handler(cum, Command("cum"))
    dp.register_message_handler(stats, Command("stats"), ChatTypeFilter(chat_type=ChatType.PRIVATE) | IDFilter(chat_id=-1001474397357))
    dp.register_message_handler(log_message, IDFilter(chat_id=-1001474397357), lambda message: not message.text.startswith('/'))
    dp.register_message_handler(convert_currency, IDFilter(chat_id=-1001474397357))
    dp.register_callback_query_handler(delete_currency_message, IDFilter(chat_id=-1001474397357))

    await dp.start_polling()
    if HTTP_SERVER:
        web.run_app(app)
    await dp.idle()

if __name__ == '__main__':
    asyncio.run(main())
