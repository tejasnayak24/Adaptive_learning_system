
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

LESSON_ID = 192
LESSON_TITLE = "Science, Inventions, Discoveries and Famous Scientists"
TOPIC = "General Knowledge"

BANK = {
    "Easy": [
        ("Who is known as the Father of Modern Physics?", "Albert Einstein", "Isaac Newton", "Galileo Galilei", "Nikola Tesla"),
        ("Who discovered penicillin?", "Alexander Fleming", "Louis Pasteur", "Robert Koch", "Edward Jenner"),
        ("Who invented the telephone?", "Alexander Graham Bell", "Thomas Edison", "Guglielmo Marconi", "James Watt"),
        ("Who is credited with inventing the practical incandescent light bulb?", "Thomas Edison", "Isaac Newton", "Michael Faraday", "Charles Darwin"),
        ("Who developed the theory of relativity?", "Albert Einstein", "Niels Bohr", "Max Planck", "Ernest Rutherford"),
        ("Who discovered the law of gravity?", "Isaac Newton", "Galileo Galilei", "Albert Einstein", "Johannes Kepler"),
        ("Who is known as the Father of Computers?", "Charles Babbage", "Alan Turing", "John von Neumann", "Blaise Pascal"),
        ("Who invented the World Wide Web?", "Tim Berners-Lee", "Bill Gates", "Steve Jobs", "Vint Cerf"),
        ("Who discovered the circulation of blood in the human body?", "William Harvey", "Louis Pasteur", "Robert Hooke", "Gregor Mendel"),
        ("Who is associated with the discovery of X-rays?", "Wilhelm Conrad Röntgen", "Marie Curie", "J. J. Thomson", "Ernest Rutherford"),
        ("Who discovered radioactivity in uranium salts?", "Henri Becquerel", "Marie Curie", "James Chadwick", "Enrico Fermi"),
        ("Who is famous for developing the periodic table?", "Dmitri Mendeleev", "John Dalton", "Antoine Lavoisier", "Robert Boyle"),
        ("Who proposed the three laws of motion?", "Isaac Newton", "Albert Einstein", "Galileo Galilei", "Michael Faraday"),
        ("Which scientist is associated with the discovery of the electron?", "J. J. Thomson", "James Chadwick", "Ernest Rutherford", "Niels Bohr"),
        ("Who discovered the neutron?", "James Chadwick", "J. J. Thomson", "Ernest Rutherford", "Max Planck"),
        ("Who is known for the theory of evolution by natural selection?", "Charles Darwin", "Gregor Mendel", "Louis Pasteur", "Carl Linnaeus"),
        ("Who is regarded as the Father of Genetics?", "Gregor Mendel", "Charles Darwin", "Robert Hooke", "Thomas Hunt Morgan"),
        ("Who invented the printing press in Europe?", "Johannes Gutenberg", "William Caxton", "Leonardo da Vinci", "Galileo Galilei"),
        ("Who is associated with the invention of the steam engine's improved design?", "James Watt", "George Stephenson", "Thomas Newcomen", "Michael Faraday"),
        ("Who invented the first successful practical aeroplane?", "Wright brothers", "Montgolfier brothers", "Lumière brothers", "Curie brothers"),
        ("Who is associated with the invention of the radio?", "Guglielmo Marconi", "Alexander Graham Bell", "Thomas Edison", "James Watt"),
        ("Which scientist discovered the Raman Effect?", "C. V. Raman", "Homi J. Bhabha", "S. N. Bose", "Vikram Sarabhai"),
        ("Who is known as the Missile Man of India?", "A. P. J. Abdul Kalam", "Vikram Sarabhai", "Homi J. Bhabha", "C. V. Raman"),
        ("Who is known as the Father of the Indian Space Programme?", "Vikram Sarabhai", "A. P. J. Abdul Kalam", "Satish Dhawan", "Homi J. Bhabha"),
        ("Who founded the Tata Institute of Fundamental Research?", "Homi J. Bhabha", "Vikram Sarabhai", "C. V. Raman", "Meghnad Saha"),
        ("Which scientist discovered the Raman Effect in 1928?", "C. V. Raman", "S. N. Bose", "Jagadish Chandra Bose", "Meghnad Saha"),
        ("Who invented the dynamite?", "Alfred Nobel", "Louis Pasteur", "Michael Faraday", "Nikola Tesla"),
        ("Which scientist is associated with the development of the first successful smallpox vaccine?", "Edward Jenner", "Alexander Fleming", "Robert Koch", "Joseph Lister"),
        ("Who invented the safety lamp used by miners?", "Humphry Davy", "James Watt", "Michael Faraday", "Thomas Edison"),
        ("Which scientist is famous for research on radioactivity and won two Nobel Prizes in different sciences?", "Marie Curie", "Rosalind Franklin", "Dorothy Hodgkin", "Lise Meitner"),
    ],

    "Medium": [
        ("Who formulated the uncertainty principle?", "Werner Heisenberg", "Niels Bohr", "Erwin Schrödinger", "Max Born"),
        ("Who developed the wave equation of quantum mechanics?", "Erwin Schrödinger", "Max Planck", "Albert Einstein", "Paul Dirac"),
        ("Who proposed the atomic model with electrons orbiting a central nucleus?", "Ernest Rutherford", "J. J. Thomson", "James Chadwick", "John Dalton"),
        ("Who proposed the planetary model of the atom with quantised electron orbits?", "Niels Bohr", "Ernest Rutherford", "J. J. Thomson", "Max Planck"),
        ("Who discovered the proton through experiments involving canal rays and positive rays?", "Eugen Goldstein", "James Chadwick", "J. J. Thomson", "Robert Millikan"),
        ("Who measured the elementary electric charge through the oil-drop experiment?", "Robert Millikan", "J. J. Thomson", "Ernest Rutherford", "Michael Faraday"),
        ("Who discovered electromagnetic induction?", "Michael Faraday", "James Clerk Maxwell", "Nikola Tesla", "Heinrich Hertz"),
        ("Who formulated the classical electromagnetic field equations?", "James Clerk Maxwell", "Michael Faraday", "Isaac Newton", "Niels Bohr"),
        ("Who discovered the laws of planetary motion?", "Johannes Kepler", "Galileo Galilei", "Isaac Newton", "Nicolaus Copernicus"),
        ("Who proposed the heliocentric model of the solar system in his famous work published in 1543?", "Nicolaus Copernicus", "Ptolemy", "Johannes Kepler", "Tycho Brahe"),
        ("Who discovered the moons of Jupiter using a telescope in 1610?", "Galileo Galilei", "Isaac Newton", "Edwin Hubble", "Johannes Kepler"),
        ("Who discovered the expanding nature of the universe through observations of galaxies?", "Edwin Hubble", "Albert Einstein", "Stephen Hawking", "Arthur Eddington"),
        ("Who proposed the Big Bang theory in its early form as the hypothesis of the primeval atom?", "Georges Lemaître", "Edwin Hubble", "Fred Hoyle", "Carl Sagan"),
        ("Who discovered the structure of DNA using X-ray diffraction data that contributed to the double-helix model?", "Rosalind Franklin", "Barbara McClintock", "Dorothy Hodgkin", "Jane Goodall"),
        ("Who proposed the double-helix model of DNA with Francis Crick?", "James Watson", "Linus Pauling", "Maurice Wilkins", "Frederick Sanger"),
        ("Who discovered blood groups ABO?", "Karl Landsteiner", "William Harvey", "Alexander Fleming", "Edward Jenner"),
        ("Who developed the first widely used polio vaccine?", "Jonas Salk", "Edward Jenner", "Louis Pasteur", "Robert Koch"),
        ("Who developed the oral polio vaccine?", "Albert Sabin", "Jonas Salk", "Alexander Fleming", "Joseph Lister"),
        ("Who developed the first successful rabies vaccine?", "Louis Pasteur", "Robert Koch", "Edward Jenner", "Alexander Fleming"),
        ("Who discovered the bacterium responsible for tuberculosis?", "Robert Koch", "Louis Pasteur", "Alexander Fleming", "Joseph Lister"),
        ("Who discovered the bacterium responsible for cholera?", "Robert Koch", "Edward Jenner", "William Harvey", "Gregor Mendel"),
        ("Who developed the first practical laser?", "Theodore Maiman", "Albert Einstein", "Charles Townes", "Nikola Tesla"),
        ("Who is credited with inventing the first working transistor at Bell Labs with Walter Brattain and John Bardeen?", "William Shockley", "Thomas Edison", "Alan Turing", "Claude Shannon"),
        ("Who is widely regarded as the father of information theory?", "Claude Shannon", "Alan Turing", "Charles Babbage", "John McCarthy"),
        ("Who proposed the concept of a universal computing machine?", "Alan Turing", "Charles Babbage", "Blaise Pascal", "John von Neumann"),
        ("Who coined the term artificial intelligence at the 1956 Dartmouth workshop?", "John McCarthy", "Alan Turing", "Marvin Minsky", "Claude Shannon"),
        ("Who discovered the planet Uranus in 1781?", "William Herschel", "Galileo Galilei", "Johannes Kepler", "Edwin Hubble"),
        ("Who discovered the planet Neptune through mathematical predictions and observations?", "Johann Galle", "William Herschel", "Galileo Galilei", "Tycho Brahe"),
        ("Which scientist proposed the laws of inheritance based on pea plant experiments?", "Gregor Mendel", "Charles Darwin", "Thomas Hunt Morgan", "Louis Pasteur"),
        ("Who discovered the phenomenon of superconductivity?", "Heike Kamerlingh Onnes", "Michael Faraday", "James Joule", "William Thomson"),
    ],

    "Hard": [
        ("Which scientist introduced the concept of the quantum of action in 1900?", "Max Planck", "Albert Einstein", "Niels Bohr", "Werner Heisenberg"),
        ("Who explained the photoelectric effect using the idea of light quanta?", "Albert Einstein", "Max Planck", "James Clerk Maxwell", "Erwin Schrödinger"),
        ("Which experiment provided strong evidence for the nuclear model of the atom?", "Gold foil experiment", "Oil-drop experiment", "Millikan's experiment on photoelectric effect", "Michelson-Morley experiment"),
        ("Who conducted the gold foil experiment under the direction of Ernest Rutherford?", "Hans Geiger and Ernest Marsden", "J. J. Thomson and James Chadwick", "Niels Bohr and Max Planck", "Robert Millikan and Albert Einstein"),
        ("Which scientist discovered nuclear fission experimentally with Otto Hahn and Fritz Strassmann's work being explained theoretically?", "Lise Meitner", "Marie Curie", "Irène Joliot-Curie", "Emmy Noether"),
        ("Which scientists are credited with the experimental discovery of nuclear fission in 1938?", "Otto Hahn and Fritz Strassmann", "James Chadwick and Ernest Rutherford", "Niels Bohr and Max Planck", "J. J. Thomson and Robert Millikan"),
        ("Who proposed the exclusion principle in quantum mechanics?", "Wolfgang Pauli", "Werner Heisenberg", "Max Born", "Paul Dirac"),
        ("Who formulated the relativistic wave equation for the electron?", "Paul Dirac", "Erwin Schrödinger", "Max Planck", "Niels Bohr"),
        ("Which scientist predicted the existence of antimatter through a relativistic equation?", "Paul Dirac", "Albert Einstein", "James Chadwick", "Enrico Fermi"),
        ("Who discovered the positron experimentally?", "Carl Anderson", "Paul Dirac", "Ernest Rutherford", "James Chadwick"),
        ("Who discovered cosmic microwave background radiation along with Robert Wilson?", "Arno Penzias", "Edwin Hubble", "George Gamow", "Georges Lemaître"),
        ("Who proposed the theory of continental drift?", "Alfred Wegener", "Charles Lyell", "James Hutton", "Harry Hess"),
        ("Who proposed the seafloor spreading hypothesis?", "Harry Hess", "Alfred Wegener", "Charles Darwin", "James Hutton"),
        ("Who developed the first widely accepted modern classification of living organisms into kingdoms?", "Robert Whittaker", "Carl Linnaeus", "Charles Darwin", "Gregor Mendel"),
        ("Who developed the binomial nomenclature system for naming organisms?", "Carl Linnaeus", "Robert Whittaker", "Charles Darwin", "Louis Pasteur"),
        ("Who discovered transposable genetic elements in maize?", "Barbara McClintock", "Rosalind Franklin", "Dorothy Hodgkin", "Rachel Carson"),
        ("Who determined the molecular structure of penicillin using X-ray crystallography?", "Dorothy Crowfoot Hodgkin", "Alexander Fleming", "Rosalind Franklin", "Marie Curie"),
        ("Who developed the first successful method of DNA sequencing?", "Frederick Sanger", "James Watson", "Francis Crick", "Gregor Mendel"),
        ("Which scientist is associated with the discovery of restriction enzymes?", "Werner Arber", "Alexander Fleming", "Edward Jenner", "Robert Hooke"),
        ("Who developed the polymerase chain reaction (PCR) technique?", "Kary Mullis", "Frederick Sanger", "James Watson", "Craig Venter"),
        ("Which scientist developed the CRISPR-Cas9 gene-editing method with Emmanuelle Charpentier?", "Jennifer Doudna", "Rosalind Franklin", "Barbara McClintock", "Dorothy Hodgkin"),
        ("Who discovered the law of conservation of mass through chemical experiments?", "Antoine Lavoisier", "John Dalton", "Dmitri Mendeleev", "Robert Boyle"),
        ("Who formulated the law of multiple proportions?", "John Dalton", "Antoine Lavoisier", "Robert Boyle", "Amedeo Avogadro"),
        ("Who proposed Avogadro's law?", "Amedeo Avogadro", "John Dalton", "Joseph Proust", "Robert Boyle"),
        ("Who discovered the element polonium along with Marie Curie?", "Pierre Curie", "Ernest Rutherford", "Henri Becquerel", "Niels Bohr"),
        ("Who discovered the element radium along with Pierre Curie?", "Marie Curie", "Lise Meitner", "Dorothy Hodgkin", "Rosalind Franklin"),
        ("Which Indian physicist proposed the Saha ionisation equation?", "Meghnad Saha", "S. N. Bose", "C. V. Raman", "Homi J. Bhabha"),
        ("The Bose-Einstein statistics are named after Satyendra Nath Bose and which other scientist?", "Albert Einstein", "Niels Bohr", "Max Planck", "Erwin Schrödinger"),
        ("Who developed the theory of the unified field in an attempt to unify fundamental interactions?", "Albert Einstein", "Isaac Newton", "Michael Faraday", "James Clerk Maxwell"),
        ("Which scientist is associated with the discovery of the law of radioactive decay?", "Ernest Rutherford", "J. J. Thomson", "Robert Hooke", "James Watt"),
    ]
}


