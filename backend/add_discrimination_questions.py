import logging
import os
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
        ("What does diversity mean?", "People having different backgrounds and characteristics", "Everyone being exactly alike", "Only speaking one language", "Living in one place", "A"),
        ("What is discrimination?", "Treating people unfairly because of their identity", "Treating everyone fairly", "Helping someone learn", "Celebrating different cultures", "A"),
        ("Which is an example of diversity?", "People following different traditions", "Everyone having the same opinion", "Everyone wearing identical clothes", "Everyone speaking one language", "A"),
        ("Which value helps reduce discrimination?", "Equality", "Prejudice", "Exclusion", "Stereotyping", "A"),
        ("What is a stereotype?", "A fixed generalisation about a group", "A fair assessment of each person", "A written law", "A festival", "A"),
        ("Which action shows respect for diversity?", "Respecting different languages", "Mocking another person's accent", "Excluding newcomers", "Spreading rumours", "A"),
        ("What does equality mean?", "People having equal rights and opportunities", "Giving rights only to wealthy people", "Treating some groups as inferior", "Preventing people from studying", "A"),
        ("Which can be a basis for discrimination?", "Caste", "Choice of pencil", "Handwriting style", "Favourite notebook", "A"),
        ("What is prejudice?", "An unfair opinion formed without enough knowledge", "A carefully researched fact", "A public service", "A school subject", "A"),
        ("Which institution helps protect people's rights in India?", "The judiciary", "A sports team", "A shopping centre", "A private club only", "A"),
        ("What is inclusion?", "Allowing everyone to participate", "Keeping certain people out", "Refusing to listen", "Giving opportunities to one group only", "A"),
        ("Which is an example of religious diversity?", "People following different religions", "Everyone having the same hobby", "Everyone using the same book", "Everyone living in one house", "A"),
        ("How should we treat people from different communities?", "With dignity and respect", "With automatic suspicion", "As less important", "By excluding them", "A"),
        ("What is a possible effect of discrimination?", "Unfair loss of opportunities", "Equal treatment for all", "Greater inclusion automatically", "Removal of every barrier", "A"),
        ("Which action challenges a stereotype?", "Learning about individuals instead of assuming", "Repeating rumours", "Judging everyone in a group alike", "Ignoring evidence", "A"),
        ("What does dignity mean?", "The worth and respect every person deserves", "A person's wealth", "A person's popularity", "A person's social rank", "A"),
        ("Which is an example of unfair exclusion?", "Refusing entry because of caste", "Inviting everyone to participate", "Sharing learning materials", "Respecting different customs", "A"),
        ("Why is diversity valuable?", "It brings different experiences and perspectives", "It makes fairness unnecessary", "It means everyone must agree", "It prevents learning", "A"),
        ("Which action promotes equality in school?", "Giving every student a fair chance to learn", "Allowing only certain students to answer", "Mocking weaker students", "Excluding new students", "A"),
        ("What should you do if you witness discrimination?", "Seek help and support the affected person safely", "Join the unfair treatment", "Spread gossip", "Blame the affected person", "A"),
        ("What is a community?", "People connected by place, identity, or shared interests", "Only people from one family", "Only government officials", "Only people of one age", "A"),
        ("Which is an example of cultural diversity?", "Different foods, music, and customs", "One compulsory food for everyone", "No cultural traditions", "Everyone sharing one opinion", "A"),
        ("What is equal opportunity?", "A fair chance to participate and succeed", "Success reserved for one group", "Removing access to education", "Choosing people only by caste", "A"),
        ("Which behaviour can strengthen prejudice?", "Believing rumours without checking them", "Listening to different viewpoints", "Learning from reliable sources", "Meeting people from different backgrounds", "A"),
        ("What does empathy involve?", "Trying to understand another person's feelings", "Ignoring another person's difficulties", "Making fun of someone", "Assuming everyone feels the same", "A"),
        ("Which statement is respectful?", "People deserve respect regardless of their background", "Some communities deserve fewer rights", "Identity determines ability", "Different languages are inferior", "A"),
        ("Which is an example of gender discrimination?", "Denying education because of gender", "Offering equal learning opportunities", "Sharing household responsibilities", "Encouraging every child to study", "A"),
        ("What helps people challenge prejudice?", "Education and meaningful interaction", "Rumours and assumptions", "Social exclusion", "Unfair generalisations", "A"),
        ("What is a human right?", "A basic right belonging to a person", "A privilege only for the rich", "A reward for popularity", "A right only for adults", "A"),
        ("What should guide decisions about people?", "Fair evidence and individual circumstances", "Stereotypes about their community", "Unverified rumours", "Social status alone", "A"),
    ],

    "Medium": [
        ("Why can stereotypes be harmful?", "They ignore individual differences and can justify unfair treatment", "They always describe every individual accurately", "They guarantee equal opportunity", "They eliminate prejudice", "A"),
        ("A school refuses admission because of caste. What is this?", "Discrimination", "Cultural exchange", "Inclusion", "Cooperation", "A"),
        ("How are prejudice and discrimination different?", "Prejudice is an unfair attitude; discrimination is unfair treatment", "They always mean the same action", "Prejudice is a law", "Discrimination is always harmless", "A"),
        ("Why is representation of different communities important?", "It can help different experiences be heard", "It requires everyone to think alike", "It removes the need for rights", "It guarantees agreement", "A"),
        ("A teacher assumes a student cannot do mathematics because of gender. What is this?", "A gender stereotype", "Equal opportunity", "Cultural inclusion", "A scientific conclusion", "A"),
        ("Why can unequal access to education continue discrimination?", "It limits future choices and opportunities", "It guarantees social mobility", "It removes economic barriers", "It makes rights unnecessary", "A"),
        ("What is an appropriate response to an unfamiliar custom?", "Ask respectfully and learn about its meaning", "Call it inferior immediately", "Spread jokes about it", "Demand everyone abandon it", "A"),
        ("How can laws help address discrimination?", "They can prohibit unfair practices and protect rights", "They make all prejudice disappear instantly", "They remove the need for enforcement", "They guarantee agreement", "A"),
        ("Why should claims about a community be checked?", "Generalisations may be inaccurate or misleading", "Every rumour is reliable", "Evidence increases prejudice automatically", "Checking facts prevents learning", "A"),
        ("A public facility is inaccessible to a person with a disability. What issue may arise?", "Unequal access and exclusion", "Guaranteed inclusion", "Cultural celebration", "Equal participation automatically", "A"),
        ("Which response best supports a classmate facing prejudice?", "Listen, offer support, and report serious incidents appropriately", "Tell them discrimination is unimportant", "Repeat the insulting comments", "Exclude them from group work", "A"),
        ("How can media influence stereotypes?", "Repeated one-sided portrayals can reinforce assumptions", "Media can never influence attitudes", "Every portrayal is balanced", "Media removes all social differences", "A"),
        ("Why is equal treatment not always the same as equal opportunity?", "Some people may need barriers removed to access the same opportunity", "Fairness means ignoring every barrier", "Equal opportunity requires exclusion", "Fairness means rights do not matter", "A"),
        ("Which situation shows indirect exclusion?", "A rule prevents some students from participating", "Every student can access an activity", "Students share materials freely", "Different opinions are welcomed", "A"),
        ("Why is listening to marginalised groups important?", "Their experiences can reveal barriers others overlook", "Their experiences never matter", "Every claim must be accepted without thought", "It removes public discussion", "A"),
        ("How can education challenge caste-based prejudice?", "It can encourage critical thinking and awareness of equality", "It proves caste hierarchy is necessary", "It makes unfair treatment acceptable", "It prevents questioning", "A"),
        ("What is a possible consequence of discrimination in employment?", "Qualified people may be denied opportunities unfairly", "All applicants receive fair consideration", "Workplace barriers disappear", "Skills become irrelevant to everyone", "A"),
        ("Why should school rules be applied fairly?", "Fair rules help protect students from arbitrary treatment", "Rules should favour popular students", "Rules should depend on family wealth", "Fairness prevents learning", "A"),
        ("Which action best challenges a stereotype?", "Recognising that ability varies between individuals", "Assuming everyone in a group behaves alike", "Repeating an unverified claim", "Avoiding contact with other groups", "A"),
        ("Why can social exclusion be harmful?", "It can reduce belonging and access to shared resources", "It guarantees participation", "It creates equal status", "It eliminates barriers", "A"),
        ("What can inclusive textbooks achieve?", "Show a wider range of people and experiences", "Teach that only one community matters", "Remove historical evidence", "Make diversity irrelevant", "A"),
        ("A club allows membership only to one religious group. What concern does this raise?", "Exclusion based on religious identity", "Equal access for every group", "Universal participation", "Freedom from all bias", "A"),
        ("How can cooperation across communities help?", "It can build understanding through shared activities", "It guarantees all differences vanish", "It requires one culture to dominate", "It prevents learning", "A"),
        ("Why is individual ability more relevant than a stereotype?", "A stereotype cannot reliably establish a person's actual ability", "Group assumptions are always precise", "Individual evidence is never useful", "Identity determines every outcome", "A"),
        ("Which action promotes inclusion during a group project?", "Distribute roles fairly and hear everyone's ideas", "Give all decisions to one group", "Ignore students who differ", "Prevent some students from contributing", "A"),
        ("What is a fair way to address a biased school policy?", "Raise the concern with evidence through appropriate channels", "Spread false claims", "Target students who benefit", "Ignore every affected student", "A"),
        ("How can language-based prejudice affect students?", "It may discourage participation and create exclusion", "It always improves confidence", "It guarantees equal treatment", "It removes communication barriers", "A"),
        ("Why is diversity more than visible differences?", "It includes varied experiences, beliefs, languages, and perspectives", "It refers only to clothing", "Everyone has identical experiences", "It excludes differences in belief", "A"),
        ("What is the purpose of an anti-discrimination policy?", "To set expectations and ways to address unfair treatment", "To encourage stereotypes", "To remove basic rights", "To make complaints impossible", "A"),
        ("How should a claim that one community is less capable be assessed?", "Question the generalisation and seek reliable evidence", "Accept it without examination", "Apply it to every individual", "Use it to deny opportunities", "A"),
    ],

    "Hard": [
        ("A neutral-looking policy prevents many disadvantaged students from participating. What should be examined first?", "Its actual effects and the barriers it creates", "Only whether its wording sounds neutral", "Whether affected students are popular", "Whether the policy avoids review", "A"),
        ("Why can identical treatment still produce unequal outcomes?", "People may face different starting conditions and barriers", "Identical rules remove every barrier", "Different circumstances never matter", "Equal rights require unequal treatment", "A"),
        ("A report portrays one community using only negative examples. What is the main concern?", "Selective representation may reinforce a stereotype", "It represents every member accurately", "It proves every negative claim", "It guarantees balanced reporting", "A"),
        ("Which evidence most directly challenges a claim about every member of a group?", "Reliable evidence showing individual variation", "A single unverified rumour", "A repeated slogan", "An assumption based on identity", "A"),
        ("A school entrance process disadvantages students without internet access. What response best promotes fairness?", "Provide accessible alternatives and assess the barrier", "Keep the barrier because the rule is identical", "Exclude affected applicants", "Stop reviewing the process", "A"),
        ("Why distinguish intent from impact in discrimination cases?", "A rule can cause unequal harm without an explicit intention to discriminate", "Good intentions guarantee fair outcomes", "Impact never matters", "Intent and impact are always identical", "A"),
        ("A student repeats a stereotype without knowing anyone from that group. What is relevant?", "The belief may come from assumptions rather than personal evidence", "The belief must be accurate", "The statement proves individual ability", "The stereotype is a legal finding", "A"),
        ("What makes a response to discrimination more effective than a statement alone?", "Concrete procedures, accountability, and follow-through", "Avoiding reports and records", "Keeping rules unclear", "Leaving barriers unexamined", "A"),
        ("Why can intersectional disadvantage be difficult to identify?", "Different aspects of identity can interact to shape experience", "People have only one social identity", "Social identities never affect access", "Everyone experiences identical barriers", "A"),
        ("A qualified applicant is rejected because of assumptions about their community. What issue is central?", "An employment decision based on a stereotype", "A fair evaluation of individual evidence", "A neutral skills assessment", "An equal opportunity policy", "A"),
        ("Which approach best evaluates institutional inclusion?", "Examine participation, access, experiences, and outcomes across groups", "Check only the mission statement", "Count only public celebrations", "Assume no complaints means no barriers", "A"),
        ("Why should anti-discrimination rules include a reporting process?", "People need a practical way to raise concerns and seek remedies", "Reporting should always be impossible", "Rules work only when hidden", "Affected people should manage every case alone", "A"),
        ("A minority-group member is asked to represent everyone in that group. What assumption is problematic?", "One individual can speak for a diverse group without variation", "Individuals may have different opinions", "Communities contain internal diversity", "People can describe their own experiences", "A"),
        ("How can inaccessible public transport contribute to exclusion?", "It can limit access to education, work, and public services", "It guarantees full participation", "It affects no opportunities", "It removes every barrier", "A"),
        ("Why consider historical discrimination when evaluating present inequality?", "Past exclusion can shape current access to resources and opportunities", "History never affects present conditions", "Past events explain every individual outcome automatically", "Historical evidence is never relevant", "A"),
        ("Which response best addresses a stereotype in class?", "Ask for evidence and consider individual variation", "Allow the stereotype to stand unquestioned", "Insult the speaker's identity", "Ban all discussion of fairness", "A"),
        ("An organisation celebrates diversity but ignores biased promotion decisions. What is missing?", "Action on structural barriers and decision-making practices", "More stereotypes", "Less accountability", "Removal of fair procedures", "A"),
        ("Why can anonymous statistics help review discrimination?", "They can reveal patterns that individual cases may not show", "They prove every cause automatically", "They make context unnecessary", "They replace all qualitative evidence", "A"),
        ("A rule has unequal effects. What is the most careful conclusion before investigation?", "The effects warrant examination; more evidence may explain them", "The rule is definitely harmless", "The effects must be intentional", "No review is necessary", "A"),
        ("What is the difference between celebrating diversity and tokenism?", "Celebration values meaningful participation; tokenism may be superficial representation", "Both always mean exclusion", "Tokenism guarantees equal decision-making power", "Celebration requires identical cultures", "A"),
        ("Why is accountability important when discrimination is reported?", "It helps ensure concerns are investigated and appropriate action is taken", "It prevents evidence from being considered", "It makes fair procedures unnecessary", "Every allegation is automatically proven", "A"),
        ("Which measure best tests whether recruitment is fair?", "Review criteria, accessibility, decisions, and outcome patterns", "Assume fairness from reputation", "Use community identity as a proxy for skill", "Avoid recording decisions", "A"),
        ("Why should a person not be judged solely by group-level statistics?", "Group patterns do not determine every individual's characteristics or ability", "Statistics describe each person exactly", "Individual evidence cannot be collected", "Group membership proves behaviour", "A"),
        ("A student faces insults about language and economic background. What is important to recognise?", "Multiple forms of bias may affect the same person's experience", "Only one aspect of identity can matter", "The insults cannot affect participation", "The student must resolve the issue alone", "A"),
        ("Which principle should guide a discrimination investigation?", "Fairness, relevant evidence, appropriate confidentiality, and due process", "Assume guilt before gathering evidence", "Ignore the affected person's account", "Publish private details unnecessarily", "A"),
        ("Why can diverse decision-making groups improve institutional decisions?", "They may bring different experiences and expose overlooked assumptions", "They guarantee unanimous agreement", "They eliminate the need for evidence", "Every member has identical views", "A"),
        ("What is a risk of using one anecdote to judge an entire community?", "One case cannot establish a universal group characteristic", "Anecdotes prove universal claims", "Individual experiences are never real", "One example removes the need for research", "A"),
        ("Which action addresses the cause rather than the appearance of exclusion?", "Identify and remove barriers in policies and practices", "Hold one event while retaining every barrier", "Avoid gathering feedback", "Leave inaccessible procedures unchanged", "A"),
        ("Data shows a participation gap between groups. What should an institution do?", "Investigate causes, consult affected people, and evaluate possible remedies", "Assume one group lacks ability", "Ignore the difference automatically", "Treat the gap as proof of one specific cause", "A"),
        ("Why avoid discriminatory generalisations?", "They can distort judgment and deny people fair treatment as individuals", "They always simplify decisions accurately", "They guarantee equal opportunities", "They remove the need for evidence", "A"),
    ],
}


