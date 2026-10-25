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
        ("What is a regional kingdom?", "A kingdom that ruled a particular region", "A modern international organisation", "A village school", "A type of coin", "A"),
        ("Which dynasty ruled much of the Deccan region during the medieval period?", "Rashtrakutas", "Mughals only", "Lodis only", "Mauryas only", "A"),
        ("Which dynasty was associated with the city of Kalyani in the Deccan?", "Western Chalukyas", "Lodis", "Sayyids", "Mamluks", "A"),
        ("Which dynasty ruled from Thanjavur and later had influence across southern India?", "Cholas", "Lodis", "Tughlaqs", "Sayyids", "A"),
        ("Which dynasty was associated with the Vijayanagara Empire?", "Sangama dynasty", "Lodi dynasty", "Mamluk dynasty", "Sayyid dynasty", "A"),
        ("Where was the Vijayanagara Empire mainly located?", "Southern India", "Northwestern Europe", "Central Asia", "Eastern Africa", "A"),
        ("Which city was the capital of the Vijayanagara Empire?", "Vijayanagara", "Delhi", "Lahore", "Patna", "A"),
        ("Which kingdom was associated with the city of Warangal?", "Kakatiya kingdom", "Lodi kingdom", "Mughal kingdom", "Sayyid kingdom", "A"),
        ("Which dynasty ruled the region around Madurai during parts of the medieval period?", "Pandyas", "Mamluks", "Lodis", "Sayyids", "A"),
        ("Which dynasty was famous for its maritime activities and temple architecture in southern India?", "Cholas", "Lodis", "Sayyids", "Mamluks", "A"),
        ("What was a common source of income for medieval regional kingdoms?", "Agricultural revenue", "Income tax on software", "Railway fares", "Airline tickets", "A"),
        ("What was a fort mainly used for?", "Defence and protection", "Growing crops", "Printing books", "Measuring rainfall", "A"),
        ("What was the role of a king's court?", "Administration and decision-making", "Operating modern railways", "Conducting national elections", "Managing the internet", "A"),
        ("What were inscriptions often used to record?", "Donations, victories and royal orders", "Modern election results", "Weather forecasts only", "Computer programmes", "A"),
        ("What is a dynasty?", "A succession of rulers from the same family or lineage", "A type of agricultural tool", "A trade tax", "A military building", "A"),
        ("Why were rivers important to many kingdoms?", "They supported agriculture, transport and settlements", "They prevented all farming", "They eliminated the need for water", "They were used only for royal ceremonies", "A"),
        ("What did merchants do in medieval kingdoms?", "Trade goods between regions and markets", "Only collect military taxes", "Rule every kingdom", "Construct every fort", "A"),
        ("What was the main purpose of temples in many medieval kingdoms?", "Religious worship and, in some cases, social and economic activities", "Modern parliamentary elections", "Operating railway stations", "Manufacturing computers", "A"),
        ("Which dynasty is associated with the famous Brihadeeswarar Temple at Thanjavur?", "Cholas", "Lodis", "Mamluks", "Sayyids", "A"),
        ("Which medieval empire is associated with Hampi?", "Vijayanagara Empire", "Maurya Empire", "Gupta Empire", "Lodi Sultanate", "A"),
        ("What is Hampi known for today?", "The remains of the historic Vijayanagara capital", "The capital of the Maurya Empire", "A modern Mughal capital", "The site of the First Battle of Panipat", "A"),
        ("What was a common reason kingdoms fought one another?", "Control over territory, resources and trade routes", "To eliminate all agriculture", "To establish modern airports", "To stop every form of trade permanently", "A"),
        ("What did irrigation systems help farmers do?", "Provide water to crops", "Build military weapons", "Write inscriptions", "Collect coins", "A"),
        ("What is a trade route?", "A path connecting places where goods are exchanged", "A royal family tree", "A temple ritual", "A type of fort wall", "A"),
        ("Which region is strongly associated with the Ahom kingdom?", "Assam", "Gujarat", "Kerala", "Rajasthan", "A"),
        ("Which kingdom became powerful in Bengal during the medieval period?", "Bengal Sultanate", "Chola Empire only", "Vijayanagara Empire only", "Kakatiya kingdom only", "A"),
        ("Which dynasty was associated with the region of Odisha and built the Konark Sun Temple?", "Eastern Ganga dynasty", "Lodi dynasty", "Mamluk dynasty", "Sayyid dynasty", "A"),
        ("What was the purpose of maintaining an army?", "To defend territory and support the ruler's authority", "To conduct farming only", "To manage modern schools", "To operate printing presses only", "A"),
        ("What can coins tell historians about regional kingdoms?", "Information about rulers, symbols and economic activity", "Every person's private thoughts", "Only modern weather conditions", "The exact population of every village", "A"),
        ("What happened to many regional kingdoms over time?", "Their power changed through alliances, conflicts and political developments", "They all ruled forever without change", "They all disappeared in the same year", "They never interacted with one another", "A"),
    ],

    "Medium": [
        ("Why did regional kingdoms emerge in different parts of India?", "Local powers gained control as political conditions and central authority changed", "All kingdoms were created by modern elections", "Agriculture disappeared across India", "There were no local rulers", "A"),
        ("How did agricultural revenue support regional kingdoms?", "It helped finance administration, armies and royal activities", "It replaced all forms of trade", "It was used only for modern transport", "It eliminated the need for officials", "A"),
        ("Why were river valleys attractive locations for kingdoms?", "They offered water, fertile land and transport opportunities", "They had no agricultural potential", "They prevented settlement", "They were always impossible to defend", "A"),
        ("Why did rulers construct forts?", "To defend strategic locations and protect political centres", "To eliminate the need for administration", "To stop all farming", "To replace every marketplace", "A"),
        ("How could control of a trade route strengthen a kingdom?", "It could increase revenue and influence over the movement of goods", "It guaranteed permanent peace", "It removed the need for agriculture", "It prevented merchants from travelling", "A"),
        ("Why were inscriptions important to medieval rulers?", "They publicised royal orders, donations and claims to authority", "They were used only as school textbooks", "They recorded modern census data", "They replaced all oral communication", "A"),
        ("What does temple construction often reveal about a ruler?", "Religious patronage, resources and claims to political prestige", "The exact income of every farmer", "The absence of artistic activity", "The introduction of modern elections", "A"),
        ("How did the Cholas support agriculture in parts of southern India?", "Through irrigation works and management of water resources", "By banning all cultivation", "By replacing rivers with roads", "By ending village settlement", "A"),
        ("Why was the Chola navy historically significant?", "It supported maritime activity and campaigns across the Bay of Bengal region", "It was the first modern air force", "It operated railways across Europe", "It ended all overseas trade", "A"),
        ("What was the importance of village assemblies in parts of Chola territory?", "They participated in certain local administrative and community affairs", "They elected the emperor through universal suffrage", "They controlled every kingdom in India", "They had no relationship with local administration", "A"),
        ("Why did the Vijayanagara rulers build and maintain a strong military?", "To protect their territories and compete with neighbouring powers", "To eliminate all regional trade", "To abolish their capital city", "To replace farming with mining", "A"),
        ("Why was Hampi an important city under Vijayanagara?", "It was an imperial centre with political, religious and commercial significance", "It was the capital of the Lodi dynasty", "It was founded by the British in 1858", "It was a port on the Arabian Sea", "A"),
        ("What was one reason for conflict between Vijayanagara and the Deccan Sultanates?", "Competition over territory, strategic places and political influence", "Competition over modern oil pipelines", "Disputes about parliamentary elections", "The complete absence of shared borders", "A"),
        ("What was the significance of the Battle of Talikota in 1565?", "The Vijayanagara forces suffered a major defeat against a coalition of Deccan Sultanates", "Babur defeated Ibrahim Lodi", "The British defeated the Marathas in 1818", "The Delhi Sultanate was founded", "A"),
        ("What happened to Vijayanagara after the Battle of Talikota?", "Its capital suffered major destruction, although successor powers continued in the region", "Every southern kingdom immediately disappeared", "The Mughal Empire ended permanently", "The Chola Empire was founded", "A"),
        ("Why did the Kakatiya kingdom value control over Warangal?", "Warangal was an important political centre in the eastern Deccan", "It was the capital of the Cholas", "It was a European trading port", "It was the Mughal capital under Shah Jahan", "A"),
        ("How did the Ahom kingdom maintain its position in Assam?", "Through regional administration, military organisation and adaptation to local conditions", "By ruling all of India from Delhi", "By abolishing agriculture", "By relying only on overseas merchants", "A"),
        ("Why did regional kingdoms form alliances?", "Alliances could strengthen security or help counter rival powers", "Alliances always eliminated every disagreement", "Alliances removed the need for rulers", "Alliances prevented all economic activity", "A"),
        ("How could marriage alliances influence medieval politics?", "They could strengthen relationships between ruling families", "They automatically transferred every kingdom to foreign rule", "They replaced all military activity", "They were used only to collect agricultural data", "A"),
        ("Why was a kingdom's army often linked to its revenue system?", "Maintaining troops required reliable resources and supplies", "Armies never needed food or equipment", "Revenue was unrelated to government", "Soldiers were always unpaid volunteers", "A"),
        ("What can regional coinage reveal about political authority?", "Rulers used coins to circulate currency and sometimes communicate royal identity", "It records every private conversation", "It provides complete weather records", "It proves every ruler controlled all of India", "A"),
        ("Why should historians compare inscriptions with other sources?", "Different sources may provide complementary or conflicting evidence", "Every inscription contains a complete history", "Inscriptions are always false", "Other evidence has no historical value", "A"),
        ("How did merchants contribute to the growth of towns?", "Their trade supported markets, crafts and connections between regions", "They prevented all urban growth", "They replaced every agricultural worker", "They controlled every royal succession", "A"),
        ("Why could a kingdom's prosperity depend on agricultural conditions?", "Harvests affected food supply, rural livelihoods and revenue collection", "Agriculture had no economic role", "Rainfall never affected crops", "Kings collected no revenue from rural areas", "A"),
        ("What role could local chiefs play in regional kingdoms?", "They could assist rulers but might also challenge central authority", "They always had no political influence", "They were modern elected members of parliament", "They never controlled local resources", "A"),
        ("Why did some kingdoms invest in reservoirs and tanks?", "Water storage supported irrigation and helped manage seasonal water availability", "It prevented all rainfall", "It eliminated the need for cultivation", "It was used only to build forts", "A"),
        ("How did regional kingdoms contribute to cultural development?", "Patronage supported architecture, literature, music and religious institutions", "They prohibited all artistic work", "They eliminated every regional language", "They built no public or religious structures", "A"),
        ("Why is the history of regional kingdoms not simply a history of warfare?", "It also includes administration, trade, agriculture, culture and social change", "Regional kingdoms never had armies", "Only battles can be studied historically", "Trade and culture did not exist", "A"),
        ("What could happen when a regional ruler became weaker?", "Rivals, neighbouring states or local chiefs might gain influence", "The kingdom was guaranteed to expand", "All disputes immediately ended", "Revenue collection became unnecessary", "A"),
        ("Why is it useful to study regional kingdoms together?", "Comparison reveals both shared patterns and regional differences in history", "Every kingdom followed exactly the same system", "Regional differences have no historical value", "All kingdoms existed in one period only", "A"),
    ],

    "Hard": [
        ("Which statement best explains the rise of regional kingdoms in medieval India?", "Shifts in imperial power, local political organisation and regional resources contributed to changing centres of authority", "All regional kingdoms emerged through modern elections", "Every kingdom was founded at the same time", "Regional politics was unrelated to agriculture or military power", "A"),
        ("Why should the history of regional kingdoms be studied through multiple types of evidence?", "Inscriptions, coins, architecture and literary sources illuminate different aspects of power and society", "A single inscription explains every historical development", "Archaeological evidence is never useful", "Written sources are always completely neutral", "A"),
        ("How could control over irrigation infrastructure strengthen a regional state?", "It could support agricultural production, settlement and the collection of revenue", "It automatically ended every drought", "It removed all need for administration", "It prevented communities from cultivating land", "A"),
        ("What is a limitation of using royal inscriptions to reconstruct history?", "They may emphasise the ruler's achievements and political claims", "They never mention rulers", "They are always modern statistical records", "They contain no information about donations or administration", "A"),
        ("Why were agricultural surpluses important to medieval urban centres?", "They supported non-agricultural populations, including officials, artisans and traders", "They made urban markets unnecessary", "They eliminated the need for transport", "They prevented the growth of crafts", "A"),
        ("How did military power and revenue reinforce one another?", "Revenue supported armies, while military control helped secure territory and revenue sources", "Neither had any relationship to the other", "Armies eliminated the need for state income", "Revenue systems prevented all warfare", "A"),
        ("Why could control of strategic forts influence regional politics?", "Forts could protect routes and centres while providing positions for military operations", "Forts had no military value", "Forts guaranteed permanent peace", "Forts replaced every form of government", "A"),
        ("What does Chola maritime activity indicate about medieval South Indian kingdoms?", "Some regional powers participated in overseas trade and naval campaigns", "All southern kingdoms avoided the sea", "Maritime trade began only in the twentieth century", "The Cholas had no political or economic interests outside their villages", "A"),
        ("Why should the Chola village assembly system not be equated with modern democracy?", "Local participation existed within a very different social and political structure", "Every resident had identical voting rights", "The Chola state had a modern written constitution", "Village assemblies controlled all kingdoms in India", "A"),
        ("What was one strategic consequence of the Battle of Talikota?", "It severely weakened Vijayanagara's imperial centre and changed the balance of power in the Deccan", "It founded the Mughal Empire", "It ended all political activity in southern India", "It marked the beginning of the Delhi Sultanate", "A"),
        ("Why did the decline of a capital not necessarily mean the immediate disappearance of a kingdom's political traditions?", "Successor rulers and regional centres could continue after the capital's destruction", "All institutions vanished permanently after every battle", "A capital was the only place where people lived", "Regional powers could not survive without one city", "A"),
        ("How did the geography of the Deccan affect political competition?", "Its forts, plateaus, agricultural areas and routes shaped military and economic priorities", "Geography had no effect on warfare or trade", "The Deccan had no settlements", "All routes were located outside the subcontinent", "A"),
        ("Why did the Ahom kingdom's political history differ from that of kingdoms centred in the Indo-Gangetic plain?", "Its regional environment, institutions and political interactions shaped its development", "It had no contact with neighbouring powers", "It followed every policy of the Cholas exactly", "It was governed from Delhi throughout its entire history", "A"),
        ("What is the strongest interpretation of royal temple patronage?", "It could express devotion, political legitimacy, economic capacity and cultural priorities", "It always proves that all subjects followed one religion", "It had no connection to politics or resources", "It replaced every other form of public activity", "A"),
        ("How could merchants influence the development of a regional kingdom without ruling it directly?", "Trade could generate wealth, connect markets and support urban communities", "Merchants had no effect on economic life", "Merchants automatically became kings", "Trade eliminated all political boundaries", "A"),
        ("Why might regional rulers compete for control of the same fertile territory?", "Agricultural resources, revenue and strategic location could make territory valuable", "Fertile land had no economic significance", "Territory could not support settlement", "All rulers rejected revenue collection", "A"),
        ("What does the circulation of coins across regions potentially indicate?", "Economic connections and the movement of currency between political areas", "The complete political unity of every region", "That every person used only one language", "That no local markets existed", "A"),
        ("Why might a ruler's claim of victory differ from the actual political outcome?", "Royal records could exaggerate success, so other evidence is needed to assess control and consequences", "Royal claims are always exact", "Political outcomes never change after battles", "No historical source ever presents a viewpoint", "A"),
        ("How could regional chiefs both support and weaken a kingdom?", "They could provide local resources and military support while pursuing independent interests", "They always obeyed without negotiation", "They had no access to local resources", "They were unrelated to regional politics", "A"),
        ("Why were alliances often temporary in medieval politics?", "Rulers' interests could change as threats, resources and rivalries shifted", "Every alliance lasted forever by law", "All rulers shared identical goals", "Alliances eliminated competition permanently", "A"),
        ("What is a careful way to compare the Chola and Vijayanagara states?", "Compare their periods, institutions, resources and regional contexts rather than assuming identical systems", "Assume both existed in exactly the same period", "Treat their administrative systems as identical without evidence", "Ignore the differences between their territories", "A"),
        ("Why is the phrase 'regional kingdom' useful but broad?", "It covers varied political formations whose scale, institutions and territorial reach differed", "It refers to one dynasty only", "Every regional kingdom had the same capital", "It means a modern state government", "A"),
        ("What can the study of regional architecture reveal beyond artistic style?", "It can provide clues about patronage, resources, religious institutions and political priorities", "It always reveals exact population figures", "It provides no information about society", "It proves every written account correct", "A"),
        ("How could changes in trade routes affect a regional kingdom?", "They could shift commercial opportunities, revenue and the importance of towns", "They could never influence economic activity", "They automatically abolished all taxes", "They prevented every form of cultural exchange", "A"),
        ("Why could environmental conditions affect political stability?", "Droughts, floods or poor harvests could strain livelihoods and state revenue", "Environmental conditions never affect agriculture", "Every harvest was identical", "Rulers never depended on agricultural income", "A"),
        ("What is a key reason to avoid describing medieval India as politically uniform?", "Different regions had distinct rulers, institutions, cultures and relationships with larger empires", "Every region was always governed directly by one ruler", "Local languages and customs did not exist", "All regional states had identical borders", "A"),
        ("How could religious institutions participate in regional economies?", "They could receive land or donations and support activities beyond worship", "They were always excluded from economic life", "They never owned resources", "They replaced all markets", "A"),
        ("What does the survival of regional traditions after dynastic change demonstrate?", "Cultural and administrative practices may continue or adapt beyond a particular ruling family", "Every new dynasty erased all previous practices", "Cultural traditions never change", "Dynastic change had no effect anywhere", "A"),
        ("Why should the outcomes of a medieval battle be evaluated beyond the immediate result?", "Longer-term political changes could include shifts in alliances, capitals and regional authority", "Every battle had no consequences after one day", "The winning side always controlled all of India", "Military outcomes never affected politics", "A"),
        ("Which approach best supports a balanced account of India's regional kingdoms?", "Combine political chronology with evidence about society, economy, culture and regional variation", "List battles alone and ignore all other evidence", "Rely on legends without comparison", "Assume every kingdom followed one unchanging model", "A"),
    ],
}


def main():
    db = SessionLocal()
    total_added = 0

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "Regional Kingdoms of India",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if not lesson:
            print("ERROR: Lesson 'Regional Kingdoms of India' was not found.")
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
            print("SUCCESS: Regional Kingdoms of India has all 90 questions!")
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