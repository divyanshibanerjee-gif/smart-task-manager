import sqlite3

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("SELECT id, email FROM users")

for row in cursor.fetchall():
    print(row)

conn.close()