import { useState } from "react";
import StudentLayout from "../layouts/StudentLayout";
import LessonCard from "../components/LessonCard";

function Lessons() {

  const lessons = [
    {
      title: "Python Basics",
      difficulty: "Beginner",
      duration: "30 mins",
      description: "Learn variables, data types, input/output and basic syntax.",
    },
    {
      title: "Loops",
      difficulty: "Intermediate",
      duration: "25 mins",
      description: "Understand for loops, while loops and nested loops.",
    },
    {
      title: "Functions",
      difficulty: "Intermediate",
      duration: "35 mins",
      description: "Create reusable functions and understand parameters.",
    },
    {
      title: "Lists",
      difficulty: "Intermediate",
      duration: "30 mins",
      description: "Learn list operations, indexing and slicing.",
    },
    {
      title: "Dictionaries",
      difficulty: "Advanced",
      duration: "40 mins",
      description: "Master key-value pairs and dictionary methods.",
    },
    {
      title: "File Handling",
      difficulty: "Advanced",
      duration: "45 mins",
      description: "Read and write files using Python.",
    },
  ];

  const [search, setSearch] = useState("");

  const filteredLessons = lessons.filter((lesson) =>
    lesson.title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <StudentLayout>

      <div className="mb-8">

        <h1 className="text-4xl font-bold">
          Lessons
        </h1>

        <p className="text-gray-600 mt-2">
          Explore lessons and continue your learning journey.
        </p>

      </div>

      {/* Search Box */}

      <div className="mb-8">

        <input
          type="text"
          placeholder="🔍 Search lessons..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full md:w-96 border border-gray-300 rounded-lg p-3 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

      </div>

      {/* Lesson Cards */}

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">

        {filteredLessons.map((lesson, index) => (

          <LessonCard
            key={index}
            title={lesson.title}
            difficulty={lesson.difficulty}
            duration={lesson.duration}
            description={lesson.description}
          />

        ))}

      </div>

    </StudentLayout>
  );
}

export default Lessons;