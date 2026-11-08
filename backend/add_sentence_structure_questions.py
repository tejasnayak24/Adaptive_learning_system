
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

BANK = {
    "Easy": [
        ("A sentence must generally contain which essential element?", "A subject and a predicate", "Only an adjective", "Only an adverb", "Two conjunctions"),
        ("What is a simple sentence?", "A sentence with one independent clause", "A sentence with two dependent clauses", "A sentence with no verb", "A sentence with two independent clauses"),
        ("What is a compound sentence?", "A sentence with two or more independent clauses", "A sentence with only one phrase", "A sentence with no subject", "A sentence with one dependent clause only"),
        ("What is a complex sentence?", "A sentence with one independent and at least one dependent clause", "A sentence with only one word", "A sentence with two independent clauses only", "A sentence without a predicate"),
        ("Identify the simple sentence.", "The children played outside.", "I called him, but he did not answer.", "Although it rained, we went out.", "She cooked while he cleaned."),
        ("Identify the compound sentence.", "I was tired, but I continued working.", "She sings beautifully.", "When he arrived, we left.", "Because it was late, I slept."),
        ("Identify the complex sentence.", "Although it was raining, we played.", "The baby is sleeping.", "He opened the door and entered.", "Ravi likes music."),
        ("What is an independent clause?", "A clause that expresses a complete thought", "A group of words without a subject", "A clause that cannot stand alone", "A phrase without a verb"),
        ("What is a dependent clause?", "A clause that cannot stand alone as a complete sentence", "A clause that expresses a complete thought", "A sentence without a subject", "A complete independent sentence"),
        ("Which conjunction commonly joins independent clauses?", "And", "Because", "Although", "Unless"),
        ("Identify the subject in: 'The little girl is reading a book.'", "The little girl", "Is reading", "A book", "Reading a book"),
        ("Identify the predicate in: 'The birds are singing.'", "Are singing", "The birds", "Birds", "The"),
        ("Which of these is a phrase?", "In the morning", "She is sleeping.", "They played football.", "He runs quickly."),
        ("Which of these is a complete sentence?", "The teacher explained the lesson.", "Because the teacher was late", "Under the table", "When the bell rang"),
        ("Which sentence contains a dependent clause?", "I stayed home because I was ill.", "She likes dancing.", "The dog barked.", "They play cricket."),
        ("Which word is a subordinating conjunction?", "Although", "And", "But", "Or"),
        ("Which word is a coordinating conjunction?", "But", "Because", "Although", "Unless"),
        ("Identify the compound sentence.", "She studied hard, and she passed the exam.", "She studied hard.", "Because she studied hard, she passed.", "After studying, she slept."),
        ("Identify the complex sentence.", "I smiled when I saw her.", "The sun is bright.", "He ran and jumped.", "They sang loudly."),
        ("How many independent clauses are there in a simple sentence?", "One", "Two", "Three", "None"),
        ("Which sentence has a subject and a verb?", "The cat sleeps.", "Under the bed", "Very beautiful", "After the rain"),
        ("Identify the dependent clause: 'I know that she is honest.'", "That she is honest", "I know", "She is honest", "I know that"),
        ("Which sentence begins with a dependent clause?", "When the rain stopped, we went outside.", "We went outside.", "The rain stopped.", "We enjoyed the weather."),
        ("Which sentence contains two independent clauses?", "He cooked dinner, and she washed the dishes.", "He cooked dinner.", "After dinner, he slept.", "Because he was hungry, he cooked."),
        ("A group of words that acts as a unit but lacks a complete subject-predicate structure is called a ___.", "Phrase", "Clause", "Paragraph", "Sentence"),
        ("Identify the sentence with the correct basic structure.", "The boy kicked the ball.", "The boy the ball kicked.", "Kicked the boy the ball.", "The ball the boy."),
        ("Which sentence contains a prepositional phrase?", "The book is on the table.", "The book is interesting.", "She reads books.", "They are happy."),
        ("Which sentence contains an adjective clause?", "The girl who won the prize is my friend.", "She won the prize.", "The girl is my friend.", "She is very talented."),
        ("Which sentence contains an adverb clause?", "I left when the meeting ended.", "I left early.", "The meeting ended.", "I attended the meeting."),
        ("What does a predicate tell us?", "Something about the subject", "The meaning of a conjunction", "The position of a punctuation mark", "The number of paragraphs")
    ],

    "Medium": [
        ("Identify the sentence pattern: 'The baby sleeps.'", "Subject + Verb", "Subject + Verb + Object", "Subject + Linking Verb + Complement", "Subject + Verb + Indirect Object + Direct Object"),
        ("Identify the sentence pattern: 'Riya reads novels.'", "Subject + Verb + Object", "Subject + Verb", "Subject + Linking Verb + Complement", "Subject + Verb + Adverb"),
        ("Identify the sentence pattern: 'The sky became dark.'", "Subject + Linking Verb + Complement", "Subject + Verb + Object", "Subject + Verb", "Subject + Verb + Indirect Object + Direct Object"),
        ("Identify the sentence pattern: 'She gave her brother a gift.'", "Subject + Verb + Indirect Object + Direct Object", "Subject + Verb", "Subject + Linking Verb + Complement", "Subject + Verb + Object + Object Complement"),
        ("Identify the sentence pattern: 'They elected him captain.'", "Subject + Verb + Object + Object Complement", "Subject + Verb", "Subject + Verb + Indirect Object + Direct Object", "Subject + Linking Verb + Complement"),
        ("Which sentence is compound-complex?", "Although it was late, we continued working, and the manager stayed with us.", "The manager stayed late.", "We continued working, and the manager stayed.", "Although it was late, we continued working."),
        ("Which sentence is a compound sentence joined by a semicolon?", "The sun had set; the streets were still busy.", "The sun had set because it was evening.", "The sun had set.", "When the sun had set, we returned."),
        ("Identify the independent clause: 'Although she was tired, she completed the assignment.'", "She completed the assignment.", "Although she was tired", "Although she was", "Was tired"),
        ("Identify the noun clause: 'I believe that he is innocent.'", "That he is innocent", "I believe", "He is innocent", "That he is"),
        ("Identify the adjective clause: 'The book that you gave me is interesting.'", "That you gave me", "The book", "Is interesting", "You gave me"),
        ("Identify the adverb clause: 'She smiled because she was happy.'", "Because she was happy", "She smiled", "She was happy", "Because she was"),
        ("Which sentence contains a relative clause?", "The man who lives next door is a doctor.", "The man is a doctor.", "He lives next door.", "The doctor is friendly."),
        ("Which sentence contains an infinitive phrase?", "She wants to learn French.", "She learns French.", "She is learning French.", "She learned French yesterday."),
        ("Which sentence contains a gerund phrase?", "Swimming in the sea is enjoyable.", "She swims every morning.", "She is swimming now.", "She swam yesterday."),
        ("Which sentence contains a participial phrase?", "Exhausted by the journey, the travellers rested.", "The travellers rested.", "The travellers were exhausted.", "They completed the journey."),
        ("Which sentence has a compound subject?", "Ravi and Priya attended the seminar.", "Ravi attended the seminar.", "Ravi attended and spoke.", "The seminar was interesting."),
        ("Which sentence has a compound predicate?", "The child laughed and clapped.", "The child and his mother laughed.", "The child was happy.", "The child laughed loudly."),
        ("Which sentence is grammatically incomplete?", "Because the train was delayed.", "The train was delayed.", "We waited for the train.", "The train arrived late."),
        ("Which sentence correctly combines the ideas using a subordinating conjunction?", "I stayed inside because it was raining.", "I stayed inside, and because it was raining.", "Because it was raining, but I stayed inside.", "I stayed inside, or it was raining."),
        ("Which sentence uses a coordinating conjunction correctly?", "She wanted to go, but she was busy.", "Although she was busy, but she went.", "Because she was busy, and she stayed.", "She wanted but to go."),
        ("Which sentence contains an essential adjective clause?", "The student who studies regularly usually performs well.", "The student, who is my neighbour, studies regularly.", "My neighbour is a student.", "The student studies regularly."),
        ("Which sentence contains an adverb clause of condition?", "If you practise daily, you will improve.", "Because you practised, you improved.", "Although you practised, you struggled.", "When you practise, you improve."),
        ("Which sentence contains an adverb clause of concession?", "Although he was tired, he continued working.", "He continued working because he was interested.", "He worked until midnight.", "He worked so that he could finish."),
        ("Which sentence contains an adverb clause of purpose?", "She spoke slowly so that everyone could understand.", "She spoke slowly because she was tired.", "She spoke slowly when the teacher arrived.", "Although she was nervous, she spoke."),
        ("Which sentence contains an adverb clause of time?", "I will call you when I reach home.", "I will call you because I need help.", "I will call you if I am free.", "I will call you so that you know."),
        ("Which sentence is complex rather than compound?", "Since it was cold, we stayed indoors.", "It was cold, so we stayed indoors.", "It was cold, and we stayed indoors.", "It was cold; we stayed indoors."),
        ("Which sentence contains a direct object?", "She bought a new laptop.", "She is intelligent.", "The baby slept peacefully.", "He became a doctor."),
        ("Which sentence contains a subject complement?", "My sister is an engineer.", "My sister built a house.", "My sister reads books.", "My sister gave me a book."),
        ("Which sentence contains an object complement?", "They painted the wall blue.", "They painted the wall.", "The wall is blue.", "The wall looks beautiful."),
        ("Which sentence contains an indirect object?", "He sent his friend a letter.", "He sent a letter yesterday.", "He wrote carefully.", "He is a writer.")
    ],

    "Hard": [
        ("Identify the sentence type: 'The committee approved the plan, but the director requested changes.'", "Compound", "Simple", "Complex", "Compound-complex"),
        ("Identify the sentence type: 'Although the weather was poor, the players continued, and the spectators cheered.'", "Compound-complex", "Simple", "Compound", "Complex"),
        ("Identify the sentence type: 'Having completed the project, she submitted the report.'", "Simple", "Compound", "Complex", "Compound-complex"),
        ("Identify the sentence type: 'I know that he is honest and that he works hard.'", "Complex", "Simple", "Compound", "Compound-complex"),
        ("Identify the sentence type: 'The bell rang, and the students left after the teacher dismissed them.'", "Compound-complex", "Simple", "Compound", "Complex"),
        ("Which sentence contains a noun clause functioning as the subject?", "What he decided remains unclear.", "I know what he decided.", "She explained what happened.", "We discussed what he decided."),
        ("Which sentence contains a noun clause functioning as the direct object?", "She explained why she was late.", "Why she was late remains unclear.", "The reason is that she was late.", "The girl who was late apologised."),
        ("Identify the sentence with a non-defining relative clause.", "My brother, who lives in Delhi, is visiting us.", "The student who topped the class received a medal.", "People who exercise regularly stay fit.", "The book that I borrowed is useful."),
        ("Which sentence contains a defining relative clause?", "The car that he purchased is electric.", "My car, which is electric, is new.", "Delhi, which is the capital of India, is crowded.", "My sister, who is a doctor, lives here."),
        ("Which sentence contains a reduced relative clause?", "The documents submitted yesterday are missing.", "The documents that were submitted yesterday are missing.", "The documents are missing.", "The documents were submitted yesterday."),
        ("Identify the dangling modifier.", "Walking to college, the rain started suddenly.", "Walking to college, I met my friend.", "After finishing the work, she went home.", "Having eaten dinner, they watched television."),
        ("Which sentence has a misplaced modifier?", "She almost drove her children to school every day.", "She drove her children to school every day.", "She drove almost all her children to school.", "She drove her children to school safely."),
        ("Which sentence has parallel structure?", "She enjoys reading, writing, and painting.", "She enjoys reading, to write, and painting.", "She enjoys to read, writing, and to paint.", "She enjoys reading, to write, and to paint."),
        ("Which sentence contains a subordinate clause functioning as an adjective?", "The house that stands on the hill is old.", "I know that the house is old.", "When the house was built, it was new.", "The house is old and beautiful."),
        ("Which sentence contains an adverb clause modifying an adjective?", "She was happy because she had succeeded.", "She smiled because she had succeeded.", "Because she succeeded, she celebrated.", "She succeeded and celebrated."),
        ("Which sentence contains an appositive phrase?", "My friend, a skilled musician, performed tonight.", "My friend performed tonight.", "My friend is a musician.", "My friend performed skillfully."),
        ("Which sentence contains an absolute phrase?", "The meeting over, everyone left the room.", "After the meeting, everyone left.", "Everyone left the meeting.", "When the meeting ended, everyone left."),
        ("Which sentence contains a participial phrase modifying the subject?", "Covered in dust, the old chair stood in the corner.", "The old chair was covered in dust.", "Dust covered the old chair.", "The chair stood in the corner."),
        ("Which sentence contains a gerund phrase functioning as the subject?", "Learning a new language requires patience.", "She is learning a new language.", "She wants to learn a new language.", "She learned a new language."),
        ("Which sentence contains an infinitive phrase functioning as an adjective?", "She has a book to read.", "She wants to read a book.", "To read regularly is beneficial.", "She reads to improve her vocabulary."),
        ("Which sentence contains a subject complement rather than a direct object?", "The soup tastes delicious.", "She tasted the soup.", "She prepared the soup.", "She served the soup."),
        ("Which sentence contains a ditransitive verb?", "The teacher gave the students homework.", "The teacher explained the lesson.", "The teacher arrived early.", "The teacher became famous."),
        ("Which sentence contains a complex transitive structure?", "They considered him reliable.", "They considered the proposal.", "They arrived early.", "They became successful."),
        ("Which sentence contains a prepositional phrase acting as an adjective?", "The girl with the red bag is my cousin.", "The girl walked quickly.", "The girl is happy.", "The girl smiled brightly."),
        ("Which sentence contains a prepositional phrase acting as an adverb?", "She placed the keys on the table.", "The keys on the table are mine.", "The table is wooden.", "The keys are missing."),
        ("Which sentence has an embedded interrogative clause?", "I wonder whether she will attend.", "Will she attend?", "Attend the meeting.", "She will attend the meeting."),
        ("Which sentence contains a conditional subordinate clause?", "Unless you hurry, you will miss the bus.", "You hurried and caught the bus.", "You missed the bus because you were late.", "You caught the bus after running."),
        ("Which sentence contains an adverb clause of result?", "He was so tired that he fell asleep immediately.", "He slept because he was tired.", "Although he was tired, he continued.", "He slept when he became tired."),
        ("Which sentence contains a correlative conjunction joining parallel elements?", "She is both intelligent and hardworking.", "She is intelligent but works hard.", "She is intelligent because she studies.", "She is intelligent, although she is quiet."),
        ("Which sentence is structurally parallel and grammatically correct?", "The role requires planning, organising, and communicating.", "The role requires planning, to organise, and communicating.", "The role requires to plan, organising, and to communicate.", "The role requires planning, organisation, and to communicate.")
    ]
}


def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Sentence Structure", "English")
        )
        row = cur.fetchone()

        if not row:
            raise Exception(
                "Lesson 'Sentence Structure' with topic 'English' was not found."
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
                    (lesson_id, f"Sentence Structure - {difficulty}", difficulty)
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
        print("\nSUCCESS: Sentence Structure has exactly 90 questions!")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
