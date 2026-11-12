import React from 'react'
import { BrowserRouter, Routes, Route, Navigate, useParams } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { MonitoringProvider } from './context/MonitoringContext'
import MonitoringGate from './components/MonitoringGate'
import ProtectedRoute from './components/ProtectedRoute'
import AppLayout from './layouts/AppLayout'

// Pages
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Subjects from './pages/Subjects'
import LessonDetail from './pages/LessonDetail'
import QuizView from './pages/QuizView'
import Progress from './pages/Progress'
import Recommendations from './pages/Recommendations'

// Learning pages require verified camera monitoring.
function MonitoredLesson() {
  const { id } = useParams()
  return (
    <MonitoringGate lessonId={Number(id)}>
      <LessonDetail key={id} />
    </MonitoringGate>
  )
}

function MonitoredQuiz() {
  const { id } = useParams()
  return (
    <MonitoringGate>
      <QuizView key={id} />
    </MonitoringGate>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <MonitoringProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Routes */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Protected Application Routes */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <AppLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Dashboard />} />
            <Route path="subjects" element={<Subjects />} />
            <Route path="lesson/:id" element={<MonitoredLesson />} />
            <Route path="quiz/:id" element={<MonitoredQuiz />} />
            <Route path="progress" element={<Progress />} />
            <Route path="recommendations" element={<Recommendations />} />
          </Route>

          {/* Fallback Route */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
      </MonitoringProvider>
    </AuthProvider>
  )
}
