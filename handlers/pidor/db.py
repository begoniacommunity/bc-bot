import datetime
from typing import List, Tuple

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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                timestamp INTEGER NOT NULL, 
                outcome INTEGER NOT NULL
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


async def mark_as_used_pidor(chat_id: int, outcome_user_id: int) -> None:
    """Mark the pidor usage for a chat as used by updating the timestamp."""
    current_timestamp = int(datetime.datetime.now().timestamp())
    async with aiosqlite.connect('./data/pidors.db') as db:
        await db.execute("""
            INSERT INTO pidor_uses (chat_id, timestamp, outcome) VALUES (?, ?, ?)
        """, (chat_id, current_timestamp, outcome_user_id))
        await db.commit()


async def get_todays_pidor(chat_id: int) -> Tuple[int] or None:
    """Check if the pidor can be used again for the given chat_id."""
    current_timestamp = int(datetime.datetime.now().timestamp())
    one_day_ago = current_timestamp - 86400  # 24 hours in seconds

    async with aiosqlite.connect('./data/pidors.db') as db:
        cursor = await db.execute("""
            SELECT outcome FROM pidor_uses 
            WHERE chat_id = ? AND timestamp > ? 
            ORDER BY timestamp DESC LIMIT 1
        """, (chat_id, one_day_ago))
        result = await cursor.fetchone()

    return result


async def get_pidor_usage_stats(chat_id: int) -> List[dict]:
    """Retrieve pidor usage stats for the last year, sorted by occurrence."""
    one_year_ago = int((datetime.datetime.now() - datetime.timedelta(days=365)).timestamp())

    async with aiosqlite.connect('./data/pidors.db') as db:
        cursor = await db.execute("""
            SELECT outcome, COUNT(outcome) as occurrences 
            FROM pidor_uses 
            WHERE chat_id = ? AND timestamp >= ?
            GROUP BY outcome 
            ORDER BY occurrences DESC
        """, (chat_id, one_year_ago))
        results = await cursor.fetchall()

    return [{'user_id': row[0], 'number_of_occurrences': row[1]} for row in results]
