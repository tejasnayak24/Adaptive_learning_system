import sqlite3

connection = sqlite3.connect("adaptive_learning.db")
cursor = connection.cursor()

print("\nTOTAL LESSONS:")
cursor.execute("SELECT COUNT(*) FROM lessons")
print(cursor.fetchone()[0])

print("\nLESSONS GROUPED BY TOPIC:")
cursor.execute("""
    SELECT topic, COUNT(*)
    FROM lessons
    GROUP BY topic
    ORDER BY topic
""")

for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]}")

print("\nTOTAL QUIZZES:")
cursor.execute("SELECT COUNT(*) FROM quizzes")
print(cursor.fetchone()[0])

print("\nTOTAL QUESTIONS:")
cursor.execute("SELECT COUNT(*) FROM questions")
print(cursor.fetchone()[0])

print("\nQUESTIONS PER LESSON:")
cursor.execute("""
    SELECT l.id, l.title, COUNT(q.id)
    FROM lessons l
    LEFT JOIN quizzes z ON z.lesson_id = l.id
    LEFT JOIN questions q ON q.quiz_id = z.id
    GROUP BY l.id, l.title
    ORDER BY l.id
""")

for row in cursor.fetchall():
    print(row)

connection.close()