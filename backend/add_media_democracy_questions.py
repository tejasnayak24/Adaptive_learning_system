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
        ("What is the main role of media in society?", "To share information", "To make laws", "To conduct elections", "To run courts", "A"),
        ("Which of these is an example of mass media?", "A newspaper", "A private diary", "A personal letter", "A school notebook", "A"),
        ("What does television commonly provide?", "News and entertainment", "Court judgments only", "Laws only", "Weather control", "A"),
        ("Which medium allows people to read news online?", "News website", "Blackboard only", "Wall clock", "Calculator", "A"),
        ("What is journalism mainly concerned with?", "Gathering and reporting information", "Building roads", "Manufacturing food", "Conducting medical surgery", "A"),
        ("What is democracy?", "Government in which people participate in choosing leaders", "Rule by one hereditary monarch only", "Government without laws", "Rule by the military only", "A"),
        ("Why is media important in a democracy?", "It informs citizens about public issues", "It replaces all courts", "It appoints every judge", "It writes every law directly", "A"),
        ("What is a newspaper?", "A publication that reports news and information", "A type of voting machine", "A government court", "A transport service", "A"),
        ("Which is a form of digital media?", "Online news portal", "Printed stone tablet only", "Handwritten personal diary", "Classroom attendance register", "A"),
        ("What is an advertisement intended to do?", "Promote a product, service, or idea", "Conduct a court trial", "Count votes officially", "Make constitutional amendments", "A"),
        ("What is public opinion?", "The views held by members of the public", "The decision of one person only", "A weather report", "A court building", "A"),
        ("Which source can provide breaking news quickly?", "News websites", "Old school textbooks only", "Personal diaries only", "Printed maps only", "A"),
        ("What should a responsible reader do with a news report?", "Check its credibility", "Believe every claim immediately", "Share it without reading", "Ignore its source", "A"),
        ("What is censorship?", "Control or restriction of certain information", "Free distribution of every newspaper", "A method of counting votes", "A type of election", "A"),
        ("Which is an example of broadcast media?", "Radio", "Personal notebook", "Printed worksheet", "Handwritten postcard", "A"),
        ("What is a journalist?", "A person who gathers and reports news", "A person who only builds bridges", "A person who counts rainfall", "A person who issues currency", "A"),
        ("What is meant by freedom of the press?", "The ability of media to report within the protection of applicable laws", "The power to ignore every law", "The right to decide court cases", "The authority to cancel elections", "A"),
        ("Which platform can help citizens discuss public issues?", "A public discussion forum", "A locked private cupboard", "A blank notebook", "A calculator screen", "A"),
        ("What is misinformation?", "False or inaccurate information shared as information", "A verified weather reading", "A confirmed public notice", "A genuine textbook definition", "A"),
        ("Why should media report public problems?", "To bring issues to public attention", "To prevent citizens from learning", "To replace local government", "To stop all public discussion", "A"),
        ("Which is an example of print media?", "Magazine", "Radio broadcast", "Podcast", "Live television stream", "A"),
        ("What is a news headline?", "A short title summarising a news story", "The complete list of voters", "A court's final judgment", "A list of school holidays only", "A"),
        ("What does a fact-checker do?", "Checks whether claims are supported by evidence", "Creates rumours for entertainment", "Counts television screens", "Prints currency notes", "A"),
        ("What is social media commonly used for?", "Sharing content and communicating online", "Conducting every court trial", "Issuing passports directly", "Making rainfall occur", "A"),
        ("Why do citizens need reliable news?", "To make informed decisions", "To avoid all civic participation", "To replace the Constitution", "To eliminate public debate", "A"),
        ("What is a media audience?", "People who receive or consume media content", "Only newspaper printers", "Only elected representatives", "Only television repair workers", "A"),
        ("What is a public issue?", "An issue affecting a community or society", "A person's private shopping list", "A fictional game score only", "A personal drawing", "A"),
        ("Which action supports responsible online sharing?", "Verifying information before forwarding it", "Forwarding every message immediately", "Removing all source details", "Changing facts to attract attention", "A"),
        ("What can radio provide to people?", "News, information, and programmes", "Printed photographs only", "Physical court orders only", "Road construction materials", "A"),
        ("What is the basic purpose of a news report?", "To communicate information about events", "To replace democratic institutions", "To decide election results", "To make laws without authority", "A"),
    ],

    "Medium": [
        ("How can media strengthen democracy?", "By informing citizens and enabling public debate", "By preventing citizens from questioning leaders", "By replacing elected governments", "By banning all political discussion", "A"),
        ("Why is media sometimes called a watchdog?", "It can investigate and report misuse of power", "It directly commands the armed forces", "It replaces the judiciary", "It appoints all ministers", "A"),
        ("What is one concern when a few companies control most media outlets?", "A narrow range of viewpoints may dominate", "Every citizen automatically becomes a journalist", "News becomes legally unnecessary", "Elections must be cancelled", "A"),
        ("How can paid advertisements influence news coverage?", "Commercial interests may affect which issues receive attention", "They automatically guarantee unbiased reporting", "They remove the need for journalists", "They make all reports government orders", "A"),
        ("Why should news organisations distinguish facts from opinions?", "So audiences can understand what is verified and what is interpretation", "So that evidence can be avoided", "So every opinion becomes law", "So sources never need checking", "A"),
        ("What is media bias?", "Presenting information in a way that unfairly favours a viewpoint", "Reporting every event with equal evidence", "Correcting a spelling error", "Publishing a weather table", "A"),
        ("Why is diversity of media ownership valuable?", "It can allow different viewpoints to reach the public", "It ensures only one opinion is heard", "It prevents citizens from reading news", "It removes public accountability", "A"),
        ("How can citizens evaluate a suspicious online claim?", "Check reliable sources and supporting evidence", "Trust it because it is popular", "Share it before checking", "Judge it only by its headline", "A"),
        ("What is the relationship between media and accountability?", "Reporting can help the public question those in power", "Media automatically passes every law", "Media appoints every elected official", "Accountability exists only during advertisements", "A"),
        ("Why might important rural issues receive less media coverage?", "Commercial priorities and limited reporting resources may affect coverage", "Rural citizens cannot have public concerns", "Rural issues are never relevant", "All rural events are legally secret", "A"),
        ("What is investigative journalism?", "In-depth reporting that examines issues and uncovers evidence", "Reading advertisements without analysis", "Publishing rumours without checking", "Reporting only sports scores", "A"),
        ("Why is source transparency important in reporting?", "It helps audiences assess the reliability of information", "It guarantees that every source is correct", "It makes evidence unnecessary", "It prevents correction of mistakes", "A"),
        ("How can misinformation affect democratic participation?", "It can mislead citizens making public decisions", "It always improves political understanding", "It guarantees fair elections", "It removes all disagreement", "A"),
        ("What is the purpose of a correction or retraction?", "To address inaccurate or misleading published information", "To hide every factual mistake", "To replace elections", "To prevent further investigation", "A"),
        ("How does media coverage help during elections?", "It provides information about candidates and public issues", "It legally chooses every winner", "It replaces voters' decisions", "It eliminates the need for election rules", "A"),
        ("Why can sensational headlines be harmful?", "They may exaggerate events and mislead readers", "They always provide complete context", "They guarantee accurate reporting", "They replace the need for evidence", "A"),
        ("What is the digital divide?", "Unequal access to digital technologies and connectivity", "Equal access to all online services", "A difference between two newspaper headlines", "A type of parliamentary debate", "A"),
        ("How can media literacy help citizens?", "It helps them analyse and evaluate media messages", "It teaches them to accept every claim", "It prevents them from asking questions", "It makes sources irrelevant", "A"),
        ("Why should journalists protect confidential sources in appropriate circumstances?", "To help sources provide information about matters of public interest", "To guarantee every allegation is true", "To avoid checking evidence", "To make all reporting anonymous", "A"),
        ("What is one risk of concentrated media ownership?", "Editorial priorities may reflect a limited set of interests", "Every report becomes automatically neutral", "No advertisements can appear", "Citizens lose all access to public information by law", "A"),
        ("How can community radio contribute to democracy?", "By sharing locally relevant information and voices", "By replacing every elected institution", "By deciding criminal cases", "By issuing national legislation", "A"),
        ("Why is independent reporting important?", "It can scrutinise powerful institutions without improper influence", "It must support every government decision", "It removes the need for evidence", "It prevents public discussion", "A"),
        ("What is the difference between reporting and commentary?", "Reporting presents information about events, while commentary interprets or evaluates them", "Reporting is always fictional", "Commentary never expresses a viewpoint", "Both are legally identical in every situation", "A"),
        ("How can algorithms affect online news exposure?", "They may influence which stories users see", "They ensure everyone sees exactly the same news", "They verify every story automatically", "They remove all commercial interests", "A"),
        ("Why should media include different social perspectives?", "It can provide a fuller picture of society's concerns", "It ensures all disagreements disappear", "It prevents public participation", "It makes verification unnecessary", "A"),
        ("What is a conflict of interest in journalism?", "A personal or financial interest that could affect impartial reporting", "A routine spelling correction", "A confirmed rainfall measurement", "A neutral description of a public event", "A"),
        ("Why is timely correction of false information important?", "It can reduce the continued spread of inaccurate claims", "It guarantees nobody has seen the original claim", "It eliminates the need for fact-checking", "It makes the original report permanently accurate", "A"),
        ("What is a public service role of media?", "Providing useful information about health, safety, and civic matters", "Selling products only", "Replacing all public services", "Making court decisions", "A"),
        ("Why might advertisers influence editorial decisions?", "Media organisations may depend on advertising revenue", "Advertisers always control the Constitution", "Advertising removes all financial pressure", "Journalists never interact with businesses", "A"),
        ("How does public debate benefit from a free and responsible media?", "Citizens can examine competing ideas and evidence", "Only one viewpoint can be discussed", "Public questions become illegal", "Evidence becomes unnecessary", "A"),
    ],

    "Hard": [
        ("A news channel repeatedly ignores evidence of wrongdoing by its major advertiser. Which concern is most relevant?", "Commercial interests may compromise editorial independence", "Advertising automatically guarantees accuracy", "The judiciary has been replaced by television", "All public information must be secret", "A"),
        ("A viral post makes a serious allegation but provides no evidence. What is the most responsible response?", "Seek independent corroboration before treating it as fact", "Share it because it is widely circulated", "Assume the allegation is proven", "Remove all references to its source", "A"),
        ("A media organisation reports a public controversy but includes only one side's claims. What is the strongest criticism?", "The report may lack relevant context and fair representation", "The report necessarily proves that side is correct", "The report has become a law", "The report eliminates the need for evidence", "A"),
        ("Why does media pluralism matter beyond simply having many channels?", "Different owners and editorial perspectives can broaden public debate", "Many channels guarantee that every report is accurate", "It eliminates all commercial incentives", "It prevents citizens from disagreeing", "A"),
        ("A journalist publishes a serious accusation based on an anonymous message alone. What is the main professional concern?", "The claim lacks sufficient verification", "Anonymous sources can never provide useful information", "All accusations are automatically true", "Evidence is unnecessary for public-interest reporting", "A"),
        ("How can an algorithmic recommendation system create an information bubble?", "Repeatedly recommending similar viewpoints may limit exposure to alternatives", "It ensures users encounter every viewpoint equally", "It verifies all political claims", "It removes all personal preferences", "A"),
        ("Why is transparency about sponsored content important?", "Audiences should be able to distinguish advertising from independent editorial content", "Sponsored content is always false", "Advertising can never be useful", "All editorial content is paid promotion", "A"),
        ("A newspaper corrects a factual error but leaves the correction difficult to find. What concern remains?", "Readers may continue to be misled by the original error", "The original error becomes legally correct", "The correction removes the need for evidence", "All readers must have seen the correction", "A"),
        ("How can censorship weaken democratic accountability?", "It may prevent citizens from learning about important public matters", "It guarantees public scrutiny", "It ensures every viewpoint is represented", "It makes independent journalism unnecessary", "A"),
        ("A broadcaster gives extensive coverage to urban events but repeatedly overlooks rural concerns. What is a likely democratic consequence?", "Some communities may be underrepresented in public discussion", "Rural concerns automatically become laws", "All citizens receive identical coverage", "Public participation becomes unnecessary", "A"),
        ("What distinguishes evidence-based investigative reporting from rumour?", "It uses corroboration, documentation, and careful verification", "It depends entirely on popularity", "It avoids checking sources", "It treats every allegation as a proven fact", "A"),
        ("A politician criticises a report and demands that it be withdrawn without addressing its evidence. What should responsible journalism prioritise?", "Reviewing the evidence and responding transparently to substantiated errors", "Withdrawing every report about public officials", "Ignoring all new evidence", "Publishing only the politician's statements", "A"),
        ("Why can ownership transparency support media accountability?", "It helps audiences identify interests that may influence coverage", "It proves every story is biased", "It makes verification unnecessary", "It eliminates the need for editorial standards", "A"),
        ("Which practice best reduces the risk of spreading manipulated images?", "Checking the image's origin, context, and corroborating sources", "Trusting the image because it looks realistic", "Sharing it before searching for context", "Using the number of likes as proof", "A"),
        ("Why is equal access to reliable information important during elections?", "It supports citizens' ability to make informed choices", "It guarantees that all voters choose the same candidate", "It allows media to cast votes for citizens", "It eliminates the need for election procedures", "A"),
        ("A report quotes a statistic without explaining its source or method. What is the key limitation?", "The audience cannot adequately assess how reliable the statistic is", "The statistic is necessarily correct", "The statistic becomes an official law", "The report is automatically investigative journalism", "A"),
        ("What is the most balanced view of media freedom in a democracy?", "Media freedom supports scrutiny while responsible reporting requires verification and accountability", "Media freedom means false claims must never be corrected", "Media freedom removes every legal responsibility", "Media freedom requires all outlets to agree", "A"),
        ("How can a correction policy improve public trust?", "It demonstrates willingness to acknowledge and address mistakes", "It ensures that mistakes never occur", "It prevents readers from questioning reports", "It makes source checks unnecessary", "A"),
        ("Why is the distinction between fact and opinion important in political reporting?", "It helps audiences evaluate evidence separately from interpretation", "It means opinions can never be discussed", "It makes all opinions factual", "It removes the need for context", "A"),
        ("A media company publishes only stories likely to attract clicks, overlooking important public-interest issues. What tension does this illustrate?", "Commercial incentives can conflict with public-service responsibilities", "Public-interest reporting always attracts no audience", "Clicks guarantee complete coverage", "Commercial media cannot publish news", "A"),
        ("How can diverse ownership reduce the risk of a single narrative dominating public discussion?", "It can create more independent editorial perspectives", "It guarantees every owner is impartial", "It prevents disagreement between citizens", "It makes every report equally reliable", "A"),
        ("Why should a journalist seek a response from a person facing a serious allegation?", "It supports fairness and gives relevant parties an opportunity to respond", "It automatically proves the allegation false", "It removes the need to verify evidence", "It guarantees the response is truthful", "A"),
        ("What is a major limitation of using social media popularity to judge truth?", "Popularity measures engagement, not necessarily accuracy", "Popular posts are always fabricated", "Unpopular posts are always accurate", "Engagement replaces independent verification", "A"),
        ("How can community media improve representation?", "It can provide space for locally important concerns and perspectives", "It guarantees that all community members agree", "It replaces national democratic institutions", "It prevents discussion of local issues", "A"),
        ("A government releases information only to outlets that praise it. What democratic concern does this raise?", "Unequal access may restrict independent scrutiny and pluralism", "All outlets now have equal access", "Independent reporting is guaranteed", "Public debate no longer matters", "A"),
        ("Why is media literacy especially important when content is emotionally provocative?", "Strong emotions can encourage people to share claims before checking them", "Emotional content is always accurate", "Emotions eliminate confirmation bias", "Provocative headlines guarantee reliable sources", "A"),
        ("What is the strongest reason to distinguish a correction from censorship?", "A correction addresses accuracy, while censorship restricts expression or access to information", "Both always mean that a report is accurate", "A correction always bans an entire subject", "Censorship always improves pluralism", "A"),
        ("How can independent public-interest journalism contribute to the rule of law?", "It can expose concerns that prompt public scrutiny and lawful investigation", "It can independently convict accused persons", "It replaces courts and legal procedures", "It determines guilt from headlines", "A"),
        ("A report contains accurate facts but omits essential context that changes their meaning. What problem may result?", "The presentation can mislead despite the individual facts being correct", "Accurate facts can never mislead", "Context is irrelevant to journalism", "The report automatically becomes a court ruling", "A"),
        ("Which combination best supports a healthy media environment in a democracy?", "Pluralism, editorial independence, verification, and accountability", "Single-source control, secrecy, and unchecked rumours", "Censorship, unsupported claims, and no corrections", "Advertising influence without disclosure or scrutiny", "A"),
    ],
}


def main():
    db = SessionLocal()
    added = 0

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "Media and Democracy",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if not lesson:
            print("ERROR: Media and Democracy lesson was not found.")
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

            existing_texts = {
                q.question.strip().lower() for q in existing
            }

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