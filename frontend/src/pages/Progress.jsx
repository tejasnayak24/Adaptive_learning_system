import StudentLayout from "../layouts/StudentLayout";
import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import progressService from "../services/progressService";

function Progress() {
  const { user } = useAuth();
  const [progress, setProgress] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;
    const load = async () => {
      setLoading(true);
      try {
        if (!user) {
          if (mounted) setProgress([]);
          return;
        }
        const res = await progressService.getStudentProgress(user.id);
        const data = res?.data ?? res;
        if (mounted) setProgress(Array.isArray(data) ? data : data?.items ?? []);
      } catch (e) {
        if (mounted) setError(e.message || "Failed to load progress");
      } finally {
        if (mounted) setLoading(false);
      }
    };
    load();
    return () => (mounted = false);
  }, [user]);

  const lessonsCompleted = progress.filter((p) => p.completed).length;
  const quizAvg = progress.length > 0 ? Math.round((progress.reduce((s, p) => s + (p.quiz_score ?? 0), 0) / progress.length)) : 0;

  return (
    <StudentLayout>
      <h1 className="text-4xl font-bold mb-8">Learning Progress</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-lg font-semibold">Lessons Completed</h2>
          <p className="text-4xl font-bold text-blue-600 mt-4">{lessonsCompleted}</p>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-lg font-semibold">Quiz Average</h2>
          <p className="text-4xl font-bold text-green-600 mt-4">{quizAvg}%</p>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-lg font-semibold">Learning Streak</h2>
          <p className="text-4xl font-bold text-orange-500 mt-4">{/* Streak not provided by backend */}🔥 {progress?.streak ?? 0} Days</p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-md p-8 mt-8">
        <h2 className="text-2xl font-bold mb-4">Weekly Activity</h2>

        <div className="space-y-4">
          {loading && <div>Loading...</div>}
          {!loading && progress.length === 0 && <div>No progress data yet.</div>}

          {progress.map((p) => (
            <div key={p.lesson_id ?? p.id}>
              <div className="flex justify-between">
                <span>{p.lesson_title ?? p.lesson_name ?? `Lesson ${p.lesson_id ?? p.id}`}</span>
                <span>{Math.round(p.quiz_score ?? 0)}%</span>
              </div>

              <div className="w-full bg-gray-200 rounded-full h-3 mt-2">
                <div className="bg-blue-600 h-3 rounded-full" style={{ width: `${Math.min(100, Math.round(p.quiz_score ?? 0))}%` }}></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </StudentLayout>
  );
}

export default Progress;