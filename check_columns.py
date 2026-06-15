import sqlite3

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(tasks)")

for column in cursor.fetchall():
    print(column)

conn.close()