import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="w-64 bg-gray-900 text-white min-h-screen p-6 shadow-lg">

      <h2 className="text-3xl font-bold text-center mb-10">
        🎓 Student
      </h2>

      <nav className="flex flex-col gap-3">

        <Link
          to="/dashboard"
          className="px-4 py-3 rounded-lg hover:bg-blue-600 transition"
        >
          🏠 Dashboard
        </Link>

        <Link
          to="/lessons"
          className="px-4 py-3 rounded-lg hover:bg-blue-600 transition"
        >
          📚 Lessons
        </Link>

        <Link
          to="/progress"
          className="px-4 py-3 rounded-lg hover:bg-blue-600 transition"
        >
          📈 Progress
        </Link>

        <Link
          to="/profile"
          className="px-4 py-3 rounded-lg hover:bg-blue-600 transition"
        >
          👤 Profile
        </Link>

      </nav>

    </aside>
  );
}

export default Sidebar;