from aiogram.types import Message


async def alo(message: Message) -> None:
    await message.answer('📞 Alo, я на связи')
