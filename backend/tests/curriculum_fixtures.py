"""Small synthetic curricula that satisfy the content validator (for API tests)."""

FILLER = " ".join(["Learners study this idea carefully and explain it in their own words."] * 22)


def question(text: str, answer: str = "B") -> list:
    return [text, ["first option", "second option", "third option", "fourth option"], answer, "Think about the lesson.", "Because the lesson says so."]


def lesson(slug: str, title: str, *, legacy_title: str | None = None, quiz: bool = True) -> dict:
    data = {
        "slug": slug,
        "title": title,
        "objectives": ["Understand the idea", "Apply the idea"],
        "intro": FILLER,
        "sections": [["Part one", FILLER], ["Part two", "More detail."]],
        "definitions": [["Term", "Meaning"], ["Other term", "Other meaning"]],
        "examples": ["An example."],
        "worked": [{"problem": "Do it", "steps": ["Step 1", "Step 2"], "answer": "Done"}],
        "diagram": {"type": "flow", "title": "Steps", "items": ["One", "Two"]},
        "real_world": "Used in daily life.",
        "takeaways": ["One", "Two", "Three"],
        "practice": [["Q1", "A1"], ["Q2", "A2"], ["Q3", "A3"]],
    }
    if legacy_title:
        data["legacy_title"] = legacy_title
        data["legacy_notes"] = {
            "What is the basic structural and functional unit of life?": ["Think smallest living unit.", "The cell is the basic unit of life."]
        }
    if quiz:
        letters = "ABCD"
        data["quiz"] = {
            level: [question(f"{slug} {level} question {i}", letters[(i + n) % 4]) for i in range(4)]
            for n, level in enumerate(("EASY", "MEDIUM", "HARD"))
        }
    return data


def curriculum_file(grade: int, subject: str, prefix: str, legacy: dict | None = None) -> dict:
    topics = []
    for t in range(3):
        lessons = [lesson(f"{prefix}-t{t}-l{n}", f"{subject} G{grade} T{t} L{n}") for n in range(2)]
        if legacy and t == 0:
            lessons[0] = lesson(f"{prefix}-legacy", legacy["title"], legacy_title=legacy["title"], quiz=False)
        topics.append({"slug": f"{prefix}-t{t}", "title": f"Topic {t}", "description": "About it", "lessons": lessons})
    return {
        "grade": grade,
        "subject": subject,
        "units": [{"slug": f"{prefix}-u0", "title": "Unit", "topics": topics}],
        "_file": f"{prefix}.json",
    }
