from aiogram.types import CallbackQuery, ParseMode

async def delete_currency_message(call: CallbackQuery):
    if call.data == 'delete':
        user_name = call.from_user.username
        user_id = call.from_user.id

        await call.message.edit_text(
            text=f"{call.message.text}\n\n\* удалил @{user_name} (`{user_id}`).",
            parse_mode=ParseMode.MARKDOWN
        )

        await call.message.delete()
