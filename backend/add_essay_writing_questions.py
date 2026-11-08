
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

# Format: (question, correct answer, wrong1, wrong2, wrong3)

BANK = {
    "Easy": [
        ("What is an essay?", "A piece of writing on a particular topic", "A collection of random numbers", "A mathematical formula", "A list of addresses"),
        ("What is the beginning of an essay called?", "Introduction", "Conclusion", "Bibliography", "Appendix"),
        ("What is the main purpose of an introduction?", "To introduce the topic and engage the reader", "To list all references", "To repeat the conclusion", "To introduce unrelated topics"),
        ("What is the main body of an essay used for?", "To develop and explain the main ideas", "To provide only the author's name", "To list page numbers", "To repeat the title"),
        ("What is the purpose of an essay conclusion?", "To summarise the main points and provide closure", "To introduce an unrelated topic", "To list all the characters", "To begin a new essay"),
        ("What is a thesis statement?", "A sentence expressing the central argument or idea", "The author's postal address", "The final reference in an essay", "The essay's page number"),
        ("Which part of an essay usually contains the thesis statement?", "Introduction", "Bibliography", "Appendix", "Footer"),
        ("What is a descriptive essay?", "An essay that describes a person, place or experience", "An essay that contains only mathematical calculations", "A list of instructions", "A formal application"),
        ("What is a narrative essay?", "An essay that tells a story or describes an experience", "An essay containing only definitions", "A list of unrelated facts", "A scientific formula"),
        ("What is an argumentative essay?", "An essay that presents and supports a position", "An essay that lists random words", "An essay without a central idea", "An essay containing only descriptions"),
        ("What is an expository essay?", "An essay that explains or informs about a topic", "An essay that tells only fictional stories", "An essay containing personal greetings", "An essay without supporting details"),
        ("Which tone is generally suitable for academic essays?", "Formal and clear", "Rude and aggressive", "Slang-filled and casual", "Careless and humorous"),
        ("What is a paragraph in an essay?", "A group of related sentences developing one idea", "A single punctuation mark", "A list of page numbers", "An unrelated collection of words"),
        ("What are supporting details?", "Facts, examples and explanations that develop an idea", "The essay's title only", "The author's signature", "Unrelated sentences"),
        ("What is plagiarism?", "Using someone else's work without proper acknowledgement", "Writing an original essay", "Correcting grammatical errors", "Organising paragraphs"),
        ("Why should an essay have a clear title?", "To indicate its subject or main focus", "To replace the introduction", "To provide the conclusion", "To list the references"),
        ("What is proofreading?", "Checking writing for spelling, grammar and punctuation errors", "Adding unrelated paragraphs", "Changing the topic", "Removing all supporting evidence"),
        ("Which word is suitable for introducing an additional point?", "Furthermore", "However", "Although", "Nevertheless"),
        ("Which transition word indicates a conclusion?", "Therefore", "Meanwhile", "Although", "Instead"),
        ("What is brainstorming?", "Generating ideas before writing", "Checking spelling after writing", "Printing the final essay", "Removing the title"),
        ("What is an outline?", "A plan showing the organisation of essay ideas", "A list of grammatical mistakes", "The final paragraph", "A collection of quotations"),
        ("Which of these is an appropriate essay topic?", "The Importance of Education", "A Comma", "A Single Letter", "A Random Number"),
        ("What is coherence in essay writing?", "Logical connection and smooth flow of ideas", "Using unrelated sentences", "Repeating every paragraph", "Avoiding transitions"),
        ("What is unity in an essay paragraph?", "All sentences contribute to one central idea", "Every sentence discusses a different topic", "All sentences must have identical length", "The paragraph contains only one word"),
        ("Which source is generally suitable for academic research?", "A reliable scholarly publication", "An anonymous unsupported social media post", "An invented quotation", "An unrelated advertisement"),
        ("What should be avoided in an essay?", "Unnecessary repetition and irrelevant information", "Clear explanations", "Relevant examples", "Logical organisation"),
        ("What is a persuasive essay intended to do?", "Convince readers to accept a viewpoint", "Describe a place only", "List unrelated events", "Provide only definitions"),
        ("What is a comparative essay?", "An essay examining similarities and differences", "An essay containing only a personal story", "A list of unrelated instructions", "An essay without a topic"),
        ("Why is editing important?", "It improves clarity, structure and overall quality", "It removes the need for an introduction", "It guarantees a longer essay", "It changes every fact"),
        ("What should a strong essay contain?", "A clear introduction, organised body and conclusion", "Only a title and random sentences", "Only quotations", "Unrelated paragraphs")
    ],

    "Medium": [
        ("Which sequence represents the usual structure of an essay?", "Introduction, body paragraphs and conclusion", "Conclusion, bibliography and introduction", "Title, references and conclusion only", "Body, title and appendix only"),
        ("Which thesis statement is the strongest for an essay about online education?", "Online education improves access to learning but requires reliable technology and student engagement.", "Online education is a topic.", "Education is important to everyone.", "Many people use computers."),
        ("What is the main purpose of a topic sentence in a body paragraph?", "To introduce the paragraph's central idea", "To provide the author's biography", "To list all references", "To introduce the final conclusion"),
        ("Which technique makes an argumentative essay more convincing?", "Supporting claims with relevant evidence and logical reasoning", "Using unsupported opinions", "Repeating the thesis without explanation", "Ignoring opposing viewpoints"),
        ("What is a counterargument?", "An opposing viewpoint to the writer's argument", "The essay's title", "The final reference", "A sentence introducing a description"),
        ("What is a rebuttal?", "A response that challenges or answers a counterargument", "A list of unrelated examples", "A summary of the introduction only", "A type of essay heading"),
        ("Which approach is best for writing a compare-and-contrast essay?", "Use consistent criteria to examine similarities and differences", "Discuss only one subject", "List unrelated facts", "Avoid mentioning similarities"),
        ("Which transition phrase indicates contrast?", "On the other hand", "In addition", "For example", "As a result"),
        ("Which transition phrase introduces an example?", "For instance", "Nevertheless", "Consequently", "In contrast"),
        ("What is the purpose of a hook in an essay introduction?", "To capture the reader's attention", "To provide the final conclusion", "To list all references", "To replace the thesis statement"),
        ("Which is an example of an effective hook?", "Imagine a world where every child has access to quality education.", "This essay has five paragraphs.", "The conclusion is given below.", "The bibliography contains several books."),
        ("What is a cause-and-effect essay?", "An essay explaining reasons and their consequences", "An essay describing only physical appearance", "An essay listing unrelated events", "An essay comparing two characters only"),
        ("What is a chronological essay organisation?", "Presenting events in the order they occurred", "Presenting information alphabetically", "Grouping ideas by colour", "Listing arguments randomly"),
        ("Which method is suitable for developing an expository essay?", "Explain the topic using facts, examples and clear definitions", "Use only emotional appeals", "Avoid explaining key concepts", "Include unsupported claims"),
        ("What is the purpose of citations in academic writing?", "To acknowledge sources and support claims", "To decorate the essay", "To increase paragraph length", "To replace the thesis statement"),
        ("Which sentence demonstrates formal academic language?", "The findings indicate a significant relationship between the variables.", "The results are super cool.", "This thing is totally awesome.", "You know, the data is kind of crazy."),
        ("What is paraphrasing?", "Restating information in one's own words while preserving its meaning", "Copying a passage without acknowledgement", "Deleting the original author's name", "Repeating a sentence word for word"),
        ("What is summarising?", "Presenting the main ideas briefly", "Repeating every sentence in full", "Adding unrelated opinions", "Changing the original topic"),
        ("Which is the most effective way to organise body paragraphs?", "Arrange ideas in a logical sequence with supporting evidence", "Place ideas randomly", "Repeat the same argument in every paragraph", "Avoid topic sentences"),
        ("What is a reflective essay?", "An essay examining personal experiences and learning", "An essay containing only scientific equations", "A list of formal instructions", "An essay without personal interpretation"),
        ("Which statement best describes a persuasive thesis?", "It presents a clear position that can be supported with reasons.", "It asks an unrelated question.", "It lists several unrelated topics.", "It avoids expressing any position."),
        ("What is the purpose of a transition sentence between paragraphs?", "To connect ideas and maintain the flow of discussion", "To introduce an unrelated subject", "To repeat the title", "To replace the conclusion"),
        ("Which approach helps avoid plagiarism?", "Cite borrowed ideas and use quotation marks for direct quotations", "Copy paragraphs without acknowledgement", "Change a few words without citing the source", "Remove the bibliography"),
        ("What is the main purpose of an analytical essay?", "To examine and interpret a topic using reasoning and evidence", "To narrate a fictional story only", "To list personal greetings", "To describe a holiday without analysis"),
        ("Which element improves the credibility of an argumentative essay?", "Reliable evidence from trustworthy sources", "Unsupported assumptions", "Personal attacks", "Unverified statistics"),
        ("What is a bibliography?", "A list of sources consulted or cited", "A list of essay titles", "The first body paragraph", "A collection of unrelated quotations"),
        ("Which revision improves conciseness?", "Removing unnecessary words while preserving meaning", "Adding repeated explanations", "Using unnecessarily complicated expressions", "Repeating the thesis in every sentence"),
        ("What is the difference between editing and proofreading?", "Editing improves content and organisation, while proofreading checks surface errors", "Editing checks spelling only, while proofreading changes the argument", "Both involve only changing font size", "There is no difference"),
        ("Which sentence is an appropriate conclusion for an essay on environmental protection?", "Ultimately, protecting the environment requires consistent action from individuals, communities and governments.", "My school has many classrooms.", "The weather was pleasant yesterday.", "There are different types of vehicles."),
        ("Why should an essay maintain a consistent point of view?", "To ensure clarity and avoid confusing the reader", "To make the essay longer", "To eliminate supporting details", "To avoid using paragraphs")
    ],

    "Hard": [
        ("Which thesis statement provides the most focused argument about artificial intelligence in education?", "AI can personalise instruction and improve feedback, but its use requires safeguards for privacy and academic integrity.", "Artificial intelligence is a popular technology.", "Education has existed for centuries.", "Computers are used in schools."),
        ("An essay presents a strong claim but provides evidence unrelated to that claim. What is the main weakness?", "Lack of logical support for the argument", "Excessive paragraph unity", "Correct use of citations", "Effective development of the thesis"),
        ("Which approach best strengthens an academic argument?", "Combine credible evidence, logical analysis and consideration of alternative views", "Use emotional statements without evidence", "Repeat the claim in every paragraph", "Ignore contradictory information"),
        ("What is a synthesis essay?", "An essay that combines ideas from multiple sources to develop a coherent argument", "An essay that copies one source completely", "An essay containing only personal memories", "A list of unrelated quotations"),
        ("What is the purpose of a literature review within an academic essay?", "To examine and connect existing research relevant to the topic", "To provide fictional information", "To replace the research question", "To list unrelated books"),
        ("Which approach is best when sources present conflicting findings?", "Compare their methods, evidence and limitations before drawing a conclusion", "Select one finding without examination", "Ignore all conflicting sources", "Combine the findings without explanation"),
        ("What is a logical fallacy?", "An error in reasoning that weakens an argument", "A reliable research method", "A properly supported conclusion", "A correct citation format"),
        ("Which statement demonstrates a hasty generalisation?", "Two students disliked the course, so every student must dislike it.", "Some students reported difficulties with the course.", "The survey included 200 participants.", "The findings require further investigation."),
        ("What is the purpose of a qualification in an academic argument?", "To limit a claim so that it accurately reflects the available evidence", "To make every claim absolute", "To remove all supporting evidence", "To introduce an unrelated topic"),
        ("Which conclusion best suits an analytical essay?", "It interprets the findings and explains how they support the central argument.", "It introduces several unrelated claims.", "It repeats every paragraph word for word.", "It presents new evidence without explanation."),
        ("What is the difference between primary and secondary sources?", "Primary sources provide original material, while secondary sources interpret or analyse it.", "Primary sources are always unreliable, while secondary sources are always correct.", "Both terms refer only to textbooks.", "Secondary sources contain no analysis."),
        ("Which method best improves the flow of a complex essay?", "Use logical sequencing, clear topic sentences and effective transitions", "Change the central argument in every paragraph", "Remove all linking expressions", "Repeat the introduction after each paragraph"),
        ("What is a rhetorical question in essay writing?", "A question asked to emphasise a point rather than obtain an answer", "A question that must always be answered with statistics", "A question used only in references", "A question that replaces the thesis statement"),
        ("Which approach is most appropriate when integrating a direct quotation?", "Introduce it, cite its source and explain its relevance to the argument", "Insert it without context or citation", "Use it as a substitute for the entire essay", "Change its wording while retaining quotation marks"),
        ("What is an abstract in academic writing?", "A brief overview of the purpose, methods, findings and conclusions of a study", "A list of all grammatical rules", "A detailed bibliography", "The final paragraph of every essay"),
        ("Which statement best describes critical analysis?", "Evaluating ideas, evidence, assumptions and implications", "Repeating information without interpretation", "Accepting every source without examination", "Listing facts without explaining their importance"),
        ("What is the main purpose of a research question?", "To define the specific issue the investigation aims to address", "To provide the final answer before research", "To replace all research methods", "To list the author's qualifications"),
        ("Which approach best avoids confirmation bias in an argumentative essay?", "Consider evidence that supports and challenges the central position", "Use only sources that agree with the writer", "Ignore alternative explanations", "Reject contradictory findings automatically"),
        ("What is an annotated bibliography?", "A source list accompanied by brief descriptions or evaluations", "A list of essay titles without references", "A collection of direct quotations only", "A summary of the conclusion"),
        ("Which sentence best demonstrates cautious academic language?", "The findings suggest that the intervention may improve student engagement.", "The intervention definitely works for everyone.", "This research proves every possible outcome.", "There can never be any exceptions."),
        ("What is the role of methodology in a research-based essay?", "To explain how information or evidence was collected and analysed", "To provide only the author's personal opinions", "To replace the research findings", "To list unrelated references"),
        ("Which approach is best when evidence is insufficient to support a broad thesis?", "Narrow the thesis or qualify the claim to match the evidence", "Make the claim more absolute", "Invent additional evidence", "Ignore the limitations"),
        ("What is a counterclaim in an argumentative essay?", "An opposing claim that challenges the writer's position", "The writer's final signature", "A list of references", "A descriptive opening sentence"),
        ("Which technique best integrates multiple sources?", "Compare their findings and explain how they collectively support the argument", "Place quotations next to each other without discussion", "Copy the same information repeatedly", "Ignore differences between sources"),
        ("What is the purpose of an essay's scope?", "To define the boundaries of the subject being discussed", "To determine the font size", "To list every possible topic", "To replace the introduction"),
        ("Which approach produces a more balanced argumentative essay?", "Acknowledge reasonable opposing views and respond with evidence", "Dismiss all opposing views without explanation", "Use personal attacks against opponents", "Avoid presenting supporting evidence"),
        ("What is the main risk of using outdated sources in a rapidly changing research area?", "The information may no longer accurately represent current knowledge", "The sources automatically become primary sources", "The essay no longer needs citations", "The thesis statement becomes unnecessary"),
        ("Which revision best improves an essay containing repeated arguments?", "Combine overlapping points and develop distinct supporting ideas", "Repeat each argument in more paragraphs", "Remove the thesis statement", "Add unrelated quotations"),
        ("What is the purpose of a limitations section in academic writing?", "To explain constraints that may affect the interpretation or generalisation of findings", "To claim that the research has no weaknesses", "To introduce an unrelated topic", "To replace the conclusion"),
        ("Which quality is most important in a strong academic essay?", "A clear argument supported by relevant evidence and logical analysis", "A large number of difficult words", "Repeated claims without proof", "A long introduction without a thesis")
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
            ("Essay Writing", "English")
        )

        row = cur.fetchone()

        if not row:
            raise Exception(
                "Lesson 'Essay Writing' with topic 'English' was not found."
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
                        f"Essay Writing - {difficulty}",
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

            print(f"{difficulty}: {final_count}/30 questions ready.")

        con.commit()

        print("\nSUCCESS: Essay Writing has exactly 90 questions!")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
