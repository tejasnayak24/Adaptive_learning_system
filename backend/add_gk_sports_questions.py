
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 171
LESSON_TITLE = "Indian and World Sports - Games, Players, Trophies and Records"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("How many players from one team are on the field in a standard football match?", "11", "9", "7", "12"),
        ("How many players from one team are on the court in basketball?", "5", "6", "7", "11"),
        ("Which sport is associated with the term 'love' for a score of zero?", "Tennis", "Cricket", "Football", "Hockey"),
        ("Which country hosted the first modern Olympic Games in 1896?", "Greece", "France", "Italy", "United Kingdom"),
        ("How often are the Summer Olympic Games normally held?", "Every four years", "Every two years", "Every three years", "Every five years"),
        ("Which sport is played at Wimbledon?", "Tennis", "Badminton", "Golf", "Squash"),
        ("How many players are there in a cricket team?", "11", "10", "9", "12"),
        ("Which Indian athlete is popularly known as the Flying Sikh?", "Milkha Singh", "P. T. Usha", "Neeraj Chopra", "Abhinav Bindra"),
        ("Which sport is associated with the FIFA World Cup?", "Football", "Cricket", "Hockey", "Rugby"),
        ("Which Indian athlete won an Olympic gold medal in javelin throw at Tokyo 2020?", "Neeraj Chopra", "Abhinav Bindra", "Milkha Singh", "Sushil Kumar"),
        ("Which sport uses a shuttlecock?", "Badminton", "Tennis", "Table tennis", "Squash"),
        ("How many rings are there in the Olympic symbol?", "Five", "Four", "Six", "Seven"),
        ("Which country is traditionally associated with the martial art of judo?", "Japan", "China", "Brazil", "Thailand"),
        ("Which sport is played in the Davis Cup?", "Tennis", "Cricket", "Football", "Hockey"),
        ("Which Indian cricketer is popularly known as the Little Master?", "Sunil Gavaskar", "Kapil Dev", "Rahul Dravid", "Sourav Ganguly"),
        ("Which sport is associated with the Ashes series?", "Cricket", "Football", "Rugby", "Tennis"),
        ("Which Indian sportsperson is known as the Queen of Indian Track and Field?", "P. T. Usha", "Saina Nehwal", "Mary Kom", "Sakshi Malik"),
        ("Which sport uses terms such as birdie, eagle and bogey?", "Golf", "Tennis", "Badminton", "Hockey"),
        ("Which country won the first Cricket World Cup in 1975?", "West Indies", "India", "Australia", "England"),
        ("Which sport is associated with the Thomas Cup?", "Badminton", "Tennis", "Football", "Table tennis"),
        ("Which Indian boxer is popularly known as Magnificent Mary?", "Mary Kom", "Lovlina Borgohain", "Sarita Devi", "Nikhat Zareen"),
        ("Which sport is played on a court divided by a net and uses a lightweight ball and paddles?", "Table tennis", "Cricket", "Football", "Rugby"),
        ("Which Indian city hosted the 2010 Commonwealth Games?", "New Delhi", "Mumbai", "Chennai", "Bengaluru"),
        ("Which sport is associated with the Ryder Cup?", "Golf", "Tennis", "Cricket", "Hockey"),
        ("How many points is a successful free throw worth in basketball?", "One", "Two", "Three", "Four"),
        ("Which sport is associated with the term 'checkmate'?", "Chess", "Carrom", "Billiards", "Golf"),
        ("Which Indian shooter won gold in the men's 10-metre air rifle event at the 2008 Beijing Olympics?", "Abhinav Bindra", "Gagan Narang", "Rajyavardhan Singh Rathore", "Vijay Kumar"),
        ("Which sport is played in the French Open?", "Tennis", "Golf", "Badminton", "Squash"),
        ("Which country is associated with the traditional sport of sumo wrestling?", "Japan", "South Korea", "China", "Mongolia"),
        ("Which Indian cricketer is known as the Wall?", "Rahul Dravid", "Virender Sehwag", "Yuvraj Singh", "MS Dhoni"),
    ],

    "Medium": [
        ("Which Indian athlete won India's first individual Olympic gold medal?", "Abhinav Bindra", "Neeraj Chopra", "Rajyavardhan Singh Rathore", "Sushil Kumar"),
        ("In which year did India win its first Cricket World Cup?", "1983", "1975", "1987", "1992"),
        ("Who captained India when it won the 1983 Cricket World Cup?", "Kapil Dev", "Sunil Gavaskar", "Mohinder Amarnath", "Ravi Shastri"),
        ("Which Indian badminton player won the 2012 Olympic bronze medal in women's singles?", "Saina Nehwal", "P. V. Sindhu", "Jwala Gutta", "Ashwini Ponnappa"),
        ("Who became the first Indian woman to win an Olympic silver medal?", "P. V. Sindhu", "Saina Nehwal", "Mary Kom", "Karnam Malleswari"),
        ("Which Indian weightlifter won a bronze medal at the 2000 Sydney Olympics?", "Karnam Malleswari", "Mirabai Chanu", "Kunjarani Devi", "Sanjita Chanu"),
        ("Which trophy is awarded to the winner of India's premier first-class cricket competition?", "Ranji Trophy", "Duleep Trophy", "Irani Cup", "Vijay Hazare Trophy"),
        ("Which trophy is associated with India's domestic one-day cricket competition?", "Vijay Hazare Trophy", "Ranji Trophy", "Duleep Trophy", "Irani Cup"),
        ("Which trophy is associated with the India-Pakistan cricket rivalry in some historical Test series?", "None of these; they have played for several bilateral trophies", "Border-Gavaskar Trophy", "Ashes", "Ryder Cup"),
        ("Which country won the 2022 FIFA World Cup?", "Argentina", "France", "Brazil", "Germany"),
        ("Which country won the 2011 Cricket World Cup?", "India", "Australia", "Sri Lanka", "Pakistan"),
        ("Who was the captain of the Indian team that won the 2011 Cricket World Cup?", "MS Dhoni", "Sourav Ganguly", "Rahul Dravid", "Virat Kohli"),
        ("Which Indian chess grandmaster became the country's first Grandmaster in 1988?", "Viswanathan Anand", "Pentala Harikrishna", "D. Gukesh", "Praggnanandhaa"),
        ("Which Indian chess player became the youngest undisputed World Chess Champion in 2024?", "D. Gukesh", "Viswanathan Anand", "R. Praggnanandhaa", "Arjun Erigaisi"),
        ("Which country hosts the famous Tour de France cycling race?", "France", "Italy", "Spain", "Belgium"),
        ("Which sport is associated with the BWF Sudirman Cup?", "Badminton", "Tennis", "Hockey", "Table tennis"),
        ("Which country won the inaugural ICC Men's T20 World Cup in 2007?", "India", "Pakistan", "Australia", "Sri Lanka"),
        ("Which Indian athlete won a silver medal in badminton at the Rio 2016 Olympics?", "P. V. Sindhu", "Saina Nehwal", "Jwala Gutta", "Ashwini Ponnappa"),
        ("Which Indian wrestler won a bronze medal at the 2020 Tokyo Olympics?", "Bajrang Punia", "Sushil Kumar", "Yogeshwar Dutt", "Aman Sehrawat"),
        ("Which Indian athlete won a bronze medal in boxing at the 2020 Tokyo Olympics?", "Lovlina Borgohain", "Mary Kom", "Nikhat Zareen", "Vijender Singh"),
        ("Which country is associated with the All Blacks rugby team?", "New Zealand", "Australia", "South Africa", "England"),
        ("What is the maximum score possible with three darts in one turn in standard darts?", "180", "150", "120", "200"),
        ("Which Grand Slam tennis tournament is played on clay courts?", "French Open", "Wimbledon", "US Open", "Australian Open"),
        ("Which Grand Slam tennis tournament is traditionally played on grass courts?", "Wimbledon", "French Open", "US Open", "Australian Open"),
        ("Which country won the first men's FIFA World Cup in 1930?", "Uruguay", "Brazil", "Italy", "Argentina"),
        ("Which Indian hockey player is widely known as the Wizard of Hockey?", "Dhyan Chand", "Balbir Singh Sr.", "Dhanraj Pillay", "Manpreet Singh"),
        ("Which Indian hockey team won three consecutive Olympic gold medals from 1928 to 1936?", "Indian men's hockey team", "Indian women's hockey team", "British men's hockey team", "Pakistan men's hockey team"),
        ("Which sport is associated with the term 'scrum'?", "Rugby", "Basketball", "Tennis", "Golf"),
        ("Which organisation governs international cricket?", "International Cricket Council", "FIFA", "International Olympic Committee", "World Athletics"),
        ("Which organisation governs international football?", "FIFA", "ICC", "BWF", "World Athletics"),
    ],

    "Hard": [
        ("Who was the first Indian to win an individual Olympic medal after independence?", "K. D. Jadhav", "Abhinav Bindra", "Milkha Singh", "Leander Paes"),
        ("In which sport did K. D. Jadhav win an Olympic medal in 1952?", "Wrestling", "Boxing", "Hockey", "Athletics"),
        ("Who was the first Indian woman to win an Olympic medal?", "Karnam Malleswari", "P. T. Usha", "Saina Nehwal", "Mary Kom"),
        ("Which Indian athlete won the first Olympic medal in badminton for India?", "Saina Nehwal", "P. V. Sindhu", "Prakash Padukone", "Jwala Gutta"),
        ("Who was the first Indian to win the World Chess Championship?", "Viswanathan Anand", "D. Gukesh", "R. Praggnanandhaa", "Dibyendu Barua"),
        ("Which country hosted the first Asian Games in 1951?", "India", "Japan", "Indonesia", "Philippines"),
        ("Where were the first Asian Games held in 1951?", "New Delhi", "Mumbai", "Tokyo", "Manila"),
        ("Which Indian athlete won a silver medal in men's javelin at the 2024 Paris Olympics?", "Neeraj Chopra", "Kishore Jena", "Arshad Nadeem", "D. P. Manu"),
        ("Who won the men's javelin throw gold medal at the 2024 Paris Olympics?", "Arshad Nadeem", "Neeraj Chopra", "Anderson Peters", "Julian Weber"),
        ("Which Indian shooter won two medals at the 2024 Paris Olympics?", "Manu Bhaker", "Anjum Moudgil", "Saurabh Chaudhary", "Abhinav Bindra"),
        ("Which Indian athlete became the first Indian woman to win two medals at a single Olympic Games?", "Manu Bhaker", "P. V. Sindhu", "Saina Nehwal", "Mirabai Chanu"),
        ("Which country won the men's hockey gold medal at the 2020 Tokyo Olympics?", "Belgium", "India", "Australia", "Germany"),
        ("Which country won the men's hockey gold medal at the 2024 Paris Olympics?", "Netherlands", "Germany", "India", "Belgium"),
        ("Which Indian men's hockey team won bronze at the 2024 Paris Olympics?", "India", "Pakistan", "Australia", "Germany"),
        ("Which Indian athlete won a silver medal in weightlifting at the 2020 Tokyo Olympics?", "Mirabai Chanu", "Karnam Malleswari", "Sanjita Chanu", "Kunjarani Devi"),
        ("Which Indian wrestler won a bronze medal in the men's 57 kg freestyle category at the 2024 Paris Olympics?", "Aman Sehrawat", "Bajrang Punia", "Ravi Dahiya", "Yogeshwar Dutt"),
        ("Which Indian athlete won two consecutive Olympic medals in badminton singles in 2016 and 2020?", "P. V. Sindhu", "Saina Nehwal", "Jwala Gutta", "Ashwini Ponnappa"),
        ("Which country won the ICC Men's Cricket World Cup in 2023?", "Australia", "India", "England", "New Zealand"),
        ("Which country won the ICC Men's T20 World Cup in 2024?", "India", "South Africa", "Australia", "England"),
        ("Who captained India to victory in the 2024 ICC Men's T20 World Cup?", "Rohit Sharma", "Virat Kohli", "Hardik Pandya", "Jasprit Bumrah"),
        ("Which country won the ICC Women's Cricket World Cup in 2022?", "Australia", "England", "South Africa", "India"),
        ("Which Indian cricketer was the first to score a double century in men's One Day International cricket?", "Sachin Tendulkar", "Virender Sehwag", "Rohit Sharma", "MS Dhoni"),
        ("Who was the first cricketer to score 10,000 runs in men's Test cricket?", "Sunil Gavaskar", "Sachin Tendulkar", "Allan Border", "Brian Lara"),
        ("Which player holds the record for the highest individual score in men's Test cricket?", "Brian Lara", "Matthew Hayden", "Virender Sehwag", "Don Bradman"),
        ("Which country won the inaugural Rugby World Cup in 1987?", "New Zealand", "Australia", "South Africa", "England"),
        ("Which athlete holds the men's 100-metre world record of 9.58 seconds?", "Usain Bolt", "Carl Lewis", "Yohan Blake", "Justin Gatlin"),
        ("Which athlete holds the women's 100-metre world record?", "Florence Griffith-Joyner", "Shelly-Ann Fraser-Pryce", "Elaine Thompson-Herah", "Marion Jones"),
        ("Which tennis player completed the calendar-year Grand Slam in men's singles in 1969?", "Rod Laver", "Roger Federer", "Rafael Nadal", "Novak Djokovic"),
        ("Which country won the first Women's Cricket World Cup in 1973?", "England", "Australia", "India", "New Zealand"),
        ("Which Indian athlete won the first gold medal for India at the Paralympic Games?", "Murlikant Petkar", "Devendra Jhajharia", "Sumit Antil", "Mariyappan Thangavelu"),
    ]
}


