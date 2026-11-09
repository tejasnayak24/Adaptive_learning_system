
import sqlite3
import random
from pathlib import Path

random.seed(42)

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

TOPIC = "Bar Graphs and Pie Charts"
SUBJECT = "Mathematics"


# Format: (question, correct_answer, [wrong1, wrong2, wrong3])


EASY = [
    ("What is a bar graph?", "A graph using rectangular bars", ["A graph using only circles", "A graph using triangles", "A graph using curved lines"]),
    ("Which graph represents data using sectors of a circle?", "Pie chart", ["Bar graph", "Line graph", "Pictograph"]),
    ("What does the height of a bar represent?", "Value or frequency", ["Graph title", "Category name", "Source of data"]),
    ("What is the total angle of a pie chart?", "360 degrees", ["180 degrees", "90 degrees", "270 degrees"]),
    ("Which graph is useful for comparing different categories?", "Bar graph", ["Pie chart only", "Number line", "Coordinate plane"]),
    ("What shape is used in a pie chart?", "Circle", ["Square", "Rectangle", "Triangle"]),
    ("What does each sector of a pie chart represent?", "A proportion of the whole", ["Only the largest value", "The graph title", "The horizontal axis"]),
    ("What is usually shown on the horizontal axis of a bar graph?", "Categories", ["Frequencies only", "Graph title", "Legend only"]),
    ("What is usually shown on the vertical axis of a bar graph?", "Values or frequencies", ["Category names only", "Graph title", "Source name"]),
    ("What should the bars in a simple bar graph have?", "Equal width", ["Different widths", "Circular shapes", "Curved edges"]),
    ("What is the space between bars in a simple bar graph usually like?", "Equal spacing", ["No spacing in every case", "Random spacing", "Unequal spacing"]),
    ("Which graph is suitable for showing how a whole is divided into parts?", "Pie chart", ["Bar graph", "Line graph", "Histogram"]),
    ("If a pie chart sector represents one-fourth of the whole, what is its angle?", "90 degrees", ["45 degrees", "120 degrees", "180 degrees"]),
    ("What percentage of a pie chart does a half-circle represent?", "50%", ["25%", "75%", "100%"]),
    ("What percentage of a pie chart does a quarter-circle represent?", "25%", ["10%", "50%", "75%"]),
    ("How many degrees are there in a semicircle?", "180 degrees", ["90 degrees", "120 degrees", "360 degrees"]),
    ("A bar graph has a bar of height 5. What value does it represent if the scale is 1 unit per student?", "5 students", ["1 student", "10 students", "15 students"]),
    ("What is a scale in a graph?", "A system for representing values", ["The graph title", "The colour of bars", "The name of a category"]),
    ("Which graph can compare the number of boys and girls in a class?", "Bar graph", ["Pie chart only", "Circle only", "Number line"]),
    ("If a pie chart represents 100 students, what does 50% represent?", "50 students", ["25 students", "75 students", "100 students"]),
    ("What is the sum of all sectors in a pie chart?", "360 degrees", ["100 degrees", "180 degrees", "270 degrees"]),
    ("What does a legend in a graph explain?", "Symbols or colours used", ["Only the title", "The total angle", "The page number"]),
    ("Which graph is generally easier for comparing exact category values?", "Bar graph", ["Pie chart", "Circle diagram", "Venn diagram"]),
    ("If a bar represents 10 books, what do 3 equal bars represent?", "30 books", ["10 books", "20 books", "40 books"]),
    ("What is the angle of a complete circle?", "360 degrees", ["90 degrees", "180 degrees", "270 degrees"]),
    ("Which graph is divided into sectors?", "Pie chart", ["Bar graph", "Line graph", "Pictograph"]),
    ("If one bar represents 5 students, what do 4 bars of equal height represent in total?", "20 students", ["10 students", "15 students", "25 students"]),
    ("What is the purpose of a title in a bar graph?", "To describe the data", ["To calculate the mean", "To show the scale only", "To draw the bars"]),
    ("Which graph uses bars of different heights?", "Bar graph", ["Pie chart", "Circle graph", "Venn diagram"]),
    ("If a pie chart sector is 180 degrees, what fraction of the whole is it?", "1/2", ["1/4", "1/3", "3/4"]),
]


