import { useState } from "react";
import StudentLayout from "../layouts/StudentLayout";
import LessonCard from "../components/LessonCard";

function Lessons() {
  const lessons = [
    {
      id: "python-basics",
      title: "Python Basics",
      difficulty: "Beginner",
      duration: "30 mins",
      description: "Learn variables, data types, input/output and basic syntax.",
    },
    {
      id: "loops",
      title: "Loops",
      difficulty: "Intermediate",
      duration: "25 mins",
      description: "Understand for loops, while loops and nested loops.",
    },
    {
      id: "functions",
      title: "Functions",
      difficulty: "Intermediate",
      duration: "35 mins",
      description: "Create reusable functions and understand parameters.",
    },
    {
      id: "lists",
      title: "Lists",
      difficulty: "Intermediate",
      duration: "30 mins",
      description: "Learn list operations, indexing and slicing.",
    },
    {
      id: "dictionaries",
      title: "Dictionaries",
      difficulty: "Advanced",
      duration: "40 mins",
      description: "Master key-value pairs and dictionary methods.",
    },
    {
      id: "file-handling",
      title: "File Handling",
      difficulty: "Advanced",
      duration: "45 mins",
      description: "Read and write files using Python.",
    },
  ];

  const [search, setSearch] = useState("");
  const [difficulty, setDifficulty] = useState("All");

  const filteredLessons = lessons.filter((lesson) => {
    const matchesSearch = lesson.title
      .toLowerCase()
      .includes(search.toLowerCase());

    const matchesDifficulty =
      difficulty === "All" || lesson.difficulty === difficulty;

    return matchesSearch && matchesDifficulty;
  });

  return (
    <StudentLayout>
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold">Lessons</h1>

        <p className="text-gray-600 mt-2">
          Explore lessons and continue your learning journey.
        </p>
      </div>

      {/* Search + Filter */}
      <div className="flex flex-col md:flex-row gap-4 mb-8">
        <input
          type="text"
          placeholder="🔍 Search lessons..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1 border border-gray-300 rounded-lg p-3 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <select
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
          className="border border-gray-300 rounded-lg p-3 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option>All</option>
          <option>Beginner</option>
          <option>Intermediate</option>
          <option>Advanced</option>
        </select>
      </div>

      {/* Lesson Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {filteredLessons.length > 0 ? (
          filteredLessons.map((lesson) => (
            <LessonCard
              key={lesson.id}
              id={lesson.id}
              title={lesson.title}
              difficulty={lesson.difficulty}
              duration={lesson.duration}
              description={lesson.description}
            />
          ))
        ) : (
          <div className="col-span-full bg-white rounded-xl shadow-md p-8 text-center">
            <h2 className="text-xl font-semibold text-gray-700">
              No lessons found 📚
            </h2>

            <p className="text-gray-500 mt-2">
              Try a different search or difficulty filter.
            </p>
          </div>
        )}
      </div>
    </StudentLayout>
  );
}

export default Lessons;