def validate_bank():
    for difficulty, questions in BANK.items():
        if len(questions) != 30:
            raise ValueError(
                f"{difficulty}: Expected 30 questions, found {len(questions)}"
            )

        for index, item in enumerate(questions, 1):
            if len(item) != 5:
                raise ValueError(
                    f"Invalid question format: {difficulty} #{index}"
                )

            question, correct, *wrong = item
            options = [correct] + wrong

            if not all(isinstance(x, str) and x.strip() for x in item):
                raise ValueError(
                    f"Empty field: {difficulty} #{index}"
                )

            if len(set(options)) != 4:
                raise ValueError(
                    f"Duplicate options: {difficulty} #{index}"
                )

    print("Question bank validation successful.")


def main():
    validate_bank()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT title, topic FROM lessons WHERE id = ?",
            (LESSON_ID,)
        )
        existing = cursor.fetchone()

        if existing is None:
            cursor.execute("""
                INSERT INTO lessons
                (id, title, topic, difficulty, content, created_at)
                VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                LESSON_ID,
                LESSON_TITLE,
                TOPIC,
                "Mixed",
                "Learn about Indian and international sports, athletes, tournaments, trophies and major sporting achievements."
            ))

        elif existing != (LESSON_TITLE, TOPIC):
            raise ValueError(
                f"Lesson ID {LESSON_ID} is already occupied by {existing}"
            )

        for difficulty, questions in BANK.items():
            cursor.execute("""
                SELECT id FROM quizzes
                WHERE lesson_id = ? AND difficulty = ?
            """, (LESSON_ID, difficulty))

            quiz_rows = cursor.fetchall()

            if len(quiz_rows) > 1:
                raise ValueError(
                    f"Multiple {difficulty} quizzes found."
                )

            if quiz_rows:
                quiz_id = quiz_rows[0][0]
            else:
                cursor.execute("""
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                """, (
                    LESSON_ID,
                    f"{LESSON_TITLE} - {difficulty}",
                    difficulty
                ))
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

            for item in questions[existing_count:]:
                question, correct, wrong1, wrong2, wrong3 = item

                options = [correct, wrong1, wrong2, wrong3]
                random.shuffle(options)

                correct_letter = "ABCD"[options.index(correct)]

                cursor.execute("""
                    INSERT INTO questions (
                        quiz_id, question,
                        option_a, option_b, option_c, option_d,
                        correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    quiz_id,
                    question,
                    options[0],
                    options[1],
                    options[2],
                    options[3],
                    correct_letter
                ))

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
        print("GK TOPIC 11 INSERTED SUCCESSFULLY")
        print("Indian and World Sports")
        print("Easy: 30")
        print("Medium: 30")
        print("Hard: 30")
        print("TOTAL: 90 QUESTIONS")
        print("====================================")

    except Exception as error:
        connection.rollback()
        print("ERROR:", error)
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
