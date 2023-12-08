from aiogram import html
from aiogram.types import CallbackQuery


async def delete_currency_message(call: CallbackQuery) -> None:
    username = call.from_user.username
    user_id = call.from_user.id

    await call.message.edit_text(
        f"{call.message.text}"
        "\n\n"
        f"{html.bold('– удалил(-а)')} @{html.quote(username)} ({html.code(user_id)})."
    )

    await call.message.delete()
