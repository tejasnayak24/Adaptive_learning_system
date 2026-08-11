import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { lessonService } from '../services/lessonService'
import { progressService } from '../services/progressService'

export default function Subjects() {
  const { user } = useAuth()
  const [lessons, setLessons] = useState([])
  const [progress, setProgress] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [selectedSubject, setSelectedSubject] = useState('Science')

 useEffect(() => {
  async function loadData() {
    try {
      const lessonsRes = await lessonService.getLessons()

      if (lessonsRes.success) {
        setLessons(lessonsRes.data)
      }
    } catch (err) {
      setError(err.message || 'Failed to load lessons')
    }

    try {
      const studentId = user?.id ?? user?.sub

      if (studentId) {
        const progressRes = await progressService.getStudentProgress(studentId)

        if (progressRes.success) {
          setProgress(progressRes.data)
        }
      }
    } catch (err) {
      console.warn('Progress could not be loaded:', err)
    } finally {
      setLoading(false)
    }
  }

  loadData()
}, [user?.id, user?.sub])

  if (loading) {
    return (
      <div className="space-y-6 animate-pulse">
        <div className="h-10 w-1/4 bg-slate-800 rounded-xl"></div>
        <div className="h-4 w-1/2 bg-slate-800 rounded-lg"></div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pt-6">
          {[...Array(6)].map((_, i) => (
            <div key={i} className="h-64 bg-slate-800 rounded-3xl"></div>
          ))}
        </div>
      </div>
    )
  }

  // Helper to find highest score for a lesson
  const getLessonStats = (lessonId) => {
    const attempts = progress.filter(p => p.lesson_id === lessonId)
    if (attempts.length === 0) return null

    const completed = attempts.some(a => a.completed)
    const highestScore = Math.max(...attempts.map(a => a.quiz_score))
    const highestDifficulty = attempts.sort((a, b) => {
      const order = { EASY: 1, MEDIUM: 2, HARD: 3 }
      return order[b.difficulty.toUpperCase()] - order[a.difficulty.toUpperCase()]
    })[0]?.difficulty

    return {
      completed,
      highestScore,
      difficulty: highestDifficulty,
      attempts: attempts.length
    }
  }

  // Group lessons by topic
  const groupedLessons = lessons.reduce((acc, lesson) => {
    const topic = lesson.topic || 'General Science'
    if (!acc[topic]) {
      acc[topic] = []
    }
    acc[topic].push(lesson)
    return acc
  }, {})

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="space-y-1.5">
        <h1 className="font-display text-3xl font-extrabold tracking-tight text-white md:text-4xl">
          Curriculum Browser
        </h1>
        <p className="text-slate-400 text-sm leading-relaxed max-w-2xl">
          Select a subject and explore topic modules. Aegis automatically scales assessment difficulty based on performance.
        </p>
      </div>

      {error && (
        <div className="rounded-2xl bg-rose-500/10 border border-rose-500/20 p-4 text-sm text-rose-400">
          {error}
        </div>
      )}

      {/* Subject Filter Tabs */}
      <div className="flex flex-wrap gap-3 pb-2 border-b border-slate-900">
        {['Mathematics', 'Science', 'Social Science', 'English'].map((sub) => (
          <button
            key={sub}
            onClick={() => setSelectedSubject(sub)}
            className={`px-5 py-2.5 rounded-xl text-xs font-bold border transition-all duration-200 ${
              selectedSubject === sub
                ? 'bg-indigo-500 border-indigo-500 text-white shadow-md shadow-indigo-500/20'
                : 'bg-slate-950 border-slate-900 hover:border-slate-800 text-slate-400 hover:text-slate-200'
            }`}
          >
            {sub}
          </button>
        ))}
      </div>

      {selectedSubject !== 'Science' ? (
        <div className="glass-panel rounded-3xl p-12 border border-slate-900 shadow-md text-center py-16 space-y-4">
          <div className="text-5xl">📚</div>
          <h3 className="text-lg font-bold text-white">No Lessons Available</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto leading-relaxed">
            Curriculum content for <span className="font-semibold text-white">{selectedSubject}</span> is currently under calibration. Please check back soon or switch to <span className="text-indigo-400 font-semibold">Science</span>.
          </p>
        </div>
      ) : Object.keys(groupedLessons).length === 0 ? (
        <div className="glass-panel rounded-3xl p-12 border border-slate-900 shadow-md text-center py-16 space-y-4">
          <div className="text-5xl">🍃</div>
          <h3 className="text-lg font-bold text-white">Curriculum Empty</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto leading-relaxed">
            No Science lessons were found in the database. Please verify your seed configuration.
          </p>
        </div>
      ) : (
        <div className="space-y-12">
          {Object.entries(groupedLessons).map(([topicName, topicLessons]) => (
            <div key={topicName} className="space-y-6">
              {/* Topic Divider */}
              <div className="flex items-center gap-4">
                <h2 className="font-display text-xl font-bold text-white shrink-0 tracking-wide">
                  {topicName}
                </h2>
                <div className="h-px bg-slate-800/80 w-full"></div>
              </div>

              {/* Grid of lessons */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {topicLessons.map((lesson) => {
                  const stats = getLessonStats(lesson.id)

                  return (
                    <div
                      key={lesson.id}
                      className="glass-panel glass-panel-hover rounded-3xl p-6 border border-slate-900 shadow-md flex flex-col justify-between h-64"
                    >
                      <div className="space-y-3">
                        {/* Topic Category */}
                        <div className="flex items-center justify-between">
                          <span className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider">
                            {selectedSubject.toUpperCase()} CURRICULUM
                          </span>

                          {stats?.completed ? (
                            <span className="inline-flex items-center gap-1 px-2 py-0.5 text-[9px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-full">
                              <svg className="h-2.5 w-2.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" />
                              </svg>
                              Completed
                            </span>
                          ) : stats?.attempts > 0 ? (
                            <span className="inline-flex items-center gap-1 px-2 py-0.5 text-[9px] font-bold bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded-full">
                              In Progress
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1 px-2 py-0.5 text-[9px] font-bold bg-slate-800 text-slate-400 rounded-full">
                              Not Started
                            </span>
                          )}
                        </div>

                        {/* Title */}
                        <h3 className="text-lg font-bold text-white leading-snug line-clamp-2">
                          {lesson.title}
                        </h3>

                        {/* Content Preview Snippet */}
                        <p className="text-xs text-slate-400 line-clamp-3 leading-relaxed">
                          {lesson.content}
                        </p>
                      </div>

                      {/* Stats & CTA */}
                      <div className="border-t border-slate-800/60 pt-4 flex items-center justify-between">
                        {stats ? (
                          <div className="space-y-1">
                            <p className="text-[9px] font-bold text-slate-500 uppercase tracking-wider">
                              Best score
                            </p>
                            <div className="flex items-center gap-2 text-xs">
                              <span className="font-extrabold text-white">{stats.highestScore}%</span>
                              <span className="text-slate-600">&bull;</span>
                              <span className="text-[10px] font-semibold bg-slate-900 px-1.5 py-0.5 rounded text-slate-400">
                                {stats.difficulty}
                              </span>
                            </div>
                          </div>
                        ) : (
                          <div className="space-y-1">
                            <p className="text-[9px] font-bold text-slate-500 uppercase tracking-wider">
                              Pacing
                            </p>
                            <p className="text-xs text-slate-400">Self-calibrating</p>
                          </div>
                        )}

                        <Link
                          to={`/lesson/${lesson.id}`}
                          state={{ subject: selectedSubject }}
                          className="inline-flex px-4 py-2 rounded-xl bg-slate-900 hover:bg-indigo-600 border border-slate-800 hover:border-indigo-600 text-xs font-semibold text-slate-200 hover:text-white transition-all active:scale-[0.97]"
                        >
                          {stats?.completed ? 'Review Material' : 'Start Reading'}
                        </Link>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
