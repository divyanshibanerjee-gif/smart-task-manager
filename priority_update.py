import sqlite3

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE tasks
ADD COLUMN priority TEXT DEFAULT 'Medium'
""")

conn.commit()
conn.close()

print("Priority column added!")