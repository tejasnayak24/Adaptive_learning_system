
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("What does 'a piece of cake' mean?", "Very easy", "Very expensive", "Very difficult", "Very interesting"),
        ("What does 'once in a blue moon' mean?", "Very rarely", "Every day", "Very quickly", "At night"),
        ("What does 'break the ice' mean?", "Start a friendly conversation", "Break something", "End a friendship", "Create an argument"),
        ("What does 'hit the books' mean?", "Study seriously", "Throw books", "Buy books", "Read casually"),
        ("What does 'under the weather' mean?", "Feeling ill", "Feeling excited", "Feeling wealthy", "Feeling hungry"),
        ("What does 'spill the beans' mean?", "Reveal a secret", "Cook a meal", "Waste food", "Make a mistake"),
        ("What does 'cost an arm and a leg' mean?", "Be very expensive", "Be very cheap", "Cause an injury", "Be free"),
        ("What does 'in hot water' mean?", "In trouble", "Taking a bath", "Feeling warm", "Enjoying a holiday"),
        ("What does 'keep an eye on' mean?", "Watch carefully", "Ignore completely", "Close your eyes", "Look away"),
        ("What does 'call it a day' mean?", "Stop working for the day", "Start a new job", "Make a phone call", "Celebrate an event"),
        ("What does 'on cloud nine' mean?", "Extremely happy", "Very angry", "Extremely tired", "Very confused"),
        ("What does 'a blessing in disguise' mean?", "Something good that seemed bad at first", "An obvious disaster", "A false promise", "A hidden enemy"),
        ("What does 'get cold feet' mean?", "Become nervous", "Feel physically cold", "Become angry", "Feel sleepy"),
        ("What does 'the ball is in your court' mean?", "It is your turn to act", "You have lost a game", "You should play football", "Someone has blamed you"),
        ("What does 'add fuel to the fire' mean?", "Make a bad situation worse", "Solve a problem", "Calm someone down", "Start cooking"),
        ("What does 'a bed of roses' mean?", "An easy and comfortable situation", "A difficult journey", "A garden full of flowers", "A lonely experience"),
        ("What does 'beat around the bush' mean?", "Avoid talking directly", "Speak honestly", "Work in a garden", "Finish quickly"),
        ("What does 'better late than never' mean?", "Doing something late is better than not doing it", "Being late is always good", "Never complete a task", "Always arrive early"),
        ("What does 'by heart' mean?", "From memory", "With affection", "With difficulty", "Without interest"),
        ("What does 'cry over spilt milk' mean?", "Regret something that cannot be changed", "Complain about food", "Feel happy about the past", "Waste drinking water"),
        ("What does 'every cloud has a silver lining' mean?", "Something good can come from a bad situation", "Clouds always bring rain", "Life is always difficult", "Good things never happen"),
        ("What does 'make up your mind' mean?", "Make a decision", "Change your appearance", "Forget a problem", "Ask for advice"),
        ("What does 'out of the blue' mean?", "Unexpectedly", "Very slowly", "In a planned way", "Without permission"),
        ("What does 'pull someone's leg' mean?", "Tease or joke with someone", "Physically hurt someone", "Help someone walk", "Argue seriously"),
        ("What does 'see eye to eye' mean?", "Agree with someone", "Look at someone", "Dislike someone", "Avoid meeting someone"),
        ("What does 'through thick and thin' mean?", "In good and bad times", "Through a narrow road", "Without any difficulty", "For a short time"),
        ("What does 'time flies' mean?", "Time passes quickly", "Time stops suddenly", "Time moves backwards", "Time is wasted deliberately"),
        ("What does 'when pigs fly' mean?", "Something that will never happen", "Something that happens daily", "Something very easy", "Something that happens soon"),
        ("What does 'a storm in a teacup' mean?", "A big fuss over a small matter", "A serious natural disaster", "A peaceful situation", "A difficult examination"),
        ("What does 'burn the midnight oil' mean?", "Work or study late at night", "Waste electricity", "Go to sleep early", "Light a candle")
    ],

    "Medium": [
        ("What does 'bite the bullet' mean?", "Face a difficult situation bravely", "Avoid responsibility", "Make a careless decision", "Start an argument"),
        ("What does 'hit the nail on the head' mean?", "Say exactly the right thing", "Make a serious mistake", "Work as a carpenter", "Avoid answering"),
        ("What does 'let the cat out of the bag' mean?", "Reveal a secret accidentally", "Release a pet", "Hide important information", "Create confusion"),
        ("What does 'jump on the bandwagon' mean?", "Join a popular trend", "Start a new business", "Avoid public attention", "Reject an opportunity"),
        ("What does 'kill two birds with one stone' mean?", "Achieve two things with one action", "Harm two people", "Waste time on two tasks", "Solve only one problem"),
        ("What does 'leave no stone unturned' mean?", "Make every possible effort", "Ignore important details", "Avoid difficult work", "Search only one place"),
        ("What does 'miss the boat' mean?", "Lose an opportunity", "Miss a bus or train", "Arrive early", "Avoid travelling"),
        ("What does 'put all your eggs in one basket' mean?", "Risk everything on one plan", "Prepare several options", "Avoid taking risks", "Share resources equally"),
        ("What does 'throw in the towel' mean?", "Give up", "Start a competition", "Clean a room", "Celebrate success"),
        ("What does 'turn a blind eye' mean?", "Pretend not to notice", "Look carefully", "Help someone see", "Observe closely"),
        ("What does 'back to square one' mean?", "Return to the beginning", "Complete a difficult task", "Move to another location", "Win a competition"),
        ("What does 'barking up the wrong tree' mean?", "Following a mistaken idea", "Making a loud noise", "Choosing the correct path", "Working very hard"),
        ("What does 'cut corners' mean?", "Do something cheaply or carelessly", "Make a neat design", "Take a longer route", "Complete every detail"),
        ("What does 'get out of hand' mean?", "Become uncontrollable", "Become very expensive", "Be completed successfully", "Become less important"),
        ("What does 'go the extra mile' mean?", "Make more effort than expected", "Travel a long distance", "Avoid extra work", "Take a holiday"),
        ("What does 'keep your fingers crossed' mean?", "Hope for good luck", "Show anger", "Make a promise", "Refuse to participate"),
        ("What does 'make ends meet' mean?", "Manage expenses with available income", "Complete a difficult project", "Connect two objects", "Earn excessive money"),
        ("What does 'no pain, no gain' mean?", "Success requires effort", "Pain should always be avoided", "Success comes without work", "Hard work is unnecessary"),
        ("What does 'on the same page' mean?", "Having the same understanding", "Reading the same book", "Working in different teams", "Disagreeing about an issue"),
        ("What does 'play it by ear' mean?", "Decide what to do as events develop", "Play music without practice", "Follow strict instructions", "Repeat a memorised speech"),
        ("What does 'put your foot down' mean?", "Act firmly and refuse to give in", "Walk slowly", "Apologise sincerely", "Avoid making decisions"),
        ("What does 'read between the lines' mean?", "Understand an implied meaning", "Read a book quickly", "Skip important sentences", "Read aloud"),
        ("What does 'the last straw' mean?", "The final problem that makes a situation unbearable", "A small piece of hay", "The beginning of a problem", "An unexpected reward"),
        ("What does 'throw caution to the wind' mean?", "Take a risk without worrying about danger", "Avoid all risks", "Plan very carefully", "Refuse an adventure"),
        ("What does 'up in the air' mean?", "Not yet decided or settled", "Flying in the sky", "Completely finished", "Clearly understood"),
        ("What does 'wrap your head around' mean?", "Understand something difficult", "Cover your head", "Forget information", "Avoid thinking"),
        ("What does 'your guess is as good as mine' mean?", "I do not know either", "I know the exact answer", "Your guess is incorrect", "I disagree with you"),
        ("What does 'face the music' mean?", "Accept the consequences of your actions", "Attend a concert", "Listen carefully to music", "Celebrate an achievement"),
        ("What does 'go down in flames' mean?", "Fail spectacularly", "Become very successful", "Disappear quietly", "Change direction"),
        ("What does 'keep something at bay' mean?", "Prevent something from approaching or causing harm", "Keep something nearby", "Invite someone closer", "Ignore a warning")
    ],

    "Hard": [
        ("What does 'a Pyrrhic victory' mean?", "A victory achieved at a devastating cost", "An easy and complete victory", "A victory without competition", "A victory gained through luck"),
        ("What does 'Achilles' heel' mean?", "A person's main weakness", "A person's greatest strength", "A hidden advantage", "An unexpected achievement"),
        ("What does 'an albatross around one's neck' mean?", "A burdensome problem or responsibility", "A valuable possession", "A symbol of freedom", "An unexpected opportunity"),
        ("What does 'cross the Rubicon' mean?", "Take an irreversible step", "Avoid making a decision", "Return to an earlier situation", "Change one's opinion frequently"),
        ("What does 'the sword of Damocles' mean?", "An ever-present threat or danger", "A symbol of great success", "A reward for bravery", "A difficult choice"),
        ("What does 'Pandora's box' mean?", "An action that creates many unexpected problems", "A source of unlimited wealth", "A secret that brings happiness", "A solution to every problem"),
        ("What does 'a Gordian knot' mean?", "An extremely complicated problem", "A simple task", "A valuable discovery", "A peaceful agreement"),
        ("What does 'between Scylla and Charybdis' mean?", "Caught between two equally dangerous choices", "Enjoying two good opportunities", "Choosing between easy tasks", "Avoiding all difficulties"),
        ("What does 'a Sisyphean task' mean?", "A task requiring endless and futile effort", "A task completed very easily", "A task requiring teamwork", "A task with immediate rewards"),
        ("What does 'the writing on the wall' mean?", "A clear sign of impending trouble", "A secret message of success", "A written agreement", "An unexpected opportunity"),
        ("What does 'to throw down the gauntlet' mean?", "Issue a challenge", "Accept defeat", "Avoid a confrontation", "Offer an apology"),
        ("What does 'to take the bull by the horns' mean?", "Deal with a difficult situation directly", "Avoid a dangerous situation", "Create unnecessary trouble", "Wait for someone else's help"),
        ("What does 'to steal someone's thunder' mean?", "Take credit or attention away from someone", "Make a loud announcement", "Copy someone's work secretly", "Surprise an audience"),
        ("What does 'to move the goalposts' mean?", "Unfairly change the rules or conditions", "Achieve a difficult target", "Set a realistic objective", "Avoid a competition"),
        ("What does 'to have an axe to grind' mean?", "Have a personal motive or grievance", "Perform a difficult job", "Prepare for a competition", "Resolve a disagreement"),
        ("What does 'to throw good money after bad' mean?", "Continue investing in something that is already failing", "Save money carefully", "Spend money on useful things", "Earn money through hard work"),
        ("What does 'to cut the Gordian knot' mean?", "Solve a complicated problem decisively", "Make a problem more difficult", "Avoid making a decision", "Create unnecessary rules"),
        ("What does 'to burn one's bridges' mean?", "Destroy the possibility of returning to an earlier situation", "Build strong relationships", "Prepare for future success", "Avoid taking responsibility"),
        ("What does 'to put the cart before the horse' mean?", "Do things in the wrong order", "Complete tasks efficiently", "Plan everything carefully", "Work without assistance"),
        ("What does 'to take something with a grain of salt' mean?", "Treat information with some scepticism", "Believe everything immediately", "Reject all advice", "Accept something enthusiastically"),
        ("What does 'to keep a stiff upper lip' mean?", "Remain calm and show courage during difficulty", "Refuse to speak to anyone", "Express emotions openly", "Avoid difficult situations"),
        ("What does 'to throw someone under the bus' mean?", "Betray someone to protect oneself", "Help someone in trouble", "Invite someone to travel", "Take responsibility for another person"),
        ("What does 'to make a mountain out of a molehill' mean?", "Exaggerate a small problem", "Solve a major problem", "Ignore a serious issue", "Make a difficult task easier"),
        ("What does 'to have one's back against the wall' mean?", "Be in a difficult situation with few options", "Have complete control", "Enjoy a comfortable position", "Avoid all responsibility"),
        ("What does 'to open a can of worms' mean?", "Create a complicated set of problems", "Find an easy solution", "Reveal a pleasant surprise", "Finish an unfinished task"),
        ("What does 'to be on tenterhooks' mean?", "Be in a state of anxious suspense", "Feel completely relaxed", "Be extremely confident", "Become very angry"),
        ("What does 'to take umbrage' mean?", "Feel offended or resentful", "Accept criticism happily", "Offer an apology", "Show gratitude"),
        ("What does 'to be in the doldrums' mean?", "Be in a state of low spirits or inactivity", "Experience great excitement", "Be extremely successful", "Feel completely confident"),
        ("What does 'to pay lip service' mean?", "Express support without sincere action", "Offer practical assistance", "Speak with great honesty", "Refuse to communicate"),
        ("What does 'to leave someone in the lurch' mean?", "Abandon someone in a difficult situation", "Help someone overcome difficulty", "Give someone an opportunity", "Protect someone from danger")
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
    try:
        validate_bank()
        print("Question bank validation successful.")

        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()

        try:
            cur.execute(
                "SELECT id FROM lessons WHERE title=? AND topic=?",
                ("Idioms and Phrases", "English")
            )
            row = cur.fetchone()

            if not row:
                raise Exception(
                    "Lesson 'Idioms and Phrases' with topic "
                    "'English' was not found."
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
                            f"Idioms and Phrases - {difficulty}",
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
            print(
                "\nSUCCESS: Idioms and Phrases has exactly 90 questions!"
            )

        except Exception as e:
            con.rollback()
            print("ERROR:", e)

        finally:
            con.close()

    except Exception as e:
        print("VALIDATION ERROR:", e)


if __name__ == "__main__":
    main()
