import StudentLayout from "../layouts/StudentLayout";

function Progress() {
  return (
    <StudentLayout>
      <h1 className="text-4xl font-bold mb-8">
        Learning Progress
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-lg font-semibold">
            Lessons Completed
          </h2>

          <p className="text-4xl font-bold text-blue-600 mt-4">
            18
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-lg font-semibold">
            Quiz Average
          </h2>

          <p className="text-4xl font-bold text-green-600 mt-4">
            88%
          </p>
        </div>

        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-lg font-semibold">
            Learning Streak
          </h2>

          <p className="text-4xl font-bold text-orange-500 mt-4">
            🔥 7 Days
          </p>
        </div>

      </div>

      <div className="bg-white rounded-xl shadow-md p-8 mt-8">

        <h2 className="text-2xl font-bold mb-4">
          Weekly Activity
        </h2>

        <div className="space-y-4">

          <div>
            <div className="flex justify-between">
              <span>Python Basics</span>
              <span>100%</span>
            </div>

            <div className="w-full bg-gray-200 rounded-full h-3 mt-2">
              <div className="bg-blue-600 h-3 rounded-full w-full"></div>
            </div>
          </div>

          <div>
            <div className="flex justify-between">
              <span>Loops</span>
              <span>80%</span>
            </div>

            <div className="w-full bg-gray-200 rounded-full h-3 mt-2">
              <div
                className="bg-green-500 h-3 rounded-full"
                style={{ width: "80%" }}
              ></div>
            </div>
          </div>

          <div>
            <div className="flex justify-between">
              <span>Functions</span>
              <span>60%</span>
            </div>

            <div className="w-full bg-gray-200 rounded-full h-3 mt-2">
              <div
                className="bg-yellow-500 h-3 rounded-full"
                style={{ width: "60%" }}
              ></div>
            </div>
          </div>

        </div>

      </div>
    </StudentLayout>
  );
}

export default Progress;