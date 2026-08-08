import { useEffect, useState } from "react";
import StudentLayout from "../layouts/StudentLayout";
import LessonCard from "../components/LessonCard";
import lessonService from "../services/lessonService";

function Lessons() {
  const [lessons, setLessons] = useState([]);
  const [search, setSearch] = useState("");
  const [difficulty, setDifficulty] = useState("All");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;
    setLoading(true);
    lessonService
      .getAllLessons()
      .then((data) => mounted && setLessons(data))
      .catch((err) => mounted && setError(err.message || "Failed to load lessons"))
      .finally(() => mounted && setLoading(false));
    return () => (mounted = false);
  }, []);

  const filteredLessons = lessons.filter((lesson) => {
    const matchesSearch = lesson.title?.toLowerCase().includes(search.toLowerCase());
    const matchesDifficulty = difficulty === "All" || lesson.difficulty === difficulty || lesson.difficulty?.toLowerCase() === difficulty.toLowerCase();
    return matchesSearch && matchesDifficulty;
  });

  return (
    <StudentLayout>
      <div className="mb-8">
        <h1 className="text-4xl font-bold">Lessons</h1>
        <p className="text-gray-600 mt-2">Explore lessons and continue your learning journey.</p>
      </div>

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

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {loading ? (
          <div className="col-span-full bg-white rounded-xl shadow-md p-8 text-center">Loading lessons...</div>
        ) : error ? (
          <div className="col-span-full bg-white rounded-xl shadow-md p-8 text-center text-red-600">{error}</div>
        ) : filteredLessons.length > 0 ? (
          filteredLessons.map((lesson) => (
            <LessonCard
              key={lesson.id}
              id={lesson.id}
              title={lesson.title}
              difficulty={lesson.difficulty}
              duration={lesson.duration || lesson.duration_text || ""}
              description={lesson.content || lesson.description || ""}
            />
          ))
        ) : (
          <div className="col-span-full bg-white rounded-xl shadow-md p-8 text-center">
            <h2 className="text-xl font-semibold text-gray-700">No lessons found 📚</h2>
            <p className="text-gray-500 mt-2">Try a different search or difficulty filter.</p>
          </div>
        )}
      </div>
    </StudentLayout>
  );
}

export default Lessons;