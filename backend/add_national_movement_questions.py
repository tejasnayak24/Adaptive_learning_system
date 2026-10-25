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
        ("Who is widely known as the Father of the Nation in India?", "Mahatma Gandhi", "Subhas Chandra Bose", "Bhagat Singh", "Bal Gangadhar Tilak", "A"),
        ("In which year did the Indian Revolt of 1857 take place?", "1857", "1885", "1905", "1942", "A"),
        ("Which organisation was founded in 1885 to represent Indian political interests?", "Indian National Congress", "Muslim League", "Forward Bloc", "Swaraj Party", "A"),
        ("Who led the Salt March in 1930?", "Mahatma Gandhi", "Jawaharlal Nehru", "Sardar Patel", "Dadabhai Naoroji", "A"),
        ("What was the main aim of India's freedom struggle?", "To end British colonial rule", "To expand British control", "To establish a European colony", "To end all education", "A"),
        ("Who gave the slogan 'Give me blood, and I shall give you freedom'?", "Subhas Chandra Bose", "Mahatma Gandhi", "Gopal Krishna Gokhale", "Lord Curzon", "A"),
        ("Which movement began in 1942 demanding an end to British rule?", "Quit India Movement", "Swadeshi Movement", "Khilafat Movement", "Home Rule Movement", "A"),
        ("Who was popularly called Netaji?", "Subhas Chandra Bose", "Bhagat Singh", "B. R. Ambedkar", "Rajendra Prasad", "A"),
        ("Which method was central to Gandhi's freedom struggle?", "Non-violent resistance", "Armed conquest of other countries", "Military rule", "Colonial expansion", "A"),
        ("What does the term 'Swadeshi' encourage?", "Using goods made in one's own country", "Buying only imported goods", "Avoiding all local industries", "Stopping domestic production", "A"),
        ("Who was a prominent leader of the Indian National Congress and an advocate of self-rule?", "Bal Gangadhar Tilak", "Lord Mountbatten", "Robert Clive", "Lord Dalhousie", "A"),
        ("Which British policy partitioned Bengal in 1905?", "Partition of Bengal", "Permanent Settlement", "Doctrine of Lapse", "Subsidiary Alliance", "A"),
        ("Who was one of the prominent leaders of the Dandi March?", "Mahatma Gandhi", "Lord Curzon", "Lord Wellesley", "Warren Hastings", "A"),
        ("What was the purpose of the Non-Cooperation Movement?", "To withdraw cooperation from British institutions and authority", "To strengthen colonial rule", "To support British imports exclusively", "To end Indian political participation", "A"),
        ("Who was popularly known as the Iron Man of India?", "Sardar Vallabhbhai Patel", "Jawaharlal Nehru", "Bhagat Singh", "Lala Lajpat Rai", "A"),
        ("Which freedom fighter was executed in 1931 along with Rajguru and Sukhdev?", "Bhagat Singh", "Mahatma Gandhi", "Dadabhai Naoroji", "C. Rajagopalachari", "A"),
        ("What was the principal objective of the Swadeshi Movement?", "Promoting Indian goods and boycotting foreign goods", "Promoting colonial imports", "Ending Indian handicrafts", "Supporting the partition of India", "A"),
        ("Who became the first Prime Minister of independent India?", "Jawaharlal Nehru", "Sardar Patel", "Rajendra Prasad", "Lal Bahadur Shastri", "A"),
        ("On which date did India become independent?", "15 August 1947", "26 January 1950", "2 October 1947", "9 August 1942", "A"),
        ("Which event in 1919 involved British troops firing on a gathering in Amritsar?", "Jallianwala Bagh massacre", "Dandi March", "Chauri Chaura incident", "Bardoli Satyagraha", "A"),
        ("Who was a prominent leader of the Home Rule Movement in India?", "Annie Besant", "Lord Curzon", "Lord Ripon", "Robert Clive", "A"),
        ("What does 'Purna Swaraj' mean?", "Complete independence", "Limited taxation", "British partnership", "Provincial trade", "A"),
        ("Which movement encouraged Indians to boycott British goods and institutions?", "Non-Cooperation Movement", "Green Revolution", "White Revolution", "Chipko Movement", "A"),
        ("Who was known as the Grand Old Man of India?", "Dadabhai Naoroji", "Bhagat Singh", "Subhas Chandra Bose", "Mangal Pandey", "A"),
        ("Which leader is closely associated with the slogan 'Swaraj is my birthright and I shall have it'?", "Bal Gangadhar Tilak", "Lord Curzon", "Lord Canning", "Lord Dalhousie", "A"),
        ("What was the Indian National Army associated with?", "Subhas Chandra Bose and the struggle against British rule", "The expansion of the British Empire", "The establishment of the East India Company", "The partition of Bengal in 1905", "A"),
        ("Who was a prominent woman leader in India's freedom movement?", "Sarojini Naidu", "Queen Victoria", "Lady Curzon", "Lord Mountbatten", "A"),
        ("What was the main purpose of the Salt March?", "To protest the British salt tax and monopoly", "To promote British salt imports", "To support a new land tax", "To protest the introduction of railways", "A"),
        ("Which leader was associated with the Bardoli Satyagraha?", "Sardar Vallabhbhai Patel", "Lord Mountbatten", "Robert Clive", "Warren Hastings", "A"),
        ("What did Indian nationalists seek through the freedom movement?", "Self-government and independence", "Permanent foreign rule", "The end of Indian political rights", "The restoration of East India Company rule", "A"),
    ],

    "Medium": [
        ("Why did the Indian National Congress initially use petitions and resolutions?", "It sought political reforms and greater Indian participation through constitutional methods", "It intended to end all political discussion", "It wanted to restore East India Company rule", "It opposed every form of education", "A"),
        ("What was an important consequence of the Partition of Bengal in 1905?", "It strengthened Swadeshi and boycott activities", "It immediately ended British rule", "It created the Indian Constitution", "It began the Quit India Movement", "A"),
        ("Why did Gandhi launch the Non-Cooperation Movement?", "To challenge colonial authority through mass non-cooperation", "To increase cooperation with colonial institutions", "To support the permanent partition of Bengal", "To establish British military rule", "A"),
        ("Why did Gandhi withdraw the Non-Cooperation Movement in 1922?", "The Chauri Chaura incident involved violence", "India became independent that year", "The Salt March had already succeeded", "The Simon Commission granted complete independence", "A"),
        ("What was the significance of the Dandi March?", "It challenged the British salt laws through civil disobedience", "It established the Indian National Congress", "It ended the Revolt of 1857", "It introduced the Government of India Act of 1935", "A"),
        ("Why was the Jallianwala Bagh massacre a turning point?", "It intensified opposition to British colonial rule", "It ended all nationalist activity", "It immediately granted complete independence", "It led to the founding of the East India Company", "A"),
        ("What was the main aim of the Home Rule Movement?", "To demand self-government for India", "To expand British rule in Asia", "To abolish all political organisations", "To support the partition of Bengal", "A"),
        ("Why did nationalists promote Swadeshi goods?", "To strengthen Indian industries and challenge economic dependence on Britain", "To make India more dependent on imports", "To stop all domestic manufacturing", "To increase British control over local trade", "A"),
        ("What was the importance of the Lahore Congress session of 1929?", "The Congress declared Purna Swaraj as its goal", "India became a republic", "The Quit India Movement began", "The Indian National Army was founded", "A"),
        ("Why did the Civil Disobedience Movement challenge colonial laws?", "It aimed to oppose unjust laws through deliberate non-violent defiance", "It aimed to strengthen every colonial tax", "It sought to end public participation", "It promoted compulsory British imports", "A"),
        ("What was one contribution of women to the freedom movement?", "They participated in protests, marches, boycotts, and political organising", "They were completely absent from nationalist activities", "They alone signed the independence transfer", "They replaced all political organisations", "A"),
        ("What was the role of newspapers in the freedom struggle?", "They spread nationalist ideas and criticised colonial policies", "They were used only for entertainment", "They prevented political awareness", "They replaced all public meetings", "A"),
        ("Why did the Simon Commission face protests in India?", "It had no Indian member", "It declared India independent", "It abolished British rule immediately", "It introduced universal independence in 1905", "A"),
        ("What was a major objective of the Quit India Movement?", "Demanding an end to British rule in India", "Demanding the return of East India Company rule", "Supporting the continuation of colonial rule", "Establishing British rule over Southeast Asia", "A"),
        ("How did the economic critique of colonialism contribute to nationalism?", "It highlighted the drain of Indian wealth and colonial economic exploitation", "It proved colonial rule had no economic effects", "It discouraged all Indian industries", "It ended public discussion about taxation", "A"),
        ("What was the importance of the Khilafat Movement in the early 1920s?", "It helped bring some Muslim political leaders into a period of cooperation with the Non-Cooperation Movement", "It immediately created the Indian Constitution", "It ended the First World War", "It established the Indian National Army", "A"),
        ("Why was the Indian National Army historically significant?", "It represented an armed challenge to British rule and influenced nationalist sentiment", "It governed India after 1857", "It introduced the Permanent Settlement", "It led the Salt March", "A"),
        ("What was the main purpose of the Rowlatt Act of 1919?", "It expanded colonial powers to detain and restrict people without ordinary trial safeguards", "It granted India complete independence", "It abolished all colonial policing", "It established universal adult franchise", "A"),
        ("How did the participation of peasants and workers affect the freedom struggle?", "It broadened nationalism beyond a limited group of political leaders", "It made the movement exclusively urban", "It ended all mass mobilisation", "It removed economic issues from politics", "A"),
        ("What was the significance of the Karachi Congress session of 1931?", "It adopted resolutions on fundamental rights and economic policy", "It declared India a republic in 1931", "It launched the Quit India Movement", "It created the East India Company", "A"),
        ("Why did some revolutionaries adopt armed resistance?", "They believed revolutionary action could challenge colonial power", "They wanted to strengthen every colonial law", "They opposed all forms of Indian independence", "They sought to end all political organisation", "A"),
        ("What was the importance of the Bardoli Satyagraha of 1928?", "It challenged increased land revenue and strengthened Patel's leadership", "It established British rule in Bengal", "It launched the Dandi March", "It ended the Revolt of 1857", "A"),
        ("How did the First World War affect Indian nationalism?", "Economic pressures and political expectations contributed to growing discontent", "It immediately made India independent", "It eliminated all taxes in India", "It ended the Indian National Congress", "A"),
        ("Why did the demand for complete independence grow stronger during the freedom struggle?", "Many nationalists became dissatisfied with limited reforms under colonial rule", "British rule had already ended in 1905", "All Indians rejected self-government", "The Constitution was adopted in 1919", "A"),
        ("What was one result of the Round Table Conferences?", "They formed part of negotiations over constitutional reforms in British India", "They immediately transferred power in 1929", "They began the Revolt of 1857", "They introduced the Salt March", "A"),
        ("Why was mass mobilisation important to the independence movement?", "It involved wider sections of society in challenging colonial rule", "It restricted the movement to a few officials", "It removed all public participation", "It made political communication unnecessary", "A"),
        ("What was the role of Subhas Chandra Bose in the freedom struggle?", "He led the Indian National Army and sought to end British rule", "He led the Dandi March", "He introduced the Rowlatt Act", "He served as the first Viceroy of India", "A"),
        ("Why did the British government introduce constitutional reforms at different points?", "It responded partly to political pressure while attempting to manage colonial governance", "It granted complete independence in 1905", "It abolished every British institution immediately", "It ended all nationalist demands", "A"),
        ("What was the significance of the 1942 movement?", "It intensified the demand for immediate British withdrawal", "It began the Indian National Congress", "It introduced the Permanent Settlement", "It created the Mughal Empire", "A"),
        ("What helped make independence a mass political goal?", "Long-term organising, popular protests, political negotiations, and diverse forms of resistance", "One isolated event with no earlier background", "The end of all public meetings", "A complete absence of political organisations", "A"),
    ],

    "Hard": [
        ("How did the methods of early Congress leaders differ from those of later mass movements?", "Early leaders relied heavily on petitions, while later movements used broader mass mobilisation and civil disobedience", "Early leaders used only armed rebellion and later leaders used only petitions", "Both rejected all political participation", "Later movements sought to strengthen colonial rule", "A"),
        ("Why did the Swadeshi Movement have economic as well as political significance?", "Boycotting foreign goods aimed to challenge colonial authority and encourage Indian production", "It sought to eliminate all Indian industries", "It was designed to increase dependence on British imports", "It immediately established a republic", "A"),
        ("How did the Rowlatt Act affect Gandhi's political strategy?", "It helped prompt nationwide protest and broadened opposition to colonial repression", "It ended Gandhi's political activity before 1919", "It granted universal independence", "It established the Indian National Army", "A"),
        ("Why was the withdrawal of the Non-Cooperation Movement debated among nationalists?", "Some questioned ending a mass campaign after violence, while others supported Gandhi's emphasis on non-violence", "All nationalists agreed that colonial rule should continue", "The movement had already achieved independence", "The decision abolished the Congress permanently", "A"),
        ("What did the Salt March demonstrate about civil disobedience?", "A simple everyday issue could mobilise people against an unjust colonial law", "Only wealthy landowners could participate in nationalism", "British salt laws were never challenged", "Civil disobedience required support for every colonial policy", "A"),
        ("How did economic arguments strengthen Indian nationalism?", "They connected colonial rule with poverty, resource extraction, and obstacles to Indian industry", "They argued that colonial rule had no economic consequences", "They discouraged analysis of trade and taxation", "They proved that Indian production should stop", "A"),
        ("Why is the freedom struggle best understood as a movement involving diverse groups and methods?", "Different communities, regions, ideologies, and strategies contributed to the challenge to colonial rule", "Only one person participated throughout the entire struggle", "All participants used identical methods", "No workers, peasants, or women participated", "A"),
        ("What was the political significance of declaring Purna Swaraj in 1929?", "It made complete independence the Congress's explicit objective", "It transferred power to India that same year", "It introduced the Constitution in 1950", "It ended the Second World War", "A"),
        ("How did the participation of women challenge existing social expectations?", "It expanded women's visible roles in public protest and political activity", "It removed women from every public activity", "It ended the need for political organisation", "It prevented women from joining demonstrations", "A"),
        ("Why did the Quit India Movement continue to matter despite widespread arrests of leaders?", "Local activists and popular resistance continued in many places despite repression", "It immediately produced a signed transfer of power in August 1942", "It ended all nationalist sentiment", "It restored East India Company rule", "A"),
        ("What was a key difference between constitutional negotiation and revolutionary resistance?", "They represented different strategies for challenging colonial authority", "They both required complete support for British rule", "Neither involved political goals", "They were identical in methods and organisation", "A"),
        ("How did the Jallianwala Bagh massacre affect the legitimacy of British rule among many Indians?", "It intensified criticism of colonial repression and weakened trust in British claims of just governance", "It ended all opposition to colonial rule", "It granted India independence immediately", "It established the Mughal Empire", "A"),
        ("Why was the Indian National Army's impact not limited to battlefield outcomes?", "Its activities and subsequent public response influenced nationalist feeling and debates about British control", "It independently wrote the Constitution in 1947", "It introduced the Permanent Settlement", "It ended the Revolt of 1857", "A"),
        ("How did colonial economic policies contribute to nationalist criticism?", "Critics argued that taxation, trade patterns, and resource extraction disadvantaged Indian economic development", "They were considered unrelated to public welfare", "They eliminated all Indian agricultural activity", "They guaranteed equal wealth for all Indians", "A"),
        ("What is the historical importance of the 1931 Karachi Congress session?", "It linked the national movement with stated commitments to civil liberties and socioeconomic principles", "It transferred power in 1931", "It launched the 1942 Quit India Movement", "It founded the East India Company", "A"),
        ("Why did negotiations with the British government remain part of the independence struggle?", "Leaders pursued constitutional and political routes alongside public mobilisation", "All nationalist leaders rejected any negotiation", "Negotiations had already made India independent in 1905", "Negotiations removed the need for public participation", "A"),
        ("How did the Home Rule Movement contribute to nationalism?", "It popularised demands for self-government before the major Gandhian mass movements", "It called for permanent colonial rule", "It began after Indian independence", "It abolished political campaigning", "A"),
        ("Why should the freedom struggle not be reduced to a single leader or event?", "Independence resulted from decades of varied campaigns, contributions, and political developments", "One event alone explains every development", "Only British officials contributed to nationalism", "No organisation or popular action mattered", "A"),
        ("What does the growth of mass movements reveal about Indian nationalism?", "Nationalist politics increasingly reached people beyond elite political circles", "Political activity became limited to colonial administrators", "Public participation completely disappeared", "Nationalism rejected all local issues", "A"),
        ("How did revolutionary nationalists differ from advocates of non-violent resistance?", "They differed over methods and strategy while opposing colonial rule", "They all sought to preserve British colonial authority", "They had no political objectives", "They used exactly the same tactics in every campaign", "A"),
        ("Why did the partition of Bengal become a major nationalist issue?", "Many Indians viewed it as a divisive colonial policy and organised opposition", "It granted complete independence", "It ended the British Empire in India immediately", "It created the Indian Constitution", "A"),
        ("What was the significance of the slogan 'Do or Die' in 1942?", "It conveyed the urgency of the Quit India demand", "It was the slogan of the Dandi March in 1930", "It called for permanent British rule", "It marked the founding of the Congress in 1885", "A"),
        ("How did newspapers and public meetings support nationalist mobilisation?", "They circulated ideas, communicated grievances, and encouraged political discussion", "They replaced all forms of political activity", "They were used only for colonial advertisements", "They prevented public awareness", "A"),
        ("Why did the participation of peasants make agrarian grievances important to nationalism?", "Local issues such as rent and land revenue connected colonial rule with everyday economic hardship", "Peasants never raised economic concerns", "Agrarian issues were unrelated to politics", "All land revenue was abolished in 1857", "A"),
        ("What can be inferred from the range of movements between Swadeshi and Quit India?", "Nationalist strategies changed over time in response to political conditions and public experience", "The movement followed one unchanging method", "India became independent in 1905", "No new political demands emerged", "A"),
        ("Why is the 1946 naval uprising relevant to the final phase of British rule?", "It reflected unrest within sections of the armed forces during a period of wider political uncertainty", "It began the Indian National Congress", "It introduced the Salt March", "It ended the Revolt of 1857", "A"),
        ("What was one broader consequence of the INA trials after the Second World War?", "They stimulated public sympathy and debate about British authority", "They immediately created the Republic of India", "They restored the East India Company", "They began the Partition of Bengal in 1905", "A"),
        ("How did Gandhi's emphasis on non-violence shape mass political action?", "It promoted disciplined collective protest and civil disobedience as political methods", "It required citizens to support every colonial law", "It prohibited all forms of public mobilisation", "It ended all political negotiation", "A"),
        ("What is the strongest explanation for the eventual end of British rule in India?", "A combination of mass nationalism, political negotiation, economic pressures, and changing post-war conditions", "One isolated protest with no wider context", "The absence of Indian political organisations", "A decision unrelated to events in India", "A"),
        ("Why is the Indian freedom struggle important to the study of democracy?", "It highlights collective action, political rights, self-government, and debates over how power should be exercised", "It demonstrates that public participation is unnecessary", "It established that colonial rule is permanent", "It shows that political rights have no value", "A"),
    ],
}


def main():
    db = SessionLocal()
    added = 0

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "The National Movement",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if not lesson:
            print("ERROR: The National Movement lesson was not found.")
            print("Check the lesson title and topic in the database.")
            return

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

            for item in questions:
                if len(existing) >= 30:
                    break

                question_text, a, b, c, d, correct_letter = item

                if question_text.strip().lower() in existing_texts:
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

                existing_texts.add(question_text.strip().lower())
                existing.append(None)
                added += 1

        db.commit()

        print("\nFINAL VERIFICATION")
        total = 0

        for difficulty in QUESTION_BANK:
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

            total += count
            print(f"{difficulty}: {count}/30")

        print(f"TOTAL: {total}/90")
        print(f"New questions added: {added}")

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()