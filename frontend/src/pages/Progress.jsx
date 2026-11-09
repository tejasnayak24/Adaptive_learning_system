import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { progressService } from '../services/progressService'
import { lessonService } from '../services/lessonService'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

export default function Progress() {
  const { user } = useAuth()

  const [loading, setLoading] = useState(true)
  const [progress, setProgress] = useState([])
  const [lessons, setLessons] = useState([])
  const [error, setError] = useState('')

  useEffect(() => {
    let cancelled = false

    async function loadProgressData() {
      const studentId = user?.id ?? user?.sub

      if (studentId == null || studentId === '') {
        setError('Student ID is unavailable. Please log in again.')
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        setError('')

        const [progressRes, lessonsRes] = await Promise.all([
          progressService.getStudentProgress(studentId),
          lessonService.getLessons(),
        ])

        if (cancelled) return

        // Support Axios responses and APIs that return data directly.
        const progressData =
          progressRes?.data?.data ??
          progressRes?.data ??
          progressRes

        const lessonsData =
          lessonsRes?.data?.data ??
          lessonsRes?.data ??
          lessonsRes

        // Accept arrays or common API response structures.
        const normalizedProgress = Array.isArray(progressData)
          ? progressData
          : Array.isArray(progressData?.items)
            ? progressData.items
            : Array.isArray(progressData?.progress)
              ? progressData.progress
              : []

        const normalizedLessons = Array.isArray(lessonsData)
          ? lessonsData
          : Array.isArray(lessonsData?.items)
            ? lessonsData.items
            : Array.isArray(lessonsData?.lessons)
              ? lessonsData.lessons
              : []

        setProgress(normalizedProgress)
        setLessons(normalizedLessons)

        console.log('Progress API data:', normalizedProgress)
        console.log('Lessons API data:', normalizedLessons)
      } catch (err) {
        if (cancelled) return

        console.error('Failed to load progress data:', err)

        setError(
          err?.response?.data?.detail ||
            err?.message ||
            'Failed to load progress analytics.'
        )

        setProgress([])
        setLessons([])
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    loadProgressData()

    return () => {
      cancelled = true
    }
  }, [user?.id, user?.sub])

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-10 w-1/4 bg-slate-800 rounded-xl" />
        <div className="h-4 w-1/2 bg-slate-800 rounded-lg" />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pt-6">
          <div className="h-80 bg-slate-800 rounded-3xl" />
          <div className="h-80 bg-slate-800 rounded-3xl" />
        </div>
      </div>
    )
  }

  // Convert numeric values safely.
  const toNumber = (value) => {
    if (value === null || value === undefined || value === '') {
      return null
    }

    const number = Number(value)
    return Number.isFinite(number) ? number : null
  }

  // Supports common field names without assuming the backend schema.
  const getLessonId = (item) =>
    item?.lesson_id ?? item?.lessonId ?? item?.lesson?.id

  const getQuizScore = (item) =>
    toNumber(item?.quiz_score ?? item?.score ?? item?.accuracy)

  const getAttentionScore = (item) =>
    toNumber(item?.attention_score ?? item?.attentionScore)

  const getLessonTitle = (lesson) =>
    lesson?.title ?? lesson?.name ?? 'Untitled Lesson'

  const getDifficulty = (item) =>
    String(item?.difficulty ?? 'MEDIUM').toUpperCase()

  // Calculate curriculum completion using distinct completed lessons.
  const completedDistinct = new Set(
    progress
      .filter((item) => item?.completed === true)
      .map(getLessonId)
      .filter((id) => id !== null && id !== undefined)
      .map(String)
  )

  const totalLessons = lessons.length

  const completionPercentage =
    totalLessons > 0
      ? Math.min(
          100,
          Math.round((completedDistinct.size / totalLessons) * 100)
        )
      : 0

  // Number of recorded assessment attempts.
  const totalAttempts = progress.length

  // Average only scores that actually exist.
  const scores = progress
    .map(getQuizScore)
    .filter((score) => score !== null)

  const avgScore =
    scores.length > 0
      ? Math.round(
          scores.reduce((total, score) => total + score, 0) /
            scores.length
        )
      : 0

  // Do not treat missing attention readings as measured zero values.
  // This page expects attention scores to be normalized between 0 and 1.
  const attentionScores = progress
    .map(getAttentionScore)
    .filter((score) => score !== null && score >= 0 && score <= 1)

  const avgAttention =
    attentionScores.length > 0
      ? Math.round(
          (attentionScores.reduce(
            (total, score) => total + score,
            0
          ) /
            attentionScores.length) *
            100
        )
      : null

  // Sort attempts by ID when available.
  const sortedProgress = [...progress].sort(
    (a, b) => (toNumber(a?.id) ?? 0) - (toNumber(b?.id) ?? 0)
  )

  const lineChartData = sortedProgress.map((item, index) => {
    const score = getQuizScore(item)
    const attention = getAttentionScore(item)

    return {
      attempt: `Quiz ${index + 1}`,
      score,
      attention:
        attention !== null && attention >= 0 && attention <= 1
          ? Math.round(attention * 100)
          : null,
    }
  })

  // Group recorded scores by lesson.
  const topicAggregate = lessons.map((lesson) => {
    const attempts = progress.filter(
      (item) => String(getLessonId(item)) === String(lesson.id)
    )

    const lessonScores = attempts
      .map(getQuizScore)
      .filter((score) => score !== null)

    const lessonAttention = attempts
      .map(getAttentionScore)
      .filter(
        (score) =>
          score !== null && score >= 0 && score <= 1
      )

    const highestScore =
      lessonScores.length > 0
        ? Math.max(...lessonScores)
        : null

    const averageAttention =
      lessonAttention.length > 0
        ? Math.round(
            (lessonAttention.reduce(
              (total, score) => total + score,
              0
            ) /
              lessonAttention.length) *
              100
          )
        : null

    return {
      name: getLessonTitle(lesson),
      score: highestScore,
      attention: averageAttention,
    }
  })

  const tooltipStyle = {
    background: '#0f172a',
    borderColor: '#334155',
    borderRadius: '12px',
    color: '#f8fafc',
  }

  return (
    <div className="space-y-8">
      {/* Page heading */}
      <div className="space-y-1.5">
        <h1 className="font-display text-3xl font-extrabold tracking-tight text-white md:text-4xl">
          Progress &amp; Analytics
        </h1>

        <p className="text-slate-400 text-sm leading-relaxed max-w-2xl">
          Track your quiz performance, learning progress, and attention
          metrics across all subjects.
        </p>
      </div>

      {/* API error */}
      {error && (
        <div
          role="alert"
          className="rounded-2xl bg-rose-500/10 border border-rose-500/20 p-4 text-sm text-rose-400"
        >
          {error}
        </div>
      )}

      {/* Summary cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-md">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
            Curriculum Progress
          </p>

          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">
              {completionPercentage}%
            </span>

            <span className="text-xs text-slate-400">
              ({completedDistinct.size} / {totalLessons} units)
            </span>
          </div>
        </div>

        <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-md">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
            Total Quiz Attempts
          </p>

          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">
              {totalAttempts}
            </span>

            <span className="text-xs text-slate-400">
              assessments submitted
            </span>
          </div>
        </div>

        <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-md">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
            Avg Accuracy Score
          </p>

          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">
              {scores.length > 0 ? `${avgScore}%` : '—'}
            </span>

            <span className="text-xs text-slate-400">
              correct answers
            </span>
          </div>
        </div>

        <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-md">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
            Avg Attention Metric
          </p>

          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-extrabold text-white">
              {avgAttention === null ? '—' : `${avgAttention}%`}
            </span>

            <span className="text-xs text-teal-400">
              {avgAttention === null ? 'No data recorded' : 'focus index'}
            </span>
          </div>
        </div>
      </div>

      {/* Empty state */}
      {totalAttempts === 0 ? (
        <div className="glass-panel rounded-3xl p-8 border border-slate-900 shadow-md text-center py-12 space-y-4">
          <div className="text-5xl">📈</div>

          <h3 className="text-lg font-bold text-white">
            No Analytics Available Yet
          </h3>

          <p className="text-sm text-slate-400 max-w-sm mx-auto leading-relaxed">
            Progress metrics and graphs will appear after you complete
            your first lesson assessment quiz.
          </p>

          <Link
            to="/subjects"
            className="inline-flex px-5 py-2.5 rounded-xl bg-indigo-500 hover:bg-indigo-600 text-white font-semibold text-xs shadow-md transition-all"
          >
            Begin First Lesson
          </Link>
        </div>
      ) : (
        <>
          {/* Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Historical performance */}
            <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-lg space-y-4">
              <div>
                <h3 className="text-base font-bold text-white">
                  Historical Performance Calibration
                </h3>

                <p className="text-xs text-slate-500">
                  Quiz accuracy and available attention measurements
                  per attempt.
                </p>
              </div>

              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart
                    data={lineChartData}
                    margin={{
                      top: 10,
                      right: 10,
                      left: -20,
                      bottom: 0,
                    }}
                  >
                    <CartesianGrid
                      strokeDasharray="3 3"
                      stroke="#1e293b"
                      opacity={0.3}
                    />

                    <XAxis
                      dataKey="attempt"
                      stroke="#475569"
                      fontSize={10}
                      tickLine={false}
                    />

                    <YAxis
                      stroke="#475569"
                      fontSize={10}
                      tickLine={false}
                      domain={[0, 100]}
                    />

                    <Tooltip contentStyle={tooltipStyle} />

                    <Legend
                      verticalAlign="top"
                      height={36}
                      iconType="circle"
                      wrapperStyle={{ fontSize: '11px' }}
                    />

                    <Line
                      type="monotone"
                      dataKey="score"
                      stroke="#6366f1"
                      strokeWidth={3}
                      name="Quiz Accuracy %"
                      connectNulls={false}
                      dot={{ r: 4 }}
                    />

                    <Line
                      type="monotone"
                      dataKey="attention"
                      stroke="#14b8a6"
                      strokeWidth={2}
                      name="Attention Index %"
                      strokeDasharray="4 4"
                      connectNulls={false}
                      dot={{ r: 3 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Competency by lesson */}
            <div className="glass-panel rounded-3xl p-6 border border-slate-900 shadow-lg space-y-4">
              <div>
                <h3 className="text-base font-bold text-white">
                  Competency by Lesson
                </h3>

                <p className="text-xs text-slate-500">
                  Highest recorded quiz scores and average available
                  attention measurements by lesson.
                </p>
              </div>

              <div className="h-72">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={topicAggregate}
                    margin={{
                      top: 10,
                      right: 10,
                      left: -20,
                      bottom: 0,
                    }}
                  >
                    <CartesianGrid
                      strokeDasharray="3 3"
                      stroke="#1e293b"
                      opacity={0.3}
                    />

                    <XAxis
                      dataKey="name"
                      stroke="#475569"
                      fontSize={9}
                      tickLine={false}
                      tickFormatter={(name) =>
                        String(name).split(' ')[0]
                      }
                    />

                    <YAxis
                      stroke="#475569"
                      fontSize={10}
                      tickLine={false}
                      domain={[0, 100]}
                    />

                    <Tooltip contentStyle={tooltipStyle} />

                    <Legend
                      verticalAlign="top"
                      height={36}
                      iconType="circle"
                      wrapperStyle={{ fontSize: '11px' }}
                    />

                    <Bar
                      dataKey="score"
                      fill="#4f46e5"
                      radius={[4, 4, 0, 0]}
                      name="Highest Quiz Score %"
                      maxBarSize={40}
                      isAnimationActive={false}
                    />

                    <Bar
                      dataKey="attention"
                      fill="#2dd4bf"
                      radius={[4, 4, 0, 0]}
                      name="Avg Attention %"
                      maxBarSize={40}
                      isAnimationActive={false}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Assessment history */}
          <div className="glass-panel rounded-3xl border border-slate-900 shadow-lg overflow-hidden">
            <div className="p-6 border-b border-slate-900">
              <h3 className="text-base font-bold text-white">
                Curriculum Attempts Log
              </h3>

              <p className="text-xs text-slate-500 mt-1">
                Records of quiz submissions and available attention
                indicators.
              </p>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="bg-slate-900/50 text-slate-400 font-semibold tracking-wider uppercase border-b border-slate-900">
                    <th className="py-4 px-6">Lesson Module</th>
                    <th className="py-4 px-6">Difficulty</th>
                    <th className="py-4 px-6">Quiz Score</th>
                    <th className="py-4 px-6">Attention Metric</th>
                    <th className="py-4 px-6">Duration</th>
                    <th className="py-4 px-6">Sync Status</th>
                  </tr>
                </thead>

                <tbody className="divide-y divide-slate-900/80">
                  {[...progress].reverse().map((item, index) => {
                    const lessonId = getLessonId(item)

                    const matchedLesson = lessons.find(
                      (lesson) =>
                        String(lesson.id) === String(lessonId)
                    )

                    const difficulty = getDifficulty(item)
                    const score = getQuizScore(item)
                    const attention = getAttentionScore(item)

                    const attentionIsValid =
                      attention !== null &&
                      attention >= 0 &&
                      attention <= 1

                    return (
                      <tr
                        key={item.id ?? `${lessonId}-${index}`}
                        className="hover:bg-slate-900/10 transition-colors"
                      >
                        <td className="py-4 px-6 font-bold text-slate-200">
                          {matchedLesson
                            ? getLessonTitle(matchedLesson)
                            : item?.lesson?.title ??
                              item?.lesson_title ??
                              'Unknown Lesson'}
                        </td>

                        <td className="py-4 px-6">
                          <span
                            className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                              difficulty === 'EASY'
                                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                                : difficulty === 'MEDIUM'
                                  ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                                  : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                            }`}
                          >
                            {difficulty}
                          </span>
                        </td>

                        <td className="py-4 px-6 font-semibold text-white">
                          {score === null
                            ? '—'
                            : `${Math.round(score)}%`}
                        </td>

                        <td className="py-4 px-6 font-semibold text-teal-400">
                          {attentionIsValid
                            ? `${Math.round(attention * 100)}%`
                            : 'Not recorded'}
                        </td>

                        <td className="py-4 px-6 text-slate-400">
                          {item?.response_time ??
                            item?.duration ??
                            0}
                          s
                        </td>

                        <td className="py-4 px-6 text-slate-500 font-medium">
                          {item?.id != null
                            ? '✓ Synced'
                            : 'Pending'}
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  )
}