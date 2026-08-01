import { Link } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="w-64 bg-gray-900 text-white min-h-screen p-5">

      <h2 className="text-2xl font-bold mb-8">
        Student
      </h2>

      <nav className="flex flex-col gap-4">

        <Link to="/dashboard" className="hover:text-blue-400">
          Dashboard
        </Link>

        <Link to="/lessons" className="hover:text-blue-400">
          Lessons
        </Link>

        <Link to="/quiz" className="hover:text-blue-400">
          Quiz
        </Link>

        <Link to="/progress" className="hover:text-blue-400">
          Progress
        </Link>

        <Link to="/profile" className="hover:text-blue-400">
          Profile
        </Link>

      </nav>

    </aside>
  );
}

export default Sidebar;