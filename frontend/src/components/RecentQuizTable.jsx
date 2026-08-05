function RecentQuizTable() {
  const quizzes = [
    {
      lesson: "Python Basics",
      score: "90%",
      date: "05 Aug 2026",
    },
    {
      lesson: "Loops",
      score: "85%",
      date: "04 Aug 2026",
    },
    {
      lesson: "Functions",
      score: "80%",
      date: "03 Aug 2026",
    },
  ];

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mt-8">

      <h2 className="text-2xl font-bold mb-6">
        Recent Quiz Results
      </h2>

      <table className="w-full">

        <thead>
          <tr className="border-b">
            <th className="text-left py-3">Lesson</th>
            <th className="text-left py-3">Score</th>
            <th className="text-left py-3">Date</th>
          </tr>
        </thead>

        <tbody>

          {quizzes.map((quiz, index) => (

            <tr key={index} className="border-b">

              <td className="py-4">{quiz.lesson}</td>

              <td className="py-4 font-semibold text-blue-600">
                {quiz.score}
              </td>

              <td className="py-4">{quiz.date}</td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}

export default RecentQuizTable;