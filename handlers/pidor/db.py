import datetime
from typing import List

import aiosqlite


async def create_pidors_database() -> None:
    async with aiosqlite.connect('./data/pidors.db') as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS pidors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS pidor_uses (
                chat_id INTEGER PRIMARY KEY,
                timestamp INTEGER NOT NULL 
            )
        """)
        await db.commit()


async def is_pidor(chat_id: int, user_id: int) -> bool:
    async with aiosqlite.connect('./data/pidors.db') as db:
        cursor = await db.execute(
            "SELECT * FROM pidors WHERE chat_id=? AND user_id=?",
            (chat_id, user_id),
        )
        result = await cursor.fetchone()
        if not result:
            return False
        return True


async def pidoreg(chat_id: int, user_id: int) -> None:
    async with aiosqlite.connect('./data/pidors.db') as db:
        await db.execute(
            "INSERT INTO pidors (chat_id, user_id) VALUES (?, ?)",
            (chat_id, user_id),
        )
        await db.commit()


async def pidounreg(chat_id: int, user_id: int) -> None:
    async with aiosqlite.connect('./data/pidors.db') as db:
        await db.execute(
            "DELETE FROM pidors WHERE chat_id=? AND user_id=?",
            (chat_id, user_id),
        )
        await db.commit()


async def get_pidors(chat_id: int) -> List[int]:
    async with aiosqlite.connect('./data/pidors.db') as db:
        cursor = await db.execute(
            "SELECT user_id FROM pidors WHERE chat_id=?",
            (chat_id,),
        )
        results = await cursor.fetchall()
        return [result[0] for result in results]


async def mark_as_used_pidor(chat_id: int) -> None:
    """Mark the pidor usage for a chat as used by updating the timestamp."""
    current_timestamp = int(datetime.datetime.now().timestamp())
    async with aiosqlite.connect('./data/pidors.db') as db:
        await db.execute("""
            INSERT INTO pidor_uses (chat_id, timestamp)
            VALUES (?, ?)
            ON CONFLICT(chat_id)
            DO UPDATE SET timestamp=excluded.timestamp
        """, (chat_id, current_timestamp))
        await db.commit()


async def can_use_pidor(chat_id: int) -> bool:
    """Check if the pidor can be used for a chat."""
    async with aiosqlite.connect('./data/pidors.db') as db:
        cursor = await db.execute("""
            SELECT timestamp FROM pidor_uses WHERE chat_id=?
        """, (chat_id,))
        result = await cursor.fetchone()

    if not result:
        # If there's no record, it means it can be used.
        return True

    last_used_timestamp = result[0]
    current_timestamp = int(datetime.datetime.now().timestamp())

    # Check if 24 hours have passed since the last usage.
    seconds_in_a_day = 24 * 60 * 60
    can_use = (current_timestamp - last_used_timestamp) >= seconds_in_a_day

    return can_use
