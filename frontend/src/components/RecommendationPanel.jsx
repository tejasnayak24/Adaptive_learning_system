function RecommendationPanel() {
  const recommendations = [
    {
      title: "Functions",
      reason: "Based on your quiz performance",
    },
    {
      title: "Lists",
      reason: "Continue your learning path",
    },
    {
      title: "File Handling",
      reason: "Recommended after Dictionaries",
    },
  ];

  return (
    <div className="bg-white rounded-xl shadow-md p-6">

      <h2 className="text-2xl font-bold mb-6">
        Recommended Lessons
      </h2>

      <div className="space-y-4">

        {recommendations.map((lesson, index) => (

          <div
            key={index}
            className="border rounded-lg p-4 hover:bg-gray-50 transition"
          >

            <h3 className="font-semibold text-lg">
              {lesson.title}
            </h3>

            <p className="text-gray-500">
              {lesson.reason}
            </p>

          </div>

        ))}

      </div>

    </div>
  );
}

export default RecommendationPanel;