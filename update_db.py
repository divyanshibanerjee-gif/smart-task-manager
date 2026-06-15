import sqlite3

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE tasks
ADD COLUMN completed INTEGER DEFAULT 0
""")

conn.commit()
conn.close()

print("Database updated!")