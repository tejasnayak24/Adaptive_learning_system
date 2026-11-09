
import sqlite3
import random
from pathlib import Path

# ==========================================
# DATABASE CONFIGURATION
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 161
LESSON_TITLE = "Indian States, Capitals and Union Territories"
TOPIC = "General Knowledge"

DIFFICULTIES = ["Easy", "Medium", "Hard"]

# ==========================================
# QUESTION BANK
# Format: Question, Correct, Wrong1, Wrong2, Wrong3
# ==========================================

BANK = {

"Easy": [

("What is the capital of Karnataka?", "Bengaluru", "Mysuru", "Mangaluru", "Hubballi"),
("What is the capital of Maharashtra?", "Mumbai", "Pune", "Nagpur", "Nashik"),
("What is the capital of Tamil Nadu?", "Chennai", "Madurai", "Coimbatore", "Salem"),
("What is the capital of Kerala?", "Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur"),
("What is the capital of Rajasthan?", "Jaipur", "Jodhpur", "Udaipur", "Kota"),
("What is the capital of Gujarat?", "Gandhinagar", "Ahmedabad", "Surat", "Vadodara"),
("What is the capital of West Bengal?", "Kolkata", "Darjeeling", "Siliguri", "Howrah"),
("What is the capital of Bihar?", "Patna", "Gaya", "Bhagalpur", "Muzaffarpur"),
("What is the capital of Uttar Pradesh?", "Lucknow", "Kanpur", "Agra", "Varanasi"),
("What is the capital of Madhya Pradesh?", "Bhopal", "Indore", "Gwalior", "Jabalpur"),
("What is the capital of Assam?", "Dispur", "Guwahati", "Silchar", "Dibrugarh"),
("What is the capital of Odisha?", "Bhubaneswar", "Cuttack", "Puri", "Rourkela"),
("What is the capital of Punjab?", "Chandigarh", "Amritsar", "Ludhiana", "Jalandhar"),
("What is the capital of Haryana?", "Chandigarh", "Gurugram", "Faridabad", "Panipat"),
("What is the capital of Goa?", "Panaji", "Margao", "Vasco da Gama", "Mapusa"),
("What is the capital of Sikkim?", "Gangtok", "Namchi", "Gyalshing", "Mangan"),
("What is the capital of Meghalaya?", "Shillong", "Tura", "Jowai", "Nongpoh"),
("What is the capital of Tripura?", "Agartala", "Udaipur", "Dharmanagar", "Kailashahar"),
("What is the capital of Manipur?", "Imphal", "Churachandpur", "Thoubal", "Bishnupur"),
("What is the capital of Mizoram?", "Aizawl", "Lunglei", "Champhai", "Kolasib"),
("What is the capital of Nagaland?", "Kohima", "Dimapur", "Mokokchung", "Wokha"),
("What is the capital of Arunachal Pradesh?", "Itanagar", "Tawang", "Pasighat", "Ziro"),
("What is the capital of Jharkhand?", "Ranchi", "Jamshedpur", "Dhanbad", "Bokaro"),
("What is the capital of Chhattisgarh?", "Raipur", "Bilaspur", "Durg", "Korba"),
("What is the capital of Himachal Pradesh?", "Shimla", "Manali", "Dharamshala", "Solan"),
("What is the capital of Uttarakhand?", "Dehradun", "Haridwar", "Nainital", "Rishikesh"),
("What is the capital of Telangana?", "Hyderabad", "Warangal", "Karimnagar", "Nizamabad"),
("What is the capital of Andhra Pradesh?", "Amaravati", "Visakhapatnam", "Vijayawada", "Tirupati"),
("Which Union Territory has New Delhi as its capital?", "Delhi", "Ladakh", "Chandigarh", "Puducherry"),
("What is the capital of Andaman and Nicobar Islands?", "Sri Vijaya Puram", "Port Blair", "Car Nicobar", "Diglipur"),

],

"Medium": [

("Which Indian state has the longest coastline?", "Gujarat", "Tamil Nadu", "Andhra Pradesh", "Maharashtra"),
("Which state shares its capital with Haryana?", "Punjab", "Rajasthan", "Himachal Pradesh", "Uttar Pradesh"),
("Which Union Territory has Kavaratti as its capital?", "Lakshadweep", "Puducherry", "Ladakh", "Chandigarh"),
("Which Union Territory has Leh as its administrative headquarters?", "Ladakh", "Jammu and Kashmir", "Delhi", "Andaman and Nicobar Islands"),
("Which state has Kohima as its capital?", "Nagaland", "Manipur", "Mizoram", "Meghalaya"),
("Which state has Itanagar as its capital?", "Arunachal Pradesh", "Assam", "Sikkim", "Nagaland"),
("Which state has Aizawl as its capital?", "Mizoram", "Tripura", "Manipur", "Meghalaya"),
("Which state has Agartala as its capital?", "Tripura", "Mizoram", "Nagaland", "Sikkim"),
("Which state has Gangtok as its capital?", "Sikkim", "Meghalaya", "Assam", "Arunachal Pradesh"),
("Which state has Shillong as its capital?", "Meghalaya", "Nagaland", "Manipur", "Tripura"),
("Which Union Territory has Puducherry as its capital?", "Puducherry", "Lakshadweep", "Ladakh", "Chandigarh"),
("Which Union Territory includes the Andaman and Nicobar Islands?", "Andaman and Nicobar Islands", "Lakshadweep", "Dadra and Nagar Haveli and Daman and Diu", "Puducherry"),
("Which state has Raipur as its capital?", "Chhattisgarh", "Jharkhand", "Odisha", "Madhya Pradesh"),
("Which state has Ranchi as its capital?", "Jharkhand", "Bihar", "Chhattisgarh", "West Bengal"),
("Which state has Dispur as its capital?", "Assam", "Meghalaya", "Tripura", "Manipur"),
("Which state has Bhubaneswar as its capital?", "Odisha", "West Bengal", "Bihar", "Jharkhand"),
("Which state has Bhopal as its capital?", "Madhya Pradesh", "Maharashtra", "Rajasthan", "Chhattisgarh"),
("Which state has Jaipur as its capital?", "Rajasthan", "Gujarat", "Haryana", "Punjab"),
("Which state has Thiruvananthapuram as its capital?", "Kerala", "Tamil Nadu", "Karnataka", "Goa"),
("Which state has Chennai as its capital?", "Tamil Nadu", "Andhra Pradesh", "Telangana", "Kerala"),
("Which state has Hyderabad as its capital?", "Telangana", "Karnataka", "Maharashtra", "Andhra Pradesh"),
("Which Union Territory is located off the southwestern coast of India?", "Lakshadweep", "Ladakh", "Delhi", "Chandigarh"),
("Which state has the capital city of Panaji?", "Goa", "Gujarat", "Maharashtra", "Karnataka"),
("Which state has Dehradun as its winter capital and Gairsain as its summer capital?", "Uttarakhand", "Himachal Pradesh", "Uttar Pradesh", "Sikkim"),
("Which state has Dharamshala as its winter capital and Shimla as its summer capital?", "Himachal Pradesh", "Uttarakhand", "Punjab", "Haryana"),
("Which state has Amaravati as its capital?", "Andhra Pradesh", "Telangana", "Tamil Nadu", "Karnataka"),
("Which Union Territory is itself named Chandigarh?", "Chandigarh", "Delhi", "Puducherry", "Lakshadweep"),
("Which northeastern state has Imphal as its capital?", "Manipur", "Mizoram", "Nagaland", "Tripura"),
("Which state has Kolkata as its capital?", "West Bengal", "Bihar", "Odisha", "Assam"),
("Which Union Territory was formed by merging Dadra and Nagar Haveli with Daman and Diu?", "Dadra and Nagar Haveli and Daman and Diu", "Chandigarh", "Puducherry", "Lakshadweep"),

],

"Hard": [

("How many states does India currently have?", "28", "27", "29", "30"),
("How many Union Territories does India currently have?", "8", "7", "9", "10"),
("Which state was formed in 2014 after being separated from Andhra Pradesh?", "Telangana", "Chhattisgarh", "Jharkhand", "Uttarakhand"),
("Which state was created in 2000 and has Ranchi as its capital?", "Jharkhand", "Chhattisgarh", "Uttarakhand", "Telangana"),
("Which state was formed in 2000 with Raipur as its capital?", "Chhattisgarh", "Jharkhand", "Uttarakhand", "Sikkim"),
("Which state was formed in 2000 and has Dehradun as its winter capital?", "Uttarakhand", "Jharkhand", "Chhattisgarh", "Himachal Pradesh"),
("Which Union Territory was created after the reorganisation of the former state of Jammu and Kashmir in 2019?", "Ladakh", "Chandigarh", "Delhi", "Lakshadweep"),
("Which Union Territory was formed alongside Ladakh in 2019?", "Jammu and Kashmir", "Puducherry", "Delhi", "Andaman and Nicobar Islands"),
("Which state shares its capital city with Punjab?", "Haryana", "Rajasthan", "Uttar Pradesh", "Himachal Pradesh"),
("Which city serves as the capital of both Punjab and Haryana?", "Chandigarh", "Amritsar", "Gurugram", "Patiala"),
("Which state has the largest area in India?", "Rajasthan", "Madhya Pradesh", "Maharashtra", "Uttar Pradesh"),
("Which state has the smallest area in India?", "Goa", "Sikkim", "Tripura", "Manipur"),
("Which northeastern state has Kohima as its capital?", "Nagaland", "Manipur", "Mizoram", "Arunachal Pradesh"),
("Which state has the capital Aizawl and shares international borders with Bangladesh and Myanmar?", "Mizoram", "Tripura", "Meghalaya", "Assam"),
("Which state has the capital Itanagar and shares an international border with China?", "Arunachal Pradesh", "Sikkim", "Nagaland", "Assam"),
("Which northeastern state has the capital Agartala and is surrounded by Bangladesh on three sides?", "Tripura", "Meghalaya", "Mizoram", "Manipur"),
("Which state has the capital Shillong and is famous for the Khasi, Garo and Jaintia hills?", "Meghalaya", "Nagaland", "Assam", "Sikkim"),
("Which state has the capital Gangtok and shares borders with Nepal, Bhutan and China?", "Sikkim", "Assam", "Manipur", "Tripura"),
("Which Union Territory consists of a group of coral islands in the Arabian Sea?", "Lakshadweep", "Andaman and Nicobar Islands", "Puducherry", "Chandigarh"),
("Which Union Territory lies in the Bay of Bengal and includes the Nicobar Islands?", "Andaman and Nicobar Islands", "Lakshadweep", "Delhi", "Ladakh"),
("Which Union Territory has Sri Vijaya Puram as its capital?", "Andaman and Nicobar Islands", "Lakshadweep", "Puducherry", "Chandigarh"),
("Which Union Territory has Kavaratti as its capital?", "Lakshadweep", "Delhi", "Ladakh", "Puducherry"),
("Which state has the capital Bhubaneswar and is located along the eastern coast of India?", "Odisha", "West Bengal", "Andhra Pradesh", "Tamil Nadu"),
("Which state has the capital Gandhinagar, while Ahmedabad is its largest city?", "Gujarat", "Rajasthan", "Maharashtra", "Madhya Pradesh"),
("Which state has the capital Bhopal and is often called the Heart of India?", "Madhya Pradesh", "Chhattisgarh", "Rajasthan", "Uttar Pradesh"),
("Which state has the capital Patna and is associated with the ancient kingdom of Magadha?", "Bihar", "Jharkhand", "Uttar Pradesh", "West Bengal"),
("Which state has the capital Lucknow and shares an international border with Nepal?", "Uttar Pradesh", "Bihar", "Haryana", "Madhya Pradesh"),
("Which state has the capital Jaipur and is home to the Thar Desert?", "Rajasthan", "Gujarat", "Punjab", "Haryana"),
("Which state has the capital Panaji and is India's smallest state by area?", "Goa", "Sikkim", "Tripura", "Mizoram"),
("Which state has the capital Bengaluru and is known for its technology industry?", "Karnataka", "Telangana", "Tamil Nadu", "Kerala"),

]
}


