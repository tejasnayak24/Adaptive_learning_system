
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 173
LESSON_TITLE = "Important Days, Books, Authors and Awards"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("When is India's Independence Day celebrated?", "15 August", "26 January", "2 October", "14 November"),
        ("When is India's Republic Day celebrated?", "26 January", "15 August", "5 September", "2 October"),
        ("When is Gandhi Jayanti celebrated?", "2 October", "14 November", "15 August", "26 January"),
        ("When is World Environment Day observed?", "5 June", "22 April", "21 March", "16 September"),
        ("When is International Women's Day celebrated?", "8 March", "1 May", "5 June", "10 December"),
        ("When is International Yoga Day observed?", "21 June", "5 June", "11 July", "1 December"),
        ("When is World Health Day celebrated?", "7 April", "22 April", "1 December", "5 June"),
        ("When is World AIDS Day observed?", "1 December", "14 November", "10 December", "7 April"),
        ("When is Children's Day celebrated in India?", "14 November", "20 November", "5 September", "2 October"),
        ("When is Teachers' Day celebrated in India?", "5 September", "14 November", "15 August", "26 January"),
        ("Who wrote the national anthem of India, Jana Gana Mana?", "Rabindranath Tagore", "Bankim Chandra Chatterjee", "Sarojini Naidu", "Subramania Bharati"),
        ("Who wrote the Indian national song, Vande Mataram?", "Bankim Chandra Chatterjee", "Rabindranath Tagore", "Mahatma Gandhi", "Jawaharlal Nehru"),
        ("Who wrote the book The Discovery of India?", "Jawaharlal Nehru", "Mahatma Gandhi", "B. R. Ambedkar", "Rabindranath Tagore"),
        ("Who wrote the autobiography My Experiments with Truth?", "Mahatma Gandhi", "Jawaharlal Nehru", "Sardar Patel", "Subhas Chandra Bose"),
        ("Who wrote the famous play Romeo and Juliet?", "William Shakespeare", "Charles Dickens", "Jane Austen", "George Orwell"),
        ("Who wrote the Harry Potter book series?", "J. K. Rowling", "Enid Blyton", "Agatha Christie", "Suzanne Collins"),
        ("Who wrote The Jungle Book?", "Rudyard Kipling", "Mark Twain", "Lewis Carroll", "R. K. Narayan"),
        ("Who wrote the novel Malgudi Days?", "R. K. Narayan", "Mulk Raj Anand", "Ruskin Bond", "Khushwant Singh"),
        ("Which award is India's highest civilian honour?", "Bharat Ratna", "Padma Shri", "Padma Bhushan", "Padma Vibhushan"),
        ("Which award is given for outstanding contributions to Indian cinema?", "Dadasaheb Phalke Award", "Arjuna Award", "Jnanpith Award", "Bharat Ratna"),
        ("Which award is associated with excellence in literature in India?", "Jnanpith Award", "Arjuna Award", "Dronacharya Award", "Filmfare Award"),
        ("Which award is given for outstanding achievements in sports in India?", "Arjuna Award", "Dadasaheb Phalke Award", "Jnanpith Award", "Sahitya Akademi Award"),
        ("Which award recognises outstanding coaches in Indian sports?", "Dronacharya Award", "Arjuna Award", "Bharat Ratna", "Padma Shri"),
        ("Which international award is famous for recognising achievements in peace, literature and science?", "Nobel Prize", "Booker Prize", "Pulitzer Prize", "Grammy Award"),
        ("Which award is associated with excellence in music recording?", "Grammy Award", "Oscar Award", "Booker Prize", "Nobel Prize"),
        ("Which award is presented for excellence in motion pictures by the Academy of Motion Picture Arts and Sciences?", "Academy Award (Oscar)", "Grammy Award", "Tony Award", "Pulitzer Prize"),
        ("Which award is associated with outstanding English-language fiction published in the UK or Ireland?", "Booker Prize", "Nobel Peace Prize", "Grammy Award", "Arjuna Award"),
        ("Who wrote the novel The Guide?", "R. K. Narayan", "Rabindranath Tagore", "Vikram Seth", "Amitav Ghosh"),
        ("Who wrote the novel God of Small Things?", "Arundhati Roy", "Jhumpa Lahiri", "Kiran Desai", "Anita Desai"),
        ("When is World Literacy Day observed?", "8 September", "5 June", "21 June", "10 December"),
    ],

    "Medium": [
        ("When is National Science Day celebrated in India?", "28 February", "15 January", "5 June", "11 May"),
        ("When is National Technology Day celebrated in India?", "11 May", "28 February", "14 November", "26 January"),
        ("When is Constitution Day observed in India?", "26 November", "26 January", "15 August", "2 October"),
        ("When is National Voters' Day celebrated in India?", "25 January", "26 January", "15 August", "10 December"),
        ("When is World Population Day observed?", "11 July", "5 June", "22 April", "1 December"),
        ("When is International Literacy Day observed?", "8 September", "5 September", "14 November", "21 June"),
        ("When is World Water Day observed?", "22 March", "22 April", "5 June", "16 September"),
        ("When is International Human Rights Day celebrated?", "10 December", "1 December", "8 March", "24 October"),
        ("Who wrote the novel Train to Pakistan?", "Khushwant Singh", "R. K. Narayan", "Mulk Raj Anand", "Salman Rushdie"),
        ("Who wrote the novel A Suitable Boy?", "Vikram Seth", "Amitav Ghosh", "Arundhati Roy", "Rohinton Mistry"),
        ("Who wrote the novel Midnight's Children?", "Salman Rushdie", "Vikram Seth", "Amitav Ghosh", "R. K. Narayan"),
        ("Who wrote the book Wings of Fire?", "A. P. J. Abdul Kalam", "Vikram Sarabhai", "Homi J. Bhabha", "C. V. Raman"),
        ("Who co-authored Wings of Fire with A. P. J. Abdul Kalam?", "Arun Tiwari", "R. K. Narayan", "Khushwant Singh", "Vikram Seth"),
        ("Who wrote the novel The White Tiger?", "Aravind Adiga", "Amitav Ghosh", "Salman Rushdie", "Chetan Bhagat"),
        ("Who wrote the book The God of Small Things?", "Arundhati Roy", "Kiran Desai", "Anita Desai", "Jhumpa Lahiri"),
        ("Who wrote the novel The Inheritance of Loss?", "Kiran Desai", "Arundhati Roy", "Anita Desai", "Jhumpa Lahiri"),
        ("Who wrote the book The Argumentative Indian?", "Amartya Sen", "Abhijit Banerjee", "Raghuram Rajan", "Shashi Tharoor"),
        ("Who wrote the book India After Gandhi?", "Ramachandra Guha", "Bipan Chandra", "Romila Thapar", "Irfan Habib"),
        ("Who wrote the novel The Palace of Illusions?", "Chitra Banerjee Divakaruni", "Anita Desai", "Jhumpa Lahiri", "Kiran Desai"),
        ("Who wrote the book The Immortals of Meluha?", "Amish Tripathi", "Ashwin Sanghi", "Chetan Bhagat", "Devdutt Pattanaik"),
        ("Which Indian literary award is presented by the Sahitya Akademi?", "Sahitya Akademi Award", "Dadasaheb Phalke Award", "Dronacharya Award", "Arjuna Award"),
        ("Which award is considered India's highest award in the field of literature?", "Jnanpith Award", "Padma Shri", "Arjuna Award", "Dadasaheb Phalke Award"),
        ("Which international prize is awarded for outstanding journalism and literature in the United States?", "Pulitzer Prize", "Booker Prize", "Nobel Prize", "Grammy Award"),
        ("Which Nobel Prize category recognises achievements in economic sciences?", "Economic Sciences", "Political Sciences", "Computer Sciences", "Engineering Sciences"),
        ("Which Indian poet won the Nobel Prize in Literature in 1913?", "Rabindranath Tagore", "Sarojini Naidu", "Sri Aurobindo", "Kazi Nazrul Islam"),
        ("Which Indian-origin author won the Booker Prize in 1997 for The God of Small Things?", "Arundhati Roy", "Kiran Desai", "Jhumpa Lahiri", "Anita Desai"),
        ("Who wrote the play Hamlet?", "William Shakespeare", "John Milton", "Geoffrey Chaucer", "Christopher Marlowe"),
        ("Who wrote Pride and Prejudice?", "Jane Austen", "Emily Bronte", "Virginia Woolf", "Mary Shelley"),
        ("Who wrote the novel Oliver Twist?", "Charles Dickens", "Thomas Hardy", "George Eliot", "Mark Twain"),
        ("Who wrote the detective novel Murder on the Orient Express?", "Agatha Christie", "Arthur Conan Doyle", "Dan Brown", "Ian Fleming"),
    ],

    "Hard": [
        ("When is World Heritage Day, also known as the International Day for Monuments and Sites, observed?", "18 April", "18 May", "5 June", "24 October"),
        ("When is World Meteorological Day observed?", "23 March", "22 March", "5 June", "16 September"),
        ("When is International Day of Peace observed?", "21 September", "24 October", "10 December", "8 March"),
        ("When is United Nations Day celebrated?", "24 October", "21 September", "10 December", "5 June"),
        ("When is World Food Day observed?", "16 October", "5 June", "22 April", "1 December"),
        ("When is International Mother Language Day observed?", "21 February", "21 March", "8 March", "14 November"),
        ("When is World Press Freedom Day observed?", "3 May", "1 May", "5 June", "10 December"),
        ("When is International Day of the Girl Child observed?", "11 October", "8 March", "20 November", "24 October"),
        ("Who wrote the historical novel The Last Mughal?", "William Dalrymple", "Ramachandra Guha", "Vikram Seth", "Salman Rushdie"),
        ("Who wrote the book The Great Indian Novel?", "Shashi Tharoor", "Amitav Ghosh", "Vikram Seth", "Khushwant Singh"),
        ("Who wrote the novel The Shadow Lines?", "Amitav Ghosh", "Rohinton Mistry", "Aravind Adiga", "Salman Rushdie"),
        ("Who wrote the novel A Fine Balance?", "Rohinton Mistry", "Amitav Ghosh", "Vikram Seth", "Arundhati Roy"),
        ("Who wrote the novel The Namesake?", "Jhumpa Lahiri", "Kiran Desai", "Anita Desai", "Arundhati Roy"),
        ("Who wrote the novel The Blue Umbrella?", "Ruskin Bond", "R. K. Narayan", "Mulk Raj Anand", "Khushwant Singh"),
        ("Who wrote the book The Discovery of India while imprisoned at Ahmednagar Fort?", "Jawaharlal Nehru", "Mahatma Gandhi", "Sardar Patel", "B. R. Ambedkar"),
        ("Who wrote the Sanskrit work Arthashastra?", "Kautilya", "Kalidasa", "Banabhatta", "Patanjali"),
        ("Who wrote the ancient Indian drama Abhijnanashakuntalam?", "Kalidasa", "Bhavabhuti", "Bharavi", "Bhasa"),
        ("Who wrote the Tamil classic Tirukkural?", "Thiruvalluvar", "Ilango Adigal", "Kambar", "Avvaiyar"),
        ("Which author wrote the epic poem Paradise Lost?", "John Milton", "William Shakespeare", "John Keats", "William Wordsworth"),
        ("Who wrote the novel One Hundred Years of Solitude?", "Gabriel García Márquez", "Pablo Neruda", "Jorge Luis Borges", "Mario Vargas Llosa"),
        ("Which Indian author won the Jnanpith Award for the novel The English Teacher?", "No; R. K. Narayan did not win the Jnanpith Award", "R. K. Narayan", "Mulk Raj Anand", "Khushwant Singh"),
        ("Who was the first woman to receive the Jnanpith Award?", "Ashapurna Devi", "Mahasweta Devi", "Amrita Pritam", "Mahadevi Varma"),
        ("Who was the first recipient of the Sahitya Akademi Award in English?", "R. K. Narayan", "Mulk Raj Anand", "Nissim Ezekiel", "Khushwant Singh"),
        ("Which Indian author won the 1992 Jnanpith Award for contributions to literature in Assamese?", "Birendra Kumar Bhattacharya", "Indira Goswami", "Lakshminath Bezbaroa", "Homen Borgohain"),
        ("Which Indian writer received the Nobel Prize in Literature in 1913 for Gitanjali?", "Rabindranath Tagore", "Bankim Chandra Chatterjee", "Sarojini Naidu", "Sri Aurobindo"),
        ("Which organisation awards the Nobel Prizes?", "Nobel Foundation and designated awarding institutions", "United Nations General Assembly", "UNESCO alone", "International Court of Justice"),
        ("Which Nobel Prize category was not part of Alfred Nobel's original will but was established later?", "Economic Sciences", "Physics", "Chemistry", "Literature"),
        ("Which Indian-born economist shared the 2019 Nobel Prize in Economic Sciences?", "Abhijit Banerjee", "Amartya Sen", "Raghuram Rajan", "Kaushik Basu"),
        ("Which Indian-origin author won the 2022 Booker Prize for the novel The Seven Moons of Maali Almeida?", "Shehan Karunatilaka", "Geetanjali Shree", "Arundhati Roy", "Amitav Ghosh"),
        ("Which author won the 2022 International Booker Prize for Tomb of Sand?", "Geetanjali Shree", "Arundhati Roy", "Kiran Desai", "Jhumpa Lahiri"),
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

            if not all(isinstance(value, str) and value.strip() for value in item):
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
                "Learn about important national and international days, famous books, authors and major literary and international awards."
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
        print("GK TOPIC 13 INSERTED SUCCESSFULLY")
        print("Important Days, Books, Authors and Awards")
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
