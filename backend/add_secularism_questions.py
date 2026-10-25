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
        ("What does secularism mean in India?", "The State respects religious freedom and does not establish an official religion", "Only one religion is permitted", "Religious beliefs are compulsory", "Citizens cannot practise religion", "A"),
        ("Does India have an official state religion?", "No", "Yes, Hinduism", "Yes, Islam", "Yes, Christianity", "A"),
        ("Which document establishes India's constitutional principles?", "The Constitution of India", "A private contract", "A school timetable", "A political party poster", "A"),
        ("What does freedom of religion allow?", "People to follow, practise or not follow a religion within constitutional limits", "People to force everyone to follow one religion", "People to ignore every law", "Only government officials to practise religion", "A"),
        ("Why is secularism important in a diverse country?", "It helps people of different religions live with equal respect", "It requires everyone to follow identical beliefs", "It prohibits all cultural celebrations", "It gives one religious group unlimited power", "A"),
        ("What is religious discrimination?", "Unfair treatment because of a person's religion", "Respecting everyone's legal rights", "Allowing people to practise different religions", "Treating people fairly", "A"),
        ("Can people in India choose their religious beliefs?", "Yes, subject to constitutional provisions and applicable law", "No, everyone must follow the same religion", "Only elected representatives can choose", "Only adults working for the government can choose", "A"),
        ("What does religious tolerance encourage?", "Respect for the beliefs and practices of others", "Forcing others to change their beliefs", "Discriminating against minorities", "Preventing peaceful discussion", "A"),
        ("What is the main purpose of secularism?", "To protect religious freedom and prevent religious domination", "To make religious practice compulsory", "To establish a state religion", "To prevent people from having personal beliefs", "A"),
        ("Can a person be treated unfairly solely because of their religion by the State?", "Such discrimination is restricted by constitutional protections", "Yes, in every circumstance", "Yes, if a majority requests it", "There are no constitutional protections against it", "A"),
        ("What is religious diversity?", "The presence of different religious beliefs and communities", "Everyone following one belief", "The absence of all cultural traditions", "A system with no personal beliefs", "A"),
        ("What does freedom of conscience refer to?", "Freedom to hold beliefs and convictions", "A requirement to follow a single religion", "A ban on personal beliefs", "The power to make all national laws", "A"),
        ("What is one feature of a secular democracy?", "People of different religions have constitutional protections", "Only one religious group can vote", "Religious identity determines every public office", "Courts cannot protect religious freedom", "A"),
        ("What is a minority religious community?", "A religious community that forms a smaller part of a population in a given context", "A group that has no legal rights", "A group that must follow another religion", "A political office", "A"),
        ("What does equality of religions encourage?", "Fair treatment and respect within the constitutional framework", "Automatic preference for one religion in all matters", "Compulsory religious conversion", "A ban on minority communities", "A"),
        ("Should people respect the religious freedom of others?", "Yes, while respecting others' rights and the law", "No, only one belief deserves respect", "Only during elections", "Only if everyone follows the same religion", "A"),
        ("Can people celebrate religious festivals in India?", "Yes, subject to applicable laws and reasonable restrictions", "No religious festivals are permitted", "Only government employees can celebrate", "Only one community can celebrate festivals", "A"),
        ("What is the role of the Constitution in religious freedom?", "It provides protections and defines relevant rights and limits", "It requires everyone to share one belief", "It removes all legal rights", "It gives private organisations unlimited authority", "A"),
        ("What does communal harmony mean?", "Peaceful and respectful relations among communities", "Conflict between religious groups", "Forcing communities to abandon their culture", "Preventing people from communicating", "A"),
        ("What is a religious stereotype?", "An oversimplified generalisation about people based on religion", "A constitutional article", "A court judgment", "A form of fair treatment", "A"),
        ("Does secularism require people to abandon their religion?", "No", "Yes, in every circumstance", "Only during elections", "Only in their homes", "A"),
        ("Why should public institutions treat people fairly regardless of religion?", "To uphold equality and constitutional values", "To give one community permanent control", "To prevent equal access to services", "To remove legal protections", "A"),
        ("What does religious freedom include?", "The freedom to profess, practise and propagate religion subject to constitutional limits", "The right to force others to convert", "The right to break every law", "The right to deny others all freedoms", "A"),
        ("Can religious freedom be subject to public order and other constitutional limits?", "Yes", "No, it has no limits in any situation", "Only private companies decide its limits", "Only school principals determine constitutional limits", "A"),
        ("What is peaceful coexistence?", "Different people living together peacefully despite their differences", "Everyone being forced to share one belief", "Preventing cultural exchange", "Discriminating against minorities", "A"),
        ("What does mutual respect mean?", "Recognising the dignity and rights of others", "Accepting discrimination", "Forcing others to agree with every opinion", "Ignoring other people's rights", "A"),
        ("Which institution provides the main legal framework for religious freedom in India?", "The Constitution of India", "A private business", "A sports club", "A school examination board", "A"),
        ("Why is equal citizenship important in a secular state?", "Citizens should enjoy constitutional protections without religious domination", "Only members of one religion should have rights", "Citizenship depends entirely on religious belief", "Minorities should have no access to courts", "A"),
        ("What should someone do when they encounter religious discrimination?", "Seek appropriate support or use lawful complaint and legal remedies", "Respond with violence", "Discriminate against another community", "Ignore all available legal protections", "A"),
        ("What is the relationship between secularism and democracy?", "Secularism can help protect freedom and equality in a religiously diverse democracy", "Secularism eliminates elections", "Democracy requires one compulsory religion", "They cannot exist together", "A"),
    ],

    "Medium": [
        ("How does Indian secularism differ from a system that establishes an official state religion?", "The Indian Constitution does not establish an official state religion and protects religious freedom", "India requires every citizen to follow one official religion", "Religious freedom is prohibited in India", "All public institutions must be controlled by religious organisations", "A"),
        ("Why is the separation of religious authority and government power important?", "It can help prevent religious domination and protect freedom of conscience", "It gives religious authorities unlimited state power", "It removes all constitutional rights", "It prevents citizens from participating in democracy", "A"),
        ("Which article guarantees freedom of conscience and the right to profess, practise and propagate religion, subject to constitutional limits?", "Article 25", "Article 14", "Article 32", "Article 110", "A"),
        ("Which articles protect freedom to manage religious affairs, subject to constitutional limits?", "Articles 25 and 26", "Articles 110 and 112", "Articles 300 and 301", "Articles 51 and 52", "A"),
        ("What does Article 27 generally prohibit?", "Compelling a person to pay taxes specifically appropriated for promoting or maintaining a particular religion or religious denomination", "All taxation by the government", "All charitable donations", "Every educational institution", "A"),
        ("What does Article 28 address?", "Religious instruction in certain educational institutions", "The composition of Parliament", "The appointment of judges", "The national budget", "A"),
        ("How does secularism protect religious minorities?", "It supports constitutional equality and freedom of religion", "It removes their access to courts", "It requires them to abandon their beliefs", "It grants them no constitutional protections", "A"),
        ("What is the difference between religious tolerance and religious equality?", "Tolerance involves respecting differences; equality concerns fair treatment and equal legal protection", "They always mean that one religion dominates others", "Tolerance requires conversion", "Equality means all citizens must hold the same belief", "A"),
        ("Why can government intervention in religious practices sometimes arise in India?", "Constitutional provisions allow regulation or reform in specified circumstances, subject to law", "The government has unlimited authority over every belief", "Religious freedom does not exist", "All religious practices are automatically illegal", "A"),
        ("What does secularism seek to prevent?", "Religious domination and discrimination in public life", "The existence of different beliefs", "Equal legal protection", "Peaceful religious practice", "A"),
        ("How does secularism relate to freedom of conscience?", "It supports people's ability to hold beliefs without compulsory religious conformity", "It requires every person to follow the majority religion", "It prevents personal beliefs", "It abolishes every fundamental right", "A"),
        ("Why is religious discrimination harmful to democracy?", "It undermines equality, dignity and equal participation", "It guarantees fair representation", "It strengthens equal citizenship in every case", "It removes social divisions automatically", "A"),
        ("What is meant by religious domination?", "One religious group exercising unfair or excessive control over others", "All communities enjoying equal legal protection", "Peaceful coexistence among different beliefs", "The protection of freedom of conscience", "A"),
        ("How can schools promote secular values?", "By teaching constitutional values, mutual respect and fairness", "By forcing every student to follow one religion", "By encouraging religious discrimination", "By preventing students from learning about diversity", "A"),
        ("What is the significance of Article 14 in discussions about secularism?", "It guarantees equality before the law and equal protection of the laws", "It establishes an official religion", "It abolishes all religious practices", "It gives Parliament unlimited power", "A"),
        ("How can secularism help reduce communal conflict?", "By supporting equal rights, dialogue and fair treatment of communities", "By encouraging stereotypes", "By restricting all peaceful religious practice", "By giving one community unlimited authority", "A"),
        ("What is one important limitation on religious freedom under Article 25?", "It is subject to public order, morality, health and other constitutional provisions", "It overrides every other constitutional provision in all circumstances", "It removes all legal responsibilities", "It guarantees a right to force conversion", "A"),
        ("What is the significance of Article 26?", "It protects specified rights of religious denominations to manage religious affairs, subject to constitutional limits", "It establishes Parliament", "It gives religious groups unlimited political power", "It abolishes religious institutions", "A"),
        ("What does equal citizenship mean in a secular democracy?", "Citizens should have equal constitutional status regardless of religious identity", "Citizens' legal status always depends on their religion", "Only members of a majority community can vote", "Religious minorities cannot seek legal remedies", "A"),
        ("How should a secular government respond to religious violence?", "Through lawful and impartial measures that protect people and uphold rights", "By encouraging revenge against another community", "By refusing to enforce any law", "By automatically blaming every member of one religion", "A"),
        ("Why is it important to distinguish criticism of ideas from discrimination against people?", "Ideas may be discussed while people's dignity and legal rights must be respected", "All criticism is automatically discrimination", "People should be denied rights when their beliefs differ", "No discussion of ideas is ever permitted", "A"),
        ("What is the purpose of constitutional limits on religious activities?", "To balance religious freedom with other rights and legitimate constitutional concerns", "To abolish all freedom of religion", "To give unlimited power to one community", "To make every religious act compulsory", "A"),
        ("How can public institutions demonstrate secular values?", "By providing services fairly and respecting constitutional protections", "By favouring people based solely on religion", "By denying services to religious minorities", "By replacing law with religious preference", "A"),
        ("Why is religious diversity not necessarily a source of conflict?", "Communities can coexist peacefully when rights, equality and mutual respect are protected", "Different beliefs always make democracy impossible", "All communities must become identical", "Religious freedom always leads to violence", "A"),
        ("What is the role of courts in protecting religious freedom?", "They interpret and enforce applicable constitutional protections and legal limits", "They establish one compulsory religion", "They replace all elected institutions", "They prevent people from seeking remedies", "A"),
        ("What is the difference between secularism and hostility toward religion?", "Secularism protects freedom and equality rather than requiring hostility toward religious belief", "Secularism requires everyone to abandon religion", "Both always mean religious practice is illegal", "Secularism requires compulsory conversion", "A"),
        ("How does secularism support social justice?", "It can help challenge religious discrimination and protect equal dignity", "It requires permanent privilege for one religion", "It prevents disadvantaged groups from seeking remedies", "It removes all legal protections", "A"),
        ("Why should public policy be consistent with constitutional rights?", "Government decisions must respect applicable constitutional requirements", "Popular opinion always overrides the Constitution", "Officials may ignore fundamental rights", "Only religious organisations can determine national law", "A"),
        ("What is a practical way to encourage interfaith understanding?", "Dialogue and respectful learning about different communities", "Spreading rumours about other religions", "Preventing peaceful community events", "Forcing people to change beliefs", "A"),
        ("How does Indian secularism accommodate religious diversity?", "Through constitutional protections, equality principles and regulation within legal limits", "By making one religion compulsory", "By banning all religious practices", "By removing all fundamental rights", "A"),
    ],

    "Hard": [
        ("Which article of the Indian Constitution guarantees freedom of conscience and the right to profess, practise and propagate religion?", "Article 25", "Article 14", "Article 32", "Article 51A", "A"),
        ("Which article protects the right of religious denominations to manage their own affairs in matters of religion, subject to constitutional limits?", "Article 26", "Article 19", "Article 110", "Article 280", "A"),
        ("Which article prohibits compelling a person to pay taxes specifically appropriated for promoting or maintaining a particular religion or religious denomination?", "Article 27", "Article 21", "Article 32", "Article 51A", "A"),
        ("Which article addresses religious instruction in certain educational institutions?", "Article 28", "Article 14", "Article 20", "Article 110", "A"),
        ("Which article guarantees equality before the law and equal protection of the laws?", "Article 14", "Article 25", "Article 26", "Article 51A", "A"),
        ("Which article prohibits discrimination by the State on specified grounds, including religion?", "Article 15", "Article 21A", "Article 32", "Article 110", "A"),
        ("Which article prohibits discrimination in access to specified public places on grounds including religion, subject to its terms?", "Article 15(2)", "Article 19(1)", "Article 25(2)", "Article 51A", "A"),
        ("Which article guarantees equality of opportunity in matters of public employment?", "Article 16", "Article 25", "Article 28", "Article 32", "A"),
        ("Which article protects the right of minorities to establish and administer educational institutions of their choice?", "Article 30", "Article 17", "Article 23", "Article 40", "A"),
        ("Which article protects the interests of sections of citizens regarding language, script or culture?", "Article 29", "Article 14", "Article 21A", "Article 51A", "A"),
        ("What are the principal constitutional grounds restricting the exercise of rights under Article 25?", "Public order, morality, health and other provisions of Part III", "Popularity, wealth and political influence", "Approval of every private company", "Unrestricted personal preference of officials", "A"),
        ("Which constitutional provision allows the State to regulate or restrict economic, financial, political or other secular activity associated with religious practice?", "Article 25(2)(a)", "Article 14", "Article 21A", "Article 51A", "A"),
        ("Which constitutional provision permits laws for social welfare and reform, including opening Hindu religious institutions of a public character to all classes and sections of Hindus?", "Article 25(2)(b)", "Article 19(1)", "Article 32", "Article 110", "A"),
        ("Which statement best describes the Indian constitutional approach to secularism?", "The Constitution protects religious freedom and equality while permitting regulation consistent with constitutional provisions", "The Constitution establishes one official state religion", "Religious freedom overrides every other law in all circumstances", "All religious practice is prohibited", "A"),
        ("What is the relationship between Articles 25 and 26?", "Article 25 protects individual freedom of conscience and religion; Article 26 protects specified rights of religious denominations", "Both articles establish an official religion", "Article 25 concerns Parliament and Article 26 concerns elections", "Article 26 removes all religious freedom", "A"),
        ("Why is Article 27 significant in a secular constitutional system?", "It limits compulsory taxation specifically appropriated for promoting or maintaining a particular religion or denomination", "It abolishes every form of public taxation", "It requires all citizens to fund one religion", "It prohibits every public expenditure connected with religion in all circumstances", "A"),
        ("What is the scope of Article 28 regarding religious instruction?", "It regulates religious instruction in specified educational institutions, with distinctions based on their establishment and funding", "It bans all religious education in every institution", "It requires all schools to teach one religion", "It regulates only university examinations", "A"),
        ("How does Article 14 support a secular constitutional order?", "It requires equality before the law and equal protection of the laws", "It establishes a compulsory religion", "It removes all judicial remedies", "It gives one religious group permanent legal superiority", "A"),
        ("Why is the phrase 'subject to the other provisions of this Part' important in Article 25?", "Religious freedom must be read consistently with other applicable fundamental rights and constitutional provisions", "It means religious freedom has no legal protection", "It makes every religious practice automatically unlawful", "It removes the authority of courts", "A"),
        ("What is the significance of judicial review in disputes involving religious freedom?", "Courts can assess whether government action complies with constitutional rights and limits", "Courts must always accept every government action", "Courts establish religious doctrine for every citizen", "Courts cannot consider constitutional questions", "A"),
        ("How can a secular state balance religious freedom with public order?", "By applying lawful, necessary and constitutionally permitted measures while protecting rights", "By prohibiting every peaceful religious gathering", "By allowing violence whenever religion is involved", "By giving one community unlimited authority", "A"),
        ("What is the constitutional importance of minority educational rights?", "They protect specified rights of religious and linguistic minorities to establish and administer educational institutions", "They remove all educational standards", "They give minority institutions immunity from every law", "They prevent minorities from establishing schools", "A"),
        ("Which article is especially relevant when a State action discriminates against a person solely on the ground of religion?", "Article 15", "Article 110", "Article 148", "Article 280", "A"),
        ("What does secularism require from public authorities when delivering public services?", "Compliance with equality and other applicable constitutional protections", "Automatic preference for the majority religion", "Denial of services to all minorities", "Replacement of constitutional law by private preference", "A"),
        ("Why is the Indian model of secularism sometimes described as allowing principled State intervention?", "The State may regulate or reform certain practices within constitutional limits while protecting religious freedom", "The State can arbitrarily abolish every religious right", "Religious groups have unlimited control over all government functions", "The Constitution prohibits all interaction between law and religion", "A"),
        ("What is the main difference between secularism and atheism?", "Secularism concerns how the State treats religion and belief; atheism concerns belief in the existence of deities", "They are legally and philosophically identical in every respect", "Secularism requires everyone to be atheist", "Atheism necessarily establishes a state religion", "A"),
        ("How can constitutional secularism protect freedom of conscience?", "By protecting individual belief and religious choice within applicable constitutional limits", "By requiring compulsory religious conversion", "By prohibiting all personal beliefs", "By allowing discrimination without legal review", "A"),
        ("Why is religious equality important for the legitimacy of public institutions?", "It supports fair treatment and equal citizenship across religious communities", "It requires officials to favour their own religion", "It prevents citizens from challenging public decisions", "It makes constitutional rights optional", "A"),
        ("Which approach best reflects constitutional secularism when religious practices conflict with another person's legally protected rights?", "Assess the conflict under applicable constitutional provisions and law", "Automatically prioritise one religion in every case", "Ignore all affected rights", "Allow private individuals to decide the legal outcome by force", "A"),
        ("What is the broad constitutional purpose of secularism in India?", "To support religious freedom, equality and peaceful coexistence within the constitutional framework", "To establish compulsory religious conformity", "To abolish fundamental rights", "To give unlimited legal power to one religious community", "A"),
    ],
}


