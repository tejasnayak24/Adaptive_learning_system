import { Link, useParams } from "react-router-dom";
import StudentLayout from "../layouts/StudentLayout";

function LessonDetails() {
  const { id } = useParams();

  const lessonData = {
    "python-basics": {
      title: "Python Basics",
      difficulty: "Beginner",
      duration: "30 mins",
      objectives: [
        "Understand Python syntax",
        "Learn variables and data types",
        "Use input() and print()",
        "Write simple Python programs",
      ],
      content:
        "Python is a beginner-friendly programming language used in web development, artificial intelligence, data science, automation, and many other fields. In this lesson, you'll learn the basic syntax, variables, data types, input and output, and write your first Python programs.",
    },

    loops: {
      title: "Loops",
      difficulty: "Intermediate",
      duration: "25 mins",
      objectives: [
        "Understand for loops",
        "Understand while loops",
        "Practice nested loops",
      ],
      content:
        "Loops help execute a block of code repeatedly. Python provides 'for' loops and 'while' loops that make programs efficient by reducing repetition.",
    },

    functions: {
      title: "Functions",
      difficulty: "Intermediate",
      duration: "35 mins",
      objectives: [
        "Create functions",
        "Pass parameters",
        "Return values",
      ],
      content:
        "Functions allow you to organize code into reusable blocks. They improve readability and reduce duplicate code by grouping related logic together.",
    },

    lists: {
      title: "Lists",
      difficulty: "Intermediate",
      duration: "30 mins",
      objectives: [
        "Create lists",
        "Access list elements",
        "Perform list operations",
      ],
      content:
        "Lists are ordered collections used to store multiple values. You'll learn indexing, slicing, adding, removing, and updating list elements.",
    },

    dictionaries: {
      title: "Dictionaries",
      difficulty: "Advanced",
      duration: "40 mins",
      objectives: [
        "Understand key-value pairs",
        "Access dictionary values",
        "Update dictionary data",
      ],
      content:
        "Dictionaries store information using key-value pairs. They provide fast data retrieval and are widely used in real-world Python applications.",
    },

    "file-handling": {
      title: "File Handling",
      difficulty: "Advanced",
      duration: "45 mins",
      objectives: [
        "Read text files",
        "Write files",
        "Use file modes",
      ],
      content:
        "File handling allows Python programs to store and retrieve data from files. You'll learn reading, writing, appending, and closing files safely.",
    },
  };

  const lesson = lessonData[id];

  if (!lesson) {
    return (
      <StudentLayout>
        <div className="bg-white rounded-xl shadow-md p-8 text-center">
          <h1 className="text-3xl font-bold text-red-600">
            Lesson Not Found
          </h1>

          <Link
            to="/lessons"
            className="text-blue-600 hover:underline mt-4 inline-block"
          >
            ← Back to Lessons
          </Link>
        </div>
      </StudentLayout>
    );
  }

  return (
    <StudentLayout>

      <Link
        to="/lessons"
        className="text-blue-600 hover:underline"
      >
        ← Back to Lessons
      </Link>

      <div className="bg-white rounded-xl shadow-md p-8 mt-6">

        <h1 className="text-4xl font-bold">
          {lesson.title}
        </h1>

        <div className="flex gap-4 mt-4">

          <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full">
            {lesson.difficulty}
          </span>

          <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full">
            {lesson.duration}
          </span>

        </div>

        <h2 className="text-2xl font-semibold mt-8">
          Learning Objectives
        </h2>

        <ul className="list-disc ml-6 mt-4 space-y-2">
          {lesson.objectives.map((objective, index) => (
            <li key={index}>{objective}</li>
          ))}
        </ul>

        <h2 className="text-2xl font-semibold mt-8">
          Lesson Content
        </h2>

        <div className="bg-gray-50 rounded-lg p-6 mt-4 leading-8">
          <p>{lesson.content}</p>
        </div>

       <Link
  to={`/quiz/${id}`}
  className="inline-block mt-8 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg"
>
  Start Quiz
</Link>
      </div>

    </StudentLayout>
  );
}

export default LessonDetails;