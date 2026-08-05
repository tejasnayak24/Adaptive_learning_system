function Navbar() {
  return (
    <nav className="bg-blue-700 text-white h-16 flex items-center justify-between px-8 shadow-lg">

      <h1 className="text-2xl font-bold">
        Intelligent Adaptive Learning System
      </h1>

      <div className="flex items-center gap-6">

        <button className="text-2xl">
          🔔
        </button>

        <div className="text-right">

          <p className="font-semibold">
            Welcome Back 👋
          </p>

          <p className="text-sm text-blue-100">
            Happy Learning!
          </p>

        </div>

        <button className="bg-red-500 hover:bg-red-600 px-5 py-2 rounded-lg transition">
          Logout
        </button>

      </div>

    </nav>
  );
}

export default Navbar;