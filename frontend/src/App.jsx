import { Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import StudentDashboard from "./pages/StudentDashboard";
import Lessons from "./pages/Lessons";
import LessonDetails from "./pages/LessonDetails";
import Quiz from "./pages/Quiz";
import QuizResult from "./pages/QuizResult";
import Progress from "./pages/Progress";
import Profile from "./pages/Profile";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dashboard" element={<StudentDashboard />} />
      <Route path="/lessons" element={<Lessons />} />
      <Route path="/lesson/:id" element={<LessonDetails />} />
      <Route path="/quiz/:id" element={<Quiz />} />
      <Route path="/quiz-result" element={<QuizResult />} />
      <Route path="/progress" element={<Progress />} />
      <Route path="/profile" element={<Profile />} />
    </Routes>
  );
}

export default App;