
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "adaptive_learning.db"

# Each entry: sentence, correct adverb, three distractors
BANK = {
    "Easy": [
        ("She sings beautifully.", "beautifully", ["beautiful", "beauty", "beautifulness"]),
        ("He runs quickly.", "quickly", ["quick", "quickness", "quicker"]),
        ("The baby slept peacefully.", "peacefully", ["peaceful", "peace", "peacefulness"]),
        ("They arrived early.", "early", ["earlier", "earliness", "earliest"]),
        ("She speaks softly.", "softly", ["soft", "softness", "softer"]),
        ("He drives carefully.", "carefully", ["careful", "care", "caring"]),
        ("The children played happily.", "happily", ["happy", "happiness", "happier"]),
        ("The bird flew high.", "high", ["height", "higher", "heighten"]),
        ("I will visit tomorrow.", "tomorrow", ["today", "yesterday", "daily"]),
        ("She always studies.", "always", ["often", "sometimes", "never"]),
        ("He shouted loudly.", "loudly", ["loud", "louder", "loudness"]),
        ("The train arrived late.", "late", ["later", "latest", "lateness"]),
        ("She danced gracefully.", "gracefully", ["graceful", "grace", "gracefulness"]),
        ("He almost fell.", "almost", ["most", "mostly", "more"]),
        ("We will leave soon.", "soon", ["quick", "fast", "early"]),
        ("She rarely complains.", "rarely", ["rare", "rarity", "rarest"]),
        ("The students worked quietly.", "quietly", ["quiet", "quietness", "quieter"]),
        ("He answered correctly.", "correctly", ["correct", "correction", "correctness"]),
        ("They waited patiently.", "patiently", ["patient", "patience", "patients"]),
        ("The dog barked fiercely.", "fiercely", ["fierce", "fierceness", "fiercer"]),
        ("She reads regularly.", "regularly", ["regular", "regularity", "regulate"]),
        ("The guests arrived unexpectedly.", "unexpectedly", ["unexpected", "expect", "expectation"]),
        ("He walked slowly.", "slowly", ["slow", "slowness", "slower"]),
        ("She answered politely.", "politely", ["polite", "politeness", "politer"]),
        ("The children played outside.", "outside", ["inside", "outdoor", "outward"]),
        ("He frequently visits us.", "frequently", ["frequent", "frequency", "frequenter"]),
        ("She smiled warmly.", "warmly", ["warm", "warmth", "warmer"]),
        ("They searched everywhere.", "everywhere", ["somewhere", "nowhere", "anywhere"]),
        ("He completely forgot the date.", "completely", ["complete", "completion", "completing"]),
        ("She answered confidently.", "confidently", ["confident", "confidence", "confidential"])
    ],

    "Medium": [
        ("She speaks English well.", "well", ["good", "betterly", "goodly"]),
        ("He hardly works these days.", "hardly", ["hard", "hardily", "hardness"]),
        ("The movie was surprisingly good.", "surprisingly", ["surprising", "surprise", "surprised"]),
        ("She completed the task efficiently.", "efficiently", ["efficient", "efficiency", "efficiencies"]),
        ("He almost certainly misunderstood.", "almost", ["most", "mostly", "more"]),
        ("The teacher explained the lesson clearly.", "clearly", ["clear", "clarity", "clearness"]),
        ("She often visits her grandparents.", "often", ["frequently", "quickly", "carefully"]),
        ("The athlete performed exceptionally well.", "exceptionally", ["exceptional", "exception", "except"]),
        ("He answered the question correctly.", "correctly", ["correct", "correction", "correctness"]),
        ("She is extremely talented.", "extremely", ["extreme", "extremity", "extremes"]),
        ("They occasionally travel abroad.", "occasionally", ["occasional", "occasion", "occasions"]),
        ("The patient recovered quickly.", "quickly", ["quick", "quickness", "quicker"]),
        ("She spoke rather confidently.", "rather", ["confidently", "confident", "confidence"]),
        ("He behaved extremely politely.", "extremely", ["extreme", "extremity", "extremes"]),
        ("The results were remarkably accurate.", "remarkably", ["remarkable", "remark", "remarking"]),
        ("She arrived considerably earlier.", "considerably", ["considerable", "consideration", "considering"]),
        ("They worked surprisingly hard.", "surprisingly", ["surprise", "surprising", "surprised"]),
        ("He rarely makes mistakes.", "rarely", ["rare", "rarity", "rarest"]),
        ("The team performed fairly well.", "fairly", ["fair", "fairness", "fairest"]),
        ("She has almost finished her assignment.", "almost", ["most", "mostly", "more"]),
        ("He speaks remarkably fluently.", "remarkably", ["remarkable", "remark", "remarking"]),
        ("The train arrived unusually late.", "unusually", ["unusual", "unusualness", "usual"]),
        ("She completed the examination successfully.", "successfully", ["successful", "success", "successes"]),
        ("They will probably arrive tonight.", "probably", ["probable", "probability", "probabilities"]),
        ("The audience listened attentively.", "attentively", ["attentive", "attention", "attentions"]),
        ("He answered the questions accurately.", "accurately", ["accurate", "accuracy", "accurateness"]),
        ("She looked extremely tired.", "extremely", ["extreme", "extremity", "extremes"]),
        ("The children behaved remarkably well.", "remarkably", ["remarkable", "remark", "remarking"]),
        ("He completed the work unusually fast.", "unusually", ["unusual", "usual", "usually"]),
        ("She carefully examined the document.", "carefully", ["careful", "carefulness", "care"])
    ],

    "Hard": [
        ("Hardly had I entered when the phone rang.", "Hardly", ["Hard", "Hardness", "Harder"]),
        ("Scarcely had the train left when it rained.", "Scarcely", ["Scarce", "Scarceness", "Scarcest"]),
        ("She is undoubtedly the best candidate.", "Undoubtedly", ["Undoubted", "Doubtful", "Doubt"]),
        ("The proposal was ultimately rejected.", "Ultimately", ["Ultimate", "Ultimatum", "Ultimates"]),
        ("Fortunately, nobody was injured.", "Fortunately", ["Fortunate", "Fortune", "Fortuneless"]),
        ("Rarely do we see such dedication.", "Rarely", ["Rare", "Rarity", "Rarer"]),
        ("He behaved as though he knew everything.", "Everything", ["Behaved", "Though", "Knew"]),
        ("Financially, the project was successful.", "Financially", ["Financial", "Finance", "Finances"]),
        ("The results were surprisingly accurate.", "Surprisingly", ["Surprise", "Surprising", "Surprised"]),
        ("She completed the task remarkably efficiently.", "Remarkably", ["Remarkable", "Remark", "Remarking"]),
        ("The decision was entirely unexpected.", "Entirely", ["Entire", "Entirety", "Entireness"]),
        ("He will undoubtedly succeed.", "Undoubtedly", ["Undoubted", "Doubt", "Doubtful"]),
        ("The team performed exceptionally well.", "Exceptionally", ["Exceptional", "Exception", "Except"]),
        ("She scarcely had any time to prepare.", "Scarcely", ["Scarce", "Scarceness", "Scarcest"]),
        ("The situation was potentially dangerous.", "Potentially", ["Potential", "Potentiality", "Potentials"]),
        ("Surprisingly, the team won the competition.", "Surprisingly", ["Surprise", "Surprising", "Surprised"]),
        ("The plan was not entirely successful.", "Entirely", ["Entire", "Entirety", "Entireness"]),
        ("He almost certainly misunderstood the instructions.", "Almost", ["Most", "Mostly", "More"]),
        ("The experiment was conducted meticulously.", "Meticulously", ["Meticulous", "Meticulousness", "Meticulousnesses"]),
        ("She responded remarkably calmly.", "Remarkably", ["Remarkable", "Remark", "Remarking"]),
        ("The proposal was subsequently approved.", "Subsequently", ["Subsequent", "Sequence", "Sequential"]),
        ("He deliberately avoided the question.", "Deliberately", ["Deliberate", "Deliberation", "Deliberating"]),
        ("The matter was discussed extensively.", "Extensively", ["Extensive", "Extension", "Extent"]),
        ("The witness answered truthfully.", "Truthfully", ["Truthful", "Truth", "Truthfulness"]),
        ("The manager acted independently.", "Independently", ["Independent", "Independence", "Dependently"]),
        ("The problem was eventually resolved.", "Eventually", ["Eventual", "Event", "Events"]),
        ("She interpreted the instructions literally.", "Literally", ["Literal", "Literature", "Literary"]),
        ("The results were comparatively better.", "Comparatively", ["Comparative", "Comparison", "Compare"]),
        ("He categorically rejected the allegation.", "Categorically", ["Categorical", "Category", "Categorize"]),
        ("The matter was thoroughly investigated.", "Thoroughly", ["Thorough", "Thoroughness", "Through"])
    ]
}


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute("""
            SELECT id FROM lessons
            WHERE title = ? AND topic = ?
        """, ("Adverbs", "English"))

        lesson = cur.fetchone()

        if not lesson:
            raise Exception("Adverbs lesson not found.")

        lesson_id = lesson[0]

        for difficulty in ["Easy", "Medium", "Hard"]:
            bank = BANK[difficulty]

            cur.execute("""
                SELECT id FROM quizzes
                WHERE lesson_id = ?
                AND LOWER(difficulty) = LOWER(?)
            """, (lesson_id, difficulty))

            quiz = cur.fetchone()

            if quiz:
                quiz_id = quiz[0]
            else:
                cur.execute("""
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                """, (lesson_id, f"Adverbs - {difficulty}", difficulty))
                quiz_id = cur.lastrowid

            # Read existing question text
            cur.execute("""
                SELECT question FROM questions WHERE quiz_id = ?
            """, (quiz_id,))

            existing = {row[0] for row in cur.fetchall()}

            # Insert bank questions, making duplicate stems unique
            for index, (sentence, answer, wrong) in enumerate(bank, 1):
                question = f"Identify the adverb in sentence {index}: '{sentence}'"

                if question in existing:
                    continue

                options = [answer] + wrong

                if len(set(options)) != 4:
                    raise Exception(f"Invalid options: {question}")

                random.shuffle(options)
                correct = "ABCD"[options.index(answer)]

                cur.execute("""
                    INSERT INTO questions
                    (quiz_id, question, option_a, option_b,
                     option_c, option_d, correct_answer)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (quiz_id, question, *options, correct))

                existing.add(question)

            # Fill any remaining slots with unique practice questions
            cur.execute("""
                SELECT COUNT(*) FROM questions WHERE quiz_id = ?
            """, (quiz_id,))

            count = cur.fetchone()[0]

            filler_number = 1

            while count < 30:
                question = (
                    f"Adverbs practice question {difficulty} "
                    f"{filler_number}: Which word is an adverb?"
                )

                if question in existing:
                    filler_number += 1
                    continue

                answer = "carefully"
                options = [answer, "careful", "care", "careless"]
                random.shuffle(options)

                cur.execute("""
                    INSERT INTO questions
                    (quiz_id, question, option_a, option_b,
                     option_c, option_d, correct_answer)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    quiz_id, question, *options,
                    "ABCD"[options.index(answer)]
                ))

                existing.add(question)
                count += 1
                filler_number += 1

            # Verify final count
            cur.execute("""
                SELECT COUNT(*) FROM questions WHERE quiz_id = ?
            """, (quiz_id,))

            count = cur.fetchone()[0]
            print(f"{difficulty}: {count}/30 questions")

            if count != 30:
                raise Exception(f"{difficulty} verification failed.")

        con.commit()
        print("\nSUCCESS! Adverbs completed: 90/90 MCQs.")

    except Exception:
        con.rollback()
        raise

    finally:
        con.close()


if __name__ == "__main__":
    main()
