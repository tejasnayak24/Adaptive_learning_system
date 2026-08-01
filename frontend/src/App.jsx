import Lessons from "./pages/Lessons";
import { Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import StudentDashboard from "./pages/StudentDashboard";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dashboard" element={<StudentDashboard />} />
      <Route path="/lessons" element={<Lessons />} />
    </Routes>
  );
}

export default App;