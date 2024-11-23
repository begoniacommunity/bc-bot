from aiogram.types import Message, ReactionTypeEmoji

from handlers.pidor import db


async def pidoreg(message: Message):
    if not await db.is_pidor(message.chat.id, message.from_user.id):
        await db.pidoreg(message.chat.id, message.from_user.id)
        await message.react([ReactionTypeEmoji(emoji="👌")])
    else:
        await message.reply("<b>Вы уже зарегистрированы в игре!</b>")
