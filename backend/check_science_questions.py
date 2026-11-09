import sqlite3

connection = sqlite3.connect("adaptive_learning.db")

query = """
SELECT
    l.id,
    l.title,
    l.topic,
    q.difficulty,
    COUNT(question.id) AS question_count
FROM lessons AS l
JOIN quizzes AS q ON q.lesson_id = l.id
LEFT JOIN questions AS question ON question.quiz_id = q.id
WHERE LOWER(l.topic) != 'social science'
GROUP BY l.id, l.title, l.topic, q.difficulty
ORDER BY l.id, q.difficulty;
"""

for row in connection.execute(query):
    print(row)

connection.close()