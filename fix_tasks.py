import sqlite3

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("""
UPDATE tasks
SET user_id = 1
WHERE user_id IS NULL
""")

conn.commit()
conn.close()

print("Tasks updated!")