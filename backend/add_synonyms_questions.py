
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("Choose the synonym of Happy.", "Joyful", "Angry", "Sad", "Tired"),
        ("Choose the synonym of Big.", "Large", "Tiny", "Short", "Narrow"),
        ("Choose the synonym of Small.", "Tiny", "Huge", "Tall", "Wide"),
        ("Choose the synonym of Quick.", "Fast", "Slow", "Weak", "Late"),
        ("Choose the synonym of Beautiful.", "Pretty", "Ugly", "Rough", "Dirty"),
        ("Choose the synonym of Smart.", "Clever", "Foolish", "Lazy", "Careless"),
        ("Choose the synonym of Angry.", "Furious", "Calm", "Cheerful", "Gentle"),
        ("Choose the synonym of Begin.", "Start", "Finish", "Stop", "Close"),
        ("Choose the synonym of End.", "Finish", "Start", "Open", "Continue"),
        ("Choose the synonym of Silent.", "Quiet", "Noisy", "Loud", "Busy"),
        ("Choose the synonym of Rich.", "Wealthy", "Poor", "Weak", "Hungry"),
        ("Choose the synonym of Brave.", "Courageous", "Cowardly", "Afraid", "Shy"),
        ("Choose the synonym of Easy.", "Simple", "Difficult", "Complicated", "Hard"),
        ("Choose the synonym of Difficult.", "Hard", "Simple", "Easy", "Clear"),
        ("Choose the synonym of Friend.", "Companion", "Enemy", "Stranger", "Opponent"),
        ("Choose the synonym of Gift.", "Present", "Punishment", "Debt", "Loss"),
        ("Choose the synonym of Help.", "Assist", "Harm", "Ignore", "Prevent"),
        ("Choose the synonym of Correct.", "Right", "Wrong", "False", "Unfair"),
        ("Choose the synonym of Wrong.", "Incorrect", "Accurate", "Proper", "True"),
        ("Choose the synonym of Richness.", "Abundance", "Poverty", "Shortage", "Weakness"),
        ("Choose the synonym of Reply.", "Answer", "Question", "Request", "Silence"),
        ("Choose the synonym of Afraid.", "Scared", "Confident", "Fearless", "Relaxed"),
        ("Choose the synonym of Honest.", "Truthful", "Dishonest", "Rude", "Greedy"),
        ("Choose the synonym of Famous.", "Popular", "Unknown", "Ordinary", "Hidden"),
        ("Choose the synonym of Near.", "Close", "Far", "Distant", "Separate"),
        ("Choose the synonym of Look.", "See", "Hide", "Ignore", "Forget"),
        ("Choose the synonym of Angryness.", "Irritation", "Happiness", "Peace", "Excitement"),
        ("Choose the synonym of Old.", "Ancient", "Modern", "New", "Fresh"),
        ("Choose the synonym of Weak.", "Feeble", "Strong", "Powerful", "Healthy"),
        ("Choose the synonym of Buy.", "Purchase", "Sell", "Borrow", "Lend")
    ],

    "Medium": [
        ("Choose the synonym of Abundant.", "Plentiful", "Scarce", "Limited", "Insufficient"),
        ("Choose the synonym of Accurate.", "Precise", "Vague", "Incorrect", "Careless"),
        ("Choose the synonym of Admire.", "Respect", "Despise", "Dislike", "Avoid"),
        ("Choose the synonym of Ancient.", "Antique", "Recent", "Modern", "Current"),
        ("Choose the synonym of Anxious.", "Worried", "Carefree", "Relaxed", "Certain"),
        ("Choose the synonym of Assist.", "Support", "Oppose", "Prevent", "Refuse"),
        ("Choose the synonym of Brief.", "Concise", "Lengthy", "Detailed", "Extended"),
        ("Choose the synonym of Cautious.", "Careful", "Reckless", "Careless", "Hasty"),
        ("Choose the synonym of Conceal.", "Hide", "Reveal", "Display", "Expose"),
        ("Choose the synonym of Confident.", "Assured", "Doubtful", "Uncertain", "Timid"),
        ("Choose the synonym of Decline.", "Decrease", "Increase", "Expand", "Improve"),
        ("Choose the synonym of Delicate.", "Fragile", "Sturdy", "Strong", "Durable"),
        ("Choose the synonym of Eager.", "Enthusiastic", "Reluctant", "Unwilling", "Indifferent"),
        ("Choose the synonym of Eliminate.", "Remove", "Retain", "Preserve", "Maintain"),
        ("Choose the synonym of Enormous.", "Immense", "Minute", "Tiny", "Narrow"),
        ("Choose the synonym of Essential.", "Necessary", "Optional", "Unimportant", "Unnecessary"),
        ("Choose the synonym of Expand.", "Enlarge", "Reduce", "Shrink", "Contract"),
        ("Choose the synonym of Generous.", "Giving", "Selfish", "Greedy", "Mean"),
        ("Choose the synonym of Genuine.", "Authentic", "Fake", "Artificial", "False"),
        ("Choose the synonym of Hostile.", "Unfriendly", "Friendly", "Kind", "Welcoming"),
        ("Choose the synonym of Imitate.", "Copy", "Invent", "Create", "Ignore"),
        ("Choose the synonym of Mandatory.", "Compulsory", "Optional", "Voluntary", "Unnecessary"),
        ("Choose the synonym of Obvious.", "Evident", "Hidden", "Unclear", "Doubtful"),
        ("Choose the synonym of Permit.", "Allow", "Forbid", "Prevent", "Reject"),
        ("Choose the synonym of Reluctant.", "Unwilling", "Eager", "Enthusiastic", "Ready"),
        ("Choose the synonym of Significant.", "Important", "Trivial", "Minor", "Meaningless"),
        ("Choose the synonym of Temporary.", "Brief", "Permanent", "Enduring", "Lasting"),
        ("Choose the synonym of Vivid.", "Bright", "Dull", "Faint", "Unclear"),
        ("Choose the synonym of Weary.", "Exhausted", "Energetic", "Active", "Refreshed"),
        ("Choose the synonym of Abandon.", "Forsake", "Continue", "Maintain", "Protect")
    ],

    "Hard": [
        ("Choose the synonym of Ambiguous.", "Unclear", "Obvious", "Certain", "Definite"),
        ("Choose the synonym of Benevolent.", "Kindhearted", "Cruel", "Selfish", "Hostile"),
        ("Choose the synonym of Candid.", "Frank", "Deceptive", "Secretive", "Dishonest"),
        ("Choose the synonym of Diligent.", "Industrious", "Lazy", "Careless", "Idle"),
        ("Choose the synonym of Eloquent.", "Articulate", "Inarticulate", "Silent", "Confused"),
        ("Choose the synonym of Futile.", "Useless", "Effective", "Productive", "Successful"),
        ("Choose the synonym of Gregarious.", "Sociable", "Reserved", "Unsociable", "Withdrawn"),
        ("Choose the synonym of Impeccable.", "Flawless", "Defective", "Imperfect", "Faulty"),
        ("Choose the synonym of Lucid.", "Clear", "Confusing", "Obscure", "Vague"),
        ("Choose the synonym of Meticulous.", "Thorough", "Careless", "Negligent", "Hasty"),
        ("Choose the synonym of Obsolete.", "Outdated", "Modern", "Current", "Contemporary"),
        ("Choose the synonym of Pragmatic.", "Practical", "Idealistic", "Unrealistic", "Impractical"),
        ("Choose the synonym of Resilient.", "Hardy", "Fragile", "Vulnerable", "Delicate"),
        ("Choose the synonym of Scrutinize.", "Examine", "Ignore", "Overlook", "Neglect"),
        ("Choose the synonym of Tranquil.", "Serene", "Agitated", "Chaotic", "Disturbed"),
        ("Choose the synonym of Ubiquitous.", "Omnipresent", "Rare", "Scarce", "Uncommon"),
        ("Choose the synonym of Venerate.", "Revere", "Disrespect", "Despise", "Insult"),
        ("Choose the synonym of Wary.", "Vigilant", "Careless", "Trusting", "Reckless"),
        ("Choose the synonym of Zealous.", "Passionate", "Indifferent", "Apathetic", "Uninterested"),
        ("Choose the synonym of Adversity.", "Hardship", "Prosperity", "Comfort", "Success"),
        ("Choose the synonym of Alleviate.", "Relieve", "Worsen", "Intensify", "Aggravate"),
        ("Choose the synonym of Arduous.", "Laborious", "Effortless", "Easy", "Simple"),
        ("Choose the synonym of Belligerent.", "Aggressive", "Peaceful", "Friendly", "Gentle"),
        ("Choose the synonym of Coherent.", "Logical", "Inconsistent", "Disjointed", "Confusing"),
        ("Choose the synonym of Deplorable.", "Dreadful", "Admirable", "Excellent", "Commendable"),
        ("Choose the synonym of Exonerate.", "Acquit", "Blame", "Convict", "Accuse"),
        ("Choose the synonym of Imminent.", "Impending", "Distant", "Remote", "Unlikely"),
        ("Choose the synonym of Magnanimous.", "Generous", "Petty", "Selfish", "Vindictive"),
        ("Choose the synonym of Novice.", "Beginner", "Expert", "Veteran", "Specialist"),
        ("Choose the synonym of Perpetual.", "Everlasting", "Temporary", "Brief", "Momentary")
    ]
}


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Synonyms", "English")
        )

        row = cur.fetchone()

        if not row:
            raise Exception(
                "Lesson 'Synonyms' with topic 'English' was not found."
            )

        lesson_id = row[0]

        for difficulty, questions in BANK.items():

            if len(questions) != 30:
                raise Exception(
                    f"{difficulty} bank has {len(questions)} questions instead of 30."
                )

            cur.execute(
                "SELECT id FROM quizzes WHERE lesson_id=? AND difficulty=?",
                (lesson_id, difficulty)
            )

            quiz = cur.fetchone()

            if quiz:
                quiz_id = quiz[0]
            else:
                cur.execute(
                    """
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                    """,
                    (
                        lesson_id,
                        f"Synonyms - {difficulty}",
                        difficulty
                    )
                )
                quiz_id = cur.lastrowid

            cur.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id=?",
                (quiz_id,)
            )

            existing = cur.fetchone()[0]

            if existing > 30:
                raise Exception(
                    f"{difficulty} already has {existing} questions. "
                    "Please check the database."
                )

            inserted = 0

            for question, answer, wrong1, wrong2, wrong3 in questions:

                if existing + inserted >= 30:
                    break

                options = [answer, wrong1, wrong2, wrong3]

                if len(set(options)) != 4:
                    raise Exception(
                        f"Duplicate options found: {question}"
                    )

                random.shuffle(options)
                correct_letter = "ABCD"[options.index(answer)]

                question_text = question

                cur.execute(
                    """
                    SELECT COUNT(*) FROM questions
                    WHERE quiz_id=? AND question=?
                    """,
                    (quiz_id, question_text)
                )

                if cur.fetchone()[0] > 0:
                    question_text = question + " (Version 2)"

                cur.execute(
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
                        question_text,
                        options[0],
                        options[1],
                        options[2],
                        options[3],
                        correct_letter
                    )
                )

                inserted += 1

            cur.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id=?",
                (quiz_id,)
            )

            final_count = cur.fetchone()[0]

            if final_count != 30:
                raise Exception(
                    f"{difficulty} has {final_count}/30 questions."
                )

            print(f"{difficulty}: {final_count}/30 questions ready.")

        con.commit()

        print("\nSUCCESS: Synonyms has exactly 90 questions!")
        print("Easy: 30 | Medium: 30 | Hard: 30")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
