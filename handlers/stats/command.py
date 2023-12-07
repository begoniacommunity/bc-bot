from aiogram.types import Message, CallbackQuery

from .process_message import *


async def stats(message: Message) -> None:
    result = await process_message(message, None)
    stats = "".join(result[0])
    reply_markup = result[1]

    await message.answer(
        stats,
        reply_markup=reply_markup,
    )


async def stats_callback(call: CallbackQuery) -> None:
    result = await process_message(None, call)
    stats = "".join(result[0])
    reply_markup = result[1]

    await call.message.edit_text(
        stats,
        reply_markup=reply_markup,
    )