# ==========================================
# VALIDATE QUESTION BANK
# ==========================================

def validate_bank():

    for difficulty in DIFFICULTIES:

        questions = BANK[difficulty]

        if len(questions) != 30:
            raise ValueError(
                f"{difficulty} has {len(questions)} questions instead of 30."
            )

        for index, item in enumerate(questions, start=1):

            if len(item) != 5:
                raise ValueError(
                    f"{difficulty} question {index} must have 5 values."
                )

            question, correct, wrong1, wrong2, wrong3 = item
            options = [correct, wrong1, wrong2, wrong3]

            if any(not value.strip() for value in [question] + options):
                raise ValueError(
                    f"{difficulty} question {index} contains empty text."
                )

            if len(set(options)) != 4:
                raise ValueError(
                    f"{difficulty} question {index} has duplicate options."
                )

    print("Question bank validation successful.")

    for difficulty in DIFFICULTIES:
        print(f"{difficulty}: {len(BANK[difficulty])} questions")


# ==========================================
# INSERT INTO DATABASE
# ==========================================

def main():

    validate_bank()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:

        # Check whether lesson already exists
        cursor.execute(
            "SELECT title, topic FROM lessons WHERE id = ?",
            (LESSON_ID,)
        )

        existing_lesson = cursor.fetchone()

        if existing_lesson is None:

            cursor.execute(
                """
                INSERT INTO lessons
                (id, title, topic, difficulty, content, created_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                """,
                (
                    LESSON_ID,
                    LESSON_TITLE,
                    TOPIC,
                    "Mixed",
                    "Learn about Indian states, capitals and Union Territories."
                )
            )

            print(f"Lesson {LESSON_ID} created successfully.")

        elif existing_lesson != (LESSON_TITLE, TOPIC):

            raise ValueError(
                f"Lesson ID {LESSON_ID} is already used by {existing_lesson}."
            )

        else:

            print(f"Lesson {LESSON_ID} already exists.")

        # Insert Easy, Medium and Hard quizzes
        for difficulty in DIFFICULTIES:

            cursor.execute(
                """
                SELECT id FROM quizzes
                WHERE lesson_id = ? AND difficulty = ?
                """,
                (LESSON_ID, difficulty)
            )

            quiz_rows = cursor.fetchall()

            if len(quiz_rows) > 1:
                raise ValueError(
                    f"Multiple {difficulty} quizzes found for this lesson."
                )

            if quiz_rows:

                quiz_id = quiz_rows[0][0]

            else:

                cursor.execute(
                    """
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                    """,
                    (
                        LESSON_ID,
                        f"{LESSON_TITLE} - {difficulty}",
                        difficulty
                    )
                )

                quiz_id = cursor.lastrowid

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )

            existing_count = cursor.fetchone()[0]

            if existing_count > 30:
                raise ValueError(
                    f"{difficulty} already has {existing_count} questions."
                )

            # Add only missing questions
            for item in BANK[difficulty][existing_count:]:

                question, correct, wrong1, wrong2, wrong3 = item

                options = [correct, wrong1, wrong2, wrong3]
                random.shuffle(options)

                correct_answer = "ABCD"[options.index(correct)]

                cursor.execute(
                    """
                    INSERT INTO questions (
                        quiz_id,
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
                        correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        quiz_id,
                        question,
                        options[0],
                        options[1],
                        options[2],
                        options[3],
                        correct_answer
                    )
                )

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )

            final_count = cursor.fetchone()[0]

            if final_count != 30:
                raise ValueError(
                    f"{difficulty} has {final_count} questions instead of 30."
                )

            print(f"{difficulty}: {final_count}/30 SUCCESS")

        connection.commit()

        print("\n====================================")
        print("GK TOPIC 1 COMPLETED SUCCESSFULLY")
        print("Indian States, Capitals and UTs")
        print("Easy: 30")
        print("Medium: 30")
        print("Hard: 30")
        print("TOTAL: 90 QUESTIONS")
        print("====================================")

    except Exception as error:

        connection.rollback()
        print("\nERROR:", error)
        raise

    finally:

        connection.close()


if __name__ == "__main__":
    main()
