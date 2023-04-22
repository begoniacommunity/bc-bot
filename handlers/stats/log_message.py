from telegram import Update
import sqlite3

def log_message(update: Update, context):
    connect = sqlite3.connect('./static/msg_stats.db')
    curs = connect.cursor()

    user_id = update.effective_user.id
    timestamp = update.message.date.strftime('%Y-%m-%d %H:%M:%S')
    curs.execute('INSERT INTO messages (user_id, timestamp) VALUES (?, ?)', (user_id, timestamp))
    connect.commit()