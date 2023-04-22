from datetime import datetime, timedelta
from telegram import Update
import sqlite3

def stats(update: Update, context):
    connect = sqlite3.connect('./static/msg_stats.db')
    curs = connect.cursor()

    now = datetime.utcnow()
    day_ago = (now - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    week_ago = (now - timedelta(weeks=1)).strftime('%Y-%m-%d %H:%M:%S')
    month_ago = (now - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')

    curs.execute('SELECT COUNT(*) FROM messages WHERE timestamp>?', (day_ago,))
    day_count = curs.fetchone()[0]
    curs.execute('SELECT COUNT(*) FROM messages WHERE timestamp>?', (week_ago,))
    week_count = curs.fetchone()[0]
    curs.execute('SELECT COUNT(*) FROM messages WHERE timestamp>?', (month_ago,))
    month_count = curs.fetchone()[0]
    update.message.reply_text(f'📊 Статистика по сообщениям:\n\n- 🕐 За день: {day_count}\n- 🕒 За неделю: {week_count}\n- 🕔 За месяц: {month_count}')

    connect.close()