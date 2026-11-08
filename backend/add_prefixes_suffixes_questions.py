
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("Which prefix means 'not'?", "un-", "re-", "pre-", "mis-"),
        ("Which prefix means 'again'?", "re-", "un-", "dis-", "sub-"),
        ("Which suffix means 'full of'?", "-ful", "-less", "-ness", "-ment"),
        ("Which suffix means 'without'?", "-less", "-ful", "-er", "-ly"),
        ("What is the prefix in 'unhappy'?", "un-", "happy", "-py", "hap-"),
        ("What is the suffix in 'kindness'?", "-ness", "kind-", "kin-", "-nesses"),
        ("Which word contains the prefix 're-'?", "Rewrite", "Unfair", "Careful", "Hopeless"),
        ("Which word contains the suffix '-ful'?", "Beautiful", "Unkind", "Preview", "Dislike"),
        ("What does 'disagree' mean?", "Not agree", "Agree again", "Agree before", "Agree fully"),
        ("What does 'preview' mean?", "View before", "View again", "View wrongly", "View without"),
        ("Which prefix means 'before'?", "pre-", "post-", "un-", "anti-"),
        ("Which prefix means 'under'?", "sub-", "super-", "inter-", "over-"),
        ("Which suffix forms a noun from 'happy'?", "-ness", "-ly", "-ful", "-able"),
        ("Which suffix forms an adverb from 'quick'?", "-ly", "-ness", "-ment", "-er"),
        ("What is the base word in 'careless'?", "Care", "Less", "Careless", "Car"),
        ("What is the base word in 'replaying'?", "Play", "Replay", "Re-", "Playing"),
        ("Which word means 'not possible'?", "Impossible", "Possible", "Possibly", "Possibility"),
        ("Which prefix means 'many'?", "multi-", "mono-", "semi-", "uni-"),
        ("Which prefix means 'one'?", "uni-", "bi-", "tri-", "multi-"),
        ("Which prefix means 'two'?", "bi-", "uni-", "tri-", "poly-"),
        ("Which word has a suffix meaning 'a person who'?", "Teacher", "Teaching", "Teach", "Teachable"),
        ("Which suffix means 'a person who performs an action'?", "-er", "-ness", "-ful", "-less"),
        ("Which word contains the prefix 'mis-'?", "Misbehave", "Helpful", "Careless", "Preview"),
        ("What does 'careful' mean?", "Full of care", "Without care", "Care again", "Care before"),
        ("What does 'hopeless' mean?", "Without hope", "Full of hope", "Hope again", "Hope before"),
        ("Which word contains the suffix '-ment'?", "Enjoyment", "Enjoyable", "Enjoying", "Enjoy"),
        ("Which prefix means 'against'?", "anti-", "pre-", "re-", "sub-"),
        ("Which word means 'to read again'?", "Reread", "Misread", "Unreadable", "Reader"),
        ("Which suffix can turn 'dark' into an adjective meaning 'somewhat dark'?", "-ish", "-ness", "-ment", "-er"),
        ("Which word contains both a prefix and a suffix?", "Unhelpful", "Helpful", "Unhappy", "Kindness"),
    ],

    "Medium": [
        ("What is the meaning of the prefix 'inter-' in 'international'?", "Between or among", "Within one", "Against", "Before"),
        ("What does the prefix 'trans-' mean in 'transport'?", "Across", "Under", "Against", "One"),
        ("Which suffix changes 'beauty' into an adjective?", "-ful", "-ness", "-ment", "-er"),
        ("Which suffix changes 'modern' into a noun?", "-ity", "-ly", "-ful", "-less"),
        ("Which word means 'the act of being able to read'?", "Literacy", "Literary", "Literal", "Literally"),
        ("What does 'antisocial' mean?", "Against or avoiding social interaction", "Very sociable", "Social again", "Social before"),
        ("Which prefix means 'around'?", "circum-", "sub-", "trans-", "inter-"),
        ("What does 'submarine' mean based on its prefix?", "Under the sea", "Above the sea", "Across the sea", "Beyond the sea"),
        ("Which word uses the suffix '-able' correctly?", "Readable", "Readness", "Readful", "Readment"),
        ("Which word is formed by adding '-ity' to 'active'?", "Activity", "Actively", "Activeness", "Activation"),
        ("What does the prefix 'de-' often indicate?", "Removal or reversal", "Repetition", "Small size", "Before"),
        ("Which word means 'to make something less effective'?", "Diminish", "Enlarge", "Strengthen", "Expand"),
        ("Which suffix indicates a state or condition?", "-hood", "-er", "-ly", "-ous"),
        ("What does 'childhood' mean?", "The state or period of being a child", "A childlike action", "A group of children", "A child who teaches"),
        ("Which prefix means 'half'?", "semi-", "poly-", "mono-", "hyper-"),
        ("What does 'bilingual' mean?", "Able to use two languages", "Able to use one language", "Able to use many languages", "Unable to use language"),
        ("Which prefix means 'excessive or above normal'?", "hyper-", "hypo-", "sub-", "infra-"),
        ("What does 'hypothermia' refer to?", "Abnormally low body temperature", "Abnormally high body temperature", "Normal body temperature", "Body temperature after exercise"),
        ("Which word contains a suffix that means 'the study of'?", "Biology", "Biologist", "Biological", "Biologically"),
        ("What does the suffix '-phobia' mean?", "Fear", "Love", "Study", "Writing"),
        ("Which word means 'the study of plants'?", "Botany", "Zoology", "Geology", "Astronomy"),
        ("Which prefix means 'not or opposite of' in 'nonfiction'?", "non-", "re-", "pre-", "over-"),
        ("What does 'postgraduate' mean?", "After graduation", "Before graduation", "During childhood", "Without graduation"),
        ("Which suffix forms an adjective from 'danger'?", "-ous", "-ness", "-ment", "-ly"),
        ("Which word is formed using the prefix 'over-'?", "Overcook", "Undercook", "Recook", "Misread"),
        ("What does 'underestimate' mean?", "Estimate as less than the actual amount", "Estimate as more than the actual amount", "Estimate accurately", "Estimate again"),
        ("Which suffix means 'capable of being'?", "-ible", "-ist", "-ism", "-ship"),
        ("Which word contains the suffix '-ist' indicating a person?", "Scientist", "Scientific", "Science", "Scientifically"),
        ("What does the prefix 'auto-' mean?", "Self", "Many", "Against", "Between"),
        ("What does 'autobiography' mean?", "A person's account of their own life", "A story about another person's life", "A fictional scientific story", "A collection of poems"),
    ],

    "Hard": [
        ("In 'antidisestablishmentarianism', which prefix means 'against'?", "anti-", "dis-", "re-", "pre-"),
        ("Which word contains a prefix meaning 'beyond'?", "Transcend", "Submerge", "Bilingual", "Monologue"),
        ("What does the suffix '-ology' denote?", "A field of study", "A person who studies", "A fear of something", "A written account"),
        ("Which suffix forms an abstract noun from 'accurate'?", "-acy", "-ous", "-ive", "-ly"),
        ("Which word contains a prefix meaning 'within'?", "Intravenous", "International", "Transatlantic", "Subterranean"),
        ("What does the prefix 'neo-' mean?", "New", "Old", "False", "Against"),
        ("Which word means 'a person who studies human societies and cultures'?", "Anthropologist", "Archaeology", "Geologist", "Biographer"),
        ("Which suffix means 'the act or process of'?", "-tion", "-less", "-ish", "-ous"),
        ("Which word is formed by adding a prefix meaning 'wrongly'?", "Misinterpret", "Reconsider", "Preview", "Subdivide"),
        ("What does 'counterproductive' mean?", "Producing the opposite of the desired result", "Producing an excellent result", "Producing no measurable result", "Producing the same result repeatedly"),
        ("Which prefix means 'all'?", "omni-", "uni-", "semi-", "micro-"),
        ("What does 'omniscient' mean?", "Knowing everything", "Seeing everything", "Being everywhere", "Having no knowledge"),
        ("Which suffix indicates a doctrine or system of belief?", "-ism", "-ist", "-ity", "-ment"),
        ("Which word contains a suffix meaning 'the quality or state of'?", "Simplicity", "Simplify", "Simplistic", "Simply"),
        ("What does the prefix 'equ(i)-' mean?", "Equal", "Different", "Small", "Large"),
        ("Which word means 'having equal sides'?", "Equilateral", "Equidistant", "Equivalent", "Equinox"),
        ("What does the prefix 'pseudo-' mean?", "False or not genuine", "True or genuine", "Very small", "Extremely large"),
        ("Which word means 'a false name used by an author'?", "Pseudonym", "Synonym", "Antonym", "Homonym"),
        ("Which suffix means 'the practice or condition of'?", "-ery", "-ous", "-able", "-ful"),
        ("Which word contains a suffix that indicates a specialist or practitioner?", "Cardiologist", "Cardiology", "Cardiac", "Cardiovascular"),
        ("What does the prefix 'infra-' mean?", "Below", "Above", "Across", "Between"),
        ("Which word means 'existing below the surface of the Earth'?", "Underground", "Overground", "Transcontinental", "Interstellar"),
        ("What does 'retroactive' mean?", "Taking effect from a time in the past", "Taking effect only in the future", "Having no effect", "Taking effect repeatedly"),
        ("Which prefix means 'against or opposite' in 'contradict'?", "contra-", "extra-", "intra-", "ultra-"),
        ("Which word contains a suffix meaning 'able to be heard'?", "Audible", "Audience", "Audition", "Auditory"),
        ("What does the suffix '-escence' generally indicate?", "A process or state of developing", "A person who performs an action", "A lack of something", "A place where something is kept"),
        ("Which word means 'the act of making something less severe'?", "Mitigation", "Magnification", "Modification", "Qualification"),
        ("Which prefix means 'many' in 'polyglot'?", "poly-", "mono-", "bi-", "semi-"),
        ("What does the suffix '-cracy' mean?", "Rule or government", "Fear", "Study", "Writing"),
        ("Which word means 'government by the people'?", "Democracy", "Aristocracy", "Autocracy", "Bureaucracy"),
    ]
}


