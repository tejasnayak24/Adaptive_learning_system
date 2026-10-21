import { useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { progressService } from '../services/progressService'
import { lessonService } from '../services/lessonService'

export default function Recommendations() {
  const { user } = useAuth()

  const [loading, setLoading] = useState(true)
  const [recommendations, setRecommendations] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadRecommendation() {
      const studentId = user?.id ?? user?.sub

      // Do not request progress if the student ID is unavailable.
      if (studentId == null || studentId === '') {
        setRecommendations([])
        setError('Student ID is unavailable. Please log in again.')
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        setError('')

        const progressRes =
          await progressService.getStudentProgress(studentId)

        const lessonsRes = await lessonService.getLessons()

        // Support API responses that return data directly
        // or wrap it inside a success/data object.
        const progressData =
          progressRes?.data?.data ??
          progressRes?.data ??
          []

        const lessonsData =
          lessonsRes?.data?.data ??
          lessonsRes?.data ??
          []

        const progressList = Array.isArray(progressData)
          ? progressData
          : []

        const lessonsList = Array.isArray(lessonsData)
          ? lessonsData
          : []

        // Create recommendations from lessons the student
        // has not completed yet.
        const completedLessonIds = new Set(
          progressList
            .filter(
              (item) =>
                item.completed === true ||
                item.status === 'completed'
            )
            .map((item) => String(item.lesson_id ?? item.lessonId))
        )

        const pendingLessons = lessonsList.filter(
          (lesson) =>
            !completedLessonIds.has(String(lesson.id))
        )

        setRecommendations(
          pendingLessons.map((lesson) => ({
            id: lesson.id,
            title: lesson.title ?? lesson.name ?? 'Untitled lesson',
            description:
              lesson.description ??
              'Continue learning to improve your progress.',
          }))
        )
      } catch (err) {
        console.error('Failed to load AI Coach recommendations:', err)

        setError(
          err?.response?.data?.detail ||
            'Unable to load recommendations. Please try again.'
        )
        setRecommendations([])
      } finally {
        setLoading(false)
      }
    }

    loadRecommendation()
  }, [user?.id, user?.sub])

  if (loading) {
    return (
      <div className="p-6">
        <p>Loading recommendations...</p>
      </div>
    )
  }

  return (
    <div className="p-6">
      <h1 className="mb-2 text-2xl font-bold">AI Coach</h1>

      <p className="mb-6 text-gray-600">
        Recommended lessons to help you continue learning.
      </p>

      {error && (
        <div className="mb-4 rounded-lg bg-red-100 p-4 text-red-700">
          {error}
        </div>
      )}

      {!error && recommendations.length === 0 && (
        <div className="rounded-lg bg-gray-100 p-4 text-gray-700">
          No new lesson recommendations available right now.
        </div>
      )}

      <div className="grid gap-4">
        {recommendations.map((lesson) => (
          <div
            key={lesson.id}
            className="rounded-lg border p-4 shadow-sm"
          >
            <h2 className="text-lg font-semibold">
              {lesson.title}
            </h2>

            <p className="mt-2 text-gray-600">
              {lesson.description}
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}