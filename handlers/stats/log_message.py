from aiogram import types
import aiosqlite

async def log_message(message: types.Message):
    async with aiosqlite.connect('./static/msg_stats.db') as connect:
        curs = await connect.cursor()

        user_id = message.from_user.id
        timestamp = message.date.strftime('%Y-%m-%d %H:%M:%S')
        await curs.execute('INSERT INTO messages (user_id, timestamp) VALUES (?, ?)', (user_id, timestamp))
        await connect.commit()

        await curs.close()