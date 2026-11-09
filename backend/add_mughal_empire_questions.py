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
        ("Who founded the Mughal Empire in India?", "Babur", "Akbar", "Humayun", "Aurangzeb", "A"),
        ("In which year was the First Battle of Panipat fought?", "1526", "1556", "1605", "1707", "A"),
        ("Who was defeated by Babur at the First Battle of Panipat?", "Ibrahim Lodi", "Akbar", "Sher Shah Suri", "Rana Sanga", "A"),
        ("Who was Babur's son and successor?", "Humayun", "Akbar", "Jahangir", "Shah Jahan", "A"),
        ("Who was one of the most famous Mughal emperors?", "Akbar", "Ibrahim Lodi", "Qutb al-Din Aibak", "Balban", "A"),
        ("Who was Akbar's son and successor?", "Jahangir", "Babur", "Aurangzeb", "Sher Shah Suri", "A"),
        ("Which Mughal emperor commissioned the Taj Mahal?", "Shah Jahan", "Akbar", "Babur", "Humayun", "A"),
        ("Who was the last major Mughal emperor commonly associated with the empire's greatest territorial extent?", "Aurangzeb", "Babur", "Humayun", "Jahangir", "A"),
        ("Who was Akbar's famous revenue administrator?", "Raja Todar Mal", "Tansen", "Birbal", "Abul Fazl", "A"),
        ("Which Mughal emperor is associated with the Din-i Ilahi initiative?", "Akbar", "Babur", "Shah Jahan", "Aurangzeb", "A"),
        ("Who wrote the Akbarnama?", "Abul Fazl", "Tulsidas", "Amir Khusrau", "Kalidasa", "A"),
        ("What was the Mughal capital associated with Shah Jahan's Red Fort?", "Delhi", "Kolkata", "Chennai", "Mumbai", "A"),
        ("Which monument was built by Shah Jahan in memory of Mumtaz Mahal?", "Taj Mahal", "Qutb Minar", "Sanchi Stupa", "Charminar", "A"),
        ("Who was Mumtaz Mahal?", "Shah Jahan's wife", "Akbar's mother", "Babur's sister", "Aurangzeb's daughter", "A"),
        ("Which Mughal emperor was known for his memoirs called the Tuzuk-i-Jahangiri?", "Jahangir", "Babur", "Akbar", "Shah Jahan", "A"),
        ("Which battle in 1556 helped Akbar's forces secure Mughal power in North India?", "Second Battle of Panipat", "Battle of Plassey", "Battle of Buxar", "First Battle of Tarain", "A"),
        ("Who acted as Akbar's regent during the early years of his reign?", "Bairam Khan", "Raja Man Singh", "Tansen", "Todar Mal", "A"),
        ("What was a mansab in Mughal administration?", "A rank assigned to an official", "A type of monument", "A religious book", "A farming tool", "A"),
        ("What was the main source of income for the Mughal state?", "Land revenue", "Income tax on software", "Railway fares", "Airline tickets", "A"),
        ("What was a jagir generally associated with?", "An assignment of revenue from an area", "A type of cannon", "A royal palace only", "A village festival", "A"),
        ("Which Mughal ruler was the son of Shah Jahan?", "Aurangzeb", "Babur", "Humayun", "Akbar", "A"),
        ("Which Mughal emperor built Fatehpur Sikri as an important imperial centre?", "Akbar", "Babur", "Jahangir", "Aurangzeb", "A"),
        ("Which Mughal emperor was defeated by Sher Shah Suri at the Battle of Kannauj in 1540?", "Humayun", "Akbar", "Jahangir", "Shah Jahan", "A"),
        ("Who founded the Sur Empire after defeating Humayun?", "Sher Shah Suri", "Rana Sanga", "Bairam Khan", "Raja Todar Mal", "A"),
        ("What was the Mughal court?", "The emperor's centre of political and administrative activity", "A village market only", "A modern parliament", "A religious school only", "A"),
        ("Which language was widely used in Mughal court chronicles?", "Persian", "Latin", "Portuguese", "French", "A"),
        ("What was the Mughal emperor's position in the empire?", "The supreme ruler", "An elected village representative", "A local merchant", "A provincial farmer", "A"),
        ("Which Mughal emperor was associated with a policy of broad religious tolerance?", "Akbar", "Aurangzeb only", "Ibrahim Lodi", "Balban", "A"),
        ("Which emperor's reign is often associated with the construction of the Red Fort in Delhi?", "Shah Jahan", "Babur", "Humayun", "Iltutmish", "A"),
        ("Which event is associated with the decline of Mughal central power in the eighteenth century?", "Increasing regional independence and weakening central authority", "The founding of the Maurya Empire", "The beginning of the Gupta Empire", "The start of the Delhi Sultanate", "A"),
    ],

    "Medium": [
        ("Why was Babur's victory at Panipat in 1526 important?", "It ended Lodi rule in Delhi and established Mughal power in North India", "It ended British rule", "It founded the Maurya Empire", "It united all of South India permanently", "A"),
        ("Why did Humayun lose control of much of his Indian territory?", "He faced military challenges, including defeat by Sher Shah Suri", "He was defeated by the British in 1947", "He voluntarily ended the Mughal dynasty", "He never became emperor", "A"),
        ("How did Akbar strengthen the Mughal Empire?", "Through military expansion, administrative reforms and alliances with regional elites", "By abolishing all administration", "By ending all contact with regional rulers", "By eliminating land revenue", "A"),
        ("What was the purpose of Akbar's alliances with Rajput rulers?", "To secure cooperation and strengthen imperial authority", "To end all regional administration", "To replace every local ruler with a European governor", "To stop all trade", "A"),
        ("What did the mansabdari system help the Mughal emperor organise?", "The ranks, responsibilities and military obligations of officials", "Only village festivals", "Only religious ceremonies", "Modern parliamentary elections", "A"),
        ("What was the general purpose of the Mughal jagir system?", "To assign revenue for supporting officials and their obligations", "To create modern private banks", "To eliminate government income", "To issue passports", "A"),
        ("Why was land revenue important to the Mughal state?", "It financed administration, the army and the imperial household", "It was used only to build private shops", "It replaced all forms of agriculture", "It was collected only from foreign tourists", "A"),
        ("What was Raja Todar Mal known for?", "Revenue administration and assessment reforms under Akbar", "Writing the Baburnama", "Building the Taj Mahal", "Founding the Lodi dynasty", "A"),
        ("What does the Akbarnama provide historians?", "A courtly account of Akbar's reign and imperial activities", "A modern census of India", "A record of the Indian independence movement", "A guide to modern banking", "A"),
        ("Why should historians read imperial chronicles critically?", "They may reflect the interests and viewpoints of court authors", "They always contain only neutral facts", "They were all written by modern historians", "They never discuss political events", "A"),
        ("Why was Fatehpur Sikri significant under Akbar?", "It served as an important imperial centre and reflected Mughal architecture", "It was the capital of the British Empire", "It was built by Ashoka", "It was the site of the First Battle of Panipat", "A"),
        ("What is the historical importance of the Taj Mahal?", "It is a major example of Mughal architecture commissioned by Shah Jahan", "It was built by Babur as a military fort", "It was constructed by the Mauryas", "It was a parliament building", "A"),
        ("What was one function of the Mughal imperial court?", "It displayed imperial authority and brought officials and nobles together", "It conducted modern general elections", "It operated as a village-only council", "It had no role in administration", "A"),
        ("How did Mughal rulers maintain control over distant provinces?", "Through appointed officials, revenue arrangements and military power", "Through the internet", "By allowing every province complete independence", "By eliminating all local administration", "A"),
        ("Why could powerful mansabdars pose a challenge to the emperor?", "They controlled resources and military followers that could influence politics", "They were forbidden from holding any responsibilities", "They were all elected by modern voters", "They could not interact with the court", "A"),
        ("What is a major difference between a jagir and a modern private estate?", "A jagir was generally a revenue assignment tied to official responsibilities", "A jagir was always a modern registered company", "A jagir was a railway station", "A jagir was a type of coin", "A"),
        ("What was one result of Mughal expansion?", "The empire incorporated diverse regions and communities under imperial rule", "All regional cultures disappeared immediately", "Agriculture ended across India", "The empire had no need for officials", "A"),
        ("How did trade and crafts contribute to Mughal-era cities?", "They supported urban economies, markets and imperial demand", "They had no relationship to city life", "They replaced all farming throughout India", "They were restricted to royal families only", "A"),
        ("What was the significance of Persian in Mughal administration?", "It was widely used in court records and elite literary culture", "It was the only language spoken by all people", "It replaced every Indian language", "It was used only for modern computer programming", "A"),
        ("Why did conflicts arise over succession among Mughal princes?", "There was no consistently enforced rule that always ensured peaceful succession", "Every succession was decided by universal adult suffrage", "Princes were never allowed to compete", "The empire had no royal family", "A"),
        ("What was one effect of Aurangzeb's long military campaigns?", "They placed heavy financial and administrative demands on the empire", "They eliminated all regional resistance permanently", "They ended the need for revenue", "They created modern railways", "A"),
        ("Why did regional powers become more independent as Mughal authority weakened?", "Central control and resources weakened, allowing local rulers to assert power", "The emperor gave every region the same modern constitution", "There were no regional elites", "Trade ceased everywhere", "A"),
        ("What can Mughal coins tell historians?", "Information about rulers, political authority, dates and monetary systems", "The exact thoughts of every citizen", "Every historical event without other evidence", "Only modern weather forecasts", "A"),
        ("How did Mughal painting develop?", "It combined court patronage with varied artistic influences and traditions", "It was limited to modern photography", "It began only after Indian independence", "It was used only for military maps", "A"),
        ("Why is the Mughal Empire described as a diverse empire?", "It governed populations with varied languages, customs and religious traditions", "Every subject followed the same customs", "It contained only one region", "It had no cultural exchange", "A"),
        ("What was the significance of the Battle of Haldighati in 1576?", "It was a major conflict involving Mughal forces and Maharana Pratap's forces", "It ended Mughal rule in 1526", "It founded the Delhi Sultanate", "It was fought during British rule in 1857", "A"),
        ("What happened when Humayun returned to power in India?", "He regained the Mughal throne after the Sur interlude", "He founded the Lodi dynasty", "He defeated Babur at Panipat", "He became the first British governor", "A"),
        ("Why did the Mughal Empire rely on local intermediaries in many regions?", "Local elites and officials helped administer territory and collect revenue", "The emperor could personally visit every village daily", "Local knowledge was never needed", "The empire had no taxation system", "A"),
        ("Which statement best describes the Mughal decline?", "It was a gradual process involving political, military, financial and regional factors", "It occurred in a single event in 1206", "It was caused only by one battle", "It began before Babur founded the empire", "A"),
        ("Why is 1707 often used as a reference point in Mughal history?", "Aurangzeb died that year, after which imperial authority faced growing challenges", "Babur founded the empire that year", "Akbar became emperor that year", "The First Battle of Panipat occurred that year", "A"),
    ],

    "Hard": [
        ("Which sequence correctly orders the first six Mughal emperors?", "Babur, Humayun, Akbar, Jahangir, Shah Jahan, Aurangzeb", "Humayun, Babur, Jahangir, Akbar, Aurangzeb, Shah Jahan", "Akbar, Babur, Humayun, Shah Jahan, Jahangir, Aurangzeb", "Babur, Akbar, Humayun, Aurangzeb, Jahangir, Shah Jahan", "A"),
        ("Why was the Mughal victory at Panipat in 1526 strategically important?", "Babur used military organisation and artillery effectively against Ibrahim Lodi's forces", "It was won by the British East India Company", "It restored the Maurya Empire", "It ended all warfare in India", "A"),
        ("How did Akbar's administrative system help govern a large empire?", "It linked ranked officials, revenue arrangements, military service and imperial authority", "It removed all officials from the provinces", "It relied exclusively on elected representatives", "It abolished the army and taxation", "A"),
        ("What was the key principle of the mansabdari system?", "Officials received ranks that helped define status and responsibilities, including military obligations", "Every rank was inherited automatically without exception", "It was a system of modern university degrees", "It applied only to village farmers", "A"),
        ("Why could the jagirdari system become difficult to manage?", "Revenue assignments and local conditions could create tensions over income and obligations", "Jagirs generated unlimited revenue in every region", "The system did not involve revenue", "All assignments were modern private companies", "A"),
        ("What relationship existed between the Mughal emperor and mansabdars?", "The emperor assigned ranks and responsibilities, while officials served the imperial administration", "Mansabdars elected the emperor through modern elections", "The emperor had no authority over them", "Mansabdars were exclusively religious teachers", "A"),
        ("Why was land-revenue assessment central to Mughal government?", "Agricultural revenue was a major financial basis for the imperial state", "The empire had no agricultural economy", "Revenue was collected only from modern industries", "Land revenue was unrelated to military spending", "A"),
        ("How did alliances with Rajput rulers support Akbar's empire?", "They brought influential regional elites into imperial service and political cooperation", "They abolished all regional identities", "They prevented the Mughal army from expanding", "They eliminated all noble families", "A"),
        ("Which statement about Akbar's religious policies is most accurate?", "His policies included efforts toward accommodation and debate across religious traditions", "He introduced modern universal suffrage", "He prohibited all discussion of religion", "He ruled after the end of the Mughal Empire", "A"),
        ("Why should Din-i Ilahi not be described as a mass religion adopted by all Mughal subjects?", "It was a limited initiative associated with Akbar and did not become a widespread popular religion", "It replaced every religious tradition across India", "It was founded by Babur in 1526", "It was the official religion of modern India", "A"),
        ("What is a sound way to interpret Abul Fazl's Akbarnama?", "As an important court source that should be read with awareness of its imperial perspective", "As a completely neutral modern newspaper", "As a census covering every century", "As a text written by a British governor in 1947", "A"),
        ("Why is the Baburnama valuable to historians?", "It provides Babur's own account and observations, though it reflects his personal perspective", "It is a modern statistical survey of India", "It records events after Aurangzeb's death only", "It was written by Akbar's revenue minister", "A"),
        ("How did the Sur interlude affect Mughal political history?", "Sher Shah Suri's victories displaced Humayun temporarily before Humayun restored Mughal rule", "It permanently ended all Mughal claims to India", "It preceded the foundation of the Delhi Sultanate by centuries", "It was the period of British independence", "A"),
        ("What helped Humayun regain the Mughal throne?", "Political and military circumstances enabled his return after the Sur rulers' period", "He defeated Akbar at the Second Battle of Panipat", "He founded the Maurya Empire", "He became emperor through a modern election", "A"),
        ("Why was the Second Battle of Panipat in 1556 significant?", "Akbar's forces defeated Hemu, helping secure Mughal authority in North India", "Babur defeated Ibrahim Lodi in this battle", "It marked the fall of the British Raj", "It was fought by the Marathas against the British in 1818", "A"),
        ("What was one major consequence of Shah Jahan's architectural patronage?", "It produced monumental buildings that projected imperial wealth and authority", "It eliminated the financial costs of government", "It ended all artistic traditions outside Delhi", "It introduced industrial mass production", "A"),
        ("How should historians interpret the Taj Mahal as evidence?", "As a monument reflecting imperial patronage, architecture, craftsmanship and cultural influences", "As proof that every subject lived equally wealthy lives", "As a military victory record only", "As evidence of modern democratic elections", "A"),
        ("Why did prolonged Deccan campaigns challenge Aurangzeb's empire?", "They required sustained military resources and contributed to administrative and financial pressures", "They immediately ended all regional resistance", "They removed the need for provincial officials", "They made revenue collection unnecessary", "A"),
        ("Which combination best explains the weakening of Mughal central authority after Aurangzeb?", "Succession conflicts, financial strains, regional challenges and changing military conditions", "The invention of the internet and railways", "A single natural disaster that ended the empire instantly", "The empire's complete lack of regional diversity", "A"),
        ("Why did regional states gain influence as Mughal authority weakened?", "Local rulers used political opportunities to build more autonomous power bases", "The Mughal state had abolished all local elites", "Every province was controlled directly from Delhi without officials", "All regional armies disappeared", "A"),
        ("How did the Mughal economy connect rural and urban life?", "Agricultural revenue, craft production and trade linked villages, towns and imperial centres", "Cities operated without food or raw materials", "Rural communities had no role in the economy", "All trade took place only inside palaces", "A"),
        ("Why must historians distinguish an imperial claim from actual territorial control?", "Authority could vary across regions depending on local power, military presence and administrative capacity", "A claim always proved complete control", "Territorial control never changed over time", "Every region had identical administrative conditions", "A"),
        ("What is a key limitation of using royal court paintings as historical evidence?", "They may present idealised images of power rather than everyday life for all social groups", "They never depict rulers", "They always provide complete population statistics", "They cannot reveal anything about court culture", "A"),
        ("How did Mughal painting reflect cultural exchange?", "It developed through court patronage and interactions among different artistic traditions", "It was isolated from all other artistic influences", "It began only with modern photography", "It was limited to European artists alone", "A"),
        ("Why is it misleading to explain Mughal decline through a single cause?", "Different political, economic, military and regional pressures interacted over time", "Historical changes always have exactly one cause", "No regional powers existed", "The empire had no financial system", "A"),
        ("What does the changing role of nobles reveal about Mughal politics?", "Imperial authority depended partly on managing relationships with influential elites", "Nobles had no political influence", "The emperor was elected by nobles every year", "The empire operated without administrators", "A"),
        ("Why was the Mughal state not equally powerful in every province at all times?", "Distance, local elites, resistance and resources affected how far central orders could be enforced", "Every province had the same terrain and population", "All orders were enforced instantly", "No regional officials existed", "A"),
        ("What was the significance of the death of Aurangzeb in 1707?", "It was followed by intensified succession struggles and challenges to central imperial authority", "It marked the foundation of the Mughal Empire", "It ended the Delhi Sultanate in 1206", "It began British rule in India in 1757", "A"),
        ("Which statement best describes the Mughal Empire's historical legacy?", "It influenced administration, architecture, painting, literature and regional political developments", "It affected only military history", "It left no material or written sources", "It eliminated every regional tradition", "A"),
        ("What is the most reliable approach to studying the Mughal Empire?", "Compare chronicles, coins, buildings, paintings and other evidence while considering each source's limits", "Rely entirely on one legend", "Assume court sources are always neutral", "Ignore material evidence and regional perspectives", "A"),
    ],
}


def main():
    db = SessionLocal()
    total_added = 0

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "The Mughal Empire",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if not lesson:
            print("ERROR: Lesson 'The Mughal Empire' was not found.")
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
            print("SUCCESS: The Mughal Empire has all 90 questions!")
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