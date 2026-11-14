import React, { Suspense, lazy, useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate, useLocation, useParams } from 'react-router-dom'
import { BookOpen, Lock } from 'lucide-react'
import { AuthProvider } from './context/AuthContext'
import { MonitoringProvider } from './context/MonitoringContext'
import MonitoringGate from './components/MonitoringGate'
import ProtectedRoute from './components/ProtectedRoute'
import { Button, Card, PageSkeleton } from './components/ui'
import { curriculumService } from './services/curriculumService'
import AppLayout from './layouts/AppLayout'

// Pages are loaded on demand, so the sign-in page does not download the
// lesson, quiz or chart code (the charting library is only needed by
// Progress & Analytics).
const Login = lazy(() => import('./pages/Login'))
const Register = lazy(() => import('./pages/Register'))
const Dashboard = lazy(() => import('./pages/Dashboard'))
const Subjects = lazy(() => import('./pages/Subjects'))
const LessonDetail = lazy(() => import('./pages/LessonDetail'))
const QuizView = lazy(() => import('./pages/QuizView'))
const Progress = lazy(() => import('./pages/Progress'))
const Recommendations = lazy(() => import('./pages/Recommendations'))
const SessionActivity = lazy(() => import('./pages/SessionActivity'))

function PageLoading() {
  return (
    <div className="min-h-screen bg-canvas p-6 sm:p-10">
      <PageSkeleton />
    </div>
  )
}

// Learning pages require verified camera monitoring. A lesson the student
// may not open (another grade, or no such lesson) is refused before any
// camera session starts, instead of asking for verification first.
function MonitoredLesson() {
  const { id } = useParams()
  const [access, setAccess] = useState({ id: null, refusal: null })

  useEffect(() => {
    let cancelled = false
    curriculumService
      .getNavigation(id)
      .then(() => !cancelled && setAccess({ id, refusal: null }))
      .catch((err) => {
        if (cancelled) return
        // Only an explicit refusal blocks; other errors fall through to the
        // lesson page, which reports them itself.
        setAccess({ id, refusal: err.status === 403 || err.status === 404 ? err.message : null })
      })
    return () => {
      cancelled = true
    }
  }, [id])

  if (access.id !== id) {
    return <PageSkeleton variant="reading" label="Loading lesson" />
  }
  if (access.refusal) {
    return (
      <Card padding="lg" className="mx-auto max-w-xl space-y-4 text-center" role="alert">
        <span className="mx-auto grid h-12 w-12 place-items-center rounded-2xl bg-warning/[0.12] text-warning ring-1 ring-inset ring-warning/25">
          <Lock size={22} aria-hidden="true" />
        </span>
        <h1 className="font-display text-xl font-semibold text-ink">This lesson is not available to you</h1>
        <p className="text-sm leading-relaxed text-ink-2">{access.refusal}</p>
        <Button to="/subjects" icon={BookOpen}>
          Go to my lessons
        </Button>
      </Card>
    )
  }
  return (
    <MonitoringGate lessonId={Number(id)}>
      <LessonDetail key={id} />
    </MonitoringGate>
  )
}

function MonitoredQuiz() {
  const { id } = useParams()
  // A recommended retry navigates with a new `attempt`, which remounts the
  // quiz for a fresh attempt while the monitoring session stays connected.
  const attempt = useLocation().state?.attempt ?? ''
  return (
    <MonitoringGate>
      <QuizView key={`${id}:${attempt}`} />
    </MonitoringGate>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <MonitoringProvider>
      <BrowserRouter>
        <Suspense fallback={<PageLoading />}>
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
            <Route path="activity" element={<SessionActivity />} />
          </Route>

          {/* Fallback Route */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
        </Suspense>
      </BrowserRouter>
      </MonitoringProvider>
    </AuthProvider>
  )
}
