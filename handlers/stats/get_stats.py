import aiosqlite
from datetime import datetime, timedelta


async def get_stats(days: int, users_limit: int) -> tuple:
    async with aiosqlite.connect('./static/msg_stats.db') as connect:
        curs = await connect.cursor()

        now = datetime.utcnow()
        day_ago = (now - timedelta(days=days)).strftime('%Y-%m-%d %H:%M:%S')

        await curs.execute(
            'SELECT user_id, COUNT(*) AS msg_count FROM messages WHERE timestamp>? GROUP BY user_id ORDER BY msg_count DESC LIMIT ?',
            (day_ago, users_limit)
        )
        all = zip(*await curs.fetchall())

        await curs.execute(
            'SELECT COUNT(*) FROM messages WHERE timestamp>?',
            (day_ago,)
        )
        total = (await curs.fetchone())[0]

        await curs.close()

        return all, total
