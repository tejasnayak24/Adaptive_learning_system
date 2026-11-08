import sqlite3

conn = sqlite3.connect("adaptive_learning.db")
cursor = conn.cursor()

cursor.execute("""
    SELECT id, title
    FROM lessons
    WHERE topic = 'English'
    ORDER BY id
""")

for row in cursor.fetchall():
    print(row)

conn.close()