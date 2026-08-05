function ProgressChart() {
  const progress = [
    { lesson: "Python", value: 100 },
    { lesson: "Loops", value: 80 },
    { lesson: "Functions", value: 60 },
    { lesson: "Lists", value: 40 },
  ];

  return (
    <div className="bg-white rounded-xl shadow-md p-6 mt-8">

      <h2 className="text-2xl font-bold mb-6">
        Course Progress
      </h2>

      <div className="space-y-6">

        {progress.map((item, index) => (

          <div key={index}>

            <div className="flex justify-between mb-2">

              <span>{item.lesson}</span>

              <span>{item.value}%</span>

            </div>

            <div className="w-full bg-gray-200 rounded-full h-4">

              <div
                className="bg-blue-600 h-4 rounded-full"
                style={{ width: `${item.value}%` }}
              ></div>

            </div>

          </div>

        ))}

      </div>

    </div>
  );
}

export default ProgressChart;