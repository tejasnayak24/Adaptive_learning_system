
import sqlite3
import random
from pathlib import Path

random.seed(42)

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Data Handling"
SUBJECT = "Mathematics"


# Format:
# (question, correct_answer, [wrong1, wrong2, wrong3])


EASY = [
    ("What is data?", "Collection of information", ["A type of number", "A mathematical symbol", "A geometrical shape"]),
    ("Which of the following is an example of data?", "Marks obtained by students", ["A triangle", "A circle", "A straight line"]),
    ("What is the process of collecting and organizing information called?", "Data handling", ["Measurement", "Calculation", "Construction"]),
    ("Which chart uses rectangular bars to represent data?", "Bar graph", ["Pie chart", "Line segment", "Circle"]),
    ("What is a tally mark used for?", "Counting frequency", ["Measuring length", "Finding area", "Calculating angles"]),
    ("How many tally marks represent the number 5?", "5", ["3", "4", "6"]),
    ("What is frequency?", "Number of times a value occurs", ["Sum of all values", "Difference between values", "Largest value"]),
    ("Which of these is a method of presenting data?", "Pictograph", ["Equation", "Formula", "Algebraic expression"]),
    ("What does a bar graph use to represent values?", "Bars", ["Triangles", "Circles", "Points only"]),
    ("What is the first step in handling data?", "Collecting data", ["Drawing a pie chart", "Finding the average", "Calculating percentages"]),
    ("Which type of data is collected directly from people?", "Primary data", ["Secondary data", "Grouped data", "Continuous data"]),
    ("Which value represents the highest observation?", "Maximum", ["Minimum", "Average", "Frequency"]),
    ("Which value represents the lowest observation?", "Minimum", ["Maximum", "Median", "Mode"]),
    ("What is the difference between the maximum and minimum values called?", "Range", ["Mean", "Median", "Mode"]),
    ("Find the range of 2, 4, 6, 8, 10.", "8", ["6", "10", "12"]),
    ("How many observations are there in 3, 5, 7, 9?", "4", ["3", "5", "9"]),
    ("What is the total of 2, 3 and 5?", "10", ["8", "9", "11"]),
    ("Which graph is circular in shape?", "Pie chart", ["Bar graph", "Line graph", "Pictograph"]),
    ("What does a title in a graph describe?", "Subject of the data", ["Only the colours", "Only the numbers", "The graph's border"]),
    ("What is the purpose of a key in a pictograph?", "To explain the symbols", ["To show the title", "To calculate the range", "To draw the axes"]),
    ("If one symbol represents 5 students, what do 2 symbols represent?", "10 students", ["5 students", "7 students", "15 students"]),
    ("Which graph is useful for comparing categories?", "Bar graph", ["Pie chart only", "Circle only", "Number line"]),
    ("What is an observation in data?", "An individual recorded value", ["The graph title", "The graph colour", "The table heading"]),
    ("Which of these is a source of secondary data?", "Published reports", ["Personal interview", "Direct observation", "Own survey"]),
    ("What is a frequency table used for?", "Organizing data and frequencies", ["Drawing geometric shapes", "Finding angles", "Measuring distance"]),
    ("How many times does 4 occur in 2, 4, 4, 6, 4?", "3", ["1", "2", "4"]),
    ("What is the range of 5, 10, 15, 20?", "15", ["10", "20", "25"]),
    ("Which of these is a category in a data set?", "Favourite colours", ["A mathematical operation", "A straight line", "A fraction bar"]),
    ("What does the horizontal axis of a bar graph usually show?", "Categories", ["Only the title", "The graph key", "The source name"]),
    ("What does the vertical axis of a bar graph usually show?", "Values or frequencies", ["Categories only", "The title", "The source name"]),
]


