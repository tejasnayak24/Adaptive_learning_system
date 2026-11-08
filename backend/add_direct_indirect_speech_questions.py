
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("Change into indirect speech: He said, 'I am happy.'", "He said that he was happy.", "He said that I am happy.", "He says that he was happy.", "He said that he is happy."),
        ("Change into indirect speech: She said, 'I like music.'", "She said that she liked music.", "She said that she likes music.", "She says that she liked music.", "She said that I liked music."),
        ("Change into indirect speech: Ravi said, 'I am tired.'", "Ravi said that he was tired.", "Ravi said that I am tired.", "Ravi says that he was tired.", "Ravi said that he is tired."),
        ("Change into indirect speech: He said, 'I have a car.'", "He said that he had a car.", "He said that he has a car.", "He says that he had a car.", "He said that I have a car."),
        ("Change into indirect speech: She said, 'I will come tomorrow.'", "She said that she would come the next day.", "She said that she will come tomorrow.", "She said that she would come tomorrow.", "She says that she would come the next day."),
        ("Change into indirect speech: He said, 'I can swim.'", "He said that he could swim.", "He said that he can swim.", "He says that he could swim.", "He said that I could swim."),
        ("Change into indirect speech: They said, 'We are playing.'", "They said that they were playing.", "They said that we are playing.", "They say that they were playing.", "They said that they are playing."),
        ("Change into indirect speech: She said, 'I went to school.'", "She said that she had gone to school.", "She said that she goes to school.", "She said that she has gone to school.", "She says that she had gone to school."),
        ("Change into indirect speech: He said, 'I have finished my work.'", "He said that he had finished his work.", "He said that he has finished his work.", "He says that he had finished his work.", "He said that I had finished my work."),
        ("Change into indirect speech: Mother said, 'The baby is sleeping.'", "Mother said that the baby was sleeping.", "Mother said that the baby is sleeping.", "Mother says that the baby was sleeping.", "Mother said that the baby had slept."),
        ("Change into indirect speech: He said, 'I must study.'", "He said that he had to study.", "He said that he must studied.", "He says that he had to study.", "He said that I must study."),
        ("Change into indirect speech: She said, 'I may visit Delhi.'", "She said that she might visit Delhi.", "She said that she may visit Delhi.", "She says that she might visit Delhi.", "She said that I might visit Delhi."),
        ("Change into indirect speech: He said, 'I am reading a book.'", "He said that he was reading a book.", "He said that he is reading a book.", "He says that he was reading a book.", "He said that I was reading a book."),
        ("Change into indirect speech: Riya said, 'I bought a dress.'", "Riya said that she had bought a dress.", "Riya said that she buys a dress.", "Riya said that she has bought a dress.", "Riya says that she had bought a dress."),
        ("Change into indirect speech: He said, 'I do not like tea.'", "He said that he did not like tea.", "He said that he does not liked tea.", "He says that he did not like tea.", "He said that I do not like tea."),
        ("Change into indirect speech: She said, 'I was cooking.'", "She said that she had been cooking.", "She said that she is cooking.", "She said that she was cook.", "She says that she had been cooking."),
        ("Change into indirect speech: He said to me, 'You are kind.'", "He told me that I was kind.", "He told me that you are kind.", "He said me that I was kind.", "He tells me that I am kind."),
        ("Change into indirect speech: She said to him, 'You are late.'", "She told him that he was late.", "She told him that you are late.", "She said him that he was late.", "She tells him that he is late."),
        ("Change into indirect speech: He said, 'This is my house.'", "He said that that was his house.", "He said that this is my house.", "He says that that was his house.", "He said that this was my house."),
        ("Change into indirect speech: She said, 'I will help you.'", "She said that she would help me.", "She said that I will help you.", "She says that she would help me.", "She said that she will help me."),
        ("Change into indirect speech: He said, 'I saw a bird yesterday.'", "He said that he had seen a bird the previous day.", "He said that he saw a bird yesterday.", "He said that he has seen a bird the previous day.", "He says that he had seen a bird yesterday."),
        ("Change into indirect speech: They said, 'We have won the match.'", "They said that they had won the match.", "They said that we have won the match.", "They say that they had won the match.", "They said that they have won the match."),
        ("Change into indirect speech: He said, 'I am going now.'", "He said that he was going then.", "He said that he is going now.", "He says that he was going then.", "He said that I was going now."),
        ("Change into indirect speech: She said, 'I need some water.'", "She said that she needed some water.", "She said that she needs some water.", "She says that she needed some water.", "She said that I needed some water."),
        ("Change into indirect speech: He said, 'I cannot drive.'", "He said that he could not drive.", "He said that he cannot drove.", "He says that he could not drive.", "He said that I cannot drive."),
        ("Change into indirect speech: The boy said, 'I am hungry.'", "The boy said that he was hungry.", "The boy said that I am hungry.", "The boy says that he was hungry.", "The boy said that he is hungry."),
        ("Change into indirect speech: She said, 'I have lost my pen.'", "She said that she had lost her pen.", "She said that she has lost my pen.", "She says that she had lost her pen.", "She said that I had lost my pen."),
        ("Change into indirect speech: He said, 'I shall return soon.'", "He said that he would return soon.", "He said that he shall return soon.", "He says that he would return soon.", "He said that I would return soon."),
        ("Change into indirect speech: They said, 'We were watching TV.'", "They said that they had been watching TV.", "They said that we were watching TV.", "They say that they had been watching TV.", "They said that they are watching TV."),
        ("Change into indirect speech: She said, 'I know the answer.'", "She said that she knew the answer.", "She said that she knows the answer.", "She says that she knew the answer.", "She said that I knew the answer."),
    ],

    "Medium": [
        ("Change into indirect speech: He said to me, 'Are you ready?'", "He asked me if I was ready.", "He told me that I was ready.", "He asked me that I am ready.", "He said me whether I was ready."),
        ("Change into indirect speech: She said to him, 'Where do you live?'", "She asked him where he lived.", "She asked him where did he live.", "She told him where he lives.", "She asked him where do you live."),
        ("Change into indirect speech: The teacher said, 'Have you completed your homework?'", "The teacher asked whether we had completed our homework.", "The teacher asked that we have completed our homework.", "The teacher told us if we completed our homework.", "The teacher asked whether had we completed our homework."),
        ("Change into indirect speech: He said to her, 'Why are you crying?'", "He asked her why she was crying.", "He asked her why was she crying.", "He told her why she is crying.", "He asked her why are you crying."),
        ("Change into indirect speech: She said, 'What is your name?'", "She asked what my name was.", "She asked what was my name.", "She told what my name is.", "She asked what is your name."),
        ("Change into indirect speech: He said to me, 'Do you know Rahul?'", "He asked me whether I knew Rahul.", "He asked me that I know Rahul.", "He told me whether I knew Rahul.", "He asked me do I know Rahul."),
        ("Change into indirect speech: The teacher said to the students, 'Do not make noise.'", "The teacher told the students not to make noise.", "The teacher said the students do not make noise.", "The teacher told the students to not made noise.", "The teacher asked that the students did not make noise."),
        ("Change into indirect speech: Mother said to me, 'Please help me.'", "Mother requested me to help her.", "Mother told me that please help her.", "Mother requested me that I helped her.", "Mother said me to help her."),
        ("Change into indirect speech: He said to me, 'Open the door.'", "He ordered me to open the door.", "He said me open the door.", "He told that I opened the door.", "He ordered me that open the door."),
        ("Change into indirect speech: She said, 'Let us go for a walk.'", "She suggested that they should go for a walk.", "She ordered that they went for a walk.", "She said that let us go for a walk.", "She asked that they go for a walk."),
        ("Change into indirect speech: He said, 'What a beautiful painting!'", "He exclaimed that it was a very beautiful painting.", "He asked whether it was a beautiful painting.", "He said what a beautiful painting it is.", "He exclaimed that it is a beautiful painting."),
        ("Change into indirect speech: She said, 'Alas! I have lost my purse.'", "She exclaimed with sorrow that she had lost her purse.", "She exclaimed with joy that she lost her purse.", "She said alas that I have lost my purse.", "She asked if she had lost her purse."),
        ("Change into indirect speech: He said to me, 'Can you solve this problem?'", "He asked me if I could solve that problem.", "He asked me that I can solve this problem.", "He told me whether I could solve this problem.", "He asked me can I solve that problem."),
        ("Change into indirect speech: She said, 'I will meet you here tomorrow.'", "She said that she would meet me there the next day.", "She said that she will meet me here tomorrow.", "She said that she would meet me here the next day.", "She says that she would meet me there tomorrow."),
        ("Change into indirect speech: He said, 'The Earth revolves around the Sun.'", "He said that the Earth revolves around the Sun.", "He said that the Earth revolved around the Sun.", "He said that the Earth had revolved around the Sun.", "He says that the Earth revolved around the Sun."),
        ("Change into indirect speech: She said to me, 'When will you return?'", "She asked me when I would return.", "She asked me when would I return.", "She told me when I will return.", "She asked me when will you return."),
        ("Change into indirect speech: The officer said to the guard, 'Do not allow anyone inside.'", "The officer instructed the guard not to allow anyone inside.", "The officer said the guard do not allow anyone inside.", "The officer instructed the guard to not allowed anyone inside.", "The officer asked that nobody entered inside."),
        ("Change into indirect speech: He said, 'I had finished the work before noon.'", "He said that he had finished the work before noon.", "He said that he has finished the work before noon.", "He said that he finished the work before noon.", "He says that he had finished the work before noon."),
        ("Change into indirect speech: She said to him, 'You should consult a doctor.'", "She advised him to consult a doctor.", "She asked him that he should consult a doctor.", "She advised him that consult a doctor.", "She told him he should consulted a doctor."),
        ("Change into indirect speech: He said, 'May you succeed!'", "He wished that I might succeed.", "He ordered that I may succeed.", "He asked whether I would succeed.", "He said that I succeeded."),
        ("Change into indirect speech: She said, 'I must finish this today.'", "She said that she had to finish that that day.", "She said that she must finished this today.", "She says that she had to finish this that day.", "She said that I had to finish that day."),
        ("Change into indirect speech: He said to me, 'Who taught you English?'", "He asked me who had taught me English.", "He asked me who taught you English.", "He asked me who did teach me English.", "He told me who had taught me English."),
        ("Change into indirect speech: The teacher said, 'Honesty is the best policy.'", "The teacher said that honesty is the best policy.", "The teacher said that honesty was the best policy.", "The teacher told that honesty had been the best policy.", "The teacher asked if honesty was the best policy."),
        ("Change into indirect speech: He said to her, 'Please do not disturb me.'", "He requested her not to disturb him.", "He requested her to not disturbed him.", "He told her that please do not disturb me.", "He said her not disturbing him."),
        ("Change into indirect speech: She said, 'How clever the child is!'", "She exclaimed that the child was very clever.", "She asked how clever the child was.", "She exclaimed that the child is very clever.", "She said how clever is the child."),
        ("Change into indirect speech: He said, 'I may visit my uncle next week.'", "He said that he might visit his uncle the following week.", "He said that he may visit my uncle next week.", "He says that he might visit his uncle the following week.", "He said that he might visit his uncle next week."),
        ("Change into indirect speech: She said to me, 'Did you attend the meeting yesterday?'", "She asked me whether I had attended the meeting the previous day.", "She asked me whether I attended the meeting yesterday.", "She told me if I had attended the meeting yesterday.", "She asked me did I attend the meeting the previous day."),
        ("Change into indirect speech: He said, 'I have been waiting for two hours.'", "He said that he had been waiting for two hours.", "He said that he has been waiting for two hours.", "He says that he had been waiting for two hours.", "He said that I had waited for two hours."),
        ("Change into indirect speech: The captain said, 'Bravo! We have won the match.'", "The captain exclaimed with joy that they had won the match.", "The captain exclaimed with sorrow that they had lost the match.", "The captain said bravo that we have won the match.", "The captain asked whether they had won the match."),
        ("Change into indirect speech: He said to me, 'Would you please lend me your pen?'", "He requested me to lend him my pen.", "He ordered me that I lend him your pen.", "He asked me would I lend him my pen.", "He requested that I lent him my pen."),
    ],

    "Hard": [
        ("Change into indirect speech: He said, 'If I were rich, I would travel the world.'", "He said that if he were rich, he would travel the world.", "He said that if he had been rich, he would have travelled the world.", "He said that if I were rich, I would travel the world.", "He says that if he were rich, he will travel the world."),
        ("Change into indirect speech: She said, 'I would have helped you if I had known.'", "She said that she would have helped me if she had known.", "She said that she will help me if she knew.", "She said that I would have helped you if I had known.", "She says that she would help me if she had known."),
        ("Change into indirect speech: The teacher said to me, 'Why did you not submit the assignment?'", "The teacher asked me why I had not submitted the assignment.", "The teacher asked me why had I not submitted the assignment.", "The teacher told me why I did not submit the assignment.", "The teacher asked why did you not submit the assignment."),
        ("Change into indirect speech: He said, 'Had I known the truth, I would have acted differently.'", "He said that if he had known the truth, he would have acted differently.", "He said that if he knew the truth, he would act differently.", "He said that had I known the truth, I would have acted differently.", "He says that if he had known the truth, he will act differently."),
        ("Change into indirect speech: She said, 'I wish I had studied harder.'", "She said that she wished she had studied harder.", "She said that she wishes she studied harder.", "She said that I wish I had studied harder.", "She says that she wished she has studied harder."),
        ("Change into indirect speech: He said to me, 'You had better leave immediately.'", "He advised me to leave immediately.", "He asked me that I had better left immediately.", "He told me that I had better leave immediately.", "He ordered that I leave yesterday."),
        ("Change into indirect speech: The judge said, 'The accused must be given a fair trial.'", "The judge said that the accused must be given a fair trial.", "The judge said that the accused had given a fair trial.", "The judge asked whether the accused must give a fair trial.", "The judge said that the accused was giving a fair trial."),
        ("Change into indirect speech: She said to him, 'Had you completed the work before I arrived?'", "She asked him whether he had completed the work before she arrived.", "She asked him had he completed the work before she arrived.", "She told him whether he completed the work before I arrived.", "She asked whether he has completed the work before she arrived."),
        ("Change into indirect speech: He said, 'Let the meeting begin.'", "He proposed that the meeting should begin.", "He requested the meeting to began.", "He said that let the meeting begin.", "He asked whether the meeting began."),
        ("Change into indirect speech: The manager said to the employees, 'You must not disclose this information.'", "The manager instructed the employees not to disclose that information.", "The manager told the employees that they must not disclosed this information.", "The manager asked the employees to not disclosing that information.", "The manager said that the employees did not disclose this information."),
        ("Change into indirect speech: He said, 'What an extraordinary achievement this is!'", "He exclaimed that it was an extraordinary achievement.", "He asked what an extraordinary achievement it was.", "He exclaimed that this is an extraordinary achievement.", "He said whether it was an extraordinary achievement."),
        ("Change into indirect speech: She said, 'May God bless you!'", "She prayed that God might bless me.", "She ordered that God should bless me.", "She asked whether God blessed me.", "She said that God may blessed you."),
        ("Change into indirect speech: He said to me, 'Why don't we discuss this matter tomorrow?'", "He suggested that we should discuss that matter the next day.", "He asked why we did not discuss this matter tomorrow.", "He ordered me to discuss that matter yesterday.", "He said that why don't we discuss this matter."),
        ("Change into indirect speech: She said, 'I have been working here since 2020.'", "She said that she had been working there since 2020.", "She said that she has been working here since 2020.", "She says that she had worked there since 2020.", "She said that I had been working here since 2020."),
        ("Change into indirect speech: He said, 'This is the best decision I have ever made.'", "He said that that was the best decision he had ever made.", "He said that this is the best decision I have ever made.", "He says that that was the best decision he had ever made.", "He said that this had been the best decision he made."),
        ("Change into indirect speech: The officer said to the driver, 'Show me your driving licence.'", "The officer ordered the driver to show him his driving licence.", "The officer said the driver show me your driving licence.", "The officer asked the driver that he showed his licence.", "The officer ordered that the driver shows me his licence."),
        ("Change into indirect speech: She said to me, 'Can you tell me where the station is?'", "She asked me if I could tell her where the station was.", "She asked me could I tell her where was the station.", "She told me if I can tell her where the station is.", "She asked whether can you tell me where the station is."),
        ("Change into indirect speech: He said, 'I need not attend the meeting.'", "He said that he did not need to attend the meeting.", "He said that he need not attended the meeting.", "He says that he did not need attend the meeting.", "He said that I need not attend the meeting."),
        ("Change into indirect speech: She said, 'Would that I were a bird!'", "She wished that she were a bird.", "She asked whether she was a bird.", "She said that she would be a bird.", "She wished that I had been a bird."),
        ("Change into indirect speech: He said, 'The earth has been revolving around the Sun for billions of years.'", "He said that the earth has been revolving around the Sun for billions of years.", "He said that the earth had revolved around the Sun for billions of years.", "He said that the earth was revolving around the Sun for billions of years.", "He says that the earth had been revolving around the Sun for billions of years."),
        ("Change into indirect speech: The doctor said to the patient, 'You should avoid eating oily food.'", "The doctor advised the patient to avoid eating oily food.", "The doctor asked the patient that he should avoided oily food.", "The doctor told the patient avoid eating oily food.", "The doctor advised that the patient avoided oily food."),
        ("Change into indirect speech: He said, 'Unless you work hard, you will not succeed.'", "He said that unless I worked hard, I would not succeed.", "He said that unless I work hard, I will not succeed.", "He said that unless you worked hard, you will not succeed.", "He says that unless I had worked hard, I would not succeed."),
        ("Change into indirect speech: She said to him, 'You needn't have bought such an expensive gift.'", "She told him that he need not have bought such an expensive gift.", "She told him that he need not buy such an expensive gift.", "She asked him that he had not bought such an expensive gift.", "She said that you needn't have bought such an expensive gift."),
        ("Change into indirect speech: He said, 'How foolish I have been!'", "He exclaimed that he had been very foolish.", "He asked how foolish he had been.", "He exclaimed that I have been very foolish.", "He said that how foolish he is."),
        ("Change into indirect speech: The professor said, 'Water expands when it freezes.'", "The professor said that water expands when it freezes.", "The professor said that water expanded when it froze.", "The professor said that water had expanded when it froze.", "The professor asked whether water expands when it freezes."),
        ("Change into indirect speech: She said to me, 'Please remember to call me when you reach home.'", "She requested me to remember to call her when I reached home.", "She told me please remember to call me when you reach home.", "She requested me that I remembered to call her.", "She asked me to remember calling her when I reach home."),
        ("Change into indirect speech: He said, 'I would rather stay at home than go out.'", "He said that he would rather stay at home than go out.", "He said that he had rather stayed at home than went out.", "He said that I would rather stay at home than go out.", "He says that he would rather stayed at home."),
        ("Change into indirect speech: The teacher said to the student, 'You ought to have informed me earlier.'", "The teacher told the student that he ought to have informed him earlier.", "The teacher asked the student that he ought informed him earlier.", "The teacher told the student that you ought to inform me earlier.", "The teacher said that the student ought to informing him earlier."),
        ("Change into indirect speech: She said, 'If only I could see my grandparents again!'", "She wished that she could see her grandparents again.", "She said that if only I can see my grandparents again.", "She asked whether she could see her grandparents again.", "She wished that I could see my grandparents again."),
        ("Change into indirect speech: He said to me, 'Do whatever you think is right.'", "He told me to do whatever I thought was right.", "He told me that do whatever you think is right.", "He asked me whether I did whatever I thought was right.", "He said me to do whatever I think is right."),
    ]
}


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Direct and Indirect Speech", "English")
        )
        row = cur.fetchone()

        if not row:
            raise Exception(
                "Lesson 'Direct and Indirect Speech' with topic 'English' was not found."
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
                    "INSERT INTO quizzes (lesson_id, title, difficulty) VALUES (?, ?, ?)",
                    (lesson_id, f"Direct and Indirect Speech - {difficulty}", difficulty)
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
        print("\nSUCCESS: Direct and Indirect Speech has exactly 90 questions!")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
