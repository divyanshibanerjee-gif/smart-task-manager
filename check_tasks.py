import sqlite3

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("""
SELECT id, task, user_id
FROM tasks
""")

for row in cursor.fetchall():
    print(row)

conn.close()