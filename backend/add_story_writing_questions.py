
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

# Format: (question, correct answer, wrong1, wrong2, wrong3)

BANK = {
    "Easy": [
        ("What is a story?", "A sequence of events involving characters", "A list of unrelated words", "A mathematical equation", "A collection of punctuation marks"),
        ("What is the setting of a story?", "The time and place where events happen", "The list of characters only", "The final sentence", "The author's signature"),
        ("What is the plot of a story?", "The sequence of events", "The title of the story", "The author's address", "The list of difficult words"),
        ("What is the climax of a story?", "The point of greatest tension or excitement", "The opening greeting", "The list of characters", "The description of the setting only"),
        ("What is the introduction of a story called?", "Exposition", "Climax", "Resolution", "Conclusion"),
        ("What is the resolution of a story?", "The part where the main conflict is settled", "The part where characters are introduced", "The beginning of the conflict", "The title of the story"),
        ("Who tells the story?", "Narrator", "Protagonist only", "Editor", "Illustrator"),
        ("What is a character in a story?", "A person or being involved in the events", "The place where the story happens", "The lesson at the end", "The sequence of paragraphs"),
        ("What is dialogue?", "A conversation between characters", "A description of scenery", "A list of events", "A story title"),
        ("Which punctuation marks are commonly used to show direct speech?", "Quotation marks", "Brackets only", "Hyphens only", "Apostrophes only"),
        ("What is the conflict in a story?", "The problem or struggle faced by characters", "The author's name", "The story's publication date", "The list of chapters"),
        ("What is a short story?", "A brief fictional narrative", "A long research report", "A collection of unrelated facts", "A formal application"),
        ("Which tense is commonly used to narrate completed past events?", "Simple past tense", "Simple future tense", "Present continuous tense", "Future perfect tense"),
        ("What is a moral in a story?", "A lesson about life or behaviour", "The name of the main character", "The location of the story", "The opening paragraph"),
        ("Which of these is an example of a story setting?", "A village during the rainy season", "A character's name", "A conversation between friends", "The final lesson"),
        ("What is the role of a title?", "To identify or introduce the story", "To explain every event in detail", "To replace the ending", "To list all dialogues"),
        ("What is a protagonist?", "The central character of a story", "The person who edits the story", "The place where events happen", "The final event"),
        ("What is an antagonist?", "A character or force opposing the protagonist", "The narrator in every story", "The story's setting", "The person who writes the title"),
        ("Which element makes a story interesting?", "A meaningful plot and engaging characters", "Unrelated sentences", "Repeated words without purpose", "Missing events"),
        ("What is a fictional story?", "A story created from imagination", "A verified scientific report", "A newspaper timetable", "A list of historical dates only"),
        ("Which part of a story usually introduces its characters?", "Beginning", "Climax", "Resolution", "Final moral only"),
        ("What does a narrator's point of view describe?", "The perspective from which the story is told", "The number of pages", "The story's title length", "The author's handwriting"),
        ("Which word is commonly used to begin a sequence of events?", "First", "Because", "Although", "Unless"),
        ("What is the purpose of descriptive language in a story?", "To help readers imagine people, places and events", "To remove all details", "To make the plot disappear", "To replace characters"),
        ("What should a good story ending provide?", "A satisfying conclusion to the events", "An unrelated new beginning", "An unfinished conflict without purpose", "A list of random words"),
        ("Which of these is a suitable story opening?", "One rainy evening, a young girl discovered a mysterious box.", "The answer to the equation is twelve.", "Please grant me two days of leave.", "The meeting will begin at ten."),
        ("What is a theme in a story?", "The central idea or message", "The author's home address", "The number of characters", "The font used in the text"),
        ("Why is paragraphing important in story writing?", "It organises events and improves readability", "It removes the need for a plot", "It changes the story's characters", "It replaces punctuation"),
        ("What is the purpose of an interesting opening?", "To capture the reader's attention", "To reveal every event immediately", "To end the story before it begins", "To list unrelated facts"),
        ("Which of these is a common story genre?", "Mystery", "Invoice", "Application form", "Timetable")
    ],

    "Medium": [
        ("Which sequence represents a common story structure?", "Exposition, rising action, climax, falling action, resolution", "Climax, exposition, resolution, rising action, title", "Resolution, title, exposition, climax, introduction", "Rising action, conclusion, title, exposition, climax"),
        ("What is rising action?", "Events that build tension and lead towards the climax", "The final explanation of the story", "The introduction of the author's name", "The section containing only the moral"),
        ("What is falling action?", "Events that follow the climax and lead towards the resolution", "The events before the characters are introduced", "The first sentence of the story", "The title and subtitle"),
        ("Which narrative perspective uses the pronoun 'I'?", "First-person point of view", "Second-person point of view", "Third-person point of view", "Omniscient point of view"),
        ("Which pronouns are commonly used in third-person narration?", "He, she and they", "I and me", "You and your", "We and us only"),
        ("What is an omniscient narrator?", "A narrator who knows the thoughts and feelings of multiple characters", "A narrator who knows only their own thoughts", "A character who never appears in the story", "A narrator who describes only the setting"),
        ("Which technique introduces information about a past event?", "Flashback", "Foreshadowing", "Cliffhanger", "Dialogue tag"),
        ("What is foreshadowing?", "Giving hints about events that may happen later", "Explaining only past events", "Repeating the story title", "Describing a character's appearance"),
        ("What is a cliffhanger?", "An ending that leaves an important situation unresolved", "A complete explanation of every event", "A description of the setting", "A list of characters"),
        ("Which technique is most useful for developing a believable character?", "Showing the character's actions, dialogue and decisions", "Giving the character many unrelated names", "Avoiding all character interaction", "Changing the character's identity in every scene"),
        ("What is character development?", "The way a character changes or grows throughout a story", "The process of choosing a story title", "The description of the publication date", "The arrangement of page numbers"),
        ("Which sentence best demonstrates sensory description?", "The warm bread smelled of butter and filled the kitchen with a rich aroma.", "The bread was there.", "Someone bought bread yesterday.", "Bread is a common food."),
        ("What is the purpose of dialogue in a story?", "To reveal character, develop relationships and move the plot forward", "To replace the setting completely", "To provide only the author's biography", "To avoid developing characters"),
        ("Which is the correct punctuation for a direct statement?", "\"I will return tomorrow,\" said Meera.", "I will return tomorrow said Meera.", "\"I will return tomorrow, said Meera.", "I will return tomorrow,\" said Meera."),
        ("What is an internal conflict?", "A struggle within a character's mind or emotions", "A disagreement between two countries", "A battle between two armies only", "A storm affecting the setting"),
        ("What is an external conflict?", "A struggle between a character and an outside force", "A character's private doubt only", "A narrator's writing style", "A story's central theme"),
        ("Which of these is an example of personification?", "The wind whispered through the trees.", "The tree was tall.", "The wind was strong.", "The leaves were green."),
        ("Which figure of speech compares two things using 'like' or 'as'?", "Simile", "Metaphor", "Irony", "Hyperbole"),
        ("Which sentence contains a metaphor?", "Her voice was music to his ears.", "Her voice was as soft as music.", "She spoke very softly.", "She spoke to her friend."),
        ("What is a subplot?", "A secondary storyline that supports or connects with the main plot", "The title of the story", "The story's final sentence", "A list of characters without events"),
        ("Why should a writer maintain consistency in a story's setting?", "To preserve continuity and avoid confusing readers", "To prevent characters from speaking", "To remove the main conflict", "To avoid describing the environment"),
        ("What is the purpose of a plot twist?", "To introduce an unexpected development that changes the reader's understanding", "To repeat the introduction", "To remove all characters", "To explain the author's biography"),
        ("Which opening technique begins a story in the middle of an action?", "In medias res", "Flashback", "Epilogue", "Resolution"),
        ("What is an epilogue?", "A section after the main story that provides additional information", "The opening sentence", "The central conflict", "The first appearance of the protagonist"),
        ("Which is the best way to create suspense?", "Gradually reveal information while increasing uncertainty or danger", "Explain every mystery immediately", "Avoid all conflict", "Repeat the same event without change"),
        ("What is a reliable way to show a character's emotions?", "Describe their actions, expressions and dialogue", "State unrelated facts about the setting", "Change the story's title", "Remove all character interactions"),
        ("Which sentence best shows rather than tells?", "Ravi clenched his fists and paced across the room.", "Ravi was angry.", "Ravi felt an emotion.", "Ravi had a problem."),
        ("What is the function of a story's theme?", "To communicate an underlying idea or message", "To identify the narrator's age", "To determine the number of dialogues", "To replace the plot"),
        ("Why should the climax be connected to the central conflict?", "It provides the major turning point in the story's main struggle", "It introduces an unrelated character", "It replaces the setting", "It explains the author's qualifications"),
        ("Which revision improves the pacing of a story?", "Adjust the detail and length of scenes according to their importance", "Describe every minor action equally", "Remove all important events", "Repeat the same dialogue several times")
    ],

    "Hard": [
        ("A story begins with the protagonist discovering a crime and later reveals the events that led to it. Which structure is being used?", "A non-linear narrative with flashbacks", "A purely chronological narrative", "A list-based narrative", "A narrative without a plot"),
        ("Which approach creates the most effective character arc?", "Show gradual changes in beliefs or behaviour resulting from important experiences", "Change the character's personality without explanation", "Keep the character unrelated to the central conflict", "Describe the character only once"),
        ("A narrator describes events but misunderstands the true motives of other characters. What narrative device may this demonstrate?", "Unreliable narration", "Omniscient narration", "Objective reporting", "Chronological narration"),
        ("What is dramatic irony?", "The audience knows something important that a character does not", "A character knows every future event", "The story contains an unexpected joke only", "The narrator describes the setting in detail"),
        ("Which technique is most effective for revealing a character's hidden motivation?", "Use actions, dialogue and internal thoughts that gradually expose the motivation", "Explain the motivation only in the title", "Avoid showing the character's decisions", "Introduce unrelated descriptions"),
        ("A story's ending changes the meaning of an earlier event without contradicting established facts. What makes this effective?", "The twist reinterprets earlier clues in a coherent way", "The twist introduces random information", "The twist ignores the established plot", "The twist removes the central characters"),
        ("Which narrative technique allows readers to understand a character's private thoughts directly?", "Interior monologue", "External dialogue only", "Stage directions", "A descriptive title"),
        ("What is the main advantage of using a limited third-person narrator?", "It provides access to one character's perspective while retaining third-person narration", "It reveals every character's thoughts equally", "It eliminates the narrator", "It prevents the use of dialogue"),
        ("Which approach best integrates a subplot into the main story?", "Connect the subplot to the central theme or influence the main conflict", "Allow it to introduce unrelated events without purpose", "Use it to repeat the opening", "Make it contradict the main story's setting"),
        ("What is the purpose of a red herring in a mystery story?", "To mislead readers with a plausible but incorrect clue", "To reveal the culprit immediately", "To describe the protagonist's childhood", "To provide the final moral"),
        ("Which approach is most effective when building suspense in a mystery?", "Distribute clues and revelations while controlling what readers know", "Reveal every answer in the first paragraph", "Avoid introducing questions or uncertainty", "Repeat the same clue without development"),
        ("A character makes a morally difficult choice between loyalty and honesty. What type of conflict is central?", "Internal moral conflict", "Purely environmental conflict", "Conflict between unrelated settings", "A conflict without consequences"),
        ("Which statement best describes subtext in dialogue?", "The implied meaning beneath the words characters speak", "The exact words printed in the title", "A list of events in chronological order", "The narrator's page numbering"),
        ("Why might an author use an open ending?", "To leave some questions unresolved and invite interpretation", "To ensure that every detail is explained", "To remove the story's central theme", "To prevent readers from understanding any event"),
        ("Which technique is most effective for maintaining a consistent narrative voice?", "Use consistent vocabulary, tone and perspective throughout the narration", "Change the narrator's identity without explanation", "Switch between unrelated tenses randomly", "Use contradictory descriptions of the same speaker"),
        ("What is the effect of juxtaposing two contrasting scenes?", "It highlights differences and can deepen the story's meaning", "It removes the relationship between scenes", "It prevents the development of themes", "It makes all characters identical"),
        ("Which approach makes a fictional setting integral to the plot?", "Allow environmental conditions to influence characters' choices and events", "Mention the setting once and never use it again", "Describe scenery unrelated to the conflict", "Use place names without context"),
        ("What is an archetype in storytelling?", "A recurring character, symbol or situation pattern", "A unique spelling mistake", "A type of punctuation", "A list of publication details"),
        ("Which revision best improves a story with an abrupt climax?", "Develop the conflict and character motivations more gradually before the turning point", "Remove the rising action", "Add an unrelated ending", "Introduce the antagonist only after the resolution"),
        ("What is the purpose of a motif in a story?", "To repeat a meaningful element that reinforces a theme", "To replace the plot with decoration", "To introduce every character", "To identify the author's address"),
        ("A story is narrated by several characters, each presenting a different interpretation of the same event. What technique is this?", "Multiple perspectives", "Single first-person narration", "Objective narration", "A linear description"),
        ("Which approach best prevents a plot hole?", "Check that events follow the established rules and information of the story", "Add unexplained events whenever convenient", "Change established facts without explanation", "Ignore cause-and-effect relationships"),
        ("What is the narrative function of an inciting incident?", "It introduces the event that sets the main story conflict in motion", "It resolves the entire conflict", "It provides the final moral", "It lists all secondary characters"),
        ("Which statement best distinguishes theme from plot?", "Theme is the underlying message, while plot is the sequence of events", "Theme and plot always mean exactly the same thing", "Plot is the author's name, while theme is the title", "Theme is the setting, while plot is punctuation"),
        ("What is the purpose of a frame narrative?", "To present one story within the structure of another story", "To remove the narrator completely", "To arrange events alphabetically", "To describe only one character"),
        ("Which approach is most effective for writing a psychologically complex antagonist?", "Give the antagonist understandable motives and internal contradictions", "Make the antagonist evil without any motivation", "Avoid showing the antagonist's actions", "Give the antagonist no connection to the conflict"),
        ("What is the effect of an intentionally ambiguous symbol?", "It can support multiple interpretations and enrich the theme", "It always has only one literal meaning", "It removes all possible symbolism", "It replaces the story's setting"),
        ("A writer reveals the protagonist's fear through repeated avoidance of a particular place rather than directly naming the fear. Which technique is used?", "Indirect characterisation", "Direct exposition only", "Chronological summary", "Formal argumentation"),
        ("Which approach is most effective for creating a meaningful resolution?", "Resolve the central conflict in a way that reflects the characters' development", "Introduce a completely unrelated conflict", "End without considering the story's main events", "Change the protagonist's identity without explanation"),
        ("What is the most important consideration when choosing a narrative point of view?", "Which perspective best serves the story's purpose and controls information effectively", "Which perspective uses the fewest words in every case", "Which perspective avoids all character development", "Which perspective eliminates the need for a plot")
    ]
}


def validate_bank():
    for difficulty, questions in BANK.items():
        if len(questions) != 30:
            raise ValueError(
                f"{difficulty} must contain exactly 30 questions. "
                f"Found {len(questions)}."
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
            ("Story Writing", "English")
        )

        row = cur.fetchone()

        if not row:
            raise Exception(
                "Lesson 'Story Writing' with topic 'English' was not found."
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
                    INSERT INTO quizzes (lesson_id, title, difficulty)
                    VALUES (?, ?, ?)
                    """,
                    (
                        lesson_id,
                        f"Story Writing - {difficulty}",
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
                    INSERT INTO questions (
                        quiz_id,
                        question,
                        option_a,
                        option_b,
                        option_c,
                        option_d,
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

            print(
                f"{difficulty}: {final_count}/30 questions ready."
            )

        con.commit()

        print("\nSUCCESS: Story Writing has exactly 90 questions!")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
