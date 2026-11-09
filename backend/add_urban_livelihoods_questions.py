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
        ("What is a common source of livelihood in a city?", "Street vending", "Growing rice in every household", "Fishing in every street", "Forest gathering only", "A"),
        ("Who is a street vendor?", "A person who sells goods in public places", "A person who manages a court", "A person who flies aircraft", "A person who grows only forest trees", "A"),
        ("What does a construction worker do?", "Helps build or repair structures", "Issues passports", "Teaches every school subject", "Controls rainfall", "A"),
        ("Who is a domestic worker?", "A person employed to perform household work", "A person who commands the army", "A person who operates a satellite", "A person who runs a court", "A"),
        ("Which is an example of a service occupation?", "Driving a taxi", "Growing wheat on a farm", "Harvesting paddy", "Rearing cattle only", "A"),
        ("What is a daily-wage worker?", "A worker paid according to the days worked", "A person paid only in school marks", "A person who never works", "A person who owns every factory", "A"),
        ("Who is a vendor?", "A person who sells goods", "A person who writes laws only", "A person who repairs aircraft only", "A person who teaches farming only", "A"),
        ("Which job helps keep city streets clean?", "Sanitation worker", "Airline pilot", "Forest ranger only", "Ship captain", "A"),
        ("What does a delivery worker do?", "Transports goods to customers", "Grows crops in every case", "Makes court judgments", "Conducts elections", "A"),
        ("What is a livelihood?", "A way of earning a living", "A type of building", "A transport signal", "A school examination", "A"),
        ("Who is a factory worker?", "A person employed in production or factory operations", "A person who only grows crops", "A person who issues court orders", "A person who manages rainfall", "A"),
        ("What is self-employment?", "Working for oneself rather than as an employee", "Never earning an income", "Working only for a school grade", "Receiving wages from every employer", "A"),
        ("Which is a common urban transport occupation?", "Auto-rickshaw driver", "Paddy farmer only", "Forest gatherer only", "Fisherman on every street", "A"),
        ("What does a shop assistant generally do?", "Helps customers and sells products", "Builds every national highway", "Issues driving licences", "Grows crops in a field", "A"),
        ("Who is a security guard?", "A person employed to help protect premises", "A person who sells vegetables only", "A person who harvests rice", "A person who manages rainfall", "A"),
        ("Which activity can provide income in an urban area?", "Tailoring clothes", "Growing crops in every apartment", "Harvesting a forest in every street", "Mining in every home", "A"),
        ("What is a formal job generally associated with?", "Defined employment arrangements and applicable rules", "No responsibilities or conditions", "Always unpaid work", "No employer or agreement in any case", "A"),
        ("Who may repair household electrical wiring?", "An electrician", "A street sweeper only", "A bus passenger", "A shop customer", "A"),
        ("What is a small business?", "A business operating on a relatively small scale", "A national parliament", "A public highway", "A school examination board", "A"),
        ("Who is a waste collector?", "A worker who collects waste for disposal or processing", "A person who issues court judgments", "A person who flies a plane", "A person who grows every crop", "A"),
        ("Why do people work in cities?", "To earn income and meet their needs", "To avoid all expenses", "To make employment unnecessary", "To stop all economic activity", "A"),
        ("What does a plumber do?", "Installs or repairs water pipes and fittings", "Repairs only railway engines", "Grows vegetables only", "Issues tax laws", "A"),
        ("Which occupation is associated with a market?", "Selling vegetables", "Piloting a spacecraft", "Conducting a court trial", "Issuing a passport", "A"),
        ("Who is a rickshaw driver?", "A person who transports passengers by rickshaw", "A person who repairs only computers", "A person who teaches in every school", "A person who manages a bank", "A"),
        ("What is an employer?", "A person or organisation that hires workers", "A customer in every transaction", "A school textbook", "A public road", "A"),
        ("Which worker may be employed at a restaurant?", "Cook", "Patwari only", "Forest officer only", "Crop inspector only", "A"),
        ("What is a wage?", "Payment made to a worker for work", "A type of building material", "A city boundary", "A school timetable", "A"),
        ("What is unemployment?", "A situation in which a person seeking work cannot find it", "A guaranteed salary increase", "A type of transport", "A form of paid leave", "A"),
        ("Which is a common urban service?", "Laundry service", "Harvesting rice in every street", "Fishing in every building", "Mining in every apartment", "A"),
        ("Why are workers important to urban life?", "They provide goods and services people need", "They make all services unnecessary", "They eliminate every city expense", "They stop all business activity", "A"),
    ],

    "Medium": [
        ("Why might a street vendor's income change from day to day?", "Customer demand and selling conditions may vary", "The vendor receives the same guaranteed salary in every case", "Weather can never affect sales", "All goods always sell at the same rate", "A"),
        ("What is a major difference between regular salaried work and casual work?", "Regular salaried work may provide more predictable pay arrangements", "Casual work always pays more", "Salaried workers never have responsibilities", "Casual workers are never paid", "A"),
        ("Why can urban informal workers face financial uncertainty?", "Their work and earnings may be irregular", "They always receive guaranteed pensions", "Their income cannot change", "They never depend on customers", "A"),
        ("How can skill training help an urban worker?", "It may improve access to different job opportunities", "It guarantees a high salary immediately", "It eliminates every employment requirement", "It prevents all competition", "A"),
        ("Why do some workers migrate from rural areas to cities?", "They seek employment or better earning opportunities", "All rural jobs are illegal", "Cities guarantee every migrant a permanent job", "Migration eliminates every living expense", "A"),
        ("What is one challenge faced by street vendors?", "Finding suitable selling space and dealing with changing demand", "Guaranteed sales of every item", "Unlimited storage everywhere", "No need to purchase stock", "A"),
        ("Why may a construction worker's employment be temporary?", "Work may depend on the duration of a project", "Construction projects never end", "Workers are never paid wages", "Every project uses the same workforce permanently", "A"),
        ("How can social security benefits help eligible workers?", "They may provide support during specified risks or life events", "They guarantee wealth to every worker", "They eliminate the need for employment", "They prevent every illness", "A"),
        ("Why is access to affordable housing important for urban workers?", "Housing costs affect the money available for other needs", "Housing has no effect on household budgets", "Every worker receives free housing", "It guarantees a promotion", "A"),
        ("What may happen when living costs rise but wages remain unchanged?", "Workers' purchasing power may decline", "Workers can automatically buy more", "All prices must fall", "Employment becomes unnecessary", "A"),
        ("Why might domestic workers be vulnerable to exploitation?", "They may have limited bargaining power or unclear work conditions", "They always control their employers", "They never depend on wages", "They are exempt from all workplace risks", "A"),
        ("How can a worker's identity documents help when seeking employment?", "They may support identity verification and access to services", "They guarantee every job application succeeds", "They replace all required skills", "They guarantee a fixed salary", "A"),
        ("Why can a small shop owner experience income fluctuations?", "Sales, operating costs and customer demand can change", "Business income is always fixed", "Shop owners have no expenses", "Customer behaviour never changes", "A"),
        ("What is a benefit of organising workers collectively?", "Workers may represent shared concerns more effectively", "Every worker receives an identical salary automatically", "All workplace disagreements disappear", "Employers become unnecessary", "A"),
        ("Why is workplace safety important for construction workers?", "It helps reduce the risk of injury and accidents", "It guarantees that accidents can never occur", "It removes the need for training", "It makes protective equipment unnecessary", "A"),
        ("How can digital payment systems benefit some urban workers?", "They can make receiving and tracking payments more convenient", "They guarantee higher wages", "They remove all transaction risks", "They eliminate every bank requirement", "A"),
        ("What is underemployment?", "Working fewer hours or below one's capacity or skills", "Receiving a guaranteed promotion", "Never seeking work", "Owning a business with unlimited income", "A"),
        ("Why might women in informal urban jobs face additional difficulties?", "Care responsibilities and unequal opportunities may limit their choices", "They are unable to perform any paid work", "They always earn more than every other worker", "They never need safe workplaces", "A"),
        ("What can a worker do if wages are unlawfully withheld?", "Seek help through appropriate workplace or legal channels", "Secretly destroy the employer's records", "Assume wages are never owed", "Stop keeping any employment evidence", "A"),
        ("Why are public transport services important for urban workers?", "They can help people reach workplaces and services", "They guarantee every passenger a job", "They eliminate all travel time", "They make all workplaces unnecessary", "A"),
        ("How can stable employment benefit a household?", "It can make income planning more predictable", "It guarantees that household expenses disappear", "It prevents every emergency", "It makes budgeting unnecessary", "A"),
        ("Why do some urban workers depend on daily customer demand?", "Their earnings may be linked to the number of jobs or sales completed", "They always receive a fixed monthly salary", "Their work is unrelated to customers", "Their income cannot change", "A"),
        ("What can contribute to child labour in some urban settings?", "Household poverty and limited access to education may contribute", "All children must work by law", "Education always causes child labour", "Every employer provides unlimited schooling", "A"),
        ("Why is access to education important for children in working households?", "It can support learning and future employment opportunities", "It guarantees a high salary immediately", "It removes all household expenses", "It makes every skill unnecessary", "A"),
        ("What is one challenge for waste pickers?", "Exposure to unsafe materials and uncertain earnings", "Guaranteed salaries in every case", "No need for protective equipment", "Unlimited access to safe storage", "A"),
        ("How can formalising a small enterprise potentially help its owner?", "It may improve access to certain services and recognised business arrangements", "It guarantees profit", "It eliminates all taxes in every case", "It removes every compliance requirement", "A"),
        ("Why might workers share accommodation in a city?", "To reduce individual housing costs", "To guarantee a higher wage", "To eliminate transport needs", "To avoid all household expenses", "A"),
        ("What is a possible effect of automation on urban livelihoods?", "Some tasks and job requirements may change", "Every job must disappear immediately", "No occupation can ever change", "All workers receive automatic promotions", "A"),
        ("Why is reliable childcare useful to working parents?", "It can help them balance employment and care responsibilities", "It guarantees a promotion", "It eliminates all work-related expenses", "It removes the need for safe workplaces", "A"),
        ("What can help improve conditions for informal workers?", "Access to relevant protections, services and fair work opportunities", "Removing every public service", "Preventing workers from organising", "Ignoring unsafe work conditions", "A"),
    ],

    "Hard": [
        ("A street vendor earns well on weekends but very little on weekdays. What is the most reasonable explanation?", "Customer traffic and demand may differ across days", "The vendor's income must be legally fixed", "All customers buy the same amount every day", "The vendor has no operating costs", "A"),
        ("An urban worker loses several days of income after an injury. What does this illustrate?", "Workers with irregular earnings may be vulnerable to income shocks", "Every worker automatically receives full wages during every absence", "Injuries always increase household income", "Daily wages are unrelated to work performed", "A"),
        ("Why can rising rent disproportionately affect low-income urban workers?", "Housing may consume a larger share of their limited income", "Low-income workers never pay rent", "Rent increases guarantee higher wages", "Housing costs do not affect living standards", "A"),
        ("A construction worker is repeatedly hired for short projects without predictable future work. What is the main employment concern?", "Income and employment continuity may be uncertain", "The worker has a guaranteed permanent position", "Project work never involves employment risk", "The worker receives unlimited paid leave", "A"),
        ("How can access to affordable healthcare support urban livelihoods?", "It can reduce barriers to treatment and help limit financial hardship", "It guarantees that workers never become ill", "It removes every employment risk", "It guarantees every worker a promotion", "A"),
        ("A vendor is displaced from a selling area without a suitable alternative. What livelihood effect may follow?", "The vendor may lose customers and income", "The vendor's sales are guaranteed to increase", "The vendor no longer needs a market", "All business costs disappear", "A"),
        ("Why should urban livelihood policies consider both employment and living costs?", "Having work does not necessarily ensure that income covers essential expenses", "Employment always guarantees financial security", "Living costs are identical for everyone", "Wages have no effect on living conditions", "A"),
        ("A household relies on one person's daily wages and has no savings. What increases its vulnerability?", "A short interruption in work can threaten essential spending", "Daily wages are always guaranteed", "The household has unlimited backup income", "Living costs cannot change", "A"),
        ("How can collective organisation help workers negotiate better conditions?", "It may strengthen their ability to raise common concerns", "It guarantees every demand is accepted", "It removes all differences between jobs", "It makes workplace rules unnecessary", "A"),
        ("Why might informal workers be missed by employment statistics?", "Irregular or unregistered work may be harder to capture fully", "Informal work never generates income", "Every informal worker is automatically registered", "Employment statistics include only business owners", "A"),
        ("A delivery worker is paid per completed order and faces high transport costs. What should be considered when evaluating earnings?", "Net income after relevant work-related expenses", "Gross payments alone in every case", "The number of nearby parks", "The worker's preferred colour", "A"),
        ("How can lack of written work terms create problems for a worker?", "Pay, duties and responsibilities may be harder to establish", "It guarantees higher wages", "It prevents every workplace dispute", "It makes evidence unnecessary", "A"),
        ("A worker has the required skills but cannot afford transport to interviews. What is the barrier?", "The cost of accessing employment opportunities", "A lack of all professional ability", "Guaranteed access to every job", "The absence of any city transport", "A"),
        ("Why can discrimination restrict access to urban livelihoods?", "It may prevent qualified people from receiving fair opportunities", "It guarantees equal pay in every situation", "It removes all employment competition", "It makes qualifications irrelevant in every case", "A"),
        ("A small business has high sales but still struggles financially. What should be examined?", "Operating costs, debts and profit margins", "Sales figures alone", "Only the business signboard", "The owner's favourite subject", "A"),
        ("How might affordable skills training affect informal workers over time?", "It may broaden opportunities to move into different or better-paid work", "It guarantees every trainee a permanent job", "It removes all hiring requirements", "It makes experience irrelevant", "A"),
        ("Why can inadequate sanitation affect workers' livelihoods?", "Illness and unsafe surroundings can disrupt work and household well-being", "Sanitation has no connection to health", "It guarantees higher wages", "It eliminates all transport costs", "A"),
        ("A city improves public transport but housing near workplaces remains unaffordable. What does this suggest?", "Different factors jointly influence workers' access to jobs and services", "Transport alone solves every livelihood problem", "Housing costs never affect workers", "All workers can move without constraints", "A"),
        ("Why should policies for street vendors consider both public access and livelihoods?", "Public-space management and workers' ability to earn both matter", "Vendors have no livelihood needs", "Public access is never relevant", "Every vendor must be given unlimited space", "A"),
        ("A worker receives irregular income and has high-interest debt. Why may budgeting alone not solve the problem?", "Income may be insufficient to cover necessary costs and debt payments", "Budgeting automatically increases wages", "Debt never affects cash flow", "Irregular income guarantees savings", "A"),
        ("How can social protection reduce livelihood vulnerability?", "It may provide support against specified risks such as illness or loss of income", "It prevents every possible hardship", "It guarantees wealth to all recipients", "It eliminates the need for employment", "A"),
        ("Why should urban planning include workers who commute from the outskirts?", "Their transport, housing and access needs affect the functioning of the city", "Only city-centre residents contribute to urban life", "Commuters never use public services", "Commuting has no effect on employment access", "A"),
        ("A worker's job is replaced by a new technology. What is a constructive response at the policy level?", "Support relevant retraining and pathways to new employment", "Assume every displaced worker will immediately find identical work", "Ban all forms of education", "Ignore changes in job requirements", "A"),
        ("Why might women workers need safe transport and workplaces?", "Safety concerns can affect access to and participation in employment", "Safety has no effect on job choices", "Every workplace is automatically safe", "Transport conditions never affect work attendance", "A"),
        ("What is a possible consequence when children work long hours instead of attending school?", "Their education and future opportunities may be harmed", "Their qualifications automatically increase", "All household poverty disappears", "They become legally exempt from education needs", "A"),
        ("How can access to banking or suitable financial services help some urban workers?", "It can support secure transactions and financial management", "It guarantees that no financial loss can occur", "It guarantees a loan to every applicant", "It removes all household expenses", "A"),
        ("Why can a city's economic growth coexist with insecure work for some residents?", "Economic gains may not be distributed equally across jobs and households", "Economic growth guarantees identical benefits to everyone", "Insecure work cannot exist in a city", "All jobs have identical pay and protections", "A"),
        ("A municipal policy removes informal work locations but offers no transition support. What is a key risk?", "Affected workers may lose income without a practical alternative", "Every worker automatically receives a new job", "All businesses become more profitable", "The policy guarantees improved wages", "A"),
        ("What should be considered when assessing whether an urban livelihood is sustainable?", "Income stability, working conditions, costs and longer-term opportunities", "One day's sales alone", "The worker's clothing colour", "Only the number of nearby buildings", "A"),
        ("Which approach best supports inclusive urban livelihoods?", "Combining fair work opportunities, relevant protections, skills and access to essential services", "Ignoring informal workers and living costs", "Relying only on temporary employment without safeguards", "Removing access to training and public transport", "A"),
    ],
}


def main():
    db = SessionLocal()

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "Urban Livelihoods",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if not lesson:
            print("ERROR: Urban Livelihoods lesson was not found.")
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
                    title=f"Urban Livelihoods - {difficulty}",
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

                options = [a, b, c, d]
                correct_text = options[ord(correct_letter) - ord("A")]
                random.shuffle(options)
                new_correct = "ABCD"[options.index(correct_text)]

                db.add(
                    Question(
                        quiz_id=quiz.id,
                        question=question,
                        option_a=options[0],
                        option_b=options[1],
                        option_c=options[2],
                        option_d=options[3],
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