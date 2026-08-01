function LearningStreak() {
  const streak = 12;
  const goal = 15;
  const progress = (streak / goal) * 100;

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mt-8">

      <div className="flex justify-between items-center">

        <div>
          <h2 className="text-2xl font-semibold">
            🔥 Learning Streak
          </h2>

          <p className="text-gray-500">
            Consecutive learning days
          </p>
        </div>

        <div className="text-4xl font-bold text-orange-500">
          {streak}
        </div>

      </div>

      <div className="mt-6">

        <div className="w-full bg-gray-200 rounded-full h-4">

          <div
            className="bg-orange-500 h-4 rounded-full"
            style={{ width: `${progress}%` }}
          ></div>

        </div>

      </div>

      <p className="mt-4 text-gray-600">
        Great job! You're only {goal - streak} days away from your goal.
      </p>

    </div>
  );
}

export default LearningStreak;