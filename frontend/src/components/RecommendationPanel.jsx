function RecommendationPanel() {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 mt-8">

      <div className="flex items-center gap-3 mb-4">
        <span className="text-4xl">🤖</span>

        <div>
          <h2 className="text-2xl font-semibold">
            AI Recommendation
          </h2>

          <p className="text-gray-500">
            Personalized learning recommendation
          </p>
        </div>
      </div>

      <div className="space-y-4">

        <div className="bg-blue-50 rounded-lg p-4">

          <p className="text-gray-600 text-sm">
            Recommended Lesson
          </p>

          <h3 className="text-xl font-bold text-blue-700">
            Loops & Conditional Statements
          </h3>

        </div>

        <div className="grid grid-cols-2 gap-4">

          <div className="bg-gray-100 rounded-lg p-4">

            <p className="text-gray-500">
              Difficulty
            </p>

            <h4 className="text-lg font-bold">
              Intermediate
            </h4>

          </div>

          <div className="bg-gray-100 rounded-lg p-4">

            <p className="text-gray-500">
              Estimated Time
            </p>

            <h4 className="text-lg font-bold">
              25 mins
            </h4>

          </div>

        </div>

        <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold transition">
          Start Recommended Lesson
        </button>

      </div>

    </div>
  );
}

export default RecommendationPanel;