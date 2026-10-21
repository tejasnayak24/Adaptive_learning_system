import logging
from pathlib import Path
import os

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

LESSON_TITLE = "Understanding Diversity"
SUBJECT = "Social Science"
TARGET = 30

# Each tuple: question, option A, option B, option C, option D, correct option
EXTRA_QUESTIONS = {
    "Easy": [
        ("Which term describes the variety of cultures in a society?", "Uniformity", "Diversity", "Isolation", "Separation", "B"),
        ("Which can be part of a person's cultural identity?", "Only height", "Only shoe size", "Language and traditions", "Only blood group", "C"),
        ("Which is an example of regional diversity in India?", "Every state has the same cuisine", "All regions have identical climates", "Every region speaks only Hindi", "Different regions have different food traditions", "D"),
        ("What is a community?", "A group of people connected by place or shared interests", "A type of mountain", "A kind of weather", "A national currency", "A"),
        ("Which action shows respect for diversity?", "Mocking someone's language", "Listening respectfully to different viewpoints", "Excluding people with different customs", "Assuming everyone is identical", "B"),
        ("What can vary between regions?", "The number of hours in a day", "The direction of Earth's rotation", "Clothing and food traditions", "The value of gravity", "C"),
        ("Which of these is a cultural practice?", "Measuring temperature", "Calculating distance", "Reading a clock", "Celebrating a traditional festival", "D"),
        ("Why do people in India speak different languages?", "India has many linguistic communities and traditions", "Every family uses the same language", "Languages are determined only by climate", "Regional languages do not exist", "A"),
        ("Which is an example of diversity in clothing?", "Everyone wearing the same uniform everywhere", "Different communities wearing different traditional clothes", "Clothing being unrelated to culture", "Everyone wearing identical clothes at home", "B"),
        ("What is a fair way to treat people from different backgrounds?", "Give respect only to familiar groups", "Judge people by stereotypes", "Treat people with equal respect", "Prevent people from sharing traditions", "C"),
        ("Which factor can shape local customs?", "Only the colour of buildings", "Only the length of a school day", "Only the number of roads", "History and community traditions", "D"),
        ("What does a stereotype do?", "Assumes that members of a group share certain traits", "Explains every individual accurately", "Removes all social differences", "Guarantees fair treatment", "A"),
        ("Which is an example of linguistic diversity?", "Everyone speaking in the same accent", "People using different languages", "All books being the same size", "Everyone studying the same subject", "B"),
        ("How can children learn about different cultures?", "By avoiding other communities", "By believing every stereotype", "By reading, listening and interacting respectfully", "By refusing to ask questions", "C"),
        ("What may influence traditional occupations?", "Only a person's favourite colour", "Only the day of birth", "Only the number of letters in a name", "Local resources and historical practices", "D"),
        ("Which statement about diversity is reasonable?", "Differences can exist within the same community", "Every community is completely uniform", "Culture never changes", "All regions have identical traditions", "A"),
        ("What is one way people share cultural traditions?", "By prohibiting all festivals", "Through stories, music and celebrations", "By ending communication", "By avoiding family gatherings", "B"),
        ("What does inclusion mean?", "Allowing participation only by one group", "Ignoring people with different needs", "Helping people participate and belong", "Making everyone abandon their identity", "C"),
        ("Which can be an example of religious diversity?", "Everyone owning the same book", "Everyone using the same bus", "Everyone attending the same school", "People following different faiths or beliefs", "D"),
        ("Why is it useful to learn about diversity?", "It can improve understanding and respect", "It proves stereotypes are always correct", "It eliminates every cultural difference", "It makes communication unnecessary", "A"),
    ],
    "Medium": [
        ("How can geography affect people's livelihoods?", "It makes all occupations identical", "It can influence farming, fishing and other work", "It determines everyone's religion", "It prevents communities from adapting", "B"),
        ("Why can food habits differ between two regions?", "Food habits never change", "All regions have identical crops", "Climate, resources and traditions can differ", "People cannot learn recipes from others", "C"),
        ("How can migration influence a community?", "It always removes the local language", "It prevents cultural exchange", "It makes all customs identical", "It can introduce new languages, foods and customs", "D"),
        ("Why is it important to distinguish cultural difference from inequality?", "Differences do not automatically justify unequal treatment", "Every cultural difference is discrimination", "Inequality is always necessary", "All communities must have identical customs", "A"),
        ("How can schools encourage intercultural understanding?", "By teaching students to mock differences", "By presenting varied perspectives and encouraging respectful discussion", "By banning discussion of traditions", "By treating stereotypes as facts", "B"),
        ("Why might traditional houses differ across regions?", "Architecture never responds to surroundings", "All regions have the same weather", "Materials, climate and local practices can vary", "Housing styles depend only on language", "C"),
        ("What can shared public celebrations help create?", "A requirement to abandon local customs", "A reason to exclude minorities", "A rule that everyone must share one religion", "Opportunities for interaction across communities", "D"),
        ("How can language barriers affect participation?", "They may make communication or access to services harder", "They always prevent learning", "They prove one language is superior", "They make translation useless", "A"),
        ("What is a responsible way to learn about a community?", "Assume one person speaks for everyone", "Listen to different members and consult reliable information", "Use stereotypes instead of evidence", "Ignore historical context", "B"),
        ("Why can a community's traditions change over time?", "Traditions cannot change", "Every generation has identical experiences", "Interaction and changing circumstances can influence practices", "Change always destroys every tradition", "C"),
        ("What is one effect of prejudice?", "It guarantees equal opportunity", "It ensures accurate understanding", "It removes social barriers", "It can lead to unfair treatment of people", "D"),
        ("Why should media represent diverse communities carefully?", "Representation can shape how audiences understand groups", "Media has no effect on perceptions", "Every portrayal is automatically accurate", "Communities never vary internally", "A"),
        ("What can be learned from comparing festivals in different regions?", "All celebrations have exactly the same meaning", "Traditions may share themes while differing in practice", "Regional history is irrelevant", "Only one community celebrates festivals", "B"),
        ("How can public institutions support inclusion?", "By excluding people who speak different languages", "By offering services to only one community", "By making services accessible and treating people fairly", "By requiring identical cultural practices", "C"),
        ("Why should generalisations about a region be checked?", "All generalisations are always true", "Individual differences never matter", "Evidence is unnecessary for social claims", "They may overlook variation within the region", "D"),
        ("How can trade contribute to cultural exchange?", "People may encounter new goods, ideas and practices", "Trade always removes local customs", "Trade prevents communication", "Trade makes all languages identical", "A"),
        ("What is the difference between diversity and discrimination?", "They mean exactly the same thing", "Diversity describes differences; discrimination involves unfair treatment", "Diversity always causes discrimination", "Discrimination is necessary for diversity", "B"),
        ("Why might two people from the same state have different lifestyles?", "People from one state cannot differ", "A state has only one occupation", "Family, region, income and personal choices can vary", "State boundaries determine every habit", "C"),
        ("How can learning local history improve cultural understanding?", "It proves every community has the same past", "It removes the need to listen to people", "It makes all regional differences irrelevant", "It helps explain how traditions developed", "D"),
        ("What should someone do after discovering a belief about a community is inaccurate?", "Correct the belief using reliable information", "Repeat it because it is familiar", "Apply it to every member of the group", "Avoid considering any new evidence", "A"),
    ],
    "Hard": [
        ("A school has students from several linguistic backgrounds. Which policy best promotes inclusion?", "Permit participation only in one home language", "Provide appropriate language support while respecting students' languages", "Separate students permanently by language", "Discourage students from communicating", "B"),
        ("A researcher interviews only one person before describing an entire community. What is the main limitation?", "One interview always represents everyone", "Personal accounts are never useful", "The sample may not represent the community's internal diversity", "Community research never needs evidence", "C"),
        ("A regional custom changes after people from different places settle together. What does this suggest?", "Cultural practices cannot change", "Migration always destroys all traditions", "Cultural exchange is impossible", "Practices can adapt through interaction", "D"),
        ("A textbook describes a community using a single fixed trait. What should a careful reader consider?", "Whether the description overlooks individual and regional differences", "Whether every person must fit the description", "Whether evidence should be ignored", "Whether stereotypes are always accurate", "A"),
        ("Two communities have different customs but equal legal rights. Which conclusion follows?", "One community must abandon its customs", "Cultural differences can coexist with equal rights", "Different customs automatically imply unequal rights", "Equal rights require identical lifestyles", "B"),
        ("A survey finds different food habits within one region. What does this demonstrate?", "Regional identity never exists", "All food habits are random", "There can be diversity within a region", "Every region has only one cuisine", "C"),
        ("A public service is available only in a language some residents cannot understand. What barrier may result?", "Guaranteed equal access", "Greater cultural understanding in every case", "The end of linguistic diversity", "Reduced ability to access the service", "D"),
        ("How should a claim that one culture is inherently superior be assessed?", "Question its assumptions and examine evidence without ranking people by identity", "Accept it if it is widely repeated", "Apply it to every member of each group", "Treat stereotypes as scientific findings", "A"),
        ("A festival is celebrated differently by families in the same town. Which explanation is most reasonable?", "Only one family can have a tradition", "Families may interpret and practise traditions differently", "Local traditions never vary", "All celebrations must be identical", "B"),
        ("How can inclusive education challenge prejudice?", "By preventing students from meeting different groups", "By presenting stereotypes without discussion", "By encouraging evidence-based learning and respectful interaction", "By treating differences as defects", "C"),
        ("A journalist interviews only prominent members of a community. What should the journalist consider?", "Prominent people always represent everyone", "Other perspectives are irrelevant", "One viewpoint eliminates bias", "Including varied voices can provide a fuller picture", "D"),
        ("A community adopts new music while retaining older ceremonies. What does this illustrate?", "Cultural change and continuity can coexist", "Cultures must either remain unchanged or disappear", "New influences always erase traditions", "Traditions cannot be shared", "A"),
        ("Why is equal treatment not always the same as providing identical support?", "Every person has exactly the same needs", "Different barriers may require different support to enable fair participation", "Support must always be withheld", "Fairness means ignoring accessibility", "B"),
        ("A claim about a community is based on a single unusual incident. What is the strongest response?", "Assume the incident is typical", "Ignore all other evidence", "Seek broader evidence before drawing a general conclusion", "Apply the incident to every group member", "C"),
        ("How can public celebrations balance shared identity and diversity?", "By prohibiting regional traditions", "By requiring everyone to practise one religion", "By excluding minority communities", "By creating shared participation while respecting different customs", "D"),
        ("A school notices that some students are mocked for their accents. What response addresses the problem?", "Challenge the mocking and establish respectful participation", "Tell students that accents determine ability", "Prevent those students from speaking", "Treat the mocking as harmless in every case", "A"),
        ("Why is language preservation relevant to cultural diversity?", "Languages contain no cultural knowledge", "Languages can carry stories, knowledge and traditions", "Every language has identical vocabulary", "Preserving a language requires rejecting all others", "B"),
        ("A policy benefits one cultural group but unfairly excludes another. What concern does this raise?", "Cultural differences have disappeared", "The policy automatically guarantees equality", "The policy may create discriminatory barriers", "The excluded group has no rights", "C"),
        ("Why should researchers consider historical context when studying cultural practices?", "History never influences communities", "Practices have only one universal cause", "Historical evidence is always irrelevant", "Past events can help explain how practices developed", "D"),
        ("Several communities cooperate on a local project while retaining distinct traditions. What does this show?", "Cooperation does not require cultural uniformity", "Shared work requires identical beliefs", "Diversity prevents all cooperation", "Traditions must be abandoned for teamwork", "A"),
    ],
}


def main():
    db = SessionLocal()

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == LESSON_TITLE,
                Lesson.topic == SUBJECT,
            )
            .first()
        )

        if lesson is None:
            print("Understanding Diversity lesson not found.")
            return

        total_added = 0

        for difficulty, bank in EXTRA_QUESTIONS.items():
            title = f"{LESSON_TITLE} - {difficulty}"

            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.title == title,
                )
                .first()
            )

            if quiz is None:
                print(f"{difficulty}: quiz not found; skipping.")
                continue

            existing_count = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
            )

            added = 0

            for item in bank:
                if existing_count + added >= TARGET:
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
            total_added += added

            final_count = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
            )

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