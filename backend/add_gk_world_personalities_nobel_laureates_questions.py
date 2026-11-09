
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 198
LESSON_TITLE = "Famous Personalities, World Leaders, Nobel Laureates and Global Achievements"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Who was the first person to walk on the Moon?", "Neil Armstrong", "Buzz Aldrin", "Yuri Gagarin", "Michael Collins"),
        ("Who was the first woman to travel into space?", "Valentina Tereshkova", "Sally Ride", "Mae Jemison", "Kalpana Chawla"),
        ("Who is known as the Father of Modern Physics?", "Albert Einstein", "Isaac Newton", "Galileo Galilei", "Niels Bohr"),
        ("Who developed the theory of relativity?", "Albert Einstein", "Isaac Newton", "Charles Darwin", "Nikola Tesla"),
        ("Who is associated with the discovery of gravity through the law of universal gravitation?", "Isaac Newton", "Albert Einstein", "James Watt", "Michael Faraday"),
        ("Who is known for developing the theory of evolution by natural selection?", "Charles Darwin", "Gregor Mendel", "Louis Pasteur", "Alexander Fleming"),
        ("Who discovered penicillin?", "Alexander Fleming", "Edward Jenner", "Robert Koch", "Joseph Lister"),
        ("Who is known as the Father of Modern Chemistry?", "Antoine Lavoisier", "Dmitri Mendeleev", "John Dalton", "Robert Boyle"),
        ("Who invented the telephone?", "Alexander Graham Bell", "Thomas Edison", "Nikola Tesla", "Guglielmo Marconi"),
        ("Who is commonly credited with developing the practical incandescent light bulb?", "Thomas Edison", "James Watt", "Alexander Fleming", "Louis Pasteur"),
        ("Who is known as the Father of Computers?", "Charles Babbage", "Alan Turing", "John von Neumann", "Bill Gates"),
        ("Who founded Microsoft along with Paul Allen?", "Bill Gates", "Steve Jobs", "Mark Zuckerberg", "Larry Page"),
        ("Who co-founded Apple with Steve Wozniak?", "Steve Jobs", "Bill Gates", "Jeff Bezos", "Elon Musk"),
        ("Who founded Amazon?", "Jeff Bezos", "Larry Ellison", "Mark Zuckerberg", "Tim Cook"),
        ("Who founded Facebook?", "Mark Zuckerberg", "Jack Dorsey", "Larry Page", "Sergey Brin"),
        ("Who was the first President of the United States?", "George Washington", "Abraham Lincoln", "John Adams", "Thomas Jefferson"),
        ("Who was the first woman Prime Minister of the United Kingdom?", "Margaret Thatcher", "Theresa May", "Queen Victoria", "Angela Merkel"),
        ("Who became the first Black President of South Africa?", "Nelson Mandela", "Desmond Tutu", "Thabo Mbeki", "Jacob Zuma"),
        ("Who was the leader of the Indian independence movement known for non-violence?", "Mahatma Gandhi", "Subhas Chandra Bose", "Bhagat Singh", "Bal Gangadhar Tilak"),
        ("Who was known as the Iron Lady of Britain?", "Margaret Thatcher", "Indira Gandhi", "Angela Merkel", "Golda Meir"),
        ("Who was the first Secretary-General of the United Nations?", "Trygve Lie", "Kofi Annan", "U Thant", "Ban Ki-moon"),
        ("Who wrote the play Romeo and Juliet?", "William Shakespeare", "Charles Dickens", "George Orwell", "Jane Austen"),
        ("Who wrote the novel Oliver Twist?", "Charles Dickens", "William Shakespeare", "Mark Twain", "Leo Tolstoy"),
        ("Who painted the famous artwork The Starry Night?", "Vincent van Gogh", "Pablo Picasso", "Claude Monet", "Leonardo da Vinci"),
        ("Who painted the artwork Guernica?", "Pablo Picasso", "Vincent van Gogh", "Salvador Dalí", "Claude Monet"),
        ("Who composed the famous Ninth Symphony?", "Ludwig van Beethoven", "Wolfgang Amadeus Mozart", "Johann Sebastian Bach", "Frédéric Chopin"),
        ("Who was the first woman to win a Nobel Prize?", "Marie Curie", "Mother Teresa", "Dorothy Hodgkin", "Jane Addams"),
        ("Who received the Nobel Peace Prize in 1964 for civil rights activism?", "Martin Luther King Jr.", "Nelson Mandela", "Desmond Tutu", "Barack Obama"),
        ("Who is famous for the humanitarian work of the Missionaries of Charity?", "Mother Teresa", "Florence Nightingale", "Marie Curie", "Jane Goodall"),
        ("Who was the first human to travel into outer space?", "Yuri Gagarin", "Neil Armstrong", "Alan Shepard", "John Glenn"),
    ],

    "Medium": [
        ("Who became the first woman Prime Minister of India?", "Indira Gandhi", "Sarojini Naidu", "Pratibha Patil", "Vijaya Lakshmi Pandit"),
        ("Who was the first woman President of the United Nations General Assembly?", "Vijaya Lakshmi Pandit", "Indira Gandhi", "Eleanor Roosevelt", "Golda Meir"),
        ("Who was the first woman to receive the Nobel Prize in Literature?", "Selma Lagerlöf", "Toni Morrison", "Pearl S. Buck", "Gabriela Mistral"),
        ("Who was the first African American to receive the Nobel Prize in Literature?", "Toni Morrison", "Maya Angelou", "James Baldwin", "Langston Hughes"),
        ("Which scientist won Nobel Prizes in both Physics and Chemistry?", "Marie Curie", "Dorothy Hodgkin", "Lise Meitner", "Rosalind Franklin"),
        ("Who discovered the bacterium responsible for tuberculosis?", "Robert Koch", "Louis Pasteur", "Alexander Fleming", "Edward Jenner"),
        ("Who developed the first successful vaccine against smallpox?", "Edward Jenner", "Louis Pasteur", "Robert Koch", "Jonas Salk"),
        ("Who developed the first successful polio vaccine for widespread use?", "Jonas Salk", "Alexander Fleming", "Edward Jenner", "Robert Koch"),
        ("Who is associated with the discovery of the structure of DNA using X-ray diffraction research?", "Rosalind Franklin", "Marie Curie", "Jane Goodall", "Barbara McClintock"),
        ("Who proposed the uncertainty principle in quantum mechanics?", "Werner Heisenberg", "Niels Bohr", "Max Planck", "Erwin Schrödinger"),
        ("Who formulated the laws of planetary motion?", "Johannes Kepler", "Galileo Galilei", "Nicolaus Copernicus", "Isaac Newton"),
        ("Who proposed the heliocentric model of the solar system in a major work published in 1543?", "Nicolaus Copernicus", "Ptolemy", "Tycho Brahe", "Johannes Kepler"),
        ("Who is known for pioneering radioactivity research and winning Nobel Prizes in two sciences?", "Marie Curie", "Ada Lovelace", "Jane Goodall", "Lise Meitner"),
        ("Who is widely regarded as the first computer programmer because of her work on the Analytical Engine?", "Ada Lovelace", "Grace Hopper", "Hedy Lamarr", "Katherine Johnson"),
        ("Who developed the concept of the World Wide Web?", "Tim Berners-Lee", "Vint Cerf", "Bill Gates", "Steve Jobs"),
        ("Who is known for foundational work in theoretical computer science and artificial intelligence?", "Alan Turing", "Charles Babbage", "Thomas Edison", "James Watt"),
        ("Who was the first woman to win the Nobel Prize in Physics?", "Marie Curie", "Lise Meitner", "Maria Goeppert Mayer", "Dorothy Hodgkin"),
        ("Who won the Nobel Peace Prize in 1979 for humanitarian work in India and elsewhere?", "Mother Teresa", "Jane Addams", "Wangari Maathai", "Aung San Suu Kyi"),
        ("Who became the first woman Chancellor of Germany?", "Angela Merkel", "Margaret Thatcher", "Ursula von der Leyen", "Hillary Clinton"),
        ("Who was the first woman elected President of Liberia?", "Ellen Johnson Sirleaf", "Wangari Maathai", "Joyce Banda", "Sahle-Work Zewde"),
        ("Who led the Cuban Revolution and became Prime Minister of Cuba?", "Fidel Castro", "Che Guevara", "Raúl Castro", "Fulgencio Batista"),
        ("Who was the South African anti-apartheid activist and Archbishop awarded the Nobel Peace Prize in 1984?", "Desmond Tutu", "Nelson Mandela", "Oliver Tambo", "Thabo Mbeki"),
        ("Who was awarded the Nobel Peace Prize in 2004 for environmental and democratic activism in Kenya?", "Wangari Maathai", "Ellen Johnson Sirleaf", "Leymah Gbowee", "Rigoberta Menchú"),
        ("Who wrote the novel One Hundred Years of Solitude?", "Gabriel García Márquez", "Pablo Neruda", "Jorge Luis Borges", "Mario Vargas Llosa"),
        ("Who wrote the novel The Old Man and the Sea?", "Ernest Hemingway", "F. Scott Fitzgerald", "John Steinbeck", "Mark Twain"),
        ("Who wrote the dystopian novel Nineteen Eighty-Four?", "George Orwell", "Aldous Huxley", "H. G. Wells", "Ray Bradbury"),
        ("Who composed the opera The Magic Flute?", "Wolfgang Amadeus Mozart", "Ludwig van Beethoven", "Giuseppe Verdi", "Richard Wagner"),
        ("Who was the first woman to win an Olympic gold medal in an individual event?", "Charlotte Cooper", "Nadia Comăneci", "Wilma Rudolph", "Fanny Blankers-Koen"),
        ("Who was the first person to reach the South Pole?", "Roald Amundsen", "Robert Falcon Scott", "Ernest Shackleton", "James Cook"),
        ("Who was the first woman to fly solo across the Atlantic Ocean?", "Amelia Earhart", "Bessie Coleman", "Harriet Quimby", "Jacqueline Cochran"),
    ],

    "Hard": [
        ("Who became the first woman to receive the Nobel Prize in Chemistry?", "Marie Curie", "Irène Joliot-Curie", "Dorothy Hodgkin", "Ada Yonath"),
        ("Who shared the 1953 Nobel Prize in Physiology or Medicine for discovering the structure of DNA?", "James Watson and Francis Crick", "Watson and Maurice Wilkins", "Crick and Rosalind Franklin", "Wilkins and Franklin"),
        ("Who was awarded the 1979 Nobel Prize in Physics for the discovery of the cosmic microwave background radiation?", "Arno Penzias and Robert Wilson", "Albert Einstein and Niels Bohr", "James Watson and Francis Crick", "John Bardeen and Walter Brattain"),
        ("Who developed the theory of continental drift?", "Alfred Wegener", "Charles Lyell", "James Hutton", "Harry Hess"),
        ("Who proposed the theory of seafloor spreading?", "Harry Hess", "Alfred Wegener", "Charles Darwin", "James Hutton"),
        ("Who discovered the neutron in 1932?", "James Chadwick", "Ernest Rutherford", "J. J. Thomson", "Niels Bohr"),
        ("Who discovered the atomic nucleus through the gold foil experiment?", "Ernest Rutherford", "James Chadwick", "J. J. Thomson", "John Dalton"),
        ("Who discovered the electron through cathode-ray experiments?", "J. J. Thomson", "Ernest Rutherford", "James Chadwick", "Robert Millikan"),
        ("Who measured the elementary electric charge through the oil-drop experiment?", "Robert Millikan", "J. J. Thomson", "Michael Faraday", "James Clerk Maxwell"),
        ("Who formulated the laws of electromagnetic induction?", "Michael Faraday", "James Watt", "Isaac Newton", "André-Marie Ampère"),
        ("Who developed the mathematical framework of classical electromagnetism known as Maxwell's equations?", "James Clerk Maxwell", "Michael Faraday", "Nikola Tesla", "Heinrich Hertz"),
        ("Who is credited with inventing the first practical mechanical television system?", "John Logie Baird", "Philo Farnsworth", "Guglielmo Marconi", "Thomas Edison"),
        ("Who demonstrated the first working transistor with John Bardeen and Walter Brattain?", "William Shockley", "Alan Turing", "Claude Shannon", "John von Neumann"),
        ("Who is known for pioneering information theory?", "Claude Shannon", "Alan Turing", "John McCarthy", "Norbert Wiener"),
        ("Who coined the term artificial intelligence for the 1956 Dartmouth conference proposal?", "John McCarthy", "Alan Turing", "Marvin Minsky", "Claude Shannon"),
        ("Who developed the concept of the Turing Test?", "Alan Turing", "John McCarthy", "Charles Babbage", "John von Neumann"),
        ("Who was the first woman to receive the Abel Prize in Mathematics?", "Karen Uhlenbeck", "Maryam Mirzakhani", "Emmy Noether", "Ingrid Daubechies"),
        ("Who was the first woman to win the Fields Medal?", "Maryam Mirzakhani", "Karen Uhlenbeck", "Sophie Germain", "Emmy Noether"),
        ("Who was the first African woman to win the Nobel Prize in Literature?", "Nadine Gordimer", "Toni Morrison", "Wangari Maathai", "Buchi Emecheta"),
        ("Who was the first person from sub-Saharan Africa to receive the Nobel Prize in Literature?", "Wole Soyinka", "Chinua Achebe", "Ngũgĩ wa Thiong'o", "Nadine Gordimer"),
        ("Who won the Nobel Peace Prize in 1993 jointly with F. W. de Klerk?", "Nelson Mandela", "Desmond Tutu", "Thabo Mbeki", "Oliver Tambo"),
        ("Who was the first Secretary-General of the United Nations from Asia?", "U Thant", "Kofi Annan", "Boutros Boutros-Ghali", "Dag Hammarskjöld"),
        ("Who served as the United Nations Secretary-General during the 1990s and received the 2001 Nobel Peace Prize jointly with the UN?", "Kofi Annan", "U Thant", "Ban Ki-moon", "Javier Pérez de Cuéllar"),
        ("Who was the first woman to serve as President of the International Court of Justice?", "Rosalyn Higgins", "Eleanor Roosevelt", "Navanethem Pillay", "Fatou Bensouda"),
        ("Who was the first woman to serve as President of the European Commission?", "Ursula von der Leyen", "Angela Merkel", "Simone Veil", "Christine Lagarde"),
        ("Who was the first woman to become Prime Minister of Pakistan?", "Benazir Bhutto", "Sheikh Hasina", "Khaleda Zia", "Indira Gandhi"),
        ("Who was the first woman to win the Nobel Prize in Economic Sciences?", "Elinor Ostrom", "Esther Duflo", "Claudia Goldin", "Joan Robinson"),
        ("Who was awarded the Nobel Prize in Literature in 1954 for The Old Man and the Sea and other works?", "Ernest Hemingway", "John Steinbeck", "William Faulkner", "T. S. Eliot"),
        ("Who received the Nobel Prize in Literature in 1982 for One Hundred Years of Solitude?", "Gabriel García Márquez", "Pablo Neruda", "Octavio Paz", "Mario Vargas Llosa"),
        ("Who became the first woman to win the Nobel Prize in Physics in 1903?", "Marie Curie", "Lise Meitner", "Maria Goeppert Mayer", "Donna Strickland"),
    ]
}


