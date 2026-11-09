
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

# Format: (question, correct answer, wrong1, wrong2, wrong3)

BANK = {
    "Easy": [
        ("What is a paragraph?", "A group of related sentences about one main idea", "A single punctuation mark", "A list of unrelated words", "A collection of random letters"),
        ("What should a paragraph generally begin with?", "A topic sentence", "A concluding sentence", "A bibliography", "A question mark"),
        ("What does a topic sentence introduce?", "The main idea of the paragraph", "The author's address", "The page number", "The final reference"),
        ("What is the purpose of supporting sentences?", "To explain or develop the main idea", "To introduce unrelated topics", "To replace punctuation", "To end the entire essay"),
        ("What is the purpose of a concluding sentence?", "To bring the paragraph to a close", "To introduce a completely new topic", "To list the author's qualifications", "To begin another paragraph"),
        ("Which quality makes a paragraph effective?", "Unity", "Unrelated ideas", "Repeated information", "Missing sentences"),
        ("What does paragraph unity mean?", "All sentences support one central idea", "Every sentence discusses a different topic", "The paragraph contains only one word", "All sentences must have the same length"),
        ("What is coherence in paragraph writing?", "Logical and smooth connection of ideas", "Use of difficult words only", "Writing without punctuation", "Repeating every sentence"),
        ("Which sentence is most suitable as a topic sentence for a paragraph about exercise?", "Regular exercise improves physical and mental health.", "My favourite colour is blue.", "The library closes at five.", "Yesterday was a rainy day."),
        ("Which word is a suitable transition to show addition?", "Furthermore", "However", "Although", "Instead"),
        ("Which word indicates contrast?", "However", "Similarly", "Moreover", "Therefore"),
        ("Which word indicates a result?", "Therefore", "Meanwhile", "For example", "Similarly"),
        ("What should supporting details do?", "Provide explanations, examples or facts", "Distract from the main idea", "Introduce unrelated stories", "Repeat the title only"),
        ("Which punctuation mark normally ends a declarative sentence?", "Full stop", "Comma", "Apostrophe", "Colon"),
        ("How should sentences in a paragraph generally be organised?", "In a logical order", "In a completely random order", "Alphabetically in every case", "Without any connection"),
        ("What is a transition word?", "A word that connects ideas", "A word used only in titles", "A word without meaning", "A word that replaces every noun"),
        ("Which is an appropriate concluding sentence for a paragraph about reading?", "Thus, reading is a valuable habit that benefits everyone.", "My school is near the park.", "First, open the notebook.", "The weather was cloudy yesterday."),
        ("What should be avoided in a paragraph?", "Unrelated ideas", "Relevant examples", "Clear sentences", "Logical organisation"),
        ("What is the usual indentation at the beginning of a traditional paragraph?", "A small space before the first line", "A large blank page", "A space after every letter", "A line through the first sentence"),
        ("Which sentence best supports the topic 'Benefits of trees'?", "Trees provide oxygen and shade.", "The train arrived late.", "My shoes are black.", "The examination begins tomorrow."),
        ("What is the main purpose of a paragraph?", "To develop a particular idea", "To list unrelated topics", "To replace an entire book", "To display punctuation marks"),
        ("Which sentence is unrelated to a paragraph about healthy eating?", "The railway station is crowded.", "Fruits provide essential vitamins.", "Vegetables contain important nutrients.", "A balanced diet supports good health."),
        ("Why should a paragraph have a clear main idea?", "To help readers understand its focus", "To make the paragraph confusing", "To avoid using supporting details", "To increase unrelated information"),
        ("Which phrase introduces an example?", "For example", "On the contrary", "As a result", "In conclusion"),
        ("What should a writer do before writing a paragraph?", "Identify and organise the main ideas", "Write random sentences", "Ignore the topic", "Choose punctuation without planning"),
        ("Which is the best way to improve paragraph clarity?", "Use simple and precise language", "Use unnecessarily complicated sentences", "Repeat the same idea many times", "Avoid all punctuation"),
        ("What does a concluding sentence usually do?", "Summarises or reinforces the main idea", "Introduces unrelated evidence", "Changes the topic completely", "Lists every word used"),
        ("Which of these is a suitable paragraph topic?", "The Importance of Education", "A comma", "A single letter", "An unrelated collection of numbers"),
        ("What is proofreading?", "Checking writing for errors", "Adding random sentences", "Changing the topic", "Removing all punctuation"),
        ("What should the sentences in a paragraph have?", "A clear relationship with the main idea", "No connection with one another", "Different unrelated subjects", "Only questions")
    ],

    "Medium": [
        ("Which is the strongest topic sentence for a paragraph about environmental conservation?", "Protecting the environment requires responsible action from individuals and communities.", "The sky was blue yesterday.", "My favourite subject is mathematics.", "The shop sells different types of shoes."),
        ("A paragraph discusses the benefits of exercise, but one sentence describes the history of computers. What is the main problem?", "Lack of unity", "Correct coherence", "Effective conclusion", "Proper paragraph development"),
        ("Which technique improves coherence between sentences?", "Using appropriate transition words and logical sequencing", "Changing the subject repeatedly", "Removing all connecting words", "Repeating the topic sentence after every line"),
        ("Which sentence is the best supporting detail for the topic 'Online education has expanded learning opportunities'?", "Students can attend courses from different geographical locations.", "The moon appears bright at night.", "The city has several shopping centres.", "A farmer grows vegetables."),
        ("Which transition best completes the sentence: 'The road was damaged by heavy rain. _____, traffic was diverted.'?", "As a result", "For example", "Similarly", "In contrast"),
        ("Which sentence would be the most effective concluding sentence for a paragraph about teamwork?", "Therefore, cooperation and shared responsibility are essential for team success.", "Team members arrived at different times.", "The office has several windows.", "A new computer was purchased."),
        ("What is the most appropriate order for a paragraph explaining how to prepare tea?", "Boil water, add tea leaves, allow it to brew, and serve.", "Serve tea, boil water, and then add leaves.", "Add leaves after serving the tea.", "Describe unrelated drinks before beginning."),
        ("Which method is most useful when developing a paragraph through illustration?", "Providing relevant examples", "Repeating the heading", "Listing unrelated facts", "Avoiding explanations"),
        ("What is a paragraph developed through comparison and contrast intended to do?", "Show similarities and differences between subjects", "Describe only one subject without reference to another", "List events in chronological order", "Explain a process step by step"),
        ("Which transition phrase introduces a contrasting idea?", "On the other hand", "In addition", "For instance", "As a result"),
        ("Which sentence contains an effective supporting example?", "For instance, public libraries provide students with free access to books and reference materials.", "Libraries are places.", "I went outside yesterday.", "The car is red."),
        ("A paragraph begins with a clear topic sentence but ends without connecting to its main idea. Which element needs improvement?", "Concluding sentence", "Title formatting", "Author's signature", "Page numbering"),
        ("What is the main advantage of outlining before paragraph writing?", "It helps organise ideas in a logical sequence", "It eliminates the need for supporting details", "It encourages unrelated information", "It guarantees that no editing is needed"),
        ("Which sentence best maintains formal academic tone?", "Regular physical activity contributes to overall well-being.", "Exercise is super cool and awesome.", "Working out is totally wild!", "You gotta exercise or else."),
        ("Which technique can prevent unnecessary repetition in a paragraph?", "Using appropriate synonyms and pronouns", "Repeating every sentence exactly", "Removing all nouns", "Avoiding sentence variety"),
        ("What is the role of a transitional sentence?", "To connect one idea or paragraph with another", "To introduce spelling mistakes", "To remove the central argument", "To replace all supporting evidence"),
        ("Which paragraph development method explains events according to time?", "Chronological order", "Compare and contrast", "Classification", "Definition"),
        ("Which paragraph development method groups information into categories?", "Classification", "Chronological order", "Narration", "Cause and effect"),
        ("Which sentence is best suited to a cause-and-effect paragraph about deforestation?", "Removing trees can increase soil erosion and destroy wildlife habitats.", "The forest is located near a village.", "My favourite animal is a tiger.", "The library contains old books."),
        ("What is the purpose of a descriptive paragraph?", "To create a clear picture using sensory details", "To explain only mathematical calculations", "To list unrelated instructions", "To present arguments without description"),
        ("Which approach is best when writing a paragraph about a personal experience?", "Present events in a clear and meaningful sequence", "Mix events randomly", "Avoid describing relevant details", "Use only unrelated facts"),
        ("What is the problem with an excessively long paragraph?", "It may contain too many ideas and become difficult to follow", "It always has perfect unity", "It cannot contain supporting details", "It automatically becomes more coherent"),
        ("Which sentence best introduces a paragraph about time management?", "Effective time management helps individuals balance responsibilities and achieve goals.", "The ocean contains many species.", "My brother bought a bicycle.", "The weather changed suddenly."),
        ("Which transition indicates a sequence of steps?", "First", "Nevertheless", "Although", "In contrast"),
        ("What should a writer check while revising a paragraph?", "Unity, coherence, clarity and grammar", "Only the number of letters", "Only the font colour", "Only the page margins"),
        ("Which sentence is an example of irrelevant supporting detail in a paragraph about water conservation?", "The national cricket team won yesterday's match.", "Repairing leaking taps saves water.", "Rainwater harvesting reduces dependence on freshwater supplies.", "Turning off taps while brushing prevents wastage."),
        ("Which technique makes a paragraph more convincing?", "Including relevant facts and examples", "Making unsupported claims", "Using unrelated personal stories", "Avoiding the main idea"),
        ("What is the purpose of a concluding transition such as 'In conclusion'?", "To signal that the discussion is ending", "To introduce the first supporting example", "To indicate a contrast", "To begin a new unrelated argument"),
        ("Which sentence shows parallel structure?", "She enjoys reading, writing and painting.", "She enjoys reading, to write and painting.", "She enjoys to read, writing and paint.", "She enjoys reading, writes and to paint."),
        ("What is the best way to develop a paragraph on the causes of air pollution?", "Explain major causes with relevant examples and details", "Describe unrelated tourist attractions", "List solutions without mentioning causes", "Repeat the title in every sentence")
    ],

    "Hard": [
        ("A paragraph contains several relevant facts but lacks a clear relationship between them. Which revision would most directly improve it?", "Reorganise the facts and add logical transitions", "Add more unrelated facts", "Remove the topic sentence", "Replace every sentence with a question"),
        ("Which topic sentence provides the most focused argument for a paragraph on renewable energy?", "Expanding renewable energy can reduce dependence on fossil fuels while supporting long-term sustainability.", "Energy is important in modern life.", "Many countries have different climates.", "Technology has changed considerably."),
        ("A writer presents a claim, provides statistical evidence and explains how the evidence supports the claim. Which paragraph structure is being used?", "Point, evidence and explanation", "Random narration", "Unconnected description", "Question and answer without reasoning"),
        ("Which revision best improves the sentence transition: 'Public transport reduces traffic. It also lowers emissions. It can make cities more accessible.'?", "Public transport reduces traffic and emissions while making cities more accessible.", "Public transport. Traffic. Emissions. Cities.", "Public transport is useful. The weather is pleasant.", "Traffic exists. Public transport is a word."),
        ("A paragraph contains a strong topic sentence and supporting evidence, but introduces a new argument in its final sentence. What should the writer do?", "Move the new argument to a separate paragraph or remove it", "Keep it because conclusions should always introduce new topics", "Delete all supporting evidence", "Replace the topic sentence with the new argument"),
        ("Which method is most effective for developing a persuasive paragraph?", "State a claim, support it with evidence and address relevant objections", "Use emotional statements without explanation", "Repeat the claim without evidence", "Introduce several unrelated opinions"),
        ("Which sentence best maintains an objective academic tone?", "The findings indicate a measurable improvement in student performance.", "The results are unbelievably amazing!", "Everyone knows this method is the best.", "This research is obviously perfect."),
        ("What is the primary difference between revision and proofreading?", "Revision improves ideas and organisation, while proofreading checks surface errors", "Revision checks spelling only, while proofreading changes the argument", "Both involve only changing font size", "There is no difference between them"),
        ("Which organisational pattern is most appropriate for explaining the causes and consequences of climate change?", "Cause and effect", "Chronological biography", "Alphabetical listing", "Dialogue format"),
        ("A paragraph compares two teaching methods. Which structure would make the comparison easiest to follow?", "Discuss shared criteria for both methods in a consistent order", "Describe one method randomly and omit the other", "Include unrelated personal stories", "Discuss only the disadvantages of both methods"),
        ("Which sentence provides the strongest evidence-based support for the claim that reading improves vocabulary?", "Regular exposure to varied texts introduces readers to unfamiliar words in meaningful contexts.", "Reading is definitely the best activity ever.", "Everyone should read because it is nice.", "Books are available in many colours."),
        ("What is the purpose of a concession in a persuasive paragraph?", "To acknowledge a valid opposing point before responding to it", "To abandon the main argument completely", "To introduce an unrelated example", "To repeat the conclusion"),
        ("Which sentence contains a weak generalisation?", "All students learn in exactly the same way.", "Some students benefit from visual learning materials.", "Learning preferences may differ between individuals.", "Teaching methods can influence student engagement."),
        ("A paragraph uses 'this', 'they' and 'it' without clear references. What problem may result?", "Ambiguity in reference", "Improved precision", "Stronger evidence", "Better paragraph unity"),
        ("Which technique is most appropriate for concluding an analytical paragraph?", "Interpret the evidence and connect it to the central claim", "Introduce an unrelated quotation", "Add several new arguments without explanation", "Repeat every supporting sentence word for word"),
        ("Which sentence best demonstrates a logical qualification?", "Although the policy has limitations, it may improve access when supported by adequate infrastructure.", "The policy is perfect in every possible situation.", "The policy has no advantages or disadvantages.", "The policy should be accepted without evaluation."),
        ("What is the effect of using varied sentence structures in a paragraph?", "It can improve readability and maintain reader interest", "It automatically removes the need for coherence", "It makes every paragraph informal", "It prevents the use of supporting evidence"),
        ("Which paragraph structure is most suitable for explaining a scientific process?", "Present the stages in a logical sequence", "Compare unrelated historical figures", "List opinions without order", "Begin with the final result and omit the process"),
        ("A paragraph's evidence is relevant but insufficient to support its conclusion. What is the best improvement?", "Add stronger evidence and explain the connection to the conclusion", "Make the conclusion more dramatic", "Remove all references to evidence", "Add unrelated descriptions"),
        ("Which sentence best avoids an unsupported absolute claim?", "In many cases, regular feedback can improve student learning.", "Feedback always guarantees success for every student.", "Every student learns perfectly through feedback.", "Feedback is the only factor affecting education."),
        ("What is the main purpose of a controlling idea in a paragraph?", "To limit and guide the development of the topic", "To introduce every possible subject", "To replace supporting evidence", "To determine the number of punctuation marks"),
        ("Which approach best develops a paragraph about the advantages and limitations of artificial intelligence?", "Present benefits, discuss limitations and support both with examples", "Discuss only benefits and ignore limitations", "List technical terms without explanation", "Focus on unrelated inventions"),
        ("A paragraph moves from a broad statement to specific examples and then to a general conclusion. Which organisational pattern is this?", "General-to-specific development", "Random arrangement", "Reverse alphabetical order", "Dialogue-based development"),
        ("Which sentence is the most effective bridge between two paragraphs discussing education access and digital infrastructure?", "However, expanding educational access also depends on reliable digital infrastructure.", "My favourite sport is badminton.", "The examination was difficult.", "There are many kinds of trees."),
        ("Why should quotations be integrated into a paragraph rather than inserted without explanation?", "To show how the quoted material supports the writer's point", "To increase the word count without purpose", "To avoid explaining the argument", "To replace the topic sentence"),
        ("Which revision best improves conciseness?", "Remove redundant phrases while preserving the meaning", "Add repeated explanations", "Replace simple words with unnecessary jargon", "Repeat the topic sentence several times"),
        ("What is the most appropriate way to maintain coherence in a long paragraph?", "Use a consistent focus, logical progression and suitable transitions", "Change the central topic in every sentence", "Avoid all references to previous ideas", "Use as many unrelated examples as possible"),
        ("Which is the strongest concluding statement for a paragraph arguing for sustainable urban planning?", "Therefore, cities must balance economic growth, environmental protection and residents' needs.", "There are many buildings in cities.", "Urban areas contain roads and shops.", "I visited a city last summer."),
        ("What is a logical fallacy in paragraph writing?", "An error in reasoning that weakens an argument", "A correct use of supporting evidence", "A transition between related ideas", "A properly structured conclusion"),
        ("A writer uses examples that support the topic but ignores evidence that challenges the argument. What weakness may this create?", "One-sided reasoning and confirmation bias", "Perfect objectivity", "Improved balance", "Complete neutrality")
    ]
}


