
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("What does 'Actions speak louder than words' mean?", "What people do matters more than what they say", "Words are always powerful", "Speaking is better than acting", "Actions should be avoided"),
        ("What does 'Honesty is the best policy' mean?", "Being truthful is the best approach", "Lying is sometimes necessary", "Honesty causes problems", "Policies should be written"),
        ("What does 'Practice makes perfect' mean?", "Regular practice improves skill", "Nobody can become perfect", "Practice is unnecessary", "Talent is more important than effort"),
        ("What does 'Where there is a will, there is a way' mean?", "Determination helps overcome difficulties", "Success comes without effort", "Every road leads somewhere", "People should avoid challenges"),
        ("What does 'A friend in need is a friend indeed' mean?", "A true friend helps during difficult times", "Friends should always agree", "Friends are useful only for fun", "Everyone is a friend"),
        ("What does 'Better late than never' mean?", "Doing something late is better than not doing it", "Being late is always acceptable", "Never try anything", "Early action is harmful"),
        ("What does 'Look before you leap' mean?", "Think carefully before acting", "Jump before thinking", "Avoid making decisions", "Always take risks"),
        ("What does 'Time is money' mean?", "Time is valuable and should not be wasted", "Money can buy more time", "Time and money are identical", "Working slowly saves money"),
        ("What does 'All that glitters is not gold' mean?", "Appearances can be deceptive", "Gold always shines", "Everything beautiful is valuable", "Expensive things are always genuine"),
        ("What does 'No pain, no gain' mean?", "Success requires effort and hard work", "Pain always brings failure", "Success comes easily", "Avoid difficult tasks"),
        ("What does 'Health is wealth' mean?", "Good health is extremely valuable", "Money guarantees good health", "Wealth is more important than health", "Healthy people need no money"),
        ("What does 'Knowledge is power' mean?", "Knowledge gives people strength and ability", "Power comes only from money", "Knowledge should be hidden", "Power makes learning unnecessary"),
        ("What does 'Too many cooks spoil the broth' mean?", "Too many people involved can spoil a task", "Cooking requires many people", "More cooks always improve food", "Food should be prepared quickly"),
        ("What does 'The early bird catches the worm' mean?", "People who act early often get opportunities", "Birds should wake up early", "Worms are easy to catch", "Late workers always succeed"),
        ("What does 'Every cloud has a silver lining' mean?", "There is something positive in every difficult situation", "Clouds are always beautiful", "Bad situations never improve", "Rain always brings happiness"),
        ("What does 'Rome was not built in a day' mean?", "Great achievements take time", "Rome was built quickly", "Cities cannot be built today", "Success depends only on luck"),
        ("What does 'Two heads are better than one' mean?", "Working together can produce better ideas", "Two people always disagree", "One person cannot think", "Group work is unnecessary"),
        ("What does 'Beggars can't be choosers' mean?", "People with limited options cannot be too selective", "Begging is a good profession", "Everyone has many choices", "People should always choose carefully"),
        ("What does 'Don't judge a book by its cover' mean?", "Do not judge something by appearance alone", "Books should have attractive covers", "All books are similar", "Appearance is always important"),
        ("What does 'A stitch in time saves nine' mean?", "Solving a problem early prevents bigger trouble", "Sewing requires nine stitches", "Small problems should be ignored", "Repair work is expensive"),
        ("What does 'When in Rome, do as the Romans do' mean?", "Follow local customs when visiting a place", "Always travel to Rome", "People should ignore traditions", "Everyone must speak Italian"),
        ("What does 'Make hay while the sun shines' mean?", "Use a favourable opportunity while it lasts", "Work only during sunny weather", "Avoid taking opportunities", "Hay should be stored outside"),
        ("What does 'Two wrongs don't make a right' mean?", "One wrong action does not justify another", "Two mistakes create success", "Wrong actions should be repeated", "People should never disagree"),
        ("What does 'Silence is golden' mean?", "Sometimes staying quiet is valuable", "Gold is a silent metal", "Speaking is always harmful", "Silence guarantees success"),
        ("What does 'Necessity is the mother of invention' mean?", "Need encourages people to create solutions", "Inventions are unnecessary", "Only mothers invent things", "Necessity prevents creativity"),
        ("What does 'An apple a day keeps the doctor away' suggest?", "Healthy habits help maintain good health", "Apples replace all medicines", "Doctors dislike apples", "Fruit should be avoided"),
        ("What does 'United we stand, divided we fall' mean?", "Unity makes people stronger", "Division always brings success", "People should work alone", "Unity creates weakness"),
        ("What does 'Half a loaf is better than none' mean?", "Something is better than nothing", "Half a loaf is unhealthy", "Nothing is better than something", "Food should never be shared"),
        ("What does 'Easy come, easy go' mean?", "Things gained easily may be lost easily", "Easy things last forever", "Money never disappears", "Hard work brings no reward"),
        ("What does 'A penny saved is a penny earned' mean?", "Saving money is as valuable as earning it", "Pennies have no value", "Spending money creates wealth", "Saving is always impossible")
    ],

    "Medium": [
        ("What does 'The grass is always greener on the other side' mean?", "Other people's situations often seem better than our own", "Grass grows faster elsewhere", "Everyone has the same opportunities", "Gardens should be maintained"),
        ("What does 'You can't have your cake and eat it too' mean?", "You cannot enjoy two conflicting advantages simultaneously", "Cake should always be eaten", "Food should be shared equally", "Having more cake brings happiness"),
        ("What does 'Don't count your chickens before they hatch' mean?", "Do not assume success before it happens", "Always count farm animals", "Chickens are difficult to raise", "Planning is unnecessary"),
        ("What does 'A rolling stone gathers no moss' traditionally suggest?", "A person who never settles may not accumulate roots or possessions", "Moving stones collect more moss", "Travelling always brings wealth", "People should never change jobs"),
        ("What does 'People who live in glass houses shouldn't throw stones' mean?", "Do not criticise others for faults you also have", "Glass houses are fragile", "People should avoid throwing stones", "Criticism always improves people"),
        ("What does 'The proof of the pudding is in the eating' mean?", "The true value of something is shown by experience", "Pudding should be tasted first", "Food is better than proof", "Cooking requires evidence"),
        ("What does 'Many hands make light work' mean?", "A task becomes easier when people cooperate", "Manual work is always easy", "Many people create confusion", "Work should be avoided"),
        ("What does 'A watched pot never boils' mean?", "Time seems to pass slowly when waiting impatiently", "Pots cannot boil when watched", "Cooking requires patience only", "Water boils immediately"),
        ("What does 'Don't put all your eggs in one basket' advise?", "Avoid depending entirely on one plan or investment", "Keep eggs in several baskets", "Never buy eggs in bulk", "Always carry a basket"),
        ("What does 'One man's trash is another man's treasure' mean?", "Something worthless to one person may be valuable to another", "Trash should always be recycled", "Treasure is easy to find", "Everyone values the same things"),
        ("What does 'Still waters run deep' mean?", "Quiet people may have deep thoughts or feelings", "Deep water is always calm", "Quiet people have no opinions", "Water becomes deeper over time"),
        ("What does 'You reap what you sow' mean?", "Your actions determine the results you receive", "Farming always brings profit", "Seeds grow without care", "People should avoid farming"),
        ("What does 'The pen is mightier than the sword' mean?", "Ideas and writing can be more powerful than violence", "Pens are stronger than weapons", "Writing always causes conflict", "Words have no influence"),
        ("What does 'Barking dogs seldom bite' mean?", "People who make loud threats often do not act on them", "Dogs never bite", "Loud animals are dangerous", "Silence always indicates danger"),
        ("What does 'A leopard cannot change its spots' mean?", "A person's basic nature is difficult to change", "Animals cannot change appearance", "People should avoid change", "Spots disappear with age"),
        ("What does 'Out of sight, out of mind' mean?", "People tend to forget what they no longer see", "Seeing something improves memory", "Distance always creates affection", "People remember everything"),
        ("What does 'The best things in life are free' mean?", "Important joys do not always require money", "Everything valuable costs nothing", "Money has no purpose", "Free things are always better"),
        ("What does 'Don't bite the hand that feeds you' mean?", "Do not harm someone who helps or supports you", "Never eat with your hands", "Always feed animals", "Avoid accepting food"),
        ("What does 'A chain is only as strong as its weakest link' mean?", "The weakest member can limit the strength of the whole group", "Chains are always weak", "Strong links are unnecessary", "Every group needs a leader"),
        ("What does 'Familiarity breeds contempt' mean?", "Knowing someone too well can sometimes reduce respect", "Familiar people are always trustworthy", "Respect grows automatically", "People should avoid meeting others"),
        ("What does 'Too little, too late' mean?", "An action comes too late to make a difference", "A small effort is always enough", "Late arrivals are helpful", "Everything improves with time"),
        ("What does 'Every dog has its day' mean?", "Everyone gets an opportunity or moment of success eventually", "Dogs celebrate daily", "Animals always succeed", "Success comes only to animals"),
        ("What does 'A bad workman blames his tools' mean?", "Incompetent people blame their equipment for their failures", "Tools are always faulty", "Workers should avoid tools", "Good tools guarantee success"),
        ("What does 'Fortune favours the brave' mean?", "Courageous people are more likely to find success", "Luck comes only to wealthy people", "Bravery guarantees safety", "Risk should always be avoided"),
        ("What does 'The road to hell is paved with good intentions' mean?", "Good intentions can still lead to harmful results", "Good intentions always bring success", "Roads are dangerous", "People should avoid helping others"),
        ("What does 'You can't make an omelette without breaking eggs' mean?", "Achieving something may require sacrifice", "Cooking is always difficult", "Eggs should never be broken", "Every sacrifice is unnecessary"),
        ("What does 'A rising tide lifts all boats' mean?", "Improvement in general conditions benefits everyone", "Boats rise during every storm", "Success belongs to one person", "Water levels determine wealth"),
        ("What does 'Discretion is the better part of valour' mean?", "Sometimes avoiding danger is wiser than showing bravery", "Bravery is always foolish", "Discretion means weakness", "Danger should always be faced"),
        ("What does 'He who laughs last laughs longest' mean?", "The final outcome matters more than early success", "Laughter should be delayed", "Early winners always lose", "People should laugh quietly"),
        ("What does 'The exception proves the rule' traditionally mean?", "An explicitly stated exception can indicate that a general rule exists", "Rules never have exceptions", "Every exception is incorrect", "Rules should always be ignored")
    ],

    "Hard": [
        ("What does 'Brevity is the soul of wit' mean?", "Concise expression can make communication more effective", "Long speeches are always intelligent", "Wit requires silence", "Humour should be avoided"),
        ("What does 'Uneasy lies the head that wears a crown' mean?", "People in positions of power often carry heavy responsibilities", "Kings never sleep", "Power always brings happiness", "Leadership requires no effort"),
        ("What does 'The course of true love never did run smooth' mean?", "Genuine love often faces difficulties", "Love always ends badly", "Relationships should be avoided", "Love is always simple"),
        ("What does 'Hell hath no fury like a woman scorned' traditionally suggest?", "A deeply wronged person may react with intense anger", "Anger always solves problems", "Women never forgive", "Fury is a sign of happiness"),
        ("What does 'Beggars mounted on horseback ride faster to their ruin' suggest?", "Sudden prosperity can lead the unprepared into greater trouble", "Horse riding guarantees success", "Poor people should avoid horses", "Wealth always brings wisdom"),
        ("What does 'The child is father of the man' mean?", "Childhood experiences help shape the adult a person becomes", "Children are older than adults", "Parents learn everything from children", "Age has no influence on character"),
        ("What does 'The darkest hour is just before the dawn' mean?", "Things may improve after their most difficult point", "Night always lasts longer", "Dawn brings more darkness", "Difficulties never end"),
        ("What does 'A little knowledge is a dangerous thing' mean?", "Limited knowledge can create false confidence and mistakes", "Knowledge should be avoided", "Experts always make mistakes", "Learning little is better than learning much"),
        ("What does 'Fools rush in where angels fear to tread' mean?", "Inexperienced people may act recklessly where wiser people hesitate", "Angels are always afraid", "Courage is unnecessary", "Fools never take action"),
        ("What does 'The road to success is always under construction' suggest?", "Success requires continuous effort and improvement", "Success is impossible", "Roads determine achievement", "People should avoid change"),
        ("What does 'A soft answer turns away wrath' mean?", "A calm response can reduce anger", "Silence always creates anger", "Arguments should be encouraged", "Harsh words solve conflicts"),
        ("What does 'To whom much is given, much will be required' mean?", "People with greater advantages have greater responsibilities", "Wealth removes responsibility", "People should avoid receiving gifts", "Giving always leads to loss"),
        ("What does 'The more things change, the more they stay the same' mean?", "Despite changes, fundamental situations often remain unchanged", "Nothing ever changes", "Change always creates progress", "Traditions disappear immediately"),
        ("What does 'No man is an island' mean?", "People depend on one another and are part of society", "Everyone should live alone", "Islands are overcrowded", "Independence is impossible"),
        ("What does 'A house divided against itself cannot stand' mean?", "Internal conflict can destroy a group or organisation", "Houses need strong foundations", "Families should never disagree", "Division always creates strength"),
        ("What does 'The mills of God grind slowly, yet they grind exceedingly small' mean?", "Justice or consequences may be delayed but are eventually thorough", "Justice always happens immediately", "Time destroys every problem", "Slow work is always ineffective"),
        ("What does 'He who pays the piper calls the tune' mean?", "The person who provides the money often controls the decisions", "Musicians control every event", "Money has no influence", "Everyone has equal authority"),
        ("What does 'There is many a slip between the cup and the lip' mean?", "Unexpected problems can prevent success even at the last moment", "Drinking requires care", "Success is always guaranteed", "Small mistakes are unimportant"),
        ("What does 'One swallow does not make a summer' mean?", "One positive sign does not prove that a situation has changed completely", "Birds predict the weather accurately", "Summer begins with one bird", "A single event explains everything"),
        ("What does 'The cobbler should stick to his last' mean?", "People should focus on the work they know best", "Shoemakers should avoid customers", "People should change professions often", "Expertise is unnecessary"),
        ("What does 'A fool and his money are soon parted' mean?", "Unwise people quickly lose their money", "Money always makes people foolish", "Saving money is impossible", "Wealth guarantees intelligence"),
        ("What does 'The leopard does not change its spots' emphasise?", "Fundamental character traits are difficult to alter", "Appearance determines character", "Animals cannot adapt", "People never learn new skills"),
        ("What does 'The best-laid schemes of mice and men often go awry' mean?", "Even carefully planned efforts can fail unexpectedly", "Planning guarantees success", "Animals are better planners", "Failure is always intentional"),
        ("What does 'There is honour among thieves' mean?", "Even dishonest people may follow a code of loyalty among themselves", "Thieves are always honest", "Honour belongs only to criminals", "Crime creates respect"),
        ("What does 'A rising tide lifts all boats' imply in economics?", "Broad economic improvement can benefit many people", "Only wealthy people benefit from growth", "Rising prices help everyone equally", "Economic growth affects no one"),
        ("What does 'The squeaky wheel gets the grease' mean?", "People who complain or speak up are more likely to receive attention", "Machines should always be repaired", "Quiet people always get rewards", "Complaints should be ignored"),
        ("What does 'Don't throw the baby out with the bathwater' mean?", "Do not discard something valuable while removing what is unwanted", "Babies should never be bathed", "Old things are always valuable", "Cleaning should be avoided"),
        ("What does 'A drowning man will clutch at a straw' mean?", "A desperate person will try even an unlikely solution", "People should avoid water", "Straws are useful for swimming", "Desperate people never seek help"),
        ("What does 'The end justifies the means' mean?", "An outcome is considered to justify the methods used to achieve it", "Methods are more important than results", "Every action is justified", "Ends and means are unrelated"),
        ("What does 'There are none so blind as those who will not see' mean?", "People who refuse to accept the truth are more ignorant than those who cannot see", "Blind people cannot learn", "Everyone sees the same truth", "Knowledge depends only on eyesight")
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
            ("Proverbs", "English")
        )
        row = cur.fetchone()

        if not row:
            raise Exception(
                "Lesson 'Proverbs' with topic 'English' was not found."
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
                    (lesson_id, f"Proverbs - {difficulty}", difficulty)
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
        print("\nSUCCESS: Proverbs has exactly 90 questions!")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
