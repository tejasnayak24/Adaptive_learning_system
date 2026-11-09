
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 180
LESSON_TITLE = "Important Indian Personalities, Leaders, Scientists and Social Reformers"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Who is known as the Father of the Nation in India?", "Mahatma Gandhi", "Jawaharlal Nehru", "Subhas Chandra Bose", "Sardar Patel"),
        ("Who was the first Prime Minister of independent India?", "Jawaharlal Nehru", "Mahatma Gandhi", "Rajendra Prasad", "Lal Bahadur Shastri"),
        ("Who was the first President of India?", "Dr. Rajendra Prasad", "Dr. S. Radhakrishnan", "Zakir Hussain", "V. V. Giri"),
        ("Who is popularly known as the Iron Man of India?", "Sardar Vallabhbhai Patel", "Bhagat Singh", "Bal Gangadhar Tilak", "Subhas Chandra Bose"),
        ("Who gave the slogan 'Jai Jawan Jai Kisan'?", "Lal Bahadur Shastri", "Jawaharlal Nehru", "Mahatma Gandhi", "Indira Gandhi"),
        ("Who is known as the Missile Man of India?", "A. P. J. Abdul Kalam", "Homi J. Bhabha", "Vikram Sarabhai", "C. V. Raman"),
        ("Who was the first woman Prime Minister of India?", "Indira Gandhi", "Sarojini Naidu", "Pratibha Patil", "Sushma Swaraj"),
        ("Who was the first woman President of India?", "Pratibha Patil", "Indira Gandhi", "Droupadi Murmu", "Sarojini Naidu"),
        ("Who wrote the Indian national anthem?", "Rabindranath Tagore", "Bankim Chandra Chatterjee", "Sarojini Naidu", "Munshi Premchand"),
        ("Who wrote 'Vande Mataram'?", "Bankim Chandra Chatterjee", "Rabindranath Tagore", "Subramania Bharati", "Muhammad Iqbal"),
        ("Who is known as the Nightingale of India?", "Sarojini Naidu", "Annie Besant", "Indira Gandhi", "Kasturba Gandhi"),
        ("Who founded the Arya Samaj?", "Swami Dayanand Saraswati", "Swami Vivekananda", "Raja Ram Mohan Roy", "Ishwar Chandra Vidyasagar"),
        ("Who founded the Brahmo Samaj?", "Raja Ram Mohan Roy", "Swami Dayanand Saraswati", "Jyotirao Phule", "Ramanuja"),
        ("Who founded the Ramakrishna Mission?", "Swami Vivekananda", "Ramakrishna Paramahamsa", "Rabindranath Tagore", "Mahatma Gandhi"),
        ("Who is known as the Father of the Indian Constitution?", "Dr. B. R. Ambedkar", "Dr. Rajendra Prasad", "Jawaharlal Nehru", "Sardar Patel"),
        ("Who was the first Indian to win a Nobel Prize?", "Rabindranath Tagore", "C. V. Raman", "Mother Teresa", "Amartya Sen"),
        ("Who won the Nobel Prize in Physics in 1930?", "C. V. Raman", "Homi J. Bhabha", "Satyendra Nath Bose", "Vikram Sarabhai"),
        ("Who is known as the Father of the Indian Space Programme?", "Vikram Sarabhai", "A. P. J. Abdul Kalam", "Homi J. Bhabha", "Satish Dhawan"),
        ("Who is popularly known as the Father of India's Green Revolution?", "M. S. Swaminathan", "Verghese Kurien", "C. Subramaniam", "Norman Borlaug"),
        ("Who is known as the Father of the White Revolution in India?", "Verghese Kurien", "M. S. Swaminathan", "Homi Bhabha", "Vikram Sarabhai"),
        ("Who was the famous queen of Jhansi during the Revolt of 1857?", "Rani Lakshmibai", "Begum Hazrat Mahal", "Ahilyabai Holkar", "Razia Sultan"),
        ("Who was popularly known as Netaji?", "Subhas Chandra Bose", "Bhagat Singh", "Chandrashekhar Azad", "Lala Lajpat Rai"),
        ("Who founded the Indian National Army's first version in 1942?", "Mohan Singh", "Subhas Chandra Bose", "Mahatma Gandhi", "Jawaharlal Nehru"),
        ("Who is known as the Punjab Kesari?", "Lala Lajpat Rai", "Bhagat Singh", "Udham Singh", "Sukhdev"),
        ("Who was a prominent revolutionary associated with the Kakori train action?", "Ram Prasad Bismil", "Dadabhai Naoroji", "Gopal Krishna Gokhale", "Surendranath Banerjee"),
        ("Who was the first Indian woman to go to space?", "Kalpana Chawla", "Sunita Williams", "Bachendri Pal", "Tessy Thomas"),
        ("Who was the first Indian woman to climb Mount Everest?", "Bachendri Pal", "Santosh Yadav", "Arunima Sinha", "Kalpana Chawla"),
        ("Who is known as the Father of the Indian Green Revolution's dairy counterpart?", "Verghese Kurien", "M. S. Swaminathan", "Homi Bhabha", "C. V. Raman"),
        ("Who was the first Indian woman to become the President of the Indian National Congress?", "Annie Besant", "Sarojini Naidu", "Vijaya Lakshmi Pandit", "Sucheta Kripalani"),
        ("Who was the first woman Chief Minister of an Indian state?", "Sucheta Kripalani", "Indira Gandhi", "Jayalalithaa", "Mayawati"),
    ],

    "Medium": [
        ("Who founded the Satyashodhak Samaj?", "Jyotirao Phule", "Raja Ram Mohan Roy", "Swami Vivekananda", "Ishwar Chandra Vidyasagar"),
        ("Who worked extensively for women's education in Maharashtra along with Jyotirao Phule?", "Savitribai Phule", "Sarojini Naidu", "Annie Besant", "Kasturba Gandhi"),
        ("Who founded the Self-Respect Movement?", "Periyar E. V. Ramasamy", "C. Rajagopalachari", "K. Kamaraj", "B. R. Ambedkar"),
        ("Who founded the Aligarh Movement?", "Sir Syed Ahmad Khan", "Maulana Abul Kalam Azad", "Muhammad Ali Jinnah", "Allama Iqbal"),
        ("Who founded the Servants of India Society?", "Gopal Krishna Gokhale", "Bal Gangadhar Tilak", "Lala Lajpat Rai", "Dadabhai Naoroji"),
        ("Who is known as the Grand Old Man of India?", "Dadabhai Naoroji", "Gopal Krishna Gokhale", "Surendranath Banerjee", "M. G. Ranade"),
        ("Who wrote the book 'The Discovery of India'?", "Jawaharlal Nehru", "Mahatma Gandhi", "Rabindranath Tagore", "B. R. Ambedkar"),
        ("Who wrote 'Hind Swaraj'?", "Mahatma Gandhi", "Jawaharlal Nehru", "Bal Gangadhar Tilak", "Subhas Chandra Bose"),
        ("Who wrote the book 'Annihilation of Caste'?", "Dr. B. R. Ambedkar", "Jyotirao Phule", "Periyar", "Mahatma Gandhi"),
        ("Who wrote 'Gitanjali'?", "Rabindranath Tagore", "Bankim Chandra Chatterjee", "Sarojini Naidu", "R. K. Narayan"),
        ("Who was the first Indian woman to preside over the Indian National Congress?", "Sarojini Naidu", "Annie Besant", "Vijaya Lakshmi Pandit", "Sucheta Kripalani"),
        ("Who was the first Indian woman to become the President of the United Nations General Assembly?", "Vijaya Lakshmi Pandit", "Sarojini Naidu", "Indira Gandhi", "Pratibha Patil"),
        ("Who was the first Indian to become Governor-General of independent India?", "C. Rajagopalachari", "Lord Mountbatten", "Dr. Rajendra Prasad", "Jawaharlal Nehru"),
        ("Who was the chairman of the Drafting Committee of the Indian Constitution?", "Dr. B. R. Ambedkar", "Jawaharlal Nehru", "Sardar Patel", "B. N. Rau"),
        ("Who served as the first Deputy Prime Minister of India?", "Sardar Vallabhbhai Patel", "Morarji Desai", "Lal Bahadur Shastri", "Jagjivan Ram"),
        ("Who was the first woman to receive the Bharat Ratna?", "Indira Gandhi", "Mother Teresa", "Sarojini Naidu", "M. S. Subbulakshmi"),
        ("Who was the first recipient of the Bharat Ratna?", "C. Rajagopalachari, S. Radhakrishnan and C. V. Raman", "Jawaharlal Nehru alone", "Mahatma Gandhi", "Sardar Patel alone"),
        ("Who received the Nobel Prize in Economics in 1998?", "Amartya Sen", "Abhijit Banerjee", "Manmohan Singh", "Raghuram Rajan"),
        ("Who was the first Indian woman to win an Olympic medal?", "Karnam Malleswari", "P. T. Usha", "Saina Nehwal", "Mary Kom"),
        ("Who was the first Indian to win an individual Olympic gold medal?", "Abhinav Bindra", "Neeraj Chopra", "Rajyavardhan Singh Rathore", "Leander Paes"),
        ("Who is known as the Flying Sikh?", "Milkha Singh", "P. T. Usha", "Kapil Dev", "Dhanraj Pillay"),
        ("Who was the first Indian woman to win an Olympic medal in badminton?", "Saina Nehwal", "P. V. Sindhu", "Jwala Gutta", "Ashwini Ponnappa"),
        ("Who became the first Indian woman to win two Olympic medals?", "P. V. Sindhu", "Saina Nehwal", "Mary Kom", "Sakshi Malik"),
        ("Who was the first Indian woman to win an Olympic boxing medal?", "Mary Kom", "Lovlina Borgohain", "Sarita Devi", "Nikhat Zareen"),
        ("Who is popularly known as the Father of Indian Cinema?", "Dadasaheb Phalke", "Satyajit Ray", "Raj Kapoor", "Guru Dutt"),
        ("Who directed the film 'Pather Panchali'?", "Satyajit Ray", "Bimal Roy", "Dadasaheb Phalke", "Mrinal Sen"),
        ("Who was the first Indian woman to receive the Nobel Peace Prize?", "Mother Teresa", "Indira Gandhi", "Sarojini Naidu", "Aruna Asaf Ali"),
        ("Which Indian scientist is associated with the Raman Effect?", "C. V. Raman", "Homi Bhabha", "S. N. Bose", "Meghnad Saha"),
        ("Which Indian scientist is associated with the Bose-Einstein statistics?", "Satyendra Nath Bose", "C. V. Raman", "Vikram Sarabhai", "Jagadish Chandra Bose"),
        ("Who was the first Indian woman to receive the Jnanpith Award?", "Ashapurna Devi", "Mahasweta Devi", "Amrita Pritam", "Mahadevi Varma"),
    ],

    "Hard": [
        ("Who founded the Prarthana Samaj in 1867?", "Atmaram Pandurang", "Raja Ram Mohan Roy", "Jyotirao Phule", "Swami Dayanand Saraswati"),
        ("Who was a prominent leader of the Prarthana Samaj and social reformer?", "M. G. Ranade", "Bal Gangadhar Tilak", "Bhagat Singh", "Subhas Chandra Bose"),
        ("Who founded the Theosophical Society in India along with its international founders?", "Annie Besant", "Sarojini Naidu", "Savitribai Phule", "Kasturba Gandhi"),
        ("Who founded the Indian Association in 1876 along with Ananda Mohan Bose?", "Surendranath Banerjee", "Dadabhai Naoroji", "Gopal Krishna Gokhale", "Bal Gangadhar Tilak"),
        ("Who established the Deccan Education Society with other associates?", "Bal Gangadhar Tilak", "Mahatma Gandhi", "Sardar Patel", "Subhas Chandra Bose"),
        ("Who founded the newspaper 'Kesari'?", "Bal Gangadhar Tilak", "Gopal Krishna Gokhale", "Dadabhai Naoroji", "Lala Lajpat Rai"),
        ("Who founded the newspaper 'The Hindu' along with other associates?", "G. Subramania Iyer", "C. Rajagopalachari", "Annie Besant", "M. G. Ranade"),
        ("Who founded the newspaper 'Young India' as a publication associated with the Indian freedom movement?", "Mahatma Gandhi", "Jawaharlal Nehru", "Subhas Chandra Bose", "B. R. Ambedkar"),
        ("Who founded the Indian Home Rule League in Maharashtra in 1916?", "Bal Gangadhar Tilak", "Annie Besant", "Mahatma Gandhi", "Lala Lajpat Rai"),
        ("Who founded the All India Home Rule League in 1916?", "Annie Besant", "Sarojini Naidu", "Vijaya Lakshmi Pandit", "Kasturba Gandhi"),
        ("Who was the first Indian woman to become President of the Indian National Congress?", "Annie Besant", "Sarojini Naidu", "Indira Gandhi", "Vijaya Lakshmi Pandit"),
        ("Who was the first Indian woman to become the President of the Indian National Congress?", "Sarojini Naidu", "Annie Besant", "Aruna Asaf Ali", "Sucheta Kripalani"),
        ("Who founded the Bahishkrit Hitakarini Sabha in 1924?", "Dr. B. R. Ambedkar", "Jyotirao Phule", "Periyar", "Mahatma Gandhi"),
        ("Who led the Mahad Satyagraha in 1927?", "Dr. B. R. Ambedkar", "Mahatma Gandhi", "Sardar Patel", "Jawaharlal Nehru"),
        ("Who founded the Harijan Sevak Sangh in 1932?", "Mahatma Gandhi", "Dr. B. R. Ambedkar", "Jawaharlal Nehru", "Rabindranath Tagore"),
        ("Who was the founder of the Indian Statistical Institute?", "P. C. Mahalanobis", "C. V. Raman", "Homi Bhabha", "Meghnad Saha"),
        ("Which Indian scientist developed the Mahalanobis distance?", "P. C. Mahalanobis", "S. N. Bose", "C. V. Raman", "Jagadish Chandra Bose"),
        ("Who founded the Tata Institute of Fundamental Research?", "Homi J. Bhabha", "Vikram Sarabhai", "A. P. J. Abdul Kalam", "Satyendra Nath Bose"),
        ("Who founded the Indian Institute of Science with major support from Jamsetji Tata and others?", "Jamsetji Tata was its principal founder and benefactor", "Homi Bhabha", "Vikram Sarabhai", "C. V. Raman"),
        ("Which Indian scientist is associated with the discovery of the Raman Effect?", "C. V. Raman", "Homi Bhabha", "Meghnad Saha", "S. N. Bose"),
        ("Which Indian physicist developed the Saha ionisation equation?", "Meghnad Saha", "C. V. Raman", "Homi Bhabha", "S. N. Bose"),
        ("Who is associated with the development of India's first indigenous supercomputer PARAM 8000?", "Vijay Bhatkar", "A. P. J. Abdul Kalam", "Vikram Sarabhai", "Homi Bhabha"),
        ("Who was the first Indian woman to receive the Ramon Magsaysay Award?", "Kiran Bedi", "Mother Teresa", "Aruna Roy", "Medha Patkar"),
        ("Who founded the Self-Employed Women's Association (SEWA)?", "Ela Bhatt", "Medha Patkar", "Aruna Roy", "Kiran Bedi"),
        ("Who founded the Bachpan Bachao Andolan?", "Kailash Satyarthi", "Anna Hazare", "Verghese Kurien", "Baba Amte"),
        ("Who founded the Narmada Bachao Andolan along with other activists?", "Medha Patkar", "Ela Bhatt", "Kiran Bedi", "Aruna Roy"),
        ("Who founded the Mazdoor Kisan Shakti Sangathan?", "Aruna Roy", "Ela Bhatt", "Medha Patkar", "Kiran Bedi"),
        ("Which Indian social reformer founded the Anandwan community for people affected by leprosy?", "Baba Amte", "Vinoba Bhave", "Kailash Satyarthi", "Jayaprakash Narayan"),
        ("Who initiated the Bhoodan Movement?", "Vinoba Bhave", "Jayaprakash Narayan", "Mahatma Gandhi", "Sardar Patel"),
        ("Who was awarded the Nobel Peace Prize in 2014 jointly with Kailash Satyarthi?", "Malala Yousafzai", "Mother Teresa", "Wangari Maathai", "Aung San Suu Kyi"),
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
                "Learn about important Indian freedom fighters, political leaders, scientists, writers, social reformers and sports personalities."
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
        print("GK TOPIC 20 INSERTED SUCCESSFULLY")
        print("Important Indian Personalities, Leaders, Scientists and Social Reformers")
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
