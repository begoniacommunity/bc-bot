from datetime import datetime, timedelta

import aiosqlite
from aiogram import html
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

# TO DO: don't hardcode bcID
from main import bcID


class Stats:
    def __init__(self):
        pass

    async def get(self, *args):
        response = await self._process_message(*args)
        return response

    async def log(self, *args):
        response = await self._log_message(*args)
        return response

    def _get_reply_markup(self, day=False, week=False, month=False):
        buttons = []
        if day:
            buttons.append(InlineKeyboardButton(text="🕒 За день", callback_data='day'))
        if week:
            buttons.append(InlineKeyboardButton(text="🕒 За неделю", callback_data='week'))
        if month:
            buttons.append(InlineKeyboardButton(text="🕒 За месяц", callback_data='month'))

        return InlineKeyboardMarkup(inline_keyboard=[buttons])

    async def _get_stats(self, days: int, users_limit: int) -> tuple:
        async with aiosqlite.connect('./static/msg_stats.db') as db:
            cursor = await db.cursor()
            now = datetime.utcnow()
            time = (now - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')

            await cursor.execute(
                'SELECT user_id, COUNT(*) AS msg_count FROM messages WHERE timestamp > ? GROUP BY user_id ORDER BY msg_count DESC LIMIT ?',
                (time, users_limit)
            )
            stats = zip(*await cursor.fetchall())

            await cursor.execute(
                'SELECT COUNT(*) FROM messages WHERE timestamp > ?',
                (time,)
            )
            total = (await cursor.fetchone())[0]

            return stats, total

    async def _log_message(self, message: Message) -> None:
        async with aiosqlite.connect('./static/msg_stats.db') as db:
            user_id = message.from_user.id
            timestamp = message.date.strftime('%Y-%m-%d %H:%M:%S')

            await db.execute(
                'INSERT INTO messages (user_id, timestamp) VALUES (?, ?)',
                (user_id, timestamp),
            )
            await db.commit()

    async def _process_list(self, days: int, message: Message) -> tuple:
        # 10 users by default
        stats = await self._get_stats(days, 10)
        ids, counts = stats[0]
        total = stats[1]

        names = []
        for user_id in ids:
            try:
                user = await message.bot.get_chat_member(bcID, user_id)
                names.append(user.user.full_name)
            # Doesn't work rarely for some reason, append user_id instead
            except TelegramBadRequest:
                print("ERROR: Bad Request: user not found")
                names.append(user_id)

        stats_list = []
        for position, (name, user_id, msg_count) in enumerate(zip(names, ids, counts), 1):
            if isinstance(name, str):
                stats_list.append(
                    f"{position}. "
                    + html.link(
                        html.quote(name),
                        f"tg://openmessage?user_id={user_id}"
                    )
                    + f" – {msg_count}"
                )
            else:
                stats_list.append(
                    f"{position}. "
                    + html.code(name)
                    + f" – {msg_count}"
                )

        return stats_list, total

    async def _process_message(self, message: Message, call: CallbackQuery) -> tuple:
        # 1 day by default
        days = 1
        period = "день"

        reply_markup = self._get_reply_markup(week=True, month=True)

        if call:
            if call.data == 'week':
                days = 7
                period = "неделю"
                reply_markup = self._get_reply_markup(day=True, month=True)
            elif call.data == 'month':
                days = 30
                period = "месяц"
                reply_markup = self._get_reply_markup(day=True, week=True)

            stats = await self._process_list(days, call.message)
        else:
            stats = await self._process_list(days, message)

        message_list = "\n".join(stats[0])
        total = "".join(str(stats[1]))

        stats_message = (
            f"<b>📊 Сообщения за {period}</b>"
            + "\n\n"
            + f"{message_list}"
            + "\n\n"
            + f"<b>Всего сообщений — {total}</b>"
        )

        return stats_message, reply_markup
