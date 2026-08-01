import { Link } from "react-router-dom";

function LessonCard({
  title,
  difficulty,
  duration,
  description,
}) {
  return (
    <div className="bg-white rounded-xl shadow-md hover:shadow-xl transition duration-300 p-6">

      <div className="flex justify-between items-center">

        <h2 className="text-xl font-bold">
          {title}
        </h2>

        <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm">
          {difficulty}
        </span>

      </div>

      <p className="text-gray-600 mt-4">
        {description}
      </p>

      <div className="flex justify-between items-center mt-6">

        <span className="text-gray-500">
          ⏱ {duration}
        </span>

        <Link
          to="/lesson/python-basics"
          className="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700 transition"
        >
          Start Lesson
        </Link>

      </div>

    </div>
  );
}

export default LessonCard;