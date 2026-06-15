import sqlite3

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE tasks
ADD COLUMN due_date TEXT
""")

conn.commit()
conn.close()

print("Due date column added!")