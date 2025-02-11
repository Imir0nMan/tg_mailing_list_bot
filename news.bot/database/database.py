import sqlite3
from section1.commands import usr_data
conn = sqlite3.connect("database/main_database.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
user_id INTEGER,
key TEXT,
value TEXT,
PRIMARY KEY (user_id, key)
)
''')

conn.commit()

for key, value in usr_data.items():
	cursor.execute("""INSERT INTO Users(user_id, key, value) VALUES(?, ?, ?) 
					ON CONFLICT(user_id, key) DO UPDATE SET value=?""",
	(usr_data['user_id'], key, value, value)
	)

conn.commit()
conn.close()
