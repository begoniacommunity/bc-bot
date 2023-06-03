from datetime import datetime, timedelta
from aiogram import types
import aiosqlite

async def stats(message: types.Message):
    async with aiosqlite.connect('./static/msg_stats.db') as connect:
        curs = await connect.cursor()

        now = datetime.utcnow()
        day_ago = (now - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        week_ago = (now - timedelta(weeks=1)).strftime('%Y-%m-%d %H:%M:%S')
        month_ago = (now - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')

        await curs.execute('SELECT COUNT(*) FROM messages WHERE timestamp>?', (day_ago,))
        day_count = (await curs.fetchone())[0]
        await curs.execute('SELECT COUNT(*) FROM messages WHERE timestamp>?', (week_ago,))
        week_count = (await curs.fetchone())[0]
        await curs.execute('SELECT COUNT(*) FROM messages WHERE timestamp>?', (month_ago,))
        month_count = (await curs.fetchone())[0]
        await message.answer(f'📊 Статистика по сообщениям:\n\n- 🕐 За день: {day_count}\n- 🕒 За неделю: {week_count}\n- 🕔 За месяц: {month_count}')

        await curs.close()
