from aiogram import html
from aiogram.types import CallbackQuery


async def delete_currency_message(call: CallbackQuery) -> None:
    if call.data == 'delete':
        user_name = call.from_user.username
        user_id = call.from_user.id

        await call.message.edit_text(
            text=f"{call.message.text}\n\n{html.bold('– удалил(-а)')} @{html.quote(user_name)} ({html.code(user_id)})."
        )

        await call.message.delete()
