import os
import random
import logging
from pathlib import Path

logging.disable(logging.CRITICAL)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "adaptive_learning.db"
os.environ["DATABASE_URL"] = f"sqlite:///{DATABASE_PATH.as_posix()}"

from app.database.connection import SessionLocal
from app.models.student import Student
from app.models.lesson import Lesson
from app.models.quiz import Quiz
from app.models.question import Question
from app.models.progress import Progress
from app.models.session import LearningSession
from app.models.reward import RewardHistory


QUESTION_BANK = {
    "Easy": [
        ("In which year was the Indian National Congress founded?", "1885", "1857", "1905", "1947", "A"),
        ("Who is commonly associated with the founding of the Indian National Congress?", "A. O. Hume", "Lord Mountbatten", "Lord Dalhousie", "Robert Clive", "A"),
        ("Who was known as the Father of the Nation in India?", "Mahatma Gandhi", "Jawaharlal Nehru", "Subhas Chandra Bose", "Sardar Patel", "A"),
        ("In which year did Gandhi return to India from South Africa?", "1915", "1905", "1920", "1930", "A"),
        ("Which movement began in 1920 under Gandhi's leadership?", "Non-Cooperation Movement", "Quit India Movement", "Civil Disobedience Movement", "Swadeshi Movement of 1905", "A"),
        ("In which year did the Jallianwala Bagh massacre occur?", "1919", "1905", "1930", "1942", "A"),
        ("Who led the Dandi March in 1930?", "Mahatma Gandhi", "Bhagat Singh", "Subhas Chandra Bose", "Bal Gangadhar Tilak", "A"),
        ("What did Gandhi protest against during the Dandi March?", "The British salt tax and salt laws", "The railway timetable", "The partition of Bengal in 1905 only", "The formation of the United Nations", "A"),
        ("In which year was the Quit India Movement launched?", "1942", "1919", "1930", "1947", "A"),
        ("What slogan is associated with the Quit India Movement?", "Do or Die", "Jai Jawan Jai Kisan", "Inquilab Zindabad only", "Garibi Hatao", "A"),
        ("Who was popularly known as Netaji?", "Subhas Chandra Bose", "Jawaharlal Nehru", "Dadabhai Naoroji", "Gopal Krishna Gokhale", "A"),
        ("What was the Indian National Army associated with?", "Subhas Chandra Bose", "Lord Curzon", "Robert Clive", "Lord Wellesley", "A"),
        ("Who was known as the Iron Man of India?", "Sardar Vallabhbhai Patel", "Bhagat Singh", "Mahatma Gandhi", "Lala Lajpat Rai", "A"),
        ("Who was a prominent leader of the Indian independence movement and India's first Prime Minister?", "Jawaharlal Nehru", "Lord Mountbatten", "Lord Dalhousie", "Warren Hastings", "A"),
        ("Who was one of the leading revolutionaries associated with the Hindustan Socialist Republican Association?", "Bhagat Singh", "Lord Ripon", "Lord Curzon", "A. O. Hume", "A"),
        ("In which year was Bengal partitioned by the British under Lord Curzon?", "1905", "1885", "1919", "1942", "A"),
        ("Which movement encouraged the boycott of British goods after the partition of Bengal?", "Swadeshi Movement", "Quit India Movement", "Khilafat Movement only", "Champaran Movement", "A"),
        ("What does 'swadeshi' broadly mean?", "Using goods produced within one's own country", "Buying only imported goods", "Refusing all agricultural products", "Supporting colonial taxation", "A"),
        ("Who was popularly known as Lokmanya?", "Bal Gangadhar Tilak", "Sardar Patel", "Mahatma Gandhi", "C. Rajagopalachari", "A"),
        ("Who gave the slogan 'Inquilab Zindabad' its association with revolutionary nationalism?", "Bhagat Singh and other revolutionaries popularised it", "Lord Curzon", "Robert Clive", "Lord Mountbatten", "A"),
        ("Who was the first woman president of the Indian National Congress?", "Annie Besant", "Sarojini Naidu", "Indira Gandhi", "Rani Lakshmibai", "A"),
        ("Who was the first Indian woman president of the Indian National Congress?", "Sarojini Naidu", "Annie Besant", "Vijaya Lakshmi Pandit", "Kasturba Gandhi", "A"),
        ("What was the main goal of India's freedom struggle?", "Ending British colonial rule and achieving independence", "Expanding British control", "Restoring the East India Company", "Establishing a European empire", "A"),
        ("On which date did India become independent?", "15 August 1947", "26 January 1950", "2 October 1947", "15 August 1942", "A"),
        ("Who was the last Viceroy of British India?", "Lord Mountbatten", "Lord Curzon", "Lord Dalhousie", "Lord Canning", "A"),
        ("Who was associated with the Champaran Satyagraha of 1917?", "Mahatma Gandhi", "Subhas Chandra Bose", "Bhagat Singh", "Sardar Patel", "A"),
        ("What was satyagraha based on?", "Non-violent resistance and the pursuit of truth", "Armed conquest only", "Economic isolation from every country", "Military rule", "A"),
        ("Who was a prominent leader of the Home Rule Movement in India?", "Annie Besant", "Lord Mountbatten", "Robert Clive", "Warren Hastings", "A"),
        ("Which event led to widespread anger after British troops fired on a gathering in Amritsar in 1919?", "Jallianwala Bagh massacre", "Dandi March", "Quit India Movement", "Cabinet Mission", "A"),
        ("What happened to British rule in India in August 1947?", "India became independent, and partition created India and Pakistan", "The East India Company began ruling India", "The Mughal Empire was founded", "The Indian National Congress was established", "A"),
    ],

    "Medium": [
        ("Why was the Indian National Congress formed in 1885?", "It provided a political platform for discussing Indian concerns and seeking reforms", "It was established to strengthen the East India Company", "It was created to oppose all education", "It was founded after independence", "A"),
        ("What distinguished many early Congress leaders known as Moderates?", "They generally used petitions, discussions and constitutional methods to seek reforms", "They relied exclusively on armed rebellion", "They rejected every form of political discussion", "They supported permanent British rule without reforms", "A"),
        ("Why did the partition of Bengal in 1905 provoke opposition?", "Many Indians viewed it as a political measure that divided people and weakened nationalist unity", "It immediately granted India independence", "It ended all British administration", "It abolished every provincial boundary", "A"),
        ("What was an important aim of the Swadeshi Movement?", "Promoting Indian goods and boycotting British goods", "Increasing dependence on imported British goods", "Ending Indian manufacturing", "Supporting the permanent partition of India", "A"),
        ("Why was the Jallianwala Bagh massacre a turning point for many Indians?", "It intensified anger against colonial repression and weakened trust in British rule", "It immediately ended British rule", "It established the Indian Constitution", "It created the Indian National Congress", "A"),
        ("What was the purpose of the Non-Cooperation Movement?", "To withdraw cooperation from British institutions and authority through non-violent protest", "To expand British military recruitment", "To restore the East India Company", "To support every colonial law", "A"),
        ("Why did Gandhi suspend the Non-Cooperation Movement in 1922?", "The Chauri Chaura incident involved violence that conflicted with his commitment to non-violence", "India had already become independent", "The British abolished all taxes", "The Dandi March had already succeeded", "A"),
        ("What made the Dandi March important?", "It turned opposition to the salt laws into a highly visible act of civil disobedience", "It established the Indian National Congress", "It ended the Mughal Empire", "It was a military invasion of Britain", "A"),
        ("What was the main principle of the Civil Disobedience Movement?", "Openly and non-violently breaking selected colonial laws", "Following every colonial law without protest", "Replacing elections with military rule", "Ending all Indian-made products", "A"),
        ("Why did the Simon Commission face protests in India?", "It had no Indian members", "It granted independence immediately", "It was created by the Indian National Congress", "It abolished British rule", "A"),
        ("What was the significance of the Lahore session of the Congress in 1929?", "The Congress adopted the goal of Purna Swaraj or complete independence", "India became independent at the session", "The East India Company was founded", "The Quit India Movement was launched", "A"),
        ("Why was 26 January 1930 significant for the independence movement?", "It was observed as Independence Day following the declaration of Purna Swaraj", "It was the date of the Jallianwala Bagh massacre", "It marked the beginning of the Mughal Empire", "It was the date of the Dandi March's completion", "A"),
        ("What was the main demand associated with the Quit India Movement?", "An end to British rule in India", "The return of the East India Company", "The permanent expansion of colonial rule", "The restoration of the Delhi Sultanate", "A"),
        ("Why did the Quit India Movement face severe repression?", "British authorities arrested leaders and used force to suppress protests", "The British government supported immediate independence", "The movement took place only outside India", "There were no public demonstrations", "A"),
        ("What was Subhas Chandra Bose's approach to the independence struggle?", "He pursued a more militant strategy and sought international support against British rule", "He opposed independence", "He served as the last Viceroy", "He founded the East India Company", "A"),
        ("What was the purpose of the Indian National Army?", "To fight British rule with the goal of India's independence", "To protect the British Crown from Indian independence activists", "To establish the Mughal Empire", "To administer the Indian Constitution", "A"),
        ("How did the Home Rule Movement contribute to nationalism?", "It campaigned for self-government within the British Empire", "It demanded the restoration of Company rule", "It opposed all political participation", "It began after India became a republic", "A"),
        ("Why was the Khilafat Movement important to the wider nationalist context?", "It helped create a period of cooperation between some Muslim leaders and the broader non-cooperation campaign", "It established British rule in India", "It was a military campaign led by Lord Curzon", "It ended all nationalist activity", "A"),
        ("What role did women play in India's freedom struggle?", "They participated in protests, boycotts, organising and other forms of resistance", "They were entirely absent from the movement", "They only served in British government offices", "They were prohibited from every public activity", "A"),
        ("Why was the participation of students and workers significant?", "It broadened the social base of nationalist protest", "It restricted the movement to colonial officials", "It ended all public participation", "It prevented regional movements", "A"),
        ("What was one important contribution of revolutionary nationalists?", "They challenged colonial rule through militant actions and political writings", "They introduced British rule to India", "They rejected Indian independence", "They created the modern British Parliament", "A"),
        ("Why is it important to distinguish the different strands of the freedom struggle?", "Nationalists used varied strategies, including constitutional politics, mass movements and revolutionary action", "Every leader followed exactly the same strategy", "Only one individual participated", "There were no disagreements within the movement", "A"),
        ("What was the purpose of the Cabinet Mission Plan of 1946?", "To propose a framework for transferring power and forming a constitutional arrangement", "To establish the East India Company", "To begin the Revolt of 1857", "To introduce the Doctrine of Lapse", "A"),
        ("What was the Mountbatten Plan of 1947 associated with?", "The transfer of power and partition of British India", "The founding of the Indian National Congress", "The launch of the Non-Cooperation Movement", "The beginning of British rule in Bengal", "A"),
        ("Why was partition a major consequence of independence in 1947?", "British India was divided into India and Pakistan amid large-scale displacement and violence", "It ended all population movement", "It restored the Mughal Empire", "It created a single undivided state", "A"),
        ("What was the role of Sardar Vallabhbhai Patel after independence?", "He played a major role in integrating many princely states into the Indian Union", "He served as the last Mughal emperor", "He led the Dandi March", "He founded the East India Company", "A"),
        ("Why did the freedom struggle involve economic boycotts?", "Boycotts aimed to challenge colonial economic interests and promote Indian production", "They were intended to eliminate Indian industries", "They were designed to expand British imports", "They ended every form of trade permanently", "A"),
        ("What was the importance of newspapers and political literature in nationalism?", "They spread ideas, criticised colonial policies and helped mobilise public opinion", "They prevented all political communication", "They were used only for weather reports", "They replaced every public meeting", "A"),
        ("Why was the freedom struggle not limited to major cities?", "Protests and political activity also developed in towns, villages and different regions", "Every village remained completely uninvolved", "Only British officials participated", "The movement took place outside India only", "A"),
        ("What is a balanced interpretation of India's independence in 1947?", "It resulted from prolonged political mobilisation, varied resistance and changing historical circumstances", "It resulted from one event alone", "It occurred without Indian participation", "It ended every social and political challenge", "A"),
    ],

    "Hard": [
        ("Which explanation best accounts for the growth of Indian nationalism?", "Political exclusion, economic grievances, new communication networks and organised movements all contributed", "A single event explains every stage of nationalism", "Nationalism developed without any social or political context", "It was created only after independence", "A"),
        ("Why did early Moderate leaders favour constitutional methods?", "They believed petitions, public debate and institutional reform could advance Indian political demands", "They controlled a national army", "They wanted to end all political discussion", "They opposed every form of reform", "A"),
        ("How did the Swadeshi Movement change nationalist politics?", "It connected political protest with economic self-reliance and the boycott of foreign goods", "It ended Indian manufacturing", "It established the Republic of India", "It eliminated public participation", "A"),
        ("Why did the Jallianwala Bagh massacre have consequences beyond Amritsar?", "News of the massacre intensified criticism of colonial authority across India", "It immediately transferred power to Indian leaders", "It ended all British military activity", "It created the Mughal Empire", "A"),
        ("What does the suspension of the Non-Cooperation Movement in 1922 reveal about Gandhi's strategy?", "He prioritised non-violence even when this meant halting a major political campaign", "He abandoned Indian independence permanently", "He supported violence as the only method", "He became the British Viceroy", "A"),
        ("How did the Dandi March turn a local act into a national campaign?", "It used a widely understood grievance to inspire civil disobedience across different regions", "It restricted protest to one village permanently", "It replaced all political organisations", "It immediately ended colonial rule", "A"),
        ("Why was the declaration of Purna Swaraj in 1929 historically important?", "It made complete independence the Congress's stated objective rather than limiting demands to reforms", "It created the East India Company", "It ended the Revolt of 1857", "It established British parliamentary rule in India", "A"),
        ("What is the key difference between non-cooperation and civil disobedience?", "Non-cooperation withdraws support from institutions, while civil disobedience can involve openly breaking specific laws", "Both terms mean supporting every colonial policy", "Civil disobedience excludes all forms of protest", "Non-cooperation requires military conquest", "A"),
        ("Why did the Simon Commission provoke nationalist opposition?", "Its lack of Indian membership reinforced objections to Indians being excluded from decisions about their political future", "It offered immediate complete independence", "It was composed entirely of Indian nationalists", "It abolished the British Parliament", "A"),
        ("How did the Quit India Movement differ from earlier campaigns?", "Its 1942 demand called for an immediate end to British rule amid wartime conditions", "It was launched before the founding of the Congress", "It focused only on the salt tax in 1930", "It sought to restore Company rule", "A"),
        ("Why did British authorities arrest national leaders during the Quit India Movement?", "They sought to disrupt organised resistance and prevent challenges to colonial wartime control", "They wanted to transfer power immediately", "They were enforcing India's post-independence Constitution", "They had no interest in suppressing protest", "A"),
        ("What did Subhas Chandra Bose's strategy demonstrate about the independence movement?", "Some nationalists pursued international alliances and armed struggle alongside other approaches", "All nationalists rejected every form of military action", "The movement had one universally accepted strategy", "Bose supported permanent British rule", "A"),
        ("Why should the Indian National Army's contribution be assessed in a broader context?", "Its military campaign, public response and influence on debates about the armed forces all matter to historical interpretation", "It single-handedly defeated every British force", "It had no connection to the independence movement", "It was formed after the Indian Constitution", "A"),
        ("How did the participation of women challenge established social expectations?", "Women entered public protest and political organising in ways that expanded participation in nationalist activity", "Women were completely absent from every campaign", "Participation had no social significance", "Women led the British Parliament", "A"),
        ("Why is the freedom struggle best understood as a mass movement with diverse participants?", "Different classes, communities, regions and organisations contributed through different forms of political action", "Every participant shared identical motives", "Only one city participated", "There were no regional differences", "A"),
        ("What is the historical importance of the Home Rule Movement?", "It popularised demands for self-government and expanded organised nationalist activity", "It established British rule in 1858", "It ended all political organisation", "It began after independence", "A"),
        ("Why did the Khilafat and Non-Cooperation movements overlap for a period?", "Shared opposition to aspects of British policy created an opportunity for cooperation among some political groups", "They had identical aims in every respect", "Neither movement opposed British policy", "They were both launched after 1947", "A"),
        ("How did revolutionary nationalists differ from constitutional Moderates in their methods?", "Some revolutionaries supported militant action, while Moderates generally emphasised petitions and constitutional reform", "All revolutionaries served as British officials", "Moderates always led armed rebellions", "There was no difference in political strategy", "A"),
        ("Why is it important not to reduce independence to the actions of one leader?", "The outcome involved multiple leaders, organisations, public participation and changing political circumstances", "Only one individual ever opposed British rule", "Mass movements had no effect", "Independence occurred without political organisation", "A"),
        ("What was the significance of the Cabinet Mission Plan in 1946?", "It attempted to negotiate a constitutional framework and the transfer of power amid political disagreements", "It began the Revolt of 1857", "It established the East India Company", "It ended the Indian National Congress", "A"),
        ("Why did negotiations over the transfer of power become increasingly urgent after the Second World War?", "Political pressure, Britain's post-war circumstances and disputes over India's constitutional future intensified", "Britain had no political or economic difficulties", "Indian nationalism had disappeared", "The Mughal Empire had returned", "A"),
        ("What was the political significance of the Mountbatten Plan?", "It set out the approach to transferring power and partitioning British India", "It established the Mughal Empire", "It launched the Swadeshi Movement", "It introduced the Doctrine of Lapse", "A"),
        ("Why must the achievement of independence be considered alongside partition?", "Freedom from colonial rule coincided with division, displacement, violence and major social upheaval", "Partition had no effect on people", "Independence occurred without any territorial changes", "Partition created the East India Company", "A"),
        ("How did economic nationalism support the independence struggle?", "Boycotts and support for indigenous products challenged colonial economic relationships and promoted self-reliance", "It encouraged dependence on imported goods only", "It eliminated every Indian industry", "It rejected all economic activity", "A"),
        ("What role did print culture play in political mobilisation?", "Newspapers and pamphlets circulated arguments, reported events and helped connect political campaigns", "Print culture prevented the spread of political ideas", "Only government notices were printed", "It replaced every form of public participation", "A"),
        ("Why should historians distinguish a movement's stated goals from its actual outcomes?", "Political campaigns may produce unintended effects and achieve only some of their objectives", "Stated goals always guarantee complete success", "Outcomes are irrelevant to history", "Every campaign achieves all its aims immediately", "A"),
        ("What does the long duration of the freedom struggle demonstrate?", "Indian independence developed through changing strategies, organisations and political circumstances over decades", "It was completed in a single day in 1885", "No political change occurred before 1947", "All movements followed one fixed plan", "A"),
        ("How did the integration of princely states relate to the post-independence challenge?", "Political independence required building a functioning union from British Indian provinces and princely states", "Every princely state had already joined a single elected government before 1947", "Integration meant restoring Company rule", "The task was unrelated to state formation", "A"),
        ("Which approach gives the most balanced account of the freedom struggle?", "Examine mass movements, constitutional politics, revolutionary action, social participation and negotiations together", "Study only one battle", "Focus exclusively on one leader's speeches", "Ignore regional and social participation", "A"),
        ("Which statement best summarises India's freedom struggle?", "A long and diverse anti-colonial struggle culminated in independence in 1947, alongside the trauma of partition", "It was a short event without public participation", "It began only after independence", "It ended with the restoration of Company rule", "A"),
    ],
}


