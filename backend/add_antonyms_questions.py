
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("Choose the antonym of Happy.", "Sad", "Joyful", "Cheerful", "Glad"),
        ("Choose the antonym of Hot.", "Cold", "Warm", "Boiling", "Heated"),
        ("Choose the antonym of Big.", "Small", "Huge", "Large", "Giant"),
        ("Choose the antonym of Fast.", "Slow", "Quick", "Rapid", "Swift"),
        ("Choose the antonym of Rich.", "Poor", "Wealthy", "Prosperous", "Affluent"),
        ("Choose the antonym of Clean.", "Dirty", "Neat", "Tidy", "Spotless"),
        ("Choose the antonym of Strong.", "Weak", "Powerful", "Mighty", "Tough"),
        ("Choose the antonym of Beautiful.", "Ugly", "Pretty", "Attractive", "Lovely"),
        ("Choose the antonym of Early.", "Late", "Prompt", "Timely", "Punctual"),
        ("Choose the antonym of Open.", "Closed", "Unlocked", "Accessible", "Available"),
        ("Choose the antonym of Tall.", "Short", "High", "Elevated", "Towering"),
        ("Choose the antonym of Day.", "Night", "Morning", "Afternoon", "Sunrise"),
        ("Choose the antonym of Laugh.", "Cry", "Smile", "Giggle", "Chuckle"),
        ("Choose the antonym of Give.", "Take", "Offer", "Donate", "Present"),
        ("Choose the antonym of Full.", "Empty", "Packed", "Complete", "Loaded"),
        ("Choose the antonym of Easy.", "Difficult", "Simple", "Effortless", "Straightforward"),
        ("Choose the antonym of Young.", "Old", "New", "Fresh", "Recent"),
        ("Choose the antonym of Love.", "Hate", "Adore", "Like", "Admire"),
        ("Choose the antonym of Start.", "Finish", "Begin", "Commence", "Initiate"),
        ("Choose the antonym of Inside.", "Outside", "Interior", "Within", "Inner"),
        ("Choose the antonym of Wet.", "Dry", "Damp", "Moist", "Soaked"),
        ("Choose the antonym of Sweet.", "Bitter", "Sugary", "Delicious", "Syrupy"),
        ("Choose the antonym of Friend.", "Enemy", "Partner", "Ally", "Companion"),
        ("Choose the antonym of Safe.", "Dangerous", "Secure", "Protected", "Harmless"),
        ("Choose the antonym of Bright.", "Dark", "Shiny", "Brilliant", "Glowing"),
        ("Choose the antonym of Near.", "Far", "Close", "Nearby", "Adjacent"),
        ("Choose the antonym of True.", "False", "Correct", "Accurate", "Genuine"),
        ("Choose the antonym of Buy.", "Sell", "Purchase", "Acquire", "Obtain"),
        ("Choose the antonym of Increase.", "Decrease", "Grow", "Expand", "Rise"),
        ("Choose the antonym of Always.", "Never", "Forever", "Constantly", "Frequently")
    ],

    "Medium": [
        ("Choose the antonym of Abundant.", "Scarce", "Plentiful", "Ample", "Numerous"),
        ("Choose the antonym of Ancient.", "Modern", "Old", "Historic", "Antique"),
        ("Choose the antonym of Generous.", "Stingy", "Kind", "Giving", "Charitable"),
        ("Choose the antonym of Victory.", "Defeat", "Triumph", "Success", "Achievement"),
        ("Choose the antonym of Expand.", "Contract", "Enlarge", "Extend", "Broaden"),
        ("Choose the antonym of Permanent.", "Temporary", "Lasting", "Enduring", "Constant"),
        ("Choose the antonym of Optimistic.", "Pessimistic", "Hopeful", "Positive", "Confident"),
        ("Choose the antonym of Transparent.", "Opaque", "Clear", "See-through", "Translucent"),
        ("Choose the antonym of Artificial.", "Natural", "Synthetic", "Man-made", "Imitation"),
        ("Choose the antonym of Humble.", "Arrogant", "Modest", "Unassuming", "Meek"),
        ("Choose the antonym of Compulsory.", "Optional", "Mandatory", "Required", "Obligatory"),
        ("Choose the antonym of Flexible.", "Rigid", "Adaptable", "Elastic", "Adjustable"),
        ("Choose the antonym of Diligent.", "Lazy", "Hardworking", "Industrious", "Dedicated"),
        ("Choose the antonym of Praise.", "Criticize", "Compliment", "Applaud", "Appreciate"),
        ("Choose the antonym of Conceal.", "Reveal", "Hide", "Cover", "Disguise"),
        ("Choose the antonym of Innocent.", "Guilty", "Blameless", "Pure", "Harmless"),
        ("Choose the antonym of Frequent.", "Rare", "Regular", "Common", "Repeated"),
        ("Choose the antonym of Accept.", "Reject", "Receive", "Approve", "Welcome"),
        ("Choose the antonym of Prosperity.", "Poverty", "Wealth", "Success", "Fortune"),
        ("Choose the antonym of Include.", "Exclude", "Contain", "Involve", "Incorporate"),
        ("Choose the antonym of Elaborate.", "Simple", "Detailed", "Complex", "Intricate"),
        ("Choose the antonym of Hostile.", "Friendly", "Aggressive", "Unfriendly", "Antagonistic"),
        ("Choose the antonym of Superior.", "Inferior", "Excellent", "Better", "Higher"),
        ("Choose the antonym of Authentic.", "Fake", "Genuine", "Real", "Original"),
        ("Choose the antonym of Advance.", "Retreat", "Progress", "Proceed", "Develop"),
        ("Choose the antonym of Maximum.", "Minimum", "Greatest", "Highest", "Utmost"),
        ("Choose the antonym of Artificially.", "Naturally", "Mechanically", "Deliberately", "Intentionally"),
        ("Choose the antonym of Encourage.", "Discourage", "Motivate", "Inspire", "Support"),
        ("Choose the antonym of Reveal.", "Conceal", "Disclose", "Expose", "Uncover"),
        ("Choose the antonym of Lenient.", "Strict", "Tolerant", "Forgiving", "Merciful")
    ],

    "Hard": [
        ("Choose the antonym of Benevolent.", "Malevolent", "Charitable", "Compassionate", "Kind"),
        ("Choose the antonym of Meticulous.", "Careless", "Thorough", "Precise", "Detailed"),
        ("Choose the antonym of Ephemeral.", "Eternal", "Brief", "Temporary", "Short-lived"),
        ("Choose the antonym of Obsolete.", "Current", "Outdated", "Ancient", "Archaic"),
        ("Choose the antonym of Ambiguous.", "Unambiguous", "Vague", "Unclear", "Uncertain"),
        ("Choose the antonym of Candid.", "Deceitful", "Frank", "Honest", "Open"),
        ("Choose the antonym of Frugal.", "Extravagant", "Economical", "Thrifty", "Prudent"),
        ("Choose the antonym of Vivid.", "Dull", "Bright", "Lively", "Brilliant"),
        ("Choose the antonym of Reluctant.", "Willing", "Unwilling", "Hesitant", "Unenthusiastic"),
        ("Choose the antonym of Tranquil.", "Agitated", "Peaceful", "Calm", "Serene"),
        ("Choose the antonym of Exaggerate.", "Understate", "Overstate", "Amplify", "Emphasize"),
        ("Choose the antonym of Scrutinize.", "Overlook", "Examine", "Inspect", "Analyze"),
        ("Choose the antonym of Rigid.", "Flexible", "Stiff", "Inflexible", "Strict"),
        ("Choose the antonym of Lucid.", "Confusing", "Clear", "Understandable", "Intelligible"),
        ("Choose the antonym of Arduous.", "Easy", "Difficult", "Demanding", "Strenuous"),
        ("Choose the antonym of Inevitable.", "Avoidable", "Unavoidable", "Certain", "Inescapable"),
        ("Choose the antonym of Hostile.", "Amicable", "Aggressive", "Antagonistic", "Unfriendly"),
        ("Choose the antonym of Dormant.", "Active", "Inactive", "Sleeping", "Motionless"),
        ("Choose the antonym of Eloquent.", "Inarticulate", "Fluent", "Expressive", "Articulate"),
        ("Choose the antonym of Adversity.", "Prosperity", "Hardship", "Misfortune", "Difficulty"),
        ("Choose the antonym of Prolific.", "Unproductive", "Fruitful", "Productive", "Creative"),
        ("Choose the antonym of Omit.", "Include", "Exclude", "Leave out", "Neglect"),
        ("Choose the antonym of Concur.", "Disagree", "Agree", "Approve", "Consent"),
        ("Choose the antonym of Deteriorate.", "Improve", "Worsen", "Decline", "Degenerate"),
        ("Choose the antonym of Sporadic.", "Continuous", "Occasional", "Irregular", "Infrequent"),
        ("Choose the antonym of Subtle.", "Obvious", "Delicate", "Faint", "Slight"),
        ("Choose the antonym of Ascend.", "Descend", "Climb", "Rise", "Soar"),
        ("Choose the antonym of Vindicate.", "Condemn", "Justify", "Defend", "Clear"),
        ("Choose the antonym of Impartial.", "Biased", "Fair", "Neutral", "Objective"),
        ("Choose the antonym of Concise.", "Verbose", "Brief", "Succinct", "Compact")
    ]
}


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Antonyms", "English")
        )
        row = cur.fetchone()

        if not row:
            raise Exception(
                "Lesson 'Antonyms' with topic 'English' was not found."
            )

        lesson_id = row[0]

        for difficulty, questions in BANK.items():

            if len(questions) != 30:
                raise Exception(
                    f"{difficulty} bank must contain exactly 30 questions."
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
                    (lesson_id, f"Antonyms - {difficulty}", difficulty)
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
                suffix = 2

                while True:
                    cur.execute(
                        """
                        SELECT COUNT(*) FROM questions
                        WHERE quiz_id=? AND question=?
                        """,
                        (quiz_id, question_text)
                    )

                    if cur.fetchone()[0] == 0:
                        break

                    question_text = f"{question} (Version {suffix})"
                    suffix += 1

                cur.execute(
                    """
                    INSERT INTO questions
                    (quiz_id, question, option_a, option_b,
                     option_c, option_d, correct_answer)
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

            print(
                f"{difficulty}: {final_count}/30 questions ready."
            )

        con.commit()
        print("\nSUCCESS: Antonyms has exactly 90 questions!")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
