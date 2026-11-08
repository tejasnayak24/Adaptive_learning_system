
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("Choose the synonym of Happy.", "Joyful", "Angry", "Sad", "Tired"),
        ("Choose the antonym of Hot.", "Cold", "Warm", "Boiling", "Burning"),
        ("What does 'Enormous' mean?", "Very large", "Very small", "Very weak", "Very short"),
        ("Choose the synonym of Quick.", "Fast", "Slow", "Late", "Lazy"),
        ("What does 'Ancient' mean?", "Very old", "Very new", "Very modern", "Very recent"),
        ("Choose the antonym of Brave.", "Cowardly", "Courageous", "Fearless", "Bold"),
        ("What does 'Tiny' mean?", "Very small", "Very large", "Very heavy", "Very bright"),
        ("Choose the synonym of Begin.", "Start", "Finish", "Stop", "Close"),
        ("What does 'Honest' mean?", "Truthful", "Dishonest", "Careless", "Rude"),
        ("Choose the antonym of Generous.", "Selfish", "Kind", "Giving", "Helpful"),
        ("What does 'Rapid' mean?", "Fast", "Weak", "Quiet", "Dull"),
        ("Choose the synonym of Beautiful.", "Attractive", "Ugly", "Awful", "Unpleasant"),
        ("What does 'Exhausted' mean?", "Extremely tired", "Very excited", "Very hungry", "Very confused"),
        ("Choose the antonym of Victory.", "Defeat", "Success", "Achievement", "Triumph"),
        ("What does 'Fragile' mean?", "Easily broken", "Very strong", "Very heavy", "Difficult to move"),
        ("Choose the synonym of Silent.", "Quiet", "Noisy", "Loud", "Busy"),
        ("What does 'Polite' mean?", "Well-mannered", "Rude", "Angry", "Careless"),
        ("Choose the antonym of Accept.", "Reject", "Receive", "Agree", "Approve"),
        ("What does 'Wealthy' mean?", "Rich", "Poor", "Weak", "Famous"),
        ("Choose the synonym of Difficult.", "Hard", "Easy", "Simple", "Clear"),
        ("What does 'Vacant' mean?", "Empty", "Full", "Occupied", "Crowded"),
        ("Choose the antonym of Expand.", "Contract", "Increase", "Enlarge", "Extend"),
        ("What does 'Assist' mean?", "Help", "Hinder", "Ignore", "Refuse"),
        ("Choose the synonym of Angry.", "Furious", "Calm", "Peaceful", "Cheerful"),
        ("What does 'Cautious' mean?", "Careful", "Reckless", "Careless", "Hasty"),
        ("Choose the antonym of Include.", "Exclude", "Contain", "Involve", "Add"),
        ("What does 'Purchase' mean?", "Buy", "Sell", "Borrow", "Lend"),
        ("Choose the synonym of Famous.", "Well-known", "Unknown", "Ordinary", "Hidden"),
        ("What does 'Observe' mean?", "Watch carefully", "Forget quickly", "Avoid completely", "Speak loudly"),
        ("Choose the antonym of Permanent.", "Temporary", "Lasting", "Enduring", "Fixed")
    ],

    "Medium": [
        ("Choose the meaning of Meticulous.", "Extremely careful and precise", "Careless and hurried", "Loud and aggressive", "Easily frightened"),
        ("Choose the synonym of Reluctant.", "Unwilling", "Eager", "Confident", "Certain"),
        ("What does 'Ambiguous' mean?", "Open to more than one interpretation", "Completely obvious", "Highly accurate", "Impossible to understand"),
        ("Choose the antonym of Optimistic.", "Pessimistic", "Hopeful", "Positive", "Confident"),
        ("What does 'Benevolent' mean?", "Kind and generous", "Cruel and selfish", "Weak and uncertain", "Proud and arrogant"),
        ("Choose the synonym of Inevitable.", "Unavoidable", "Unlikely", "Optional", "Preventable"),
        ("What does 'Concise' mean?", "Brief but clear", "Long and confusing", "Unnecessarily detailed", "Difficult to pronounce"),
        ("Choose the antonym of Artificial.", "Natural", "Synthetic", "Manufactured", "Imitation"),
        ("What does 'Diligent' mean?", "Hardworking and careful", "Lazy and careless", "Angry and impatient", "Shy and nervous"),
        ("Choose the synonym of Obsolete.", "Outdated", "Modern", "Popular", "Useful"),
        ("What does 'Resilient' mean?", "Able to recover from difficulties", "Easily defeated", "Unable to change", "Always successful"),
        ("Choose the antonym of Scarce.", "Abundant", "Limited", "Rare", "Insufficient"),
        ("What does 'Arrogant' mean?", "Having an exaggerated sense of self-importance", "Being humble and modest", "Showing kindness", "Feeling uncertain"),
        ("Choose the synonym of Commence.", "Begin", "Conclude", "Postpone", "Cancel"),
        ("What does 'Versatile' mean?", "Able to adapt to many different functions", "Limited to one activity", "Unable to learn", "Extremely fragile"),
        ("Choose the antonym of Transparent.", "Opaque", "Clear", "Visible", "Obvious"),
        ("What does 'Scrutinize' mean?", "Examine very carefully", "Ignore completely", "Approve immediately", "Destroy deliberately"),
        ("Choose the synonym of Hostile.", "Unfriendly", "Friendly", "Generous", "Supportive"),
        ("What does 'Pragmatic' mean?", "Practical and realistic", "Imaginative and unrealistic", "Emotional and sensitive", "Careless and confused"),
        ("Choose the antonym of Compulsory.", "Optional", "Mandatory", "Essential", "Required"),
        ("What does 'Impartial' mean?", "Fair and unbiased", "Prejudiced", "Selfish", "Unreliable"),
        ("Choose the synonym of Abundant.", "Plentiful", "Insufficient", "Limited", "Scarce"),
        ("What does 'Conspicuous' mean?", "Easily noticed", "Difficult to detect", "Completely hidden", "Unimportant"),
        ("Choose the antonym of Vague.", "Precise", "Unclear", "Uncertain", "Ambiguous"),
        ("What does 'Futile' mean?", "Producing no useful result", "Highly successful", "Extremely valuable", "Easy to achieve"),
        ("Choose the synonym of Eloquent.", "Fluent and persuasive", "Silent and shy", "Confused and unclear", "Rude and aggressive"),
        ("What does 'Alleviate' mean?", "Make something less severe", "Make something worse", "Create a new problem", "Prevent all progress"),
        ("Choose the antonym of Fragile.", "Sturdy", "Delicate", "Breakable", "Weak"),
        ("What does 'Scrupulous' mean?", "Very careful and honest", "Dishonest and careless", "Impatient and rude", "Uncertain and fearful"),
        ("Choose the synonym of Tranquil.", "Peaceful", "Chaotic", "Violent", "Restless")
    ],

    "Hard": [
        ("What does 'Ubiquitous' mean?", "Present or found everywhere", "Extremely rare", "Completely invisible", "Limited to one location"),
        ("Choose the synonym of Ephemeral.", "Short-lived", "Permanent", "Ancient", "Unchanging"),
        ("What does 'Obfuscate' mean?", "Make something unclear or confusing", "Explain something clearly", "Make something visible", "Simplify a difficult idea"),
        ("Choose the antonym of Altruistic.", "Selfish", "Selfless", "Generous", "Compassionate"),
        ("What does 'Pernicious' mean?", "Having a harmful or destructive effect", "Extremely beneficial", "Completely harmless", "Highly entertaining"),
        ("Choose the synonym of Loquacious.", "Talkative", "Silent", "Reserved", "Unresponsive"),
        ("What does 'Fastidious' mean?", "Very attentive to detail and difficult to please", "Careless about quality", "Easily satisfied", "Uninterested in details"),
        ("Choose the antonym of Laconic.", "Verbose", "Brief", "Concise", "Terse"),
        ("What does 'Equivocal' mean?", "Open to multiple interpretations", "Completely definite", "Highly accurate", "Easy to verify"),
        ("Choose the synonym of Gregarious.", "Sociable", "Introverted", "Solitary", "Unsociable"),
        ("What does 'Intransigent' mean?", "Unwilling to compromise", "Open to negotiation", "Easily persuaded", "Flexible in decisions"),
        ("Choose the antonym of Capricious.", "Consistent", "Unpredictable", "Erratic", "Impulsive"),
        ("What does 'Magnanimous' mean?", "Generous and forgiving", "Petty and revengeful", "Selfish and greedy", "Fearful and hesitant"),
        ("Choose the synonym of Sagacious.", "Wise", "Foolish", "Ignorant", "Careless"),
        ("What does 'Esoteric' mean?", "Understood by only a small group with specialized knowledge", "Known by everyone", "Easy for beginners", "Commonly available"),
        ("Choose the antonym of Belligerent.", "Peaceful", "Aggressive", "Hostile", "Combative"),
        ("What does 'Prolific' mean?", "Producing a large amount", "Producing very little", "Unable to create", "Rarely occurring"),
        ("Choose the synonym of Pernicious.", "Destructive", "Beneficial", "Harmless", "Constructive"),
        ("What does 'Obsequious' mean?", "Excessively eager to please or obey", "Strongly independent", "Openly rebellious", "Completely indifferent"),
        ("Choose the antonym of Ephemeral.", "Enduring", "Temporary", "Brief", "Momentary"),
        ("What does 'Enervate' mean?", "To weaken or drain energy", "To strengthen greatly", "To encourage enthusiastically", "To make more efficient"),
        ("Choose the synonym of Clandestine.", "Secret", "Public", "Obvious", "Official"),
        ("What does 'Quintessential' mean?", "Representing the most perfect example of something", "Being completely unrelated", "Showing an unusual exception", "Having little importance"),
        ("Choose the antonym of Reticent.", "Talkative", "Reserved", "Silent", "Uncommunicative"),
        ("What does 'Recalcitrant' mean?", "Stubbornly resistant to authority", "Eager to cooperate", "Willing to obey", "Easy to persuade"),
        ("Choose the synonym of Sanguine.", "Optimistic", "Pessimistic", "Anxious", "Hopeless"),
        ("What does 'Abstruse' mean?", "Difficult to understand", "Simple and obvious", "Easy to remember", "Clearly explained"),
        ("Choose the antonym of Ostentatious.", "Unpretentious", "Showy", "Flashy", "Excessive"),
        ("What does 'Vicissitude' mean?", "A change in circumstances or fortune", "A permanent condition", "A fixed belief", "A deliberate deception"),
        ("Choose the synonym of Tenacious.", "Persistent", "Weak-willed", "Indifferent", "Careless")
    ]
}


