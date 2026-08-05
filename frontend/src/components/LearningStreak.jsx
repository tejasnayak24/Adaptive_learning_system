function LearningStreak() {
  return (
    <div className="bg-white rounded-xl shadow-md p-6">

      <h2 className="text-2xl font-bold mb-6">
        Learning Streak 🔥
      </h2>

      <div className="flex justify-around text-center">

        <div>
          <h1 className="text-4xl font-bold text-orange-500">
            7
          </h1>

          <p className="text-gray-500">
            Current
          </p>
        </div>

        <div>
          <h1 className="text-4xl font-bold text-blue-600">
            21
          </h1>

          <p className="text-gray-500">
            Best
          </p>
        </div>

        <div>
          <h1 className="text-4xl font-bold text-green-600">
            52
          </h1>

          <p className="text-gray-500">
            Lessons
          </p>
        </div>

      </div>

    </div>
  );
}

export default LearningStreak;