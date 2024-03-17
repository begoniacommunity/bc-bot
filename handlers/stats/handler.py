import re

from aiogram import html
from aiogram.types import CallbackQuery, Message

from .stats import Stats


async def stats_command(message: Message) -> None:
    wait_msg = await message.answer(
        html.bold("🔄 Обработка данных...")
    )

    stats = Stats()
    stats = await stats.get(message, None)
    msg = "".join(stats[0])
    reply_markup = stats[1]

    await wait_msg.edit_text(
        msg,
        reply_markup=reply_markup,
    )


async def stats_callback(call: CallbackQuery) -> None:
    wait_msg = call.message.text
    reply_markup = call.message.reply_markup

    wait_msg = re.sub(
        r"📊 Сообщения за \w+",
        html.bold("🔄 Обработка данных..."),
        wait_msg,
    )
    wait_msg = re.sub(
        r"(\d+)\. .+ – \d+",
        r"\1. ...",
        wait_msg,
    )
    wait_msg = re.sub(
        r"Всего сообщений — \d+",
        html.bold("Всего сообщений — ?"),
        wait_msg,
    )

    await call.message.edit_text(
        wait_msg,
    )

    stats = Stats()
    stats = await stats.get(None, call)
    msg = "".join(stats[0])
    reply_markup = stats[1]

    await call.message.edit_text(
        msg,
        reply_markup=reply_markup,
    )
