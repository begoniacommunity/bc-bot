import sqlite3

connect = sqlite3.connect('./static/msg_stats.db')
curs = connect.cursor()

curs.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        timestamp TEXT
    )
''')

connect.commit()