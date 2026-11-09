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
        ("Which dynasty ruled Delhi after the Ghurid conquests established Turkish rule?", "Mamluk or Slave dynasty", "Gupta dynasty", "Maurya dynasty", "Chola dynasty", "A"),
        ("Who is generally regarded as the founder of the Delhi Sultanate?", "Qutb al-Din Aibak", "Akbar", "Sher Shah Suri", "Ashoka", "A"),
        ("Which ruler began the construction of the Qutb Minar?", "Qutb al-Din Aibak", "Ibrahim Lodi", "Firoz Shah Tughlaq", "Balban", "A"),
        ("Who completed much of the early construction of the Qutb Minar?", "Iltutmish", "Razia Sultan", "Alauddin Khalji", "Bahlul Lodi", "A"),
        ("Who was the famous woman ruler of the Delhi Sultanate?", "Razia Sultan", "Nur Jahan", "Chand Bibi", "Rani Durgavati", "A"),
        ("Which dynasty ruled Delhi immediately before the Khalji dynasty?", "Mamluk dynasty", "Mughal dynasty", "Lodi dynasty", "Sayyid dynasty", "A"),
        ("Who was a prominent ruler of the Khalji dynasty?", "Alauddin Khalji", "Babur", "Humayun", "Prithviraj Chauhan", "A"),
        ("Which ruler introduced extensive market-control measures in Delhi?", "Alauddin Khalji", "Iltutmish", "Ibrahim Lodi", "Qutb al-Din Aibak", "A"),
        ("Which dynasty followed the Khaljis in the Delhi Sultanate?", "Tughlaq dynasty", "Gupta dynasty", "Maurya dynasty", "Chola dynasty", "A"),
        ("Who attempted to introduce token currency in the Delhi Sultanate?", "Muhammad bin Tughlaq", "Balban", "Razia Sultan", "Bahlul Lodi", "A"),
        ("Which ruler shifted the capital from Delhi to Daulatabad for a period?", "Muhammad bin Tughlaq", "Alauddin Khalji", "Iltutmish", "Sikandar Lodi", "A"),
        ("Who founded the Tughlaq dynasty?", "Ghiyasuddin Tughlaq", "Firoz Shah Tughlaq", "Ibrahim Lodi", "Qutb al-Din Aibak", "A"),
        ("Which Delhi Sultan was known for constructing canals and public buildings?", "Firoz Shah Tughlaq", "Razia Sultan", "Bahlul Lodi", "Balban", "A"),
        ("Which dynasty was the last ruling dynasty of the Delhi Sultanate?", "Lodi dynasty", "Mamluk dynasty", "Khalji dynasty", "Tughlaq dynasty", "A"),
        ("Who was the last Sultan of Delhi before the Mughal victory at Panipat in 1526?", "Ibrahim Lodi", "Sikandar Lodi", "Bahlul Lodi", "Alauddin Khalji", "A"),
        ("In which year did the First Battle of Panipat take place?", "1526", "1206", "1290", "1398", "A"),
        ("Who defeated Ibrahim Lodi at the First Battle of Panipat?", "Babur", "Akbar", "Sher Shah Suri", "Humayun", "A"),
        ("What was an iqta in the Delhi Sultanate?", "An assignment of revenue from an area", "A type of coin only", "A royal weapon", "A religious festival", "A"),
        ("What was the title of the ruler of the Delhi Sultanate?", "Sultan", "Pharaoh", "Shogun", "Consul", "A"),
        ("Which traveller visited India during Muhammad bin Tughlaq's reign?", "Ibn Battuta", "Marco Polo during Akbar's reign", "Megasthenes during Lodi rule", "Fa-Hien during Khalji rule", "A"),
        ("Which language was widely used in the Delhi Sultanate's court and administration?", "Persian", "Latin", "Greek", "Portuguese", "A"),
        ("What was the main occupation of most people in the Sultanate's countryside?", "Agriculture", "Shipbuilding only", "Mining gold only", "Silk trading only", "A"),
        ("What was a major source of income for the Sultanate?", "Land revenue", "Modern income tax", "Income from railways", "Income from airlines", "A"),
        ("Which monument complex contains the Qutb Minar?", "Qutb complex", "Red Fort complex in Agra", "Sanchi complex", "Konark complex", "A"),
        ("Which ruler is associated with strict control over nobles and a strong monarchy?", "Balban", "Ibrahim Lodi only", "Babur", "Chandragupta Maurya", "A"),
        ("Which dynasty came after the Sayyid dynasty?", "Lodi dynasty", "Mamluk dynasty", "Khalji dynasty", "Tughlaq dynasty", "A"),
        ("What was the main role of soldiers in the Sultanate?", "To defend and expand the Sultan's territories", "To conduct modern elections", "To operate railways", "To run public television", "A"),
        ("What is a dynasty?", "A succession of rulers from the same family or lineage", "A type of tax", "A farming tool", "A trade route", "A"),
        ("Which city served as the main political centre of the Delhi Sultanate for much of its history?", "Delhi", "Madurai", "Kochi", "Puri", "A"),
        ("What happened to the Delhi Sultanate after the First Battle of Panipat in 1526?", "Mughal rule replaced the Lodi Sultanate", "The Maurya Empire was restored", "The Gupta Empire began", "The Chola Empire conquered all of India", "A"),
    ],

    "Medium": [
        ("Why was Iltutmish important in the early Delhi Sultanate?", "He consolidated and strengthened the Sultanate", "He founded the Mughal Empire", "He ended all land revenue collection", "He established British rule", "A"),
        ("Why was Razia Sultan's rule historically significant?", "She was a woman who ruled as Sultan of Delhi", "She founded the Lodi dynasty", "She defeated Babur at Panipat", "She introduced railways", "A"),
        ("Why did Alauddin Khalji introduce market regulations?", "To control prices and help maintain a large army at manageable cost", "To abolish all trade", "To replace agriculture with factories", "To introduce universal voting", "A"),
        ("How did Alauddin Khalji respond to Mongol threats?", "He strengthened military preparations and defences", "He surrendered the whole Sultanate permanently", "He moved the capital to London", "He abolished the army", "A"),
        ("What was the purpose of maintaining records of soldiers and horses under Alauddin Khalji?", "To improve military supervision and reduce fraud", "To record village festivals only", "To count temple sculptures", "To regulate ocean tides", "A"),
        ("Why was Muhammad bin Tughlaq's token currency experiment difficult to manage?", "Counterfeit coins were difficult to control", "People had no need for money", "The Sultan banned every metal", "Coins could not be transported by land", "A"),
        ("What was one major problem with Muhammad bin Tughlaq's transfer of the capital to Daulatabad?", "The relocation caused hardship and disruption", "Daulatabad was located in Europe", "Delhi had no inhabitants", "The move ended all agricultural activity permanently", "A"),
        ("What does the iqta system tell us about Sultanate administration?", "Revenue assignments helped support officials and military responsibilities", "Every village elected the Sultan", "All land belonged to independent merchants", "It was a modern banking system", "A"),
        ("What was the responsibility of an iqtadar or muqti?", "Administering an assigned territory and collecting its revenue under the Sultan's authority", "Leading the Mughal army at Panipat in 1526", "Writing only religious poetry", "Operating a modern court of appeal", "A"),
        ("Why did Sultans try to control powerful nobles?", "To reduce the risk of rebellion and strengthen central authority", "To give nobles complete independence", "To eliminate the royal administration", "To abolish military service", "A"),
        ("How did Firoz Shah Tughlaq differ from some earlier rulers in his public works?", "He is associated with canals, gardens and buildings", "He introduced the railway network", "He invented the printing press in India", "He built the Taj Mahal", "A"),
        ("What was one limitation of relying heavily on a Sultan's personal authority?", "Administration could weaken when rulers were ineffective or succession was disputed", "It guaranteed peaceful succession forever", "It eliminated all regional resistance", "It prevented every tax dispute", "A"),
        ("Why are chronicles useful for studying the Delhi Sultanate?", "They provide written accounts of political events and rulers", "They contain only modern census data", "They are all neutral eyewitness recordings", "They replace the need for archaeological evidence", "A"),
        ("What is an important limitation of court chronicles?", "They may reflect the views and interests of their authors or patrons", "They never mention rulers", "They contain no historical information", "They were all written in the twenty-first century", "A"),
        ("What information did Ibn Battuta's account provide?", "Observations about society, travel and administration in the period he visited", "A complete record of every Sultan's reign", "Details of the Industrial Revolution", "A modern Indian Constitution", "A"),
        ("How did agriculture support the Delhi Sultanate?", "Agricultural production and land revenue supported the state", "It eliminated the need for trade", "It provided electricity to cities", "It replaced every form of taxation", "A"),
        ("Why were towns important under the Sultanate?", "They supported administration, crafts, trade and markets", "They were used only for royal hunting", "They had no links to villages", "They contained no artisans", "A"),
        ("What was one reason rulers built forts and fortified cities?", "To strengthen defence and protect strategic centres", "To stop all farming", "To eliminate the need for soldiers", "To prevent all movement of goods", "A"),
        ("Which statement best describes the relationship between the Sultan and regional governors?", "Governors administered territories but were expected to recognise the Sultan's authority", "Governors were always independent kings with no obligations", "Governors were elected by universal adult suffrage", "Governors had no administrative role", "A"),
        ("Why could succession become a source of conflict in the Sultanate?", "Rival claimants and powerful nobles could compete for the throne", "A fixed modern election system selected every ruler", "The Sultanate had no ruling family", "The throne passed automatically to a village council", "A"),
        ("What was one effect of military expansion?", "It could increase territory but also create administrative and financial pressures", "It always removed the need for taxes", "It ended all conflict permanently", "It prevented cultural exchange", "A"),
        ("Why did the Delhi Sultanate sometimes face revolts in distant regions?", "Local rulers and governors could resist central control", "Every region had identical interests", "The Sultan never appointed officials", "There were no regional communities", "A"),
        ("What does the Qutb Minar complex reveal about the period?", "Architecture and building projects associated with political and cultural change", "The development of modern railways", "The start of the Gupta Empire", "The creation of the Indian Parliament", "A"),
        ("Why is it inaccurate to describe all Sultanate rulers as following identical policies?", "Rulers differed in priorities, methods and political circumstances", "All rulers were the same person", "Every dynasty lasted exactly one year", "No ruler ever changed policy", "A"),
        ("What role did Persian play in administration and elite culture?", "It was widely used in courtly writing and official communication", "It was the only language spoken by every villager", "It replaced all spoken languages across India", "It was used only for modern computer code", "A"),
        ("What was the broad purpose of land-revenue assessment?", "To determine and collect revenue from agricultural production", "To count the number of city walls", "To choose a new national anthem", "To issue driving licences", "A"),
        ("Why did maintaining a large army require substantial resources?", "Soldiers, horses, equipment and supplies had to be paid for", "Armies never needed food", "Weapons were free in every region", "Soldiers were never stationed anywhere", "A"),
        ("What can coins help historians investigate?", "Rulers, political authority, dates and aspects of the economy", "Only modern weather patterns", "The exact thoughts of every farmer", "Every event without any other evidence", "A"),
        ("Why is the First Battle of Panipat considered a turning point?", "Babur's victory ended Lodi rule and established Mughal power in North India", "It restored the Maurya Empire", "It marked the beginning of the Delhi Sultanate in 1206", "It ended agriculture in India", "A"),
        ("How should historians assess the successes of a Sultan's policy?", "By examining its aims, implementation, outcomes and contemporary evidence", "By relying on legends alone", "By assuming every policy succeeded", "By ignoring evidence that disagrees", "A"),
    ],

    "Hard": [
        ("Which sequence correctly orders the major dynasties of the Delhi Sultanate?", "Mamluk, Khalji, Tughlaq, Sayyid, Lodi", "Khalji, Lodi, Mamluk, Sayyid, Tughlaq", "Tughlaq, Mamluk, Lodi, Khalji, Sayyid", "Lodi, Sayyid, Khalji, Mamluk, Tughlaq", "A"),
        ("Which statement about the foundation of the Delhi Sultanate is most accurate?", "Qutb al-Din Aibak established an independent Sultanate in 1206 after the Ghurid political order weakened", "The Sultanate was founded by Babur in 1526", "The Sultanate began under Ashoka", "The Sultanate was founded by the British in 1858", "A"),
        ("Why did Iltutmish's reign matter for the survival of the early Sultanate?", "He consolidated control, strengthened institutions and dealt with rival claims", "He permanently abolished the army", "He transferred all authority to the Mongols", "He established the Indian Republic", "A"),
        ("Which interpretation best explains Razia Sultan's political challenges?", "Gender expectations and opposition from powerful elites complicated her rule", "She ruled after the fall of the Mughal Empire", "She was elected through universal adult suffrage", "She never faced opposition", "A"),
        ("How could Alauddin Khalji's market controls support military policy?", "Regulated prices could help the state maintain a large army without proportionately higher cash costs", "They made military supplies unnecessary", "They ended the use of money throughout India", "They prevented the Sultan from collecting revenue", "A"),
        ("Why did Alauddin Khalji's campaigns require strong revenue administration?", "Territorial expansion and military defence required reliable state resources", "Campaigns were funded entirely by modern banks", "The army operated without food or pay", "Revenue had no connection to the state", "A"),
        ("What was the central administrative risk of the iqta system?", "Assigned officials could accumulate local power or misuse revenue if supervision weakened", "It guaranteed every official would be loyal", "It eliminated all provincial administration", "It made agricultural revenue impossible to collect", "A"),
        ("Why did the Sultanate distinguish revenue assignments from complete private ownership?", "An assignment of revenue did not automatically make its holder an independent sovereign landowner", "Every iqtadar became a modern elected president", "Revenue assignments were always permanent private estates", "The system had no relationship to government", "A"),
        ("What was a key weakness of Muhammad bin Tughlaq's token currency experiment?", "The state struggled to prevent imitation and maintain trust in the tokens' value", "The tokens were accepted only by modern banks", "The experiment involved paper notes issued by the Reserve Bank of India", "The Sultan had no currency system at all", "A"),
        ("Why is Muhammad bin Tughlaq's capital transfer often assessed as a costly policy?", "The large-scale relocation created logistical hardship and did not achieve all its intended aims", "The move occurred after the British built railways", "Daulatabad was outside the Indian subcontinent", "The policy was implemented without moving anyone", "A"),
        ("Which conclusion about Muhammad bin Tughlaq is most historically responsible?", "His ambitious policies had mixed results and should be evaluated individually", "Every policy he introduced succeeded completely", "Every policy failed for exactly the same reason", "No written source discusses his reign", "A"),
        ("How did Firoz Shah Tughlaq's public works relate to governance?", "Infrastructure projects could support irrigation, urban life and the ruler's public image", "They were designed to create a modern railway system", "They eliminated every agricultural tax", "They transferred the capital to Europe", "A"),
        ("Why might a ruler's reliance on nobles create political instability?", "Nobles could become kingmakers or support rival claimants during succession disputes", "Nobles had no military or administrative influence", "Nobles were selected by nationwide electronic voting", "Nobles could never oppose a Sultan", "A"),
        ("Which source criticism is most appropriate when using a court chronicle?", "Compare its claims with other written, material and archaeological evidence where possible", "Assume the author had no political viewpoint", "Reject every chronicle without reading it", "Treat every statement as a modern statistical survey", "A"),
        ("Why is Minhaj-i-Siraj important to historians of the early Sultanate?", "His historical writing provides information about early rulers and political events", "He wrote the Indian Constitution", "He commanded Babur's army at Panipat in 1526", "He designed the modern Indian Parliament", "A"),
        ("What is a careful way to use Ibn Battuta's travel account?", "Use it as a valuable but situated account, considering what he observed and the perspective he brought", "Assume he personally witnessed every event in the Sultanate", "Treat it as a complete annual census", "Ignore its descriptions of travel and society", "A"),
        ("What relationship existed between the countryside and Sultanate cities?", "Agricultural surpluses and revenue connected rural producers with urban officials, markets and consumers", "Cities were entirely independent of rural production", "Villages supplied no food to towns", "All urban residents worked in agriculture", "A"),
        ("How could excessive revenue demands affect rural society?", "They could increase hardship and resistance among cultivators", "They guaranteed higher harvests in every year", "They removed all dependence on rainfall", "They ended every local dispute", "A"),
        ("Why was controlling distant territories difficult for the Sultanate?", "Communication delays, local power holders and the cost of enforcement limited central control", "Officials could communicate instantly using the internet", "All regions had identical terrain and political interests", "The Sultan never needed local officials", "A"),
        ("What does the changing sequence of dynasties indicate?", "Political authority changed through succession struggles, elite competition and shifts in power", "The same family ruled continuously from 1206 to 1526", "Dynasties changed only because of scheduled elections", "The Sultanate had no political conflicts", "A"),
        ("Why should the Delhi Sultanate not be treated as a single unchanging political system?", "Its rulers, administrative practices, territorial reach and political conditions varied over time", "It had no rulers after its foundation", "All five dynasties used identical policies in every area", "Its territory never changed", "A"),
        ("How did military expansion create a governance challenge?", "The state needed to secure conquered areas, manage local elites and sustain supply lines", "Conquest automatically created permanent loyalty", "New territory required no officials", "Expansion removed the need for defence", "A"),
        ("What is the strongest interpretation of Sultanate architecture as historical evidence?", "Buildings can reveal patronage, political authority, artistic practices and available resources", "A building always proves every written claim correct", "Architecture reveals nothing about its period", "All monuments were constructed by one ruler", "A"),
        ("Why did rulers build fortified centres and strategic settlements?", "They could protect important routes, administration and military positions", "They removed the need for diplomacy or armies", "They prevented all trade and travel by design", "They served only as schools", "A"),
        ("What was one broader consequence of the Sultanate's use of Persian in elite administration?", "Persian became important in courtly records and communication among many officials and writers", "Every regional language disappeared", "Persian became the only language spoken in villages", "All historical documents were written in English", "A"),
        ("Which statement best distinguishes political authority from effective control?", "A Sultan might claim authority over an area without exercising equally strong control everywhere", "A royal claim always meant complete control of every village", "Political authority existed only in modern democracies", "Governors never challenged central power", "A"),
        ("Why did succession disputes often affect the stability of the Sultanate?", "Competing claimants could divide elites and trigger military conflict", "The throne was always transferred through a fixed modern constitution", "Succession disputes never involved the army", "Every ruler named the same successor", "A"),
        ("What is a major limitation of judging a medieval ruler only by later popular stories?", "Later accounts may simplify events or reflect changing political and cultural interpretations", "Stories always provide exact administrative records", "Oral traditions cannot contain any historical information", "All later accounts were written by eyewitnesses", "A"),
        ("Why should the impact of a policy be separated from its stated intention?", "A policy's goals may differ from its actual implementation and consequences", "Intentions always guarantee success", "Consequences are never historically relevant", "Policies cannot have unintended effects", "A"),
        ("Which overall statement best describes the end of the Delhi Sultanate?", "Ibrahim Lodi's defeat by Babur in 1526 ended Lodi rule and ushered in Mughal rule in North India", "The Sultanate ended with the Mauryan conquest in 261 BCE", "The Sultanate ended when the British left India in 1947", "The Sultanate ended with the founding of the Khalji dynasty", "A"),
    ],
}


def main():
    db = SessionLocal()
    total_added = 0

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "The Delhi Sultanate",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if not lesson:
            print("ERROR: Lesson 'The Delhi Sultanate' was not found.")
            print("Check the lesson title and topic in the database.")
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
                print(
                    f"{difficulty}: already has {len(existing)} questions; skipped."
                )
                continue

            existing_texts = {
                q.question.strip().lower() for q in existing
            }
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
            print(
                f"{difficulty}: added {added_this_level} questions "
                f"(target: 30)."
            )

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
            print("SUCCESS: The Delhi Sultanate has all 90 questions!")
        else:
            print("WARNING: The lesson does not yet have all 90 questions.")
            print("Check the counts above before moving to the next lesson.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()