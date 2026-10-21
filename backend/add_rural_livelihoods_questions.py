import os
import logging
import random
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
        ("What is a common occupation in rural India?", "Farming", "Airline piloting", "Stock trading only", "Shipbuilding only", "A"),
        ("Who is an agricultural labourer?", "A person who works on farms for wages", "A person who owns an airline", "A person who runs a cinema", "A person who pilots ships", "A"),
        ("What is subsistence farming?", "Farming mainly to meet a family's needs", "Farming only for export", "Growing crops without land", "Selling factory machinery", "A"),
        ("Who is a small farmer?", "A farmer cultivating a relatively small area of land", "A person who owns a large airline", "A city bus conductor", "A factory manager", "A"),
        ("Which activity is related to animal husbandry?", "Rearing cattle", "Repairing mobile phones", "Operating trains", "Printing newspapers", "A"),
        ("What is a daily-wage worker?", "A worker paid according to days worked", "A person who receives only school marks", "A person who owns a bank", "A person who works only as a volunteer", "A"),
        ("Which is a crop grown by many Indian farmers?", "Rice", "Plastic", "Steel", "Petrol", "A"),
        ("What do farmers need to grow crops?", "Seeds, water and suitable soil", "Cinema tickets", "Railway timetables", "Computer passwords only", "A"),
        ("What is irrigation?", "Supplying water to crops", "Harvesting fish in every case", "Building a railway station", "Selling household furniture", "A"),
        ("What is harvesting?", "Collecting mature crops", "Planting a school building", "Repairing a bus", "Measuring city traffic", "A"),
        ("Who is a landless agricultural labourer?", "A farm worker who does not own agricultural land", "A person who owns many farms", "A factory owner", "A government minister", "A"),
        ("Which animal is commonly reared for milk?", "Cow", "Tiger", "Lion", "Crocodile", "A"),
        ("What is a rural livelihood?", "A way people earn a living in rural areas", "A city traffic signal", "An international airport", "A computer operating system", "A"),
        ("Which activity can supplement a rural family's farm income?", "Poultry rearing", "Space tourism", "Operating an international airport", "Manufacturing aircraft engines only", "A"),
        ("What is a market used for by farmers?", "Buying inputs and selling produce", "Conducting school examinations", "Issuing passports", "Predicting earthquakes exactly", "A"),
        ("What is a crop?", "Plants grown for food or other useful products", "A type of railway ticket", "A city building permit", "A household appliance", "A"),
        ("Which resource is important for farming?", "Land", "Cinema screens", "Traffic lights", "Airline tickets", "A"),
        ("What does a farmer usually do during sowing?", "Places seeds in the soil", "Collects only finished products", "Repairs city roads", "Issues birth certificates", "A"),
        ("What is livestock?", "Farm animals raised for useful products or work", "Wild planets", "Factory machines", "Road vehicles only", "A"),
        ("Which is an example of a non-farm rural occupation?", "Pottery making", "Growing rice", "Harvesting wheat", "Sowing seeds", "A"),
        ("Why do many rural families need income?", "To meet daily household needs", "To avoid buying food forever", "To stop all agricultural activity", "To eliminate every village service", "A"),
        ("What is a dairy activity?", "Producing and selling milk", "Mining coal only", "Building roads only", "Printing school textbooks", "A"),
        ("Which is a common agricultural input?", "Fertiliser", "Cinema ticket", "Bus pass", "Mobile ringtone", "A"),
        ("What is a farmer's produce?", "Goods obtained from farming", "A school attendance sheet", "A traffic fine", "A railway signal", "A"),
        ("What is fishing as a livelihood?", "Earning income by catching or raising fish", "Earning income by issuing passports", "Repairing only farm roads", "Teaching only mathematics", "A"),
        ("Why do some rural workers migrate for work?", "To find employment and income opportunities", "Because all rural jobs are illegal", "To stop earning income", "To avoid every form of travel", "A"),
        ("What is a harvest season?", "A period when particular crops are ready to be collected", "A national election period", "A school holiday in every state", "A period when roads disappear", "A"),
        ("Which activity can provide rural employment?", "Handloom weaving", "International spaceflight only", "Operating a foreign embassy", "Printing currency", "A"),
        ("What is a farmer's income?", "Money earned from farming and related activities", "The weight of a tractor", "The length of a field", "The number of village roads", "A"),
        ("What is one reason rural families keep livestock?", "For products such as milk and eggs or other useful purposes", "To produce mobile phones", "To operate airports", "To print books", "A"),
    ],

    "Medium": [
        ("Why may agricultural labourers have seasonal employment?", "Farm work demand changes across the crop cycle", "All crops grow at exactly the same time", "Labourers can work only in cities", "Farming never requires workers", "A"),
        ("Why can irrigation improve crop production?", "It supplies water when rainfall is insufficient", "It eliminates the need for seeds", "It guarantees that crops never get diseases", "It makes soil unnecessary", "A"),
        ("Why might small farmers borrow money?", "To pay for inputs or meet household needs", "To avoid all agricultural work", "To purchase every village road", "To eliminate rainfall", "A"),
        ("How can dependence on a single crop affect a farmer?", "Income may suffer if that crop fails or prices fall", "Income is guaranteed in every season", "Weather can no longer affect the farm", "The farmer never needs a market", "A"),
        ("Why do farmers sell crops in markets?", "To earn money from their produce", "To prevent crops from being harvested", "To stop all trade", "To replace all farming tools", "A"),
        ("How can dairy farming diversify rural income?", "It can provide income in addition to crop farming", "It guarantees that crops never fail", "It eliminates animal-care costs", "It makes every family landless", "A"),
        ("Why might a farmer need credit before planting?", "Seeds, fertilisers and labour may require upfront payment", "Crops always produce immediate cash", "Farming requires no inputs", "Credit automatically increases rainfall", "A"),
        ("What is one advantage of cooperative farming or marketing?", "Farmers may share resources or improve their bargaining position", "Every member is guaranteed the same profit", "It removes the need for management", "It makes markets unnecessary", "A"),
        ("How can storage facilities benefit farmers?", "They can help reduce losses and allow more flexible selling", "They guarantee unlimited crop prices", "They eliminate every pest", "They make harvesting unnecessary", "A"),
        ("Why may women contribute significantly to rural livelihoods?", "They participate in farming, livestock care and other economic activities", "They are legally unable to perform rural work", "They never contribute to household income", "They only work in urban offices", "A"),
        ("What can happen when crop prices fall sharply?", "Farmers' earnings may decrease", "Every farmer's income doubles", "Input costs always become zero", "Crop production becomes unnecessary", "A"),
        ("Why do some rural workers undertake non-farm work?", "To diversify income and find additional employment", "To make agriculture illegal", "To avoid every economic activity", "To guarantee that no skills are needed", "A"),
        ("What is a possible benefit of a self-help group?", "Members can save together and access group-based financial support", "Every member receives unlimited money", "It eliminates all financial risk", "It replaces every public institution", "A"),
        ("Why can drought affect rural livelihoods?", "It may reduce water availability and crop yields", "It guarantees a record harvest", "It makes irrigation unnecessary", "It increases soil moisture everywhere", "A"),
        ("How can skill training help rural workers?", "It can improve access to different employment opportunities", "It guarantees a government job for everyone", "It removes all competition", "It makes education unnecessary", "A"),
        ("Why may landless workers be economically vulnerable?", "They may depend on wages and have limited productive assets", "They always own large farms", "They receive guaranteed salaries from every employer", "They control all crop prices", "A"),
        ("What is one advantage of growing different crops?", "It may spread production and market risks", "It guarantees every crop will succeed", "It removes the need for water", "It prevents all pest attacks", "A"),
        ("Why is access to rural roads important for farmers?", "It can help transport inputs and produce to markets", "It guarantees fixed crop prices", "It removes the need for buyers", "It prevents every weather hazard", "A"),
        ("What can be a consequence of high-interest informal borrowing?", "A household may struggle to repay its debt", "Debt disappears automatically", "All farm costs become zero", "Income is guaranteed to increase", "A"),
        ("How can government employment programmes help rural households?", "They may provide wage work under applicable programme rules", "They guarantee permanent employment for every resident", "They eliminate every form of poverty", "They replace all private employment", "A"),
        ("Why is access to agricultural information useful?", "It can help farmers make informed production decisions", "It guarantees that weather never changes", "It makes all seeds free", "It removes the need to consider local conditions", "A"),
        ("What is a likely effect of crop failure on a farm-dependent family?", "Reduced income and possible difficulty meeting expenses", "Automatic increase in savings", "Guaranteed debt cancellation", "No change in livelihood under any circumstances", "A"),
        ("How can food processing support rural livelihoods?", "It can create value-added products and employment", "It prevents all food spoilage without equipment", "It eliminates the need for markets", "It guarantees every business a profit", "A"),
        ("Why might farmers form producer organisations?", "To coordinate activities and strengthen collective market access", "To make all farmers grow one crop by law", "To remove every individual decision", "To eliminate buyers permanently", "A"),
        ("What can improve the bargaining power of small farmers?", "Collective selling and access to market information", "Selling without knowing prices", "Keeping all produce hidden", "Avoiding every form of cooperation", "A"),
        ("Why is livestock health important to rural households?", "Healthy animals support productivity and income", "It guarantees that animal care costs disappear", "It prevents all crop diseases", "It replaces all farm labour", "A"),
        ("How can rural crafts contribute to a household?", "They can provide income beyond agricultural work", "They guarantee year-round sales", "They eliminate the need for skills", "They make markets unnecessary", "A"),
        ("Why do rural livelihoods often depend on natural resources?", "Farming, fishing and livestock rely on land, water or ecosystems", "All rural work takes place in factories", "Natural resources never affect work", "Every household earns income from software only", "A"),
        ("What is one purpose of crop insurance?", "To provide eligible financial protection against specified losses", "To guarantee a fixed profit every year", "To prevent all weather events", "To remove all farming expenses", "A"),
        ("Why is timely payment important for agricultural labourers?", "Workers need wages to meet household expenses", "It changes the length of the growing season", "It guarantees free agricultural inputs", "It eliminates seasonal work", "A"),
    ],

    "Hard": [
        ("A small farmer loses much of a crop to drought and has an outstanding loan. What is a major livelihood risk?", "Lower earnings may make loan repayment and household spending difficult", "The loan is automatically cancelled in every case", "The farmer is guaranteed a higher crop price", "Drought eliminates all future farming costs", "A"),
        ("A village depends heavily on one cash crop whose market price fluctuates. What could reduce livelihood risk?", "Diversifying crops and income sources where feasible", "Increasing dependence on that crop alone", "Ignoring market information", "Selling all produce without comparing prices", "A"),
        ("Why can unequal access to land influence rural income inequality?", "Land ownership affects access to an important productive resource", "Land has no relationship to agricultural production", "Every household owns exactly the same land area", "Land ownership guarantees equal income", "A"),
        ("A farmer sells produce immediately after harvest at a low price because storage is unavailable. What might improve their options?", "Suitable storage and reliable market information", "Destroying unsold produce", "Avoiding all market information", "Increasing post-harvest losses", "A"),
        ("How might climate variability affect households that rely only on rain-fed farming?", "Changing rainfall can make yields and income less predictable", "It guarantees identical yields each year", "It removes the need for water management", "It prevents all crop diseases", "A"),
        ("A household combines crop farming, dairy and craft production. What is a likely benefit?", "Multiple income sources may reduce dependence on one activity", "Every income source is guaranteed to succeed", "The household no longer needs market access", "All production costs disappear", "A"),
        ("Why can indebtedness persist even after a farmer receives income from one harvest?", "Earnings may not cover debts, interest and household costs", "Every loan must be cancelled after harvest", "Harvest income is always unlimited", "Interest never affects repayment", "A"),
        ("How can access to institutional credit differ from borrowing from an informal lender?", "Terms, interest rates and safeguards may differ", "Institutional credit is always free", "Informal loans can never charge interest", "Both always have identical conditions", "A"),
        ("A rural worker wants to move from seasonal farm work into food processing. What could help?", "Relevant training and access to suitable employment opportunities", "Avoiding all skill development", "Relying only on crop prices", "Removing all local transport", "A"),
        ("Why may a rise in agricultural output fail to improve every rural household's income equally?", "Benefits depend on land access, wages, costs and market conditions", "All rural households receive identical crop profits", "Output has no relationship to rural work", "Higher output automatically eliminates inequality", "A"),
        ("A farmer group negotiates with buyers and arranges collective transport. What is a potential advantage?", "Lower per-unit transport costs or improved bargaining may be possible", "All members are guaranteed identical earnings", "Buyers become unnecessary", "Market risks disappear completely", "A"),
        ("Why can unpaid family work be overlooked when measuring rural livelihoods?", "It may contribute to production without appearing as a direct wage", "It never contributes to economic activity", "It is always paid at a fixed rate", "It eliminates household production", "A"),
        ("A village's groundwater is declining due to intensive irrigation. What is a sustainable response?", "Improve water management and consider suitable water-efficient practices", "Increase extraction without monitoring", "Ignore future water availability", "Stop maintaining all irrigation systems", "A"),
        ("How can a rural employment programme affect a household during a poor agricultural season?", "It may provide additional wage income when eligible work is available", "It guarantees permanent work to every person", "It prevents all crop losses", "It replaces every household livelihood permanently", "A"),
        ("Why is timely access to weather forecasts valuable to farmers?", "It can inform decisions about sowing, irrigation and harvesting", "It makes weather completely predictable", "It guarantees every crop's success", "It removes all market uncertainty", "A"),
        ("A rural family depends on fishing, but declining fish stocks reduce catches. What is a possible long-term response?", "Support sustainable resource management and explore feasible supplementary livelihoods", "Increase harvesting without limits", "Ignore the resource decline", "Assume catches will always recover immediately", "A"),
        ("Why might small farmers receive a low share of the final retail price?", "Intermediary costs, bargaining power and market structure can affect their share", "Farmers always set the final retail price", "Retail prices never include transport costs", "All farmers sell directly to consumers", "A"),
        ("How can access to education influence rural livelihoods over time?", "It can expand skills and access to a wider range of jobs", "It guarantees every graduate a high-paying job", "It removes all economic uncertainty", "It makes agricultural skills worthless", "A"),
        ("A farmer adopts an expensive new technology without checking whether it suits local conditions. What is the main concern?", "Costs and performance may not match the farm's needs", "Technology always guarantees higher profits", "Local conditions never affect farming", "The farmer will never need maintenance", "A"),
        ("Why can women's access to land and credit matter for rural development?", "It can influence their ability to invest, produce and earn income", "It has no relationship to economic participation", "It guarantees identical earnings in every household", "It removes every market risk", "A"),
        ("A region experiences repeated crop failures. Why is relying on emergency relief alone insufficient for long-term resilience?", "Long-term measures may also be needed to reduce future vulnerability", "Emergency relief always prevents future drought", "Relief makes water planning unnecessary", "Repeated crop failure has no effect on households", "A"),
        ("How can local processing facilities affect rural employment?", "They may create jobs and increase the value added locally", "They guarantee that every product sells", "They eliminate the need for electricity", "They prevent all transport costs", "A"),
        ("Why should livelihood programmes consider local skills and resources?", "Programmes are more likely to fit the area's practical opportunities and needs", "Every village has identical resources", "Local skills never affect outcomes", "A single activity suits every household", "A"),
        ("A household borrows to buy livestock but lacks veterinary access. What risk should it consider?", "Animal illness may reduce productivity and threaten repayment", "Livestock never become ill", "Veterinary care is never relevant", "Borrowing guarantees a profit", "A"),
        ("How can reliable transport infrastructure benefit rural producers?", "It can improve access to markets, services and inputs", "It fixes crop prices permanently", "It removes the need for buyers", "It guarantees every shipment is profitable", "A"),
        ("Why should rural development assess both income and livelihood security?", "Income alone may not capture vulnerability, stability and access to essential resources", "Income is unrelated to living conditions", "Livelihood security means having no work", "Security guarantees every family equal income", "A"),
        ("A village begins producing a crop that requires more water than is locally available. What should be evaluated?", "Water availability, environmental effects and long-term production feasibility", "Only the crop's appearance", "Whether the crop is popular elsewhere", "How quickly the village can ignore water limits", "A"),
        ("What is a potential benefit of linking farmers to current market-price information?", "It can help them compare selling options and negotiate more effectively", "It guarantees the highest possible price", "It eliminates every middleman", "It prevents all price fluctuations", "A"),
        ("Why might livelihood diversification be especially important for landless labourers?", "It can create alternatives when agricultural wage work is unavailable", "It guarantees permanent employment", "It eliminates all skill requirements", "It makes seasonal demand irrelevant", "A"),
        ("Which approach best supports resilient rural livelihoods?", "Combining suitable skills, resource management, market access and diversified income", "Depending on one activity without planning", "Ignoring debt and natural-resource limits", "Avoiding training and market information", "A"),
    ],
}


