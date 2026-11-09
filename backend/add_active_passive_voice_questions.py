
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("Choose the passive form: 'She writes a letter.'", "A letter is written by her.", "A letter was written by her.", "A letter has written by her.", "A letter is writing by her."),
        ("Choose the passive form: 'He kicked the ball.'", "The ball was kicked by him.", "The ball is kicked by him.", "The ball has kicked by him.", "The ball was kicking by him."),
        ("Choose the passive form: 'They clean the room.'", "The room is cleaned by them.", "The room was cleaned by them.", "The room has cleaned by them.", "The room is cleaning by them."),
        ("Choose the passive form: 'The teacher praised Ravi.'", "Ravi was praised by the teacher.", "Ravi is praised by the teacher.", "Ravi has praised by the teacher.", "Ravi praised by the teacher."),
        ("Choose the passive form: 'She is cooking food.'", "Food is being cooked by her.", "Food was being cooked by her.", "Food has been cooked by her.", "Food is cooked by her."),
        ("Choose the passive form: 'He will complete the work.'", "The work will be completed by him.", "The work will completed by him.", "The work is completed by him.", "The work was completed by him."),
        ("Choose the passive form: 'The police caught the thief.'", "The thief was caught by the police.", "The thief is caught by the police.", "The thief has caught by the police.", "The thief caught by the police."),
        ("Choose the passive form: 'I opened the door.'", "The door was opened by me.", "The door is opened by me.", "The door has opened by me.", "The door was opening by me."),
        ("Choose the passive form: 'They are building a bridge.'", "A bridge is being built by them.", "A bridge was built by them.", "A bridge has built by them.", "A bridge is built by them."),
        ("Choose the passive form: 'She has finished the task.'", "The task has been finished by her.", "The task had finished by her.", "The task is being finished by her.", "The task has finished by her."),
        ("Choose the passive form: 'The chef prepares dinner.'", "Dinner is prepared by the chef.", "Dinner was prepared by the chef.", "Dinner has prepared by the chef.", "Dinner is preparing by the chef."),
        ("Choose the passive form: 'He painted the wall.'", "The wall was painted by him.", "The wall is painted by him.", "The wall has painted by him.", "The wall was painting by him."),
        ("Choose the passive form: 'The children are flying kites.'", "Kites are being flown by the children.", "Kites were flown by the children.", "Kites have flown by the children.", "Kites are flown by the children."),
        ("Choose the passive form: 'She will invite the guests.'", "The guests will be invited by her.", "The guests will invited by her.", "The guests are invited by her.", "The guests were invited by her."),
        ("Choose the passive form: 'Someone stole my bag.'", "My bag was stolen.", "My bag is stolen.", "My bag has stole.", "My bag was stealing."),
        ("Choose the active form: 'The cake was baked by Riya.'", "Riya baked the cake.", "Riya bakes the cake.", "Riya is baking the cake.", "Riya has baked the cake."),
        ("Choose the active form: 'The song is sung by her.'", "She sings the song.", "She sang the song.", "She is singing the song.", "She has sung the song."),
        ("Choose the active form: 'The match was won by our team.'", "Our team won the match.", "Our team wins the match.", "Our team is winning the match.", "Our team has won the match."),
        ("Choose the active form: 'The room is cleaned by the maid.'", "The maid cleans the room.", "The maid cleaned the room.", "The maid is cleaning the room.", "The maid has cleaned the room."),
        ("Choose the active form: 'The letter was written by Rahul.'", "Rahul wrote the letter.", "Rahul writes the letter.", "Rahul is writing the letter.", "Rahul has written the letter."),
        ("Choose the passive form: 'People speak English worldwide.'", "English is spoken worldwide.", "English was spoken worldwide.", "English has spoken worldwide.", "English is speaking worldwide."),
        ("Choose the passive form: 'She washed the clothes.'", "The clothes were washed by her.", "The clothes are washed by her.", "The clothes have washed by her.", "The clothes were washing by her."),
        ("Choose the passive form: 'He is repairing the car.'", "The car is being repaired by him.", "The car was repaired by him.", "The car has repaired by him.", "The car is repaired by him."),
        ("Choose the passive form: 'They have completed the project.'", "The project has been completed by them.", "The project had completed by them.", "The project is completed by them.", "The project has completed by them."),
        ("Choose the passive form: 'The dog chased the cat.'", "The cat was chased by the dog.", "The cat is chased by the dog.", "The cat has chased by the dog.", "The cat chased by the dog."),
        ("Choose the passive form: 'The company sells mobile phones.'", "Mobile phones are sold by the company.", "Mobile phones were sold by the company.", "Mobile phones have sold by the company.", "Mobile phones are selling by the company."),
        ("Choose the passive form: 'She is reading a novel.'", "A novel is being read by her.", "A novel was read by her.", "A novel has read by her.", "A novel is read by her."),
        ("Choose the passive form: 'The manager will announce the result.'", "The result will be announced by the manager.", "The result will announced by the manager.", "The result is announced by the manager.", "The result was announced by the manager."),
        ("Choose the passive form: 'He has repaired the computer.'", "The computer has been repaired by him.", "The computer had repaired by him.", "The computer is repairing by him.", "The computer has repaired by him."),
        ("Choose the passive form: 'The students respect their teacher.'", "Their teacher is respected by the students.", "Their teacher was respected by the students.", "Their teacher has respected by the students.", "Their teacher is respecting by the students."),
    ],

    "Medium": [
        ("Choose the passive form: 'They were watching a movie.'", "A movie was being watched by them.", "A movie is being watched by them.", "A movie had been watched by them.", "A movie was watched by them."),
        ("Choose the passive form: 'She had completed the assignment.'", "The assignment had been completed by her.", "The assignment has been completed by her.", "The assignment was completed by her.", "The assignment had completed by her."),
        ("Choose the passive form: 'The workers will have finished the building.'", "The building will have been finished by the workers.", "The building will be finished by the workers.", "The building has been finished by the workers.", "The building will have finished by the workers."),
        ("Choose the passive form: 'Did he write the report?'", "Was the report written by him?", "Is the report written by him?", "Has the report written by him?", "Did the report written by him?"),
        ("Choose the passive form: 'Who broke the window?'", "By whom was the window broken?", "By whom is the window broken?", "Who was the window broke?", "By whom has the window broken?"),
        ("Choose the passive form: 'You must follow the rules.'", "The rules must be followed.", "The rules must followed.", "The rules are followed.", "The rules must have follow."),
        ("Choose the passive form: 'They can solve this problem.'", "This problem can be solved by them.", "This problem can solved by them.", "This problem is solving by them.", "This problem could solved by them."),
        ("Choose the passive form: 'The committee is reviewing the proposal.'", "The proposal is being reviewed by the committee.", "The proposal was reviewed by the committee.", "The proposal has reviewed by the committee.", "The proposal is reviewed by the committee."),
        ("Choose the passive form: 'Someone has stolen the documents.'", "The documents have been stolen.", "The documents had stolen.", "The documents are stealing.", "The documents have stolen."),
        ("Choose the passive form: 'The teacher will give the students certificates.'", "The students will be given certificates by the teacher.", "The students will given certificates by the teacher.", "The students are given certificates by the teacher.", "The students were given certificates by the teacher."),
        ("Choose the passive form: 'The doctor examined the patient.'", "The patient was examined by the doctor.", "The patient is examined by the doctor.", "The patient has examined by the doctor.", "The patient was examining by the doctor."),
        ("Choose the passive form: 'They should respect the elderly.'", "The elderly should be respected.", "The elderly should respected.", "The elderly are respecting.", "The elderly should have respect."),
        ("Choose the passive form: 'The storm damaged several houses.'", "Several houses were damaged by the storm.", "Several houses are damaged by the storm.", "Several houses have damaged by the storm.", "Several houses were damaging by the storm."),
        ("Choose the passive form: 'The police are questioning the suspect.'", "The suspect is being questioned by the police.", "The suspect was questioned by the police.", "The suspect has questioned by the police.", "The suspect is questioned by the police."),
        ("Choose the passive form: 'They had not informed me.'", "I had not been informed by them.", "I have not been informed by them.", "I was not informed by them.", "I had not informed by them."),
        ("Choose the active form: 'The invitation will be sent by the secretary.'", "The secretary will send the invitation.", "The secretary sent the invitation.", "The secretary sends the invitation.", "The secretary is sending the invitation."),
        ("Choose the active form: 'The work must be completed today.'", "Someone must complete the work today.", "Someone completed the work today.", "Someone completes the work today.", "Someone is completing the work today."),
        ("Choose the active form: 'The house is being painted by the workers.'", "The workers are painting the house.", "The workers painted the house.", "The workers paint the house.", "The workers have painted the house."),
        ("Choose the active form: 'The results have been declared by the university.'", "The university has declared the results.", "The university declared the results.", "The university declares the results.", "The university is declaring the results."),
        ("Choose the active form: 'The patient was being treated by the doctor.'", "The doctor was treating the patient.", "The doctor treated the patient.", "The doctor treats the patient.", "The doctor has treated the patient."),
        ("Choose the passive form: 'Do they sell books here?'", "Are books sold here?", "Were books sold here?", "Have books sold here?", "Do books sold here?"),
        ("Choose the passive form: 'The principal made an announcement.'", "An announcement was made by the principal.", "An announcement is made by the principal.", "An announcement has made by the principal.", "An announcement was making by the principal."),
        ("Choose the passive form: 'She may accept the offer.'", "The offer may be accepted by her.", "The offer may accepted by her.", "The offer is accepted by her.", "The offer may have accept by her."),
        ("Choose the passive form: 'They are going to launch a new product.'", "A new product is going to be launched by them.", "A new product is going to launched by them.", "A new product was launched by them.", "A new product has been launched by them."),
        ("Choose the passive form: 'The police have arrested the criminal.'", "The criminal has been arrested by the police.", "The criminal had arrested by the police.", "The criminal is arresting by the police.", "The criminal has arrested by the police."),
        ("Choose the passive form: 'The students were solving difficult questions.'", "Difficult questions were being solved by the students.", "Difficult questions are being solved by the students.", "Difficult questions had been solved by the students.", "Difficult questions were solved by the students."),
        ("Choose the passive form: 'We ought to obey the law.'", "The law ought to be obeyed.", "The law ought obeyed.", "The law is obeying.", "The law ought to have obey."),
        ("Choose the passive form: 'The company is not hiring new employees.'", "New employees are not being hired by the company.", "New employees were not hired by the company.", "New employees have not hired by the company.", "New employees are not hired by the company."),
        ("Choose the passive form: 'Has she submitted the application?'", "Has the application been submitted by her?", "Was the application submitted by her?", "Is the application submitted by her?", "Has the application submitted by her?"),
        ("Choose the passive form: 'They gave me a prize.'", "I was given a prize by them.", "I am given a prize by them.", "I have given a prize by them.", "I was giving a prize by them."),
    ],

    "Hard": [
        ("Choose the passive form: 'They will have completed the bridge by June.'", "The bridge will have been completed by June.", "The bridge will be completed by June.", "The bridge has been completed by June.", "The bridge will have completed by June."),
        ("Choose the passive form: 'The manager made the employees work late.'", "The employees were made to work late by the manager.", "The employees were made work late by the manager.", "The employees are made to work late by the manager.", "The employees had made to work late by the manager."),
        ("Choose the passive form: 'They saw him cross the road.'", "He was seen to cross the road.", "He was seen cross the road.", "He is seen crossing the road.", "He had seen to cross the road."),
        ("Choose the passive form: 'People believe that he is honest.'", "It is believed that he is honest.", "It was believed that he is honest.", "It is believing that he is honest.", "It has believed that he is honest."),
        ("Choose the passive form: 'They say that she knows the answer.'", "It is said that she knows the answer.", "It was said that she knows the answer.", "It says that she knows the answer.", "It has said that she knows the answer."),
        ("Choose the passive form: 'Someone has to complete this task.'", "This task has to be completed.", "This task has to completed.", "This task had to completed.", "This task is having to complete."),
        ("Choose the passive form: 'The authorities are looking into the matter.'", "The matter is being looked into by the authorities.", "The matter is looking into by the authorities.", "The matter was looked into by the authorities.", "The matter has looked into by the authorities."),
        ("Choose the passive form: 'They laughed at the stranger.'", "The stranger was laughed at.", "The stranger was laughed.", "The stranger is laughed at.", "The stranger has laughed at."),
        ("Choose the passive form: 'Nobody has answered the question.'", "The question has not been answered.", "The question had not answered.", "The question is not answering.", "The question has not answered."),
        ("Choose the passive form: 'The teacher gave the students extra time.'", "The students were given extra time by the teacher.", "The students are given extra time by the teacher.", "The students have given extra time by the teacher.", "The students were giving extra time by the teacher."),
        ("Choose the passive form: 'They expect the team to win the match.'", "The team is expected to win the match.", "The team is expected winning the match.", "The team was expecting to win the match.", "The team has expected to win the match."),
        ("Choose the passive form: 'The company offered her a promotion.'", "She was offered a promotion by the company.", "She is offered a promotion by the company.", "She has offered a promotion by the company.", "She was offering a promotion by the company."),
        ("Choose the passive form: 'They have called off the meeting.'", "The meeting has been called off.", "The meeting had called off.", "The meeting is calling off.", "The meeting has called off."),
        ("Choose the passive form: 'The police are following up the complaint.'", "The complaint is being followed up by the police.", "The complaint is followed up by the police.", "The complaint was following up by the police.", "The complaint has followed up by the police."),
        ("Choose the passive form: 'Someone should have informed the authorities.'", "The authorities should have been informed.", "The authorities should have informed.", "The authorities should be informing.", "The authorities should had been informed."),
        ("Choose the active form: 'The proposal is believed to have been rejected.'", "People believe that the proposal has been rejected.", "People believed that the proposal was rejected.", "People are believing the proposal has rejected.", "People believe that the proposal is rejecting."),
        ("Choose the active form: 'He was made to apologise by the manager.'", "The manager made him apologise.", "The manager made him to apologise.", "The manager makes him apologised.", "The manager had made to apologise."),
        ("Choose the active form: 'The matter has been dealt with by the committee.'", "The committee has dealt with the matter.", "The committee dealt the matter.", "The committee is dealing the matter.", "The committee has been dealing by the matter."),
        ("Choose the active form: 'The suspect was seen entering the building.'", "Someone saw the suspect entering the building.", "Someone was seeing the suspect enter the building.", "Someone has seen the suspect entered the building.", "Someone sees the suspect entering the building."),
        ("Choose the active form: 'The old building is said to be haunted.'", "People say that the old building is haunted.", "People said that the old building was haunted.", "People are saying the old building haunted.", "People have said the old building be haunted."),
        ("Choose the passive form: 'Who has written this report?'", "By whom has this report been written?", "By whom was this report written?", "Who has this report written?", "By whom has written this report?"),
        ("Choose the passive form: 'Why did they cancel the programme?'", "Why was the programme cancelled?", "Why is the programme cancelled?", "Why has the programme cancelled?", "Why did the programme cancelled?"),
        ("Choose the passive form: 'The teacher expects students to submit the work.'", "Students are expected to submit the work.", "Students are expected submitting the work.", "Students were expecting to submit the work.", "Students have expected to submit the work."),
        ("Choose the passive form: 'They know him to be an expert.'", "He is known to be an expert.", "He is known being an expert.", "He was knowing to be an expert.", "He has known to be an expert."),
        ("Choose the passive form: 'The organisation will provide the candidates with accommodation.'", "The candidates will be provided with accommodation by the organisation.", "The candidates will provide with accommodation by the organisation.", "The candidates are provided accommodation by the organisation.", "The candidates will have provided with accommodation."),
        ("Choose the passive form: 'Do not touch the exhibits.'", "The exhibits must not be touched.", "The exhibits are not touch.", "The exhibits should not touched.", "The exhibits were not being touched."),
        ("Choose the passive form: 'They made him repeat the experiment.'", "He was made to repeat the experiment.", "He was made repeat the experiment.", "He is made repeating the experiment.", "He had made to repeat the experiment."),
        ("Choose the passive form: 'We must take care of these documents.'", "These documents must be taken care of.", "These documents must taken care of.", "These documents are taking care of.", "These documents must have take care of."),
        ("Choose the passive form: 'The authorities have put off the event.'", "The event has been put off by the authorities.", "The event had put off by the authorities.", "The event is putting off by the authorities.", "The event has put off by the authorities."),
        ("Choose the passive form: 'Someone is watching the children.'", "The children are being watched.", "The children are watched.", "The children were being watched.", "The children have watched."),
    ]
}


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Active and Passive Voice", "English")
        )
        row = cur.fetchone()

        if not row:
            raise Exception(
                "Lesson 'Active and Passive Voice' with topic 'English' was not found."
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
                    (lesson_id, f"Active and Passive Voice - {difficulty}", difficulty)
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
        print("\nSUCCESS: Active and Passive Voice has exactly 90 questions!")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