def validate_bank():
    print("\nValidating question bank...")

    for difficulty in ("Easy", "Medium", "Hard"):
        questions = BANK[difficulty]
        print(f"{difficulty}: {len(questions)}/30")

        if len(questions) != 30:
            raise ValueError(
                f"{difficulty} must contain exactly 30 questions; "
                f"found {len(questions)}"
            )

        for index, item in enumerate(questions, start=1):
            if len(item) != 5:
                raise ValueError(
                    f"{difficulty} question {index} must contain 5 values."
                )

            if not all(isinstance(value, str) and value.strip() for value in item):
                raise ValueError(
                    f"Invalid or empty value in {difficulty} question {index}."
                )

            if len(set(item[1:])) != 4:
                raise ValueError(
                    f"Duplicate options in {difficulty} question {index}."
                )

    print("Validation successful: exactly 90 questions.")


def main():
    validate_bank()

    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT title, topic FROM lessons WHERE id = ?",
            (LESSON_ID,)
        )
        lesson = cursor.fetchone()

        if lesson is None:
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
                    "Famous world personalities, political leaders, "
                    "scientists, Nobel laureates and global achievements."
                )
            )
            print("Lesson created.")

        elif lesson != (LESSON_TITLE, TOPIC):
            raise ValueError(
                f"Lesson ID {LESSON_ID} already belongs to another lesson: {lesson}"
            )

        for difficulty, questions in BANK.items():

            cursor.execute(
                """
                SELECT id FROM quizzes
                WHERE lesson_id = ? AND difficulty = ?
                ORDER BY id
                LIMIT 1
                """,
                (LESSON_ID, difficulty)
            )

            quiz = cursor.fetchone()

            if quiz is None:
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
            else:
                quiz_id = quiz[0]

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )
            existing_count = cursor.fetchone()[0]

            if existing_count > 30:
                raise ValueError(
                    f"{difficulty} quiz already has {existing_count} questions."
                )

            for question, correct, wrong1, wrong2, wrong3 in questions[existing_count:]:
                options = [correct, wrong1, wrong2, wrong3]
                random.shuffle(options)

                correct_answer = "ABCD"[options.index(correct)]

                cursor.execute(
                    """
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
                    f"{difficulty} quiz has {final_count} questions instead of 30."
                )

            print(f"{difficulty}: {final_count}/30 questions")

        connection.commit()

        print("\nSUCCESS!")
        print(f"Lesson ID: {LESSON_ID}")
        print(f"Lesson: {LESSON_TITLE}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Total: 90 questions.")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
