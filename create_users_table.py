import sqlite3

conn = sqlite3.connect("tasks.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    email TEXT UNIQUE NOT NULL,

    password TEXT NOT NULL

)
""")

conn.commit()

conn.close()

print("Users table created successfully!")