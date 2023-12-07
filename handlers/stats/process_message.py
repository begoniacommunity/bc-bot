from aiogram import html
from aiogram.types import (
    CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
)

from .process_list import *


async def process_message(message: Message, call: CallbackQuery) -> tuple:
    # Default is 1 day
    days = 1
    period = "сутки"

    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="🕒 За неделю", callback_data="week"),
            InlineKeyboardButton(
                text="🕒 За месяц", callback_data="month"),
        ]]
    )
    if call:
        if call.data == "back":
            pass
        else:
            reply_markup = InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(
                        text="⬅️ Назад", callback_data="back"),
                ]]
            )

            if call.data == "week":
                days = 7
                period = "неделю"
            if call.data == "month":
                days = 30
                period = "месяц"

        stats = await process_list(days, period, call.message)
    else:
        stats = await process_list(days, period, message)

    message_list = "\n".join(stats[0])
    total = "".join(str(stats[1]))

    stats_message = (
        html.bold(f"📊 Сообщения за {period}") + "\n\n"
        + message_list +
        "\n\n" + html.bold(f"Всего сообщений – {total}")
    )

    return stats_message, reply_markup
