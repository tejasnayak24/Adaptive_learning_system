
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

# Format: (question, correct answer, wrong option 1, wrong option 2, wrong option 3)

BANK = {
    "Easy": [
        ("Passage: 'Riya wakes up at six every morning. She exercises for thirty minutes before going to college.' What does Riya do before college?", "Exercises", "Watches television", "Reads a novel", "Cooks breakfast"),
        ("Passage: 'The garden was full of colourful flowers, butterflies and birds.' Where does the passage take place?", "In a garden", "In a classroom", "In a market", "In a hospital"),
        ("Passage: 'Arun forgot his umbrella. When it started raining, he got completely wet.' Why did Arun get wet?", "He did not have an umbrella", "He went swimming", "He stayed indoors", "He wore a raincoat"),
        ("Passage: 'Meena saved a little money every week. After six months, she bought a bicycle.' What helped Meena buy the bicycle?", "Saving money regularly", "Borrowing money", "Winning a competition", "Selling her books"),
        ("Passage: 'The library was silent. Students were reading books and preparing for their examinations.' What were the students doing?", "Studying", "Playing football", "Singing songs", "Watching a movie"),
        ("Passage: 'Ravi planted a mango tree in his backyard. He watered it every day, and after several years it produced fruit.' What did Ravi do to care for the tree?", "Watered it regularly", "Cut its branches daily", "Moved it indoors", "Stopped giving it sunlight"),
        ("Passage: 'The train was scheduled to leave at 8 a.m., but it arrived at the station at 8:30 a.m.' What happened to the train?", "It was delayed", "It arrived early", "It was cancelled", "It left at midnight"),
        ("Passage: 'Anita enjoys painting landscapes. She often paints mountains, rivers and forests.' What is Anita interested in?", "Painting nature scenes", "Cooking food", "Playing cricket", "Writing computer programs"),
        ("Passage: 'The road was slippery because it had rained throughout the night.' Why was the road slippery?", "Because of the rain", "Because of heavy traffic", "Because of strong sunlight", "Because it was newly built"),
        ("Passage: 'The shopkeeper opened his store at nine in the morning and closed it at eight in the evening.' How many hours was the store open?", "Eleven hours", "Eight hours", "Nine hours", "Ten hours"),
        ("Passage: 'Children planted trees around their school to make the surroundings greener.' Why did the children plant trees?", "To improve the environment", "To block the school entrance", "To reduce classroom space", "To attract vehicles"),
        ("Passage: 'Priya missed the bus, so her father dropped her at school in his car.' How did Priya reach school?", "By car", "By bicycle", "By train", "On foot"),
        ("Passage: 'The farmer worked hard during the summer. He harvested a large quantity of rice in autumn.' What was the farmer rewarded with?", "A good harvest", "A new house", "A holiday abroad", "A sports trophy"),
        ("Passage: 'The baby began crying when the lights suddenly went off.' What might have frightened the baby?", "The sudden darkness", "The bright sunlight", "The sound of music", "The colourful toys"),
        ("Passage: 'During the holidays, Nikhil visited his grandparents in a village surrounded by green fields.' Where did Nikhil spend his holidays?", "At his grandparents' village", "At a shopping mall", "At his college", "At a railway station"),
        ("Passage: 'The team practised every evening and finally won the football tournament.' What contributed to the team's success?", "Regular practice", "Avoiding training", "Changing the rules", "Playing without preparation"),
        ("Passage: 'Sara wore a thick jacket because the temperature had dropped considerably.' What was the weather probably like?", "Cold", "Extremely hot", "Very humid", "Warm and sunny"),
        ("Passage: 'The museum displays ancient coins, sculptures and paintings.' What can visitors learn about at the museum?", "History and art", "Modern sports", "Cooking techniques", "Computer repair"),
        ("Passage: 'The doctor advised Rahul to drink more water and eat fresh fruits.' What was the doctor's advice about?", "Healthy habits", "Travelling abroad", "Learning mathematics", "Buying expensive clothes"),
        ("Passage: 'A little bird built its nest on a branch of the old tree.' Where did the bird build its nest?", "On a tree branch", "Inside a river", "Under a bridge", "On a road"),
        ("Passage: 'The classroom became noisy when the teacher left for a few minutes.' What happened when the teacher left?", "Students became noisy", "Students went home", "The examination started", "Everyone went to sleep"),
        ("Passage: 'Vikram read the instructions carefully before assembling the table.' What did Vikram do before assembling the table?", "Read the instructions", "Painted the table", "Sold the table", "Threw away the parts"),
        ("Passage: 'The village received heavy rainfall, and the nearby river began to overflow.' What caused the river to overflow?", "Heavy rainfall", "A long drought", "Strong sunlight", "A forest fire"),
        ("Passage: 'Neha gave her old storybooks to children who could not afford to buy books.' What quality does Neha demonstrate?", "Generosity", "Selfishness", "Dishonesty", "Laziness"),
        ("Passage: 'The supermarket offers fresh vegetables, fruits, milk and bread.' What type of place is described?", "A supermarket", "A hospital", "A library", "A cinema"),
        ("Passage: 'The students listened carefully while the teacher explained the science experiment.' What were the students doing?", "Paying attention", "Arguing loudly", "Leaving the classroom", "Playing games"),
        ("Passage: 'The old bridge was closed because engineers found cracks in its structure.' Why was the bridge closed?", "It was unsafe", "It was newly painted", "It was too short", "It was being decorated"),
        ("Passage: 'Mohan missed his friends, so he called them during the weekend.' Why did Mohan call his friends?", "He wanted to talk to them", "He wanted to borrow a car", "He needed directions to school", "He wanted to cancel a meeting"),
        ("Passage: 'The sun disappeared behind the clouds, and the sky became dark.' What change occurred in the sky?", "It became darker", "It became brighter", "It turned completely red", "It became cloudless"),
        ("Passage: 'After completing her homework, Latha watched her favourite television programme.' What did Latha do first?", "Completed her homework", "Watched television", "Went shopping", "Played outdoors")
    ],

    "Medium": [
        ("Passage: 'The city introduced bicycle-sharing stations to reduce traffic congestion. Many residents began using bicycles for short journeys.' What is the main purpose of this initiative?", "To reduce traffic congestion", "To increase fuel consumption", "To discourage outdoor activity", "To replace public libraries"),
        ("Passage: 'Although the mountain trail was steep, the hikers continued climbing because they wanted to see the sunrise from the summit.' What motivated the hikers?", "The opportunity to see the sunrise", "The desire to avoid exercise", "The need to find a hotel", "The fear of returning home"),
        ("Passage: 'Maya initially struggled with mathematics. Instead of giving up, she attended extra classes and practised daily. Her grades gradually improved.' What is the central message?", "Consistent effort can improve performance", "Mathematics cannot be learned", "Extra classes always guarantee full marks", "Difficult subjects should be avoided"),
        ("Passage: 'The restaurant replaced plastic containers with biodegradable packaging. This decision increased its expenses slightly but reduced its environmental impact.' What trade-off did the restaurant accept?", "Higher expenses for environmental benefits", "Lower quality for higher profits", "More plastic for faster service", "Less food for cheaper packaging"),
        ("Passage: 'The village once depended entirely on rainfall for farming. After a drought, residents constructed rainwater harvesting systems.' What can be inferred about the residents?", "They adapted to an environmental challenge", "They stopped farming permanently", "They preferred wasting water", "They opposed new solutions"),
        ("Passage: 'The author's first novel received little attention. Years later, after several successful publications, readers began discovering the earlier book.' What does this suggest?", "Recognition may come long after work is produced", "First novels are always unsuccessful", "Readers never appreciate older books", "Publishing success depends only on age"),
        ("Passage: 'The school introduced a reading hour every afternoon. Teachers noticed that students gradually developed stronger vocabulary and reading habits.' What is the likely relationship described?", "Regular reading supported language development", "Reading reduced students' vocabulary", "Afternoon classes prevented learning", "Vocabulary developed without practice"),
        ("Passage: 'When the power failed, the employees continued working using stored battery power and emergency lighting.' What does this reveal about the workplace?", "It had prepared for unexpected disruptions", "It had no emergency arrangements", "It stopped all operations permanently", "It depended entirely on natural light"),
        ("Passage: 'The scientist repeated the experiment several times before publishing the results.' Why did the scientist repeat the experiment?", "To check the reliability of the results", "To change the subject of research", "To avoid collecting evidence", "To make the experiment more expensive"),
        ("Passage: 'Despite having limited resources, the community organised a successful cultural festival through donations and volunteer work.' What made the festival possible?", "Community cooperation", "Government restrictions", "Expensive advertisements", "Professional entertainers alone"),
        ("Passage: 'The advertisement described the product as revolutionary, but it provided no independent evidence to support its claims.' What should a careful reader do?", "Question the claims and seek reliable evidence", "Believe every promotional statement", "Purchase the product immediately", "Ignore all other information"),
        ("Passage: 'The coastal town developed warning systems and evacuation routes after experiencing severe cyclones.' What was the main objective?", "To improve disaster preparedness", "To encourage tourism during storms", "To increase coastal construction", "To eliminate all rainfall"),
        ("Passage: 'A journalist interviewed residents from different neighbourhoods before writing about the city's housing problem.' Why was this approach useful?", "It provided different perspectives", "It eliminated the need for facts", "It guaranteed agreement among residents", "It made the article fictional"),
        ("Passage: 'The old factory building was converted into a public art centre, preserving its original walls and industrial features.' What does this example demonstrate?", "Adaptive reuse of an existing structure", "Complete destruction of historical buildings", "Expansion of factory production", "Replacement of art with industry"),
        ("Passage: 'Rohan rejected the first job offer because it did not match his career goals. He continued applying until he found a suitable position.' What quality does Rohan demonstrate?", "Patience and commitment to his goals", "Indifference towards his future", "Fear of professional growth", "Dependence on others' decisions"),
        ("Passage: 'The report noted that rainfall had increased, but crop production remained low because the soil had lost essential nutrients.' What is the main explanation for poor crop production?", "Poor soil quality", "Insufficient rainfall", "Excessive sunlight", "Lack of agricultural land"),
        ("Passage: 'The speaker used simple examples and familiar situations to explain a complicated scientific theory.' Why was this effective?", "It made the theory easier to understand", "It made the theory less accurate", "It removed the need for explanation", "It confused the audience"),
        ("Passage: 'The company allowed employees to work remotely twice a week. Employees reported saving commuting time, although some missed face-to-face interaction.' What is the main idea?", "Remote work offers benefits as well as challenges", "Remote work always reduces productivity", "Office interaction is unnecessary", "Commuting is the only workplace concern"),
        ("Passage: 'The river looked clean, but laboratory tests detected harmful chemicals in the water.' What lesson does this passage suggest?", "Appearance alone cannot establish safety", "Clear water is always safe to drink", "Laboratory tests are unnecessary", "Pollution is always visible"),
        ("Passage: 'The historian compared letters, government records and newspaper reports before drawing conclusions about the event.' What research method did the historian use?", "Cross-checking multiple sources", "Relying on a single personal opinion", "Avoiding historical evidence", "Using fictional accounts only"),
        ("Passage: 'The new public transport route connected several residential areas to the industrial district.' What was a likely benefit?", "Easier commuting for workers", "Increased distance between workplaces", "Reduced access to employment", "Complete elimination of road travel"),
        ("Passage: 'The author describes a crowded railway station using words such as restless, hurried and impatient.' What is the likely atmosphere?", "Busy and tense", "Calm and peaceful", "Empty and silent", "Festive and relaxed"),
        ("Passage: 'The student read the entire chapter but could not answer questions requiring comparisons between its ideas.' What reading skill does the student need to improve?", "Analytical comprehension", "Alphabet recognition", "Handwriting speed", "Pronunciation"),
        ("Passage: 'A local business supported a school library by donating books every year without seeking publicity.' What can be inferred about the business?", "It values community support", "It only helps for advertising", "It opposes education", "It wants to close the library"),
        ("Passage: 'The article presents both the advantages and disadvantages of artificial intelligence in education.' What is the author's approach?", "Balanced and informative", "Entirely humorous", "Strongly one-sided", "Unrelated to the topic"),
        ("Passage: 'After the city introduced separate waste bins, the amount of recyclable material collected increased.' What does the evidence suggest?", "Waste segregation can improve recycling", "Separate bins increase pollution", "Recycling depends only on weather", "Residents stopped producing waste"),
        ("Passage: 'The athlete lost the first two matches but studied her opponents and changed her strategy before winning the final.' What does the story highlight?", "Learning and adapting after setbacks", "Winning without preparation", "Avoiding competition", "Depending entirely on luck"),
        ("Passage: 'The museum reduced ticket prices for students and senior citizens to make its exhibitions more accessible.' What was the museum trying to achieve?", "Wider public access", "Higher prices for everyone", "Reduced visitor participation", "Removal of educational displays"),
        ("Passage: 'The article explains how urban trees reduce heat, absorb carbon dioxide and provide shelter for birds.' What is the main focus?", "The environmental benefits of urban trees", "The commercial value of timber", "The history of city buildings", "The dangers of outdoor exercise"),
        ("Passage: 'The manager asked the team to submit feedback anonymously so that employees could express concerns honestly.' Why was anonymity useful?", "It encouraged honest feedback without fear of identification", "It prevented employees from sharing opinions", "It guaranteed that every suggestion would be accepted", "It removed the need for management")
    ],

    "Hard": [
        ("Passage: 'The report celebrates the city's technological growth but warns that rapid development has widened the gap between wealthy and low-income neighbourhoods.' Which statement best captures the author's position?", "Progress should be evaluated alongside its social consequences", "Technological growth should always be stopped", "Economic inequality is unrelated to development", "All neighbourhoods benefit equally from innovation"),
        ("Passage: 'The historian notes that official records describe the reform as universally welcomed, while private letters reveal considerable public resistance.' What is the most reasonable inference?", "Official accounts may not represent every viewpoint", "Private letters are always inaccurate", "The reform had no supporters", "Historical records should never be trusted"),
        ("Passage: 'The scientist's findings challenge a widely accepted theory, but the author repeatedly reminds readers that further testing is necessary.' What is the author's attitude?", "Cautiously open to new evidence", "Completely dismissive of research", "Certain that the theory is false", "Uninterested in scientific debate"),
        ("Passage: 'The town's economic revival was attributed to tourism. However, the article points out that local wages remained unchanged while property prices increased.' What concern is implied?", "Economic growth may not benefit all residents equally", "Tourism always reduces property prices", "Local wages determine visitor numbers", "Property prices have no social impact"),
        ("Passage: 'The poet describes the city as a machine that never sleeps, where people move like gears in an endless cycle.' What literary effect is created?", "A metaphor suggesting mechanical and repetitive urban life", "A literal description of factory equipment", "A humorous account of rural farming", "A comparison between nature and childhood"),
        ("Passage: 'Although the policy reduced average waiting times, patients in remote areas continued to experience long delays.' Which conclusion is best supported?", "The policy improved overall performance but did not solve every access problem", "The policy had no effect anywhere", "Remote patients received the fastest service", "Average waiting times increased everywhere"),
        ("Passage: 'The author first presents a popular belief, then introduces research that contradicts it, and finally examines why the belief persists.' How is the passage organised?", "Belief, counter-evidence and explanation", "Chronological biography and conclusion", "Problem, recipe and advertisement", "Description followed by unrelated dialogue"),
        ("Passage: 'The committee praised the proposal's ambition but questioned its financial assumptions and the absence of a clear implementation plan.' What is the committee's overall response?", "Supportive of the goal but critical of its feasibility", "Completely opposed to the proposal's purpose", "Unconditionally enthusiastic", "Indifferent to its financial details"),
        ("Passage: 'The novel's narrator insists that the family is happy, yet describes long silences, locked rooms and conversations that abruptly end.' What may the reader infer?", "The narrator's description may conceal family tension", "The family has no secrets", "The narrator provides a fully objective account", "The setting is designed to show celebration"),
        ("Passage: 'The author argues that digital access is necessary for modern education, but warns that technology cannot replace skilled teachers.' Which statement best reflects the argument?", "Technology should support rather than replace effective teaching", "Digital tools make teachers unnecessary", "Education should avoid all technology", "Teacher quality is unrelated to learning"),
        ("Passage: 'The company announced record profits while reducing staff benefits. Its statement described the decision as necessary for long-term sustainability.' What critical question should readers consider?", "Who bears the cost of the company's financial strategy?", "How many products does the company manufacture?", "What colour is the company logo?", "When was the company founded?"),
        ("Passage: 'The author describes the river as generous in spring and unforgiving during the monsoon.' What does this contrast suggest?", "Nature can provide benefits while also posing risks", "The river behaves exactly like a person", "The river remains unchanged throughout the year", "The author dislikes all natural landscapes"),
        ("Passage: 'A survey found that most respondents supported public parks, but participation was much lower among residents working long hours.' What limitation should be considered?", "Survey responses do not necessarily translate into participation", "Public parks are unpopular", "Working hours have no effect on participation", "The survey proves parks are unnecessary"),
        ("Passage: 'The article quotes three experts who agree on the problem but disagree sharply about the proposed solution.' What is the main effect of including these views?", "It demonstrates that agreement on a problem does not ensure agreement on solutions", "It proves that experts cannot understand problems", "It removes the need for evidence", "It suggests that only one expert matters"),
        ("Passage: 'The memoir describes a childhood home in loving detail, but repeatedly mentions the sound of a train leaving the station.' What might the recurring image symbolise?", "Separation, change or departure", "Financial success", "Agricultural growth", "A fear of mathematics"),
        ("Passage: 'The researcher reports a strong correlation between exercise and improved mood but explicitly avoids claiming that exercise alone caused the improvement.' Why?", "Correlation does not by itself establish causation", "Exercise cannot influence mood", "Research findings must always be ignored", "Mood cannot be measured"),
        ("Passage: 'The editorial calls the proposal a bold step forward, then questions whether its promised benefits can be delivered without adequate funding.' What is the tone?", "Qualified optimism", "Unrestrained celebration", "Complete hostility", "Detached humour"),
        ("Passage: 'The author describes a historic building's restoration as successful because its original character was preserved while modern safety standards were introduced.' What principle is emphasised?", "Balancing heritage preservation with contemporary needs", "Replacing old structures without consideration", "Avoiding all modern safety measures", "Prioritising appearance over structural safety"),
        ("Passage: 'The speaker says, \"We have never been so connected, and yet so distant,\" referring to people's reliance on digital communication.' What contrast is being highlighted?", "Greater technological connection alongside possible social isolation", "Improved transport and reduced travel", "Economic growth and environmental protection", "More books and less education"),
        ("Passage: 'The article presents a dramatic decline in forest cover but notes that the data comes from only one region and one year.' What should a critical reader recognise?", "The evidence may be insufficient to generalise across all regions and years", "The decline must be identical everywhere", "One-year data is always meaningless", "Forest cover cannot be measured"),
        ("Passage: 'The narrator describes the politician's promises as a familiar song that returns every election season.' What does this comparison imply?", "The promises are repeated and may lack originality", "The politician is a professional musician", "The election is a musical event", "The promises are entirely new"),
        ("Passage: 'The article argues that individual recycling is useful but cannot compensate for industrial pollution and weak waste-management systems.' What is the central argument?", "Environmental solutions require both individual and systemic action", "Individual recycling is completely useless", "Industries have no responsibility for pollution", "Waste management should be left to households"),
        ("Passage: 'The critic praises the novel's vivid descriptions while noting that its characters lack psychological depth.' What kind of evaluation is this?", "A mixed assessment recognising strengths and weaknesses", "An entirely negative review", "An uncritical endorsement", "A summary unrelated to literary quality"),
        ("Passage: 'The report claims that a new transport project will reduce emissions, but its calculations exclude the environmental cost of construction.' What issue does this raise?", "The assessment may overlook important lifecycle impacts", "Construction has no environmental impact", "Transport projects cannot reduce emissions", "Emissions are unrelated to infrastructure"),
        ("Passage: 'The author explains that a language changes as communities migrate, interact and adopt new expressions.' Which assumption underlies the passage?", "Language is dynamic and shaped by social interaction", "Language remains identical across generations", "Migration prevents language development", "New expressions always damage communication"),
        ("Passage: 'The researcher acknowledges that the sample is small but argues that the findings provide a useful starting point for further investigation.' What is the most accurate interpretation?", "The results are preliminary rather than conclusive", "The research is completely invalid", "The findings prove a universal law", "Further research is unnecessary"),
        ("Passage: 'The article begins with a personal story about one family's struggle, then introduces national statistics about housing affordability.' Why does the author use this structure?", "To connect an individual experience with a broader social issue", "To replace factual information with entertainment", "To argue that statistics are unreliable", "To avoid discussing the main topic"),
        ("Passage: 'The author states that silence in a meeting may indicate agreement, uncertainty or fear, depending on the circumstances.' What does this suggest about interpretation?", "The same behaviour can have different meanings in different contexts", "Silence always means agreement", "People communicate only through speech", "Context is irrelevant to understanding"),
        ("Passage: 'The article describes a city that built flood barriers but continued allowing construction on vulnerable land.' What contradiction does the author expose?", "Protective infrastructure may be undermined by risky planning decisions", "Flood barriers always increase flooding", "Construction prevents all natural disasters", "Urban planning has no connection to flood risk"),
        ("Passage: 'The conclusion states that no single policy can solve the education gap, but coordinated improvements in funding, teacher support and access are necessary.' What is the author's final position?", "Complex educational problems require coordinated solutions", "Funding alone will solve every problem", "Teacher support is unnecessary", "Educational access should be reduced")
    ]
}