MEDIUM = [
    ("Find the angle representing 25% of a pie chart.", "90 degrees", ["45 degrees", "120 degrees", "180 degrees"]),
    ("Find the angle representing 40% of a pie chart.", "144 degrees", ["120 degrees", "150 degrees", "180 degrees"]),
    ("Find the angle representing 10% of a pie chart.", "36 degrees", ["18 degrees", "45 degrees", "60 degrees"]),
    ("Find the angle representing 75% of a pie chart.", "270 degrees", ["180 degrees", "225 degrees", "300 degrees"]),
    ("A pie chart represents 200 students. How many students are represented by a 90-degree sector?", "50", ["25", "75", "100"]),
    ("A pie chart represents 120 people. How many are represented by 25%?", "30", ["20", "40", "60"]),
    ("A pie chart sector has an angle of 72 degrees. Find its percentage.", "20%", ["10%", "25%", "30%"]),
    ("A sector of 180 degrees represents how many percent of a pie chart?", "50%", ["25%", "40%", "75%"]),
    ("Find the angle for 30% of a pie chart.", "108 degrees", ["90 degrees", "120 degrees", "150 degrees"]),
    ("Find the angle for 15% of a pie chart.", "54 degrees", ["36 degrees", "45 degrees", "72 degrees"]),
    ("A pie chart represents 360 students. Find the number represented by a 120-degree sector.", "120", ["60", "90", "180"]),
    ("A pie chart represents 400 people. Find the number represented by 10%.", "40", ["20", "60", "80"]),
    ("In a bar graph, a bar has height 8 and each unit represents 5 students. Find the value.", "40 students", ["25 students", "35 students", "45 students"]),
    ("A bar graph shows 25 boys and 35 girls. Find the total number of students.", "60", ["50", "55", "65"]),
    ("A bar graph shows sales of 20, 30 and 40 units. Find the total sales.", "90", ["80", "100", "110"]),
    ("The sales of a shop are 15, 25, 35 and 45 units. Find the difference between the highest and lowest sales.", "30", ["20", "25", "35"]),
    ("A bar graph uses a scale of 1 cm = 10 books. What does a 4 cm bar represent?", "40 books", ["10 books", "20 books", "50 books"]),
    ("A pie chart represents 500 students. Find the number represented by 40%.", "200", ["100", "150", "250"]),
    ("The angle of a sector is 90 degrees. What percentage does it represent?", "25%", ["10%", "20%", "50%"]),
    ("A pie chart sector represents 20% of 300 students. Find the number of students.", "60", ["30", "50", "90"]),
    ("Find the angle representing 5% of a pie chart.", "18 degrees", ["15 degrees", "25 degrees", "36 degrees"]),
    ("A bar graph shows values 10, 20, 30 and 40. Find their average.", "25", ["20", "30", "35"]),
    ("A pie chart represents 600 people. What number is represented by a 60-degree sector?", "100", ["60", "120", "150"]),
    ("A pie chart has sectors of 90, 120 and 60 degrees. Find the remaining angle.", "90 degrees", ["60 degrees", "120 degrees", "180 degrees"]),
    ("A bar graph shows 18 students choosing cricket and 12 choosing football. Find the difference.", "6", ["4", "8", "10"]),
    ("A pie chart represents 800 people. Find the number represented by 15%.", "120", ["80", "100", "160"]),
    ("A sector of 45 degrees represents how much percentage?", "12.5%", ["10%", "15%", "25%"]),
    ("A bar graph shows production of 40, 50 and 60 items. Find the total production.", "150", ["140", "160", "180"]),
    ("A pie chart represents 240 students. Find the number represented by a 180-degree sector.", "120", ["60", "80", "180"]),
    ("A bar graph uses a scale of 1 unit = 4 products. What does a bar of height 7 represent?", "28 products", ["21 products", "24 products", "32 products"]),
]


