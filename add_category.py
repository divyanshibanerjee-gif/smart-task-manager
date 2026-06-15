import sqlite3

conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE tasks
ADD COLUMN category TEXT DEFAULT 'Personal'
""")

conn.commit()
conn.close()

print("Category column added!")