def validate_bank():
    for difficulty, questions in BANK.items():
        if len(questions) != 30:
            raise ValueError(
                f"{difficulty} must contain exactly 30 questions."
            )

        for item in questions:
            if len(item) != 5:
                raise ValueError(f"Invalid question format: {item}")

            question, answer, wrong1, wrong2, wrong3 = item
            options = [answer, wrong1, wrong2, wrong3]

            if len(set(options)) != 4:
                raise ValueError(
                    f"Duplicate options in {difficulty}: {question}"
                )


def main():
    validate_bank()
    print("Question bank validation successful.")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Vocabulary Building", "English")
        )
        row = cur.fetchone()

        if not row:
            raise Exception(
                "Lesson 'Vocabulary Building' with topic 'English' was not found."
            )

        lesson_id = row[0]

        for difficulty, questions in BANK.items():
            cur.execute(
                """
                SELECT id FROM quizzes
                WHERE lesson_id=? AND difficulty=?
                """,
                (lesson_id, difficulty)
            )
            quiz = cur.fetchone()

            if quiz:
                quiz_id = quiz[0]
            else:
                cur.execute(
                    """
                    INSERT INTO quizzes
                    (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                    """,
                    (
                        lesson_id,
                        f"Vocabulary Building - {difficulty}",
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
                    f"{difficulty} already has {existing} questions."
                )

            inserted = 0

            for question, answer, wrong1, wrong2, wrong3 in questions:
                if existing + inserted >= 30:
                    break

                options = [answer, wrong1, wrong2, wrong3]
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
                    (
                        quiz_id, question,
                        option_a, option_b, option_c, option_d,
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
        print("\nSUCCESS: Vocabulary Building has exactly 90 questions!")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