def validate_bank():
    for difficulty, questions in BANK.items():
        if len(questions) != 30:
            raise ValueError(f"{difficulty} must contain exactly 30 questions.")

        for item in questions:
            if len(item) != 5:
                raise ValueError(f"Invalid question format: {item}")

            question, answer, wrong1, wrong2, wrong3 = item
            options = [answer, wrong1, wrong2, wrong3]

            if len(set(options)) != 4:
                raise ValueError(f"Duplicate options in {difficulty}: {question}")


def main():
    validate_bank()
    print("Question bank validation successful.")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute(
            "SELECT id FROM lessons WHERE title=? AND topic=?",
            ("Paragraph Writing", "English")
        )
        row = cur.fetchone()

        if not row:
            raise Exception("Lesson 'Paragraph Writing' with topic 'English' was not found.")

        lesson_id = row[0]

        for difficulty, questions in BANK.items():
            cur.execute(
                "SELECT id FROM quizzes WHERE lesson_id=? AND difficulty=?",
                (lesson_id, difficulty)
            )
            quiz = cur.fetchone()

            if quiz:
                quiz_id = quiz[0]
            else:
                cur.execute(
                    """
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                    """,
                    (lesson_id, f"Paragraph Writing - {difficulty}", difficulty)
                )
                quiz_id = cur.lastrowid

            cur.execute(
                "SELECT COUNT(*) FROM questions WHERE quiz_id=?",
                (quiz_id,)
            )
            existing = cur.fetchone()[0]

            if existing > 30:
                raise Exception(f"{difficulty} already has {existing} questions.")

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
                        "SELECT COUNT(*) FROM questions WHERE quiz_id=? AND question=?",
                        (quiz_id, question_text)
                    )
                    if cur.fetchone()[0] == 0:
                        break

                    question_text = f"{question} (Version {suffix})"
                    suffix += 1

                cur.execute(
                    """
                    INSERT INTO questions (
                        quiz_id, question,
                        option_a, option_b, option_c, option_d,
                        correct_answer
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        quiz_id, question_text,
                        options[0], options[1], options[2], options[3],
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
                raise Exception(f"{difficulty} has {final_count}/30 questions.")

            print(f"{difficulty}: {final_count}/30 questions ready.")

        con.commit()
        print("\nSUCCESS: Paragraph Writing has exactly 90 questions!")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