def main():
    db = SessionLocal()

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "Diversity and Discrimination",
                Lesson.topic == "Social Science",
            )
            .first()
        )

        if lesson is None:
            print("Lesson not found. Run the Social Science seed script first.")
            return

        total_added = 0

        for difficulty, questions in QUESTION_BANK.items():
            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.title == f"Diversity and Discrimination - {difficulty}",
                )
                .first()
            )

            if quiz is None:
                quiz = Quiz(
                    lesson_id=lesson.id,
                    title=f"Diversity and Discrimination - {difficulty}",
                    difficulty=difficulty,
                )
                db.add(quiz)
                db.flush()

            existing = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
            )

            if existing >= 30:
                print(f"{difficulty}: already has {existing} questions; skipped.")
                continue

            added = 0

            for item in questions:
                if existing + added >= 30:
                    break

                question_text, a, b, c, d, answer = item

                duplicate = (
                    db.query(Question)
                    .filter(
                        Question.quiz_id == quiz.id,
                        Question.question == question_text,
                    )
                    .first()
                )

                if duplicate:
                    continue

                db.add(
                    Question(
                        quiz_id=quiz.id,
                        question=question_text,
                        option_a=a,
                        option_b=b,
                        option_c=c,
                        option_d=d,
                        correct_answer=answer,
                    )
                )
                added += 1

            db.commit()

            final_count = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
            )

            total_added += added
            print(
                f"{difficulty}: added {added}; "
                f"final count {final_count}/30"
            )

        print(f"\nTotal questions added: {total_added}")

    except Exception as error:
        db.rollback()
        print(f"Error: {error}")

    finally:
        db.close()


if __name__ == "__main__":
    main()