def validate_bank():
    if set(BANK.keys()) != {"Easy", "Medium", "Hard"}:
        raise ValueError("Bank must contain Easy, Medium, and Hard categories.")

    for difficulty, questions in BANK.items():
        if len(questions) != 30:
            raise ValueError(
                f"{difficulty} has {len(questions)} questions instead of 30."
            )

        for index, item in enumerate(questions, start=1):
            if len(item) != 5:
                raise ValueError(
                    f"{difficulty} question {index} must contain 5 values."
                )

            question, correct, wrong1, wrong2, wrong3 = item
            options = [correct, wrong1, wrong2, wrong3]

            if len(set(options)) != 4:
                raise ValueError(
                    f"Duplicate options in {difficulty} question {index}: {question}"
                )

            if not all(isinstance(value, str) and value.strip() for value in item):
                raise ValueError(
                    f"Empty or invalid text in {difficulty} question {index}."
                )

    print("VALIDATION PASSED: 30 unique-option questions per difficulty.")


def main():
    validate_bank()

    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute("""
            SELECT id, title
            FROM lessons
            WHERE id = 153 AND topic = 'English'
        """)

        lesson = cur.fetchone()

        if not lesson:
            raise ValueError(
                "Lesson ID 153 with topic 'English' was not found."
            )

        lesson_id, title = lesson
        print(f"\nFound lesson: {title} (ID: {lesson_id})")

        for difficulty, questions in BANK.items():

            cur.execute("""
                SELECT id
                FROM quizzes
                WHERE lesson_id = ? AND difficulty = ?
                ORDER BY id
            """, (lesson_id, difficulty))

            quiz_rows = cur.fetchall()

            if len(quiz_rows) > 1:
                raise ValueError(
                    f"Multiple {difficulty} quizzes found for lesson {lesson_id}. "
                    "Please inspect the database."
                )

            if quiz_rows:
                quiz_id = quiz_rows[0][0]
            else:
                cur.execute("""
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                """, (
                    lesson_id,
                    f"{title} - {difficulty}",
                    difficulty
                ))

                quiz_id = cur.lastrowid

            cur.execute("""
                SELECT COUNT(*)
                FROM questions
                WHERE quiz_id = ?
            """, (quiz_id,))

            existing_count = cur.fetchone()[0]

            if existing_count > 30:
                raise ValueError(
                    f"{difficulty} already has {existing_count} questions. "
                    "No changes will be committed."
                )

            cur.execute("""
                SELECT question
                FROM questions
                WHERE quiz_id = ?
            """, (quiz_id,))

            used_questions = {row[0] for row in cur.fetchall()}

            for question, correct, wrong1, wrong2, wrong3 in questions:

                if existing_count >= 30:
                    break

                final_question = question
                version = 2

                while final_question in used_questions:
                    final_question = f"{question} (Version {version})"
                    version += 1

                options = [correct, wrong1, wrong2, wrong3]
                random.shuffle(options)

                correct_letter = "ABCD"[options.index(correct)]

                cur.execute("""
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
                    final_question,
                    options[0],
                    options[1],
                    options[2],
                    options[3],
                    correct_letter
                ))

                used_questions.add(final_question)
                existing_count += 1

            cur.execute("""
                SELECT COUNT(*)
                FROM questions
                WHERE quiz_id = ?
            """, (quiz_id,))

            final_count = cur.fetchone()[0]

            if final_count != 30:
                raise ValueError(
                    f"{difficulty} has {final_count}/30 questions after insertion."
                )

            print(f"{difficulty}: {final_count}/30 SUCCESS")

        con.commit()

        print("\n========================================")
        print("SUCCESS: PREFIXES AND SUFFIXES COMPLETE")
        print("Easy:   30/30")
        print("Medium: 30/30")
        print("Hard:   30/30")
        print("TOTAL:  90/90 QUESTIONS")
        print("========================================")

    except Exception as error:
        con.rollback()
        print("\nERROR:", error)
        print("All database changes have been rolled back.")

    finally:
        con.close()


if __name__ == "__main__":
    main()
