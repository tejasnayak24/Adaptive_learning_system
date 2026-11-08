
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("Which type of sentence makes a statement?", "Declarative", "Interrogative", "Imperative", "Exclamatory"),
        ("Which type of sentence asks a question?", "Interrogative", "Declarative", "Imperative", "Exclamatory"),
        ("Which type of sentence gives a command?", "Imperative", "Declarative", "Interrogative", "Exclamatory"),
        ("Which type of sentence expresses strong emotion?", "Exclamatory", "Declarative", "Interrogative", "Imperative"),
        ("Identify the sentence type: 'The sun rises in the east.'", "Declarative", "Interrogative", "Imperative", "Exclamatory"),
        ("Identify the sentence type: 'Where do you live?'", "Interrogative", "Declarative", "Imperative", "Exclamatory"),
        ("Identify the sentence type: 'Please close the door.'", "Imperative", "Declarative", "Interrogative", "Exclamatory"),
        ("Identify the sentence type: 'What a beautiful flower!'", "Exclamatory", "Declarative", "Interrogative", "Imperative"),
        ("Which punctuation mark usually ends a question?", "Question mark (?)", "Full stop (.)", "Comma (,)", "Colon (:)"),
        ("Which punctuation mark usually ends a declarative sentence?", "Full stop (.)", "Question mark (?)", "Exclamation mark (!)", "Comma (,)"),
        ("'Do your homework.' is an example of which sentence type?", "Imperative", "Interrogative", "Declarative", "Exclamatory"),
        ("'I enjoy reading books.' is which type of sentence?", "Declarative", "Imperative", "Interrogative", "Exclamatory"),
        ("'How are you today?' is which type of sentence?", "Interrogative", "Declarative", "Imperative", "Exclamatory"),
        ("'Hurray! We won the match!' is which type of sentence?", "Exclamatory", "Declarative", "Interrogative", "Imperative"),
        ("Which sentence expresses a request?", "Please lend me your pen.", "The pen is blue.", "Where is your pen?", "What a lovely pen!"),
        ("Which sentence gives an instruction?", "Turn left at the next street.", "The street is crowded.", "Is the street crowded?", "What a busy street!"),
        ("Which sentence is declarative?", "She is my best friend.", "Are you my friend?", "Be my friend.", "What a good friend!"),
        ("Which sentence is interrogative?", "Have you finished your work?", "I finished my work.", "Finish your work.", "What wonderful work!"),
        ("Which sentence is exclamatory?", "What a wonderful performance!", "The performance was wonderful.", "Was the performance wonderful?", "Watch the performance."),
        ("Which sentence is imperative?", "Keep your room clean.", "Your room is clean.", "Is your room clean?", "What a clean room!"),
        ("A sentence that communicates information is called a ___ sentence.", "Declarative", "Interrogative", "Imperative", "Exclamatory"),
        ("A sentence that seeks information is called a ___ sentence.", "Interrogative", "Declarative", "Imperative", "Exclamatory"),
        ("A sentence that expresses excitement is called a ___ sentence.", "Exclamatory", "Declarative", "Interrogative", "Imperative"),
        ("A sentence that tells someone to do something is called a ___ sentence.", "Imperative", "Declarative", "Interrogative", "Exclamatory"),
        ("Which sentence ends with an exclamation mark?", "What an amazing view!", "The view is amazing.", "Is the view amazing?", "Look at the view."),
        ("Identify the sentence type: 'My brother plays football.'", "Declarative", "Interrogative", "Imperative", "Exclamatory"),
        ("Identify the sentence type: 'Never touch that wire.'", "Imperative", "Declarative", "Interrogative", "Exclamatory"),
        ("Identify the sentence type: 'Why are you laughing?'", "Interrogative", "Declarative", "Imperative", "Exclamatory"),
        ("Identify the sentence type: 'Alas! The old man is dead.'", "Exclamatory", "Declarative", "Interrogative", "Imperative"),
        ("Which of these is a statement?", "The train arrives at six.", "When does the train arrive?", "Catch the train.", "What a fast train!")
    ],

    "Medium": [
        ("Identify the sentence type: 'Could you pass me the salt?'", "Interrogative", "Declarative", "Imperative", "Exclamatory"),
        ("Identify the sentence type: 'Kindly submit your assignment tomorrow.'", "Imperative", "Declarative", "Interrogative", "Exclamatory"),
        ("Identify the sentence type: 'What a terrible mistake you have made!'", "Exclamatory", "Interrogative", "Declarative", "Imperative"),
        ("Identify the sentence type: 'The earth revolves around the sun.'", "Declarative", "Imperative", "Interrogative", "Exclamatory"),
        ("Which sentence is an indirect request?", "Would you mind opening the window?", "The window is open.", "Why is the window open?", "What a large window!"),
        ("Which sentence is a negative declarative sentence?", "She does not like coffee.", "Does she like coffee?", "Do not drink coffee.", "How bitter the coffee is!"),
        ("Which sentence is an interrogative sentence?", "Who called you last night?", "Someone called me last night.", "Call me tonight.", "What a surprise call!"),
        ("Which sentence is an imperative sentence?", "Please remain seated.", "You are seated.", "Are you seated?", "What a comfortable seat!"),
        ("Which sentence expresses a strong feeling?", "How beautiful the sunset is!", "The sunset is beautiful.", "Is the sunset beautiful?", "Watch the sunset."),
        ("Identify the sentence type: 'Don't forget to lock the door.'", "Imperative", "Declarative", "Interrogative", "Exclamatory"),
        ("Identify the sentence type: 'There is no water in the tank.'", "Declarative", "Interrogative", "Imperative", "Exclamatory"),
        ("Identify the sentence type: 'Why don't you join us for dinner?'", "Interrogative", "Declarative", "Imperative", "Exclamatory"),
        ("Identify the sentence type: 'May you live a long and happy life!'", "Exclamatory", "Interrogative", "Declarative", "Imperative"),
        ("Which sentence is a command rather than a statement?", "Stop talking immediately.", "You are talking loudly.", "Are you talking loudly?", "How loudly you talk!"),
        ("Which sentence is a declarative sentence with negative meaning?", "They never arrive on time.", "Do they arrive on time?", "Arrive on time.", "How late they are!"),
        ("Which sentence is interrogative in form?", "Can you solve this problem?", "You can solve this problem.", "Solve this problem.", "What an easy problem!"),
        ("Which sentence is imperative in form?", "Let us begin the meeting.", "The meeting begins now.", "When does the meeting begin?", "What an important meeting!"),
        ("Which sentence is exclamatory in form?", "What a magnificent building it is!", "It is a magnificent building.", "Is it a magnificent building?", "Visit the magnificent building."),
        ("Identify the sentence type: 'Never judge a book by its cover.'", "Imperative", "Declarative", "Interrogative", "Exclamatory"),
        ("Identify the sentence type: 'Nobody attended the function.'", "Declarative", "Imperative", "Interrogative", "Exclamatory"),
        ("Which sentence asks a question but also expresses surprise?", "You finished the entire book already?", "You finished the entire book.", "Finish the entire book.", "What an interesting book!"),
        ("Which sentence gives advice?", "You should exercise regularly.", "Do you exercise regularly?", "What regular exercise!", "Exercise is a physical activity."),
        ("Which sentence is a polite command?", "Please wait here for a moment.", "You are waiting here.", "Are you waiting here?", "What a long wait!"),
        ("Identify the sentence type: 'How foolish I have been!'", "Exclamatory", "Declarative", "Imperative", "Interrogative"),
        ("Which sentence is declarative despite containing a question word?", "I know where she lives.", "Where does she live?", "Tell me where she lives.", "Where she lives!"),
        ("Which sentence is an interrogative sentence with a negative form?", "Didn't you receive my message?", "You received my message.", "Do not ignore my message.", "What a useful message!"),
        ("Which sentence expresses a wish?", "May all your dreams come true!", "All your dreams are wonderful.", "Will your dreams come true?", "Follow your dreams."),
        ("Identify the sentence type: 'Let the children play outside.'", "Imperative", "Declarative", "Interrogative", "Exclamatory"),
        ("Which sentence makes a factual statement?", "Water boils at 100°C at standard atmospheric pressure.", "Does water boil at 100°C?", "Boil the water.", "How hot the water is!"),
        ("Which sentence is an exclamation?", "What an extraordinary achievement!", "It was an extraordinary achievement.", "Was it an extraordinary achievement?", "Remember the achievement.")
    ],

    "Hard": [
        ("Identify the sentence type: 'I wonder whether he will attend the conference.'", "Declarative", "Interrogative", "Imperative", "Exclamatory"),
        ("Identify the sentence type: 'Tell me what you have decided.'", "Imperative", "Declarative", "Interrogative", "Exclamatory"),
        ("Identify the sentence type: 'How dare you question my honesty!'", "Exclamatory", "Declarative", "Interrogative", "Imperative"),
        ("Identify the sentence type: 'Would that I could travel around the world!'", "Exclamatory", "Interrogative", "Declarative", "Imperative"),
        ("Which sentence is declarative in form but functions as a request?", "I would like you to close the door.", "Close the door.", "Could you close the door?", "What a noisy door!"),
        ("Which sentence is interrogative in form but functions as a request?", "Could you please help me?", "You should help me.", "Help me immediately.", "How helpful you are!"),
        ("Which sentence is imperative in form but expresses a suggestion?", "Let's go for a walk.", "We went for a walk.", "Shall we go for a walk?", "What a lovely walk!"),
        ("Identify the sentence type: 'It is surprising how quickly time passes.'", "Declarative", "Interrogative", "Imperative", "Exclamatory"),
        ("Identify the sentence type: 'What she said was completely unexpected.'", "Declarative", "Interrogative", "Imperative", "Exclamatory"),
        ("Which sentence contains an embedded question but is declarative overall?", "She asked me where I lived.", "Where do you live?", "Tell me where you live.", "What a strange place!"),
        ("Identify the sentence type: 'Do tell me the truth.'", "Imperative", "Interrogative", "Declarative", "Exclamatory"),
        ("Which sentence is an exclamatory sentence?", "What a difference a day makes!", "A day makes a difference.", "Does a day make a difference?", "Notice the difference."),
        ("Which sentence is declarative in structure?", "How he managed it remains a mystery.", "How did he manage it?", "Tell me how he managed it.", "How brilliantly he managed it!"),
        ("Identify the sentence type: 'Never have I witnessed such a performance!'", "Exclamatory", "Declarative", "Interrogative", "Imperative"),
        ("Which sentence is an imperative with an implied subject?", "Please switch off the lights.", "You switch off the lights.", "Do you switch off the lights?", "The lights are switched off."),
        ("Identify the sentence type: 'Whether he agrees or not is irrelevant.'", "Declarative", "Interrogative", "Imperative", "Exclamatory"),
        ("Which sentence uses interrogative form to express disbelief?", "You expect me to believe that?", "I believe that story.", "Believe that story.", "What a believable story!"),
        ("Which sentence is an exclamatory statement beginning with 'How'?", "How beautifully she sings!", "How does she sing?", "She sings beautifully.", "Sing beautifully."),
        ("Identify the sentence type: 'Let no one enter this room.'", "Imperative", "Declarative", "Interrogative", "Exclamatory"),
        ("Which sentence is a declarative sentence containing an indirect question?", "I cannot understand why he left.", "Why did he leave?", "Tell me why he left.", "Why he left!"),
        ("Which sentence is interrogative in structure but can function as a suggestion?", "Shall we take a break?", "We should take a break.", "Take a break.", "What a refreshing break!"),
        ("Identify the sentence type: 'If only I had listened to your advice!'", "Exclamatory", "Declarative", "Interrogative", "Imperative"),
        ("Which sentence is imperative in form and expresses a warning?", "Watch your step!", "Your step is dangerous.", "Is your step dangerous?", "What a dangerous step!"),
        ("Which sentence is declarative despite beginning with 'What'?", "What he needs is more time.", "What does he need?", "Tell me what he needs.", "What a lot of time he needs!"),
        ("Identify the sentence type: 'The question is whether we can finish on time.'", "Declarative", "Interrogative", "Imperative", "Exclamatory"),
        ("Which sentence is an interrogative question seeking confirmation?", "You have completed the assignment, haven't you?", "You have completed the assignment.", "Complete the assignment.", "What a completed assignment!"),
        ("Which sentence is imperative but softened by the word 'kindly'?", "Kindly refrain from making noise.", "You are making noise.", "Are you making noise?", "What noisy surroundings!"),
        ("Identify the sentence type: 'Long live the king!'", "Exclamatory", "Declarative", "Interrogative", "Imperative"),
        ("Which sentence is declarative rather than interrogative?", "I asked whether the shop was open.", "Was the shop open?", "Can you tell me if the shop is open?", "How long is the shop open!"),
        ("Which sentence is an exclamatory sentence expressing regret?", "Alas! We have lost the opportunity!", "We lost the opportunity.", "Did we lose the opportunity?", "Do not lose the opportunity.")
    ]
}


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Sentence Types", "English")
        )
        row = cur.fetchone()

        if not row:
            raise Exception("Lesson 'Sentence Types' with topic 'English' was not found.")

        lesson_id = row[0]

        for difficulty, questions in BANK.items():
            if len(questions) != 30:
                raise Exception(f"{difficulty} bank must contain exactly 30 questions.")

            cur.execute(
                "SELECT id FROM quizzes WHERE lesson_id=? AND difficulty=?",
                (lesson_id, difficulty)
            )
            quiz = cur.fetchone()

            if quiz:
                quiz_id = quiz[0]
            else:
                cur.execute(
                    "INSERT INTO quizzes (lesson_id, title, difficulty) VALUES (?, ?, ?)",
                    (lesson_id, f"Sentence Types - {difficulty}", difficulty)
                )
                quiz_id = cur.lastrowid

            cur.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id=?",
                (quiz_id,)
            )
            existing = cur.fetchone()[0]

            if existing > 30:
                raise Exception(
                    f"{difficulty} already has {existing} questions. Check the database."
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

                cur.execute("""
                    INSERT INTO questions
                    (quiz_id, question, option_a, option_b, option_c, option_d, correct_answer)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    quiz_id,
                    question,
                    options[0],
                    options[1],
                    options[2],
                    options[3],
                    correct_letter
                ))

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
        print("\nSUCCESS: Sentence Types has exactly 90 questions!")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
