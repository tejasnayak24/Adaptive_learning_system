
import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "adaptive_learning.db"

# Format: (question, correct answer, wrong1, wrong2, wrong3)

BANK = {
    "Easy": [
        ("What is a letter?", "A written message sent to someone", "A mathematical formula", "A computer program", "A newspaper advertisement"),
        ("Which part usually appears at the beginning of a formal letter?", "Sender's address", "Signature", "Conclusion", "Postscript"),
        ("What is the purpose of the date in a letter?", "To indicate when the letter was written", "To identify the reader's age", "To show the page number", "To provide the postal code only"),
        ("What is a salutation?", "The greeting used to address the recipient", "The final signature", "The subject of an essay", "The sender's address"),
        ("Which is an appropriate formal salutation?", "Dear Sir or Madam", "Hey buddy", "What's up!", "Hi dude"),
        ("Which closing is suitable for a formal letter when the recipient is addressed as Sir or Madam?", "Yours faithfully", "See ya", "Bye buddy", "Cheers mate"),
        ("Which closing is commonly used in an informal letter?", "With love", "Yours faithfully", "Respectfully submitted", "To whom it may concern"),
        ("What is the main purpose of a formal letter?", "To communicate official or professional matters", "To share jokes with friends only", "To write a fictional story", "To record personal diary entries"),
        ("Which letter is written to a friend?", "Informal letter", "Business complaint letter", "Application letter", "Official notice"),
        ("What is the subject line in a formal letter?", "A brief statement of the letter's purpose", "The sender's signature", "The recipient's phone number", "The final greeting"),
        ("Which tone is generally used in formal letters?", "Polite and professional", "Rude and casual", "Slang-filled", "Careless and humorous"),
        ("Where is the recipient's address generally written in a formal letter?", "Below the date", "After the signature", "Inside the subject line", "At the very end after the postscript"),
        ("What does the body of a letter contain?", "The main message", "Only the sender's name", "Only the date", "Only the closing greeting"),
        ("Which is an appropriate way to begin an informal letter?", "Dear Rahul,", "Respected Sir or Madam,", "To the Manager,", "Dear Hiring Committee,"),
        ("What is the purpose of the complimentary close?", "To end the letter politely", "To introduce the subject", "To provide the recipient's address", "To explain the sender's qualifications"),
        ("Which of the following is a formal letter?", "A job application letter", "A birthday letter to a friend", "A letter to a cousin about holidays", "A personal note to a sibling"),
        ("Which of these is an informal expression?", "How are you doing?", "I am writing to formally request", "Kindly consider my application", "I would appreciate your assistance"),
        ("What should be included in a job application letter?", "Relevant qualifications and interest in the position", "Unrelated personal stories", "Jokes and slang", "Only the sender's favourite hobbies"),
        ("What is the purpose of a complaint letter?", "To report a problem and request a solution", "To invite someone to a party", "To congratulate a friend", "To narrate a holiday experience"),
        ("Which detail should be included in a letter of invitation?", "Date, time and venue", "Only the sender's nickname", "The recipient's examination marks", "An unrelated personal story"),
        ("What is a signature in a letter?", "The sender's name or signed mark", "The subject heading", "The recipient's address", "The date of delivery"),
        ("Which phrase is suitable for requesting information formally?", "I would appreciate it if you could provide further details.", "Tell me everything now!", "What's the deal?", "Give me the stuff."),
        ("Which letter is generally used to apply for leave from school?", "Formal application letter", "Informal invitation", "Personal diary entry", "Friendly postcard"),
        ("What should a letter's subject line be?", "Brief and relevant", "Very long and unrelated", "Written as a complete story", "Filled with slang"),
        ("Which is an appropriate opening for a letter to a principal?", "Respected Sir/Madam,", "Hey Principal!", "What's up, Sir?", "Dear bestie,"),
        ("What is the purpose of an address in a letter?", "To identify where the sender or recipient can be contacted", "To explain the main argument", "To replace the greeting", "To provide the conclusion"),
        ("Which letter is written to express gratitude?", "Thank-you letter", "Complaint letter", "Resignation letter", "Enquiry letter"),
        ("What should a writer avoid in a formal letter?", "Unnecessary slang and informal language", "Clear sentences", "Polite expressions", "Relevant information"),
        ("What is the purpose of an enquiry letter?", "To request information about something", "To announce a personal birthday", "To tell a fictional story", "To resign from a job"),
        ("Which part normally appears at the end of a formal letter?", "Signature and sender's name", "Subject line", "Sender's address", "Date")
    ],

    "Medium": [
        ("Which sequence represents the usual structure of a formal letter?", "Sender's address, date, recipient's address, subject, salutation, body, closing", "Body, signature, date, subject, sender's address", "Closing, subject, body, date, recipient's address", "Recipient's address, signature, body, sender's address, date"),
        ("Which subject line is most appropriate for a formal complaint about a damaged product?", "Complaint Regarding Damaged Product Received", "Hey, My Product Is Bad!", "A Story About My Shopping", "Please Read This Long Message"),
        ("Which sentence is most suitable for a formal request?", "I kindly request you to grant me permission to attend the workshop.", "You have to let me go to the workshop.", "I wanna go, so approve it.", "Let me attend, okay?"),
        ("What is the main difference between formal and informal letters?", "Formal letters follow professional conventions, while informal letters use a personal tone.", "Formal letters never contain a body.", "Informal letters must always contain a subject line.", "Formal letters are always handwritten."),
        ("Which closing is appropriate when writing to a known professional recipient?", "Yours sincerely", "Lots of hugs", "See you soon, buddy", "Catch you later"),
        ("A student writes to the principal requesting permission for a college event. Which tone is most suitable?", "Respectful and formal", "Aggressive and demanding", "Overly casual", "Sarcastic"),
        ("Which sentence best introduces the purpose of a job application letter?", "I am writing to apply for the position of Software Engineer advertised by your organisation.", "I heard you have a job, so here I am.", "I really need money and want this job.", "Let me tell you about my weekend."),
        ("What should be the main focus of a complaint letter?", "A clear description of the issue and the expected resolution", "Unrelated personal experiences", "Emotional insults", "A lengthy description of unrelated events"),
        ("Which detail is especially important in a business enquiry letter?", "Specific information being requested", "The sender's favourite movie", "A friend's birthday", "An unrelated travel experience"),
        ("Which phrase is the most professional way to end a request?", "Thank you for your time and consideration.", "Do it as soon as possible!", "That's all, bye!", "You better reply."),
        ("What is the purpose of a reference line in some formal letters?", "To identify a related file, matter or previous communication", "To provide a personal greeting", "To replace the recipient's name", "To introduce an informal story"),
        ("Which sentence is most appropriate in a letter of apology?", "I sincerely apologise for the inconvenience caused by the delay.", "Whatever happened is not my problem.", "Sorry if you felt bad, anyway.", "Forget it and move on."),
        ("Which information should be highlighted in a resignation letter?", "The intention to resign and the proposed last working day", "Unrelated family events", "The sender's childhood memories", "The recipient's personal hobbies"),
        ("What is the main purpose of a cover letter?", "To introduce an applicant and explain their suitability for a position", "To replace every document in an application", "To describe a holiday", "To request a product refund"),
        ("Which sentence demonstrates a polite complaint?", "I would like to bring to your attention an issue with the service received.", "Your service is terrible and useless.", "You people never do anything right.", "I hate everything about this place."),
        ("Which feature is important in an invitation letter?", "Clear details about the event and how to respond", "A list of unrelated complaints", "Only the sender's academic qualifications", "A detailed explanation of past events"),
        ("What is the purpose of a follow-up letter?", "To refer to an earlier communication and seek an update or response", "To introduce an unrelated subject", "To replace a formal greeting", "To provide fictional information"),
        ("Which is the best way to organise the body of a formal letter?", "State the purpose, provide relevant details and conclude with the request or action", "Begin with unrelated details and omit the purpose", "Repeat the subject line in every paragraph", "Place the conclusion before explaining the issue"),
        ("Which sentence is most suitable for a letter requesting a certificate?", "I request you to kindly issue my transfer certificate at your earliest convenience.", "Give me my certificate immediately.", "I need that paper, okay?", "Why haven't you given me my paper?"),
        ("Which element helps the recipient understand the main purpose quickly?", "A clear subject line", "A lengthy postscript", "An unrelated quotation", "A decorative signature"),
        ("What should be done when writing to an organisation without knowing the recipient's name?", "Use an appropriate general salutation such as Dear Sir or Madam", "Invent a recipient's name", "Use a nickname", "Omit the salutation and body"),
        ("Which sentence is appropriate for requesting a meeting?", "I would be grateful if you could suggest a convenient time for a meeting.", "Meet me whenever you want.", "I am coming to see you, no discussion.", "Let's catch up sometime, dude."),
        ("What is the role of an enclosure notation in a formal letter?", "To indicate that additional documents are attached", "To introduce the recipient", "To show the date of writing", "To replace the complimentary close"),
        ("Which approach improves clarity in a formal letter?", "Use short, direct and well-organised paragraphs", "Use long sentences with multiple unrelated ideas", "Include unnecessary repetition", "Avoid stating the purpose"),
        ("A letter to a company requests details about a course's fees and duration. What type of letter is it?", "Enquiry letter", "Resignation letter", "Condolence letter", "Invitation letter"),
        ("Which phrase is suitable for acknowledging receipt of a document?", "I acknowledge receipt of the documents sent on 5 November.", "I got your stuff, cool.", "Your papers came, whatever.", "I think something arrived."),
        ("Why should a formal letter be proofread before sending?", "To identify errors in grammar, spelling, facts and formatting", "To make the letter longer", "To remove all supporting details", "To change the recipient's identity"),
        ("Which sentence is most appropriate in a letter requesting leave due to illness?", "I am unable to attend classes due to illness and request leave for two days.", "I don't feel like coming, so I won't.", "I am taking a break, no questions.", "School is boring, so I am absent."),
        ("What should a writer do if a formal letter contains several separate issues?", "Organise the issues into clear paragraphs", "Combine everything into one confusing sentence", "Remove all headings and punctuation", "Repeat each issue several times"),
        ("Which detail is important in a letter reporting a defective electronic item?", "Purchase date, product details and description of the defect", "The sender's favourite sport", "The recipient's family history", "Unrelated personal opinions")
    ],

    "Hard": [
        ("Which opening is most effective for a formal letter to a university requesting reconsideration of an admission decision?", "I am writing to respectfully request a review of the admission decision communicated on 10 October.", "I do not like your decision, so change it.", "Why did you reject me? This is unfair.", "I want admission and expect an immediate answer."),
        ("A formal letter contains a clear subject and relevant facts but uses emotional accusations. What is the best revision?", "Replace accusations with objective descriptions and specific evidence", "Add stronger insults", "Remove the facts and retain the accusations", "Change the letter into an informal message"),
        ("Which strategy is most effective when writing a persuasive business letter?", "Present a clear proposal supported by relevant benefits and evidence", "Make exaggerated promises without evidence", "Use threatening language", "Avoid mentioning the recipient's needs"),
        ("Which sentence best balances politeness and firmness in a payment reminder?", "We kindly request settlement of the outstanding invoice by the stated due date.", "Pay immediately or face our anger.", "You are always late with payments.", "Please pay whenever you remember."),
        ("A writer needs to complain about repeated service failures. Which structure is most effective?", "State the history of the issue, provide evidence, explain the impact and request corrective action", "Begin with personal insults and end without a request", "Describe unrelated events and omit dates", "Repeat the same complaint in every paragraph"),
        ("Which closing is most appropriate after a formal request when the recipient is addressed by name?", "Yours sincerely", "Yours faithfully", "Lots of love", "Take care, buddy"),
        ("What is the strongest reason for including a reference number in a formal complaint?", "It helps the organisation locate the relevant transaction or case", "It makes the letter sound emotional", "It replaces the subject line", "It identifies the writer's educational background"),
        ("Which sentence is most suitable for negotiating a revised delivery date?", "Would it be possible to arrange delivery by 20 November instead?", "Your delivery date is unacceptable, change it.", "Deliver whenever you feel like it.", "I do not care when it arrives."),
        ("What is the best approach when declining a business invitation?", "Express appreciation, politely decline and provide a brief reason if appropriate", "Ignore the invitation completely", "Criticise the event", "Give an unrelated excuse with unnecessary details"),
        ("Which feature distinguishes an effective cover letter from a generic application?", "It connects the applicant's specific skills to the employer's requirements", "It repeats the resume without explanation", "It focuses mainly on unrelated personal interests", "It uses the same message for every position without changes"),
        ("A formal letter must communicate an urgent issue without sounding rude. Which technique is best?", "State the urgency clearly and request a reasonable response deadline", "Use capital letters throughout", "Threaten the recipient", "Repeat urgent in every sentence"),
        ("Which information should be prioritised in a letter requesting sponsorship for an event?", "Event objectives, audience, sponsorship benefits and requested support", "The organiser's unrelated hobbies", "A fictional history of the organisation", "Personal opinions without supporting details"),
        ("Which revision best improves the sentence 'I am writing this letter in order to make a request for the purpose of asking for leave'?", "I am writing to request leave.", "I am writing this letter for making a request to ask for leave.", "This letter is about a request that I want to make.", "I wish to write a letter in order to request a leave request."),
        ("What is the most appropriate way to refer to an earlier conversation in a formal letter?", "Further to our discussion on 5 November, I am writing to confirm the agreed arrangements.", "Remember that thing we talked about?", "As I already told you, you know what to do.", "You should know what happened before."),
        ("Which approach is most effective in a letter requesting reconsideration of a rejected application?", "Acknowledge the decision, present relevant new information and make a respectful request for review", "Accuse the organisation of unfairness without evidence", "Demand approval without explanation", "Repeat the original application word for word"),
        ("Why should a business letter avoid vague expressions such as 'soon' or 'some time' when discussing deadlines?", "Specific dates and times reduce ambiguity", "Vague expressions make the letter more formal", "Deadlines are unnecessary in business communication", "They improve the emotional tone"),
        ("Which sentence is best for communicating a confirmed attachment?", "Please find attached the requested quotation for your review.", "I may have attached something.", "There is some file somewhere.", "Look around for the document."),
        ("A letter is addressed to a named person but begins with 'Dear Sir or Madam'. What is the best correction?", "Use the recipient's appropriate name or title in the salutation", "Remove the body of the letter", "Replace the date with the recipient's name", "Use an informal nickname"),
        ("Which approach best handles confidential information in a formal letter?", "Include only necessary details and use an appropriate secure communication channel", "Share all private details with unrelated recipients", "Include confidential information in the subject line unnecessarily", "Copy every available contact"),
        ("What is the main benefit of using a direct approach in a routine business request?", "The purpose is communicated quickly and clearly", "The reader must search for the request", "It hides the main message", "It makes the letter less organised"),
        ("Which sentence demonstrates tact when communicating an unfavourable decision?", "After careful consideration, we are unable to approve the request at this time.", "Your request is bad and has been rejected.", "We do not want to deal with this.", "You should not have applied."),
        ("Which is the most suitable content for a professional recommendation request?", "The purpose of the recommendation, relevant deadline and supporting background information", "A demand for an immediate positive recommendation", "Unrelated personal complaints", "A request to invent qualifications"),
        ("What is the best way to make a formal letter actionable?", "Clearly state the requested action, responsible party and relevant deadline", "Use indirect hints without a request", "Avoid mentioning what should happen next", "Include several unrelated questions"),
        ("Which principle is most important when writing a letter on behalf of an organisation?", "Accuracy, professionalism and consistency with organisational policy", "Personal opinions should replace verified facts", "Informal slang should be used throughout", "The writer should make unsupported commitments"),
        ("Which sentence best communicates a correction to previously supplied information?", "Please note that the correct meeting date is 18 November, not 16 November as stated earlier.", "Forget the previous date; it was wrong.", "I think the date might be different.", "The meeting date is confusing, anyway."),
        ("A complaint letter includes evidence but does not specify the desired remedy. What should be added?", "A clear request for repair, replacement, refund or another appropriate resolution", "More unrelated background information", "A personal attack on the recipient", "An additional greeting"),
        ("Which technique is most effective for maintaining a professional tone in a difficult letter?", "Use neutral language, factual descriptions and respectful requests", "Use sarcasm and personal criticism", "Make unsupported accusations", "Use threatening expressions"),
        ("What should a writer do when a formal letter has multiple recipients with different responsibilities?", "Identify the recipients clearly and explain relevant responsibilities where necessary", "Hide all recipient information", "Use one unclear greeting for everyone", "Address only an unrelated person"),
        ("Which is the best way to close a letter requesting a decision?", "I would appreciate your response by 25 November so that we can proceed with the arrangements.", "Reply whenever you feel like it.", "I am waiting, so do something.", "No need to respond if you are busy."),
        ("Which quality makes a formal letter legally or administratively stronger?", "Accurate dates, verifiable facts and clearly documented requests", "Exaggerated claims and emotional language", "Unclear references and missing dates", "Unverified statements and vague demands")
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
            ("Letter Writing", "English")
        )
        row = cur.fetchone()

        if not row:
            raise Exception("Lesson 'Letter Writing' with topic 'English' was not found.")

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
                    (lesson_id, f"Letter Writing - {difficulty}", difficulty)
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
        print("\nSUCCESS: Letter Writing has exactly 90 questions!")

    except Exception as e:
        con.rollback()
        print("ERROR:", e)

    finally:
        con.close()


if __name__ == "__main__":
    main()
