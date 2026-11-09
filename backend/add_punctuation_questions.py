
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("Which punctuation mark is used to end a statement?", ".", "?", "!", ","),
        ("Which punctuation mark is used at the end of a direct question?", "?", ".", ",", ":"),
        ("Which punctuation mark expresses strong emotion?", "!", ".", ";", ":"),
        ("Which punctuation mark separates items in a list?", ",", "?", "!", "'"),
        ("Which punctuation mark shows possession?", "Apostrophe", "Comma", "Colon", "Question mark"),
        ("Which punctuation mark introduces a list?", "Colon", "Full stop", "Question mark", "Apostrophe"),
        ("Which punctuation mark can join two closely related independent clauses?", "Semicolon", "Apostrophe", "Question mark", "Hyphen"),
        ("Which punctuation marks enclose the exact words spoken by someone?", "Quotation marks", "Brackets", "Commas", "Hyphens"),
        ("Choose the correctly punctuated sentence.", "I like apples, oranges, and grapes.", "I like apples oranges and grapes.", "I like apples; oranges; and grapes.", "I like apples: oranges: and grapes."),
        ("Choose the correct punctuation: 'Where are you going___'", "?", ".", "!", ","),
        ("Choose the correct punctuation: 'What a wonderful day___'", "!", "?", ",", ";"),
        ("Which sentence uses an apostrophe correctly?", "This is Riya's book.", "This is Riyas book.", "This is Riya,s book.", "This is Riya;s book."),
        ("Which sentence uses a comma correctly?", "After lunch, we went shopping.", "After lunch we, went shopping.", "After, lunch we went shopping.", "After lunch; we, went shopping."),
        ("Which punctuation mark is used to show omitted letters in contractions?", "Apostrophe", "Colon", "Semicolon", "Full stop"),
        ("Which is the correct contraction of 'do not'?", "Don't", "Dont", "Do'nt", "Don,t"),
        ("Which punctuation mark is used at the end of an abbreviation such as 'Dr.'?", "Full stop", "Question mark", "Colon", "Hyphen"),
        ("Choose the correctly punctuated sentence.", "She said, \"I am happy.\"", "She said \"I am happy\".", "She said; \"I am happy\"?", "She said: I am happy."),
        ("Which punctuation mark separates a question from its answer in a written dialogue?", "Question mark", "Hyphen", "Apostrophe", "Colon"),
        ("Which punctuation mark is used to separate a city from a state in an address?", "Comma", "Apostrophe", "Exclamation mark", "Question mark"),
        ("Choose the correctly punctuated sentence.", "My brother, who lives in Delhi, is a doctor.", "My brother who lives in Delhi is, a doctor.", "My brother; who lives in Delhi is a doctor.", "My brother: who lives in Delhi, is a doctor."),
        ("Which punctuation mark is used to indicate a pause within a sentence?", "Comma", "Full stop", "Question mark", "Exclamation mark"),
        ("Choose the correct punctuation: 'I bought pens, pencils___ and books.'", "and", "?", "!", ";"),
        ("Which sentence uses an exclamation mark correctly?", "Watch out!", "Watch out?", "Watch out,", "Watch out;"),
        ("Which punctuation mark is commonly used to connect compound words?", "Hyphen", "Apostrophe", "Colon", "Full stop"),
        ("Choose the correctly punctuated sentence.", "The teacher said, \"Open your books.\"", "The teacher said \"Open your books\".", "The teacher said; \"Open your books.\"", "The teacher said, Open your books."),
        ("Which punctuation mark is used to enclose additional information?", "Brackets", "Question mark", "Apostrophe", "Full stop"),
        ("Choose the correct sentence.", "It's raining outside.", "Its' raining outside.", "Its raining outside.", "It,s raining outside."),
        ("Which punctuation mark is used to indicate the end of a sentence?", "Full stop", "Comma", "Hyphen", "Apostrophe"),
        ("Which sentence uses a comma in direct address correctly?", "Ravi, please come here.", "Ravi please, come here.", "Ravi please come, here.", "Ravi; please come here."),
        ("Which punctuation mark is used after a greeting in a formal letter?", "Comma", "Question mark", "Exclamation mark", "Hyphen")
    ],

    "Medium": [
        ("Choose the correctly punctuated sentence.", "Let's eat, Grandma!", "Let's eat Grandma!", "Lets eat, Grandma!", "Lets eat Grandma."),
        ("Which sentence uses a semicolon correctly?", "I was tired; I went to bed early.", "I was tired,; I went to bed early.", "I was tired: I went to bed early.", "I was tired? I went to bed early."),
        ("Choose the correct punctuation: 'The following items are required___ a pen, a notebook, and a ruler.'", ":", ";", "?", "'"),
        ("Which sentence uses an apostrophe correctly for plural possession?", "The girls' classroom is spacious.", "The girl's classroom is spacious.", "The girls classroom's is spacious.", "The girls's classroom is spacious."),
        ("Choose the correct sentence.", "The dog's tail is wagging.", "The dogs tail is wagging.", "The dogs' tail is wagging.", "The dog's' tail is wagging."),
        ("Which sentence correctly uses a comma after an introductory clause?", "When the rain stopped, we went outside.", "When the rain stopped we, went outside.", "When, the rain stopped we went outside.", "When the rain, stopped we went outside."),
        ("Which sentence uses a colon correctly?", "She had one goal: to succeed.", "She had: one goal to succeed.", "She had one: goal to succeed.", "She: had one goal to succeed."),
        ("Choose the correctly punctuated direct speech.", "Maya said, \"I will call you tomorrow.\"", "Maya said \"I will call you tomorrow\".", "Maya said; \"I will call you tomorrow.\"", "Maya said, I will call you tomorrow."),
        ("Which sentence uses commas correctly with a non-essential clause?", "My car, which is red, is parked outside.", "My car which is red, is parked outside.", "My car, which is red is parked outside.", "My car; which is red; is parked outside."),
        ("Choose the correct punctuation for a list containing commas within its items.", "We visited Mysuru, Karnataka; Kochi, Kerala; and Pune, Maharashtra.", "We visited Mysuru, Karnataka, Kochi, Kerala, and Pune, Maharashtra.", "We visited Mysuru: Karnataka; Kochi: Kerala; and Pune: Maharashtra.", "We visited Mysuru? Karnataka; Kochi? Kerala; and Pune? Maharashtra."),
        ("Which sentence correctly uses a hyphen?", "She is a well-known author.", "She is a well known-author.", "She is a wellknown author.", "She is a well-known-author."),
        ("Choose the correct punctuation: 'My sister___ a talented singer___ performed tonight.'", "— —", ", ,", ": :", "? ?"),
        ("Which sentence correctly uses a dash to indicate an interruption?", "I was going to explain—but never mind.", "I was going to explain, but—never mind.", "I was going to explain?—never mind.", "I was going to explain;—never mind."),
        ("Which sentence correctly punctuates a question tag?", "You are coming, aren't you?", "You are coming aren't you.", "You are coming; aren't you.", "You are coming: aren't you?"),
        ("Choose the correctly punctuated sentence.", "However, we decided to continue.", "However we, decided to continue.", "However; we decided, to continue.", "However: we decided to continue."),
        ("Which sentence uses an apostrophe correctly in a contraction?", "She's finished her work.", "Shes' finished her work.", "Shes finished her work.", "She,s finished her work."),
        ("Which sentence correctly uses quotation marks for a quoted question?", "He asked, \"Are you ready?\"", "He asked, \"Are you ready\"?", "He asked \"Are you ready?\".", "He asked; \"Are you ready?\""),
        ("Which sentence correctly uses parentheses?", "The meeting (originally scheduled for Monday) was postponed.", "The meeting originally (scheduled for Monday was postponed.", "The meeting (originally scheduled for Monday was postponed.", "The meeting originally scheduled for Monday) was postponed."),
        ("Choose the correctly punctuated sentence.", "No, I have not finished the assignment.", "No I, have not finished the assignment.", "No; I have not finished, the assignment.", "No: I have not finished the assignment?"),
        ("Which sentence uses a comma to separate coordinate adjectives correctly?", "It was a long, difficult journey.", "It was a long difficult, journey.", "It was a, long difficult journey.", "It was a long; difficult journey."),
        ("Which punctuation mark is appropriate between two independent clauses joined without a conjunction?", "Semicolon", "Apostrophe", "Hyphen", "Question mark"),
        ("Choose the correct punctuation: 'She asked___ \"Have you completed the task___\"'", "comma, question mark", "colon, full stop", "semicolon, comma", "full stop, exclamation mark"),
        ("Which sentence correctly uses a comma with a direct quotation?", "He replied, \"I agree with you.\"", "He replied \"I agree with you,\".", "He replied; \"I agree with you.\"", "He replied: \"I agree with you\"?"),
        ("Which sentence correctly uses an apostrophe for joint possession?", "Ravi and Priya's house is beautiful.", "Ravi's and Priya house is beautiful.", "Ravi and Priya house's is beautiful.", "Ravi's and Priya's house are beautiful."),
        ("Choose the correct sentence.", "The principal's office is on the first floor.", "The principals office is on the first floor.", "The principals' office is on the first floor.", "The principal office's is on the first floor."),
        ("Which sentence uses a colon to introduce an explanation?", "There was one problem: nobody had the key.", "There was: one problem nobody had the key.", "There was one: problem nobody had the key.", "There was one problem; nobody: had the key."),
        ("Choose the correctly punctuated sentence.", "If you need help, please contact me.", "If you need help please, contact me.", "If, you need help please contact me.", "If you need, help please contact me."),
        ("Which sentence correctly uses an ellipsis to show an unfinished thought?", "I thought I had everything, but...", "I thought I had everything but....", "I thought I had everything, but????", "I thought I had everything; but:"),
        ("Which sentence correctly uses a comma before a coordinating conjunction joining two independent clauses?", "I wanted to travel, but I had no time.", "I wanted to travel but, I had no time.", "I wanted, to travel but I had no time.", "I wanted to travel; but I had no time."),
        ("Which sentence correctly uses punctuation with an introductory phrase?", "After a long discussion, the team reached a decision.", "After a long discussion the team, reached a decision.", "After, a long discussion the team reached a decision.", "After a long discussion; the team reached a decision.")
    ],

    "Hard": [
        ("Which sentence correctly uses a semicolon with a conjunctive adverb?", "The road was blocked; therefore, we took another route.", "The road was blocked, therefore; we took another route.", "The road was blocked: therefore we took another route.", "The road was blocked; therefore we took another route."),
        ("Choose the correctly punctuated sentence.", "The results were impressive; however, further testing is required.", "The results were impressive, however; further testing is required.", "The results were impressive: however further testing is required.", "The results were impressive; however further testing is required."),
        ("Which sentence correctly uses commas to set off an interrupter?", "The plan, in my opinion, is practical.", "The plan in, my opinion is practical.", "The plan; in my opinion; is practical.", "The plan: in my opinion is practical."),
        ("Which sentence correctly uses an apostrophe for separate possession?", "Riya's and Meera's bags were on the table.", "Riya and Meera's bags were on the table.", "Riyas' and Meera bags were on the table.", "Riya's and Meera bags' were on the table."),
        ("Which sentence correctly distinguishes between 'its' and 'it's'?", "The company changed its policy because it's necessary.", "The company changed it's policy because its necessary.", "The company changed its' policy because it's necessary.", "The company changed it's policy because its' necessary."),
        ("Which sentence correctly uses a colon after a complete independent clause?", "Bring these items: a notebook, a pen, and a ruler.", "Bring: these items a notebook, a pen, and a ruler.", "Bring these items; a notebook, a pen, and a ruler.", "Bring these items, a notebook: a pen, and a ruler."),
        ("Which sentence correctly punctuates a quotation interrupted by a speaker tag?", "\"I am,\" she said, \"ready to begin.\"", "\"I am,\" she said \"ready to begin.\"", "\"I am\" she said, \"ready to begin.\"", "\"I am;\" she said, \"ready to begin.\""),
        ("Which sentence correctly uses a dash to emphasize additional information?", "There was only one solution—start again.", "There was only one solution, start again.", "There was only one solution;—start again.", "There was only one solution:—start again."),
        ("Which sentence correctly uses commas around a non-restrictive relative clause?", "The Taj Mahal, which is in Agra, attracts millions of visitors.", "The Taj Mahal which is in Agra, attracts millions of visitors.", "The Taj Mahal, which is in Agra attracts millions of visitors.", "The Taj Mahal; which is in Agra; attracts millions of visitors."),
        ("Which sentence correctly punctuates a compound-complex sentence?", "Although it was late, we continued working, and the manager stayed.", "Although it was late; we continued working and the manager stayed.", "Although, it was late we continued working, and the manager stayed.", "Although it was late, we continued working; and the manager stayed."),
        ("Which sentence correctly uses a semicolon between items in a complex list?", "The speakers came from Delhi, India; Tokyo, Japan; and Paris, France.", "The speakers came from Delhi; India, Tokyo; Japan, and Paris; France.", "The speakers came from Delhi, India, Tokyo, Japan, and Paris, France.", "The speakers came from Delhi: India; Tokyo: Japan; and Paris: France."),
        ("Which sentence correctly punctuates a sentence containing a parenthetical expression?", "The answer, as you might expect, was incorrect.", "The answer as, you might expect was incorrect.", "The answer; as you might expect; was incorrect.", "The answer: as you might expect, was incorrect."),
        ("Which sentence correctly uses quotation marks and punctuation for a quoted statement?", "She said, \"The meeting starts at nine.\"", "She said \"The meeting starts at nine.\".", "She said; \"The meeting starts at nine.\"", "She said, \"The meeting starts at nine\"."),
        ("Which sentence correctly uses a hyphen in a compound modifier before a noun?", "It was a well-written report.", "It was a well written-report.", "It was a wellwritten report.", "It was a well-written-report."),
        ("Which sentence correctly avoids an unnecessary hyphen?", "The report was well written.", "The report was well-written.", "The report was well-written report.", "The report was wellwritten."),
        ("Which sentence correctly uses an apostrophe in a plural noun ending in 's' to show possession?", "The students' projects were displayed.", "The student's projects were displayed.", "The students projects' were displayed.", "The students's projects were displayed."),
        ("Which sentence correctly uses a comma after a long introductory dependent clause?", "Although the instructions were complicated, everyone understood them.", "Although the instructions were complicated everyone, understood them.", "Although, the instructions were complicated everyone understood them.", "Although the instructions, were complicated everyone understood them."),
        ("Which sentence correctly uses a colon to introduce a quotation?", "The coach gave one instruction: \"Never give up.\"", "The coach gave: one instruction \"Never give up.\"", "The coach gave one instruction; \"Never give up.\"", "The coach gave one instruction, \"Never give up.\""),
        ("Which sentence correctly uses an ellipsis to indicate omitted words in a quotation?", "The report states, \"The results ... were significant.\"", "The report states, \"The results, ... were significant.\"", "The report states; \"The results ... were significant.\"", "The report states: \"The results ... were significant\"?"),
        ("Which sentence correctly uses a question mark with an indirect question?", "She asked whether I was ready.", "She asked whether I was ready?", "She asked, whether I was ready?", "She asked; whether I was ready."),
        ("Which sentence correctly uses a question mark with a direct question?", "She asked, \"Are you ready?\"", "She asked, \"Are you ready.\"?", "She asked whether, \"Are you ready?\"", "She asked; \"Are you ready.\""),
        ("Which sentence correctly uses commas to separate an introductory participial phrase?", "Having completed the assignment, she submitted it.", "Having completed, the assignment she submitted it.", "Having, completed the assignment she submitted it.", "Having completed the assignment; she submitted it."),
        ("Which sentence correctly punctuates a series with a final coordinating conjunction?", "We need paper, ink, and envelopes.", "We need paper ink and, envelopes.", "We need paper; ink; and envelopes.", "We need paper: ink: and envelopes."),
        ("Which sentence correctly uses a comma to prevent ambiguity?", "Let's eat, children.", "Let's eat children.", "Let's, eat children.", "Let's eat; children."),
        ("Which sentence correctly uses a dash to indicate a sudden change in thought?", "I was certain I had won—or so I thought.", "I was certain I had won, or—so I thought.", "I was certain; I had won—or so I thought.", "I was certain: I had won—or so I thought."),
        ("Which sentence correctly uses brackets to add editorial clarification inside a quotation?", "He said, \"They [the students] arrived early.\"", "He said, \"They (the students arrived early.\"", "He said, \"They [the students arrived early.\"", "He said, \"They the students] arrived early.\""),
        ("Which sentence correctly uses a comma with a contrastive introductory phrase?", "On the other hand, the second proposal is affordable.", "On the other hand the second proposal, is affordable.", "On, the other hand the second proposal is affordable.", "On the other hand; the second proposal is affordable."),
        ("Which sentence correctly uses a semicolon between two independent clauses without a conjunction?", "The deadline was approaching; everyone worked faster.", "The deadline was approaching, everyone worked faster.", "The deadline was approaching: and everyone worked faster.", "The deadline was approaching; and everyone worked faster."),
        ("Which sentence correctly uses punctuation around a non-essential appositive?", "Mr. Rao, our mathematics teacher, is retiring.", "Mr. Rao our mathematics teacher, is retiring.", "Mr. Rao; our mathematics teacher; is retiring.", "Mr. Rao: our mathematics teacher is retiring."),
        ("Which sentence correctly uses punctuation in a formal salutation?", "Dear Professor Sharma,", "Dear Professor Sharma?", "Dear Professor Sharma!", "Dear, Professor Sharma.")
    ]
}


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Punctuation", "English")
        )
        row = cur.fetchone()

        if not row:
            raise Exception(
                "Lesson 'Punctuation' with topic 'English' was not found."
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
                    (lesson_id, f"Punctuation - {difficulty}", difficulty)
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
                    raise Exception(f"Duplicate options found: {question}")

                random.shuffle(options)
                correct_letter = "ABCD"[options.index(answer)]

                cur.execute(
                    """
                    INSERT INTO questions
                    (quiz_id, question, option_a, option_b,
                     option_c, option_d, correct_answer)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        quiz_id,
                        question,
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
                    f"{difficulty}: Expected 30 questions, found {final_count}."
                )

            print(f"{difficulty}: {final_count}/30 questions ready.")

        con.commit()
        print("\nSUCCESS: Punctuation has exactly 90 questions!")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