def validate_bank():
    for difficulty, questions in BANK.items():
        if len(questions) != 30:
            raise ValueError(
                f"{difficulty} must contain exactly 30 questions; "
                f"found {len(questions)}"
            )

        for index, item in enumerate(questions, start=1):
            if len(item) != 5:
                raise ValueError(
                    f"{difficulty} question {index} must contain 5 values"
                )

            if not all(isinstance(value, str) and value.strip() for value in item):
                raise ValueError(
                    f"Empty or invalid value in {difficulty} question {index}"
                )

            if len(set(item[1:])) != 4:
                raise ValueError(
                    f"Duplicate options in {difficulty} question {index}"
                )


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
                    "MCQ lesson covering science, inventions, discoveries "
                    "and famous scientists."
                )
            )
            print(f"Created lesson {LESSON_ID}: {LESSON_TITLE}")

        elif lesson != (LESSON_TITLE, TOPIC):
            raise ValueError(
                f"Lesson ID {LESSON_ID} already belongs to "
                f"{lesson[0]!r} under topic {lesson[1]!r}. "
                "No data was changed."
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
                print(f"Created {difficulty} quiz: {quiz_id}")
            else:
                quiz_id = quiz[0]

            cursor.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id = ?",
                (quiz_id,)
            )
            existing_count = cursor.fetchone()[0]

            if existing_count > 30:
                raise ValueError(
                    f"{difficulty} quiz already has {existing_count} questions. "
                    "Expected maximum: 30."
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
                    f"{difficulty} quiz has {final_count} questions, not 30"
                )

            print(f"{difficulty}: {final_count}/30 questions")

        connection.commit()

        print("\nSUCCESS!")
        print(f"Lesson ID: {LESSON_ID}")
        print(f"Lesson: {LESSON_TITLE}")
        print("Easy: 30 questions")
        print("Medium: 30 questions")
        print("Hard: 30 questions")
        print("Total: 90 questions")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
