import aiosqlite
import asyncio
from datetime import datetime, timedelta


# Create an new database if not exists
async def create_table() -> None:
    async with aiosqlite.connect('./static/msg_stats.db') as connect:
        curs = await connect.cursor()

        await curs.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                timestamp TEXT
            )
        ''')
        await connect.commit()

        await curs.close()


# Remove old stats database records
async def delete_old_records() -> None:
    month_ago = datetime.now() - timedelta(days=30)
    date_str = month_ago.strftime("%Y-%m-%d")

    async with aiosqlite.connect('./static/msg_stats.db') as connect:
        curs = await connect.cursor()

        await curs.execute('''
            DELETE FROM messages
            WHERE timestamp < ?
        ''', (date_str,)
        )
        await connect.commit()

        await curs.execute('''
            VACUUM
        ''')
        await connect.commit()

        await curs.close()

asyncio.run(create_table())
asyncio.run(delete_old_records())
