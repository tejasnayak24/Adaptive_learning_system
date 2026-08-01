const quizData = [
  {
    quiz: "Python Basics",
    score: "90%",
    date: "Today",
    status: "Passed",
  },
  {
    quiz: "Loops",
    score: "82%",
    date: "Yesterday",
    status: "Passed",
  },
  {
    quiz: "Functions",
    score: "68%",
    date: "Monday",
    status: "Needs Practice",
  },
];

function RecentQuizTable() {
  return (
    <div className="bg-white rounded-xl shadow-md p-6 mt-8">

      <h2 className="text-2xl font-semibold mb-6">
        Recent Quiz Attempts
      </h2>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse">

          <thead>
            <tr className="bg-blue-600 text-white">
              <th className="p-3 text-left">Quiz</th>
              <th className="p-3 text-left">Score</th>
              <th className="p-3 text-left">Date</th>
              <th className="p-3 text-left">Status</th>
            </tr>
          </thead>

          <tbody>
            {quizData.map((quiz, index) => (
              <tr
                key={index}
                className="border-b hover:bg-gray-100"
              >
                <td className="p-3">{quiz.quiz}</td>
                <td className="p-3">{quiz.score}</td>
                <td className="p-3">{quiz.date}</td>
                <td className="p-3">
                  {quiz.status === "Passed" ? "✅ Passed" : "⚠ Needs Practice"}
                </td>
              </tr>
            ))}
          </tbody>

        </table>
      </div>

    </div>
  );
}

export default RecentQuizTable;