def validate_bank():
    for difficulty, questions in BANK.items():
        if len(questions) != 30:
            raise ValueError(
                f"{difficulty} must contain exactly 30 questions."
            )

        for item in questions:
            if len(item) != 5:
                raise ValueError(f"Invalid question format: {item}")

            question, answer, wrong1, wrong2, wrong3 = item
            options = [answer, wrong1, wrong2, wrong3]

            if len(set(options)) != 4:
                raise ValueError(
                    f"Duplicate options in {difficulty}: {question}"
                )


def main():
    validate_bank()
    print("Question bank validation successful.")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Reading Comprehension", "English")
        )
        row = cur.fetchone()

        if not row:
            raise Exception(
                "Lesson 'Reading Comprehension' with topic 'English' was not found."
            )

        lesson_id = row[0]

        for difficulty, questions in BANK.items():
            cur.execute(
                """
                SELECT id FROM quizzes
                WHERE lesson_id=? AND difficulty=?
                """,
                (lesson_id, difficulty)
            )
            quiz = cur.fetchone()

            if quiz:
                quiz_id = quiz[0]
            else:
                cur.execute(
                    """
                    INSERT INTO quizzes
                    (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                    """,
                    (
                        lesson_id,
                        f"Reading Comprehension - {difficulty}",
                        difficulty
                    )
                )
                quiz_id = cur.lastrowid

            cur.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id=?",
                (quiz_id,)
            )
            existing = cur.fetchone()[0]

            if existing > 30:
                raise Exception(
                    f"{difficulty} already has {existing} questions."
                )

            inserted = 0

            for question, answer, wrong1, wrong2, wrong3 in questions:
                if existing + inserted >= 30:
                    break

                options = [answer, wrong1, wrong2, wrong3]
                random.shuffle(options)
                correct_letter = "ABCD"[options.index(answer)]

                question_text = question
                suffix = 2

                while True:
                    cur.execute(
                        """
                        SELECT COUNT(*) FROM questions
                        WHERE quiz_id=? AND question=?
                        """,
                        (quiz_id, question_text)
                    )

                    if cur.fetchone()[0] == 0:
                        break

                    question_text = f"{question} (Version {suffix})"
                    suffix += 1

                cur.execute(
                    """
                    INSERT INTO questions
                    (
                        quiz_id, question,
                        option_a, option_b, option_c, option_d,
                        correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        quiz_id,
                        question_text,
                        options[0],
                        options[1],
                        options[2],
                        options[3],
                        correct_letter
                    )
                )

                inserted += 1

            cur.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id=?",
                (quiz_id,)
            )
            final_count = cur.fetchone()[0]

            if final_count != 30:
                raise Exception(
                    f"{difficulty} has {final_count}/30 questions."
                )

            print(f"{difficulty}: {final_count}/30 questions ready.")

        con.commit()
        print("\nSUCCESS: Reading Comprehension has exactly 90 questions!")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
