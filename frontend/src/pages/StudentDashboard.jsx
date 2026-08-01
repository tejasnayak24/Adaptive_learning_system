import StudentLayout from "../layouts/StudentLayout";

import DashboardCard from "../components/DashboardCard";
import ProgressChart from "../components/ProgressChart";
import RecentQuizTable from "../components/RecentQuizTable";
import RecommendationPanel from "../components/RecommendationPanel";
import LearningStreak from "../components/LearningStreak";

function StudentDashboard() {
  return (
    <StudentLayout>

      {/* Page Header */}

      <div className="mb-8">

        <h1 className="text-4xl font-bold">
          Welcome Back 👋
        </h1>

        <p className="text-gray-600 mt-2">
          Here's an overview of your learning progress today.
        </p>

      </div>

      {/* Top Statistics Cards */}

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">

        <DashboardCard
          title="Current Lesson"
          value="Python Basics"
          description="Continue learning"
        />

        <DashboardCard
          title="Recommended"
          value="Loops"
          description="Suggested by AI"
        />

        <DashboardCard
          title="Quiz Score"
          value="88%"
          description="Latest Quiz"
        />

        <DashboardCard
          title="Attention"
          value="92%"
          description="Current Focus"
        />

      </div>

      {/* Progress Chart + Learning Streak */}

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6 mt-8">

        <div className="xl:col-span-2">
          <ProgressChart />
        </div>

        <LearningStreak />

      </div>

      {/* Quiz Table + AI Recommendation */}

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 mt-8">

        <RecentQuizTable />

        <RecommendationPanel />

      </div>

    </StudentLayout>
  );
}

export default StudentDashboard;