def main():
    db = SessionLocal()

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "Rural Livelihoods",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if not lesson:
            print("ERROR: Rural Livelihoods lesson was not found.")
            print("Check the exact lesson title and topic.")
            return

        print(f"Lesson found: {lesson.title} (ID: {lesson.id})")
        total_added = 0

        for difficulty in ["Easy", "Medium", "Hard"]:
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
                    title=f"Rural Livelihoods - {difficulty}",
                    difficulty=difficulty,
                )
                db.add(quiz)
                db.flush()

            existing = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .all()
            )

            existing_text = {
                q.question.strip().lower() for q in existing
            }

            if len(existing) >= 30:
                print(
                    f"{difficulty}: already has {len(existing)} "
                    "questions; skipped."
                )
                continue

            added = 0

            for question, a, b, c, d, correct_letter in QUESTION_BANK[difficulty]:
                if len(existing) + added >= 30:
                    break

                if question.strip().lower() in existing_text:
                    continue

                options = [
                    ("A", a),
                    ("B", b),
                    ("C", c),
                    ("D", d),
                ]

                correct_text = dict(options)[correct_letter]
                random.shuffle(options)
                shuffled = [value for _, value in options]
                new_correct = "ABCD"[shuffled.index(correct_text)]

                db.add(
                    Question(
                        quiz_id=quiz.id,
                        question=question,
                        option_a=shuffled[0],
                        option_b=shuffled[1],
                        option_c=shuffled[2],
                        option_d=shuffled[3],
                        correct_answer=new_correct,
                    )
                )

                existing_text.add(question.strip().lower())
                added += 1

            db.flush()
            total_added += added
            print(
                f"{difficulty}: added {added} questions "
                f"({len(existing) + added}/30 total)."
            )

        db.commit()

        print("\nFINAL VERIFICATION")
        grand_total = 0

        for difficulty in ["Easy", "Medium", "Hard"]:
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
                if quiz else 0
            )

            grand_total += count
            print(f"{difficulty}: {count}/30")

        print(f"Total: {grand_total}/90")
        print(f"New questions added: {total_added}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()