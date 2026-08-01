function Navbar() {
  return (
    <nav className="bg-blue-700 text-white h-16 flex items-center justify-between px-6 shadow-md">
      <h1 className="text-xl font-bold">
        Adaptive Learning System
      </h1>

      <div className="flex items-center gap-4">
        <span>Welcome, Student</span>

        <button className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded-lg">
          Logout
        </button>
      </div>
    </nav>
  );
}

export default Navbar;