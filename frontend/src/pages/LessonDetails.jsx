import { Link, useParams } from "react-router-dom";
import StudentLayout from "../layouts/StudentLayout";
import { useEffect, useState } from "react";
import lessonService from "../services/lessonService";

function LessonDetails() {
  const { id } = useParams();
  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;
    const load = async () => {
      setLoading(true);
      try {
        const res = await lessonService.getLessonById(id);
        const data = res?.data ?? res;
        if (mounted) setLesson(data);
      } catch (e) {
        if (mounted) setError(e.message || "Failed to load lesson");
      } finally {
        if (mounted) setLoading(false);
      }
    };
    load();
    return () => (mounted = false);
  }, [id]);

  if (loading) {
    return (
      <StudentLayout>
        <div className="bg-white rounded-xl shadow-md p-8 text-center">Loading lesson...</div>
      </StudentLayout>
    );
  }

  if (error || !lesson) {
    return (
      <StudentLayout>
        <div className="bg-white rounded-xl shadow-md p-8 text-center">
          <h1 className="text-3xl font-bold text-red-600">Lesson Not Found</h1>
          <Link to="/lessons" className="text-blue-600 hover:underline mt-4 inline-block">← Back to Lessons</Link>
        </div>
      </StudentLayout>
    );
  }

  const objectives = lesson.objectives ?? lesson?.meta?.objectives ?? [];
  const duration = lesson.duration ?? lesson?.meta?.duration ?? "-";
  const difficulty = lesson.difficulty ?? lesson?.meta?.difficulty ?? "-";

  return (
    <StudentLayout>
      <Link to="/lessons" className="text-blue-600 hover:underline">← Back to Lessons</Link>

      <div className="bg-white rounded-xl shadow-md p-8 mt-6">
        <h1 className="text-4xl font-bold">{lesson.title ?? lesson.name}</h1>

        <div className="flex gap-4 mt-4">
          <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full">{difficulty}</span>
          <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full">{duration}</span>
        </div>

        <h2 className="text-2xl font-semibold mt-8">Learning Objectives</h2>
        <ul className="list-disc ml-6 mt-4 space-y-2">
          {objectives.map((objective, index) => (<li key={index}>{objective}</li>))}
        </ul>

        <h2 className="text-2xl font-semibold mt-8">Lesson Content</h2>
        <div className="bg-gray-50 rounded-lg p-6 mt-4 leading-8">
          <div dangerouslySetInnerHTML={{ __html: lesson.content ?? lesson.body ?? lesson.description ?? "" }} />
        </div>

        <Link to={`/quiz/${lesson.quiz_id ?? lesson.id ?? id}`} className="inline-block mt-8 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg">Start Quiz</Link>
      </div>
    </StudentLayout>
  );
}

export default LessonDetails;