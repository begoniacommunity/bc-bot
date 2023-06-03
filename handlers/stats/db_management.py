import aiosqlite
import asyncio

async def create_table():
    async with aiosqlite.connect('./static/msg_stats.db') as connect: # добавил async и with
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

asyncio.run(create_table())