def main():
    db = SessionLocal()

    try:
        lesson = (
            db.query(Lesson)
            .filter(
                Lesson.title == "Secularism",
                Lesson.topic == "Social Science"
            )
            .first()
        )

        if not lesson:
            print("ERROR: Secularism lesson was not found.")
            print("Check the exact lesson title and topic in your database.")
            return

        added = 0

        for difficulty, questions in QUESTION_BANK.items():
            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.difficulty == difficulty
                )
                .first()
            )

            if not quiz:
                quiz = Quiz(
                    lesson_id=lesson.id,
                    title=f"{lesson.title} - {difficulty}",
                    difficulty=difficulty
                )
                db.add(quiz)
                db.flush()

            existing = db.query(Question).filter(
                Question.quiz_id == quiz.id
            ).all()

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
                        correct_answer=new_correct_letter
                    )
                )

                existing_texts.add(question_text.strip().lower())
                existing.append(None)
                added += 1

            print(f"{difficulty}: prepared {min(len(existing), 30)}/30 questions.")

        db.commit()

        print("\n========== FINAL VERIFICATION ==========")
        total = 0

        for difficulty in ["Easy", "Medium", "Hard"]:
            quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.lesson_id == lesson.id,
                    Quiz.difficulty == difficulty
                )
                .first()
            )

            count = (
                db.query(Question)
                .filter(Question.quiz_id == quiz.id)
                .count()
                if quiz else 0
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