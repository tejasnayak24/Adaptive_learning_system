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
        ("In which year did the Revolt of 1857 begin?", "1857", "1757", "1885", "1947", "A"),
        ("Where did the Revolt of 1857 begin among sepoys?", "Meerut", "Bombay", "Madras", "Calcutta", "A"),
        ("On which date did the sepoys at Meerut revolt in 1857?", "10 May 1857", "15 August 1857", "26 January 1857", "1 January 1858", "A"),
        ("Who was declared the symbolic emperor by the rebels in Delhi?", "Bahadur Shah Zafar", "Akbar II", "Shah Alam I", "Aurangzeb", "A"),
        ("Who was the queen of Jhansi associated with the revolt?", "Rani Lakshmibai", "Rani Durgavati", "Ahilyabai Holkar", "Razia Sultan", "A"),
        ("Who led the revolt in Kanpur?", "Nana Sahib", "Kunwar Singh", "Begum Hazrat Mahal", "Mangal Pandey", "A"),
        ("Who was an important leader of the revolt in Bihar?", "Kunwar Singh", "Nana Sahib", "Tantia Tope", "Bahadur Shah Zafar", "A"),
        ("Who led resistance in Lucknow and Awadh?", "Begum Hazrat Mahal", "Rani Lakshmibai", "Sarojini Naidu", "Annie Besant", "A"),
        ("Who was Mangal Pandey?", "A sepoy associated with the events leading to the revolt", "The British Governor-General in 1857", "The Mughal emperor", "The ruler of Jhansi", "A"),
        ("Which company controlled large parts of India before the revolt?", "East India Company", "Dutch East India Company alone", "French Republic", "United Nations", "A"),
        ("What was a sepoy?", "An Indian soldier serving in the army of the East India Company", "A village tax collector only", "A British governor", "A royal poet", "A"),
        ("Which policy allowed the British to annex certain kingdoms when a ruler lacked a recognised natural male heir?", "Doctrine of Lapse", "Subsidiary Alliance only", "Permanent Settlement", "Ryotwari system", "A"),
        ("Which Governor-General is associated with the Doctrine of Lapse?", "Lord Dalhousie", "Lord Mountbatten", "Lord Curzon", "Lord Ripon", "A"),
        ("Which kingdom was annexed by the British in 1856 before the revolt?", "Awadh", "Mysore", "Travancore", "Kashmir", "A"),
        ("What was one immediate trigger of the sepoy anger in 1857?", "The controversy over the new rifle cartridges", "The introduction of railways alone", "The opening of universities alone", "The abolition of the Mughal Empire in 1947", "A"),
        ("Why were the rifle cartridges controversial?", "Sepoys believed their grease could involve cow and pig fat", "They were made entirely of gold", "They could not be used in rifles", "They were imported from Japan", "A"),
        ("Which animal was sacred to many Hindus and associated with the cartridge controversy?", "Cow", "Camel", "Horse", "Elephant", "A"),
        ("Which animal was considered unclean by many Muslims and associated with the cartridge controversy?", "Pig", "Camel", "Horse", "Elephant", "A"),
        ("What happened to the East India Company after the revolt?", "Its rule ended and the British Crown took direct control in 1858", "It became the government of independent India", "It gained control of all Europe", "It was renamed the Mughal Empire", "A"),
        ("Who became the first Viceroy of India after the transfer of power to the Crown?", "Lord Canning", "Lord Dalhousie", "Lord Curzon", "Lord Wellesley", "A"),
        ("Which city was an important centre of the revolt associated with Bahadur Shah Zafar?", "Delhi", "Pondicherry", "Cochin", "Shimla only", "A"),
        ("What was one important centre of resistance led by Rani Lakshmibai?", "Jhansi", "Surat", "Calicut", "Dacca", "A"),
        ("What was one major British response to the revolt?", "Military suppression and severe punishment of rebels", "Immediate independence for India", "Abolition of the British Crown", "Transfer of power to the Indian National Congress", "A"),
        ("What was the broad political result of the revolt for India?", "The end of East India Company rule", "The beginning of Mughal rule", "The creation of the Indian Republic", "The end of British influence in 1857", "A"),
        ("Which group formed an important part of the early uprising?", "Indian sepoys in Company service", "Only European merchants", "Only British parliamentarians", "Only foreign sailors", "A"),
        ("What was the capital city of the Mughal Empire that became a rebel centre in 1857?", "Delhi", "Chennai", "Pune", "Hyderabad in Sindh", "A"),
        ("Who was Tantia Tope?", "A military leader associated with the revolt", "A British Prime Minister", "The founder of the East India Company", "The last Viceroy of India", "A"),
        ("What does the term 'annexation' mean?", "Taking control of a territory and incorporating it into another state", "Giving a territory complete independence", "Holding a village festival", "Building a railway station", "A"),
        ("Why is the Revolt of 1857 important in Indian history?", "It was a major uprising against East India Company rule", "It established the Indian Constitution", "It ended the British Raj in 1947", "It began the Maurya Empire", "A"),
        ("What happened to Bahadur Shah Zafar after the revolt was suppressed?", "He was exiled to Rangoon", "He became the first President of India", "He returned to rule the whole subcontinent", "He founded the Indian National Congress", "A"),
    ],

    "Medium": [
        ("Why did many sepoys become dissatisfied with Company rule?", "Military grievances combined with fears about religion, service conditions and British policies", "They were all guaranteed promotions", "The Company had abolished every military rule", "They wanted to establish a modern parliament immediately", "A"),
        ("Why did the cartridge issue become such a powerful trigger?", "It raised fears that religious practices and beliefs were being disrespected", "It immediately ended land revenue collection", "It involved the construction of a new capital", "It had no connection to military service", "A"),
        ("How did the Doctrine of Lapse contribute to resentment?", "It enabled annexations that displaced ruling families and their supporters", "It gave every ruler complete independence", "It abolished British authority", "It ended all land taxes", "A"),
        ("Why did the annexation of Awadh create discontent?", "It displaced the ruler and affected nobles, soldiers and other groups connected to the kingdom", "It gave all residents equal political representation", "It ended the East India Company", "It created an independent republic", "A"),
        ("Why did some dispossessed rulers and nobles support the revolt?", "British expansion threatened their political power, status and income", "They were all employed by the British Crown", "They had no connection to regional politics", "They wanted to introduce modern railways", "A"),
        ("What role did Bahadur Shah Zafar play in the revolt?", "He became a symbolic figure around whom some rebels rallied", "He commanded every rebel force personally", "He founded the East India Company", "He served as the British Prime Minister", "A"),
        ("Why did the revolt spread beyond Meerut and Delhi?", "Existing grievances and local political conditions encouraged uprisings in several regions", "Every region had identical goals and leadership", "The British army had already left India", "The revolt was organised by a modern national parliament", "A"),
        ("How did Rani Lakshmibai become associated with the revolt?", "She resisted British authority and led forces connected with the defence of Jhansi", "She served as Governor-General", "She led the revolt in Bengal only", "She founded the Indian National Congress", "A"),
        ("What was Nana Sahib's connection to the revolt?", "He became a leading figure in the uprising at Kanpur", "He was the last Mughal emperor", "He was the British commander at Meerut", "He introduced the Doctrine of Lapse", "A"),
        ("Why is Kunwar Singh remembered in the history of 1857?", "He led resistance against British rule in Bihar despite his advanced age", "He ruled Jhansi as queen", "He served as Governor-General", "He wrote the Indian Constitution", "A"),
        ("What role did Begum Hazrat Mahal play?", "She became a prominent leader of resistance in Awadh", "She founded the Mughal Empire", "She led the British army at Panipat", "She was the first Viceroy of India", "A"),
        ("Why is it difficult to describe the revolt as a fully unified national movement?", "Participants and regions had varied aims, leadership and levels of involvement", "No Indian participated in it", "Every rebel followed one central command", "The revolt took place only outside India", "A"),
        ("Which statement best describes the geographical spread of the revolt?", "Major centres included Delhi, Kanpur, Lucknow, Jhansi and parts of Bihar", "It was equally intense in every Indian region", "It occurred only in southern coastal towns", "It was confined to one military barrack", "A"),
        ("Why did the British suppress the revolt in the end?", "They used military reinforcements, resources and divisions among opposing forces", "All British troops immediately surrendered", "The rebels controlled every major port permanently", "The East India Company abolished its army before fighting began", "A"),
        ("What changed in India's administration after 1858?", "The British Crown assumed direct rule from the East India Company", "India immediately became independent", "The Mughal Empire was restored permanently", "All princely states were abolished immediately", "A"),
        ("What did the British government promise in the 1858 proclamation?", "It announced changes in governance and assurances concerning religious non-interference and princely states", "It granted immediate universal independence", "It restored the East India Company to power", "It created the Indian Constitution", "A"),
        ("How did British policy toward princely states change after 1857?", "The British became more cautious about annexation and increasingly sought princely loyalty", "All princely states were immediately annexed", "Princely rulers were required to establish republics", "The Doctrine of Lapse was expanded without change", "A"),
        ("How did the British reorganise the army after the revolt?", "They changed recruitment and military organisation to reduce the risk of another uprising", "They disbanded every regiment permanently", "They allowed sepoys to elect the Viceroy", "They ended all military recruitment in India", "A"),
        ("Why did the British become more cautious about religious and social reforms after 1857?", "They feared that perceived interference in religious customs could contribute to unrest", "They abolished all religions", "They ended all administrative activity", "They transferred authority to the rebels", "A"),
        ("What was one economic grievance among sections of Indian society before the revolt?", "British policies and revenue demands could threaten livelihoods and established interests", "Every farmer received a guaranteed salary", "The Company abolished all taxes", "Trade and landholding were unaffected everywhere", "A"),
        ("Why did the revolt not achieve its immediate aim of ending British rule?", "The rebels lacked unified coordination and faced the military and resource advantages of the British", "The rebels had no grievances", "The British had no soldiers in India", "Every Indian region joined the revolt with one strategy", "A"),
        ("What was the significance of the fall of Delhi to British forces?", "It weakened a major rebel centre and ended Bahadur Shah Zafar's role as a symbolic emperor", "It established the Indian Republic", "It restored the East India Company permanently", "It ended all British rule in India", "A"),
        ("Why should the term 'sepoy revolt' not be the only description used for 1857?", "Civilian groups, dispossessed rulers and other participants also joined in some regions", "No sepoys participated", "Only British officials took part", "The uprising had no political context", "A"),
        ("Why do historians use different names for the events of 1857?", "They interpret its participants, geographic reach and political meaning differently", "There is no evidence that the events happened", "All historians agree on one official title", "The revolt was outside recorded history", "A"),
        ("What does the participation of local leaders suggest about the revolt?", "Regional grievances and political circumstances shaped resistance", "Every participant had exactly the same goal", "The revolt was controlled by one modern political party", "Local conditions were irrelevant", "A"),
        ("What was one consequence for the Mughal dynasty?", "The dynasty ended as Bahadur Shah Zafar was exiled after the uprising", "It expanded to rule all of Europe", "It regained permanent control of India", "It founded the British Crown", "A"),
        ("How did the revolt affect the East India Company?", "The Company lost its governing role in India", "It became the first elected Indian government", "It gained control of the Mughal court", "It remained the direct ruler until 1947", "A"),
        ("Why is the Revolt of 1857 often considered a turning point?", "It led to major changes in British administration, military policy and relations with Indian rulers", "It created the United Nations", "It introduced universal adult suffrage in India", "It ended every princely state", "A"),
        ("What is a balanced way to study the causes of the revolt?", "Examine military, political, economic and religious concerns together", "Attribute it entirely to one cartridge issue", "Ignore the annexation of kingdoms", "Assume every region had identical causes", "A"),
        ("What does the varied participation across India reveal?", "The uprising was widespread in some regions but limited or absent in others", "Every region participated equally", "No regional differences existed", "The revolt happened only in London", "A"),
    ],

    "Hard": [
        ("Which interpretation best explains the origins of the Revolt of 1857?", "A combination of military grievances, annexation policies, economic pressures and fears about social and religious interference", "A single cause explains every event in every region", "It began as a movement for modern internet access", "It had no connection to Company rule", "A"),
        ("Why should the cartridge controversy be understood as a trigger rather than the only cause?", "It intensified existing grievances among sepoys and other groups", "It occurred after British rule ended", "It had no religious significance", "It was unrelated to military service", "A"),
        ("How did the Doctrine of Lapse undermine some ruling families?", "It allowed annexation in certain succession situations and threatened dynastic claims", "It guaranteed succession to every adopted heir", "It transferred power to elected village councils", "It ended all British territorial expansion", "A"),
        ("Why was the annexation of Awadh particularly consequential?", "It affected the ruler, court elites, landholders and people linked to the kingdom's political and military structures", "It affected only British merchants", "It had no impact beyond the royal palace", "It immediately ended Company rule", "A"),
        ("Which statement best characterises the leadership of the revolt?", "Leadership was distributed among prominent regional figures rather than unified under one effective central command", "One commander controlled every region throughout", "The British led the rebel forces", "No identifiable leaders emerged", "A"),
        ("Why did Bahadur Shah Zafar's symbolic role matter despite his limited practical power?", "His Mughal status offered a recognised symbol around which some rebels could rally", "He commanded all British troops", "He controlled modern communication networks", "He had founded the East India Company", "A"),
        ("How did the revolt expose weaknesses in the East India Company's rule?", "It revealed the risks of military discontent, political annexation and alienation of influential groups", "It proved that every Indian group supported the Company", "It eliminated all military conflict", "It showed that annexation caused no resentment", "A"),
        ("Why is it inaccurate to assume the revolt was equally strong throughout India?", "Its intensity depended on local grievances, leadership, military presence and regional political conditions", "Every province had identical political conditions", "The revolt was restricted to one person", "No regional leaders participated", "A"),
        ("What is a major historiographical issue in calling 1857 the First War of Independence?", "The label highlights anti-colonial resistance but can obscure the varied aims and participation of different groups", "It means the events occurred after independence in 1947", "It proves all participants had identical nationalist ideas", "It denies that any British rule existed", "A"),
        ("Why do some accounts describe 1857 as a sepoy mutiny?", "The uprising began among Company soldiers, though it later involved wider civilian and political participation in some areas", "No soldiers took part", "The event happened entirely in Britain", "The term proves there were no civilian participants", "A"),
        ("How did regional political grievances shape the revolt?", "Displaced rulers and their supporters sometimes used the uprising to challenge British expansion", "Every ruler supported British annexation", "Political grievances were absent in Awadh and Jhansi", "All regional leaders sought identical constitutional reforms", "A"),
        ("What can the participation of peasants and townspeople in some areas indicate?", "The uprising could draw on local social and economic grievances as well as military discontent", "Every participant was a Company soldier", "Economic conditions never influenced resistance", "The revolt was unrelated to local society", "A"),
        ("Why did British military superiority and reinforcements matter?", "They helped the British recapture strategic centres and suppress rebel forces", "The British had no access to weapons", "Rebel forces controlled every supply route", "Military resources played no role in the outcome", "A"),
        ("What was a major administrative consequence of the Government of India Act 1858?", "The transfer of governing authority from the East India Company to the British Crown", "The immediate creation of an independent India", "The restoration of Mughal rule", "The abolition of the British monarchy", "A"),
        ("How did the 1858 proclamation affect the relationship between the Crown and Indian princes?", "It offered assurances and encouraged princely loyalty under British paramountcy", "It granted every prince complete sovereignty over all India", "It abolished all princely states immediately", "It restored the Doctrine of Lapse without modification", "A"),
        ("Why did British army recruitment policy change after 1857?", "British authorities sought to reorganise forces and reduce the likelihood of coordinated rebellion", "They ended all recruitment permanently", "They allowed soldiers to elect the monarch", "They abolished military service across the empire", "A"),
        ("What was one longer-term effect of the revolt on British attitudes toward social reform?", "Officials became more cautious about reforms perceived as interference in religious and social practices", "The British ended all administration in India", "Every reform was immediately abolished", "India became independent in 1858", "A"),
        ("Why is the economic dimension of the revolt important?", "Revenue policies and changing political-economic relationships contributed to dissatisfaction among some groups", "Economic conditions were identical for all people", "The Company collected no revenue", "The uprising took place without any social context", "A"),
        ("How should historians use accounts written by British officials about 1857?", "Critically, considering their perspective and comparing them with Indian and other sources", "As entirely neutral records without bias", "As proof that no Indian resistance occurred", "Without comparing any other evidence", "A"),
        ("Why are local proclamations, letters and memories useful for studying the revolt?", "They can reveal regional concerns and perspectives that official records may underrepresent", "They always provide a complete and unbiased account", "They have no connection to historical interpretation", "They replace all other evidence automatically", "A"),
        ("What was the significance of the British recapture of Delhi?", "It removed a major rebel centre and enabled the exile of the last Mughal emperor", "It established the Mughal Empire for another century", "It led to immediate Indian independence", "It restored the East India Company as sovereign ruler", "A"),
        ("Why did the revolt fail to create a lasting unified alternative government?", "The rebels had diverse objectives, uneven coordination and limited common military organisation", "All rebels refused to fight", "The British immediately supported the rebels", "Every region had a single agreed constitution", "A"),
        ("What is the most accurate way to assess the role of Rani Lakshmibai?", "She became a prominent regional military leader whose resistance formed part of the wider uprising", "She led all rebel armies across India", "She served as the British Viceroy", "She founded the East India Company", "A"),
        ("Why is Kunwar Singh's participation historically notable?", "It demonstrates that resistance also emerged among influential leaders in Bihar", "It proves the revolt was confined to Delhi", "He served as Governor-General of India", "He was the ruler of the Mughal Empire", "A"),
        ("How did the end of Mughal rule affect the political symbolism of the revolt?", "The exile of Bahadur Shah Zafar marked the final end of the Mughal dynasty's imperial role", "The Mughal Empire expanded across India", "The dynasty became the British Parliament", "It led to the restoration of the Delhi Sultanate", "A"),
        ("Which approach best distinguishes immediate outcomes from long-term consequences?", "Separate the military defeat of the uprising from subsequent changes in governance and colonial policy", "Assume defeat meant nothing changed", "Treat the revolt as the end of all colonial rule", "Ignore changes after 1858", "A"),
        ("Why should the events of 1857 be understood in their regional contexts?", "Different communities experienced British policies and participated in resistance in different ways", "Every region had the same leadership and goals", "Local histories have no relevance", "The uprising had no connection to regional politics", "A"),
        ("What does the revolt reveal about colonial rule?", "Policies that threatened established interests and beliefs could generate broad and varied resistance", "Colonial policies never created grievances", "All groups supported colonial expansion", "Military organisation had no political significance", "A"),
        ("Why is it important to distinguish a movement's later meaning from every participant's original motivation?", "Later national interpretations may differ from the varied aims held by participants at the time", "All participants always share one ideology", "Historical interpretations never change", "Original motivations cannot be studied", "A"),
        ("Which summary best captures the historical significance of 1857?", "A major but uneven uprising that ended Company rule and transformed British governance in India", "A minor event with no administrative consequences", "The event that created the Indian Republic in 1857", "A revolt that immediately ended all British power", "A"),
    ],
}


def main():
    db = SessionLocal()
    total_added = 0

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "The Revolt of 1857",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if not lesson:
            print("ERROR: Lesson 'The Revolt of 1857' was not found.")
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
            print("SUCCESS: The Revolt of 1857 has all 90 questions!")
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