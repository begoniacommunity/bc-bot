from aiogram import html
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from main import bcID
from .get_stats import *


async def process_list(days: int, period: str, message: Message) -> tuple:
    # Default are 10 users
    stats = await get_stats(days, 10)
    ids, counts = stats[0]
    total = stats[1]

    names = []
    for user_id in ids:
        # Chat ID is set to bc filter ID for proper work in DM
        try:
            user = await message.bot.get_chat_member(bcID, user_id)
            names.append(user.user.full_name)
        # Doesn't work rarely for some reason, append the user id in case of exception
        except TelegramBadRequest:
            print("ERROR: Bad Request: user not found")
            names.append(user_id)

    stats_list = []
    for position, (name, user_id, msg_count) in enumerate(zip(names, ids, counts), 1):
        if isinstance(name, str):
            stats_list.append(
                f"{position}. " +
                html.link(
                    html.quote(name),
                    f"tg://openmessage?user_id={user_id}"
                )
                + f" – {msg_count}"
            )
        else:
            stats_list.append(
                f"{position}. " +
                html.code(name)
                + f" – {msg_count}"
            )

    return stats_list, total
