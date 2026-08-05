import StudentLayout from "../layouts/StudentLayout";

function Profile() {
  return (
    <StudentLayout>
      <div className="max-w-4xl mx-auto">

        <h1 className="text-4xl font-bold mb-8">
          My Profile
        </h1>

        <div className="bg-white rounded-xl shadow-md p-8">

          <div className="flex items-center gap-6">

            <div className="w-24 h-24 rounded-full bg-blue-600 text-white flex items-center justify-center text-4xl font-bold">
              R
            </div>

            <div>
              <h2 className="text-3xl font-bold">
                Roshwin Dsouza
              </h2>

              <p className="text-gray-600">
                Information Science Student
              </p>

              <p className="text-gray-500">
                roshwindsouza12@gmail.com
              </p>
            </div>

          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-10">

            <div className="bg-blue-50 rounded-lg p-6">
              <h3 className="font-bold text-lg">
                Completed Lessons
              </h3>

              <p className="text-3xl font-bold mt-2">
                18
              </p>
            </div>

            <div className="bg-green-50 rounded-lg p-6">
              <h3 className="font-bold text-lg">
                Quiz Average
              </h3>

              <p className="text-3xl font-bold mt-2">
                88%
              </p>
            </div>

            <div className="bg-yellow-50 rounded-lg p-6">
              <h3 className="font-bold text-lg">
                Learning Streak
              </h3>

              <p className="text-3xl font-bold mt-2">
                🔥 7 Days
              </p>
            </div>

            <div className="bg-purple-50 rounded-lg p-6">
              <h3 className="font-bold text-lg">
                AI Attention Score
              </h3>

              <p className="text-3xl font-bold mt-2">
                92%
              </p>
            </div>

          </div>

          <button className="mt-10 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg">
            Edit Profile
          </button>

        </div>

      </div>
    </StudentLayout>
  );
}

export default Profile;