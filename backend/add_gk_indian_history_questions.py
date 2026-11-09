
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 163
LESSON_TITLE = "Indian History and Freedom Movement"
TOPIC = "General Knowledge"

BANK = {

"Easy": [
("Who is known as the Father of the Nation in India?", "Mahatma Gandhi", "Jawaharlal Nehru", "Sardar Patel", "Subhas Chandra Bose"),
("When did India become independent?", "15 August 1947", "26 January 1950", "2 October 1947", "15 August 1945"),
("Who was the first Prime Minister of independent India?", "Jawaharlal Nehru", "Mahatma Gandhi", "Sardar Patel", "Rajendra Prasad"),
("Who was the first President of India?", "Dr. Rajendra Prasad", "Dr. S. Radhakrishnan", "Jawaharlal Nehru", "Zakir Hussain"),
("Who led the Dandi March in 1930?", "Mahatma Gandhi", "Subhas Chandra Bose", "Bhagat Singh", "Bal Gangadhar Tilak"),
("In which year did the Jallianwala Bagh massacre take place?", "1919", "1920", "1915", "1930"),
("Who was responsible for the Jallianwala Bagh massacre?", "General Dyer", "Lord Curzon", "Lord Mountbatten", "Lord Dalhousie"),
("Who founded the Indian National Congress?", "A. O. Hume", "Mahatma Gandhi", "Dadabhai Naoroji", "Bal Gangadhar Tilak"),
("In which year was the Indian National Congress founded?", "1885", "1905", "1919", "1942"),
("Who gave the slogan 'Give me blood, and I will give you freedom'?", "Subhas Chandra Bose", "Bhagat Singh", "Mahatma Gandhi", "Jawaharlal Nehru"),
("Who was popularly known as Netaji?", "Subhas Chandra Bose", "Bhagat Singh", "Lala Lajpat Rai", "Gopal Krishna Gokhale"),
("Who was known as the Iron Man of India?", "Sardar Vallabhbhai Patel", "Jawaharlal Nehru", "Mahatma Gandhi", "B. R. Ambedkar"),
("Who was known as the Nightingale of India?", "Sarojini Naidu", "Annie Besant", "Kasturba Gandhi", "Vijaya Lakshmi Pandit"),
("Who wrote the book Discovery of India?", "Jawaharlal Nehru", "Mahatma Gandhi", "Rabindranath Tagore", "B. R. Ambedkar"),
("Who wrote the autobiography My Experiments with Truth?", "Mahatma Gandhi", "Jawaharlal Nehru", "Subhas Chandra Bose", "Bal Gangadhar Tilak"),
("Who was popularly known as Shaheed-e-Azam?", "Bhagat Singh", "Chandrashekhar Azad", "Rajguru", "Sukhdev"),
("Who was the first woman president of the Indian National Congress?", "Annie Besant", "Sarojini Naidu", "Indira Gandhi", "Kasturba Gandhi"),
("Who was the first Indian woman president of the Indian National Congress?", "Sarojini Naidu", "Annie Besant", "Sucheta Kripalani", "Aruna Asaf Ali"),
("Which movement was launched by Mahatma Gandhi in 1942?", "Quit India Movement", "Non-Cooperation Movement", "Swadeshi Movement", "Khilafat Movement"),
("What was the slogan of the Quit India Movement?", "Do or Die", "Jai Jawan Jai Kisan", "Inquilab Zindabad", "Vande Mataram"),
("Who founded the Azad Hind Fauj (Indian National Army)?", "Mohan Singh", "Mahatma Gandhi", "Jawaharlal Nehru", "Dadabhai Naoroji"),
("Who led the Indian National Army in its later phase?", "Subhas Chandra Bose", "Bhagat Singh", "Sardar Patel", "Lala Lajpat Rai"),
("Who was the last Viceroy of British India?", "Lord Mountbatten", "Lord Curzon", "Lord Wavell", "Lord Canning"),
("Who was the first Governor-General of independent India?", "Lord Mountbatten", "C. Rajagopalachari", "Lord Wavell", "Warren Hastings"),
("Who was the first Indian Governor-General of independent India?", "C. Rajagopalachari", "Rajendra Prasad", "Jawaharlal Nehru", "Sardar Patel"),
("Who was popularly known as Lokmanya?", "Bal Gangadhar Tilak", "Gopal Krishna Gokhale", "Lala Lajpat Rai", "Bipin Chandra Pal"),
("Who gave the slogan 'Swaraj is my birthright and I shall have it'?", "Bal Gangadhar Tilak", "Mahatma Gandhi", "Subhas Chandra Bose", "Bhagat Singh"),
("Who was popularly known as Punjab Kesari?", "Lala Lajpat Rai", "Bhagat Singh", "Udham Singh", "Sukhdev"),
("Who designed the Indian Constitution's Drafting Committee as its chairman?", "Dr. B. R. Ambedkar", "Jawaharlal Nehru", "Rajendra Prasad", "Sardar Patel"),
("When did the Constitution of India come into effect?", "26 January 1950", "15 August 1947", "26 November 1949", "2 October 1950"),
],

"Medium": [
("What was the immediate cause of the Revolt of 1857?", "Use of greased cartridges", "Introduction of railways", "Partition of Bengal", "Salt tax"),
("Who was the last Mughal emperor during the Revolt of 1857?", "Bahadur Shah Zafar", "Akbar II", "Shah Alam II", "Aurangzeb"),
("Who led the revolt of 1857 in Jhansi?", "Rani Lakshmibai", "Begum Hazrat Mahal", "Sarojini Naidu", "Annie Besant"),
("Who led the revolt of 1857 in Kanpur?", "Nana Sahib", "Tantia Tope", "Kunwar Singh", "Bakht Khan"),
("Who led the revolt of 1857 in Bihar?", "Kunwar Singh", "Nana Sahib", "Mangal Pandey", "Bahadur Shah Zafar"),
("Who was the first major leader associated with the Revolt of 1857 at Barrackpore?", "Mangal Pandey", "Tantia Tope", "Nana Sahib", "Rani Lakshmibai"),
("In which year was Bengal partitioned by Lord Curzon?", "1905", "1901", "1911", "1919"),
("Which movement was launched in response to the Partition of Bengal in 1905?", "Swadeshi Movement", "Quit India Movement", "Civil Disobedience Movement", "Khilafat Movement"),
("In which year was the Partition of Bengal annulled?", "1911", "1905", "1919", "1920"),
("Who founded the Home Rule League in India in 1916 along with Annie Besant?", "Bal Gangadhar Tilak", "Mahatma Gandhi", "Dadabhai Naoroji", "Subhas Chandra Bose"),
("In which year did Mahatma Gandhi return to India from South Africa?", "1915", "1910", "1919", "1922"),
("Which was Gandhi's first major satyagraha in India?", "Champaran Satyagraha", "Dandi March", "Kheda Satyagraha", "Bardoli Satyagraha"),
("In which state did the Champaran Satyagraha take place?", "Bihar", "Gujarat", "Maharashtra", "Punjab"),
("Which movement was launched by Gandhi in 1920?", "Non-Cooperation Movement", "Quit India Movement", "Civil Disobedience Movement", "Swadeshi Movement"),
("Why did Gandhi withdraw the Non-Cooperation Movement in 1922?", "Chauri Chaura incident", "Jallianwala Bagh massacre", "Partition of Bengal", "Simon Commission"),
("In which year did the Chauri Chaura incident take place?", "1922", "1919", "1925", "1930"),
("Which commission arrived in India in 1928 without any Indian member?", "Simon Commission", "Hunter Commission", "Cabinet Mission", "Cripps Mission"),
("What slogan was raised against the Simon Commission?", "Simon Go Back", "Do or Die", "Quit India", "Delhi Chalo"),
("Who died after injuries sustained during a protest against the Simon Commission?", "Lala Lajpat Rai", "Bal Gangadhar Tilak", "Bhagat Singh", "Gopal Krishna Gokhale"),
("In which year did the Dandi March begin?", "1930", "1920", "1928", "1942"),
("From where did Gandhi begin the Dandi March?", "Sabarmati Ashram", "Sevagram Ashram", "Wardha", "Champaran"),
("Which agreement was signed between Gandhi and Lord Irwin in 1931?", "Gandhi-Irwin Pact", "Poona Pact", "Lucknow Pact", "Gandhi-Mountbatten Pact"),
("Who founded the Forward Bloc in 1939?", "Subhas Chandra Bose", "Jawaharlal Nehru", "Sardar Patel", "Bhagat Singh"),
("Who founded the Ghadar Party in 1913 along with other Indian revolutionaries?", "Sohan Singh Bhakna", "Mahatma Gandhi", "Bal Gangadhar Tilak", "Annie Besant"),
("Who was the founder of the Servants of India Society?", "Gopal Krishna Gokhale", "Dadabhai Naoroji", "Lala Lajpat Rai", "Madan Mohan Malaviya"),
("Which pact was signed between Mahatma Gandhi and Dr. B. R. Ambedkar in 1932?", "Poona Pact", "Lucknow Pact", "Gandhi-Irwin Pact", "Delhi Pact"),
("Who was the chairman of the Indian Constituent Assembly?", "Dr. Rajendra Prasad", "Dr. B. R. Ambedkar", "Jawaharlal Nehru", "Sardar Patel"),
("When was the Constitution of India adopted?", "26 November 1949", "26 January 1950", "15 August 1947", "2 October 1949"),
("Which mission proposed a plan for India's constitutional future in 1946?", "Cabinet Mission", "Simon Commission", "Cripps Mission", "Hunter Commission"),
("Who was the chairman of the Drafting Committee of the Indian Constitution?", "Dr. B. R. Ambedkar", "Dr. Rajendra Prasad", "Jawaharlal Nehru", "K. M. Munshi"),
],

"Hard": [
("Which Governor-General introduced the Doctrine of Lapse?", "Lord Dalhousie", "Lord Canning", "Lord Curzon", "Lord Wellesley"),
("Which British Governor-General was in office during the Revolt of 1857?", "Lord Canning", "Lord Dalhousie", "Lord Ripon", "Lord Curzon"),
("Which treaty ended the First Anglo-Maratha War in 1782?", "Treaty of Salbai", "Treaty of Bassein", "Treaty of Purandar", "Treaty of Lahore"),
("Who founded the Indian National Congress in 1885 with the support of Indian leaders?", "A. O. Hume", "Lord Dufferin", "Dadabhai Naoroji", "W. C. Bonnerjee"),
("Who was the first president of the Indian National Congress?", "W. C. Bonnerjee", "A. O. Hume", "Dadabhai Naoroji", "Gopal Krishna Gokhale"),
("Where was the first session of the Indian National Congress held?", "Bombay", "Calcutta", "Madras", "Delhi"),
("Who presided over the 1907 Surat session of the Indian National Congress?", "Rash Behari Ghosh", "Dadabhai Naoroji", "Bal Gangadhar Tilak", "Gopal Krishna Gokhale"),
("Which two groups emerged from the split at the Surat session of 1907?", "Moderates and Extremists", "Socialists and Communists", "Revolutionaries and Loyalists", "Liberals and Conservatives"),
("Which agreement brought the Congress and Muslim League together in 1916?", "Lucknow Pact", "Poona Pact", "Gandhi-Irwin Pact", "Delhi Pact"),
("Who founded the All India Muslim League in 1906?", "Nawab Salimullah Khan and other Muslim leaders", "Mahatma Gandhi", "Jawaharlal Nehru", "Subhas Chandra Bose"),
("Which Act introduced separate electorates for Muslims in British India?", "Indian Councils Act 1909", "Government of India Act 1919", "Government of India Act 1935", "Regulating Act 1773"),
("Which British Act was popularly associated with the Rowlatt Satyagraha?", "Rowlatt Act of 1919", "Indian Councils Act 1909", "Government of India Act 1935", "Charter Act 1813"),
("Who was the Lieutenant Governor of Punjab during the Jallianwala Bagh massacre?", "Michael O'Dwyer", "General Dyer", "Lord Chelmsford", "Lord Irwin"),
("Who assassinated Michael O'Dwyer in London in 1940?", "Udham Singh", "Bhagat Singh", "Chandrashekhar Azad", "Ram Prasad Bismil"),
("Which revolutionary organisation was associated with Bhagat Singh and his companions?", "Hindustan Socialist Republican Association", "Ghadar Party", "Indian National Congress", "Anushilan Samiti"),
("Who threw bombs in the Central Legislative Assembly in 1929 along with Batukeshwar Dutt?", "Bhagat Singh", "Rajguru", "Sukhdev", "Chandrashekhar Azad"),
("Who was popularly known as Azad and died in a police encounter at Alfred Park?", "Chandrashekhar Azad", "Ram Prasad Bismil", "Ashfaqulla Khan", "Surya Sen"),
("Who led the Chittagong Armoury Raid in 1930?", "Surya Sen", "Bhagat Singh", "Rash Behari Bose", "Subhas Chandra Bose"),
("Who founded the Hindustan Republican Association in 1924 with other revolutionaries?", "Ram Prasad Bismil", "Mahatma Gandhi", "Jawaharlal Nehru", "Gopal Krishna Gokhale"),
("Which event involved the looting of a train carrying government funds in 1925?", "Kakori Train Action", "Chauri Chaura incident", "Dandi March", "Bardoli Satyagraha"),
("Who led the Bardoli Satyagraha of 1928?", "Sardar Vallabhbhai Patel", "Mahatma Gandhi", "Jawaharlal Nehru", "Subhas Chandra Bose"),
("Which report was prepared in 1928 by a committee headed by Motilal Nehru?", "Nehru Report", "Simon Report", "Hunter Report", "Cabinet Report"),
("At which Congress session was Poorna Swaraj declared as the goal of the freedom movement?", "Lahore Session, 1929", "Surat Session, 1907", "Bombay Session, 1885", "Lucknow Session, 1916"),
("Who presided over the Lahore Session of the Congress in 1929?", "Jawaharlal Nehru", "Mahatma Gandhi", "Subhas Chandra Bose", "Motilal Nehru"),
("Which date was observed as the first Independence Day by Congress supporters in 1930?", "26 January", "15 August", "2 October", "9 August"),
("Who was the British Prime Minister when the Cabinet Mission came to India in 1946?", "Clement Attlee", "Winston Churchill", "Neville Chamberlain", "Ramsay MacDonald"),
("Which plan announced the partition of British India in June 1947?", "Mountbatten Plan", "Cripps Mission Plan", "Cabinet Mission Plan", "Wavell Plan"),
("Who moved the Objectives Resolution in the Constituent Assembly?", "Jawaharlal Nehru", "Dr. B. R. Ambedkar", "Dr. Rajendra Prasad", "Sardar Patel"),
("Who served as the temporary chairman of the Constituent Assembly at its first meeting?", "Sachchidananda Sinha", "Dr. Rajendra Prasad", "Jawaharlal Nehru", "B. N. Rau"),
("Who was the constitutional adviser to the Constituent Assembly?", "B. N. Rau", "K. M. Munshi", "Alladi Krishnaswamy Iyer", "Dr. B. R. Ambedkar"),
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
                raise ValueError(f"Invalid question format: {difficulty} #{index}")

            question, correct, *wrong = item
            options = [correct] + wrong

            if not all(isinstance(value, str) and value.strip() for value in item):
                raise ValueError(f"Empty value: {difficulty} #{index}")

            if len(set(options)) != 4:
                raise ValueError(f"Duplicate options: {difficulty} #{index}")

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
                "Learn about Indian history, freedom fighters and the independence movement."
            ))
            print("Lesson created successfully.")

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
                raise ValueError(f"Multiple {difficulty} quizzes found.")

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
                        quiz_id,
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
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

        print("\n======================================")
        print("GK TOPIC 3 INSERTED SUCCESSFULLY")
        print("Indian History and Freedom Movement")
        print("Easy: 30")
        print("Medium: 30")
        print("Hard: 30")
        print("TOTAL: 90 QUESTIONS")
        print("======================================")

    except Exception as error:
        connection.rollback()
        print("ERROR:", error)
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
