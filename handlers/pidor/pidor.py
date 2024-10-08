import asyncio
import random

from aiogram import html
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from handlers.pidor import db

BEGINNING_STRINGS = [
    "Эй, зачем разбудили...",
    "### RUNNING 'TYPIDOR.SH'...",
    "Инициирую поиск пидора дня...",
    "Зачем вы меня разбудили...",
    "Woop-woop! That's the sound of da pidor-police!",
    "Осторожно! <b>Пидор дня</b> активирован!"
]
PROCESS_STRINGS = [
    "Хм...",
    "* fxaura пукнул"
    "Высокий приоритет мобильному юниту.",
    "Доступ получен. Аннулирование протокола.",
    "Где-же он...",
    "В этом совершенно нет смысла...",
    "Так, что тут у нас?",
    "<i>Ведётся поиск в базе данных</i>",
    "<i>Интересно...</i>",
    "Система взломана. Нанесён урон. Запущено планирование контрмер."
    "<i>(Ворчит)</i> А могли бы на работе делом заниматься",
    "Проверяю данные..."

]
FINAL_STRINGS = [
    "Няшный <b>пидор дня</b> - ",
    "Кажется, <b>пидор дня</b> - ",
    "Ну ты и <b>пидор</b>, ",
    "<b>Пидор дня</b> обыкновенный, 1шт. - ",
    "Согласно моей информации, по результатам сегодняшнего розыгрыша <b>пидор дня</b> - "
]


async def pidor(message: Message) -> None:
    if not await db.can_use_pidor(message.chat.id):
        await message.reply("<b>Искать пидора можно только раз в день!</b>")
        return

    pidors = await db.get_pidors(message.chat.id)
    if not pidors:
        await message.reply("<b>Никто не зарегистрирован в игре. Зарегистрироваться -</b> /pidoreg")
        return
    pidor_id = random.choice(pidors)

    try:
        member = await message.bot.get_chat_member(message.chat.id, pidor_id)
        if member.user.username is not None:
            name = html.quote(member.user.username)
            mention = f"@{html.quote(name)}"
        else:
            name = html.quote(member.user.first_name)
    except TelegramBadRequest:
        name = pidor_id  # In worst case, use the user_id
    finally:
        try:
            mention
        except NameError:  # User does not have a username
            mention = f'<a href="tg://user?id={pidor_id}">{name}</a>'

    await message.answer(random.choice(BEGINNING_STRINGS))
    await asyncio.sleep(3)
    await message.answer(random.choice(PROCESS_STRINGS))
    await asyncio.sleep(3)
    await message.answer(random.choice(PROCESS_STRINGS))
    await asyncio.sleep(3)
    await message.answer(random.choice(FINAL_STRINGS) + mention)

    await db.mark_as_used_pidor(message.chat.id)