MEDIUM = [
    ("Find the mean of 4, 6, 8, 10, 12.", "8", ["6", "9", "10"]),
    ("Find the median of 3, 5, 7, 9, 11.", "7", ["5", "8", "9"]),
    ("Find the mode of 2, 3, 3, 4, 5.", "3", ["2", "4", "5"]),
    ("Find the range of 12, 18, 25, 30, 35.", "23", ["18", "25", "35"]),
    ("Find the mean of 5, 10, 15, 20.", "12.5", ["10", "15", "20"]),
    ("Find the median of 2, 4, 6, 8, 10, 12.", "7", ["6", "8", "9"]),
    ("Find the mode of 4, 5, 5, 6, 6, 6, 7.", "6", ["5", "7", "4"]),
    ("The marks are 10, 20, 30, 40. Find their mean.", "25", ["20", "30", "35"]),
    ("Find the range of 7, 14, 21, 28, 35.", "28", ["21", "35", "14"]),
    ("Find the median of 10, 20, 30, 40, 50.", "30", ["20", "25", "40"]),
    ("The frequencies are 2, 3, 5. Find the total frequency.", "10", ["8", "9", "11"]),
    ("If 4 students like cricket and 6 like football, how many students are there in total?", "10", ["8", "12", "14"]),
    ("A pictograph uses one symbol for 4 people. What do 5 symbols represent?", "20 people", ["16 people", "12 people", "24 people"]),
    ("A bar graph shows 15 boys and 20 girls. What is the total number of students?", "35", ["30", "40", "45"]),
    ("Find the mean of 6, 8, 10, 12, 14.", "10", ["8", "11", "12"]),
    ("Find the median of 1, 3, 5, 7, 9, 11, 13.", "7", ["5", "9", "11"]),
    ("Find the mode of 8, 9, 8, 10, 11, 8, 12.", "8", ["9", "10", "12"]),
    ("The range of a data set is 18 and the minimum value is 7. Find the maximum value.", "25", ["11", "18", "24"]),
    ("The maximum value is 40 and the range is 15. Find the minimum value.", "25", ["15", "20", "30"]),
    ("Find the mean of 2, 4, 6, 8, 10, 12.", "7", ["6", "8", "9"]),
    ("A class has 12 boys and 18 girls. What percentage of the class are girls?", "60%", ["40%", "50%", "70%"]),
    ("A pie chart represents 100 students. What angle represents 25 students?", "90 degrees", ["45 degrees", "120 degrees", "180 degrees"]),
    ("What angle represents 50% of a pie chart?", "180 degrees", ["90 degrees", "120 degrees", "270 degrees"]),
    ("What angle represents 25% of a pie chart?", "90 degrees", ["45 degrees", "180 degrees", "270 degrees"]),
    ("The mean of 5 numbers is 10. What is their total sum?", "50", ["10", "15", "40"]),
    ("The total of 6 observations is 72. Find their mean.", "12", ["10", "14", "18"]),
    ("Find the median of 4, 8, 10, 12, 16, 20.", "11", ["10", "12", "14"]),
    ("Find the range of 15, 22, 28, 35, 42.", "27", ["22", "35", "42"]),
    ("A survey records 8, 12 and 10 students choosing three activities. Find the total.", "30", ["28", "32", "35"]),
    ("If 3 symbols represent 15 students, how many students does one symbol represent?", "5", ["3", "10", "15"]),
]


HARD = [
    ("The mean of 5 numbers is 18. Four numbers are 12, 16, 20 and 22. Find the fifth number.", "20", ["18", "22", "24"]),
    ("The mean of 6 observations is 15. Find their total sum.", "90", ["75", "80", "100"]),
    ("The median of 5, 8, 12, x, 20 is 12, where the values are in ascending order. Which value can x be?", "12", ["8", "5", "20"]),
    ("The mean of 10, 20, 30, 40 and x is 30. Find x.", "50", ["40", "30", "60"]),
    ("The range of a data set is 35. Its minimum value is 15. Find the maximum value.", "50", ["45", "35", "55"]),
    ("The mean of 4 numbers is 25. Three numbers are 20, 24 and 30. Find the fourth number.", "26", ["24", "25", "28"]),
    ("Find the median of 3, 7, 9, 11, 15, 17, 19, 21.", "13", ["11", "15", "17"]),
    ("Find the mean of 12, 15, 18, 21, 24, 30.", "20", ["18", "21", "24"]),
    ("The mode of 2, 3, 3, 4, 4, 4, 5, 5 is:", "4", ["3", "5", "2"]),
    ("The total frequency is 50. If three frequencies are 10, 15 and 20, find the fourth frequency.", "5", ["10", "15", "20"]),
    ("A pie chart represents 200 students. Find the angle for 50 students.", "90 degrees", ["45 degrees", "120 degrees", "180 degrees"]),
    ("A pie chart sector has an angle of 72 degrees. What percentage does it represent?", "20%", ["10%", "25%", "30%"]),
    ("A pie chart represents 360 students. Find the number represented by a 90-degree sector.", "90", ["60", "120", "180"]),
    ("The mean of 8 numbers is 14. If one number is removed, the mean of the remaining 7 numbers is 13. Find the removed number.", "21", ["14", "18", "28"]),
    ("The average of 5 numbers is 16. If 20 is added as a sixth number, find the new mean.", "16.67 approximately", ["16", "17", "18"]),
    ("The mean of 4 numbers is 12. If each number is increased by 3, what is the new mean?", "15", ["12", "13", "16"]),
    ("The mean of 6 values is 20. If each value is doubled, what is the new mean?", "40", ["20", "30", "60"]),
    ("The mean of 5 observations is 24. Four observations add up to 100. Find the fifth observation.", "20", ["16", "24", "28"]),
    ("Find the median of 2, 5, 8, 10, 12, 15, 18, 20, 22, 25.", "11", ["10", "12", "15"]),
    ("A data set has minimum 12 and maximum 65. Find its range.", "53", ["43", "55", "77"]),
    ("In a frequency table, values 1, 2 and 3 have frequencies 2, 3 and 5. Find the mean.", "2.3", ["2", "2.5", "3"]),
    ("Values 2, 4 and 6 have frequencies 3, 2 and 5 respectively. Find the total frequency.", "10", ["8", "12", "15"]),
    ("Values 1, 2 and 3 have frequencies 2, 3 and 5 respectively. Find the total of all observations.", "23", ["20", "25", "30"]),
    ("A class has 40 students. If 30% are absent, how many are present?", "28", ["12", "30", "32"]),
    ("A pie chart sector representing 40% of data has what angle?", "144 degrees", ["120 degrees", "90 degrees", "180 degrees"]),
    ("A pie chart sector has an angle of 120 degrees. What fraction of the whole does it represent?", "1/3", ["1/2", "1/4", "2/3"]),
    ("The mean of 7 numbers is 10. If six numbers total 54, find the seventh number.", "16", ["12", "14", "18"]),
    ("The average of 4 numbers is 15. If one number is 18, what is the average of the remaining three?", "14", ["12", "15", "16"]),
    ("The frequencies of four categories are 5, 10, 15 and 20. What percentage does the largest category represent?", "40%", ["20%", "30%", "50%"]),
    ("The mean of 5 numbers is 20. If each number is reduced by 4, what is the new mean?", "16", ["14", "18", "24"]),
]