HARD = [
    ("A pie chart represents 720 students. Find the number represented by a 45-degree sector.", "90", ["60", "120", "180"]),
    ("A pie chart represents 900 people. Find the number represented by a 72-degree sector.", "180", ["90", "120", "240"]),
    ("The angle of a pie chart sector is 126 degrees. Find its percentage.", "35%", ["25%", "30%", "40%"]),
    ("A pie chart represents 600 students. The angle for cricket is 108 degrees. How many students prefer cricket?", "180", ["120", "150", "200"]),
    ("A pie chart represents 800 people. If 25% prefer reading, how many people prefer reading?", "200", ["100", "150", "250"]),
    ("A sector represents 15% of a pie chart. Find its angle.", "54 degrees", ["45 degrees", "60 degrees", "72 degrees"]),
    ("A pie chart has sectors of 80, 100, 70 and 60 degrees. Find the remaining angle.", "50 degrees", ["40 degrees", "60 degrees", "70 degrees"]),
    ("A pie chart represents 1,200 people. Find the number represented by a 30-degree sector.", "100", ["80", "120", "150"]),
    ("The angle of a sector is 144 degrees. If the total population is 500, how many people does it represent?", "200", ["150", "180", "250"]),
    ("A pie chart represents 400 students. The sector for science is 90 degrees. Find the number of students.", "100", ["80", "120", "150"]),
    ("A bar graph shows monthly sales of 120, 150, 180 and 210 items. Find the average sales.", "165", ["150", "160", "180"]),
    ("A shop sells 45, 60, 75 and 100 products on four days. Find the total sales.", "280", ["260", "270", "300"]),
    ("A bar graph uses a scale of 1 cm = 25 units. A bar is 6 cm tall. Find its value.", "150 units", ["125 units", "100 units", "175 units"]),
    ("The difference between two bar values is 35. The smaller value is 45. Find the larger value.", "80", ["70", "75", "90"]),
    ("A pie chart represents 1,000 students. If 18% prefer mathematics, how many students prefer mathematics?", "180", ["150", "200", "220"]),
    ("A sector of a pie chart is 72 degrees. If the total is 250 people, how many people does the sector represent?", "50", ["40", "60", "75"]),
    ("A pie chart represents 720 people. One category has 25% and another has 15%. How many people belong to these two categories together?", "288", ["180", "240", "360"]),
    ("The angles of three sectors are 90, 120 and 80 degrees. Find the percentage represented by the remaining sector.", "19.44% approximately", ["15%", "20%", "25%"]),
    ("A pie chart represents 600 students. The sector for sports is 72 degrees. Find the percentage of students who prefer sports.", "20%", ["15%", "25%", "30%"]),
    ("A bar graph shows production of 80, 100, 120, 140 and 160 units. Find the average production.", "120", ["100", "110", "130"]),
    ("A pie chart represents 480 people. Find the number represented by a 150-degree sector.", "200", ["150", "180", "240"]),
    ("A sector of 54 degrees represents how many people out of 800?", "120", ["100", "150", "180"]),
    ("A pie chart has sectors of 20%, 25%, 30% and 15%. Find the remaining percentage.", "10%", ["5%", "15%", "20%"]),
    ("A pie chart represents 2,000 people. Find the number represented by 12.5%.", "250", ["200", "300", "350"]),
    ("A bar graph shows 125, 150, 175 and 200 items. Find the difference between the highest and lowest values.", "75", ["50", "60", "100"]),
    ("A pie chart represents 360 students. If 40% are girls, how many are boys?", "216", ["144", "180", "240"]),
    ("The angle of a pie chart sector is 162 degrees. Find its percentage.", "45%", ["35%", "40%", "50%"]),
    ("A pie chart represents 1,500 people. Find the number represented by a 36-degree sector.", "150", ["100", "180", "200"]),
    ("A bar graph shows 60, 75, 90 and 105 units. Find the total.", "330", ["300", "315", "345"]),
    ("A pie chart represents 720 students. A sector of 108 degrees represents how many students?", "216", ["180", "200", "240"]),
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

        print("\nBar Graphs and Pie Charts seeding completed!")
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
