from aiogram import html
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from handlers.pidor import db


async def pidorstats(message: Message) -> None:
    try:
        stats = await db.get_pidor_usage_stats(message.chat.id)
    except Exception:
        stats = None

    if not stats:
        await message.reply("<b>Недостаточно данных. Попробуйте позже.</b>")
        return

    async def get_username(user_id: int) -> str:
        try:
            member = await message.bot.get_chat_member(message.chat.id, user_id)
            if member.user.username is not None:
                name = html.quote(member.user.username)
                mention = f"@{html.quote(name)}"
            else:
                name = html.quote(member.user.first_name)
        except TelegramBadRequest:
            name = user_id  # In worst case, use the user_id
        finally:
            try:
                mention
            except NameError:  # User does not have a username
                mention = f'<a href="tg://user?id={user_id}">{name}</a>'

        return mention

    text = "<b>Статистика пидоров за последний год:</b>\n"
    for entry in stats:
        text += html.bold(await get_username(entry['user_id'])) + " - " + html.italic(entry['number_of_occurrences'])

    await message.answer(text)
