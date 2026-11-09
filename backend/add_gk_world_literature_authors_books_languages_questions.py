
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 199
LESSON_TITLE = "World Literature, Authors, Books, Languages and Famous Works"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Who wrote Romeo and Juliet?", "William Shakespeare", "Charles Dickens", "Jane Austen", "George Orwell"),
        ("Who wrote the Harry Potter series?", "J. K. Rowling", "Enid Blyton", "Agatha Christie", "Suzanne Collins"),
        ("Who wrote The Jungle Book?", "Rudyard Kipling", "Mark Twain", "Lewis Carroll", "Jules Verne"),
        ("Who wrote Alice's Adventures in Wonderland?", "Lewis Carroll", "Charles Dickens", "Oscar Wilde", "Robert Louis Stevenson"),
        ("Who wrote The Adventures of Tom Sawyer?", "Mark Twain", "Ernest Hemingway", "John Steinbeck", "H. G. Wells"),
        ("Who wrote Pride and Prejudice?", "Jane Austen", "Emily Brontë", "Virginia Woolf", "Mary Shelley"),
        ("Who wrote Oliver Twist?", "Charles Dickens", "William Shakespeare", "George Eliot", "Thomas Hardy"),
        ("Who wrote The Old Man and the Sea?", "Ernest Hemingway", "F. Scott Fitzgerald", "John Steinbeck", "Herman Melville"),
        ("Who wrote The Adventures of Sherlock Holmes?", "Arthur Conan Doyle", "Agatha Christie", "Edgar Allan Poe", "Ian Fleming"),
        ("Who wrote The Lord of the Rings?", "J. R. R. Tolkien", "C. S. Lewis", "George R. R. Martin", "Philip Pullman"),
        ("Who wrote The Chronicles of Narnia?", "C. S. Lewis", "J. R. R. Tolkien", "Roald Dahl", "J. K. Rowling"),
        ("Who wrote Charlie and the Chocolate Factory?", "Roald Dahl", "Enid Blyton", "Lewis Carroll", "Rudyard Kipling"),
        ("Who wrote The Diary of a Young Girl?", "Anne Frank", "Helen Keller", "Virginia Woolf", "Agatha Christie"),
        ("Who wrote The Little Prince?", "Antoine de Saint-Exupéry", "Victor Hugo", "Jules Verne", "Albert Camus"),
        ("Who wrote Don Quixote?", "Miguel de Cervantes", "Dante Alighieri", "Geoffrey Chaucer", "Homer"),
        ("Who wrote The Divine Comedy?", "Dante Alighieri", "William Shakespeare", "John Milton", "Homer"),
        ("Who wrote The Odyssey?", "Homer", "Virgil", "Sophocles", "Plato"),
        ("Who wrote The Iliad?", "Homer", "Aristotle", "Virgil", "Aeschylus"),
        ("Who wrote Animal Farm?", "George Orwell", "Aldous Huxley", "Ernest Hemingway", "James Joyce"),
        ("Who wrote Nineteen Eighty-Four?", "George Orwell", "H. G. Wells", "J. R. R. Tolkien", "Arthur Conan Doyle"),
        ("Which language was used originally for the epic The Iliad?", "Ancient Greek", "Latin", "French", "German"),
        ("Which language is primarily associated with the works of Miguel de Cervantes?", "Spanish", "Italian", "Portuguese", "French"),
        ("Which language did Shakespeare primarily write in?", "English", "French", "Latin", "Italian"),
        ("Which country is associated with the literary character Don Quixote?", "Spain", "France", "Italy", "Germany"),
        ("Who wrote The Three Musketeers?", "Alexandre Dumas", "Victor Hugo", "Jules Verne", "Honoré de Balzac"),
        ("Who wrote Les Misérables?", "Victor Hugo", "Alexandre Dumas", "Albert Camus", "Gustave Flaubert"),
        ("Who wrote The Wonderful Wizard of Oz?", "L. Frank Baum", "Roald Dahl", "Lewis Carroll", "J. M. Barrie"),
        ("Who wrote Peter Pan?", "J. M. Barrie", "Lewis Carroll", "Rudyard Kipling", "A. A. Milne"),
        ("Who wrote Winnie-the-Pooh?", "A. A. Milne", "Beatrix Potter", "Enid Blyton", "Roald Dahl"),
        ("Who wrote The Tale of Peter Rabbit?", "Beatrix Potter", "A. A. Milne", "J. M. Barrie", "Astrid Lindgren"),
    ],

    "Medium": [
        ("Who wrote the novel One Hundred Years of Solitude?", "Gabriel García Márquez", "Mario Vargas Llosa", "Pablo Neruda", "Jorge Luis Borges"),
        ("Who wrote The Great Gatsby?", "F. Scott Fitzgerald", "Ernest Hemingway", "John Steinbeck", "William Faulkner"),
        ("Who wrote To Kill a Mockingbird?", "Harper Lee", "Toni Morrison", "Emily Dickinson", "Sylvia Plath"),
        ("Who wrote Wuthering Heights?", "Emily Brontë", "Charlotte Brontë", "Anne Brontë", "Jane Austen"),
        ("Who wrote Jane Eyre?", "Charlotte Brontë", "Emily Brontë", "George Eliot", "Mary Shelley"),
        ("Who wrote Frankenstein?", "Mary Shelley", "Jane Austen", "Virginia Woolf", "Emily Brontë"),
        ("Who wrote The Picture of Dorian Gray?", "Oscar Wilde", "Charles Dickens", "Thomas Hardy", "George Bernard Shaw"),
        ("Who wrote The Trial?", "Franz Kafka", "Albert Camus", "Hermann Hesse", "Thomas Mann"),
        ("Who wrote The Stranger?", "Albert Camus", "Franz Kafka", "Jean-Paul Sartre", "André Gide"),
        ("Who wrote The Brothers Karamazov?", "Fyodor Dostoevsky", "Leo Tolstoy", "Anton Chekhov", "Ivan Turgenev"),
        ("Who wrote War and Peace?", "Leo Tolstoy", "Fyodor Dostoevsky", "Maxim Gorky", "Nikolai Gogol"),
        ("Who wrote Crime and Punishment?", "Fyodor Dostoevsky", "Leo Tolstoy", "Anton Chekhov", "Alexander Pushkin"),
        ("Who wrote The Metamorphosis?", "Franz Kafka", "Thomas Mann", "Hermann Hesse", "Albert Camus"),
        ("Who wrote The Name of the Rose?", "Umberto Eco", "Italo Calvino", "Dante Alighieri", "Alessandro Manzoni"),
        ("Who wrote The Kite Runner?", "Khaled Hosseini", "Salman Rushdie", "Orhan Pamuk", "Naguib Mahfouz"),
        ("Who wrote The Alchemist?", "Paulo Coelho", "José Saramago", "Jorge Amado", "Gabriel García Márquez"),
        ("Who wrote The God of Small Things?", "Arundhati Roy", "Kiran Desai", "Jhumpa Lahiri", "Anita Desai"),
        ("Who wrote Midnight's Children?", "Salman Rushdie", "Vikram Seth", "Amitav Ghosh", "R. K. Narayan"),
        ("Who wrote A Suitable Boy?", "Vikram Seth", "Salman Rushdie", "Amitav Ghosh", "Khushwant Singh"),
        ("Who wrote The Guide?", "R. K. Narayan", "Mulk Raj Anand", "Raja Rao", "Vikram Seth"),
        ("Who wrote The White Tiger?", "Aravind Adiga", "Amitav Ghosh", "Chetan Bhagat", "R. K. Narayan"),
        ("Who wrote The Namesake?", "Jhumpa Lahiri", "Arundhati Roy", "Kiran Desai", "Anita Desai"),
        ("Who wrote The Inheritance of Loss?", "Kiran Desai", "Jhumpa Lahiri", "Arundhati Roy", "Shashi Deshpande"),
        ("Who wrote The Shadow Lines?", "Amitav Ghosh", "Vikram Seth", "Salman Rushdie", "Amit Chaudhuri"),
        ("Who wrote The Canterbury Tales?", "Geoffrey Chaucer", "John Milton", "William Shakespeare", "Christopher Marlowe"),
        ("Who wrote Paradise Lost?", "John Milton", "Geoffrey Chaucer", "John Donne", "William Blake"),
        ("Who wrote The Waste Land?", "T. S. Eliot", "W. B. Yeats", "Robert Frost", "Ezra Pound"),
        ("Who wrote The Catcher in the Rye?", "J. D. Salinger", "Jack Kerouac", "John Steinbeck", "F. Scott Fitzgerald"),
        ("Who wrote The Grapes of Wrath?", "John Steinbeck", "Ernest Hemingway", "William Faulkner", "F. Scott Fitzgerald"),
        ("Who wrote The Sound and the Fury?", "William Faulkner", "John Steinbeck", "Ernest Hemingway", "T. S. Eliot"),
    ],

    "Hard": [
        ("Who wrote the epic poem Beowulf?", "Anonymous author", "Geoffrey Chaucer", "John Milton", "William Langland"),
        ("In which language was Beowulf originally composed?", "Old English", "Middle English", "Latin", "Old Norse"),
        ("Who wrote the medieval work The Decameron?", "Giovanni Boccaccio", "Dante Alighieri", "Petrarch", "Niccolò Machiavelli"),
        ("Who wrote the sonnet sequence Canzoniere?", "Petrarch", "Dante Alighieri", "Giovanni Boccaccio", "Torquato Tasso"),
        ("Who wrote the political treatise The Prince?", "Niccolò Machiavelli", "Thomas More", "Jean-Jacques Rousseau", "John Locke"),
        ("Who wrote Utopia, published in 1516?", "Thomas More", "Francis Bacon", "John Milton", "Thomas Hobbes"),
        ("Who wrote the epic poem The Faerie Queene?", "Edmund Spenser", "John Milton", "Geoffrey Chaucer", "John Dryden"),
        ("Who wrote Doctor Faustus?", "Christopher Marlowe", "Ben Jonson", "John Webster", "Thomas Kyd"),
        ("Who wrote the play Volpone?", "Ben Jonson", "Christopher Marlowe", "William Congreve", "John Dryden"),
        ("Who wrote the novel Middlemarch?", "George Eliot", "Jane Austen", "Charlotte Brontë", "Virginia Woolf"),
        ("Who wrote the novel Tess of the d'Urbervilles?", "Thomas Hardy", "Charles Dickens", "George Eliot", "D. H. Lawrence"),
        ("Who wrote the modernist novel Ulysses?", "James Joyce", "Virginia Woolf", "D. H. Lawrence", "Samuel Beckett"),
        ("Who wrote To the Lighthouse?", "Virginia Woolf", "James Joyce", "Katherine Mansfield", "Doris Lessing"),
        ("Who wrote the novel Mrs Dalloway?", "Virginia Woolf", "George Eliot", "Jane Austen", "Mary Shelley"),
        ("Who wrote the novel The Sound and the Fury?", "William Faulkner", "Ernest Hemingway", "John Steinbeck", "F. Scott Fitzgerald"),
        ("Who wrote the play Waiting for Godot?", "Samuel Beckett", "Eugène Ionesco", "Harold Pinter", "Jean-Paul Sartre"),
        ("Who wrote the play Rhinoceros?", "Eugène Ionesco", "Samuel Beckett", "Bertolt Brecht", "Arthur Miller"),
        ("Who wrote the play Mother Courage and Her Children?", "Bertolt Brecht", "Henrik Ibsen", "Anton Chekhov", "August Strindberg"),
        ("Who wrote the novel The Magic Mountain?", "Thomas Mann", "Hermann Hesse", "Franz Kafka", "Stefan Zweig"),
        ("Who wrote Siddhartha?", "Hermann Hesse", "Thomas Mann", "Franz Kafka", "Rainer Maria Rilke"),
        ("Who wrote the novel The Tin Drum?", "Günter Grass", "Thomas Mann", "Heinrich Böll", "Hermann Hesse"),
        ("Who wrote the novel The Plague?", "Albert Camus", "Jean-Paul Sartre", "André Malraux", "Franz Kafka"),
        ("Who wrote the novel Blindness?", "José Saramago", "Umberto Eco", "Paulo Coelho", "Milan Kundera"),
        ("Who wrote the novel The Unbearable Lightness of Being?", "Milan Kundera", "Franz Kafka", "Václav Havel", "Bohumil Hrabal"),
        ("Who wrote the novel The Master and Margarita?", "Mikhail Bulgakov", "Boris Pasternak", "Maxim Gorky", "Ivan Turgenev"),
        ("Who wrote the novel Doctor Zhivago?", "Boris Pasternak", "Mikhail Bulgakov", "Leo Tolstoy", "Alexander Solzhenitsyn"),
        ("Who wrote the novel Things Fall Apart?", "Chinua Achebe", "Wole Soyinka", "Ngũgĩ wa Thiong'o", "Ben Okri"),
        ("Who wrote the novel Season of Migration to the North?", "Tayeb Salih", "Naguib Mahfouz", "Chinua Achebe", "Ayi Kwei Armah"),
        ("Who wrote the novel Palace of Illusions?", "Chitra Banerjee Divakaruni", "Arundhati Roy", "Anita Desai", "Jhumpa Lahiri"),
        ("Who wrote the novel The Satanic Verses?", "Salman Rushdie", "Vikram Seth", "Amitav Ghosh", "R. K. Narayan"),
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
                    "World literature, famous authors, books, languages "
                    "and important literary works."
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