def main():
    db = SessionLocal()
    total_added = 0

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "India's Freedom Struggle",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if not lesson:
            print("ERROR: Lesson 'India's Freedom Struggle' was not found.")
            print("Check the exact lesson title and topic in the database.")
            return

        print(f"Lesson found: {lesson.title}")
        print(f"Subject: {lesson.topic}")
        print("-" * 55)

        for difficulty, questions in QUESTION_BANK.items():
            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.difficulty == difficulty,
                )
                .first()
            )

            if not quiz:
                quiz = Quiz(
                    lesson_id=lesson.id,
                    title=f"{lesson.title} - {difficulty}",
                    difficulty=difficulty,
                )
                db.add(quiz)
                db.flush()

            existing = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .all()
            )

            if len(existing) >= 30:
                print(f"{difficulty}: already has {len(existing)} questions; skipped.")
                continue

            existing_texts = {q.question.strip().lower() for q in existing}
            added_this_level = 0

            for item in questions:
                if len(existing) + added_this_level >= 30:
                    break

                question_text, a, b, c, d, correct_letter = item
                normalized_text = question_text.strip().lower()

                if normalized_text in existing_texts:
                    continue

                options = [a, b, c, d]
                correct_text = options[ord(correct_letter) - ord("A")]
                random.shuffle(options)
                new_correct_letter = "ABCD"[options.index(correct_text)]

                db.add(
                    Question(
                        quiz_id=quiz.id,
                        question=question_text,
                        option_a=options[0],
                        option_b=options[1],
                        option_c=options[2],
                        option_d=options[3],
                        correct_answer=new_correct_letter,
                    )
                )

                existing_texts.add(normalized_text)
                added_this_level += 1

            total_added += added_this_level
            db.flush()
            print(f"{difficulty}: added {added_this_level} questions (target: 30).")

        db.commit()
        print("-" * 55)
        print(f"New questions added: {total_added}")

        print("\nFINAL VERIFICATION")
        final_total = 0

        for difficulty in ("Easy", "Medium", "Hard"):
            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.difficulty == difficulty,
                )
                .first()
            )

            count = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
                if quiz
                else 0
            )

            final_total += count
            print(f"{difficulty}: {count}/30")

        print(f"TOTAL: {final_total}/90")

        if final_total == 90:
            print("SUCCESS: India's Freedom Struggle has all 90 questions!")
        else:
            print("WARNING: The lesson does not yet have all 90 questions.")
            print("Check the counts before moving to the next lesson.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()