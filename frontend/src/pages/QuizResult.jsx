import { Link, useLocation } from "react-router-dom";
import StudentLayout from "../layouts/StudentLayout";

function QuizResult() {
  const location = useLocation();

  const score = location.state?.score ?? 0;
  const total = location.state?.total ?? 5;

  const percentage = Math.round((score / total) * 100);

  let message = "";
  let color = "";

  if (percentage >= 80) {
    message = "Excellent Work! 🎉";
    color = "text-green-600";
  } else if (percentage >= 60) {
    message = "Good Job! 👍";
    color = "text-blue-600";
  } else {
    message = "Keep Practicing! 💪";
    color = "text-red-600";
  }

  return (
    <StudentLayout>
      <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-md p-8 text-center">

        <h1 className="text-4xl font-bold mb-6">
          Quiz Completed
        </h1>

        <h2 className={`text-3xl font-bold ${color}`}>
          {message}
        </h2>

        <div className="mt-8">

          <p className="text-6xl font-bold text-blue-600">
            {score}/{total}
          </p>

          <p className="text-xl text-gray-600 mt-2">
            {percentage}% Score
          </p>

        </div>

        <div className="w-full bg-gray-200 rounded-full h-4 mt-8">

          <div
            className="bg-blue-600 h-4 rounded-full"
            style={{ width: `${percentage}%` }}
          ></div>

        </div>

        <div className="flex justify-center gap-4 mt-10">

          <Link
            to="/dashboard"
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg"
          >
            Dashboard
          </Link>

          <Link
            to="/lessons"
            className="bg-gray-700 hover:bg-gray-800 text-white px-6 py-3 rounded-lg"
          >
            Lessons
          </Link>

        </div>

      </div>
    </StudentLayout>
  );
}

export default QuizResult;