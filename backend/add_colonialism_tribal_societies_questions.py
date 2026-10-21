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
        ("What does colonialism mean?", "Control of one country or region by another power", "Equal partnership between independent countries", "A system of village elections", "A type of farming tool", "A"),
        ("Which European power ruled India before independence in 1947?", "Britain", "Japan", "Germany", "Russia", "A"),
        ("What is a tribal community?", "A community with its own social and cultural traditions", "A group consisting only of royal officials", "A modern political party", "A company that collects taxes", "A"),
        ("What was a common livelihood among many tribal communities?", "Farming, hunting, gathering and forest-based activities", "Working only in factories", "Operating airlines", "Managing modern banks", "A"),
        ("What is shifting cultivation?", "Growing crops on a plot for a period and then moving to another plot", "Growing crops only in flowerpots", "Cultivating crops inside factories", "Growing crops without using land", "A"),
        ("What is a forest produce?", "A product obtained from forests, such as honey or timber", "A product made only in a railway workshop", "A type of government tax", "A modern computer programme", "A"),
        ("Which community is historically associated with the Santhal uprising of 1855–56?", "Santhals", "Ahoms only", "Mughals", "Cholas", "A"),
        ("Who was an important leader of the Santhal rebellion?", "Sidhu and Kanhu Murmu", "Akbar and Birbal", "Babur and Humayun", "Nana Sahib and Tantia Tope", "A"),
        ("Who led the Munda uprising known as Ulgulan?", "Birsa Munda", "Rani Lakshmibai", "Kunwar Singh", "Bahadur Shah Zafar", "A"),
        ("What does the word 'Ulgulan' refer to in the context of the Munda movement?", "The Great Tumult or great upheaval", "A royal coronation", "A harvest festival only", "A type of land tax", "A"),
        ("What was one major effect of British forest policies on tribal communities?", "Restrictions on access to forests and forest resources", "Unlimited access to all forests", "The end of all colonial laws", "The replacement of forests by universities", "A"),
        ("What is a moneylender?", "A person who lends money, often charging interest", "A person who only grows crops", "A village schoolteacher", "A forest ranger only", "A"),
        ("Why did some tribal farmers borrow money?", "To meet expenses, pay revenue or cope with hardship", "To buy modern aeroplanes", "To avoid all economic activity", "To become colonial governors", "A"),
        ("What is a plantation?", "A large area used to grow a particular commercial crop", "A place used only for military training", "A village court", "A royal library", "A"),
        ("Which crop was widely grown on plantations in parts of colonial India?", "Tea", "Wheat only", "Millets only", "Rice only", "A"),
        ("What was a common colonial goal behind expanding commercial agriculture?", "Producing crops for markets and trade", "Ending all international trade", "Eliminating every market", "Stopping all agricultural production", "A"),
        ("What is a forest reserve?", "A forest area placed under particular legal controls", "A modern shopping centre", "A type of village school", "A privately owned aeroplane", "A"),
        ("What is a customary right?", "A right based on long-established community practices", "A right that exists only on social media", "A right granted only to foreign traders", "A modern railway ticket", "A"),
        ("Which region is associated with the Munda community?", "Chotanagpur region", "Thar Desert only", "Malabar coast only", "Andaman Sea only", "A"),
        ("Which region is strongly associated with the Santhal rebellion?", "The Santhal Parganas region", "The Kashmir Valley only", "The Konkan coast only", "The Nilgiri Hills only", "A"),
        ("What was one common reason tribal communities resisted colonial rule?", "Loss of land, forest access and traditional rights", "Too many opportunities to govern Britain", "The introduction of universal free travel", "The end of all outside interference", "A"),
        ("Who were outsiders sometimes called 'dikus' in accounts of tribal resistance?", "People viewed as outsiders, including exploitative moneylenders or traders", "Only tribal elders", "Only village children", "Only forest animals", "A"),
        ("What was a zamindar?", "A landholder or revenue intermediary in certain land systems", "A tribal dance", "A forest product", "A type of plantation crop", "A"),
        ("Why were forests important to many tribal communities?", "They provided food, materials, livelihoods and cultural resources", "They were used only for royal hunting", "They had no economic value", "They prevented every form of settlement", "A"),
        ("What is a rebellion?", "An organised act of resistance against an authority", "A routine market transaction", "A type of agricultural season", "A royal wedding", "A"),
        ("What was the broad aim of many tribal uprisings against colonial rule?", "To resist exploitation and defend land, livelihood or customary rights", "To establish British control over more forests", "To end all community traditions", "To abolish every local language", "A"),
        ("What is an oral tradition?", "Knowledge or history passed down through spoken accounts", "A printed government tax receipt", "A modern computer database", "A railway timetable", "A"),
        ("What is meant by land alienation?", "The loss of land by people or communities to others", "The improvement of soil fertility", "The creation of a forest reserve", "The building of a village school", "A"),
        ("What is one way historians learn about tribal resistance?", "By studying records, oral histories, community traditions and other evidence", "By using only modern weather reports", "By ignoring all local accounts", "By relying only on fictional stories", "A"),
        ("Why is the history of tribal communities important?", "It helps explain diverse experiences of colonialism and resistance", "It only describes European royal families", "It has no connection to Indian history", "It deals exclusively with modern technology", "A"),
    ],

    "Medium": [
        ("How did colonial rule change the relationship between many tribal communities and forests?", "New laws and restrictions often limited traditional forest access", "All forest access became unrestricted", "Forests stopped providing any resources", "Tribal communities were given complete control of every forest", "A"),
        ("Why did colonial authorities classify and regulate forests?", "To control forest resources and secure supplies such as timber", "To eliminate all commercial forestry", "To make every forest a farming village", "To stop the use of timber completely", "A"),
        ("How could restrictions on shifting cultivation affect tribal communities?", "They could disrupt established farming practices and livelihoods", "They always increased available farmland", "They eliminated every tax", "They made forest access unlimited", "A"),
        ("Why did moneylenders become a source of resentment in some tribal areas?", "Debt and high interest could lead to the loss of land or greater dependence", "They always lent money without repayment", "They were all tribal community leaders", "They abolished colonial revenue demands", "A"),
        ("How did commercial farming affect some tribal communities?", "It could shift land use toward market crops and affect customary livelihoods", "It ended all trade and markets", "It guaranteed equal land ownership for everyone", "It made forests unnecessary for every community", "A"),
        ("Why did British officials sometimes recruit tribal people for plantation or other labour?", "Colonial enterprises needed workers for commercial production", "Tribal people were prohibited from all forms of work", "Plantations did not require workers", "The British had ended commercial agriculture", "A"),
        ("What was one consequence of plantation expansion in colonial India?", "Land and labour were increasingly directed toward commercial crops", "All farming disappeared", "All workers became independent landowners", "Every forest was returned to community control", "A"),
        ("Why was the Santhal rebellion of 1855–56 significant?", "It challenged exploitative practices and colonial authority in the Santhal region", "It established the Mughal Empire", "It ended British rule throughout India", "It founded the Indian National Congress", "A"),
        ("What were Sidhu and Kanhu Murmu known for?", "Leading the Santhal rebellion", "Building the Taj Mahal", "Founding the Delhi Sultanate", "Introducing the Doctrine of Lapse", "A"),
        ("Why is Birsa Munda remembered?", "He led a movement challenging colonial authority and exploitation in the Munda region", "He served as the first Viceroy of India", "He founded the East India Company", "He led the revolt at Meerut in 1857", "A"),
        ("What were some aims of the Munda movement under Birsa Munda?", "To challenge exploitation and restore rights and autonomy associated with Munda society", "To expand British control over tribal lands", "To establish plantation companies", "To abolish all tribal customs", "A"),
        ("How did the spread of moneylending affect land ownership in some tribal areas?", "Debt could contribute to the transfer or loss of land", "It guaranteed that all land stayed with cultivators", "It ended all economic inequality", "It prevented outsiders from entering villages", "A"),
        ("Why did colonial land and revenue policies create tension?", "They could impose new demands and disrupt established relationships with land", "They eliminated all obligations on cultivators", "They prevented the collection of any revenue", "They gave every community identical legal rights in practice", "A"),
        ("What role did tribal chiefs sometimes play under colonial rule?", "Their authority and responsibilities could be altered by colonial administration", "They always retained complete independence", "They became elected members of the British Parliament", "They were never involved in local governance", "A"),
        ("How could the designation of forests as reserved areas affect local people?", "Activities such as grazing, collecting produce and cultivation could become restricted", "Every traditional activity became automatically legal", "All forests were converted to private homes", "It removed all colonial control", "A"),
        ("Why did some tribal people migrate for wage labour?", "Land loss, debt and changes in access to resources could make local livelihoods difficult", "Every tribal household received a guaranteed government salary", "Migration was required only for royal ceremonies", "No employment existed outside tribal villages", "A"),
        ("What is the significance of oral histories in studying tribal movements?", "They can preserve community perspectives that official records may omit", "They are always identical to official records", "They cannot contain historical information", "They replace the need to evaluate evidence", "A"),
        ("Why should colonial records be read critically?", "They may reflect the priorities and assumptions of colonial officials", "They are always entirely neutral", "They never mention tribal communities", "They were all written after independence", "A"),
        ("How could railways and expanding markets affect forest regions?", "They could increase demand for timber and commercial resources", "They ended all demand for forest products", "They prevented trade between regions", "They guaranteed community ownership of all land", "A"),
        ("Why did the meaning of land differ between some tribal communities and colonial authorities?", "Customary community relationships could differ from formal individual or state-based land systems", "Every community used identical ownership rules", "Land had no cultural or economic importance", "Colonial laws always matched local customs exactly", "A"),
        ("What was one common feature of tribal resistance movements?", "They responded to local forms of exploitation and threats to customary life", "They all followed one central national organisation", "They all began in the same year", "They had no connection to land or livelihood", "A"),
        ("Why is it inaccurate to assume all tribal communities had identical livelihoods?", "Communities differed according to region, environment, economy and social traditions", "Every community lived only by hunting", "Every community lived only in cities", "All communities followed the same farming system", "A"),
        ("How did colonial commercial interests influence forest policy?", "Forests were increasingly managed to meet state and commercial demands", "Forests were never used for timber", "Commercial interests had no influence on administration", "All forest laws were abolished", "A"),
        ("What was one effect of debt on tribal cultivators?", "It could increase dependence on creditors and threaten land security", "It guaranteed permanent financial independence", "It removed every obligation to repay loans", "It eliminated differences in wealth", "A"),
        ("Why did some tribal communities oppose outsiders entering their lands?", "Outsiders could be associated with land loss, debt, exploitation or changes to customary rights", "Every outsider always provided free land", "Outsiders never participated in local economies", "All communities rejected every form of trade", "A"),
        ("How did tribal resistance contribute to Indian history?", "It revealed local opposition to colonial power and exploitation", "It had no political or social significance", "It only supported colonial expansion", "It ended every conflict immediately", "A"),
        ("What can the Munda and Santhal movements demonstrate when studied together?", "Different tribal communities organised resistance in response to particular regional grievances", "They were one identical movement led by the same person", "They both began after Indian independence", "They had no connection to colonial policies", "A"),
        ("Why did colonial governments sometimes respond to tribal uprisings with new rules?", "Resistance could expose problems in existing administration and prompt policy changes", "They always abolished all laws immediately", "They permanently withdrew from India", "They stopped recording any events", "A"),
        ("What is an important difference between a forest and a plantation?", "A plantation is generally organised for growing selected crops commercially, while forests contain broader ecosystems and resources", "They are always exactly the same", "A plantation can never grow trees", "A forest contains no living organisms", "A"),
        ("What is a balanced approach to studying tribal resistance?", "Consider community aims, local conditions, colonial policies and different historical sources", "Assume every movement had identical goals", "Rely only on the accounts of colonial officials", "Ignore regional differences", "A"),
    ],

    "Hard": [
        ("Which explanation best describes the roots of many tribal uprisings under colonial rule?", "The interaction of land alienation, forest restrictions, debt, labour demands and threats to customary authority", "A single issue affected every community in the same way", "Tribal communities had no economic or political interests", "The uprisings were unrelated to colonial rule", "A"),
        ("Why is it important to distinguish customary access to land from formal legal ownership?", "Community rights and practices could be poorly represented by colonial property rules", "Customary access always meant private ownership under modern law", "Formal ownership had no impact on land disputes", "All communities used identical legal categories", "A"),
        ("How did colonial forest management reflect the priorities of the state?", "It often prioritised administrative control and commercially valuable forest resources", "It always placed every forest under unrestricted community control", "It eliminated the demand for timber", "It removed all state interest in natural resources", "A"),
        ("Why could restrictions on shifting cultivation create both economic and cultural disruption?", "They affected food production and practices connected to community knowledge and land use", "They changed only the names of villages", "They guaranteed unlimited agricultural land", "They had no impact on livelihood", "A"),
        ("What does the Santhal rebellion reveal about the relationship between local exploitation and colonial power?", "Resistance could target both exploitative intermediaries and the authority that supported the prevailing system", "All participants opposed only modern technology", "The rebellion established British rule", "It had no relationship to land or debt", "A"),
        ("Why should the Santhal rebellion not be interpreted solely as a military event?", "It also reflected grievances about land, debt, outsiders and the colonial administrative order", "It involved no social grievances", "It had no connection to local livelihoods", "Its participants were all British officials", "A"),
        ("How did Birsa Munda's movement combine social and political concerns?", "It challenged exploitation while calling for the restoration of rights and community autonomy", "It focused exclusively on building modern factories", "It supported unrestricted colonial land transfers", "It had no connection to Munda society", "A"),
        ("Why is the concept of 'dikus' historically important in accounts of some tribal movements?", "It expressed perceptions of outsiders associated with exploitation and threats to customary life", "It was the official title of every tribal chief", "It referred only to forest animals", "It was a type of British currency", "A"),
        ("How could indebtedness create a cycle of vulnerability for tribal cultivators?", "Debt obligations could reduce economic independence and increase the risk of losing land or labour autonomy", "Debt always increased land ownership", "Creditors could never demand repayment", "Borrowing eliminated all social inequality", "A"),
        ("What was one structural effect of commercialisation in forest regions?", "Land, labour and forest resources could become more closely tied to wider markets and state revenue", "It eliminated every market connection", "It restored all customary rights automatically", "It prevented the extraction of timber", "A"),
        ("Why is it misleading to treat tribal communities as isolated from wider society?", "They interacted with traders, states, markets and neighbouring communities in different ways", "They had no contact with outsiders at any time", "They never traded goods", "They had no regional political relationships", "A"),
        ("How could colonial revenue demands contribute to land alienation?", "Cultivators facing payment pressures might borrow money or lose land through debt and related processes", "Revenue demands always protected every cultivator's land", "Land transfers were impossible under colonial rule", "Taxes had no connection to rural livelihoods", "A"),
        ("What is a key challenge in using colonial descriptions of tribal communities?", "Officials might classify communities through administrative assumptions that did not reflect all local perspectives", "Every official account included every community's viewpoint", "Colonial records never used categories", "Historical descriptions require no critical evaluation", "A"),
        ("Why should oral traditions and written documents be compared when possible?", "They may preserve different perspectives, memories and details about historical events", "One type of evidence is always completely accurate", "Oral traditions never change", "Written records cannot contain bias", "A"),
        ("How could the expansion of plantations affect labour relations?", "It could increase demand for wage workers and draw people away from established livelihoods", "It ended the need for workers", "It guaranteed every worker land ownership", "It abolished commercial agriculture", "A"),
        ("What does the history of forest laws reveal about state power?", "Legal control over forests could redefine who was permitted to use resources and how", "Law never affected access to natural resources", "Forests were outside all political systems", "All forest users had identical rights in every period", "A"),
        ("Why might tribal resistance movements have different outcomes in different regions?", "Local leadership, political conditions, resources and colonial responses varied", "Every region had identical conditions", "No movement had identifiable leaders", "All rebellions received the same military support", "A"),
        ("How did tribal movements challenge colonial ideas about authority?", "They asserted competing claims to land, customary rights and legitimate community leadership", "They accepted every colonial rule without question", "They had no political aims", "They focused only on European elections", "A"),
        ("Why is land alienation more than a simple transfer of property?", "It can affect livelihoods, community relationships, identity and access to resources", "It affects only the price of buildings", "It has no social consequences", "It always improves community autonomy", "A"),
        ("What is the strongest way to compare the Santhal and Munda movements?", "Identify shared concerns while recognising their distinct leaders, settings and historical aims", "Assume both movements were identical in every respect", "Ignore the regions in which they occurred", "Treat them as events after independence", "A"),
        ("How could state demand for timber alter forest ecosystems and community livelihoods?", "Commercial extraction and restrictive management could change forest use and access to resources", "Timber demand had no effect on forests", "Forest management always increased customary access", "Commercial extraction prevented every environmental change", "A"),
        ("Why should colonialism be analysed as more than foreign political rule?", "It also reshaped economic relations, land systems, labour and access to natural resources", "It affected only the identity of the ruler", "It had no impact on local economies", "It never changed laws or administration", "A"),
        ("What does resistance to moneylenders and landlords reveal about rural power relations?", "Economic dependence could overlap with unequal social and political authority", "Debt was unrelated to social relationships", "All cultivators had equal resources", "Creditors had no influence on rural life", "A"),
        ("Why might a colonial government introduce administrative changes after an uprising?", "It might seek to address unrest, strengthen control or reduce the likelihood of future resistance", "Every uprising immediately ended colonialism", "Governments never changed policy after unrest", "Administrative changes were unrelated to political stability", "A"),
        ("How did tribal histories broaden the understanding of anti-colonial resistance?", "They show that opposition developed through diverse local struggles as well as wider political movements", "They prove resistance occurred only in major cities", "They show that colonial rule faced no opposition", "They remove the importance of local history", "A"),
        ("What is the main danger of describing all tribal communities as one uniform group?", "It overlooks differences in language, livelihood, social organisation and historical experience", "It makes every regional distinction more accurate", "It proves every community had identical customs", "It removes all need for historical research", "A"),
        ("Why is the term 'tribal' itself best used with historical care?", "Communities grouped under the term have diverse identities and experiences that broad labels may obscure", "It identifies one identical culture across India", "It means every community had the same livelihood", "It has no relationship to historical classification", "A"),
        ("What is a balanced interpretation of the long-term effects of colonial forest policy?", "Its effects varied, but many policies restricted customary use and strengthened state control over forests", "Every policy had identical effects in every region", "No community was affected", "All forest restrictions ended immediately in 1857", "A"),
        ("How can historians avoid romanticising tribal resistance?", "Study its documented aims, internal diversity, local conditions and consequences critically", "Assume every movement was identical and flawless", "Ignore all community accounts", "Treat every colonial report as unquestionably correct", "A"),
        ("Which statement best summarises the significance of colonialism and tribal societies in Indian history?", "Colonial changes to land, forests, labour and authority prompted diverse forms of tribal adaptation and resistance", "Tribal communities had no history before colonial rule", "Colonial rule left every community unchanged", "All tribal movements began after 1947", "A"),
    ],
}


def main():
    db = SessionLocal()
    total_added = 0

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "Colonialism and Tribal Societies",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if not lesson:
            print("ERROR: Lesson 'Colonialism and Tribal Societies' was not found.")
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
            print("SUCCESS: Colonialism and Tribal Societies has all 90 questions!")
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