def make_questions(data):
    questions = []

    for item in data:
        question = str(item[0])
        answer = str(item[1])
        wrong_answers = [str(x) for x in item[2]]

        options = [answer] + wrong_answers

        if len(options) != 4 or len(set(options)) != 4:
            raise ValueError(
                f"Invalid or duplicate options: {question} | {options}"
            )

        random.shuffle(options)

        correct_answer = ["A", "B", "C", "D"][options.index(answer)]

        questions.append((
            question,
            options[0],
            options[1],
            options[2],
            options[3],
            correct_answer
        ))

    return questions


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM lessons WHERE title = ? AND topic = ?",
            (TOPIC, SUBJECT)
        )

        lesson = cursor.fetchone()

        if not lesson:
            print(f"Lesson not found: {TOPIC}")
            return

        lesson_id = lesson[0]

        difficulty_data = {
            "Easy": EASY,
            "Medium": MEDIUM,
            "Hard": HARD
        }

        total_inserted = 0

        for difficulty, data in difficulty_data.items():

            if len(data) != 30:
                raise ValueError(
                    f"{difficulty} must contain exactly 30 questions. "
                    f"Found {len(data)}."
                )

            cursor.execute("""
                SELECT id FROM quizzes
                WHERE lesson_id = ?
                AND LOWER(difficulty) = LOWER(?)
            """, (lesson_id, difficulty))

            quiz = cursor.fetchone()

            if not quiz:
                print(f"{difficulty} quiz not found!")
                continue

            quiz_id = quiz[0]

            questions = make_questions(data)
            inserted = 0

            for question in questions:

                cursor.execute("""
                    SELECT 1 FROM questions
                    WHERE quiz_id = ? AND question = ?
                """, (quiz_id, question[0]))

                if cursor.fetchone():
                    continue

                cursor.execute("""
                    INSERT INTO questions
                    (
                        quiz_id,
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
                        correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (quiz_id, *question))

                inserted += 1

            total_inserted += inserted

            print(
                f"{difficulty}: {inserted} new questions inserted."
            )

        conn.commit()

        print("\nData Handling seeding completed!")
        print(f"Total new questions inserted: {total_inserted}")

        for difficulty in difficulty_data:
            cursor.execute("""
                SELECT COUNT(*)
                FROM questions
                WHERE quiz_id IN (
                    SELECT id FROM quizzes
                    WHERE lesson_id = ?
                    AND LOWER(difficulty) = LOWER(?)
                )
            """, (lesson_id, difficulty))

            count = cursor.fetchone()[0]
            print(f"{difficulty} total questions in database: {count}")

    except Exception as e:
        conn.rollback()
        print(f"\nError: {e}")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()
